#!/usr/bin/env node
/**
 * scrape.js — Extract text content from web pages using Puppeteer
 * 
 * Usage:
 *   node scrape.js <url> [selector]
 * 
 * Examples:
 *   node scrape.js https://news.ycombinator.com
 *   node scrape.js https://example.com .product-item
 */

const puppeteer = require('puppeteer');

const url = process.argv[2];
const selector = process.argv[3] || 'body';

if (!url) {
  console.error('Usage: node scrape.js <url> [selector]');
  console.error('Example: node scrape.js https://example.com h2');
  process.exit(1);
}

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  // Set a neutral user agent
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
  
  console.error(`Fetching: ${url}`);
  
  await page.goto(url, { 
    waitUntil: 'networkidle2',
    timeout: 30000 
  });
  
  // Wait a bit for dynamic content
  await new Promise(r => setTimeout(r, 1000));
  
  // Extract content based on selector
  const content = await page.$$eval(selector, els => 
    els.map(el => {
      // Get text content, preserving structure
      const text = el.textContent.trim();
      // If it's a link, also get href
      if (el.tagName === 'A') {
        return { text, href: el.href };
      }
      // If it contains images, get src
      const img = el.querySelector('img');
      if (img) {
        return { text, imgSrc: img.src };
      }
      return { text };
    })
  );
  
  console.log(JSON.stringify(content, null, 2));
  
  await browser.close();
  process.exit(0);
})().catch(err => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});