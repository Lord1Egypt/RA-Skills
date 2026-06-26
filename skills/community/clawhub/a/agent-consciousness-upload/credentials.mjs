import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const CONFIG_DIR = path.join(os.homedir(), ".config", "agent-consciousness-upload");
const CREDENTIALS_FILE = path.join(CONFIG_DIR, "credentials.json");
const SCHEMA_VERSION = 1;

// Token expiry buffer: treat as expired 1 hour before actual expiry
const TOKEN_EXPIRY_BUFFER_MS = 60 * 60 * 1000;

/**
 * Load cached credentials from ~/.config/agent-consciousness-upload/credentials.json
 * Returns null if file doesn't exist or is expired.
 */
export async function loadCredentials() {
  try {
    await fs.access(CONFIG_DIR);
    await fs.access(CREDENTIALS_FILE);
  } catch {
    return null;
  }

  try {
    const raw = await fs.readFile(CREDENTIALS_FILE, "utf8");
    const cred = JSON.parse(raw);
    if (cred.version !== SCHEMA_VERSION) {
      // 未来版本迁移逻辑可在此处理
      return null;
    }
    return cred;
  } catch {
    return null;
  }
}

/**
 * Save credentials to disk.
 * Sets file permissions to 0600 (owner read/write only).
 */
export async function saveCredentials(data) {
  await fs.mkdir(CONFIG_DIR, { recursive: true });
  const content = JSON.stringify(
    {
      version: SCHEMA_VERSION,
      ...data,
      last_used_at: new Date().toISOString()
    },
    null,
    2
  );
  await fs.writeFile(CREDENTIALS_FILE, content, "utf8");
  // Set file permissions: owner read/write only
  try {
    await fs.chmod(CREDENTIALS_FILE, 0o600);
  } catch {
    // chmod may not be supported on non-Unix systems, ignore
  }
}

/**
 * Clear cached credentials.
 */
export async function clearCredentials() {
  try {
    await fs.unlink(CREDENTIALS_FILE);
  } catch {
    // 文件不存在时忽略
  }
}

/**
 * Get the active (non-expired) token from cache.
 * Returns null if no credentials or token is expired / about to expire.
 */
export async function getActiveToken() {
  const cred = await loadCredentials();
  if (!cred || !cred.token || !cred.expires_at) {
    return null;
  }
  const expiresAt = new Date(cred.expires_at).getTime();
  if (Date.now() + TOKEN_EXPIRY_BUFFER_MS > expiresAt) {
    return null; // expired or about to expire
  }
  return cred.token;
}

/**
 * Get the current server URL from cache.
 * Returns null if no credentials.
 */
export async function getCachedServerUrl() {
  const cred = await loadCredentials();
  return cred?.server_url || null;
}

/**
 * Get the cached skill identity (stable per-machine identifier).
 * Returns null if not yet associated.
 */
export async function getCachedEmail() {
  const cred = await loadCredentials();
  return cred?.email || null;
}

/**
 * Get full credentials (including token, user info) if valid.
 */
export async function getActiveCredentials() {
  const cred = await loadCredentials();
  if (!cred || !cred.token || !cred.expires_at) {
    return null;
  }
  const expiresAt = new Date(cred.expires_at).getTime();
  if (Date.now() + TOKEN_EXPIRY_BUFFER_MS > expiresAt) {
    return null;
  }
  return cred;
}

/**
 * Mask email for display: "user@example.com" → "us***@example.com"
 */
export function maskEmailForDisplay(email) {
  if (!email || typeof email !== "string") {
    return "***";
  }
  const [local, domain] = email.split("@");
  if (!local || !domain) {
    return "***";
  }
  const masked = local.length > 2 ? `${local[0]}${local[1]}${"*".repeat(Math.min(local.length - 2, 3))}` : `${"*".repeat(local.length)}`;
  return `${masked}@${domain}`;
}
