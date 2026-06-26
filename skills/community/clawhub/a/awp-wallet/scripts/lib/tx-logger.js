import { createHash } from "node:crypto"
import { readFileSync, appendFileSync, existsSync } from "node:fs"
import { join } from "node:path"
import { WALLET_DIR } from "./paths.js"

const LOG_PATH = join(WALLET_DIR, "tx-log.jsonl")

export function logTransaction(data) {
  // Read the last hash to maintain chain continuity
  let prevHash = "0"
  if (existsSync(LOG_PATH)) {
    const lines = readFileSync(LOG_PATH, "utf8").trim().split("\n").filter(Boolean)
    if (lines.length > 0) {
      const last = JSON.parse(lines[lines.length - 1])
      prevHash = last._hash
    }
  }
  // Build content (timestamp + data), then hash it
  const content = { timestamp: new Date().toISOString(), ...data }
  const hashInput = prevHash + JSON.stringify(content)
  const _hash = createHash("sha256").update(hashInput).digest("hex")
  const entry = { ...content, _prevHash: prevHash, _hash }
  appendFileSync(LOG_PATH, JSON.stringify(entry) + "\n", { mode: 0o600 })
  return entry
}

export function getHistory(chain, limit = 50) {
  if (!existsSync(LOG_PATH)) return []  // No logs yet — normal state for a new wallet
  const lines = readFileSync(LOG_PATH, "utf8").trim().split("\n").filter(Boolean)
  let entries = lines.map(l => JSON.parse(l))
  if (chain) {
    // Support filtering by: config name ("bsc"), display name ("BNB Smart Chain"), or numeric chainId (56)
    const numChain = Number(chain)
    entries = entries.filter(e =>
      e.chain === chain ||
      e.chainId === chain ||
      (!isNaN(numChain) && e.chainId === numChain)
    )
  }
  return entries.slice(-limit)
}

export function verifyIntegrity() {
  if (!existsSync(LOG_PATH)) return { valid: true, entries: 0 }
  const lines = readFileSync(LOG_PATH, "utf8").trim().split("\n").filter(Boolean)
  let prevHash = "0"
  for (const line of lines) {
    const entry = JSON.parse(line)
    const { _prevHash: _, _hash: __, ...content } = entry
    const expected = createHash("sha256")
      .update(prevHash + JSON.stringify(content))
      .digest("hex")
    if (entry._hash !== expected) return { valid: false, brokenAt: entry.timestamp }
    prevHash = entry._hash
  }
  return { valid: true, entries: lines.length }
}
