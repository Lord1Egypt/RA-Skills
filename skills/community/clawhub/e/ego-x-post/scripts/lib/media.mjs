// Image attachment helpers for x-post. No browser and no network.
// The upload URL shape is the 2026-11-04 capture of upload.x.com. Do not add hosts or commands.

import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";

export const MAX_IMAGES = 4;
export const MAX_IMAGE_BYTES = 5 * 1024 * 1024;
export const CHUNK_BYTES = 1024 * 1024;
export const MAX_CHUNK_BYTES = 5 * 1024 * 1024;
export const UPLOAD_URL = "https://upload.x.com/i/media/upload.json";

const EXTENSIONS = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
};

const PROCESSING_ERRORS = {
  0: "INTERNAL_ERROR",
  1: "INVALID_MEDIA",
  2: "FILE_TOO_LARGE",
  3: "UNSUPPORTED_MEDIA",
  4: "TIMEOUT",
};

export function mediaTypeForName(filePath) {
  const ext = path.extname(String(filePath || "")).toLowerCase();
  if (ext === ".gif") {
    throw new Error("GIF is not supported (--image). Use png, jpeg, or webp. GIF needs media_category=tweet_gif and STATUS polling, which the 2026-11-04 capture did not verify.");
  }
  const mediaType = EXTENSIONS[ext];
  if (!mediaType) throw new Error(`Unsupported image type for ${filePath || "(empty)"}. Use png, jpeg, or webp.`);
  return mediaType;
}

export function magicMatches(data, mediaType) {
  if (!data || data.length == null) return false;
  const bytes = Buffer.from(data);
  if (mediaType === "image/png") {
    return bytes.length >= 8
      && bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47
      && bytes[4] === 0x0d && bytes[5] === 0x0a && bytes[6] === 0x1a && bytes[7] === 0x0a;
  }
  if (mediaType === "image/jpeg") {
    return bytes.length >= 3 && bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff;
  }
  if (mediaType === "image/webp") {
    return bytes.length >= 12
      && bytes.subarray(0, 4).toString("ascii") === "RIFF"
      && bytes.subarray(8, 12).toString("ascii") === "WEBP";
  }
  return false;
}

export function clampChunkBytes(value) {
  const requested = Number(value);
  if (!Number.isFinite(requested) || requested <= 0) return CHUNK_BYTES;
  return Math.min(Math.floor(requested), MAX_CHUNK_BYTES);
}

export function segmentSlices(buffer, chunkBytes = CHUNK_BYTES) {
  const size = clampChunkBytes(chunkBytes);
  const bytes = Buffer.from(buffer || []);
  const slices = [];
  for (let start = 0; start < bytes.length; start += size) {
    const end = Math.min(bytes.length, start + size);
    slices.push({
      index: slices.length,
      b64: bytes.subarray(start, end).toString("base64"),
    });
  }
  return slices;
}

function uploadQuery(params) {
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) query.set(key, String(value));
  return `${UPLOAD_URL}?${query.toString()}`;
}

export function initUrl({ totalBytes, mediaType }) {
  return uploadQuery({
    command: "INIT",
    total_bytes: totalBytes,
    media_type: mediaType,
    media_category: "tweet_image",
  });
}

export function appendUrl({ mediaId, segmentIndex }) {
  return uploadQuery({
    command: "APPEND",
    media_id: mediaId,
    segment_index: segmentIndex,
  });
}

export function finalizeUrl({ mediaId, md5 }) {
  return uploadQuery({
    command: "FINALIZE",
    media_id: mediaId,
    original_md5: String(md5 || "").toLowerCase(),
  });
}

export function statusUrl(mediaId) {
  return uploadQuery({ command: "STATUS", media_id: mediaId });
}

export function parseMediaJson(body) {
  if (body == null || body === "") return null;
  if (typeof body === "object") return Array.isArray(body) ? null : body;
  try {
    const parsed = JSON.parse(String(body));
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return null;
    return parsed;
  } catch {
    return null;
  }
}

export function mediaIdFrom(payload) {
  const id = payload && payload.media_id_string;
  return typeof id === "string" && /^\d{1,25}$/.test(id) ? id : "";
}

export function processingErrorText(info) {
  const code = info && info.error ? info.error.code : undefined;
  if (code == null || code === "") return "media processing FAILED (code ?)";
  const named = Object.prototype.hasOwnProperty.call(PROCESSING_ERRORS, Number(code))
    ? PROCESSING_ERRORS[Number(code)]
    : "FAILED";
  return `media processing ${named} (code ${code})`;
}

export function clipUploadBody(body) {
  const text = typeof body === "string" ? body : body == null ? "" : JSON.stringify(body);
  const value = text.replace(/\s+/g, " ").trim();
  if (!value) return "";
  return value.length > 300 ? `${value.slice(0, 300)}...` : value;
}

export async function describeImages(paths, fileSystem = fs) {
  if (!Array.isArray(paths)) throw new Error("--image expects file paths");
  if (paths.length > MAX_IMAGES) throw new Error(`At most ${MAX_IMAGES} --image files`);
  const described = [];
  for (const input of paths) {
    const requested = String(input || "").trim();
    if (!requested) throw new Error("Missing value for --image");
    const mediaType = mediaTypeForName(requested);
    const resolved = path.resolve(requested);
    let info;
    try {
      info = await fileSystem.stat(resolved);
    } catch (error) {
      const code = error && error.code;
      if (code === "ENOENT") throw new Error(`Image not found: ${requested}`);
      throw new Error(`Image not readable: ${requested}${code ? ` (${code})` : ""}`);
    }
    if (!info || typeof info.isFile !== "function" || !info.isFile()) {
      throw new Error(`Image is not a file: ${requested}`);
    }
    const size = Number(info.size);
    if (!Number.isFinite(size) || size < 0) throw new Error(`Image size is unusable: ${requested}`);
    if (size === 0) throw new Error(`Image is empty: ${requested}`);
    if (size > MAX_IMAGE_BYTES) {
      throw new Error(`Image exceeds 5 MiB (${MAX_IMAGE_BYTES} bytes): ${requested} is ${size} bytes`);
    }
    const data = await fileSystem.readFile(resolved);
    if (!data || data.length !== size) throw new Error(`Image size changed while reading: ${requested}`);
    if (!magicMatches(data, mediaType)) {
      throw new Error(`Image contents do not look like ${mediaType}: ${requested}`);
    }
    described.push({
      path: resolved,
      bytes: data.length,
      md5: crypto.createHash("md5").update(data).digest("hex"),
      mediaType,
      data,
    });
  }
  return described;
}
