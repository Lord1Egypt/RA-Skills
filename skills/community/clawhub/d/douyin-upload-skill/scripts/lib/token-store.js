const crypto = require("crypto");
const fs = require("fs");
const fsp = fs.promises;

const {
  CONFIG_DIR,
  TOKEN_KEY_PATH,
  TOKENS_PATH,
} = require("./constants");
const { ensureDir, fileExists, readJson, writeJsonAtomic } = require("./fs-utils");

function decodeExternalKey(raw) {
  const value = String(raw || "").trim();
  if (!value) {
    return null;
  }

  if (/^[a-fA-F0-9]{64}$/.test(value)) {
    return Buffer.from(value, "hex");
  }

  try {
    const base64 = Buffer.from(value, "base64");
    if (base64.length === 32) {
      return base64;
    }
  } catch (_) {
    // Ignore and fallback to hash derivation.
  }

  return crypto.createHash("sha256").update(value).digest();
}

async function readOrCreateLocalKey() {
  await ensureDir(CONFIG_DIR);

  if (await fileExists(TOKEN_KEY_PATH)) {
    const raw = (await fsp.readFile(TOKEN_KEY_PATH, "utf8")).trim();
    const decoded = decodeExternalKey(raw);
    if (decoded && decoded.length === 32) {
      return decoded;
    }
    throw new Error(`Invalid encryption key file format at ${TOKEN_KEY_PATH}`);
  }

  const key = crypto.randomBytes(32);
  await fsp.writeFile(TOKEN_KEY_PATH, key.toString("hex") + "\n", { mode: 0o600 });
  try {
    await fsp.chmod(TOKEN_KEY_PATH, 0o600);
  } catch (_) {
    // Ignore chmod failures on filesystems that do not support Unix mode bits.
  }
  return key;
}

async function getEncryptionKey() {
  const fromEnv = decodeExternalKey(process.env.DOUYIN_TOKEN_ENC_KEY || "");
  if (fromEnv && fromEnv.length === 32) {
    return fromEnv;
  }
  return readOrCreateLocalKey();
}

async function saveTokenData(tokenData) {
  const key = await getEncryptionKey();
  const iv = crypto.randomBytes(12);

  const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
  const plaintext = Buffer.from(JSON.stringify(tokenData), "utf8");
  const ciphertext = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const tag = cipher.getAuthTag();

  const payload = {
    version: 1,
    algorithm: "aes-256-gcm",
    iv: iv.toString("base64"),
    tag: tag.toString("base64"),
    ciphertext: ciphertext.toString("base64"),
    updatedAt: new Date().toISOString(),
  };

  await writeJsonAtomic(TOKENS_PATH, payload, 0o600);
}

async function loadTokenData() {
  if (!(await fileExists(TOKENS_PATH))) {
    return null;
  }

  const payload = await readJson(TOKENS_PATH, null);
  if (!payload) {
    return null;
  }

  const key = await getEncryptionKey();
  const iv = Buffer.from(payload.iv, "base64");
  const tag = Buffer.from(payload.tag, "base64");
  const ciphertext = Buffer.from(payload.ciphertext, "base64");

  const decipher = crypto.createDecipheriv("aes-256-gcm", key, iv);
  decipher.setAuthTag(tag);

  const plaintext = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
  return JSON.parse(plaintext.toString("utf8"));
}

function normalizeTokenPayload(apiData, existing = null) {
  const now = Date.now();

  const accessToken = apiData.access_token || existing?.accessToken;
  const refreshToken = apiData.refresh_token || existing?.refreshToken;
  const openId = apiData.open_id || existing?.openId || "";

  if (!accessToken) {
    const error = new Error("Missing access_token from Douyin response.");
    error.code = "TOKEN_PARSE_ERROR";
    throw error;
  }

  const expiresIn = Number(apiData.expires_in || 0);
  const refreshExpiresIn = Number(apiData.refresh_expires_in || 0);

  const expiresAt = expiresIn > 0 ? now + expiresIn * 1000 : (existing?.expiresAt || now + 3600 * 1000);
  const refreshExpiresAt = refreshExpiresIn > 0
    ? now + refreshExpiresIn * 1000
    : (existing?.refreshExpiresAt || now + 7 * 24 * 3600 * 1000);

  return {
    accessToken,
    refreshToken,
    openId,
    scope: apiData.scope || existing?.scope || "",
    expiresAt,
    refreshExpiresAt,
    updatedAt: new Date().toISOString(),
  };
}

function isAccessTokenExpired(tokenData, skewSeconds = 60) {
  if (!tokenData || !tokenData.expiresAt) {
    return true;
  }
  return Date.now() + skewSeconds * 1000 >= Number(tokenData.expiresAt);
}

module.exports = {
  TOKENS_PATH,
  isAccessTokenExpired,
  loadTokenData,
  normalizeTokenPayload,
  saveTokenData,
};
