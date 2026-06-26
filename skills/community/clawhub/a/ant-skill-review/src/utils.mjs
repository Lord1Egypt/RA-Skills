import { readdirSync } from "node:fs";
import { join } from "node:path";

/**
 * Format a Buffer region as a standard hexdump.
 *
 * Output format per line:
 *   offset: aabb ccdd eeff ... | ascii.text.. |
 *
 * @param {Buffer} buf    - source buffer
 * @param {number} [start=0]  - byte offset to start from
 * @param {number} [length]   - number of bytes to dump (default: buf.length - start)
 * @param {number} [cols=16]  - bytes per line
 * @returns {string[]} array of formatted lines
 */
export function hexdump(buf, start = 0, length, cols = 16) {
  const end = Math.min(buf.length, start + (length ?? buf.length - start));
  const lines = [];
  for (let off = start; off < end; off += cols) {
    const slice = buf.subarray(off, Math.min(off + cols, end));
    const hex = Array.from(slice).map(b => b.toString(16).padStart(2, "0")).join(" ");
    const ascii = Array.from(slice).map(b => (b >= 0x20 && b <= 0x7e) ? String.fromCharCode(b) : ".").join("");
    lines.push(`${off.toString(16).padStart(8, "0")}: ${hex.padEnd(cols * 3 - 1)}  | ${ascii} |`);
  }
  return lines;
}

/**
 * Format file permission mode as rwx string (e.g. "-rwxr-xr-x").
 */
export function formatMode(mode) {
  const r = (m) => (mode & m ? "r" : "-");
  const w = (m) => (mode & m ? "w" : "-");
  const x = (m) => (mode & m ? "x" : "-");
  return (
    (mode & 0o40000 ? "d" : "-") +
    r(0o400) + w(0o200) + x(0o100) +
    r(0o040) + w(0o020) + x(0o010) +
    r(0o004) + w(0o002) + x(0o001)
  );
}

/**
 * Format byte size as human-readable string (e.g. "1.2 KB", "3.4 MB").
 */
export function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

/**
 * Recursively walk a directory, calling callback(dir, fileNames) for each.
 * Symlinks are treated as files. Directories are visited depth-first.
 */
export function walkDir(dir, callback) {
  let entries;
  try { entries = readdirSync(dir, { withFileTypes: true }); } catch { return; }
  const dirs = [];
  const files = [];
  for (const ent of entries) {
    if (ent.isSymbolicLink()) {
      files.push(ent.name);
    } else if (ent.isDirectory()) {
      dirs.push(ent.name);
    } else {
      files.push(ent.name);
    }
  }
  files.sort();
  callback(dir, files);
  dirs.sort();
  for (const d of dirs) walkDir(join(dir, d), callback);
}

/**
 * Detect whether a Buffer contains binary (non-text) content.
 * Uses the same heuristic as git: check for NUL bytes in the first 8KB.
 */
export function isBinaryBuffer(buf) {
  const len = Math.min(buf.length, 8192);
  for (let i = 0; i < len; i++) {
    if (buf[i] === 0) return true;
  }
  return false;
}

/**
 * Fetch JSON from a URL with timeout. Follows redirects by default.
 */
export async function fetchJson(url, timeoutMs = 15_000) {
  const res = await fetch(url, { signal: AbortSignal.timeout(timeoutMs) });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.json();
}

/**
 * Extract printable ASCII strings (>= minLen chars) from a Buffer.
 * Returns at most maxCount strings.
 */
export function extractStrings(buf, minLen = 6, maxCount = 50) {
  const found = [];
  let cur = "";
  for (let i = 0; i < buf.length; i++) {
    const b = buf[i];
    if (b >= 0x20 && b <= 0x7e) { cur += String.fromCharCode(b); }
    else { if (cur.length >= minLen) found.push(cur); cur = ""; }
    if (found.length >= maxCount) break;
  }
  if (cur.length >= minLen && found.length < maxCount) found.push(cur);
  return found;
}
