#!/usr/bin/env node
/**
 * NotebookLM Playwright Generator
 * 替代 CLI generate 命令（因 CLI HTTP 400 问题）
 *
 * 用法：
 *   node notebooklm-playwright.js <notebookTitle> <generateType> [outputDir]
 *
 * 注意：传入 notebook 标题（如"公众号测试-NotebookLM"），而非 CLI ID
 *       因为 CLI ID 和 Web URL ID 格式不一致
 *
 * generateType: audio | video | report | mindmap | flashcards | quiz
 * outputDir: 可选，下载保存目录
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const STORAGE_STATE = '~/.notebooklm/storage-state.json';
const OUTPUT_DIR = process.argv[4] || '/tmp/nlm-output';

// Generate type to UI label mapping
// 必须与 NotebookLM Web UI Studio 面板中的卡片文字一致
const TYPE_MAP = {
  audio: '音频概览',
  video: '视频概览',
  report: '报告',
  mindmap: '思维导图',
  flashcards: '闪卡',
  quiz: '测验',
  presentation: '演示文稿',
  infographic: '信息图',
  datatable: '数据表格',
};

async function waitForGeneration(page, type) {
  const label = TYPE_MAP[type] || type;
  console.log(`Waiting for ${label} generation to complete...`);

  // First confirm generation actually started
  let generationStarted = false;
  for (let i = 0; i < 12; i++) {
    await page.waitForTimeout(5000);
    const text = await page.evaluate(() => document.body.innerText);

    if (text.includes('正在生成') || text.includes('Generating')) {
      console.log(`  Generation started for ${label}`);
      generationStarted = true;
      break;
    }
    if (text.includes('已达到每日') || text.includes('daily limit')) {
      console.log('⚠️ Daily generation limit reached');
      return 'limit';
    }
    if (i === 11) {
      console.log('⚠️ Generation did not start within 60s');
      return false;
    }
  }

  if (!generationStarted) return false;

  // Poll for up to 6 minutes for completion
  for (let i = 0; i < 72; i++) {
    await page.waitForTimeout(5000);

    const text = await page.evaluate(() => document.body.innerText);

    // Check if "正在生成" is gone and download/play/result appears
    if (!text.includes('正在生成') && !text.includes('Generating')) {
      if (text.includes('下载') || text.includes('Download') || text.includes('播放') || text.includes(label)) {
        console.log(`✅ ${label} generation complete!`);
        return true;
      }
    }

    if (i % 6 === 0) {
      console.log(`  Still generating... (${(i + 12) * 5}s elapsed)`);
    }
  }

  console.log('⚠️ Generation may still be in progress');
  return false;
}

async function downloadFile(page, filename) {
  // Wait for download link to appear
  const downloadBtn = await page.$('a[href*=".mp3"], a[href*=".mp4"], a[href*=".pdf"], a[href*=".zip"]');
  if (downloadBtn) {
    const href = await downloadBtn.getAttribute('href');
    console.log(`Download link found: ${href}`);

    // Save output path
    const outputPath = path.join(OUTPUT_DIR, filename);
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });

    // Download using fetch
    const response = await page.evaluate(async (url) => {
      const res = await fetch(url);
      return await res.arrayBuffer();
    }, href);

    fs.writeFileSync(outputPath, Buffer.from(response));
    console.log(`✅ Downloaded to: ${outputPath}`);
    return outputPath;
  }

  // Fallback: just save screenshot
  const screenshotPath = path.join(OUTPUT_DIR, `${filename.replace(/\.[^.]+$/, '')}.png`);
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`📸 Saved screenshot to: ${screenshotPath}`);
  return screenshotPath;
}

async function navigateToNotebook(page, notebookTitle) {
  console.log(`Navigating to notebook: "${notebookTitle}"...`);

  // Go to home page
  await page.goto('https://notebooklm.google.com/', {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await page.waitForTimeout(3000);

  // Remove overlays
  await page.evaluate(() => {
    const overlays = document.querySelectorAll('.cdk-overlay-container, [class*="overlay-backdrop"], .mat-mdc-dialog-container, [role="dialog"]');
    overlays.forEach(el => el.remove());
    document.body.style.overflow = 'auto';
    document.body.style.position = 'static';
  });

  // Find and click the notebook link
  // Strategy: find the span containing the title text, then click its parent <a> tag
  const clicked = await page.evaluate((title) => {
    // Find all spans with the title text
    const spans = Array.from(document.querySelectorAll('span'));
    const titleSpan = spans.find(s => s.textContent.trim() === title || s.textContent.trim().includes(title));

    if (!titleSpan) {
      console.log('Title span not found, trying broader search...');
      return false;
    }

    // Walk up to find the parent <a> tag or click project-button
    let el = titleSpan;
    for (let i = 0; i < 10 && el; i++) {
      if (el.tagName === 'A' && el.href && el.href.includes('/notebook/')) {
        el.click();
        return true;
      }
      if (el.tagName === 'PROJECT-BUTTON') {
        // Try clicking the inner <a> first
        const link = el.querySelector('a[href*="/notebook/"]');
        if (link) {
          link.click();
          return true;
        }
        el.click();
        return true;
      }
      el = el.parentElement;
    }

    return false;
  }, notebookTitle);

  if (!clicked) {
    throw new Error(`Could not find notebook "${notebookTitle}" on the home page`);
  }

  // Wait for navigation
  await page.waitForTimeout(5000);

  const currentUrl = page.url();
  if (currentUrl === 'https://notebooklm.google.com/') {
    throw new Error('Failed to navigate to notebook page - still on home page');
  }

  console.log(`✅ Opened notebook page: ${currentUrl}`);
}

async function uploadTextToNotebook(page, notebookTitle, sourceTitle, content) {
  console.log(`Uploading text source to "${notebookTitle}"...`);

  await navigateToNotebook(page, notebookTitle);
  await page.waitForTimeout(2000);

  // Click "+ 添加来源" (Add Source) button
  // Use evaluate click to bypass Angular CDK overlay interception
  console.log('Clicking "添加来源"...');
  const addSourceClicked = await page.evaluate(() => {
    const byAria = Array.from(document.querySelectorAll('[aria-label*="添加来源"], [aria-label*="Add source"]'));
    if (byAria.length > 0) { byAria[0].click(); return 'aria'; }
    const byText = Array.from(document.querySelectorAll('button, a, [role="button"]')).find(el =>
      el.textContent.includes('添加来源') || el.textContent.includes('Add source')
    );
    if (byText) { byText.click(); return 'text'; }
    return null;
  });

  if (!addSourceClicked) {
    throw new Error('Could not find "添加来源" button');
  }
  console.log('Clicked add source via:', addSourceClicked);
  await page.waitForTimeout(2000);

  // Select "复制的文字" (Copied text) option
  console.log('Selecting "复制的文字"...');
  const pasteClicked = await page.evaluate(() => {
    const byText = Array.from(document.querySelectorAll('button, a, [role="button"], div, span')).find(el =>
      el.textContent.trim() === '复制的文字' || el.textContent.trim() === 'Copied text'
    );
    if (byText) { byText.click(); return 'text'; }
    return null;
  });

  if (!pasteClicked) {
    throw new Error('Could not find "复制的文字" option');
  }
  console.log('Clicked paste text');
  await page.waitForTimeout(2000);

  // Fill content textarea
  console.log('Filling content...');
  await page.evaluate((data) => {
    const textareas = Array.from(document.querySelectorAll('textarea'));
    const contentInput = textareas.find(el =>
      el.placeholder?.includes('粘贴') ||
      el.placeholder?.includes('Paste') ||
      el.getAttribute('aria-label')?.includes('粘贴')
    );
    if (contentInput) {
      contentInput.value = data.content;
      contentInput.dispatchEvent(new Event('input', { bubbles: true }));
      contentInput.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }, { content });
  await page.waitForTimeout(2000);

  // Click "插入" (Insert) button
  console.log('Clicking insert button...');
  const insertClicked = await page.evaluate(() => {
    const searchScopes = [
      document.querySelector('.mat-mdc-dialog-container'),
      document.querySelector('.cdk-overlay-pane'),
      document.querySelector('[role="dialog"]'),
      document.body
    ].filter(Boolean);

    for (const scope of searchScopes) {
      const buttons = Array.from(scope.querySelectorAll('button'));
      const insertBtn = buttons.find(b => b.textContent.trim() === '插入' || b.textContent.trim() === 'Insert');
      if (insertBtn) { insertBtn.click(); return { text: insertBtn.textContent.trim(), scope: scope.className?.substring(0, 30) || 'body' }; }
    }
    return null;
  });

  if (!insertClicked) {
    throw new Error('Could not find "插入" button');
  }
  console.log('Clicked:', insertClicked.text);

  // Wait for upload to complete
  console.log('Waiting for source to be added...');
  for (let i = 0; i < 12; i++) {
    await page.waitForTimeout(5000);
    const sourceCount = await page.evaluate(() => {
      const match = document.body.innerText.match(/(\d+)\s*个来源/);
      return match ? parseInt(match[1]) : 0;
    });
    if (sourceCount > 0) {
      console.log(`✅ Source added! Notebook now has ${sourceCount} source(s)`);
      return true;
    }
  }

  throw new Error('Source was not added after 60s');
}

async function generate(notebookTitle, generateType, outputDir) {
  const OUTPUT_DIR = outputDir || process.argv[4] || '/tmp/nlm-output';
  const label = TYPE_MAP[generateType] || generateType;

  console.log(`\n🎙️ NotebookLM ${label} Generator`);
  console.log(`   Notebook: ${notebookTitle}`);
  console.log(`   Type: ${generateType}`);
  console.log(`   Output: ${OUTPUT_DIR}\n`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ storageState: STORAGE_STATE });

  const page = await context.newPage();

  try {
    // Step 1: Navigate to notebook via home page
    await navigateToNotebook(page, notebookTitle);

    // Step 2: Remove blocking overlays
    console.log('Removing blocking overlays...');
    await page.evaluate(() => {
      const overlays = document.querySelectorAll('.cdk-overlay-container, [class*="overlay-backdrop"], .mat-mdc-dialog-container, [role="dialog"]');
      overlays.forEach(el => el.remove());
      document.body.style.overflow = 'auto';
      document.body.style.position = 'static';
    });
    await page.waitForTimeout(1000);

    // Step 3: Close banner if present
    console.log('Looking for banner/close button...');
    const closeBannerBtn = await page.$('button[aria-label="关闭横幅"], button:has-text("close"), button:has-text("关闭")');
    if (closeBannerBtn) {
      try {
        await closeBannerBtn.click({ timeout: 3000 });
        console.log('Closed banner');
        await page.waitForTimeout(1000);
      } catch (e) {
        await page.evaluate(() => {
          const btn = Array.from(document.querySelectorAll('button')).find(b =>
            b.getAttribute('aria-label')?.includes('关闭') ||
            b.textContent?.includes('close')
          );
          if (btn) btn.click();
        });
        await page.waitForTimeout(1000);
      }
    }

    // Step 4: Click Studio generate card using JavaScript
    console.log(`Clicking ${label} via JS...`);
    const clicked = await page.evaluate((labelText) => {
      // Strategy 1: Exact aria-label match
      let targets = Array.from(document.querySelectorAll('[aria-label]')).filter(el =>
        el.getAttribute('aria-label').trim() === labelText
      );
      if (targets.length > 0) {
        targets[0].click();
        return 'aria-exact:' + targets[0].getAttribute('aria-label');
      }

      // Strategy 2: Partial aria-label match (specific label only)
      targets = Array.from(document.querySelectorAll('[aria-label*="' + labelText + '"]'));
      if (targets.length > 0) {
        targets[0].click();
        return 'aria-partial:' + targets[0].getAttribute('aria-label');
      }

      // Strategy 3: Text content in buttons/cards
      targets = Array.from(document.querySelectorAll('button, [role="button"], div, span')).filter(b =>
        b.textContent.trim() === labelText || b.textContent.includes(labelText)
      );
      if (targets.length > 0) {
        targets[0].click();
        return 'text:' + targets[0].textContent.trim();
      }

      return null;
    }, label);

    if (!clicked) {
      throw new Error(`Could not find ${label} button/card`);
    }

    console.log(`Clicked: ${clicked}`);
    await page.waitForTimeout(3000);

    // Step 5: Wait for generation
    // Note: NotebookLM Studio cards directly trigger generation on click.
    // There is no secondary "Generate/Create" button in the current UI.
    const genResult = await waitForGeneration(page, generateType);
    if (genResult === 'limit') {
      throw new Error('Daily generation limit reached');
    }
    if (!genResult) {
      throw new Error('Generation failed or timed out');
    }

    // Step 7: Take screenshot of result
    const screenshotPath = path.join(OUTPUT_DIR, `${generateType}_result.png`);
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    await page.screenshot({ path: screenshotPath, fullPage: true });
    console.log(`📸 Screenshot: ${screenshotPath}`);

    // Step 8: Try to download
    const dlPath = await downloadFile(page, `${notebookTitle.replace(/[^a-zA-Z0-9\u4e00-\u9fff]/g, '_')}_${generateType}`);
    console.log(`\n✅ Done! Output: ${dlPath}`);

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    // Save error screenshot
    try {
      const errorPath = path.join(OUTPUT_DIR, 'error_screenshot.png');
      fs.mkdirSync(OUTPUT_DIR, { recursive: true });
      await page.screenshot({ path: errorPath, fullPage: true });
      console.log(`📸 Error screenshot saved: ${errorPath}`);
    } catch (e) {}
    throw error;
  } finally {
    await browser.close();
  }
}

// Main
async function main() {
  const mode = process.argv[2];

  if (mode === 'upload-text') {
    const notebookTitle = process.argv[3];
    const sourceTitle = process.argv[4];
    const content = process.argv[5];
    if (!notebookTitle || !sourceTitle || !content) {
      console.log(`
Upload text source to NotebookLM

用法：
  node notebooklm-playwright.js upload-text <notebookTitle> <sourceTitle> <content>

示例：
  node notebooklm-playwright.js upload-text "公众号测试-NotebookLM" "文章标题" "文章内容..."
`);
      process.exit(1);
    }
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ storageState: STORAGE_STATE });
    const page = await context.newPage();
    try {
      await uploadTextToNotebook(page, notebookTitle, sourceTitle, content);
    } finally {
      await browser.close();
    }
    return;
  }

  if (mode === 'generate' || (!mode.startsWith('upload') && process.argv[2])) {
    const notebookTitle = mode === 'generate' ? process.argv[3] : process.argv[2];
    const generateType = (mode === 'generate' ? process.argv[4] : process.argv[3]) || 'audio';
    const outputDir = mode === 'generate' ? process.argv[5] : process.argv[4];

    if (!notebookTitle) {
      console.log(`
NotebookLM Playwright Automation

用法：
  # 上传文本来源
  node notebooklm-playwright.js upload-text <notebookTitle> <sourceTitle> <content>

  # 生成内容
  node notebooklm-playwright.js generate <notebookTitle> <generateType> [outputDir]
  # 或简写
  node notebooklm-playwright.js <notebookTitle> <generateType> [outputDir]

generateType: audio | video | report | mindmap | flashcards | quiz | presentation | infographic | datatable

示例：
  node notebooklm-playwright.js upload-text "公众号测试" "文章标题" "文章内容..."
  node notebooklm-playwright.js generate "巴菲特给股东的一封信" audio /tmp/results
  node notebooklm-playwright.js "巴菲特给股东的一封信" report
`);
      process.exit(1);
    }

    await generate(notebookTitle, generateType, outputDir);
    return;
  }

  console.log(`
NotebookLM Playwright Automation

用法：
  node notebooklm-playwright.js upload-text <notebookTitle> <sourceTitle> <content>
  node notebooklm-playwright.js generate <notebookTitle> <generateType> [outputDir]
`);
  process.exit(1);
}

main().then(() => process.exit(0)).catch((err) => {
  console.error(err.message);
  process.exit(1);
});
