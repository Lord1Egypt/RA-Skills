/**
 * utils.js — Utility functions for diff-wizard
 *
 * Provides encoding detection, Levenshtein distance, truncation helpers,
 * and safe file size checking.
 */

'use strict';

const fs = require('fs');
const path = require('path');

/**
 * Levenshtein distance between two strings.
 * @param {string} a
 * @param {string} b
 * @returns {number}
 */
function levenshtein(a, b) {
  const m = a.length, n = b.length;
  const dp = Array.from({ length: m + 1 }, () => new Uint16Array(n + 1));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i - 1] === b[j - 1]
        ? dp[i - 1][j - 1]
        : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }
  return dp[m][n];
}

/**
 * Find the closest matching path for a given input path.
 * @param {string} inputPath - The path the user provided
 * @param {string[]} candidates - List of actual paths on disk
 * @returns {string|null} - The best match or null
 */
function findClosestPath(inputPath, candidates) {
  if (!candidates || candidates.length === 0) return null;
  let best = null;
  let bestScore = Infinity;
  for (const c of candidates) {
    const score = levenshtein(inputPath, c);
    if (score < bestScore) {
      bestScore = score;
      best = c;
    }
  }
  return bestScore <= 5 ? best : null;
}

/**
 * Truncate a string to maxChars with an ellipsis indicator.
 * @param {string} str
 * @param {number} maxChars
 * @returns {string}
 */
function truncate(str, maxChars = 4000) {
  if (!str || str.length <= maxChars) return str;
  return str.slice(0, maxChars) + '\n\n... [truncated]';
}

/**
 * Check if file size exceeds limit.
 * @param {string} filePath
 * @param {number} maxMB
 * @returns {{ ok: boolean, sizeBytes: number, sizeMB: number }}
 */
function checkFileSize(filePath, maxMB = 100) {
  const stat = fs.statSync(filePath);
  const sizeBytes = stat.size;
  const sizeMB = sizeBytes / (1024 * 1024);
  return { ok: sizeMB <= maxMB, sizeBytes, sizeMB: Math.round(sizeMB * 100) / 100 };
}

/**
 * Detect encoding of a Buffer. Tries UTF-8, GBK, UTF-16.
 * @param {Buffer} buf
 * @returns {string}
 */
function detectEncoding(buf) {
  // UTF-16 BOM
  if (buf.length >= 2) {
    if (buf[0] === 0xFE && buf[1] === 0xFF) return 'utf16be';
    if (buf[0] === 0xFF && buf[1] === 0xFE) return 'utf16le';
  }
  // UTF-8 BOM
  if (buf.length >= 3 && buf[0] === 0xEF && buf[1] === 0xBB && buf[2] === 0xBF) return 'utf-8';
  // Try to decode as UTF-8, fallback to GBK
  try {
    const decoded = buf.toString('utf-8');
    // Check for invalid UTF-8 sequences
    if (decoded.includes('\uFFFD')) return 'gbk';
    return 'utf-8';
  } catch {
    return 'gbk';
  }
}

/**
 * Safe path resolve: prevent path traversal outside base directory.
 * @param {string} baseDir
 * @param {string} targetPath
 * @returns {{ ok: boolean, resolved: string|null, error: string|null }}
 */
function safeResolve(baseDir, targetPath) {
  const resolved = path.resolve(baseDir, targetPath);
  if (!resolved.startsWith(path.resolve(baseDir))) {
    return { ok: false, resolved: null, error: 'Path traversal detected: ' + targetPath };
  }
  return { ok: true, resolved, error: null };
}

/**
 * SHA-256 hex hash of a file for identity check.
 * @param {string} filePath
 * @returns {string}
 */
function fileHash(filePath) {
  const crypto = require('crypto');
  const content = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(content).digest('hex');
}

/**
 * Compute SHA-256 hash of a string.
 * @param {string} str
 * @returns {string}
 */
function stringHash(str) {
  const crypto = require('crypto');
  return crypto.createHash('sha256').update(str, 'utf-8').digest('hex');
}

/**
 * Parse comma-separated exclude patterns.
 * @param {string} patternsStr
 * @returns {string[]}
 */
function parseExcludePatterns(patternsStr) {
  if (!patternsStr) return [];
  return patternsStr.split(',').map(s => s.trim()).filter(Boolean);
}

module.exports = {
  levenshtein,
  findClosestPath,
  truncate,
  checkFileSize,
  detectEncoding,
  safeResolve,
  fileHash,
  stringHash,
  parseExcludePatterns,
};
