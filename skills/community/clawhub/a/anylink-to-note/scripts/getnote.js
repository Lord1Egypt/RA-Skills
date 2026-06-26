#!/usr/bin/env node
// Extract content from Get Notes shared links using Playwright
// Usage: node getnote.js <url>
const { chromium } = require('playwright');

async function extractGetNote(url) {
  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    await page.goto(url, {
      waitUntil: 'domcontentloaded',
      timeout: 25000,
    });

    // Wait for JS rendering
    await page.waitForTimeout(6000);

    const title = await page.title();
    const content = await page.evaluate(() => {
      const el = document.querySelector('#app') || document.body;
      return (el && 'innerText' in el) ? el.innerText : '';
    });

    if (!content || content.trim().length < 50) {
      console.error('GetNote: content too short or blocked');
      return null;
    }

    const isBlocked =
      title?.includes('无法查看') ||
      title?.includes('不存在') ||
      title?.includes('已删除') ||
      title?.includes('访问限制');

    if (isBlocked) {
      console.error('GetNote: note blocked, title =', title);
      return null;
    }

    return { title, content: content.trim() };
  } catch (err) {
    console.error('GetNote error:', err.message);
    return null;
  } finally {
    if (browser) await browser.close();
  }
}

const url = process.argv[2];
if (!url) {
  console.error('Usage: node getnote.js <url>');
  process.exit(1);
}

extractGetNote(url).then(result => {
  if (result) {
    console.log(JSON.stringify(result));
  } else {
    process.exit(1);
  }
});
