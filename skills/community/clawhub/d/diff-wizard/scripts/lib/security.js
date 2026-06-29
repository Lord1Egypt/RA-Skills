/**
 * security.js — Security module for diff-wizard
 *
 * Handles sensitive file detection, credential redaction,
 * path sanitization, and output sanitization.
 */

'use strict';

const path = require('path');

// Patterns for sensitive file detection
const SENSITIVE_FILE_PATTERNS = [
  /\.env$/i,
  /credentials/i,
  /secret/i,
  /\.pem$/i,
  /\.key$/i,
  /^id_rsa/i,
  /\.pgp$/i,
  /\.gpg$/i,
  /passwd/i,
  /shadow/i,
  /tokens?\b/i,
  /\.htpasswd$/i,
  /\.netrc$/i,
];

// Credential patterns to redact in AI explanation content
const CREDENTIAL_PATTERNS = [
  /(password|passwd|pwd)\s*[:=]\s*['"]?\S+['"]?/gi,
  /(secret)\s*[:=]\s*['"]?\S+['"]?/gi,
  /(token|api.?key|apikey|api_key)\s*[:=]\s*['"]?\S+['"]?/gi,
  /(auth|authorization)\s*[:=]\s*['"]?\S+['"]?/gi,
  /(access.?key|access_key|secret.?key|secret_key)\s*[:=]\s*['"]?\S+['"]?/gi,
  /(private.?key)\s*[:=]\s*['"]?\S+['"]?/gi,
  /(bearer)\s+\S+/gi,
  /(ghp_|gho_|ghu_|ghs_|ghr_)[\w-]+/g,          // GitHub tokens
  /(sk-[a-zA-Z0-9]{20,})/g,                         // OpenAI keys
  /(AKIA[0-9A-Z]{16})/g,                             // AWS access keys
  /-----BEGIN\s+(RSA |EC |DSA )?PRIVATE KEY-----/g,
];

// Paths permanently excluded from traversal
const SYSTEM_PATHS = new Set([
  '/System', '/bin', '/sbin', '/usr/bin', '/etc', '/dev', '/proc', '/core',
]);

/**
 * Check if a file path matches sensitive file patterns.
 * @param {string} filePath
 * @returns {{ sensitive: boolean, patterns: string[] }}
 */
function isSensitiveFile(filePath) {
  const basename = path.basename(filePath);
  const fullPath = filePath;
  const matched = [];
  for (const pat of SENSITIVE_FILE_PATTERNS) {
    if (pat.test(basename) || pat.test(fullPath)) {
      matched.push(pat.source);
    }
  }
  return { sensitive: matched.length > 0, patterns: matched };
}

/**
 * Redact credential patterns from a string.
 * @param {string} content
 * @returns {string}
 */
function redactCredentials(content) {
  if (!content) return content;
  let result = content;
  for (const pat of CREDENTIAL_PATTERNS) {
    result = result.replace(pat, (match) => {
      // Keep the key name but redact the value
      const idx = match.indexOf('=') > -1 ? match.indexOf('=') : match.indexOf(':');
      if (idx > -1) {
        return match.slice(0, idx + 1) + '***';
      }
      // For bearer tokens and API keys, replace completely
      if (/bearer/i.test(match) || /^sk-/.test(match) || /^AKIA/.test(match) || /^gh[pousr]_/.test(match)) {
        return match.slice(0, 6) + '***';
      }
      if (/BEGIN.*PRIVATE KEY/.test(match)) {
        return '-----BEGIN PRIVATE KEY----- [redacted]';
      }
      return match.slice(0, Math.min(match.length, 4)) + '***';
    });
  }
  return result;
}

/**
 * Validate that a path is safe to access.
 * @param {string} targetPath
 * @param {string} [baseDir=process.cwd()]
 * @param {boolean} [allowSystem=false]
 * @returns {{ ok: boolean, error: string|null }}
 */
function validatePath(targetPath, baseDir = process.cwd(), allowSystem = false) {
  const resolved = path.resolve(baseDir, targetPath);
  const base = path.resolve(baseDir);

  // Check system path exclusion
  if (!allowSystem) {
    for (const sysPath of SYSTEM_PATHS) {
      if (resolved.startsWith(sysPath)) {
        return { ok: false, error: `Access denied: "${sysPath}" is a system path` };
      }
    }
  }

  // Check path traversal
  if (!resolved.startsWith(base)) {
    return { ok: false, error: `Path traversal detected: "${targetPath}" escapes working directory` };
  }

  return { ok: true, error: null };
}

/**
 * Sanitize HTML output to prevent XSS.
 * @param {string} content
 * @returns {string}
 */
function sanitizeHtml(content) {
  if (!content) return '';
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '/': '&#x2F;',
  };
  return content.replace(/[&<>"'/]/g, (ch) => map[ch] || ch);
}

/**
 * Strip ANSI escape sequences (prevent injection in terminal output).
 * @param {string} content
 * @returns {string}
 */
function sanitizeTerminal(content) {
  if (!content) return '';
  // Only allow standard ANSI color codes, strip anything else
  return content.replace(/\x1b[^m]*m/g, (match) => {
    // Only allow color codes that match known patterns
    const validCodes = /^(?:\x1b\[3[0-7]m|\x1b\[4[0-7]m|\x1b\[1m|\x1b\[0m|\x1b\[7m|\x1b\[9[0-7]m|\x1b\[10[0-7]m|\x1b\[9[0-7];1m)$/;
    return validCodes.test(match) ? match : '';
  });
}

/**
 * Audit log for AI explanation requests.
 * @param {string} filePath
 * @param {number} hunksCount
 */
function auditAiRequest(filePath, hunksCount) {
  const ts = new Date().toISOString();
  const msg = `[AI-EXPLAIN] ${ts} | path: ${filePath} | hunks: ${hunksCount}`;
  // Write to stderr so it doesn't interfere with output
  process.stderr.write(msg + '\n');
}

module.exports = {
  isSensitiveFile,
  redactCredentials,
  validatePath,
  sanitizeHtml,
  sanitizeTerminal,
  auditAiRequest,
  SENSITIVE_FILE_PATTERNS,
};
