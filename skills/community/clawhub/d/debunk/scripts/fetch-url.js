#!/usr/bin/env node
/**
 * fetch-url.js — Playwright-based URL fetcher for anti-scraping sites (WeChat public accounts, etc.)
 *
 * Usage:
 *   node scripts/fetch-url.js <url> [--max-chars 15000] [--wait-ms 3000]
 *
 * Outputs extracted markdown text to stdout.
 * Returns exit code 0 on success, 1 on failure.
 */

const { chromium } = require('playwright');
const { URL } = require('url');

// Block private/internal URLs to prevent SSRF
function isBlocked(urlStr) {
  try {
    const url = new URL(urlStr);
    const hostname = url.hostname.toLowerCase();
    // Block localhost and loopback
    if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1' || hostname === '0.0.0.0') return true;
    // Block private IP ranges (10.x, 172.16-31.x, 192.168.x)
    if (/^(10\.|172\.(1[6-9]|2\d|3[01])\.|192\.168\.)/.test(hostname)) return true;
    // Block .local domains
    if (hostname.endsWith('.local') || hostname.endsWith('.internal')) return true;
    // Only allow http/https
    if (!['http:', 'https:'].includes(url.protocol)) return true;
    return false;
  } catch {
    return true; // Invalid URL
  }
}

async function main() {
  const args = process.argv.slice(2);
  const url = args.find(a => !a.startsWith('--'));
  if (!url) {
    console.error('Usage: fetch-url.js <url> [--max-chars 15000] [--wait-ms 3000]');
    process.exit(1);
  }
  if (isBlocked(url)) {
    console.error('ERROR: Blocked URL — private/internal addresses are not allowed for security reasons.');
    process.exit(1);
  }

  const maxCharsIdx = args.indexOf('--max-chars');
  const maxChars = maxCharsIdx !== -1 ? parseInt(args[maxCharsIdx + 1], 10) : 15000;

  const waitMsIdx = args.indexOf('--wait-ms');
  const waitMs = waitMsIdx !== -1 ? parseInt(args[waitMsIdx + 1], 10) : 3000;

  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      locale: 'zh-CN',
    });
    const page = await context.newPage();

    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

    // Wait extra for lazy-loaded content (especially WeChat articles)
    await page.waitForTimeout(waitMs);

    // Scroll to bottom to trigger lazy loading
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(1000);

    // Extract article content — try specific selectors first, then fallback
    const text = await page.evaluate(() => {
      // WeChat public account article
      const wechatArticle = document.querySelector('#js_content');
      if (wechatArticle) return wechatArticle.innerText;

      // Generic article content
      const article = document.querySelector('article');
      if (article) return article.innerText;

      // Fallback: main content area
      const main = document.querySelector('main') || document.querySelector('.article-content') || document.querySelector('.rich_media_content');
      if (main) return main.innerText;

      // Last resort: body (strip scripts/styles)
      const clone = document.body.cloneNode(true);
      clone.querySelectorAll('script, style, nav, header, footer, aside').forEach(el => el.remove());
      return clone.innerText;
    });

    if (!text || text.trim().length < 50) {
      console.error('ERROR: Could not extract meaningful content from the page.');
      process.exit(1);
    }

    const result = text.trim().slice(0, maxChars);
    console.log(result);
  } catch (err) {
    console.error(`ERROR: ${err.message}`);
    process.exit(1);
  } finally {
    if (browser) await browser.close();
  }
}

main();
