const fs = require("fs");
const path = require("path");

const {
  CONFIG_DIR,
  CONFIG_PATH,
  DEFAULT_CONFIG,
} = require("./constants");
const { ensureDir, readJson, writeJsonAtomic } = require("./fs-utils");
const { parseBoolean, parseInteger } = require("./cli-utils");

function applyEnvOverrides(config) {
  const merged = { ...config };

  if (process.env.DOUYIN_SCOPE) merged.scope = process.env.DOUYIN_SCOPE;
  if (process.env.DOUYIN_ASR_MODE) merged.asrMode = process.env.DOUYIN_ASR_MODE;
  if (process.env.DOUYIN_ASR_API_URL) merged.asrApiUrl = process.env.DOUYIN_ASR_API_URL;
  if (process.env.DOUYIN_ASR_API_MODEL) merged.asrApiModel = process.env.DOUYIN_ASR_API_MODEL;
  if (process.env.DOUYIN_FFMPEG_BIN) merged.ffmpegBin = process.env.DOUYIN_FFMPEG_BIN;
  if (process.env.DOUYIN_FFPROBE_BIN) merged.ffprobeBin = process.env.DOUYIN_FFPROBE_BIN;
  if (process.env.DOUYIN_WHISPER_BIN) merged.whisperBin = process.env.DOUYIN_WHISPER_BIN;
  if (process.env.DOUYIN_WHISPER_MODEL_PATH) merged.whisperModelPath = process.env.DOUYIN_WHISPER_MODEL_PATH;
  if (process.env.DOUYIN_WHISPER_LANG) merged.whisperLang = process.env.DOUYIN_WHISPER_LANG;
  if (process.env.DOUYIN_OUTBOX_DIR) merged.outboxDir = process.env.DOUYIN_OUTBOX_DIR;
  if (process.env.DOUYIN_TRANSCRIPT_CACHE_DIR) merged.transcriptCacheDir = process.env.DOUYIN_TRANSCRIPT_CACHE_DIR;
  if (process.env.DOUYIN_ASR_API_TIMEOUT_MS !== undefined) {
    merged.asrApiTimeoutMs = parseInteger(process.env.DOUYIN_ASR_API_TIMEOUT_MS, merged.asrApiTimeoutMs);
  }

  if (process.env.DOUYIN_DEFAULT_PRIVATE_STATUS !== undefined) {
    merged.defaultPrivateStatus = parseInteger(process.env.DOUYIN_DEFAULT_PRIVATE_STATUS, merged.defaultPrivateStatus);
  }

  if (process.env.DOUYIN_AUTO_CONFIRM !== undefined) {
    merged.autoConfirm = parseBoolean(process.env.DOUYIN_AUTO_CONFIRM, merged.autoConfirm);
  }

  return merged;
}

async function loadConfig() {
  await ensureDir(CONFIG_DIR);
  const fileConfig = (await readJson(CONFIG_PATH, {})) || {};
  return applyEnvOverrides({ ...DEFAULT_CONFIG, ...fileConfig });
}

async function saveConfig(config) {
  await ensureDir(CONFIG_DIR);
  await writeJsonAtomic(CONFIG_PATH, config, 0o600);
}

function validateConfigValue(key, rawValue) {
  switch (key) {
    case "defaultPrivateStatus": {
      const value = parseInteger(rawValue, null);
      if (![0, 1, 2].includes(value)) {
        throw new Error("defaultPrivateStatus must be one of: 0, 1, 2.");
      }
      return value;
    }
    case "asrApiTimeoutMs": {
      const value = parseInteger(rawValue, null);
      if (!Number.isFinite(value) || value <= 0) {
        throw new Error("asrApiTimeoutMs must be a positive integer.");
      }
      return value;
    }
    case "asrMode": {
      const value = String(rawValue || "").trim().toLowerCase();
      const allowed = ["api", "whisper-gpu", "whisper-cpu"];
      if (!allowed.includes(value)) {
        throw new Error(`asrMode must be one of: ${allowed.join(", ")}`);
      }
      return value;
    }
    case "autoConfirm":
      return parseBoolean(rawValue);
    case "scope":
    case "asrApiUrl":
    case "asrApiModel":
    case "ffmpegBin":
    case "ffprobeBin":
    case "whisperBin":
    case "whisperModelPath":
    case "whisperLang":
    case "outboxDir":
    case "transcriptCacheDir": {
      const value = String(rawValue || "").trim();
      if (!value) {
        throw new Error(`${key} cannot be empty.`);
      }
      return value;
    }
    default:
      throw new Error(`Unknown config key: ${key}`);
  }
}

async function setConfigKey(key, rawValue) {
  const config = await loadConfig();
  const value = validateConfigValue(key, rawValue);
  const next = { ...config, [key]: value };
  await saveConfig(next);
  return next;
}

function getAuthEnv() {
  return {
    clientKey: process.env.DOUYIN_CLIENT_KEY || "",
    clientSecret: process.env.DOUYIN_CLIENT_SECRET || "",
    redirectUri: process.env.DOUYIN_REDIRECT_URI || "",
  };
}

function assertAuthEnv() {
  const env = getAuthEnv();
  const missing = [];
  if (!env.clientKey) missing.push("DOUYIN_CLIENT_KEY");
  if (!env.clientSecret) missing.push("DOUYIN_CLIENT_SECRET");
  if (!env.redirectUri) missing.push("DOUYIN_REDIRECT_URI");
  if (missing.length > 0) {
    const error = new Error(`Missing required environment variables: ${missing.join(", ")}`);
    error.code = "MISSING_ENV";
    error.details = { missing };
    throw error;
  }
  return env;
}

function readConfigSync() {
  if (!fs.existsSync(CONFIG_PATH)) {
    return { ...DEFAULT_CONFIG };
  }
  const text = fs.readFileSync(CONFIG_PATH, "utf8");
  return { ...DEFAULT_CONFIG, ...JSON.parse(text) };
}

module.exports = {
  CONFIG_PATH,
  assertAuthEnv,
  getAuthEnv,
  loadConfig,
  readConfigSync,
  saveConfig,
  setConfigKey,
};
