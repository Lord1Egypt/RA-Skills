'use strict';

const https = require('https');
const http = require('http');

/**
 * Resolve site origin (Convex / app) vs legacy API root (…/api).
 */
function getUrlConfig() {
  const site = (
    process.env.CLAWPRINT_SITE_URL ||
    process.env.NEXT_PUBLIC_CONVEX_SITE_URL ||
    ''
  )
    .trim()
    .replace(/\/$/, '');
  if (site) return { mode: 'site', base: site };
  const api = (process.env.CLAWPRINT_API_URL || 'https://clawprintai.com/api')
    .trim()
    .replace(/\/$/, '');
  return { mode: 'apiRoot', base: api };
}

/**
 * Build absolute URL for a Clawprint route.
 * Accepts "/api/products", "api/products", "/users", "users", etc.
 */
function buildClawprintUrl(path) {
  let p = String(path || '').trim() || '/api/products';
  if (!p.startsWith('/')) p = `/${p}`;
  const { mode, base } = getUrlConfig();
  if (mode === 'site') {
    if (p.startsWith('/api')) return base + p;
    return `${base}/api${p}`;
  }
  let rel = p.replace(/^\/+/, '');
  if (rel.startsWith('api/')) rel = rel.slice(4);
  return `${base}/${rel}`;
}

/**
 * HTTP request to Clawprint. Pass either `url` (absolute) or `path` (segment under /api).
 * When `auth` is true, sends X-Public-Key and X-Secret-Key if both resolve from args or env.
 */
function clawprintRequest({
  method = 'GET',
  path,
  url: absoluteUrl,
  body = null,
  auth = true,
  publicKey = null,
  secretKey = null,
  timeout = 30000,
}) {
  const href = absoluteUrl || buildClawprintUrl(path);
  const u = new URL(href);
  const isHttps = u.protocol === 'https:';
  const lib = isHttps ? https : http;
  const port = u.port || (isHttps ? 443 : 80);

  const headers = {
    Accept: 'application/json',
  };

  const pub =
    publicKey !== null && publicKey !== undefined
      ? publicKey
      : process.env.CLAWPRINT_PUBLIC_KEY;
  const sec =
    secretKey !== null && secretKey !== undefined
      ? secretKey
      : process.env.CLAWPRINT_SECRET_KEY;
  const pubTrim = typeof pub === 'string' ? pub.trim() : '';
  const secTrim = typeof sec === 'string' ? sec.trim() : '';
  if (auth && pubTrim && secTrim) {
    headers['X-Public-Key'] = pubTrim;
    headers['X-Secret-Key'] = secTrim;
  }

  let payload = null;
  if (body !== undefined && body !== null && method !== 'GET' && method !== 'HEAD') {
    headers['Content-Type'] = 'application/json';
    payload = typeof body === 'string' ? body : JSON.stringify(body);
  }

  return new Promise((resolve, reject) => {
    const opts = {
      method,
      hostname: u.hostname,
      port,
      path: u.pathname + u.search,
      headers,
      timeout,
    };

    const req = lib.request(opts, (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        let parsed = null;
        try {
          parsed = data ? JSON.parse(data) : null;
        } catch {
          parsed = { raw: data };
        }
        const result = {
          statusCode: res.statusCode,
          headers: res.headers,
          body: parsed,
          ok: res.statusCode >= 200 && res.statusCode < 300,
        };
        if (result.ok) resolve(result);
        else {
          const err = new Error(
            (parsed && parsed.error) || `HTTP ${res.statusCode}`,
          );
          err.statusCode = res.statusCode;
          err.response = parsed;
          reject(err);
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });

    if (payload) req.write(payload);
    req.end();
  });
}

module.exports = {
  getUrlConfig,
  buildClawprintUrl,
  clawprintRequest,
};
