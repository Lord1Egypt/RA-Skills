import { normalizeResult, validateCreatePayload } from "./contract.mjs";

const DEFAULTS = {
  baseUrl: "https://aivideomaker.ai",
  apiKey: process.env.AIVIDEO_API_KEY || "",
  timeoutMs: Number(process.env.AIVIDEO_TIMEOUT_MS || 30000),
  maxRetries: Number(process.env.AIVIDEO_MAX_RETRIES || 3),
  minBackoffMs: 800,
  maxBackoffMs: 8000,
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function toRetryAfterSeconds(headers) {
  const retryAfter = headers.get("retry-after");
  if (!retryAfter) return null;
  const parsed = Number(retryAfter);
  return Number.isFinite(parsed) ? parsed : null;
}

function jitteredBackoffMs(attempt, minBackoffMs, maxBackoffMs) {
  const raw = Math.min(maxBackoffMs, minBackoffMs * 2 ** (attempt - 1));
  const jitter = Math.floor(Math.random() * 250);
  return raw + jitter;
}

function mapErrorCode(httpStatus, message = "") {
  const msg = String(message || "");
  if (httpStatus === 401 || httpStatus === 403) return "AUTH_FAILED";
  if (httpStatus === 404) return "TASK_NOT_FOUND";
  if (httpStatus === 429) return "RATE_LIMITED";
  if (/insufficient credits/i.test(msg)) return "INSUFFICIENT_CREDITS";
  if (httpStatus >= 400 && httpStatus < 500) return "INVALID_PAYLOAD";
  if (httpStatus >= 500) return "UPSTREAM_ERROR";
  return "UNKNOWN_ERROR";
}

function sanitizeUrl(url) {
  try {
    const u = new URL(url);
    u.search = "";
    return u.toString();
  } catch {
    return url;
  }
}

function sanitizeHeaders(headers) {
  const safe = { ...headers };
  if (safe.key) safe.key = "***";
  return safe;
}

function createLogger(enabled = true) {
  return {
    debug(message, meta = {}) {
      if (!enabled) return;
      const safeMeta = {
        ...meta,
        url: meta.url ? sanitizeUrl(meta.url) : undefined,
        headers: meta.headers ? sanitizeHeaders(meta.headers) : undefined,
      };
      // Remove headers from default logs to reduce sensitive surface.
      delete safeMeta.headers;
      // eslint-disable-next-line no-console
      console.log(`[aivideo-client] ${message}`, safeMeta);
    },
  };
}

export function createAIVideoClient(options = {}) {
  const config = {
    ...DEFAULTS,
    ...options,
  };

  const logger = options.logger || createLogger(options.debug !== false);

  if (!config.apiKey) {
    throw new Error("AIVIDEO_API_KEY is required");
  }

  async function request({
    method,
    path,
    body,
    idempotent = false,
    extraHeaders = {},
  }) {
    let attempt = 0;
    const url = `${config.baseUrl}${path}`;

    while (attempt <= config.maxRetries) {
      attempt += 1;
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), config.timeoutMs);

      const headers = {
        key: config.apiKey,
        "Content-Type": "application/json",
        ...extraHeaders,
      };

      try {
        logger.debug("sending request", { method, url, attempt, headers });
        const response = await fetch(url, {
          method,
          headers,
          body: body ? JSON.stringify(body) : undefined,
          signal: controller.signal,
        });
        clearTimeout(timeoutId);

        const retryAfter = toRetryAfterSeconds(response.headers);
        let data = null;
        try {
          data = await response.json();
        } catch {
          data = null;
        }

        if (response.ok) {
          const status = data?.status || "UNKNOWN";
          return normalizeResult({
            ok: true,
            status,
            taskId: data?.taskId || data?.id || null,
            data,
            retryAfter,
            httpStatus: response.status,
          });
        }

        const errorMessage = data?.message || response.statusText || "Request failed";
        const errorCode = mapErrorCode(response.status, errorMessage);

        const canRetryStatus = response.status === 429 || response.status >= 500;
        const canRetry = idempotent && canRetryStatus && attempt <= config.maxRetries;

        if (canRetry) {
          const waitMs =
            retryAfter && retryAfter > 0
              ? retryAfter * 1000
              : jitteredBackoffMs(attempt, config.minBackoffMs, config.maxBackoffMs);
          logger.debug("retrying request", { method, url, attempt, waitMs, retryAfter });
          await sleep(waitMs);
          continue;
        }

        return normalizeResult({
          ok: false,
          status: data?.status || "FAILED",
          taskId: data?.taskId || data?.id || null,
          data,
          errorCode,
          errorMessage,
          retryAfter,
          httpStatus: response.status,
        });
      } catch (error) {
        clearTimeout(timeoutId);
        const isAbort = error && error.name === "AbortError";
        const canRetry = idempotent && attempt <= config.maxRetries;

        if (canRetry) {
          const waitMs = jitteredBackoffMs(
            attempt,
            config.minBackoffMs,
            config.maxBackoffMs,
          );
          logger.debug("network retry", { method, url, attempt, waitMs, isAbort });
          await sleep(waitMs);
          continue;
        }

        return normalizeResult({
          ok: false,
          status: "FAILED",
          errorCode: "NETWORK_ERROR",
          errorMessage: isAbort ? "Request timeout" : "Network request failed",
        });
      }
    }

    return normalizeResult({
      ok: false,
      status: "FAILED",
      errorCode: "UNKNOWN_ERROR",
      errorMessage: "Retry loop exhausted",
    });
  }

  return {
    async createGeneration({ model, payload }) {
      const validation = validateCreatePayload(model, payload);
      if (!validation.ok) {
        return normalizeResult({
          ok: false,
          status: "FAILED",
          errorCode: validation.errorCode,
          errorMessage: validation.errorMessage,
          data: { details: validation.details },
        });
      }

      return request({
        method: "POST",
        path: `/api/v1/generate/${model}`,
        body: payload,
        idempotent: false,
      });
    },

    async getTask(taskId) {
      return request({
        method: "GET",
        path: `/api/v1/tasks/${taskId}`,
        idempotent: true,
      });
    },

    async getStatus(taskId) {
      return request({
        method: "GET",
        path: `/api/v1/tasks/${taskId}/status`,
        idempotent: true,
      });
    },

    async cancelTask(taskId) {
      return request({
        method: "PUT",
        path: `/api/v1/tasks/${taskId}/cancel`,
        idempotent: false,
      });
    },
  };
}
