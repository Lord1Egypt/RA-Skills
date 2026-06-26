import { join } from "node:path"
import { existsSync, readFileSync, writeFileSync, mkdirSync, renameSync } from "node:fs"

const BASE_DIR = join(process.env.HOME, ".openclaw-wallet")
const WALLETS_DIR = join(BASE_DIR, "wallets")
const REGISTRY_PATH = join(BASE_DIR, "wallets.json")

// Wallet ID resolution priority:
// 1. AWP_SESSION_ID — per-session isolation (most granular)
// 2. AWP_AGENT_ID  — per-agent isolation (shared across sessions)
// 3. "default"     — no isolation (all agents share one wallet)
function resolveWalletId() {
  const raw = process.env.AWP_SESSION_ID || process.env.AWP_AGENT_ID || "default"
  if (!/^[a-zA-Z0-9_-]{1,128}$/.test(raw))
    throw new Error(`Invalid wallet ID: "${raw}". Only alphanumeric, hyphen, underscore allowed.`)
  return raw
}

export const walletId = resolveWalletId()

// Backward compat: migrate old root-level wallet to wallets/default/
if (existsSync(join(BASE_DIR, "keystore.enc")) && !existsSync(join(WALLETS_DIR, "default", "keystore.enc"))) {
  mkdirSync(WALLETS_DIR, { recursive: true, mode: 0o700 })
  const defaultDir = join(WALLETS_DIR, "default")
  mkdirSync(defaultDir, { recursive: true, mode: 0o700 })
  for (const f of ["keystore.enc", "meta.json", ".wallet-password", ".session-secret", "tx-log.jsonl", "config.json"]) {
    const src = join(BASE_DIR, f)
    if (existsSync(src)) {
      writeFileSync(join(defaultDir, f), readFileSync(src), { mode: 0o600 })
      renameSync(src, src + ".migrated")
    }
  }
  for (const d of [".signer-cache", "sessions"]) {
    const src = join(BASE_DIR, d)
    const dst = join(defaultDir, d)
    if (existsSync(src) && !existsSync(dst)) {
      renameSync(src, dst)
    }
  }
}

// Wallet directory for current context
export const WALLET_DIR = join(WALLETS_DIR, walletId)

// Register wallet in registry
export function registerWallet(address) {
  let registry = {}
  if (existsSync(REGISTRY_PATH)) {
    try { registry = JSON.parse(readFileSync(REGISTRY_PATH, "utf8")) } catch {}
  }
  const source = process.env.AWP_SESSION_ID ? "session" : (process.env.AWP_AGENT_ID ? "agent" : "default")
  registry[walletId] = {
    address,
    createdAt: registry[walletId]?.createdAt || new Date().toISOString(),
    lastUsed: new Date().toISOString(),
    source,
  }
  if (!existsSync(WALLETS_DIR)) mkdirSync(WALLETS_DIR, { recursive: true, mode: 0o700 })
  // Atomic write: write to tmp then rename (prevents corruption on crash)
  const tmp = REGISTRY_PATH + ".tmp." + process.pid
  writeFileSync(tmp, JSON.stringify(registry, null, 2), { mode: 0o600 })
  renameSync(tmp, REGISTRY_PATH)
}

// List all wallets
export function listWallets() {
  if (!existsSync(REGISTRY_PATH)) return {}
  try { return JSON.parse(readFileSync(REGISTRY_PATH, "utf8")) } catch { return {} }
}

export { BASE_DIR, WALLETS_DIR }
