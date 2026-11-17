#!/usr/bin/env node
// 导出夸克网盘 cookie（Netscape 格式）— 已验证 2026-08-30
// 依赖：本机 Chrome 带 --remote-debugging-port=18800 且已登录 pan.quark.cn
// 用法：node get_quark_cookies.js [输出路径，默认 ./quark_cookies.txt]
// 说明：WS 模块路径自动探测（chrome-remote-interface 依赖的 ws）
const http = require('http');
const fs = require('fs');
const path = require('path');

const outPath = process.argv[2] || 'quark_cookies.txt';

function findWsModule() {
  const candidates = [
    process.env.WS_PATH,
    path.join(process.env.HOME || '', '.npm-global/lib/node_modules/@steipete/oracle/node_modules/chrome-remote-interface/node_modules/ws'),
    path.join(process.env.HOME || '', '.npm-global/lib/node_modules/chrome-remote-interface/node_modules/ws'),
    require.resolve('ws'),
  ].filter(Boolean);
  for (const c of candidates) {
    try { require(c); return c; } catch (e) {}
  }
  console.error('找不到 ws 模块，设置 WS_PATH 环境变量指向 ws 模块目录');
  process.exit(1);
}
const WebSocket = require(findWsModule());

http.get('http://127.0.0.1:18800/json/list', (res) => {
  let d = '';
  res.on('data', c => d += c);
  res.on('end', () => {
    const targets = JSON.parse(d);
    const page = targets.find(t => t.type === 'page' && t.url.includes('quark'));
    const t = page || targets.find(t => t.type === 'page');
    if (!t) { console.error('NO_PAGE'); process.exit(1); }
    const ws = new WebSocket(t.webSocketDebuggerUrl);
    ws.on('open', () => ws.send(JSON.stringify({id: 1, method: 'Network.getAllCookies'})));
    ws.on('message', (msg) => {
      const m = JSON.parse(msg);
      if (m.id === 1) {
        const cookies = m.result.cookies.filter(c => c.domain.includes('quark.cn'));
        const lines = cookies.map(c =>
          `${c.domain}\tTRUE\t${c.path}\t${c.secure ? 'TRUE' : 'FALSE'}\t${c.expirationDate ? Math.floor(c.expirationDate) : 0}\t${c.name}\t${c.value}`);
        const header = '# Netscape HTTP Cookie File\n' + lines.join('\n') + '\n';
        fs.writeFileSync(outPath, header);
        console.log(`OK ${cookies.length} cookies → ${outPath}`);
        process.exit(0);
      }
    });
    setTimeout(() => { console.error('TIMEOUT'); process.exit(1); }, 8000);
  });
});
