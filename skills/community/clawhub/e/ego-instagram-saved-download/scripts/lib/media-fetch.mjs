// Byte download for pinimg / Instagram CDNs.
// Node's global fetch (undici, usually HTTP/2) often throws "fetch failed" before any
// HTTP status on v1.pinimg.com video and cdninstagram hosts. That is a transport
// failure. A real 404/403 must stay a 404/403 so the caller can try the next URL.
// Order: global fetch, then HTTP/1.1 over IPv4, then the logged-in page.fetch.

import fs from "node:fs/promises";
import http from "node:http";
import https from "node:https";
import os from "node:os";
import path from "node:path";
import { sniffImage, sniffVideo } from "./pure.mjs";

export function browserTimeout(url) {
  return /\.(mp4|m3u8|cmfv|cmfa)(\?|$)/i.test(String(url || "")) ? 120_000 : 20_000;
}

export async function browserSave(page, targetUrl, { maxBytes, referer, timeout } = {}) {
  const partial = path.join(os.tmpdir(), `.ego-media-${Date.now()}-${Math.random().toString(16).slice(2)}`);
  try {
    await page.fetch(targetUrl, {
      headers: { Referer: referer || "", Accept: "*/*" },
      timeout: timeout || browserTimeout(targetUrl),
      saveAs: partial,
    });
    const buf = await fs.readFile(partial);
    const sniffed = sniffImage(buf);
    const type = sniffed || (sniffVideo(buf) ? "video/mp4" : "");
    if (!type || buf.length < 100) {
      return { ok: false, status: 200, type: "", buf: Buffer.alloc(0), error: "browser response was not image or video" };
    }
    if (maxBytes && buf.length > maxBytes) {
      return { ok: false, status: 200, type, buf: Buffer.alloc(0), error: `larger than ${maxBytes} bytes` };
    }
    return { ok: true, status: 200, type, buf, error: null };
  } catch (error) {
    return emptyRead(formatTransportError(error));
  } finally {
    await fs.rm(partial, { force: true }).catch(() => {});
  }
}

export function emptyRead(error = "not fetched") {
  return { ok: false, status: 0, type: "", buf: Buffer.alloc(0), error };
}

export function formatTransportError(error) {
  const code = error?.cause?.code || error?.code;
  const message = String(error?.message || error || "fetch failed");
  if (!code || message.includes(String(code))) return message;
  return `${message} (${code})`;
}

export function usefulMedia(read) {
  const buf = read?.buf;
  if (!read?.ok || !buf || buf.length < 12) return false;
  if (sniffImage(buf) || sniffVideo(buf)) return true;
  return String(read.type || "").toLowerCase().startsWith("video/");
}

// True when another client should try. False when the bytes are already media,
// or when the server answered with a real HTTP error (try the next URL instead).
export function shouldTryAlternateFetch(read) {
  if (!read || typeof read !== "object") return true;
  if (usefulMedia(read)) return false;
  if (Number(read.status || 0) > 0 && read.error) return false;
  return true;
}

export function requestBytes(rawUrl, { headers = {}, maxBytes, family = 4, redirects = 5, timeoutMs = 30_000 } = {}) {
  const lib = String(rawUrl).startsWith("http:") ? http : https;
  return new Promise((resolve, reject) => {
    let settled = false;
    const finish = (value) => {
      if (settled) return;
      settled = true;
      resolve(value);
    };
    const fail = (error) => {
      if (settled) return;
      settled = true;
      reject(error);
    };
    const req = lib.request(
      rawUrl,
      {
        method: "GET",
        headers,
        family,
        timeout: timeoutMs,
      },
      (res) => {
        const status = Number(res.statusCode || 0);
        const location = res.headers.location;
        if (location && status >= 300 && status < 400) {
          res.resume();
          if (redirects <= 0) {
            finish(emptyRead("too many redirects"));
            return;
          }
          let next;
          try {
            next = new URL(location, rawUrl).href;
          } catch (error) {
            fail(error);
            return;
          }
          requestBytes(next, { headers, maxBytes, family, redirects: redirects - 1, timeoutMs }).then(finish, fail);
          return;
        }
        const type = String(res.headers["content-type"] || "").split(";")[0];
        const len = Number(res.headers["content-length"] || 0);
        if (maxBytes && len > maxBytes) {
          res.resume();
          finish({ ok: false, status, type, buf: Buffer.alloc(0), error: `larger than ${maxBytes} bytes` });
          return;
        }
        const chunks = [];
        let total = 0;
        let overflow = false;
        res.on("data", (chunk) => {
          if (overflow || settled) return;
          total += chunk.length;
          if (maxBytes && total > maxBytes) {
            overflow = true;
            finish({ ok: false, status, type, buf: Buffer.alloc(0), error: `larger than ${maxBytes} bytes` });
            req.destroy();
            return;
          }
          chunks.push(chunk);
        });
        res.on("end", () => {
          if (overflow || settled) return;
          const buf = Buffer.concat(chunks);
          const ok = status >= 200 && status < 300;
          finish({
            ok,
            status,
            type,
            buf,
            error: ok ? null : `HTTP ${status}`,
          });
        });
        res.on("error", fail);
      },
    );
    req.on("timeout", () => req.destroy(new Error("timeout")));
    req.on("error", fail);
    req.end();
  });
}

export async function fetchMediaBytes({ url, maxBytes, headers, nodeFetch, directFetch, browserFetch }) {
  let read = emptyRead();
  try {
    read = await nodeFetch(url, { maxBytes, headers });
  } catch (error) {
    read = emptyRead(formatTransportError(error));
  }
  if (!read) read = emptyRead();
  if (!shouldTryAlternateFetch(read)) return read;

  if (directFetch) {
    try {
      const via = await directFetch(url, { maxBytes, headers });
      if (via && !shouldTryAlternateFetch(via)) return via;
      if (via?.error) read = via;
    } catch (error) {
      read = emptyRead(formatTransportError(error));
    }
  }
  if (!browserFetch || !shouldTryAlternateFetch(read)) return read;
  try {
    const via = await browserFetch(url, { maxBytes, headers });
    if (usefulMedia(via)) return via;
    if (via?.error) return via;
    return read.error ? read : via || read;
  } catch (error) {
    return emptyRead(formatTransportError(error));
  }
}
