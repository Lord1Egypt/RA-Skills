#!/usr/bin/env node

const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const IMAGE_CONTENT_TYPE_EXT = {
  "image/png": ".png",
  "image/jpeg": ".jpg",
  "image/jpg": ".jpg",
  "image/webp": ".webp",
  "image/gif": ".gif",
  "image/bmp": ".bmp",
  "image/svg+xml": ".svg",
};

const IMAGE_EXTS = new Set([".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg"]);

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function sha256(input) {
  return crypto.createHash("sha256").update(input).digest("hex");
}

function readText(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

function parseArgs(argv) {
  const args = [...argv];
  let mode = "generic";
  for (let i = 0; i < args.length; i += 1) {
    if (args[i] === "--mode") {
      mode = args[i + 1] || "generic";
      args.splice(i, 2);
      i -= 2;
    }
  }
  if (args.length !== 2) {
    fail("usage: prepare_task_assets.js <source-file> <task-dir> [--mode <ppt|beamer|generic>]");
  }
  return {
    sourceFile: path.resolve(args[0]),
    taskDir: path.resolve(args[1]),
    mode,
  };
}

function extractMarkdownImages(text) {
  const matches = [];
  const regex = /!\[([^\]]*)\]\((https?:\/\/[^\s)]+)(?:\s+"[^"]*")?\)/g;
  let match;
  let order = 0;
  while ((match = regex.exec(text)) !== null) {
    order += 1;
    matches.push({
      order,
      alt: String(match[1] || "").trim(),
      url: String(match[2] || "").trim(),
      source_excerpt: String(match[0] || "").slice(0, 240),
    });
  }
  return matches;
}

function looksDecorative(asset) {
  const sample = `${asset.alt || ""} ${asset.url || ""}`.toLowerCase();
  return /(author|avatar|logo|icon|badge|emoji|favicon|profile|headshot)/i.test(sample);
}

function inferExt(url, contentType) {
  const cleanType = String(contentType || "").split(";")[0].trim().toLowerCase();
  if (IMAGE_CONTENT_TYPE_EXT[cleanType]) {
    return IMAGE_CONTENT_TYPE_EXT[cleanType];
  }
  try {
    const pathname = new URL(url).pathname;
    const ext = path.extname(pathname).toLowerCase();
    if (IMAGE_EXTS.has(ext)) {
      return ext === ".jpeg" ? ".jpg" : ext;
    }
  } catch {
    // ignore
  }
  return ".bin";
}

async function fetchBuffer(url) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 60000);
  try {
    const response = await fetch(url, {
      redirect: "follow",
      signal: controller.signal,
      headers: {
        "user-agent": "openclaw-pipeline/prepare-task-assets",
      },
    });
    if (!response.ok) {
      throw new Error(`http ${response.status}`);
    }
    const arrayBuffer = await response.arrayBuffer();
    return {
      buffer: Buffer.from(arrayBuffer),
      contentType: response.headers.get("content-type") || "",
      finalUrl: response.url || url,
    };
  } finally {
    clearTimeout(timer);
  }
}

function writeJson(filePath, payload) {
  ensureDir(path.dirname(filePath));
  fs.writeFileSync(filePath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function copyFile(src, dest) {
  ensureDir(path.dirname(dest));
  fs.copyFileSync(src, dest);
}

async function main() {
  const { sourceFile, taskDir, mode } = parseArgs(process.argv.slice(2));
  if (!fs.existsSync(sourceFile)) {
    fail(`source file not found: ${sourceFile}`);
  }
  ensureDir(taskDir);

  const text = readText(sourceFile);
  const discovered = extractMarkdownImages(text);
  const taskScope = sha256(taskDir).slice(0, 16);
  const figuresDir = path.join(taskDir, "figures");
  const cacheDir = path.join(taskDir, "_asset_cache", taskScope);
  const manifestPath = path.join(taskDir, "asset_manifest.json");
  ensureDir(figuresDir);
  ensureDir(cacheDir);

  const seenUrls = new Map();
  const items = [];

  for (const asset of discovered) {
    const urlHash = sha256(asset.url);
    const entry = {
      index: asset.order,
      mode,
      task_scope: taskScope,
      alt: asset.alt,
      url: asset.url,
      url_hash: urlHash,
      source_excerpt: asset.source_excerpt,
      status: "pending",
      cache: {
        task_scope: taskScope,
        url_hash: urlHash,
        file_sha256: null,
      },
      local_path: null,
      cache_path: null,
      duplicate_of: null,
      error: null,
    };

    if (looksDecorative(asset)) {
      entry.status = "skipped";
      entry.error = "decorative_inline_image";
      items.push(entry);
      continue;
    }

    if (seenUrls.has(asset.url)) {
      const original = seenUrls.get(asset.url);
      entry.status = "duplicate";
      entry.duplicate_of = original.index;
      entry.local_path = original.local_path;
      entry.cache_path = original.cache_path;
      entry.cache.file_sha256 = original.cache.file_sha256;
      items.push(entry);
      continue;
    }

    const urlMetaPath = path.join(cacheDir, `${urlHash}.json`);
    try {
      let cachedMeta = null;
      if (fs.existsSync(urlMetaPath)) {
        try {
          cachedMeta = JSON.parse(readText(urlMetaPath));
        } catch {
          cachedMeta = null;
        }
      }

      let cachePath = cachedMeta?.cache_path || null;
      let fileSha = cachedMeta?.file_sha256 || null;
      let finalUrl = cachedMeta?.final_url || asset.url;
      let ext = cachedMeta?.ext || null;

      if (!cachePath || !fs.existsSync(cachePath)) {
        const fetched = await fetchBuffer(asset.url);
        finalUrl = fetched.finalUrl;
        fileSha = sha256(fetched.buffer);
        ext = inferExt(finalUrl, fetched.contentType);
        cachePath = path.join(cacheDir, `${urlHash}_${fileSha.slice(0, 12)}${ext}`);
        fs.writeFileSync(cachePath, fetched.buffer);
        writeJson(urlMetaPath, {
          url: asset.url,
          final_url: finalUrl,
          url_hash: urlHash,
          file_sha256: fileSha,
          ext,
          cache_path: cachePath,
          task_scope: taskScope,
        });
      }

      const localPath = path.join(figuresDir, `fig${String(asset.order).padStart(2, "0")}${ext || path.extname(cachePath) || ".bin"}`);
      copyFile(cachePath, localPath);
      entry.status = "success";
      entry.local_path = localPath;
      entry.cache_path = cachePath;
      entry.cache.file_sha256 = fileSha;
      entry.final_url = finalUrl;
      seenUrls.set(asset.url, entry);
    } catch (error) {
      entry.status = "failed";
      entry.error = error instanceof Error ? error.message : String(error);
    }

    items.push(entry);
  }

  const summary = {
    source_file: sourceFile,
    task_dir: taskDir,
    mode,
    task_scope: taskScope,
    generated_at: new Date().toISOString(),
    counts: {
      discovered: discovered.length,
      success: items.filter((item) => item.status === "success").length,
      failed: items.filter((item) => item.status === "failed").length,
      skipped: items.filter((item) => item.status === "skipped").length,
      duplicate: items.filter((item) => item.status === "duplicate").length,
    },
    items,
  };

  writeJson(manifestPath, summary);

  process.stdout.write([
    `asset_manifest: ${manifestPath}`,
    `task_scope: ${taskScope}`,
    `discovered: ${summary.counts.discovered}`,
    `success: ${summary.counts.success}`,
    `failed: ${summary.counts.failed}`,
    `skipped: ${summary.counts.skipped}`,
    `duplicate: ${summary.counts.duplicate}`,
  ].join("\n") + "\n");
}

main().catch((error) => fail(error instanceof Error ? error.stack || error.message : String(error)));
