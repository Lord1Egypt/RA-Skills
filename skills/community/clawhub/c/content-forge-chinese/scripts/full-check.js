#!/usr/bin/env node
/**
 * NotebookLM 全生成类型验证脚本
 *
 * 用法：
 *   node scripts/full-check.js
 *
 * 验证 9 种生成类型 + 2 个基础 checkpoint：
 *   - 新建 notebook + 上传文本
 *   - 依次测试：mindmap, flashcards, quiz, presentation, infographic, datatable
 *   - 依次测试：audio, video, report
 */

const { chromium } = require('playwright');
const fs = require('fs');

const STORAGE_STATE = '~/.notebooklm/storage-state.json';
const OUTPUT_DIR = '/tmp/nlm-fullcheck';

const TEST_CONTENT = `NotebookLM 全类型验证测试

这是一段用于验证 NotebookLM 所有生成类型的测试文本。
内容涵盖：AI Agent 设计模式、市场预测、技术趋势。

2024 年是 AI Agent 落地元年，主要模式包括 ReAct、Plan-and-Solve、多智能体协同。
全球 Agent 市场预计 2030 年突破 500 亿美元。
大模型技术在代码生成、文档理解、多模态推理方面持续突破。
`;

// 9 种生成类型
const GENERATE_TYPES = [
  { key: 'mindmap',     label: '思维导图',   aria: '思维导图',       category: 'notebook' },
  { key: 'flashcards',  label: '闪卡',       aria: '闪卡',           category: 'notebook' },
  { key: 'quiz',        label: '测验',       aria: '测验',           category: 'notebook' },
  { key: 'presentation',label: '演示文稿',   aria: '演示文稿',       category: 'notebook' },
  { key: 'infographic', label: '信息图',     aria: '信息图',         category: 'notebook' },
  { key: 'datatable',   label: '数据表格',   aria: '数据表格',       category: 'notebook' },
  { key: 'audio',       label: '音频概览',   aria: '音频概览',       category: 'account' },
  { key: 'video',       label: '视频概览',   aria: '视频概览',       category: 'account' },
  { key: 'report',      label: '报告',       aria: '报告',           category: 'account' },
];

async function main() {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ storageState: STORAGE_STATE, viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  const results = [];
  let notebookId = null;

  try {
    // === Step 1: 登录 + 首页 ===
    console.log('\n[基础] 打开首页...');
    await page.goto('https://notebooklm.google.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(4000);
    const currentUrl = page.url();
    const authOk = currentUrl.includes('notebooklm.google.com') && !currentUrl.includes('accounts.google.com');
    console.log(authOk ? '✅ 登录态有效' : '❌ 登录态失效');
    if (!authOk) throw new Error('Auth failed');

    // === Step 2: 新建 notebook ===
    console.log('\n[基础] 新建 notebook...');
    await page.evaluate(() => document.querySelectorAll('.cdk-overlay-container, [class*="overlay-backdrop"]').forEach(el => el.remove()));
    const newBtnCount = await page.locator('[aria-label="新建笔记本"]').count();
    if (newBtnCount === 0) throw new Error('Cannot find new notebook button');
    await page.locator('[aria-label="新建笔记本"]').first().click();
    for (let i = 0; i < 20; i++) {
      await page.waitForTimeout(2000);
      const m = page.url().match(/\/notebook\/([a-f0-9-]+)/);
      if (m) { notebookId = m[1]; break; }
    }
    console.log(notebookId ? '✅ Notebook 创建成功: ' + notebookId : '❌ Notebook 创建失败');
    if (!notebookId) throw new Error('Notebook creation failed');

    // === Step 3: 上传文本 ===
    console.log('\n[基础] 上传测试文本...');
    await page.waitForTimeout(4000);
    try {
      await page.waitForSelector('.mat-mdc-dialog-container', { timeout: 15000 });
    } catch (e) {}

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
    console.log(sourceCount > 0 ? '✅ 上传成功，来源数=' + sourceCount : '❌ 上传失败');
    if (sourceCount === 0) throw new Error('Source upload failed');
    await page.waitForTimeout(8000);

    // === Step 4: 依次测试 9 种生成类型 ===
    console.log('\n========== 生成类型验证开始 ==========');
    for (const type of GENERATE_TYPES) {
      console.log(`\n[${type.key}] 测试 ${type.label}...`);

      // 清除 overlay
      await page.evaluate(() => document.querySelectorAll('.cdk-overlay-container, [class*="overlay-backdrop"]').forEach(el => el.remove()));
      await page.waitForTimeout(1000);

      // 点击生成按钮
      let clicked = false;
      try {
        const count = await page.locator('[aria-label="' + type.aria + '"]').count();
        if (count > 0) {
          await page.locator('[aria-label="' + type.aria + '"]').first().click({ timeout: 8000 });
          clicked = true;
        }
      } catch (e) {}

      if (!clicked) {
        console.log('❌ 未找到按钮: ' + type.aria);
        results.push({ key: type.key, label: type.label, status: 'button-not-found', category: type.category });
        continue;
      }

      // 等待结果
      let genStarted = false;
      let genLimit = false;
      let genError = false;
      let statusDetail = 'unknown';

      for (let i = 0; i < 10; i++) {
        await page.waitForTimeout(5000);
        const text = await page.evaluate(() => document.body.innerText);

        if (text.includes('正在生成') || text.includes('Generating') || text.includes('创建中')) {
          genStarted = true; statusDetail = 'started'; break;
        }
        if (text.includes('已达到每日') || text.includes('daily limit') || text.includes('已达上限')) {
          genLimit = true; statusDetail = 'daily-limit'; break;
        }
        // 检测错误弹窗
        if (text.includes('出错了') || text.includes('错误') || text.includes('Error')) {
          // 检查是否是配额错误
          if (text.includes('limit') || text.includes('配额') || text.includes('上限')) {
            genLimit = true; statusDetail = 'daily-limit'; break;
          }
        }
      }

      if (genStarted) {
        console.log('✅ ' + type.label + ' 已触发生成');
        results.push({ key: type.key, label: type.label, status: 'success', category: type.category });
      } else if (genLimit) {
        console.log('🟡 ' + type.label + ' 达到每日上限');
        results.push({ key: type.key, label: type.label, status: 'daily-limit', category: type.category });
      } else {
        console.log('❌ ' + type.label + ' 未知状态');
        results.push({ key: type.key, label: type.label, status: 'unknown', category: type.category });
      }

      // 截图
      await page.screenshot({ path: OUTPUT_DIR + '/' + type.key + '.png', fullPage: true });

      // 如果是成功生成，多等一会儿让生成完成
      if (genStarted) {
        console.log('  等待生成完成...');
        for (let i = 0; i < 24; i++) {
          await page.waitForTimeout(5000);
          const text = await page.evaluate(() => document.body.innerText);
          if (!text.includes('正在生成') && !text.includes('Generating') && !text.includes('创建中')) {
            console.log('  ✅ 生成完成');
            break;
          }
          if (i === 23) {
            console.log('  🟡 生成超时（>2min），可能仍在后台运行');
          }
        }
      }

      // 每个类型测试后返回 notebook 页面（防止弹窗影响下一个）
      await page.goto('https://notebooklm.google.com/notebook/' + notebookId, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(5000);
    }

    // === 汇总 ===
    console.log('\n========== 验证结果汇总 ==========');
    const notebookOk = results.filter(r => r.category === 'notebook' && r.status === 'success').length;
    const notebookTotal = results.filter(r => r.category === 'notebook').length;
    const accountOk = results.filter(r => r.category === 'account' && r.status === 'success').length;
    const accountTotal = results.filter(r => r.category === 'account').length;
    const limitCount = results.filter(r => r.status === 'daily-limit').length;

    console.log('\n🟢 Notebook 级（新建即重置）:');
    results.filter(r => r.category === 'notebook').forEach(r => {
      const icon = r.status === 'success' ? '✅' : r.status === 'daily-limit' ? '🟡' : '❌';
      console.log('  ' + icon + ' ' + r.label + ' (' + r.key + ')');
    });

    console.log('\n🔴 账号级（新 notebook 无法重置）:');
    results.filter(r => r.category === 'account').forEach(r => {
      const icon = r.status === 'success' ? '✅' : r.status === 'daily-limit' ? '🟡' : '❌';
      console.log('  ' + icon + ' ' + r.label + ' (' + r.key + ')');
    });

    console.log('\n总计: ' + results.filter(r => r.status === 'success').length + '/' + results.length + ' 通过');
    console.log('Notebook: ' + notebookOk + '/' + notebookTotal);
    console.log('Account: ' + accountOk + '/' + accountTotal);
    console.log('Daily limit: ' + limitCount);
    console.log('Notebook URL: https://notebooklm.google.com/notebook/' + notebookId);
    console.log('Screenshots: ' + OUTPUT_DIR);

    fs.writeFileSync(OUTPUT_DIR + '/result.json', JSON.stringify({
      timestamp: new Date().toISOString(),
      notebookId,
      results,
      summary: { notebookOk, notebookTotal, accountOk, accountTotal, limitCount, totalOk: results.filter(r => r.status === 'success').length, total: results.length }
    }, null, 2));

    process.exit(0);
  } catch (err) {
    console.error('\nFATAL: ' + err.message);
    try { await page.screenshot({ path: OUTPUT_DIR + '/error.png', fullPage: true }); } catch (e) {}
    fs.writeFileSync(OUTPUT_DIR + '/result.json', JSON.stringify({
      timestamp: new Date().toISOString(), notebookId, results, error: err.message
    }, null, 2));
    process.exit(1);
  } finally {
    await browser.close();
  }
}

main();
