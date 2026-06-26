/**
 * Book-PDF 生成脚本模板
 * 使用 Playwright 将合并后的 HTML 渲染为 A4 PDF
 *
 * 前置：先运行 node build.js 生成 HTML
 * 依赖：npm install playwright && npx playwright install chromium
 * 用法：node build-pdf.js
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const versionData = JSON.parse(fs.readFileSync(path.join(__dirname, 'version.json'), 'utf-8'));
const HTML_FILE = path.join(__dirname, 'output', `${versionData.title}-v${versionData.version}.html`);
const PDF_FILE = path.join(__dirname, 'output', `${versionData.title}-v${versionData.version}.pdf`);

(async () => {
  console.log('🚀 Starting PDF generation...');

  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto(`file://${HTML_FILE}`, {
    waitUntil: 'networkidle',
    timeout: 60000
  });

  // 等待字体和图片加载
  await page.waitForTimeout(4000);

  await page.pdf({
    path: PDF_FILE,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true
  });

  await browser.close();

  const sizeMB = (fs.statSync(PDF_FILE).size / 1024 / 1024).toFixed(2);
  console.log(`✅ PDF generated: ${PDF_FILE}`);
  console.log(`   Size: ${sizeMB} MB`);
})();
