#!/usr/bin/env node
/**
 * Card News Screenshot Generator
 * Usage: node screenshot.js <html-file> <output-dir> [--jpeg]
 * 
 * Generates individual card screenshots from a card news HTML file.
 * Each .card element becomes a separate image.
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function main() {
  const args = process.argv.slice(2);
  const htmlFile = args.find(a => a.endsWith('.html'));
  const outputDir = args.find(a => !a.startsWith('-') && !a.endsWith('.html')) || 'output';
  const useJpeg = args.includes('--jpeg');

  if (!htmlFile) {
    console.error('Usage: node screenshot.js <html-file> [output-dir] [--jpeg]');
    process.exit(1);
  }

  fs.mkdirSync(outputDir, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1080, height: 1350 },
    deviceScaleFactor: 2
  });

  await page.goto('file://' + path.resolve(htmlFile), { waitUntil: 'networkidle' });
  const cards = await page.locator('.card').all();

  console.log(`Found ${cards.length} cards`);

  for (let i = 0; i < cards.length; i++) {
    const name = i === 0 ? 'cover' : i === cards.length - 1 ? 'cta' : `card_${i}`;
    const ext = useJpeg ? 'jpg' : 'png';
    const filePath = path.join(outputDir, `${name}.${ext}`);

    if (useJpeg) {
      // Screenshot as PNG first, then convert
      const pngPath = path.join(outputDir, `${name}.png`);
      await cards[i].screenshot({ path: pngPath });
      const { execSync } = require('child_process');
      execSync(`sips -s format jpeg -s formatOptions 90 "${pngPath}" --out "${filePath}" 2>/dev/null`);
      fs.unlinkSync(pngPath);
    } else {
      await cards[i].screenshot({ path: filePath });
    }

    console.log(`  ✅ ${filePath}`);
  }

  await browser.close();
  console.log(`\nDone! ${cards.length} images saved to ${outputDir}/`);
}

main().catch(e => { console.error(e); process.exit(1); });
