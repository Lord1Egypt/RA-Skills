/**
 * 截图：分页后第 1 页 / 第 2 页的画布，检查跳转胶囊的视觉位置与虚线框是否协调
 */
import { spawn } from 'node:child_process';
import fs from 'node:fs';

const PORT = 8782;
const CDP_PORT = 9332;
const CHROME = [
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
].find((p) => fs.existsSync(p));

const NODE = process.argv[0];
const srv = spawn(NODE, ['src/cli.mjs', 'serve', '--port', String(PORT)], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const udd = `D:\\tmp\\cdp-shot-${Date.now()}`;
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

await evalJs(`(() => {
  const setBreak = (name) => {
    const box = [...document.querySelectorAll('#canvas .node-box')]
      .find((g) => (g.querySelector('title')?.textContent || '').includes(name));
    box.querySelector('.nshape').dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, clientX: 400, clientY: 300 }));
    document.querySelector('#ctx [data-act="pagebreak"]').click();
  };
  setBreak('制动回路失效');
  setBreak('踏板行程传递失效');
})()`);
await evalJs(`document.querySelector('#btn-pages').click()`);
await sleep(1200);

async function shot(name) {
  // 只截画布区域
  const box = await evalJs(`(() => {
    const c = document.querySelector('#canvas').getBoundingClientRect();
    return JSON.stringify({ x: c.x, y: c.y, w: c.width, h: Math.min(c.height, 760) });
  })()`);
  const b = JSON.parse(box);
  const r = await send('Page.captureScreenshot', {
    format: 'png',
    clip: { x: b.x, y: b.y, width: b.w, height: b.h, scale: 1 },
    captureBeyondViewport: true,
  });
  fs.writeFileSync(`D:\\tmp\\${name}.png`, Buffer.from(r.result.data, 'base64'));
  console.log('saved', name);
}

await shot('jump2-p1');
// 点「制动回路失效」的胶囊（第一个胶囊）→ 第 2 页
await evalJs(`document.querySelectorAll('#canvas .pb-chip.can')[0].dispatchEvent(new MouseEvent('click', { bubbles: true }))`);
await sleep(900);
await shot('jump2-p2');
// 回第 1 页 → 点「踏板行程传递失效」的胶囊 → 第 3 页
await evalJs(`document.querySelector('#pg-first').click()`);
await sleep(600);
await evalJs(`document.querySelectorAll('#canvas .pb-chip.can')[1].dispatchEvent(new MouseEvent('click', { bubbles: true }))`);
await sleep(900);
await shot('jump2-p3');
console.log('info:', await evalJs(`document.querySelector('#pg-info')?.textContent`));

ws.close();
chrome.kill();
srv.kill();
await sleep(300);
process.exit(0);
