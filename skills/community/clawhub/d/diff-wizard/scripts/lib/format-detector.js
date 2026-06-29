/**
 * format-detector.js — Format auto-detection module for diff-wizard
 *
 * Detects file format by extension, then content signature, falling back to text.
 * Priority: Extension → Content signature → MIME (if available) → text
 */

'use strict';

const path = require('path');
const fs = require('fs');

// Extension → format mapping
const EXTENSION_MAP = {
  '.json': 'json',
  '.yaml': 'yaml',
  '.yml': 'yaml',
  '.toml': 'toml',
  '.csv': 'csv',
  '.tsv': 'tsv',
  '.xml': 'xml',
  '.html': 'html',
  '.htm': 'html',
  '.js': 'code',
  '.ts': 'code',
  '.jsx': 'code',
  '.tsx': 'code',
  '.py': 'code',
  '.rb': 'code',
  '.go': 'code',
  '.rs': 'code',
  '.java': 'code',
  '.c': 'code',
  '.cpp': 'code',
  '.h': 'code',
  '.hpp': 'code',
  '.cs': 'code',
  '.swift': 'code',
  '.kt': 'code',
  '.scala': 'code',
  '.php': 'code',
  '.sh': 'code',
  '.bash': 'code',
  '.zsh': 'code',
  '.pl': 'code',
  '.lua': 'code',
  '.r': 'code',
  '.sql': 'code',
  '.md': 'text',
  '.txt': 'text',
  '.cfg': 'text',
  '.conf': 'text',
  '.ini': 'text',
  '.properties': 'text',
  '.env': 'text',
  '.gitignore': 'text',
  '.dockerfile': 'text',
  'dockerfile': 'text',
  '.makefile': 'text',
  'makefile': 'text',
};

// Content-based signature patterns
const CONTENT_SIGNATURES = [
  { format: 'json', test: (s) => {
    const t = s.trim();
    return (t.startsWith('{') && t.endsWith('}')) || (t.startsWith('[') && t.endsWith(']'));
  }},
  { format: 'yaml', test: (s) => /^---\s*\n/.test(s.trim()) || /^(\w[\w.]*:\s|-\s)/m.test(s.trim()) },
  { format: 'xml', test: (s) => /^\s*<[\w?]/.test(s) && /<\/[\w]+>\s*$/.test(s.trim()) },
  { format: 'html', test: (s) => /^<!DOCTYPE html/i.test(s.trim()) || /^<html/i.test(s.trim()) },
  { format: 'toml', test: (s) => /^\s*\[[\w.]+\]\s*\n/.test(s) || /^\s*\w+\s*[:=]\s*["\d]/.test(s) },
  { format: 'csv', test: (s) => {
    const lines = s.trim().split('\n');
    if (lines.length < 1) return false;
    const parts = lines[0].split(',');
    return parts.length >= 2 && lines.slice(1).some(l => l.split(',').length >= 2);
  }},
  { format: 'tsv', test: (s) => {
    const lines = s.trim().split('\n');
    if (lines.length < 1) return false;
    const parts = lines[0].split('\t');
    return parts.length >= 2 && lines.slice(1).some(l => l.split('\t').length >= 2);
  }},
];

/**
 * Detect format from a file path.
 * @param {string} filePath
 * @returns {{ format: string, confidence: number, source: string }}
 */
function detectFromPath(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const basename = path.basename(filePath).toLowerCase();

  // Check exact filename matches
  if (EXTENSION_MAP[basename]) {
    return { format: EXTENSION_MAP[basename], confidence: 0.95, source: 'filename' };
  }

  // Check extension
  if (EXTENSION_MAP[ext]) {
    return { format: EXTENSION_MAP[ext], confidence: 0.9, source: 'extension' };
  }

  return { format: 'text', confidence: 0.3, source: 'unknown-ext' };
}

/**
 * Detect format from content.
 * @param {string} content
 * @returns {{ format: string, confidence: number, source: string }}
 */
function detectFromContent(content) {
  if (!content || content.trim().length === 0) {
    return { format: 'text', confidence: 1.0, source: 'empty-content' };
  }

  for (const sig of CONTENT_SIGNATURES) {
    try {
      if (sig.test(content)) {
        return { format: sig.format, confidence: 0.85, source: 'content-signature' };
      }
    } catch {
      continue;
    }
  }

  return { format: 'text', confidence: 0.5, source: 'content-fallback' };
}

/**
 * Detect format from file path and content, merging results.
 * @param {string} filePath
 * @param {string} [content]
 * @returns {{ format: string, confidence: number, source: string }}
 */
function detectFormat(filePath, content) {
  const pathResult = detectFromPath(filePath);

  // If path detection is confident enough, use it
  if (pathResult.confidence >= 0.9 && pathResult.format !== 'text') {
    return pathResult;
  }

  // If content is available, check
  if (content) {
    const contentResult = detectFromContent(content);
    // Content detection overrides low-confidence path results
    if (contentResult.confidence > pathResult.confidence) {
      return contentResult;
    }
  }

  return pathResult;
}

/**
 * Read a file and detect its format.
 * @param {string} filePath
 * @param {object} [opts]
 * @param {number} [opts.maxSizeMB=100]
 * @returns {{ format: string, content: string, confidence: number, error: string|null }}
 */
function readAndDetect(filePath, opts = {}) {
  const maxMB = opts.maxSizeMB || 100;
  try {
    const stat = fs.statSync(filePath);
    const sizeMB = stat.size / (1024 * 1024);
    if (sizeMB > maxMB) {
      return { format: null, content: null, confidence: 0, error: `E002: File ${filePath} exceeds ${maxMB}MB limit (${sizeMB.toFixed(2)}MB)` };
    }

    const content = fs.readFileSync(filePath, 'utf-8');
    const detection = detectFormat(filePath, content);
    return { format: detection.format, content, confidence: detection.confidence, error: null };
  } catch (err) {
    if (err.code === 'ENOENT') {
      return { format: null, content: null, confidence: 0, error: `E001: File not found: ${filePath}` };
    }
    if (err.code === 'EACCES') {
      return { format: null, content: null, confidence: 0, error: `E003: Permission denied: ${filePath}` };
    }
    return { format: null, content: null, confidence: 0, error: `E009: Read error: ${filePath} — ${err.message}` };
  }
}

// Detect if content appears to be binary
const BINARY_MAGIC_BYTES = [
  [0x89, 0x50, 0x4E],       // PNG
  [0xFF, 0xD8, 0xFF],       // JPEG
  [0x47, 0x49, 0x46],       // GIF
  [0x42, 0x4D],             // BMP
  [0x25, 0x50, 0x44, 0x46], // PDF
  [0x50, 0x4B],             // ZIP/DOCX/XLSX
  [0x7F, 0x45, 0x4C, 0x46], // ELF
  [0xCA, 0xFE, 0xBA, 0xBE], // Mach-O (32-bit)
  [0xCF, 0xFA, 0xED, 0xFE], // Mach-O (64-bit)
  [0x00, 0x00, 0x00],       // UTF-32 BOM / some binaries
];

/**
 * Check if a file is binary (based on magic bytes).
 * @param {string} filePath
 * @returns {boolean}
 */
function isBinaryFile(filePath) {
  try {
    const fd = fs.openSync(filePath, 'r');
    const buf = Buffer.alloc(4);
    const bytesRead = fs.readSync(fd, buf, 0, 4, 0);
    fs.closeSync(fd);

    if (bytesRead < 2) return false;

    for (const magic of BINARY_MAGIC_BYTES) {
      let match = true;
      for (let i = 0; i < magic.length && i < bytesRead; i++) {
        if (buf[i] !== magic[i]) { match = false; break; }
      }
      if (match) return true;
    }

    return false;
  } catch {
    return false;
  }
}

module.exports = {
  detectFormat,
  detectFromPath,
  detectFromContent,
  readAndDetect,
  isBinaryFile,
  EXTENSION_MAP,
};
