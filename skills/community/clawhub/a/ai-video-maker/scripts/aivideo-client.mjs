import { normalizeResult, validateCreatePayload } from "./contract.mjs";
import { loadSavedKey } from "./credentials.mjs";
import { randomUUID } from "node:crypto";

const DEFAULTS = {
  baseUrl: "https://aivideomaker.ai",
  apiKey: process.env.AIVIDEO_API_KEY || "",
  timeoutMs: Number(process.env.AIVIDEO_TIMEOUT_MS || 30000),
  maxRetries: Number(process.env.AIVIDEO_MAX_RETRIES || 3),
  minBackoffMs: 800,
  maxBackoffMs: 8000,
  source: "agent_skill",
  skillVersion: "2.1.0",
  agentPlatform: process.env.AIVIDEO_AGENT_PLATFORM || "unknown",
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
  if (httpStatus === 409) return "IDEMPOTENCY_CONFLICT";
  if (httpStatus === 429) return "RATE_LIMITED";
  if (/approved maximum|daily credit limit/i.test(msg)) return "BUDGET_EXCEEDED";
  if (/insufficient credits|insufficient balance/i.test(msg)) return "INSUFFICIENT_CREDITS";
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
      console.error(`[aivideo-client] ${message}`, safeMeta);
    },
  };
}

export function createAIVideoClient(options = {}) {
  const config = {
    ...DEFAULTS,
    ...options,
  };

  if (!config.apiKey) {
    if (config.baseUrl !== DEFAULTS.baseUrl) {
      throw new Error("Set an explicit API key to use a custom API host.");
    }
    config.apiKey = loadSavedKey();
  }

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
    requestedTaskId = null,
  }) {
    let attempt = 0;
    const url = `${config.baseUrl}${path}`;

    while (attempt <= config.maxRetries) {
      attempt += 1;
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), config.timeoutMs);

      const headers = {
        key: config.apiKey,
        "X-AIVideo-Source": config.source,
        "X-AIVideo-Skill-Version": config.skillVersion,
        "X-AIVideo-Agent-Platform": config.agentPlatform,
        ...(body ? { "Content-Type": "application/json" } : {}),
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
          const generationFailed = status === "FAILED";
          return normalizeResult({
            ok: !generationFailed,
            status,
            taskId: data?.taskId || data?.id || requestedTaskId,
            data,
            errorCode: generationFailed
              ? data?.errorCode || mapErrorCode(response.status, data?.message || data?.error)
              : null,
            errorMessage: generationFailed
              ? data?.message || data?.error || "Generation failed"
              : null,
            retryAfter,
            httpStatus: response.status,
          });
        }

        const errorMessage =
          data?.message || data?.error || response.statusText || "Request failed";
        const errorCode = data?.errorCode || mapErrorCode(response.status, errorMessage);

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
          taskId: data?.taskId || data?.id || requestedTaskId,
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
          const waitMs = jitteredBackoffMs(attempt, config.minBackoffMs, config.maxBackoffMs);
          logger.debug("network retry", { method, url, attempt, waitMs, isAbort });
          await sleep(waitMs);
          continue;
        }

        return normalizeResult({
          ok: false,
          status: "FAILED",
          taskId: requestedTaskId,
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
    async doctor() {
      return request({ method: "GET", path: "/api/v1/account", idempotent: true });
    },

    async quoteGeneration({ model, payload }) {
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
        path: `/api/v1/quote/${model}`,
        body: payload,
        idempotent: true,
      });
    },

    async createGeneration({ model, payload, idempotencyKey, maxCredits }) {
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
      if (!Number.isInteger(maxCredits) || maxCredits < 0) {
        return normalizeResult({
          ok: false,
          status: "FAILED",
          errorCode: "BUDGET_EXCEEDED",
          errorMessage: "maxCredits is required and must be a non-negative integer",
        });
      }

      const stableIdempotencyKey = idempotencyKey || randomUUID();
      const result = await request({
        method: "POST",
        path: `/api/v1/generate/${model}`,
        body: payload,
        idempotent: true,
        extraHeaders: {
          "Idempotency-Key": stableIdempotencyKey,
          "X-Max-Credits": String(maxCredits),
        },
      });

      if (result.ok && !result.taskId) {
        return {
          ...normalizeResult({
            ok: false,
            status: result.status,
            data: result.data,
            errorCode: "INVALID_RESPONSE",
            errorMessage: "Generation was accepted but the API response did not include a task ID",
            httpStatus: result.httpStatus,
          }),
          idempotencyKey: stableIdempotencyKey,
        };
      }

      return { ...result, idempotencyKey: stableIdempotencyKey };
    },

    async getTask(taskId) {
      return request({
        method: "GET",
        path: `/api/v1/tasks/${taskId}`,
        idempotent: true,
        requestedTaskId: taskId,
      });
    },

    async getStatus(taskId) {
      return request({
        method: "GET",
        path: `/api/v1/tasks/${taskId}/status`,
        idempotent: true,
        requestedTaskId: taskId,
      });
    },

    async cancelTask(taskId) {
      return request({
        method: "PUT",
        path: `/api/v1/tasks/${taskId}/cancel`,
        idempotent: false,
        requestedTaskId: taskId,
      });
    },
  };
}
