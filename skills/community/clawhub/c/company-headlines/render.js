#!/usr/bin/env node
/**
 * HTML → PNG 渲染器
 * 用法: node render.js <input.html> [output.png] [width] [height]
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const htmlFile = process.argv[2];
const outputFile = process.argv[3] || htmlFile.replace(/\.html?$/, '.png');
const width = parseInt(process.argv[4]) || 800;
const height = parseInt(process.argv[5]) || 1200;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height } });
  await page.goto(`file:///${path.resolve(htmlFile).replace(/\\/g, '/')}`, {
    waitUntil: 'networkidle',
  });
  await page.screenshot({ path: outputFile, fullPage: false });
  await browser.close();

  const kb = (fs.statSync(outputFile).size / 1024).toFixed(0);
  console.log(`PNG: ${outputFile} (${kb}KB, ${width}×${height})`);
})();
