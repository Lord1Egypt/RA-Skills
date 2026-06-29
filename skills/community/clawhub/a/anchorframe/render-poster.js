/** Render poster.html to PNG using Playwright (Node.js) */
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 1200 } });
  const htmlPath = 'file:///' + path.resolve(__dirname, 'poster.html').replace(/\\/g, '/');
  await page.goto(htmlPath, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  const outPath = path.resolve(__dirname, '创作锚-钓鱼论-海报.png');
  await page.screenshot({ path: outPath, type: 'png' });
  await browser.close();
  console.log('Poster saved:', outPath);
})();
