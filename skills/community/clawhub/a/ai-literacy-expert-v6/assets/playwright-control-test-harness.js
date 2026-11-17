#!/usr/bin/env node
/**
 * playwright-control-test-harness.js
 * ─────────────────────────────────────────────────────────────────────────
 * V6.0 工作流引擎 · VERIFY 阶段自动实测资产
 *
 * 作用：对 p5.js 课件 / 游戏 / 备课 HTML 的「全部互动控件」自动枚举、触发、
 *       捕获 JS 报错，并输出 JSON 报告 + 「强制测试门控结果块」(Markdown)。
 * 把商用标准 §11 的「人工控件实测」变成可复跑、可 CI 的自动化闭环。
 *
 * 用法：
 *   node assets/playwright-control-test-harness.js <file.html|url> [--out DIR] [--name NAME]
 *        [--json FILE] [--md FILE] [--timeout MS] [--no-headless] [--chromium PATH]
 *
 * 退出码：0 = 全部通过 / 修复后通过；2 = 存在未通过控件（禁止提交）。
 *
 * 复用：本文件与技能一同分发，AI 在 VERIFY 阶段调用它即可得到客观门控结果。
 * ─────────────────────────────────────────────────────────────────────────
 */
'use strict';

const fs = require('fs');
const path = require('path');
const cp = require('child_process');

/* ---------- 1. 解析 playwright（优先全局，兼容本地） ---------- */
function loadPlaywright() {
  const candidates = [];
  try { candidates.push(cp.execSync('npm root -g').toString().trim() + '/playwright'); } catch (_) {}
  try { candidates.push(cp.execSync('pnpm root -g').toString().trim() + '/playwright'); } catch (_) {}
  for (const base of candidates) {
    try { return require(base); } catch (_) {}
  }
  try { return require('playwright'); } catch (_) {}
  throw new Error('找不到 playwright，请先 `npm i -g playwright` 并执行 `playwright install chromium`');
}

/* ---------- 2. 参数解析 ---------- */
const args = process.argv.slice(2);
if (args.length === 0) { console.error('用法: node harness.js <file.html|url> [--out DIR]'); process.exit(1); }
let target = args[0];
let outDir = null, name = null, jsonPath = null, mdPath = null;
let timeout = 4000, headless = true, chromiumPath = process.env.CHROMIUM_PATH || '';
for (let i = 1; i < args.length; i++) {
  if (args[i] === '--out') outDir = args[++i];
  else if (args[i] === '--name') name = args[++i];
  else if (args[i] === '--json') jsonPath = args[++i];
  else if (args[i] === '--md') mdPath = args[++i];
  else if (args[i] === '--timeout') timeout = parseInt(args[++i], 10) || 4000;
  else if (args[i] === '--no-headless') headless = false;
  else if (args[i] === '--chromium') chromiumPath = args[++i];
}

const isUrl = /^https?:\/\//i.test(target);
const targetUrl = isUrl ? target : ('file://' + path.resolve(target));
const displayName = name || (isUrl ? target : path.basename(target));

/* ---------- 3. 良性噪声（p5 2.x 无头环境已知，不计入失败） ---------- */
const BENIGN = /webgl not supported|swiftshader|GL_INVALID|groupmarkerasdestroyed|failed to load resource.*favicon|net::ERR.*favicon/i;

(async () => {
  const pw = loadPlaywright();
  const launchOpts = {
    headless,
    args: ['--no-sandbox', '--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--disable-dev-shm-usage']
  };
  if (chromiumPath) launchOpts.executablePath = chromiumPath;

  const browser = await pw.chromium.launch(launchOpts);
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

  const consoleErrors = [], benignErrors = [], pageErrors = [];
  const snap = () => ({ c: consoleErrors.length, p: pageErrors.length });
  page.on('console', m => {
    if (m.type() === 'error') {
      if (BENIGN.test(m.text())) benignErrors.push(m.text());
      else consoleErrors.push(m.text());
    }
  });
  page.on('pageerror', e => pageErrors.push(e.message));

  await page.goto(targetUrl, { waitUntil: 'networkidle', timeout: 20000 }).catch(() => {});
  await page.waitForTimeout(1200); // 等 p5 setup() 完成

  /* ---------- 4. 枚举控件（DOM 层） ---------- */
  const controls = await page.evaluate(() => {
    const out = [];
    const labelOf = el => {
      const t = (el.getAttribute('aria-label') || el.getAttribute('title') || el.textContent || '').trim().slice(0, 24);
      return t || el.id || el.name || el.type || el.tagName.toLowerCase();
    };
    const pick = (sel, type) => document.querySelectorAll(sel).forEach((el) => {
      const idx = out.length;                 // 全局唯一索引，跨容器稳健定位
      el.setAttribute('data-ctrl', String(idx));
      const id = `${type}#${idx + 1}`;
      out.push({ id, type, label: labelOf(el),
        selector: `[data-ctrl="${idx}"]`,
        tag: el.tagName.toLowerCase() });
    });
    pick('button', 'button');
    pick('input[type="button"],input[type="submit"],input[type="reset"]', 'button');
    pick('[role="button"]', 'button');
    pick('input[type="text"],input[type="number"],input[type="email"],input[type="search"],input:not([type])', 'input');
    pick('textarea', 'textarea');
    pick('input[type="range"]', 'range');
    pick('select', 'select');
    pick('input[type="checkbox"]', 'checkbox');
    pick('input[type="radio"]', 'radio');
    return out;
  });

  /* ---------- 5. 逐控件触发 + 捕获报错 ---------- */
  const results = [];
  for (const c of controls) {
    const before = snap();
    let result = '通过', error = '', repairHint = '';
    try {
      const exists = await page.$(c.selector);
      if (!exists) { result = '未通过'; error = '控件不存在/不可定位'; repairHint = '检查选择器或 DOM 生成时机'; }
      else {
        if (c.type === 'button') {
          await page.$eval(c.selector, el => el.scrollIntoView({ block: 'center' }));
          await page.click(c.selector, { timeout, trial: false }).catch(async () => {
            await page.$eval(c.selector, el => el.click()); // 兜底：直接派发 click
          });
        } else if (c.type === 'input' || c.type === 'textarea') {
          await page.$eval(c.selector, (el) => {
            el.value = el.tagName === 'TEXTAREA' ? '测试输入' : '123';
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
          });
        } else if (c.type === 'range') {
          await page.$eval(c.selector, (el) => {
            const mid = (Number(el.min || 0) + Number(el.max || 100)) / 2;
            el.value = String(mid);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
          });
        } else if (c.type === 'select') {
          await page.$eval(c.selector, (el) => {
            const opt = [...el.options].find(o => !o.disabled);
            if (opt) { el.value = opt.value; el.dispatchEvent(new Event('change', { bubbles: true })); }
          });
        } else if (c.type === 'checkbox' || c.type === 'radio') {
          await page.$eval(c.selector, el => { el.checked = !el.checked; el.dispatchEvent(new Event('change', { bubbles: true })); });
        }
      }
    } catch (e) {
      result = '未通过'; error = String(e.message || e).slice(0, 200);
      repairHint = '捕获到异常，检查事件绑定/状态变量';
    }
    // 等待可能异步触发的报错
    await page.waitForTimeout(250);
    const after = snap();
    if (after.c > before.c || after.p > before.p) {
      const newErr = consoleErrors.slice(before.c).concat(pageErrors.slice(before.p));
      if (newErr.length) { result = '未通过'; error = (error ? error + ' | ' : '') + newErr[0].slice(0, 160); repairHint = '触发后产生 JS 报错，定位回调逻辑'; }
    }
    // 触发后控件是否仍存在（未白屏/未崩溃移除）
    const stillThere = await page.$(c.selector).catch(() => null);
    if (!stillThere && result === '通过') { result = '未通过'; error = '触发后控件丢失（疑似白屏/崩溃）'; }
    results.push({ ...c, action: 'auto-trigger', result, error, repairHint });
  }

  /* ---------- 6. Canvas 烟雾测试（覆盖 p5 画布内交互） ---------- */
  const hasCanvas = await page.$('canvas');
  if (hasCanvas) {
    const before = snap();
    let result = '通过', error = '';
    try {
      const box = await page.$eval('canvas', el => { const r = el.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; });
      const pts = [[0.5, 0.5], [0.1, 0.1], [0.9, 0.9], [0.1, 0.9], [0.9, 0.1]];
      for (const [fx, fy] of pts) {
        await page.mouse.click(box.x + box.w * fx, box.y + box.h * fy);
        await page.waitForTimeout(120);
      }
      for (const k of ['Space', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'a', 'b']) {
        await page.keyboard.press(k); await page.waitForTimeout(80);
      }
    } catch (e) { result = '未通过'; error = String(e.message || e).slice(0, 160); }
    await page.waitForTimeout(300);
    const after = snap();
    if (after.c > before.c || after.p > before.p) {
      const ne = consoleErrors.slice(before.c).concat(pageErrors.slice(before.p));
      if (ne.length) { result = '未通过'; error = ne[0].slice(0, 160); }
    }
    results.push({ id: 'canvas#smoke', type: 'canvas', label: 'p5 画布交互', selector: 'canvas',
      action: 'click×5 + key×7', result, error, repairHint: '画布内控件需结合视觉确认' });
  }

  await browser.close();

  /* ---------- 7. 汇总 + 门控结果块 ---------- */
  const pass = results.filter(r => r.result === '通过').length;
  const fail = results.length - pass;
  const summary = { total: results.length, pass, fail, consoleErrors: consoleErrors.length, pageErrors: pageErrors.length, benign: benignErrors.length };

  const gateBlock =
`【强制测试门控结果块 · 自动实测 by playwright-control-test-harness】
控件总数：${results.length}
| 控件名 | 类型 | 测试方法 | 结果 | 备注 |
|--------|------|----------|------|------|
${results.map(r => `| ${r.label} (${r.id}) | ${r.type} | 自动触发 | ${r.result} | ${r.error ? r.error.slice(0,40) : (r.repairHint||'OK')} |`).join('\n')}
控制台错误：${consoleErrors.length} 条（非良性）｜ 页面异常：${pageErrors.length} 条｜ 良性噪声(WebGL等)：${benignErrors.length} 条
结论：${fail === 0 ? '✅ 全部通过，准予提交' : `⛔ 存在 ${fail} 个未通过控件，禁止提交，须修复并复测`}`;

  const report = { target: displayName, targetUrl, summary, controls: results, consoleErrors, pageErrors, benignErrors, gateBlock };
  const exitCode = fail === 0 ? 0 : 2;

  /* ---------- 8. 输出 ---------- */
  const jsonOut = jsonPath || (outDir ? path.join(outDir, 'control-test-report.json') : 'control-test-report.json');
  const mdOut = mdPath || (outDir ? path.join(outDir, 'control-test-gate.md') : 'control-test-gate.md');
  fs.mkdirSync(path.dirname(path.resolve(jsonOut)), { recursive: true });
  fs.writeFileSync(jsonOut, JSON.stringify(report, null, 2));
  fs.writeFileSync(mdOut, `# ${displayName} · 控件自动实测报告\n\n${gateBlock}\n`);

  console.log(`\n=== 控件自动实测 · ${displayName} ===`);
  console.log(`控件 ${results.length} 个 · 通过 ${pass} · 未通过 ${fail} · 报错 ${consoleErrors.length + pageErrors.length}（良性 ${benignErrors.length}）`);
  console.log(gateBlock);
  console.log(`\n报告已写出:\n  JSON: ${jsonOut}\n  MD  : ${mdOut}`);
  process.exit(exitCode);
})().catch(e => { console.error('harness 运行失败:', e); process.exit(3); });
