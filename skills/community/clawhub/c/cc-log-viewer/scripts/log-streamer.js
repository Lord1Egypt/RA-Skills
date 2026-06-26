#!/usr/bin/env node

/**
 * log-streamer.js — CC 实时输出监控器 (v3)
 * 
 * 实现：
 *   - 基于 node-pty 为 CC 提供真实终端环境
 *   - 输出实时 pipe → 环形缓冲 → WebSocket 推送
 *   - stdin 转发：HTTP API / WebSocket → CC
 *   - 不再依赖 tmux, script, expect
 * 
 * 启动：node log-streamer.js [--port=18798] [--no-cc]
 *   --no-cc  不启动 CC 进程，仅提供 Web 服务和 WebSocket
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const { spawn } = require('node-pty');
const { WebSocketServer } = require('ws');

// ── 配置 ──

const PORT = parseInt(process.argv.find(a => a.startsWith('--port='))?.split('=')[1] || 18798);
const NO_CC = process.argv.includes('--no-cc');

// ── CC 进程管理 ──

let ccProcess = null;
const outputBuffer = [];
const MAX_BUFFER_LINES = 1000;
let pendingOutput = '';
let lastFlushTime = Date.now();

function startCC() {
  if (ccProcess) {
    console.log('CC already running, stopping first...');
    stopCC();
  }

  console.log('Starting CC via node-pty...');

  ccProcess = spawn('claude', ['--dangerously-skip-permissions'], {
    name: 'xterm-256color',
    cols: 100,
    rows: 30,
    env: { ...process.env, TERM: 'xterm-256color' }
  });

  console.log(`CC spawned (pid concept)`);

  ccProcess.onData((data) => {
    pendingOutput += data;
    
    // 环形缓冲
    const lines = data.split('\n');
    for (const line of lines) {
      outputBuffer.push(line);
    }
    while (outputBuffer.length > MAX_BUFFER_LINES) {
      outputBuffer.shift();
    }
  });

  ccProcess.onExit(({ exitCode, signal }) => {
    console.log(`CC exited (code=${exitCode}, signal=${signal})`);
    ccProcess = null;
    const msg = JSON.stringify({ type: 'info', data: `\r\n\x1b[31m⚠ CC 进程退出 (code=${exitCode})\x1b[0m\r\n` });
    broadcast(msg);
  });

  // CC 启动后给一个初始回车
  setTimeout(() => {
    if (ccProcess) {
      ccProcess.write('\r');
    }
  }, 3000);
}

function stopCC() {
  if (!ccProcess) return;
  console.log('Stopping CC...');
  try {
    ccProcess.write('\x03'); // Ctrl-C
    setTimeout(() => {
      ccProcess.kill('SIGTERM');
    }, 2000);
    setTimeout(() => {
      if (ccProcess) {
        ccProcess.kill('SIGKILL');
        ccProcess = null;
      }
    }, 4000);
  } catch {}
}

function sendToCC(text) {
  if (!ccProcess) {
    console.log('CC not running, cannot send');
    return false;
  }
  try {
    ccProcess.write(text + '\r');
    console.log('Sent to CC:', text.slice(0, 60));
  } catch(e) {
    console.log('send error:', e.message);
    return false;
  }
  return true;
}

function getHistory() {
  return outputBuffer.join('\n');
}

function flushOutput() {
  const data = pendingOutput;
  pendingOutput = '';
  return data;
}

// ── WebSocket ──

const wssClients = new Set();

function broadcast(msg) {
  const text = typeof msg === 'string' ? msg : JSON.stringify(msg);
  for (const ws of wssClients) {
    try { ws.send(text); } catch {}
  }
}

// ── HTTP + WebSocket 服务 ──

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');

  // 主页
  if (req.url === '/' || req.url.startsWith('/?embed=')) {
    const htmlPath = path.join(__dirname, 'index.html');
    if (fs.existsSync(htmlPath)) {
      let html = fs.readFileSync(htmlPath, 'utf-8');
      const embed = req.url.includes('embed=1') ? 'true' : 'false';
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(html.replace('__EMBED__', embed));
    } else {
      res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('Log Viewer Server Running\n');
    }
    return;
  }

  // API: 向 CC 发命令
  if (req.url === '/api/send' && req.method === 'POST') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const { command } = JSON.parse(body);
        if (!command) { res.writeHead(400); res.end('{}'); return; }
        const ok = sendToCC(command);
        res.writeHead(ok ? 200 : 503, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ sent: ok }));
      } catch (e) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  // API: 状态
  if (req.url === '/api/status') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      running: ccProcess !== null,
      clients: wssClients.size,
      bufferLines: outputBuffer.length
    }));
    return;
  }

  // API: 重启 CC
  if (req.url === '/api/restart' && req.method === 'POST') {
    stopCC();
    setTimeout(() => startCC(), 1500);
    res.writeHead(200);
    res.end(JSON.stringify({ restarting: true }));
    return;
  }

  // 静态文件
  const filePath = path.join(__dirname, req.url);
  if (req.url !== '/' && fs.existsSync(filePath) && !fs.statSync(filePath).isDirectory()) {
    const ext = path.extname(filePath);
    const mime = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.png': 'image/png', '.svg': 'image/svg+xml' };
    res.writeHead(200, { 'Content-Type': mime[ext] || 'text/plain' });
    res.end(fs.readFileSync(filePath));
    return;
  }

  // xterm 本地资源
  if (req.url.startsWith('/cdn/')) {
    const cdnPath = req.url.slice(5);
    const localMap = {
      'npm/xterm@5.3.0/lib/xterm.min.js': path.join(__dirname, 'node_modules/xterm/lib/xterm.js'),
      'npm/xterm@5.3.0/css/xterm.min.css': path.join(__dirname, 'node_modules/xterm/css/xterm.css'),
      'npm/xterm-addon-fit@0.8.0/lib/xterm-addon-fit.min.js': path.join(__dirname, 'node_modules/xterm-addon-fit/lib/xterm-addon-fit.js'),
    };
    const localFile = localMap[cdnPath];
    if (localFile && fs.existsSync(localFile)) {
      const mimeMap = { '.js': 'application/javascript', '.css': 'text/css' };
      res.writeHead(200, { 'Content-Type': mimeMap[path.extname(localFile)] || 'text/plain' });
      res.end(fs.readFileSync(localFile));
    } else {
      res.writeHead(404);
      res.end('Not found');
    }
    return;
  }

  res.writeHead(404);
  res.end('Not found');
});

const wss = new WebSocketServer({ server });

wss.on('connection', (ws) => {
  console.log(`WS client connected (${wssClients.size + 1} total)`);
  wssClients.add(ws);

  // 发送历史
  const history = getHistory();
  if (history) {
    ws.send(JSON.stringify({ type: 'history', data: history }));
  }

  // CC 状态提示
  ws.send(JSON.stringify({
    type: 'info',
    data: ccProcess
      ? `\r\n\x1b[32m● CC 运行中 (node-pty)\x1b[0m\r\n`
      : `\r\n\x1b[31m● CC 未启动\x1b[0m\r\n`
  }));

  ws.on('message', (data) => {
    const text = data.toString();
    if (text === 'ping') {
      ws.send(JSON.stringify({ type: 'pong' }));
    } else if (text === 'sync') {
      const history = getHistory();
      if (history) ws.send(JSON.stringify({ type: 'data', data: history }));
    } else if (text.startsWith('cmd:')) {
      const cmd = text.slice(4);
      const ok = sendToCC(cmd);
      ws.send(JSON.stringify({ type: 'cmd-status', ok }));
    }
  });

  ws.on('close', () => {
    wssClients.delete(ws);
    console.log(`WS client disconnected (${wssClients.size} total)`);
  });

  ws.on('error', () => wssClients.delete(ws));
});

// ── 输出轮询推送 ──

setInterval(() => {
  const data = flushOutput();
  if (data) broadcast(JSON.stringify({ type: 'data', data }));
}, 100);

// ── 启动 ──

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Log-Streamer v3 running on http://0.0.0.0:${PORT}`);
  if (NO_CC) {
    console.log('--no-cc mode: CC not started. Use POST /api/restart to start later.');
  } else {
    console.log('Starting CC via node-pty...');
    startCC();
  }
});

// 优雅退出
process.on('SIGINT', () => { stopCC(); server.close(); process.exit(0); });
process.on('SIGTERM', () => { stopCC(); server.close(); process.exit(0); });
