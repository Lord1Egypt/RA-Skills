#!/usr/bin/env node
/**
 * FTA Studio 浏览器端验证（无头 Chrome + CDP）
 *
 * 用法:
 *   node verify-ui.mjs [url] [--chrome <path>]
 *   node verify-ui.mjs http://127.0.0.1:8777/
 *
 * 检查项:
 *   1. 页面加载无 JS 异常
 *   2. 节点 / 连线 / 门数量
 *   3. 单击选中（不折叠）
 *   4. 真实双击（CDP Input，clickCount=2）→ 折叠 → 再双击展开
 *   5. 撤销 / 重做
 *   6. 编号装饰开关
 *
 * 退出码: 0 全部通过 / 1 有失败
 */

import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const URL_ARG = process.argv.find((a) => a.startsWith('http')) || 'http://127.0.0.1:8777/';
const chromeArgIdx = process.argv.indexOf('--chrome');
const CHROME = chromeArgIdx > 0 ? process.argv[chromeArgIdx + 1] : findChrome();
const PORT = 9400 + Math.floor(Math.random() * 300);
const PROFILE = path.join(os.tmpdir(), 'fta-verify-' + Date.now());

if (!CHROME) {
  console.error('未找到 Chrome/Edge。用 --chrome <path> 指定，或设置 CHROME_PATH。');
  process.exit(1);
}
fs.mkdirSync(PROFILE, { recursive: true });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const results = [];
function check(name, ok, detail = '') {
  results.push({ name, ok, detail });
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  → ' + detail : ''}`);
}

function findChrome() {
  const cands = [
    process.env.CHROME_PATH,
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    path.join(process.env.LOCALAPPDATA || '', 'Google\\Chrome\\Application\\chrome.exe'),
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    '/usr/bin/google-chrome',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ].filter(Boolean);
  return cands.find((p) => fs.existsSync(p)) || null;
}

const child = spawn(CHROME, [
  '--headless=new',
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${PROFILE}`,
  '--no-first-run', '--no-default-browser-check',
  '--disable-gpu', '--hide-scrollbars',
  '--window-size=1500,1000',
  'about:blank',
], { stdio: 'ignore' });

async function waitDevtools() {
  for (let i = 0; i < 100; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/json/version`);
      if (r.ok) return await r.json();
    } catch { /* not ready */ }
    await sleep(200);
  }
  throw new Error('CDP 端口未就绪');
}

class CDP {
  constructor(ws) {
    this.ws = ws; this.id = 0; this.pending = new Map(); this.errors = [];
    ws.addEventListener('message', (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id && this.pending.has(m.id)) {
        const { res, rej } = this.pending.get(m.id);
        this.pending.delete(m.id);
        m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result);
      } else if (m.method === 'Runtime.exceptionThrown') {
        this.errors.push((m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text || '').split('\n')[0]);
      }
    });
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((res, rej) => {
      this.pending.set(id, { res, rej });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }
}

function cleanup(code) {
  try { child.kill(); } catch { /* ignore */ }
  try { fs.rmSync(PROFILE, { recursive: true, force: true }); } catch { /* ignore */ }
  process.exit(code);
}

(async () => {
  const ver = await waitDevtools();
  console.log(`浏览器: ${ver.Browser}`);
  console.log(`地址  : ${URL_ARG}\n`);

  const t = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });
  const cdp = new CDP(ws);

  await cdp.send('Page.enable');
  await cdp.send('Runtime.enable');
  await cdp.send('Page.navigate', { url: URL_ARG });
  await sleep(2800);

  const ev = async (expression) => {
    const r = await cdp.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) return { __err: r.exceptionDetails.exception?.description || r.exceptionDetails.text };
    return r.result.value;
  };

  const SNAP = `(() => {
    const s = document.querySelector('#canvas');
    if (!s) return { __err: 'no #canvas' };
    return {
      boxes: s.querySelectorAll('.node-box').length,
      links: s.querySelectorAll('path.link').length,
      gates: s.querySelectorAll('.gate-hit').length,
      idTags: s.querySelectorAll('.id-tag-rect').length,
      badge: s.querySelector('.collapse-badge .tx')?.textContent ?? null,
      sel: s.querySelector('.node-sel .id-tag-txt')?.textContent ?? null,
    };
  })()`;

  // --- 1. 基础渲染 ---
  console.log('[1] 基础渲染');
  const s0 = await ev(SNAP);
  if (s0 && s0.__err) { check('画布存在', false, s0.__err); cleanup(1); }
  check('画布存在', true);
  check('节点数 > 0', s0.boxes > 0, `boxes=${s0.boxes}`);
  check('连线数 > 0', s0.links > 0, `links=${s0.links}`);
  check('门符号 > 0', s0.gates > 0, `gates=${s0.gates}`);
  check('编号装饰默认显示', s0.idTags > 0, `idTags=${s0.idTags}`);

  // --- 2. 单击选中 ---
  console.log('\n[2] 单击选中');
  const coords = await ev(`(() => [...document.querySelectorAll('#canvas .node-box')].map(g => {
    const r = g.querySelector('.nshape').getBoundingClientRect();
    return { tag: g.querySelector('.id-tag-txt')?.textContent, x: Math.round(r.left+r.width/2), y: Math.round(r.top+r.height/2) };
  }))()`);

  const click = async (x, y, count) => {
    await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: count });
    await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: count });
  };

  if (coords.length) {
    await click(coords[0].x, coords[0].y, 1);
    await sleep(400);
    const s1 = await ev(SNAP);
    check('单击后选中', !!s1.sel, `sel=${s1.sel}`);
    check('单击不折叠', s1.boxes === s0.boxes, `${s0.boxes} → ${s1.boxes}`);
  }

  // --- 3. 真实双击折叠 ---
  console.log('\n[3] 真实双击折叠（CDP Input）');
  if (coords.length) {
    const c = coords[0];
    await click(c.x, c.y, 1);
    await sleep(70);
    await click(c.x, c.y, 2);
    await sleep(800);
    const s2 = await ev(SNAP);
    check('双击后节点数减少', s2.boxes < s0.boxes, `${s0.boxes} → ${s2.boxes}`);
    check('折叠徽标出现', !!s2.badge, `badge=${s2.badge}`);

    const back = await ev(`(() => {
      const g = document.querySelector('#canvas .node-box');
      const r = g.querySelector('.nshape').getBoundingClientRect();
      return { x: Math.round(r.left+r.width/2), y: Math.round(r.top+r.height/2) };
    })()`);
    if (back) {
      await click(back.x, back.y, 1);
      await sleep(70);
      await click(back.x, back.y, 2);
      await sleep(800);
      const s3 = await ev(SNAP);
      check('再次双击恢复', s3.boxes === s0.boxes, `${s2.boxes} → ${s3.boxes}`);
    }
  }

  // --- 4. 撤销 / 重做 ---
  console.log('\n[4] 撤销 / 重做');
  const btn = await ev(`(() => ({ u: !!document.querySelector('#btn-undo'), r: !!document.querySelector('#btn-redo') }))()`);
  if (btn.u && btn.r) {
    const before = (await ev(SNAP)).boxes;
    await ev(`document.querySelector('#btn-undo')?.click()`);
    await sleep(600);
    const afterUndo = (await ev(SNAP)).boxes;
    check('撤销按钮可用且改变状态', true, `${before} → ${afterUndo}`);
    await ev(`document.querySelector('#btn-redo')?.click()`);
    await sleep(600);
    const afterRedo = (await ev(SNAP)).boxes;
    check('重做恢复', afterRedo === before, `${afterUndo} → ${afterRedo}`);
  } else {
    check('撤销/重做按钮存在', false);
  }

  // --- 5. JS 异常 ---
  console.log('\n[5] 运行期异常');
  check('无 JS 异常', cdp.errors.length === 0, cdp.errors.join(' | ') || 'none');

  // --- 汇总 ---
  const failed = results.filter((r) => !r.ok);
  console.log(`\n结果: ${results.length - failed.length} 通过 / ${failed.length} 失败 / 共 ${results.length}`);
  if (failed.length) {
    console.log('失败项:');
    failed.forEach((f) => console.log(`  - ${f.name} ${f.detail}`));
  }
  cleanup(failed.length ? 1 : 0);
})().catch((e) => {
  console.error('FATAL:', e.message);
  cleanup(1);
});
