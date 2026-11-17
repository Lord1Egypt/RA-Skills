#!/usr/bin/env node
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');
const { processLogsWithOptions } = require('../process_logs.js');

function parseArgs(argv) {
  const args = { port: 8787, host: '127.0.0.1' };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--port' && argv[i + 1]) args.port = Number(argv[++i]);
    else if (a === '--host' && argv[i + 1]) args.host = argv[++i];
    else if (a === '-h' || a === '--help') args.help = true;
  }
  return args;
}

function contentType(p) {
  if (p.endsWith('.html')) return 'text/html; charset=utf-8';
  if (p.endsWith('.css')) return 'text/css; charset=utf-8';
  if (p.endsWith('.js')) return 'text/javascript; charset=utf-8';
  if (p.endsWith('.json')) return 'application/json; charset=utf-8';
  if (p.endsWith('.svg')) return 'image/svg+xml';
  if (p.endsWith('.png')) return 'image/png';
  if (p.endsWith('.jpg') || p.endsWith('.jpeg')) return 'image/jpeg';
  return 'application/octet-stream';
}

const args = parseArgs(process.argv);
if (args.help) {
  console.log('Usage: node scripts/serve.js [--host 127.0.0.1] [--port 8787]');
  console.log('');
  console.log('  The dashboard binds to loopback only (127.0.0.1/::1/localhost).');
  console.log('  For remote access, use a reverse proxy with authentication.');
  process.exit(0);
}

const root = path.resolve(__dirname, '..');
const { resolveBridgeCredential } = require('../../runtime/bridge-credential.cjs');

function isAllowedOrigin(origin) {
  if (typeof origin !== 'string') return false;
  return [`http://127.0.0.1:${args.port}`, `http://localhost:${args.port}`, `http://[::1]:${args.port}`].includes(origin);
}

function readJsonBody(req, limitBytes = 8192) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', chunk => {
      raw += chunk;
      if (Buffer.byteLength(raw) > limitBytes) {
        reject(new Error('Request body too large'));
        req.destroy();
      }
    });
    req.on('end', () => {
      try {
        resolve(raw ? JSON.parse(raw) : {});
      } catch (_) {
        reject(new Error('Invalid JSON'));
      }
    });
    req.on('error', reject);
  });
}

function isLoopbackBridgeUrl(value) {
  try {
    const u = new URL(value);
    return (
      (u.protocol === 'http:' || u.protocol === 'https:') &&
      ['127.0.0.1', 'localhost', '::1', '[::1]'].includes(u.hostname)
    );
  } catch (_) {
    return false;
  }
}

function sendJson(res, status, payload) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(payload));
}

const ALLOWED_REALTIME_MODELS = new Set(['gpt-realtime', 'gpt-realtime-mini']);

const server = http.createServer((req, res) => {
  const origin = req.headers.origin;
  const allowedHosts = new Set([`127.0.0.1:${args.port}`, `localhost:${args.port}`, `[::1]:${args.port}`]);
  if (!allowedHosts.has(req.headers.host)) return sendJson(res, 403, { error: 'Invalid dashboard Host' });
  const ownOrigin = `http://${req.headers.host}`;
  if (origin && origin !== ownOrigin) return sendJson(res, 403, { error: 'Cross-origin request denied' });
  if (req.headers['sec-fetch-site'] && req.headers['sec-fetch-site'] !== 'same-origin' && req.headers['sec-fetch-site'] !== 'none') {
    return sendJson(res, 403, { error: 'Cross-site request denied' });
  }
  if (req.method === 'POST' && (origin !== ownOrigin || !/^application\/json(?:;|$)/i.test(req.headers['content-type'] || ''))) {
    return sendJson(res, 403, { error: 'Same-origin JSON POST required' });
  }

  if (isAllowedOrigin(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  }

  if (req.method === 'OPTIONS') {
    res.writeHead(isAllowedOrigin(origin) ? 204 : 403);
    res.end();
    return;
  }

  // POST /api/call — loopback-only proxy to Amber bridge /call/outbound.
  // Keeping this same-origin avoids browser CORS issues while still refusing
  // non-local bridge targets so the dashboard cannot become a generic proxy.
  if (req.method === 'POST' && ['/api/call', '/api/call/preview'].includes(req.url)) {
    readJsonBody(req)
      .then(async body => {
        const bridgeUrl = String(body.bridgeUrl || 'http://127.0.0.1:8000').replace(/\/+$/, '');
        // Auto-share the installation secret only with its configured bridge, never an arbitrary local URL.
        const configuredBridgeUrl = String(process.env.AMBER_BRIDGE_URL || 'http://127.0.0.1:8000').replace(/\/+$/, '');
        const bridgeToken = String(body.bridgeToken || (bridgeUrl === configuredBridgeUrl ? resolveBridgeCredential(path.join(root, '..', 'runtime')) : ''));
        const to = String(body.to || '').trim();
        const objective = String(body.objective || '').trim();
        const model = String(body.model || 'gpt-realtime').trim();

        if (!isLoopbackBridgeUrl(bridgeUrl)) {
          sendJson(res, 400, { success: false, error: 'Bridge URL must be localhost/loopback.' });
          return;
        }
        if (!ALLOWED_REALTIME_MODELS.has(model)) {
          sendJson(res, 400, { success: false, error: 'Invalid model. Choose gpt-realtime or gpt-realtime-mini.' });
          return;
        }
        if (!/^\+[1-9]\d{6,14}$/.test(to)) {
          sendJson(res, 400, { success: false, error: 'Invalid phone number. Use E.164, like +14165551234.' });
          return;
        }
        if (!objective) {
          sendJson(res, 400, { success: false, error: 'Objective is required.' });
          return;
        }

        const headers = { 'Content-Type': 'application/json' };
        if (bridgeToken) headers.Authorization = `Bearer ${bridgeToken}`;

        const upstream = await fetch(`${bridgeUrl}${req.url === '/api/call/preview' ? '/call/preview' : '/call/outbound'}`, {
          method: 'POST',
          headers,
          body: JSON.stringify({ to, objective, model, confirmed: body.confirmed === true, approvalToken: body.approvalToken })
        });
        const text = await upstream.text();
        let payload;
        try {
          payload = text ? JSON.parse(text) : {};
        } catch (_) {
          payload = { raw: text };
        }
        sendJson(res, upstream.ok ? 200 : upstream.status, {
          success: upstream.ok,
          ...payload
        });
      })
      .catch(err => sendJson(res, 500, { success: false, error: err.message }));
    return;
  }

  // POST /api/sync — manually trigger process_logs.js
  // Security: target script path is hardcoded (not user-controlled); no user input is
  // passed to the spawned process. Environment is scoped to only what Node needs.
  if (req.method === 'POST' && req.url === '/api/sync') {
    // Hardcoded path — not derived from request input
    const processLogsPath = path.resolve(root, 'process_logs.js');
    // Verify target stays within the dashboard root (defense in depth)
    if (!processLogsPath.startsWith(root + path.sep) && processLogsPath !== path.resolve(root, 'process_logs.js')) {
      res.writeHead(403, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: false, error: 'Forbidden' }));
      return;
    }
    const startTime = Date.now();
    processLogsWithOptions({ logsDir: process.env.LOGS_DIR, outputDir: path.join(root, 'data'), writeSample: true })
      .then(calls => {
        const durationMs = Date.now() - startTime;
        console.log(`[sync] processed ${calls.length} calls in ${durationMs}ms`);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, calls: calls.length, durationMs, error: null }));
      })
      .catch(err => {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: err.message }));
      });
    return;
  }

  const u = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  let pathname = decodeURIComponent(u.pathname);
  if (pathname === '/') pathname = '/index.html';

  const fsPath = path.resolve(root, '.' + pathname);
  if (!fsPath.startsWith(root + path.sep) && fsPath !== root) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Forbidden');
    return;
  }

  fs.readFile(fsPath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' });
      res.end('Not found');
      return;
    }
    res.writeHead(200, {
      'Content-Type': contentType(fsPath),
      'Cache-Control': 'no-store'
    });
    res.end(data);
  });
});

// Hard-reject non-loopback binding — no override flag exists.
// Call logs and transcripts contain PII; exposing them without authentication is not permitted.
// For remote access, place a reverse proxy with authentication in front of this server.
const LOOPBACK_ADDRESSES = new Set(['127.0.0.1', '::1', 'localhost']);
if (!LOOPBACK_ADDRESSES.has(args.host)) {
  console.error('');
  console.error('ERROR: Dashboard only binds to loopback (127.0.0.1 / ::1 / localhost).');
  console.error('   Requested: ' + args.host);
  console.error('   Call logs and transcripts contain PII and must not be exposed to the network without authentication.');
  console.error('   For remote access, use a reverse proxy (e.g. nginx, caddy) with authentication.');
  console.error('');
  process.exit(1);
}

server.listen(args.port, args.host, () => {
  console.log(`Serving ${root}`);
  console.log(`Open: http://${args.host}:${args.port}/`);
});
