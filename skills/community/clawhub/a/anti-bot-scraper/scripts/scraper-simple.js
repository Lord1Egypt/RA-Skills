#!/usr/bin/env node
/**
 * scraper-simple.js - Playwright 普通模式抓取
 *
 * Usage:
 *   node scripts/scraper-simple.js <URL> [--wait <ms>] [--selector <css>]
 *
 * Output: JSON to stdout
 */

const { chromium } = require('playwright');

// ── 参数解析 ──────────────────────────────────────────────
function parseArgs(argv) {
  const args = argv.slice(2);
  const opts = { url: null, wait: 2000, selector: null };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--wait' && args[i + 1]) {
      opts.wait = parseInt(args[++i], 10);
    } else if (args[i] === '--selector' && args[i + 1]) {
      opts.selector = args[++i];
    } else if (!args[i].startsWith('--') && !opts.url) {
      opts.url = args[i];
    }
  }

  if (!opts.url) {
    console.error('Usage: node scraper-simple.js <URL> [--wait <ms>] [--selector <css>]');
    process.exit(1);
  }
  return opts;
}

// ── 页面内容提取 ──────────────────────────────────────────
async function extractContent(page, selector) {
  return page.evaluate((sel) => {
    const root = sel ? document.querySelector(sel) : document.body;
    if (!root) return { content: '', links: [], images: [] };

    // 提取文本
    const content = root.innerText || root.textContent || '';

    // 提取链接
    const linkEls = root.querySelectorAll('a[href]');
    const links = Array.from(linkEls)
      .map((a) => ({ text: (a.innerText || '').trim(), href: a.href }))
      .filter((l) => l.href && l.href.startsWith('http'))
      .slice(0, 200);

    // 提取图片
    const imgEls = root.querySelectorAll('img[src]');
    const images = Array.from(imgEls)
      .map((img) => ({ alt: img.alt || '', src: img.src }))
      .filter((i) => i.src)
      .slice(0, 100);

    return { content, links, images };
  }, selector);
}

// ── 提取 meta 信息 ────────────────────────────────────────
async function extractMetadata(page) {
  return page.evaluate(() => {
    const getMeta = (name) => {
      const el =
        document.querySelector(`meta[name="${name}"]`) ||
        document.querySelector(`meta[property="${name}"]`) ||
        document.querySelector(`meta[property="og:${name}"]`);
      return el ? el.getAttribute('content') : '';
    };
    return {
      description: getMeta('description'),
      keywords: getMeta('keywords'),
      author: getMeta('author'),
      ogTitle: getMeta('og:title'),
      ogDescription: getMeta('og:description'),
      ogImage: getMeta('og:image'),
    };
  });
}

// ── 主流程 ────────────────────────────────────────────────
async function main() {
  const opts = parseArgs(process.argv);
  const startTime = Date.now();

  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    // 导航
    await page.goto(opts.url, { waitUntil: 'domcontentloaded', timeout: 30000 });

    // 等待
    if (opts.wait > 0) {
      await page.waitForTimeout(opts.wait);
    }

    // 提取
    const title = await page.title();
    const { content, links, images } = await extractContent(page, opts.selector);
    const metadata = await extractMetadata(page);

    const result = {
      success: true,
      url: opts.url,
      title,
      content: content.slice(0, 50000), // 限制大小
      links,
      images,
      metadata,
      elapsedSeconds: parseFloat(((Date.now() - startTime) / 1000).toFixed(2)),
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    const result = {
      success: false,
      url: opts.url,
      error: err.message,
      elapsedSeconds: parseFloat(((Date.now() - startTime) / 1000).toFixed(2)),
    };
    console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  } finally {
    if (browser) await browser.close();
  }
}

main();
