#!/usr/bin/env node
const http = require('http');
const fs = require('fs');
const path = require('path');
const { getDataFile, readData, validateData, writeData } = require('./scripts/bucket-list-data');

const PORT = Number(process.env.BUCKET_LIST_PORT || 9999);
const HOST = '127.0.0.1';
const MAX_BODY_BYTES = 1024 * 1024;
const SKILL_DIR = __dirname;

function sendJson(res, status, data) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(`${JSON.stringify(data, null, 2)}\n`);
}

function isSameOrigin(req) {
  const origin = req.headers.origin;
  if (!origin) return true;
  return origin === `http://localhost:${PORT}` || origin === `http://127.0.0.1:${PORT}`;
}

function setCors(req, res) {
  const origin = req.headers.origin;
  if (origin && isSameOrigin(req)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
  }
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

function collectBody(req) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on('data', (chunk) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        reject(new Error('Request body too large.'));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

async function handleData(req, res) {
  if (req.method === 'GET') {
    return sendJson(res, 200, readData());
  }

  if (req.method !== 'POST') {
    return sendJson(res, 405, { error: 'Method not allowed' });
  }

  if (!isSameOrigin(req)) {
    return sendJson(res, 403, { error: 'Only same-origin localhost writes are allowed' });
  }

  try {
    const body = await collectBody(req);
    const data = validateData(JSON.parse(body));
    return sendJson(res, 200, writeData(data));
  } catch (error) {
    return sendJson(res, 400, { error: error.message });
  }
}

function handleStatic(req, res) {
  const rawPath = req.url === '/' ? '/bucket-list.html' : decodeURIComponent(req.url.split('?')[0]);
  const filePath = path.resolve(SKILL_DIR, `.${rawPath}`);

  if (!filePath.startsWith(`${SKILL_DIR}${path.sep}`) && filePath !== path.join(SKILL_DIR, 'bucket-list.html')) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Forbidden');
    return;
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('Not found');
      return;
    }

    const ext = path.extname(filePath);
    const types = {
      '.html': 'text/html; charset=utf-8',
      '.js': 'application/javascript; charset=utf-8',
      '.css': 'text/css; charset=utf-8',
      '.json': 'application/json; charset=utf-8',
    };
    res.writeHead(200, { 'Content-Type': types[ext] || 'application/octet-stream' });
    res.end(data);
  });
}

const server = http.createServer(async (req, res) => {
  setCors(req, res);
  if (req.method === 'OPTIONS') {
    res.writeHead(isSameOrigin(req) ? 204 : 403);
    res.end();
    return;
  }

  const pathname = req.url.split('?')[0];
  if (pathname === '/data/bucket-list.json' || pathname === '/data/bucket-list.json/') {
    await handleData(req, res);
    return;
  }

  handleStatic(req, res);
});

server.listen(PORT, HOST, () => {
  console.log('Bucket List Server running');
  console.log(`  GUI: http://localhost:${PORT}/`);
  console.log(`  Data: ${getDataFile()}`);
  console.log('  Access: 127.0.0.1 only');
});
