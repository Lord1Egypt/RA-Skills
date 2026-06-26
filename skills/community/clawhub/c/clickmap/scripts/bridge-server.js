#!/usr/bin/env node
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = Number(process.env.CLICKMAP_PORT || 18795);
const HOST = '127.0.0.1';
const TOKEN = process.env.CLICKMAP_TOKEN || '';

const baseDir = path.resolve(__dirname, '..');
const dataDir = path.join(baseDir, 'data');
const dataFile = path.join(dataDir, 'pois.json');

if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
if (!fs.existsSync(dataFile)) fs.writeFileSync(dataFile, JSON.stringify({ version: 1, pois: [] }, null, 2));

function send(res, code, payload) {
  res.writeHead(code, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
  res.end(JSON.stringify(payload));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', chunk => (raw += chunk));
    req.on('end', () => resolve(raw));
    req.on('error', reject);
  });
}

function authOk(req) {
  if (!TOKEN) return true;
  return req.headers['x-clickmap-token'] === TOKEN;
}

function loadData() {
  try {
    return JSON.parse(fs.readFileSync(dataFile, 'utf8'));
  } catch {
    return { version: 1, pois: [] };
  }
}

function saveData(data) {
  fs.writeFileSync(dataFile, JSON.stringify(data, null, 2));
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-ClickMap-Token'
    });
    return res.end();
  }

  if (!authOk(req)) return send(res, 401, { ok: false, error: 'unauthorized' });

  if (req.url === '/health' && req.method === 'GET') {
    return send(res, 200, { ok: true, service: 'clickmap-bridge', port: PORT, dataFile });
  }

  if (req.url === '/api/pois' && req.method === 'GET') {
    return send(res, 200, { ok: true, ...loadData() });
  }

  if (req.url === '/api/pois' && req.method === 'POST') {
    const raw = await readBody(req);
    let body;
    try { body = JSON.parse(raw || '{}'); } catch { return send(res, 400, { ok: false, error: 'invalid_json' }); }

    if (!Array.isArray(body.pois)) return send(res, 400, { ok: false, error: 'pois_array_required' });

    const normalized = body.pois.map((p, idx) => ({
      id: p.id || `poi-${Date.now()}-${idx}`,
      name: String(p.name || '').trim(),
      urlPattern: p.urlPattern || '',
      coords: p.coords || null,
      selectors: p.selectors || {},
      meta: p.meta || {},
      updatedAt: new Date().toISOString()
    })).filter(p => p.name);

    const data = { version: 1, updatedAt: new Date().toISOString(), pois: normalized };
    saveData(data);
    return send(res, 200, { ok: true, count: normalized.length, dataFile });
  }

  send(res, 404, { ok: false, error: 'not_found' });
});

server.listen(PORT, HOST, () => {
  console.log(`[clickmap-bridge] listening on http://${HOST}:${PORT}`);
  console.log(`[clickmap-bridge] data file: ${dataFile}`);
  if (TOKEN) console.log('[clickmap-bridge] token auth: enabled');
});
