#!/usr/bin/env node
/**
 * crawl.js — Multi-page crawler for extracting data from paginated sites
 * 
 * Usage:
 *   node crawl.js <url> <selector> [maxPages]
 * 
 * Examples:
 *   node crawl.js https://example.com/products .product-item 5
 *   node crawl.js https://news.ycombinator.com .athing 3
 */

const puppeteer = require('puppeteer');

const url = process.argv[2];
const selector = process.argv[3];
const maxPages = parseInt(process.argv[4]) || 10;

if (!url || !selector) {
  console.error('Usage: node crawl.js <url> <selector> [maxPages]');
  console.error('Example: node crawl.js https://example.com/products .item 5');
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
  
  let allData = [];
  
  for (let i = 1; i <= maxPages; i++) {
    // Build page URL - append ?page=X or &page=X
    let pageUrl = url;
    if (i > 1) {
      pageUrl = url.includes('?') ? `${url}&page=${i}` : `${url}?page=${i}`;
    }
    
    console.error(`[${i}/${maxPages}] Crawling: ${pageUrl}`);
    
    try {
      await page.goto(pageUrl, { 
        waitUntil: 'networkidle2',
        timeout: 30000 
      });
      
      // Small delay for dynamic content
      await new Promise(r => setTimeout(r, 500));
      
      // Extract data
      const data = await page.$$eval(selector, els => 
        els.map(el => {
          const text = el.textContent.trim();
          const link = el.querySelector('a');
          return {
            text,
            href: link ? link.href : null
          };
        })
      );
      
      // Stop if no data found
      if (data.length === 0) {
        console.error(`No more data found at page ${i}, stopping.`);
        break;
      }
      
      allData.push(...data);
      console.error(`  Found ${data.length} items (total: ${allData.length})`);
      
    } catch (err) {
      console.error(`  Error on page ${i}: ${err.message}`);
      break;
    }
  }
  
  console.log(JSON.stringify(allData, null, 2));
  
  await browser.close();
  process.exit(0);
})().catch(err => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});