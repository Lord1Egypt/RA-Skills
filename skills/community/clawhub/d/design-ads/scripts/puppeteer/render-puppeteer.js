const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function renderHTML(htmlPath, outputPath) {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();

  const html = fs.readFileSync(htmlPath, 'utf8');
  await page.setContent(html, { waitUntil: 'networkidle0' });

  await page.screenshot({
    path: outputPath,
    clip: { x: 0, y: 0, width: 1200, height: 1800 }
  });

  await browser.close();
  console.log(`✓ ${outputPath}`);
}

const htmlPath = process.argv[2];
const outputPath = process.argv[3];

if (!htmlPath || !outputPath) {
  console.error('Usage: node render-puppeteer.js <input.html> <output.png>');
  process.exit(1);
}

const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

renderHTML(htmlPath, outputPath).catch(console.error);
