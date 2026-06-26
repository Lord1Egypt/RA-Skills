import { Wallet, encryptKeystoreJson } from "ethers"
import { privateKeyToAccount } from "viem/accounts"
import { createHash, createCipheriv, createDecipheriv, randomBytes, scryptSync } from "node:crypto"
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, unlinkSync } from "node:fs"
import { join, dirname } from "node:path"
import { fileURLToPath } from "node:url"
import { WALLET_DIR, WALLETS_DIR, registerWallet } from "./paths.js"

const __dirname = dirname(fileURLToPath(import.meta.url))
const KS_PATH = join(WALLET_DIR, "keystore.enc")
const META_PATH = join(WALLET_DIR, "meta.json")
const CACHE_DIR = join(WALLET_DIR, ".signer-cache")
const CACHE_SALT_PATH = join(CACHE_DIR, ".salt")
const AUTO_PW_PATH = join(WALLET_DIR, ".wallet-password")

function getPassword() {
  // 1. Explicit env var (Password mode — agent manages the password)
  if (process.env.WALLET_PASSWORD) return process.env.WALLET_PASSWORD

  // 2. Auto-managed password file (Default mode — passwordless UX)
  if (existsSync(AUTO_PW_PATH)) return readFileSync(AUTO_PW_PATH, "utf8").trim()

  // 3. First-time init — generate and persist
  const pw = randomBytes(32).toString("base64")
  if (!existsSync(WALLET_DIR)) mkdirSync(WALLET_DIR, { recursive: true, mode: 0o700 })
  writeFileSync(AUTO_PW_PATH, pw, { mode: 0o600 })
  return pw
}

// --- Shared helpers ---

// Decrypt keystore with error wrapping (used by loadSigner, unlockAndCache, changePassword, exportMnemonic)
function decryptKeystore(password) {
  const json = readFileSync(KS_PATH, "utf8")
  try { return Wallet.fromEncryptedJsonSync(json, password || getPassword()) }
  catch (e) {
    if ((e.message || "").toLowerCase().match(/password|decrypt|incorrect/))
      throw new Error("Wrong password — decryption failed.")
    throw e
  }
}

// Persist new wallet to disk (used by initWallet, importWallet)
async function persistNewWallet(wallet, status) {
  const pw = getPassword()
  const json = await encryptKeystoreJson(wallet, pw, { scrypt: { N: 262144 } })
  // Provision wallet directory with 0o700 on all parent dirs
  if (!existsSync(WALLETS_DIR)) mkdirSync(WALLETS_DIR, { recursive: true, mode: 0o700 })
  if (!existsSync(WALLET_DIR)) mkdirSync(WALLET_DIR, { mode: 0o700 })
  mkdirSync(join(WALLET_DIR, "sessions"), { recursive: true, mode: 0o700 })
  writeFileSync(KS_PATH, json, { mode: 0o600 })
  writeFileSync(META_PATH, JSON.stringify({ address: wallet.address, smartAccounts: {} }), { mode: 0o600 })
  // Copy default config if not present
  const configPath = join(WALLET_DIR, "config.json")
  if (!existsSync(configPath)) {
    const defaultConfig = join(__dirname, "..", "..", "assets", "default-config.json")
    if (existsSync(defaultConfig)) writeFileSync(configPath, readFileSync(defaultConfig), { mode: 0o600 })
  }
  // Generate session secret if not present
  const secretPath = join(WALLET_DIR, ".session-secret")
  if (!existsSync(secretPath)) {
    writeFileSync(secretPath, randomBytes(32).toString("hex"), { mode: 0o600 })
  }
  // Register in wallet registry
  registerWallet(wallet.address)
  _metaCache = null  // Reset cache so subsequent reads pick up new meta

  const result = { status, address: wallet.address }
  result.passwordMode = process.env.WALLET_PASSWORD ? "explicit" : "auto"
  return result
}

// --- AES-256-GCM signer cache with scrypt KDF ---

// Cache the derived AES key per-process (password doesn't change mid-process)
let _aesKeyCache = null
let _aesKeyCachePassword = null

function deriveAesKey(password) {
  if (_aesKeyCache && _aesKeyCachePassword === password) return _aesKeyCache

  let salt
  if (existsSync(CACHE_SALT_PATH)) {
    salt = readFileSync(CACHE_SALT_PATH)
  } else {
    salt = randomBytes(32)
    if (!existsSync(CACHE_DIR)) mkdirSync(CACHE_DIR, { mode: 0o700 })
    writeFileSync(CACHE_SALT_PATH, salt, { mode: 0o600 })
  }
  _aesKeyCache = scryptSync(password, salt, 32, { N: 16384, r: 8, p: 1 })
  _aesKeyCachePassword = password
  return _aesKeyCache
}

function writeSignerCache(sessionId, privateKey, expiresISO) {
  const key = deriveAesKey(getPassword())
  const iv = randomBytes(12)
  const cipher = createCipheriv("aes-256-gcm", key, iv)
  const plaintext = JSON.stringify({ privateKey, expires: expiresISO })
  const encrypted = Buffer.concat([cipher.update(plaintext, "utf8"), cipher.final()])
  const tag = cipher.getAuthTag()
  const blob = Buffer.concat([iv, tag, encrypted])
  if (!existsSync(CACHE_DIR)) mkdirSync(CACHE_DIR, { mode: 0o700 })
  writeFileSync(join(CACHE_DIR, sessionId + ".key"), blob, { mode: 0o600 })
}

function readSignerCache() {
  if (!existsSync(CACHE_DIR)) return null
  let password
  try { password = getPassword() } catch { return null }

  const key = deriveAesKey(password)
  const files = readdirSync(CACHE_DIR).filter(f => f.endsWith(".key"))
  for (const f of files) {
    try {
      const blob = readFileSync(join(CACHE_DIR, f))
      const iv = blob.subarray(0, 12)
      const tag = blob.subarray(12, 28)
      const ciphertext = blob.subarray(28)
      const decipher = createDecipheriv("aes-256-gcm", key, iv)
      decipher.setAuthTag(tag)
      const plaintext = Buffer.concat([decipher.update(ciphertext), decipher.final()])
      const data = JSON.parse(plaintext.toString("utf8"))
      if (new Date(data.expires) > new Date()) {
        return privateKeyToAccount(data.privateKey)
      }
      try { unlinkSync(join(CACHE_DIR, f)) } catch {}
    } catch {
      try { unlinkSync(join(CACHE_DIR, f)) } catch {}
    }
  }
  return null
}

// --- Exports ---

export function loadSigner() {
  const cached = readSignerCache()
  if (cached) return { account: cached }

  const w = decryptKeystore()
  return { account: privateKeyToAccount(w.privateKey) }
}

export function unlockAndCache(sessionId, expiresISO) {
  const w = decryptKeystore()
  writeSignerCache(sessionId, w.privateKey, expiresISO)
  return { account: privateKeyToAccount(w.privateKey) }
}

export function clearSignerCache() {
  if (!existsSync(CACHE_DIR)) return
  for (const f of readdirSync(CACHE_DIR)) {
    try { unlinkSync(join(CACHE_DIR, f)) } catch {}
  }
  _aesKeyCache = null
  _aesKeyCachePassword = null
}

export async function initWallet() {
  if (existsSync(KS_PATH)) throw new Error("Wallet already exists.")
  return persistNewWallet(Wallet.createRandom(), "created")
}

export async function importWallet(mnemonic) {
  if (existsSync(KS_PATH)) throw new Error("Wallet already exists.")
  return persistNewWallet(Wallet.fromPhrase(mnemonic.trim()), "imported")
}

export async function changePassword() {
  const newPw = process.env.NEW_WALLET_PASSWORD
  if (!newPw) throw new Error("NEW_WALLET_PASSWORD environment variable required.")
  const w = decryptKeystore()
  const newJson = await encryptKeystoreJson(w, newPw, { scrypt: { N: 262144 } })
  writeFileSync(KS_PATH, newJson, { mode: 0o600 })
  // Update auto-managed password file if it exists
  if (existsSync(AUTO_PW_PATH)) writeFileSync(AUTO_PW_PATH, newPw, { mode: 0o600 })
  clearSignerCache()
  return { status: "password_changed" }
}

export function exportMnemonic() {
  // Security: export requires explicit WALLET_PASSWORD — auto-managed password cannot export seed
  if (!process.env.WALLET_PASSWORD) throw new Error("WALLET_PASSWORD required for export. Auto-managed wallets cannot export seed phrases for security.")
  const w = decryptKeystore()
  if (!w.mnemonic) throw new Error("Wallet has no mnemonic (imported from private key).")
  return {
    mnemonic: w.mnemonic.phrase,
    warning: "Store this offline. Anyone with these words has full access to your funds."
  }
}

// --- Meta.json with in-process cache ---
let _metaCache = null

function loadMeta() {
  if (_metaCache) return _metaCache
  try {
    _metaCache = JSON.parse(readFileSync(META_PATH, "utf8"))
    return _metaCache
  } catch (err) {
    if (err.code === "ENOENT") throw new Error("No wallet found. Run 'init' first.")
    if (err instanceof SyntaxError) throw new Error("Wallet metadata corrupted. Re-import with 'import --mnemonic'.")
    throw err
  }
}

export function getAddress(type = "eoa", chainId) {
  const meta = loadMeta()
  if (type === "smart") return meta.smartAccounts?.[String(chainId)] || null
  return meta.address
}

export function saveSmartAccountAddress(chainId, addr) {
  const meta = loadMeta()
  if (meta.smartAccounts?.[String(chainId)] === addr) return
  if (!meta.smartAccounts) meta.smartAccounts = {}
  meta.smartAccounts[String(chainId)] = addr
  writeFileSync(META_PATH, JSON.stringify(meta), { mode: 0o600 })
  _metaCache = meta // update cache
}

export function getReceiveInfo(chainId) {
  return {
    eoaAddress: getAddress("eoa"),
    smartAccountAddress: chainId ? getAddress("smart", chainId) : null,
    note: "Send to EOA address for direct transactions. Smart Account address is for gasless operations (if deployed)."
  }
}
