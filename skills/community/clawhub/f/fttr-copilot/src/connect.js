const TRANSIENT_STATUS = new Set([408, 429, 500, 502, 503, 504]);

export class ConnectClient {
  constructor(config) {
    this.config = config;
  }

  async unary(procedure, body = {}) {
    const url = `${this.config.baseUrl}${procedure}`;
    let lastError;

    for (let attempt = 0; attempt <= this.config.maxRetries; attempt += 1) {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), this.config.timeoutMs);

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${this.config.token}`,
            "Content-Type": "application/json",
            "Accept": "application/json",
          },
          body: JSON.stringify(body),
          signal: controller.signal,
        });

        const payload = await readJson(response);
        if (response.ok) {
          return payload;
        }

        const rpcError = connectErrorFromResponse(response, payload, procedure);
        if (!TRANSIENT_STATUS.has(response.status) || attempt === this.config.maxRetries) {
          throw rpcError;
        }
        lastError = rpcError;
      } catch (error) {
        const normalized = normalizeFetchError(error, procedure);
        if (!isRetryableError(normalized) || attempt === this.config.maxRetries) {
          throw normalized;
        }
        lastError = normalized;
      } finally {
        clearTimeout(timeout);
      }

      await delay(200 * (attempt + 1));
    }

    throw lastError;
  }
}

async function readJson(response) {
  const text = await response.text();
  if (!text.trim()) {
    return {};
  }
  try {
    return JSON.parse(text);
  } catch {
    return { raw: text };
  }
}

function connectErrorFromResponse(response, payload, procedure) {
  const message = payload?.message || payload?.error || `RPC 调用失败: HTTP ${response.status}`;
  const err = new Error(message);
  err.code = payload?.code || httpStatusToCode(response.status);
  err.status = response.status;
  err.procedure = procedure;
  err.details = payload;
  return err;
}

function normalizeFetchError(error, procedure) {
  if (error?.code && error?.procedure) {
    return error;
  }
  const err = new Error(error?.name === "AbortError" ? "RPC 调用超时" : error?.message || "RPC 调用失败");
  err.code = error?.name === "AbortError" ? "deadline_exceeded" : "unavailable";
  err.procedure = procedure;
  return err;
}

function isRetryableError(error) {
  return ["deadline_exceeded", "unavailable", "resource_exhausted"].includes(error?.code);
}

function httpStatusToCode(status) {
  switch (status) {
    case 400:
      return "invalid_argument";
    case 401:
      return "unauthenticated";
    case 403:
      return "permission_denied";
    case 404:
      return "not_found";
    case 408:
      return "deadline_exceeded";
    case 429:
      return "resource_exhausted";
    default:
      return status >= 500 ? "unavailable" : "unknown";
  }
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
