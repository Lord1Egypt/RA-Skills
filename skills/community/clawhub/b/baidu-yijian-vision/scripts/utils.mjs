#!/usr/bin/env node

import https from 'https';
import http from 'http';

/**
 * Make an HTTPS (or HTTP) request. Returns a Promise that resolves to { statusCode, headers, body }.
 */
export function httpsRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const mod = parsedUrl.protocol === 'https:' ? https : http;
    const reqOptions = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
      path: parsedUrl.pathname + parsedUrl.search,
      method: options.method || 'GET',
      headers: options.headers || {},
    };

    const req = mod.request(reqOptions, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        const body = Buffer.concat(chunks).toString('utf-8');
        resolve({ statusCode: res.statusCode, headers: res.headers, body });
      });
    });

    const timeout = options.timeout || 30000;
    req.setTimeout(timeout, () => {
      req.destroy(new Error(`Request timed out after ${timeout}ms`));
    });

    req.on('error', reject);

    if (options.body) {
      req.write(options.body);
    }
    req.end();
  });
}

/**
 * Get the API key from environment. Throws if not set.
 */
export function getApiKey() {
  const key = process.env.YIJIAN_API_KEY;
  if (!key) {
    throw new Error('YIJIAN_API_KEY environment variable is not set. Please configure it in ~/.claude/settings.json under "env".');
  }
  return key;
}

/**
 * Validate that a path segment contains only safe characters.
 * Prevents path traversal attacks (e.g., "../admin") in URL construction.
 */
function validatePathSegment(id, label = 'id') {
  if (!id || /^\.{1,2}$/.test(id) || !/^[\w.-]+$/.test(id)) {
    throw new Error(`Invalid ${label}: ${id}`);
  }
}

/**
 * Construct the metadata URL for a given ep-id.
 */
export function metadataUrl(epId) {
  validatePathSegment(epId, 'epId');
  return `https://yijian-next.cloud.baidu.com/api/skills/v1/${epId}/metadata`;
}

/**
 * Construct the run URL for a given ep-id.
 */
export function runUrl(epId) {
  validatePathSegment(epId, 'epId');
  return `https://yijian-next.cloud.baidu.com/api/skills/v1/${epId}/run`;
}

/**
 * Construct the router query URL for intent-based skill matching.
 */
export function routerQueryUrl() {
  return 'https://yijian.baidubce.com/harness/v1/router/query';
}

/**
 * Construct the router multimodal URL for direct inference.
 */
export function routerMultimodalUrl() {
  return 'https://yijian.baidubce.com/harness/v1/router/multimodal';
}

/**
 * Construct the workspaces get URL.
 */
export function workspacesGetUrl() {
  return 'https://yijian-next.cloud.baidu.com/api/vistudio/v1/workspaces/get';
}

/**
 * Construct the workspace skills get URL.
 */
export function workspaceSkillsGetUrl(workspaceId) {
  validatePathSegment(workspaceId, 'workspaceId');
  return `https://yijian-next.cloud.baidu.com/api/vistudio/v1/workspaces/${workspaceId}/skills/get`;
}

/**
 * Read all stdin as a string (for piped input).
 */
export function readStdin() {
  return new Promise((resolve, reject) => {
    const chunks = [];
    process.stdin.setEncoding('utf-8');
    process.stdin.on('data', (chunk) => chunks.push(chunk));
    process.stdin.on('end', () => resolve(chunks.join('')));
    process.stdin.on('error', reject);
  });
}

/**
 * Parse named CLI flags from argv.
 * Returns { positional: string[], flags: Record<string, string> }.
 */
export function parseArgs(argv) {
  const positional = [];
  const flags = {};
  let i = 0;
  while (i < argv.length) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      if (i + 1 < argv.length && !argv[i + 1].startsWith('--')) {
        flags[key] = argv[i + 1];
        i += 2;
      } else {
        flags[key] = true;
        i += 1;
      }
    } else {
      positional.push(argv[i]);
      i += 1;
    }
  }
  return { positional, flags };
}

/**
 * Escape XML special characters for safe SVG embedding.
 */
export function escapeXml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

/**
 * Truncate a response body for safe inclusion in error messages.
 * Prevents credential/internal info leaks in logs and console output.
 */
export function truncateBody(body, maxLen = 200) {
  if (!body || body.length <= maxLen) return body;
  return body.slice(0, maxLen) + '...';
}
