/**
 * 截图验证：底事件左缘 medini 风格红色圆点
 *  - 画布：4 个底事件应各有一个 circle.basic-dot
 *  - A4 导出：SVG 里应有红点 circle
 */
import { spawn } from 'node:child_process';
import fs from 'node:fs';

const PORT = 8783;
const CDP_PORT = 9334;
const CHROME = [
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
].find((p) => fs.existsSync(p));

const NODE = process.argv[0];
const srv = spawn(NODE, ['src/cli.mjs', 'serve', '--port', String(PORT)], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const udd = `D:\\tmp\\cdp-dot-${Date.now()}`;
const chrome = spawn(CHROME, [
  '--headless=new', `--remote-debugging-port=${CDP_PORT}`, `--user-data-dir=${udd}`,
  '--no-first-run', '--no-default-browser-check', '--disable-gpu', '--window-size=1500,1000',
  'about:blank',
], { stdio: 'ignore' });

async function wsUrl() {
  for (let i = 0; i < 60; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${CDP_PORT}/json/list`)).json();
      const pg = list.find((t) => t.type === 'page');
      if (pg) return pg.webSocketDebuggerUrl;
    } catch { /* 等 */ }
    await sleep(250);
  }
  throw new Error('CDP 未就绪');
}

const ws = new WebSocket(await wsUrl());
await new Promise((r) => ws.addEventListener('open', r, { once: true }));
let seq = 0;
const pending = new Map();
ws.addEventListener('message', (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
});
const send = (method, params = {}) => new Promise((res) => {
  const id = ++seq;
  pending.set(id, res);
  ws.send(JSON.stringify({ id, method, params }));
});
const evalJs = async (expr) => (await send('Runtime.evaluate', {
  expression: expr, awaitPromise: true, returnByValue: true,
})).result?.result?.value;

await send('Page.enable');
await send('Runtime.enable');
await send('Page.navigate', { url: `http://127.0.0.1:${PORT}/` });
await sleep(2500);

// 画布红点计数 + 截图
const cnt = await evalJs(`document.querySelectorAll('#canvas .basic-dot').length`);
console.log('画布红点数:', cnt, '(期望 4)');

const box = JSON.parse(await evalJs(`(() => {
  const c = document.querySelector('#canvas').getBoundingClientRect();
  return JSON.stringify({ x: c.x, y: c.y, w: c.width, h: Math.min(c.height, 700) });
})()`));
const r = await send('Page.captureScreenshot', {
  format: 'png',
  clip: { x: box.x, y: box.y, width: box.w, height: box.h, scale: 1.4 },
  captureBeyondViewport: true,
});
fs.writeFileSync('D:\\tmp\\basic-dot.png', Buffer.from(r.result.data, 'base64'));
console.log('saved D:\\tmp\\basic-dot.png');

// A4 导出里的红点
const html = await evalJs(`(async () => {
  const res = await fetch('/api/svg-a4', { method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tree: (await (await fetch('/api/example/brake')).json()).tree, options: { budget: 14, heatmap: true } }) });
  return res.text();
})()`);
const dots = (html.match(/fill="#e01b24"/g) || []).length;
console.log('A4 导出红点数:', dots, '(期望 4)');

ws.close();
chrome.kill();
srv.kill();
await sleep(300);
process.exit(0);
