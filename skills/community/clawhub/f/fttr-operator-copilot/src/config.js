export const DEFAULT_FTTRAI_RPC_URL = "https://fms-main.fttrai.com/api";

export function loadConfig(env = process.env) {
  const baseUrl = trimTrailingSlash(env.FTTRAI_RPC_URL || DEFAULT_FTTRAI_RPC_URL);
  const token = env.FTTRAI_OPERATOR_AUTH_TOKEN || "";
  const timeoutMs = parsePositiveInt(env.FTTRAI_TIMEOUT_MS, 30000);
  const maxRetries = parsePositiveInt(env.FTTRAI_MAX_RETRIES, 2);

  const missing = [];
  if (!token) missing.push("FTTRAI_OPERATOR_AUTH_TOKEN");

  if (missing.length > 0) {
    const err = new Error(`缺少必要环境变量: ${missing.join(", ")}`);
    err.code = "missing_config";
    throw err;
  }

  let parsedUrl;
  try {
    parsedUrl = new URL(baseUrl);
  } catch {
    const err = new Error("FTTRAI_RPC_URL 不是有效 URL");
    err.code = "invalid_config";
    throw err;
  }

  if (!["http:", "https:"].includes(parsedUrl.protocol)) {
    const err = new Error("FTTRAI_RPC_URL 只支持 http 或 https");
    err.code = "invalid_config";
    throw err;
  }

  return {
    baseUrl,
    token,
    timeoutMs,
    maxRetries,
  };
}

function trimTrailingSlash(value) {
  return String(value).trim().replace(/\/+$/, "");
}

function parsePositiveInt(value, fallback) {
  if (value === undefined || value === null || String(value).trim() === "") {
    return fallback;
  }
  const parsed = Number.parseInt(String(value), 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}
