/**
 * 无头 Chrome + CDP 验证「跳转」按钮真的可用：
 *   1) 右键「制动回路失效」→ 设为分页点
 *   2) 点工具栏「分页」
 *   3) 画布上应出现可点击的绿色胶囊（.pb-chip.can），文字含「第 2 页」
 *   4) 点它 → 页眉从「第 1 页」变成「第 2 页」
 *   5) 第 2 页页顶出现「↑ 续上页 · 第 1 页」胶囊，点它 → 回到第 1 页
 *   6) 分页导航条出现 #pg-jump 按钮
 */
import { spawn } from 'node:child_process';
import fs from 'node:fs';

const PORT = 8781;
const CDP_PORT = 9331;
const CHROME = [
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
].find((p) => fs.existsSync(p));
if (!CHROME) { console.log('✗ 未找到 Chrome/Edge'); process.exit(1); }

const NODE = process.argv[0];
const srv = spawn(NODE, ['src/cli.mjs', 'serve', '--port', String(PORT)], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const udd = `D:\\tmp\\cdp-jump-${Date.now()}`;
const chrome = spawn(CHROME, [
  '--headless=new', `--remote-debugging-port=${CDP_PORT}`, `--user-data-dir=${udd}`,
  '--no-first-run', '--no-default-browser-check', '--disable-gpu', '--window-size=1600,1000',
  'about:blank',
], { stdio: 'ignore' });

async function wsUrl() {
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${CDP_PORT}/json/list`);
      const list = await r.json();
      const pg = list.find((t) => t.type === 'page');
      if (pg) return pg.webSocketDebuggerUrl;
    } catch { /* 还没起来 */ }
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
const evalJs = async (expr) => {
  const r = await send('Runtime.evaluate', {
    expression: expr, awaitPromise: true, returnByValue: true,
  });
  if (r.result?.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails));
  return r.result?.result?.value;
};

await send('Page.enable');
await send('Runtime.enable');
await send('Page.navigate', { url: `http://127.0.0.1:${PORT}/` });
await sleep(2500);

const out = [];
const check = (name, ok, extra = '') => {
  out.push(`${ok ? '✓' : '✗'} ${name}${extra ? '  ' + extra : ''}`);
  if (!ok) process.exitCode = 1;
};

// 1) 右键目标事件 → 设为分页点
const setBreak = await evalJs(`(() => {
  const box = [...document.querySelectorAll('#canvas .node-box')]
    .find((g) => (g.querySelector('title')?.textContent || '').includes('制动回路失效'));
  if (!box) return 'NOT_FOUND';
  const shape = box.querySelector('.nshape');
  shape.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, clientX: 400, clientY: 300 }));
  const item = document.querySelector('#ctx [data-act="pagebreak"]');
  if (!item) return 'NO_MENU';
  item.click();
  return 'OK';
})()`);
check('右键设分页点', setBreak === 'OK', setBreak);

// 2) 点「分页」
await evalJs(`document.querySelector('#btn-pages').click()`);
await sleep(1200);

// 3) 第 1 页：应有一个可点胶囊，指向第 2 页
const p1 = await evalJs(`(() => {
  const chips = [...document.querySelectorAll('#canvas .pb-chip.can')].map((g) => g.textContent.trim());
  return JSON.stringify({
    chips,
    head: document.querySelector('#canvas text')?.textContent || '',
    info: document.querySelector('#pg-info')?.textContent || '',
    jumpBtn: (() => { const b = document.querySelector('#pg-jump'); return b && !b.hidden ? b.textContent.trim() : ''; })(),
  });
})()`);
const s1 = JSON.parse(p1);
check('画布出现可点击胶囊', s1.chips.length > 0, JSON.stringify(s1.chips));
check('胶囊标注目标页', s1.chips.some((c) => c.includes('第 2 页')), s1.chips.join(' / '));
check('页眉在第 1 页', s1.info.includes('第 1 /'), s1.info);
check('导航条有跳转按钮', !!s1.jumpBtn, s1.jumpBtn);

// 4) 点胶囊 → 应跳到第 2 页
await evalJs(`document.querySelector('#canvas .pb-chip.can').dispatchEvent(new MouseEvent('click', { bubbles: true }))`);
await sleep(900);
const p2 = await evalJs(`(() => {
  const chips = [...document.querySelectorAll('#canvas .pb-chip.can')].map((g) => g.textContent.trim());
  return JSON.stringify({
    chips,
    info: document.querySelector('#pg-info')?.textContent || '',
    jumpBtn: (() => { const b = document.querySelector('#pg-jump'); return b && !b.hidden ? b.textContent.trim() : ''; })(),
    dashed: document.querySelectorAll('#canvas [stroke-dasharray="5 4"]').length,
  });
})()`);
const s2 = JSON.parse(p2);
check('点击后到达第 2 页', s2.info.includes('第 2 /'), s2.info);
check('第 2 页有承接胶囊', s2.chips.some((c) => c.includes('续上页') && c.includes('第 1 页')), s2.chips.join(' / '));
check('第 2 页有虚线框', s2.dashed > 0, String(s2.dashed));
check('第 2 页导航按钮指向第 1 页', s2.jumpBtn.includes('第 1 页'), s2.jumpBtn);

// 5) 点承接胶囊 → 回到第 1 页
await evalJs(`document.querySelector('#canvas .pb-chip.can').dispatchEvent(new MouseEvent('click', { bubbles: true }))`);
await sleep(900);
const back = await evalJs(`document.querySelector('#pg-info')?.textContent || ''`);
check('承接胶囊可跳回第 1 页', back.includes('第 1 /'), back);

console.log(out.join('\n'));
if (!process.exitCode) console.log('✓ 跳转功能全部通过');

ws.close();
chrome.kill();
srv.kill();
await sleep(300);
process.exit(process.exitCode || 0);
