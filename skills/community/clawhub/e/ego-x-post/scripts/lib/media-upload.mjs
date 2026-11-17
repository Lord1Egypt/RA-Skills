// upload.x.com INIT → APPEND → FINALIZE, captured 2026-11-04 from the x.com composer.
// Runs inside the page: page.fetch cannot carry a file body across the Node boundary.
// Upload requests do not send x-client-transaction-id. Images do not call STATUS
// unless FINALIZE returns processing_info (video/GIF). This skill does not upload GIF.

import {
  appendUrl,
  clipUploadBody,
  finalizeUrl,
  initUrl,
  mediaIdFrom,
  parseMediaJson,
  processingErrorText,
  segmentSlices,
  statusUrl,
} from "./media.mjs";

const ATTEMPTS = { INIT: 2, APPEND: 5, FINALIZE: 2, STATUS: 2 };
const EXPECTED = { INIT: 202, APPEND: 204, FINALIZE: 201, STATUS: 200 };
export const MAX_STATUS_POLLS = 30;

function defaultSleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function buildUploadHeaders({ bearer, csrfToken } = {}) {
  const token = String(bearer || "").replace(/^Bearer\s+/i, "").trim();
  if (!token) throw new Error("web bearer missing");
  if (!csrfToken) throw new Error("ct0 missing");
  return {
    authorization: `Bearer ${token}`,
    csrfToken: String(csrfToken),
  };
}

// Self-contained: page.evaluate re-creates this function in the page, so it
// cannot close over module bindings. Headers match the captured sruHeaders.
export async function uploadStepInPage(step) {
  const headers = {
    authorization: step.authorization,
    "x-csrf-token": step.csrfToken,
    "x-twitter-auth-type": "OAuth2Session",
  };
  const init = {
    method: step.method || "POST",
    credentials: "include",
    headers,
  };
  const signals = globalThis.AbortSignal;
  if (signals && typeof signals.timeout === "function") init.signal = signals.timeout(45000);
  if (step.command === "APPEND") {
    const raw = atob(step.b64 || "");
    const bytes = new Uint8Array(raw.length);
    for (let i = 0; i < raw.length; i += 1) bytes[i] = raw.charCodeAt(i);
    const blob = new Blob([bytes], { type: "application/octet-stream" });
    const form = new FormData();
    form.append("media", blob, "blob");
    init.body = form;
  }
  const response = await fetch(step.url, init);
  return { status: response.status, body: await response.text() };
}

function shouldRetry(result) {
  if (!result || typeof result !== "object") return true;
  const status = Number(result.status) || 0;
  if (status === 202 || status === 204 || status === 201 || status === 200) return false;
  if (status === 401 || status === 429) return false;
  if (status === 408 || status === 0 || status >= 500) return true;
  return false;
}

async function callStep(page, step) {
  const attempts = ATTEMPTS[step.command] || 1;
  let last = null;
  let attempt = 0;
  while (attempt < attempts) {
    attempt += 1;
    try {
      last = await page.evaluate(uploadStepInPage, step);
    } catch (error) {
      if (attempt === attempts) throw error;
      continue;
    }
    if (!shouldRetry(last)) return last;
  }
  return last;
}

function requireOk(command, result) {
  if (!result || typeof result !== "object") throw new Error(`${command} returned no response`);
  const status = Number(result.status) || 0;
  const expected = EXPECTED[command];
  if (status === 401) {
    const error = new Error(`${command} failed (HTTP 401): X login required in Ego Lite`);
    error.loginRequired = true;
    throw error;
  }
  if (status === 429) throw new Error(`${command} failed (HTTP 429): rate limited by X. Not retried.`);
  if (status !== expected) {
    const detail = clipUploadBody(result.body);
    throw new Error(detail ? `${command} failed (HTTP ${status}): ${detail}` : `${command} failed (HTTP ${status})`);
  }
  if (command === "APPEND") return {};
  if (result.body == null || result.body === "") throw new Error(`${command} returned an empty body`);
  const parsed = parseMediaJson(result.body);
  if (!parsed) throw new Error(`${command} returned non-JSON`);
  return parsed;
}

async function waitUntilReady(page, payload, mediaId, auth, sleep) {
  let info = payload && payload.processing_info;
  if (!info) return;
  let polls = 0;
  while (info.state === "pending" || info.state === "in_progress") {
    if (polls >= MAX_STATUS_POLLS) throw new Error("media processing timed out");
    const seconds = Number(info.check_after_secs);
    const waitMs = (Number.isFinite(seconds) && seconds >= 0 ? seconds : 10) * 1000;
    await sleep(waitMs);
    const status = await callStep(page, {
      command: "STATUS",
      method: "GET",
      url: statusUrl(mediaId),
      authorization: auth.authorization,
      csrfToken: auth.csrfToken,
    });
    const body = requireOk("STATUS", status);
    polls += 1;
    if (!body.processing_info) return;
    info = body.processing_info;
  }
  if (info.state === "succeeded") return;
  if (info.state === "failed") throw new Error(processingErrorText(info));
  throw new Error(`media processing ended in ${info.state || "an unknown state"}`);
}

export async function uploadOneImage(page, image, options = {}) {
  if (!page || typeof page.evaluate !== "function") throw new Error("page.evaluate is required to upload images");
  if (!image || !image.data || !image.data.length) throw new Error(`Image is empty: ${image && image.path ? image.path : ""}`.trim());
  if (Number(image.bytes) !== image.data.length) {
    throw new Error(`Image byte count does not match the buffer: ${image.path}`);
  }
  const md5 = String(image.md5 || "").toLowerCase();
  if (!/^[a-f0-9]{32}$/.test(md5)) throw new Error(`Image md5 is missing: ${image.path}`);
  if (!/^image\/(png|jpeg|webp)$/.test(String(image.mediaType || ""))) {
    throw new Error(`Unsupported image type for ${image.path}. Use png, jpeg, or webp.`);
  }
  const auth = buildUploadHeaders(options);
  const sleep = options.sleep || defaultSleep;
  const slices = segmentSlices(image.data, options.chunkBytes);
  const init = await callStep(page, {
    command: "INIT",
    method: "POST",
    url: initUrl({ totalBytes: image.bytes, mediaType: image.mediaType }),
    authorization: auth.authorization,
    csrfToken: auth.csrfToken,
  });
  const initBody = requireOk("INIT", init);
  const mediaId = mediaIdFrom(initBody);
  if (!mediaId) throw new Error("INIT response had no media_id_string");
  for (const slice of slices) {
    const appended = await callStep(page, {
      command: "APPEND",
      method: "POST",
      url: appendUrl({ mediaId, segmentIndex: slice.index }),
      b64: slice.b64,
      authorization: auth.authorization,
      csrfToken: auth.csrfToken,
    });
    requireOk("APPEND", appended);
  }
  const finalized = await callStep(page, {
    command: "FINALIZE",
    method: "POST",
    url: finalizeUrl({ mediaId, md5 }),
    authorization: auth.authorization,
    csrfToken: auth.csrfToken,
  });
  const finalBody = requireOk("FINALIZE", finalized);
  const finalId = mediaIdFrom(finalBody) || mediaId;
  await waitUntilReady(page, finalBody, finalId, auth, sleep);
  return finalId;
}

export async function uploadImagesOnPage(page, request = {}) {
  const images = request.images || [];
  const uploaded = [];
  for (const image of images) {
    try {
      const mediaId = await uploadOneImage(page, image, request);
      uploaded.push({ path: image.path, media_id: mediaId, bytes: image.bytes });
    } catch (error) {
      const message = error && error.message ? error.message : String(error);
      const extra = uploaded.length
        ? " An earlier image was uploaded and was not attached; it expires in about 24 hours."
        : "";
      const wrapped = new Error(`${image && image.path ? image.path : "image"}: ${message}${extra}`);
      if (error && error.loginRequired) wrapped.loginRequired = true;
      throw wrapped;
    }
  }
  return uploaded;
}
