// Resolve a Markdown file and its images into a portable article model.
// Remote images are the ones already referenced by the article. They are
// written under the skill state directory and then uploaded through the editor.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { buildArticle, parseMarkdown, sniffImage, IMAGE_MAX_BYTES } from "./pure.mjs";

function sha256(buffer) {
  return crypto.createHash("sha256").update(buffer).digest("hex");
}

export function withinRoot(file, root) {
  const abs = path.resolve(file);
  const base = path.resolve(root);
  return abs === base || abs.startsWith(base + path.sep);
}

export function classifyImageRef(markdownPath, raw, assetRoot = "") {
  const ref = String(raw || "").trim();
  if (/^https?:\/\//i.test(ref)) return { remote: ref };
  if (/^[a-z]+:/i.test(ref)) throw new Error(`unsupported image reference: ${ref}`);
  const markdownDir = path.dirname(path.resolve(markdownPath));
  if (path.isAbsolute(ref)) return { local: path.resolve(ref) };
  const abs = path.resolve(markdownDir, ref);
  const roots = [markdownDir, assetRoot].filter(Boolean);
  if (!roots.some((root) => withinRoot(abs, root))) {
    throw new Error(`image path escapes the article directory: ${ref}`);
  }
  return { local: abs };
}

async function readLocal(file, fsImpl) {
  const buf = await fsImpl.promises.readFile(file);
  if (buf.length > IMAGE_MAX_BYTES) throw new Error(`image exceeds ${IMAGE_MAX_BYTES} bytes: ${path.basename(file)}`);
  const type = sniffImage(buf);
  if (!type) throw new Error(`not an image file: ${path.basename(file)}`);
  return { buf, type };
}

async function downloadRemote(url, fetchImpl) {
  const response = await fetchImpl(url, { redirect: "follow" });
  if (!response.ok) throw new Error(`image download failed (${response.status}): ${url}`);
  const announced = Number(response.headers && response.headers.get ? response.headers.get("content-length") : 0);
  if (announced > IMAGE_MAX_BYTES) throw new Error(`image exceeds ${IMAGE_MAX_BYTES} bytes`);
  const buf = Buffer.from(await response.arrayBuffer());
  if (buf.length > IMAGE_MAX_BYTES) throw new Error(`image exceeds ${IMAGE_MAX_BYTES} bytes`);
  const type = sniffImage(buf);
  if (!type) throw new Error(`downloaded file is not an image: ${url}`);
  return { buf, type };
}

export async function prepareArticle(options) {
  const fsImpl = options.fsImpl || fs;
  const fetchImpl = options.fetchImpl === undefined ? globalThis.fetch : options.fetchImpl;
  const markdownPath = options.markdownPath;
  if (!markdownPath) return { ok: false, error: "--markdown is required" };
  let source = "";
  try {
    source = await fsImpl.promises.readFile(markdownPath, "utf8");
  } catch (error) {
    return { ok: false, error: `cannot read markdown: ${error.message}` };
  }
  const parsed = parseMarkdown(source);
  const refs = parsed.blocks.filter((block) => block.type === "image");
  const assetDir = options.assetDir;
  if (refs.length && assetDir) await fsImpl.promises.mkdir(assetDir, { recursive: true });
  const images = [];
  try {
    for (let index = 0; index < refs.length; index += 1) {
      const block = refs[index];
      const classified = classifyImageRef(markdownPath, block.src, options.assetRoot || "");
      let stored;
      let remote = "";
      if (classified.remote) {
        if (typeof fetchImpl !== "function") return { ok: false, error: "fetch is unavailable for remote images" };
        stored = await downloadRemote(classified.remote, fetchImpl);
        remote = classified.remote;
      } else {
        stored = await readLocal(classified.local, fsImpl);
      }
      const sum = sha256(stored.buf);
      const ext = stored.type === "image/png" ? "png"
        : stored.type === "image/gif" ? "gif"
          : stored.type === "image/webp" ? "webp" : "jpg";
      let filePath = classified.local;
      if (classified.remote) {
        filePath = path.join(assetDir, `${String(index).padStart(2, "0")}-${sum.slice(0, 12)}.${ext}`);
        await fsImpl.promises.writeFile(filePath, stored.buf);
      }
      images.push({
        alt: block.alt,
        name: path.basename(filePath),
        path: filePath,
        bytes: stored.buf.length,
        sha256: sum,
        remote: remote || "",
      });
    }
  } catch (error) {
    return { ok: false, error: error.message };
  }
  const article = buildArticle({
    parsed,
    images,
    title: options.title || "",
    digest: options.digest || "",
    sourceUrl: options.sourceUrl || "",
  });
  if (!article.ok) return article;
  return { ok: true, article };
}

export function receiptFile(dir, hash) {
  return path.join(dir, `${hash}.json`);
}

export function createReceiptStore(fsImpl = fs) {
  return {
    read(dir, hash) {
      if (!dir || !hash) return null;
      const file = receiptFile(dir, hash);
      if (!fsImpl.existsSync(file)) return null;
      try {
        return JSON.parse(fsImpl.readFileSync(file, "utf8"));
      } catch {
        return { hash, status: "uncertain", unreadable: true };
      }
    },
    write(dir, receipt) {
      fsImpl.mkdirSync(dir, { recursive: true });
      const file = receiptFile(dir, receipt.hash);
      fsImpl.writeFileSync(file, `${JSON.stringify(receipt, null, 2)}\n`, { mode: 0o600 });
      return file;
    },
  };
}
