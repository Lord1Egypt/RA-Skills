#!/usr/bin/env node
/**
 * Playwright Scraper — 三种模式
 * 
 * 用法: node playwright-scrape.js <URL> [mode]
 * 
 * mode:
 *   headless  — 默认，headless Chrome，适合普通网站
 *   gui       — 连接已启动的 Chrome 实例（需要先启动: google-chrome --remote-debugging-port=9222 --new-window）
 *   stealth   — headless + 反爬参数，适合有检测的网站
 */

const { chromium } = require('/home/axelhu/.openclaw/workspace/node_modules/playwright');

const url = process.argv[2];
const mode = process.argv[3] || 'headless';

if (!url) {
  console.error('用法: node playwright-scrape.js <URL> [headless|gui|stealth]');
  process.exit(1);
}

const EXEC_PATH = '/usr/bin/google-chrome';

const ARGS_HEADLESS = [
  '--no-sandbox',
  '--disable-setuid-sandbox',
  '--disable-dev-shm-usage',
  '--disable-gpu',
];

const ARGS_STEALTH = [
  '--disable-blink-features=AutomationControlled',
  '--disable-setuid-sandbox',
  '--no-sandbox',
  '--no-first-run',
  '--no-zygote',
  '--disable-gpu',
  '--disable-dev-shm-usage',
  '--disable-l-inf',
  '--disable-gpu-sandbox',
];

async function scrape() {
  let browser;

  if (mode === 'gui') {
    // 连接已有 Chrome 实例（需要先启动: google-chrome --remote-debugging-port=9222 --new-window <url>）
    browser = await chromium.connectOverCDP('http://localhost:9222');
  } else {
    const args = mode === 'stealth' ? ARGS_STEALTH : ARGS_HEADLESS;
    browser = await chromium.launch({
      headless: true,
      executablePath: EXEC_PATH,
      args,
    });
  }

  const context = await browser.newContext();
  const page = await context.newPage();

  const startTime = Date.now();
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });
  } catch(e) {
    // 部分网站超时也继续
  }
  await page.waitForTimeout(4000);
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);

  const result = await page.evaluate(() => {
    const title = document.title || '';
    let content = '';
    const jsContent = document.getElementById('js_content');
    if (jsContent) {
      content = jsContent.innerText || '';
    } else {
      content = document.body ? (document.body.innerText || '') : '';
    }
    const images = Array.from(document.querySelectorAll('img'))
      .filter(img => img.naturalWidth > 100 && img.src.startsWith('http'))
      .map(img => img.src).slice(0, 10);
    const links = Array.from(document.querySelectorAll('a[href]'))
      .filter(a => a.href.startsWith('http'))
      .map(a => ({ text: a.innerText.trim().substring(0, 100), href: a.href }))
      .slice(0, 20);
    return { title, content, images, links };
  });

  // gui 模式下不关闭浏览器（由用户手动关闭）
  if (mode !== 'gui') {
    await browser.close();
  }

  console.log(JSON.stringify({
    url,
    mode,
    title: result.title,
    content: result.content.substring(0, 15000),
    images: result.images,
    links: result.links,
    loadTime: `${elapsed}s`
  }, null, 2));
}

scrape().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
