#!/usr/bin/env node
/**
 * NotebookLM Playwright 全链路验证脚本
 *
 * 用法（在 macOS Terminal 中运行，不要在 sandboxed 环境）：
 *   node scripts/path-check.js
 *
 * 验证 6 个 checkpoint：
 *   1. 登录态有效（cookies 加载成功）
 *   2. 主页"新建笔记本"按钮可见
 *   3. 创建 notebook 成功（URL 跳转）
 *   4. addSource 对话框自动弹出
 *   5. 文本来源上传成功（来源数=1）
 *   6. 思维导图触发生成成功
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const STORAGE_STATE = '~/.notebooklm/storage-state.json';
const OUTPUT_DIR = '/tmp/nlm-pathcheck';

const TEST_CONTENT = `路径验证测试内容

这是一段用于验证 NotebookLM Playwright 自动化全链路是否正常的测试文本。
内容覆盖：登录态保留、新建 notebook、添加来源、粘贴文本、触发生成。

## 主题：AI Agent 设计模式
2024 年是 AI Agent 落地元年，主要模式包括 ReAct、Plan-and-Solve、多智能体协同。
ReAct 模式结合推理和行动，是当前最流行的 Agent 设计范式。
Plan-and-Solve 先生成完整计划再执行，可观测性高但灵活性低。
全球 Agent 市场预计 2030 年突破 500 亿美元。
`;

async function main() {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ storageState: STORAGE_STATE, viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  const checkpoints = [];
  const cp = (name, ok, detail) => {
    const status = ok ? '✅' : '❌';
    console.log(status + ' ' + name + (detail ? ' — ' + detail : ''));
    checkpoints.push({ name, ok, detail });
  };

  try {
    console.log('\n[1/6] Open home page');
    await page.goto('https://notebooklm.google.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(4000);
    const currentUrl = page.url();
    cp('Auth & home loaded', currentUrl.includes('notebooklm.google.com') && !currentUrl.includes('accounts.google.com'), 'URL=' + currentUrl);

    console.log('\n[2/6] Find new notebook button');
    await page.evaluate(() => document.querySelectorAll('.cdk-overlay-container, [class*="overlay-backdrop"]').forEach(el => el.remove()));
    const newBtnCount = await page.locator('[aria-label="新建笔记本"]').count();
    cp('New notebook button visible', newBtnCount > 0, 'count=' + newBtnCount);
    if (newBtnCount === 0) throw new Error('Cannot find new notebook button');

    console.log('\n[3/6] Click new notebook');
    await page.locator('[aria-label="新建笔记本"]').first().click();
    let notebookId = null;
    for (let i = 0; i < 20; i++) {
      await page.waitForTimeout(2000);
      const m = page.url().match(/\/notebook\/([a-f0-9-]+)/);
      if (m) { notebookId = m[1]; break; }
    }
    cp('Notebook created', !!notebookId, 'ID=' + notebookId);
    if (!notebookId) throw new Error('Notebook ID not in URL');

    console.log('\n[4/6] Wait addSource dialog');
    await page.waitForTimeout(4000);
    let dialogOk = false;
    try {
      await page.waitForSelector('.mat-mdc-dialog-container', { timeout: 15000 });
      dialogOk = true;
    } catch (e) {}
    cp('addSource dialog auto-shown', dialogOk);
    await page.screenshot({ path: OUTPUT_DIR + '/04-dialog.png', fullPage: true });

    console.log('\n[5/6] Upload text source');
    const pasted = await page.evaluate(() => {
      const all = Array.from(document.querySelectorAll('*'));
      const target = all.find(el => {
        const t = (el.textContent || '').trim();
        return (t === '复制的文字' || t === 'Copied text') && el.offsetParent !== null;
      });
      if (target) { target.click(); return true; }
      return false;
    });
    if (!pasted) throw new Error('"复制的文字" not found');
    await page.waitForTimeout(2500);

    const filled = await page.evaluate((content) => {
      const tas = Array.from(document.querySelectorAll('textarea'));
      const ta = tas.find(el => {
        const p = el.placeholder || '';
        const a = el.getAttribute('aria-label') || '';
        return p.includes('粘贴') || p.includes('Paste') || a.includes('粘贴');
      });
      if (ta) {
        ta.value = content;
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
      }
      return false;
    }, TEST_CONTENT);
    if (!filled) throw new Error('Textarea fill failed');
    await page.waitForTimeout(2000);

    await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll('button'));
      const ins = buttons.find(b => {
        const t = (b.textContent || '').trim();
        return (t === '插入' || t === 'Insert') && b.offsetParent !== null;
      });
      if (ins) ins.click();
    });

    let sourceCount = 0;
    for (let i = 0; i < 24; i++) {
      await page.waitForTimeout(5000);
      sourceCount = await page.evaluate(() => {
        const m = document.body.innerText.match(/(\d+)\s*个来源/);
        return m ? parseInt(m[1]) : 0;
      });
      if (sourceCount > 0) break;
    }
    cp('Source uploaded', sourceCount > 0, 'count=' + sourceCount);
    if (sourceCount === 0) throw new Error('Source upload failed');
    await page.waitForTimeout(8000);

    console.log('\n[6/6] Trigger 思维导图 generation');
    await page.evaluate(() => document.querySelectorAll('.cdk-overlay-container, [class*="overlay-backdrop"]').forEach(el => el.remove()));
    await page.locator('[aria-label="思维导图"]').first().click({ timeout: 8000 });

    let genStarted = false;
    let genStatus = 'unknown';
    for (let i = 0; i < 8; i++) {
      await page.waitForTimeout(5000);
      const text = await page.evaluate(() => document.body.innerText);
      if (text.includes('正在生成') || text.includes('Generating')) {
        genStarted = true; genStatus = 'started'; break;
      }
      if (text.includes('已达到每日') || text.includes('daily limit')) {
        genStatus = 'limit'; break;
      }
    }
    cp('思维导图 generation triggered', genStarted, 'status=' + genStatus);
    await page.screenshot({ path: OUTPUT_DIR + '/06-final.png', fullPage: true });

    console.log('\n=== Path verification summary ===');
    const passCount = checkpoints.filter(c => c.ok).length;
    console.log('Passed: ' + passCount + ' / ' + checkpoints.length);
    console.log('Notebook: https://notebooklm.google.com/notebook/' + notebookId);
    console.log('Screenshots: ' + OUTPUT_DIR);

    fs.writeFileSync(OUTPUT_DIR + '/result.json', JSON.stringify({
      timestamp: new Date().toISOString(), notebookId, checkpoints,
      passed: passCount, total: checkpoints.length
    }, null, 2));

    process.exit(passCount === checkpoints.length ? 0 : 2);
  } catch (err) {
    console.error('\nFATAL: ' + err.message);
    try { await page.screenshot({ path: OUTPUT_DIR + '/error.png', fullPage: true }); } catch (e) {}
    fs.writeFileSync(OUTPUT_DIR + '/result.json', JSON.stringify({
      timestamp: new Date().toISOString(), checkpoints, error: err.message
    }, null, 2));
    process.exit(1);
  } finally {
    await browser.close();
  }
}

main();
