// Public X client-web assets live on abs.twimg.com.
// page.fetch uses window.fetch and the browser CORS-blocks that host from x.com.
// These files are static and do not need the logged-in cookie jar.
// Pro accept4 reached this path and then saw `read ECONNRESET`, so a single GET is not enough.
// A caller can pass `signal` and abort the socket when the Ego browser already
// has the same bytes. An abort is not retried.

import https from "node:https";

export const PUBLIC_JS_ATTEMPTS = 4;

const RETRYABLE = /ECONNRESET|ECONNREFUSED|ETIMEDOUT|EAI_AGAIN|EPIPE|ENETUNREACH|EHOSTUNREACH|socket hang up|timed?\s*out|aborted/i;

export function isPublicClientWeb(url) {
  try {
    const parsed = new URL(String(url || ""));
    return parsed.protocol === "https:"
      && parsed.hostname === "abs.twimg.com"
      && parsed.pathname.startsWith("/responsive-web/client-web/")
      && parsed.pathname.endsWith(".js");
  } catch {
    return false;
  }
}

export function isRetryablePublicJsError(error) {
  const message = error && error.message ? error.message : String(error || "");
  if (/non public client-web/.test(message)) return false;
  if (/redirected too many times/.test(message)) return false;
  if (/HTTP 5\d\d/.test(message) || /HTTP 408\b/.test(message) || /HTTP 429\b/.test(message)) return true;
  if (/HTTP 4\d\d/.test(message)) return false;
  return RETRYABLE.test(message);
}

export function publicJsBackoffMs(attempt) {
  return 250 * (2 ** attempt);
}

function abortError(signal) {
  const reason = signal && signal.reason;
  if (reason instanceof Error) return reason;
  const error = new Error("public JS aborted");
  error.code = "ABORT_ERR";
  return error;
}

function wait(ms, signal) {
  return new Promise((resolve, reject) => {
    if (signal?.aborted) {
      reject(abortError(signal));
      return;
    }
    let timer;
    const onAbort = () => {
      clearTimeout(timer);
      reject(abortError(signal));
    };
    timer = setTimeout(() => {
      if (signal) signal.removeEventListener("abort", onAbort);
      resolve();
    }, ms);
    if (signal) signal.addEventListener("abort", onAbort, { once: true });
  });
}

function fetchPublicJsOnce(url, { request = https.request, timeout = 60_000, redirects = 3, signal } = {}) {
  if (!isPublicClientWeb(url)) {
    return Promise.reject(new Error(`refusing to Node-fetch a non public client-web URL: ${url}`));
  }
  if (signal?.aborted) return Promise.reject(abortError(signal));
  return new Promise((resolve, reject) => {
    let settled = false;
    let req;
    const finish = (error, body) => {
      if (settled) return;
      settled = true;
      if (signal) signal.removeEventListener("abort", onAbort);
      if (error) reject(error instanceof Error ? error : new Error(String(error)));
      else resolve(body);
    };
    const onAbort = () => {
      const error = abortError(signal);
      // Settle before destroy. destroy often emits ECONNRESET, which must not start another retry.
      finish(error);
      if (req && typeof req.destroy === "function") req.destroy(error);
    };
    if (signal) signal.addEventListener("abort", onAbort);
    req = request(url, {
      method: "GET",
      headers: { accept: "*/*", "accept-encoding": "identity" },
      timeout,
    }, (res) => {
      const status = Number(res.statusCode || 0);
      if (status >= 300 && status < 400 && res.headers.location) {
        res.resume();
        if (redirects <= 0) {
          finish(new Error(`public JS redirected too many times: ${url}`));
          return;
        }
        let next = "";
        try {
          next = new URL(res.headers.location, url).href;
        } catch (error) {
          finish(error);
          return;
        }
        fetchPublicJsOnce(next, { request, timeout, redirects: redirects - 1, signal }).then(
          (body) => finish(null, body),
          (error) => finish(error),
        );
        return;
      }
      const chunks = [];
      res.on("data", (chunk) => chunks.push(chunk));
      res.on("end", () => {
        const body = Buffer.concat(chunks).toString("utf8");
        if (status !== 200) {
          finish(new Error(`public JS HTTP ${status} for ${url}`));
          return;
        }
        finish(null, body);
      });
      res.on("error", (error) => finish(error));
    });
    req.on("error", (error) => finish(error));
    req.on("timeout", () => {
      const error = new Error(`public JS timeout for ${url}`);
      finish(error);
      if (typeof req.destroy === "function") req.destroy(error);
    });
    req.end();
  });
}

export async function fetchPublicJs(url, options = {}) {
  const attempts = Math.min(5, Math.max(1, Number(options.attempts) || PUBLIC_JS_ATTEMPTS));
  const signal = options.signal;
  const sleep = options.sleep || ((ms) => wait(ms, signal));
  let last = new Error("public JS fetch failed");
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    if (signal?.aborted) throw abortError(signal);
    try {
      return await fetchPublicJsOnce(url, options);
    } catch (error) {
      last = error instanceof Error ? error : new Error(String(error));
      if (signal?.aborted || attempt === attempts - 1 || !isRetryablePublicJsError(last)) throw last;
      try {
        await sleep(publicJsBackoffMs(attempt));
      } catch (sleepError) {
        if (signal?.aborted) throw abortError(signal);
        throw sleepError;
      }
      if (signal?.aborted) throw abortError(signal);
    }
  }
  throw last;
}
