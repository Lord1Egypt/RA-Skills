// Bytes for abs.twimg.com client-web scripts.
// Node HTTPS to that host can fail (Pro: ECONNREFUSED / ECONNRESET / timeout)
// while the logged-in Ego Chromium still reaches it. page.fetch cannot read the
// response: the browser CORS-blocks abs.twimg.com from x.com. A home page that
// only just passed check-login often has not loaded ondemand.s yet, so the
// resource tree is empty until something asks the browser to fetch the URL.
// Order for one URL: bytes already in the page, then a race between Node and a
// browser warm-up (Network.loadNetworkResource, else a script tag plus the
// resource-tree readers below). The winner is cancelled so a refused Node
// socket does not keep retrying after the browser already has the file.

import { isPublicClientWeb } from "./fetch-public.mjs";

export function sameClientScript(left, right) {
  try {
    const a = new URL(String(left || ""));
    const b = new URL(String(right || ""));
    return a.protocol === "https:"
      && a.hostname === b.hostname
      && a.pathname === b.pathname;
  } catch {
    return false;
  }
}

export function decodeCdpBody(body) {
  if (!body || typeof body !== "object") return "";
  const content = typeof body.content === "string"
    ? body.content
    : (typeof body.body === "string" ? body.body : "");
  if (!content) return "";
  if (body.base64Encoded) {
    try {
      return Buffer.from(content, "base64").toString("utf8");
    } catch {
      return "";
    }
  }
  return content;
}

export function frameNodes(tree) {
  const out = [];
  const visit = (node) => {
    if (!node || typeof node !== "object") return;
    out.push(node);
    for (const child of node.childFrames || []) visit(child);
  };
  visit(tree && tree.frameTree);
  return out;
}

async function pageScriptSnapshot(page) {
  if (!page || typeof page.evaluate !== "function") return { scripts: [], resources: [] };
  try {
    const snap = await page.evaluate(() => {
      const scripts = Array.from(document.scripts || []).map((script) => ({
        src: String(script.src || ""),
        text: String(script.textContent || ""),
      }));
      let resources = [];
      try {
        resources = performance.getEntriesByType("resource").map((entry) => String(entry.name || ""));
      } catch {
        resources = [];
      }
      return { scripts, resources };
    });
    return {
      scripts: Array.isArray(snap && snap.scripts) ? snap.scripts : [],
      resources: Array.isArray(snap && snap.resources) ? snap.resources : [],
    };
  } catch {
    return { scripts: [], resources: [] };
  }
}

function textFromSnapshot(snapshot, url) {
  for (const script of snapshot.scripts || []) {
    if (!sameClientScript(script.src, url)) continue;
    const text = String(script.text || "").trim();
    if (text) return text;
  }
  return "";
}

function resourceAttempts(tree, url, resources) {
  const frames = frameNodes(tree);
  const attempts = [];
  for (const node of frames) {
    const frameId = node.frame && node.frame.id;
    if (!frameId) continue;
    for (const resource of node.resources || []) {
      const resourceUrl = String(resource && resource.url || "");
      if (!sameClientScript(resourceUrl, url)) continue;
      attempts.push({ frameId, url: resourceUrl });
    }
  }
  if (attempts.length) return attempts;
  const main = frames.find((node) => node.frame && node.frame.id);
  if (!main) return attempts;
  for (const loaded of resources || []) {
    if (!sameClientScript(loaded, url)) continue;
    attempts.push({ frameId: main.frame.id, url: String(loaded) });
  }
  return attempts;
}

async function readResourceContent(page, url, resources) {
  if (!page || typeof page.cdp !== "function") return "";
  let tree;
  try {
    tree = await page.cdp("Page.getResourceTree");
  } catch {
    return "";
  }
  for (const attempt of resourceAttempts(tree, url, resources)) {
    try {
      const body = await page.cdp("Page.getResourceContent", attempt);
      const text = decodeCdpBody(body).trim();
      if (text) return text;
    } catch {
      // This frame's copy can be gone while another frame still has it.
    }
  }
  return "";
}

async function readNetworkBody(page, url) {
  if (!page || typeof page.cdp !== "function") return "";
  let tree;
  try {
    tree = await page.cdp("Page.getResourceTree");
  } catch {
    return "";
  }
  for (const node of frameNodes(tree)) {
    for (const resource of node.resources || []) {
      if (!resource || !resource.requestId) continue;
      if (!sameClientScript(resource.url, url)) continue;
      try {
        const body = await page.cdp("Network.getResponseBody", { requestId: resource.requestId });
        const text = decodeCdpBody(body).trim();
        if (text) return text;
      } catch {
        // requestId from another document is not a body.
      }
    }
  }
  return "";
}

export async function readLoadedClientScript(page, url) {
  if (!isPublicClientWeb(url)) return "";
  const snapshot = await pageScriptSnapshot(page);
  const inline = textFromSnapshot(snapshot, url);
  if (inline) return inline;
  const fromResource = await readResourceContent(page, url, snapshot.resources);
  if (fromResource) return fromResource;
  return readNetworkBody(page, url);
}

const RESOURCE_TIMEOUT_MS = 12_000;
const WARM_POLL_MS = 2_000;

export function decodeIoChunk(chunk) {
  if (!chunk || typeof chunk !== "object") return "";
  const data = typeof chunk.data === "string" ? chunk.data : "";
  if (!data) return "";
  if (chunk.base64Encoded) {
    try {
      return Buffer.from(data, "base64").toString("utf8");
    } catch {
      return "";
    }
  }
  return data;
}

export async function readIoStream(page, handle) {
  if (!handle || !page || typeof page.cdp !== "function") return "";
  let text = "";
  try {
    for (let i = 0; i < 32; i += 1) {
      const chunk = await page.cdp("IO.read", { handle });
      text += decodeIoChunk(chunk);
      if (!chunk || chunk.eof) break;
    }
  } catch {
    return text.trim();
  } finally {
    try {
      await page.cdp("IO.close", { handle });
    } catch {
      // The stream may already be closed.
    }
  }
  return text.trim();
}

function withTimeout(promise, ms, message, signal) {
  let timer;
  const work = Promise.resolve(promise).finally(() => clearTimeout(timer));
  const timeout = new Promise((resolve, reject) => {
    const fail = (error) => {
      clearTimeout(timer);
      if (signal) signal.removeEventListener("abort", onAbort);
      reject(error);
    };
    const onAbort = () => fail(new Error("browser warm aborted"));
    if (signal?.aborted) {
      fail(new Error("browser warm aborted"));
      return;
    }
    timer = setTimeout(() => fail(new Error(message)), ms);
    if (signal) signal.addEventListener("abort", onAbort, { once: true });
  });
  // The side that loses the race can reject later. A handler on each promise
  // keeps that rejection from escaping after the caller has moved on.
  work.catch(() => {});
  timeout.catch(() => {});
  return Promise.race([work, timeout]);
}

async function readNetworkResourceOnce(page, url) {
  const tree = await page.cdp("Page.getResourceTree");
  const frameId = frameNodes(tree).map((node) => node.frame && node.frame.id).find(Boolean);
  if (!frameId) return "";
  const loaded = await page.cdp("Network.loadNetworkResource", {
    frameId,
    url,
    options: { disableCache: false, includeCredentials: false },
  });
  const resource = loaded && loaded.resource && typeof loaded.resource === "object" ? loaded.resource : loaded;
  if (!resource || typeof resource !== "object") return "";
  if (resource.success === false) return "";
  const status = Number(resource.httpStatusCode || 0);
  if (status && (status < 200 || status >= 300)) return "";
  const handle = resource.stream || resource.streamId || "";
  if (!handle) return "";
  return readIoStream(page, handle);
}

export async function readNetworkResource(page, url, timeoutMs = RESOURCE_TIMEOUT_MS, signal) {
  if (!isPublicClientWeb(url) || !page || typeof page.cdp !== "function") return "";
  try {
    const text = await withTimeout(
      readNetworkResourceOnce(page, url),
      timeoutMs,
      "browser network resource timed out",
      signal,
    );
    return text && String(text).trim() ? String(text).trim() : "";
  } catch {
    return "";
  }
}

export async function injectClientScript(page, url) {
  if (!isPublicClientWeb(url)) return "skipped";
  if (!page || typeof page.evaluate !== "function") return "unavailable";
  try {
    const status = await page.evaluate((src) => {
      const root = document.head || document.documentElement || document.body;
      if (!root || typeof document.createElement !== "function") return "unavailable";
      const scripts = document.scripts ? Array.from(document.scripts) : [];
      if (scripts.some((script) => script && script.src === src)) return "pending";
      const script = document.createElement("script");
      script.src = src;
      script.async = true;
      root.appendChild(script);
      return "pending";
    }, url);
    return status === "pending" ? "pending" : "unavailable";
  } catch {
    return "unavailable";
  }
}

function pause(ms, signal) {
  return new Promise((resolve, reject) => {
    if (signal?.aborted) {
      reject(new Error("browser warm aborted"));
      return;
    }
    let timer;
    const onAbort = () => {
      clearTimeout(timer);
      reject(new Error("browser warm aborted"));
    };
    timer = setTimeout(() => {
      if (signal) signal.removeEventListener("abort", onAbort);
      resolve();
    }, ms);
    if (signal) signal.addEventListener("abort", onAbort, { once: true });
  });
}

export async function warmClientScript(page, url, options = {}) {
  const timeoutMs = Number(options.timeoutMs) > 0 ? Number(options.timeoutMs) : RESOURCE_TIMEOUT_MS;
  const signal = options.signal;
  const wait = options.wait || ((ms) => pause(ms, signal));
  if (signal?.aborted || !isPublicClientWeb(url)) return "";
  const cached = await readLoadedClientScript(page, url);
  if (cached) return cached;
  const direct = await readNetworkResource(page, url, timeoutMs, signal);
  if (signal?.aborted) return "";
  if (direct) return direct;
  const injected = await injectClientScript(page, url);
  if (injected !== "pending" || signal?.aborted) return "";
  const deadline = Date.now() + Math.min(timeoutMs, WARM_POLL_MS);
  while (!signal?.aborted && Date.now() < deadline) {
    const loaded = await readLoadedClientScript(page, url);
    if (loaded) return loaded;
    const slice = Math.min(200, deadline - Date.now());
    if (slice <= 0) break;
    try {
      await wait(slice);
    } catch {
      return "";
    }
  }
  if (signal?.aborted) return "";
  return readNetworkResource(page, url, timeoutMs, signal);
}

async function readQuiet(readCached, url, notes) {
  try {
    const text = await readCached(url);
    return text && String(text).trim() ? String(text) : "";
  } catch (error) {
    notes.push(error && error.message ? error.message : "browser cache failed");
    return "";
  }
}

function firstNonEmpty(promises) {
  return new Promise((resolve) => {
    let pending = promises.length;
    if (!pending) {
      resolve("");
      return;
    }
    for (const promise of promises) {
      Promise.resolve(promise).then((value) => {
        const text = typeof value === "string" ? value.trim() : "";
        if (text) {
          resolve(text);
          return;
        }
        pending -= 1;
        if (pending === 0) resolve("");
      }, () => {
        pending -= 1;
        if (pending === 0) resolve("");
      });
    }
  });
}

export async function loadClientWebBytes({ url, readCached, warm, loadPublic }) {
  const notes = [];
  const cached = await readQuiet(readCached, url, notes);
  if (cached) return cached;
  const controller = new AbortController();
  let nodeNote = "";
  let warmNote = "";
  const nodePromise = Promise.resolve().then(async () => {
    try {
      const body = await loadPublic(url, { signal: controller.signal });
      const text = body && String(body).trim();
      if (!text) {
        if (!controller.signal.aborted) nodeNote = "empty body";
        return "";
      }
      return String(text);
    } catch (error) {
      if (controller.signal.aborted) return "";
      nodeNote = error && error.message ? error.message : "fetch failed";
      return "";
    }
  });
  const warmPromise = Promise.resolve().then(async () => {
    if (typeof warm !== "function") {
      warmNote = "browser warm empty";
      return "";
    }
    try {
      const body = await warm(url, { signal: controller.signal });
      const text = body && String(body).trim();
      if (!text) {
        if (!controller.signal.aborted) warmNote = "browser warm empty";
        return "";
      }
      return String(text);
    } catch (error) {
      if (controller.signal.aborted) return "";
      warmNote = error && error.message ? error.message : "browser warm failed";
      return "";
    }
  });
  const text = await firstNonEmpty([nodePromise, warmPromise]);
  if (text) {
    controller.abort();
    return text;
  }
  const late = await readQuiet(readCached, url, notes);
  if (late) return late;
  const parts = [...notes, warmNote, nodeNote].filter(Boolean);
  if (!parts.some((part) => part.includes("browser cache empty"))) parts.push("browser cache empty");
  const failure = new Error(parts.join("; "));
  failure.code = "PUBLIC_JS";
  throw failure;
}
