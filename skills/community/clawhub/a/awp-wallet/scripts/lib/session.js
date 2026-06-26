import { randomBytes, createHmac, timingSafeEqual } from "node:crypto"
import { readFileSync, writeFileSync, readdirSync, unlinkSync, existsSync, mkdirSync } from "node:fs"
import { join } from "node:path"
import { unlockAndCache, clearSignerCache } from "./keystore.js"
import { WALLET_DIR } from "./paths.js"
const SESSIONS_DIR = join(WALLET_DIR, "sessions")
const SECRET_PATH = join(WALLET_DIR, ".session-secret")

function getSessionSecret() {
  let hex
  try { hex = readFileSync(SECRET_PATH, "utf8").trim() }
  catch (err) {
    if (err.code === "ENOENT")
      throw new Error("Session secret not found. Run 'awp-wallet init' first.")
    throw err
  }
  const key = Buffer.from(hex, "hex")
  if (key.length !== 32) throw new Error("Session secret file is invalid (expected 64 hex chars).")
  return key
}

function signSession(data) {
  return createHmac("sha256", getSessionSecret())
    .update(JSON.stringify(data)).digest("hex")
}

export function unlockWallet(durationSec = 3600, scope = "full") {
  const id = "wlt_" + randomBytes(16).toString("hex")
  const expires = new Date(Date.now() + durationSec * 1000).toISOString()

  // Decrypt + write encrypted cache (privateKey stays internal to keystore.js)
  unlockAndCache(id, expires)

  // Ensure sessions directory exists
  if (!existsSync(SESSIONS_DIR)) mkdirSync(SESSIONS_DIR, { mode: 0o700, recursive: true })

  // Write session token + HMAC
  const data = { id, scope, created: new Date().toISOString(), expires }
  const hmac = signSession(data)
  writeFileSync(join(SESSIONS_DIR, id + ".json"),
    JSON.stringify({ ...data, _hmac: hmac }), { mode: 0o600 })

  return { sessionToken: id, expires }
}

export function validateSession(tokenId) {
  // Prevent path traversal attacks: only allow valid session token format
  if (!/^wlt_[0-9a-f]{32}$/.test(tokenId)) {
    throw new Error("Invalid or expired session token.")
  }
  const filePath = join(SESSIONS_DIR, tokenId + ".json")
  let raw
  try {
    raw = JSON.parse(readFileSync(filePath, "utf8"))
  } catch (err) {
    // File does not exist or was deleted by a concurrent lock
    throw new Error("Invalid or expired session token.")
  }
  const { _hmac, ...data } = raw
  // HMAC verification (timing-safe)
  const expected = Buffer.from(signSession(data), "hex")
  const actual = Buffer.from(_hmac, "hex")
  if (expected.length !== actual.length || !timingSafeEqual(expected, actual)) {
    throw new Error("Session token integrity check failed.")
  }
  if (new Date(data.expires) <= new Date()) {
    try { unlinkSync(filePath) } catch { /* concurrent lock may have deleted it */ }
    throw new Error("Invalid or expired session token.")
  }
  return data  // { id, scope, created, expires }
}

const SCOPE_LEVELS = { read: 1, transfer: 2, full: 3 }

export function requireScope(tokenId, needed) {
  const session = validateSession(tokenId)
  if ((SCOPE_LEVELS[session.scope] || 0) < (SCOPE_LEVELS[needed] || 0)) {
    throw new Error(`Scope '${session.scope}' insufficient; '${needed}' required.`)
  }
  return session
}

export function lockWallet() {
  // Delete all session files (.json only, to avoid deleting subdirectories or non-session files)
  if (existsSync(SESSIONS_DIR)) {
    for (const f of readdirSync(SESSIONS_DIR).filter(f => f.endsWith(".json"))) {
      try { unlinkSync(join(SESSIONS_DIR, f)) } catch { /* concurrent deletion is harmless */ }
    }
  }
  // Delete signer cache
  clearSignerCache()
  return { status: "locked" }
}
