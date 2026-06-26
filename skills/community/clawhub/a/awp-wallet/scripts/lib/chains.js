import * as viemChains from "viem/chains"
import { createPublicClient, http, defineChain, erc20Abi } from "viem"
import { readFileSync, existsSync } from "node:fs"
import { join } from "node:path"
import { WALLET_DIR } from "./paths.js"

// chainId -> Chain mapping (viem built-in chains)
const BUILTIN = new Map()
for (const c of Object.values(viemChains)) {
  if (c?.id) BUILTIN.set(c.id, c)
}

// Name alias mapping
const NAME_TO_ID = new Map()
for (const c of BUILTIN.values()) {
  NAME_TO_ID.set(c.name.toLowerCase(), c.id)
  if (c.network) NAME_TO_ID.set(c.network.toLowerCase(), c.id)
}
NAME_TO_ID.set("bsc", 56)
NAME_TO_ID.set("avax", 43114)
NAME_TO_ID.set("ftm", 250)
NAME_TO_ID.set("zksync", 324)
NAME_TO_ID.set("linea", 59144)
NAME_TO_ID.set("scroll", 534352)
NAME_TO_ID.set("mantle", 5000)
NAME_TO_ID.set("blast", 81457)
NAME_TO_ID.set("celo", 42220)

const CUSTOM = new Map()

// --- Config loading (with graceful error handling) ---
let _configCache = null
const CONFIG_PATH = join(WALLET_DIR, "config.json")

export function loadConfig() {
  if (_configCache) return _configCache
  try {
    _configCache = JSON.parse(readFileSync(CONFIG_PATH, "utf8"))
    return _configCache
  } catch (err) {
    if (err.code === "ENOENT")
      throw new Error("Config not found. Run 'awp-wallet init' first.")
    if (err instanceof SyntaxError)
      throw new Error("Config file corrupted. Delete and re-run 'awp-wallet init'.")
    throw err
  }
}

// --- Chain ID resolution ---
export function resolveChainId(nameOrId) {
  if (typeof nameOrId === "number") return nameOrId
  const s = String(nameOrId).toLowerCase()
  // Numeric string: "56" -> 56
  const num = Number(s)
  if (!isNaN(num) && num > 0) return num
  // Name lookup
  if (NAME_TO_ID.has(s)) return NAME_TO_ID.get(s)
  // Config lookup: "base-sepolia" -> config.chains["base-sepolia"].chainId
  try {
    const cfg = loadConfig()
    if (cfg.chains?.[s]?.chainId) return cfg.chains[s].chainId
  } catch { /* config not available yet */ }
  throw new Error(`Unknown chain: "${nameOrId}". Use --chain <name|id> or --rpc-url.`)
}

export function viemChain(chainId, rpcUrl, nativeCurrency) {
  chainId = Number(chainId)
  // If user provides a custom RPC URL, always override (even for known chains)
  if (rpcUrl) {
    const base = BUILTIN.get(chainId)
    const c = defineChain({
      id: chainId,
      name: base?.name || `Chain ${chainId}`,
      nativeCurrency: nativeCurrency || base?.nativeCurrency || { name: "ETH", symbol: "ETH", decimals: 18 },
      rpcUrls: { default: { http: [rpcUrl] } },
    })
    CUSTOM.set(chainId, c)
    return c
  }
  if (CUSTOM.has(chainId)) return CUSTOM.get(chainId)
  if (BUILTIN.has(chainId)) return BUILTIN.get(chainId)
  throw new Error(`Chain ${chainId} unknown. Provide --rpc-url or add to config.`)
}

// --- Load custom chains from config ---
function loadCustomChains() {
  try {
    const cfg = loadConfig()
    for (const cc of cfg.customChains || []) {
      if (!cc.chainId || !cc.rpcUrl) continue
      const c = defineChain({
        id: cc.chainId,
        name: cc.name || `Chain ${cc.chainId}`,
        nativeCurrency: cc.nativeCurrency || { name: "ETH", symbol: "ETH", decimals: 18 },
        rpcUrls: { default: { http: [cc.rpcUrl] } },
      })
      CUSTOM.set(cc.chainId, c)
      if (cc.name) NAME_TO_ID.set(cc.name.toLowerCase(), cc.chainId)
    }
  } catch { /* config doesn't exist yet (before init) — skip */ }
}
loadCustomChains()

// --- Look up chain config by name (with chainId fallback) ---
export function chainConfig(nameOrId) {
  const cfg = loadConfig()
  // Direct name match (most common path: "bsc" -> cfg.chains["bsc"])
  const name = String(nameOrId).toLowerCase()
  if (cfg.chains?.[name]) return cfg.chains[name]
  // Numeric chainId fallback: find the entry whose entry.chainId matches
  const id = Number(nameOrId)
  if (!isNaN(id)) {
    for (const [, entry] of Object.entries(cfg.chains || {})) {
      if (entry.chainId === id) return entry
    }
  }
  return null  // Tier 1 chains have no config — direct-tx still works
}

// --- RPC URL resolution ---
// Reverse lookup: numeric chainId -> config chain name
function chainIdToName(chainId) {
  const cfg = loadConfig()
  for (const [name, entry] of Object.entries(cfg.chains || {})) {
    if (entry.chainId === chainId) return name
  }
  return null
}

export function getRpcUrl(chainNameOrId) {
  const cfg = loadConfig()
  const name = String(chainNameOrId).toLowerCase()
  // Direct name match (fast path: "bsc" -> cfg.rpcOverrides["bsc"])
  let override = cfg.rpcOverrides?.[name]
  // Numeric chainId -> reverse lookup name, then check rpcOverrides
  if (!override) {
    const id = Number(chainNameOrId)
    if (!isNaN(id)) {
      const resolved = chainIdToName(id)
      if (resolved) override = cfg.rpcOverrides?.[resolved]
    }
  }
  if (override) {
    const url = override.replace(/\{(\w+)\}/g, (_, k) => {
      const val = process.env[k]
      if (!val) throw new Error(`Environment variable "${k}" required for RPC URL is not set.`)
      return val
    })
    return url
  }
  return viemChain(resolveChainId(chainNameOrId)).rpcUrls.default.http[0]
}

const _clientCache = new Map()

export function publicClient(chainNameOrId) {
  const chainId = resolveChainId(chainNameOrId)
  if (!_clientCache.has(chainId)) {
    _clientCache.set(chainId, createPublicClient({
      chain: viemChain(chainId),
      transport: http(getRpcUrl(chainNameOrId)),
    }))
  }
  return _clientCache.get(chainId)
}

// --- Native currency symbol resolution ---
export function nativeSymbol(chain) {
  try { return viemChain(resolveChainId(chain)).nativeCurrency.symbol }
  catch { return "native" }
}

// --- Dual-mode token resolution ---
export async function tokenInfo(chain, symbolOrAddress) {
  const chainId = resolveChainId(chain)
  // Symbol (e.g. "USDC") -> look up from config.json (keyed by chain name)
  if (!/^0x/i.test(symbolOrAddress)) {
    const cfg = chainConfig(chain)
    const entry = cfg?.tokens?.[symbolOrAddress.toUpperCase()]
    if (entry) return { symbol: symbolOrAddress.toUpperCase(), ...entry }
    throw new Error(`Token "${symbolOrAddress}" not configured for chain "${chain}". Use contract address: --asset 0x...`)
  }
  // Contract address -> on-chain query (parallel decimals + symbol)
  const client = publicClient(chainId)
  const [decimals, symbol] = await Promise.all([
    client.readContract({ address: symbolOrAddress, abi: erc20Abi, functionName: "decimals" }).then(Number),
    client.readContract({ address: symbolOrAddress, abi: erc20Abi, functionName: "symbol" }).catch(() => "UNKNOWN"),
  ])
  return { symbol, address: symbolOrAddress, decimals }
}
