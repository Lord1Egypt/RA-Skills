#!/usr/bin/env node
/**
 * Localize images in a post directory: download URLs, copy local files, rewrite paths.
 * Usage: node scripts/image-localize.mjs <posts/<slug>>
 * Exit: 0 success / 1 any image failed / 2 post dir or article missing
 */
import { readFile, writeFile, copyFile, mkdir, stat } from 'node:fs/promises';
import { join, dirname, resolve, basename, extname, isAbsolute } from 'node:path';
import { createHash } from 'node:crypto';

function sha1short(s) {
  return createHash('sha1').update(s).digest('hex').slice(0, 8);
}

async function exists(p) { try { await stat(p); return true; } catch { return false; } }

function extFromContentType(ct) {
  if (!ct) return '.bin';
  const map = { 'image/jpeg': '.jpg', 'image/png': '.png', 'image/webp': '.webp', 'image/gif': '.gif', 'image/svg+xml': '.svg' };
  for (const k of Object.keys(map)) if (ct.includes(k)) return map[k];
  return '.bin';
}

async function downloadWithRetry(url, destPath, retries = 3) {
  let lastErr;
  for (let i = 0; i < retries; i++) {
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 15000);
      const res = await fetch(url, { signal: controller.signal });
      clearTimeout(timer);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const ext = extFromContentType(res.headers.get('content-type'));
      const actualPath = destPath.endsWith('.bin') ? destPath.replace(/\.bin$/, ext) : destPath;
      const buf = Buffer.from(await res.arrayBuffer());
      await writeFile(actualPath, buf);
      return actualPath;
    } catch (e) { lastErr = e; }
  }
  throw lastErr;
}

async function resolveImage(ref, mdxDir, imagesDir) {
  if (ref.startsWith('./images/') || ref.startsWith('images/')) return { skipped: true, newRef: ref };

  if (/^https?:\/\//.test(ref)) {
    const urlObj = new URL(ref);
    const bn = basename(urlObj.pathname) || 'img';
    const hash = sha1short(ref);
    const tempName = `${hash}-${bn.replace(/\.[^.]+$/, '')}.bin`;
    const destPath = join(imagesDir, tempName);
    const actualPath = await downloadWithRetry(ref, destPath);
    return { skipped: false, newRef: `./images/${basename(actualPath)}` };
  }

  const srcAbs = isAbsolute(ref) ? ref : resolve(mdxDir, ref);
  if (!await exists(srcAbs)) throw new Error(`Local file not found: ${srcAbs}`);
  const bn = basename(srcAbs);
  let destName = bn;
  let destPath = join(imagesDir, destName);
  if (await exists(destPath)) {
    const hash = sha1short(srcAbs);
    const ext = extname(bn);
    const stem = bn.slice(0, bn.length - ext.length);
    destName = `${stem}-${hash}${ext}`;
    destPath = join(imagesDir, destName);
  }
  await copyFile(srcAbs, destPath);
  return { skipped: false, newRef: `./images/${destName}` };
}

async function processFile(filePath, imagesDir) {
  if (!await exists(filePath)) return { touched: 0, failed: [] };
  let content = await readFile(filePath, 'utf8');
  const mdxDir = dirname(filePath);

  const mdRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
  const matches = [...content.matchAll(mdRegex)];
  const failed = [];
  let touched = 0;

  for (const m of matches) {
    const fullMatch = m[0];
    const alt = m[1];
    const ref = m[2];
    try {
      const { skipped, newRef } = await resolveImage(ref, mdxDir, imagesDir);
      if (!skipped) {
        content = content.replace(fullMatch, `![${alt}](${newRef})`);
        touched++;
      }
    } catch (e) {
      failed.push({ ref, error: e.message });
    }
  }

  await writeFile(filePath, content, 'utf8');
  return { touched, failed };
}

async function main() {
  const [, , postDir] = process.argv;
  if (!postDir) { console.error('Usage: node scripts/image-localize.mjs <post-dir>'); process.exit(2); }

  const absPostDir = resolve(postDir);
  if (!await exists(absPostDir)) { console.error(`Not found: ${absPostDir}`); process.exit(2); }

  const imagesDir = join(absPostDir, 'images');
  await mkdir(imagesDir, { recursive: true });

  const targets = [join(absPostDir, 'article.mdx'), join(absPostDir, 'source.md')];
  let totalTouched = 0;
  const allFailed = [];

  for (const t of targets) {
    const { touched, failed } = await processFile(t, imagesDir);
    totalTouched += touched;
    allFailed.push(...failed.map(f => ({ ...f, file: t })));
  }

  console.log(`图片本地化完成：${totalTouched} 张`);
  if (allFailed.length > 0) {
    console.error('失败清单：');
    for (const f of allFailed) console.error(`  - ${f.ref} (${f.file}): ${f.error}`);
    process.exit(1);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
