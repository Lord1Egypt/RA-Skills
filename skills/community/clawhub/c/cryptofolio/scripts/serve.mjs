#!/usr/bin/env node

/**
 * CryptoFolio Web Server
 * 启动本地服务器，提供可视化界面
 */

import { createServer } from 'http';
import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { homedir } from 'os';
import { join, extname } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PORT = process.argv[2] || 3456;
const DATA_DIR = join(homedir(), '.openclaw', 'data');
const DATA_FILE = join(DATA_DIR, 'cryptofolio.json');
const WEB_DIR = join(__dirname, '..', 'web');

// MIME types
const MIME = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
};

// 读取数据
function loadData() {
  try {
    if (existsSync(DATA_FILE)) {
      return JSON.parse(readFileSync(DATA_FILE, 'utf8'));
    }
  } catch (e) {}
  return {
    accounts: [
      { id: 'a1', name: 'Binance', type: 'CEX', color: '#F0B90B' },
      { id: 'a2', name: 'OKX', type: 'CEX', color: '#2563EB' },
      { id: 'a3', name: 'MetaMask', type: 'WALLET', color: '#E97B2E' },
    ],
    positions: [],
    trades: [],
    finance: [],
    transfers: [],
  };
}

// 保存数据
function saveData(data) {
  if (!existsSync(DATA_DIR)) {
    mkdirSync(DATA_DIR, { recursive: true });
  }
  writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf8');
}

const server = createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // API: 获取数据
  if (url.pathname === '/api/data' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ ok: true, data: loadData() }));
    return;
  }

  // API: 保存数据
  if (url.pathname === '/api/data' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        saveData(data);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: e.message }));
      }
    });
    return;
  }

  // 静态文件
  let filePath = url.pathname === '/' ? '/index.html' : url.pathname;
  const fullPath = join(WEB_DIR, filePath);

  if (existsSync(fullPath)) {
    const ext = extname(fullPath);
    const mime = MIME[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': mime });
    res.end(readFileSync(fullPath));
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
});

server.listen(PORT, () => {
  console.log(`\n🚀 CryptoFolio 可视化界面已启动`);
  console.log(`📊 打开浏览器访问: http://localhost:${PORT}`);
  console.log(`📁 数据文件: ${DATA_FILE}`);
  console.log(`\n按 Ctrl+C 停止服务器\n`);
});
