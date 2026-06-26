#!/usr/bin/env node
/**
 * screenshot.js — Capture screenshots of web pages using Puppeteer
 * 
 * Usage:
 *   node screenshot.js <url> [output.png] [--full]
 * 
 * Examples:
 *   node screenshot.js https://example.com
 *   node screenshot.js https://example.com output.png --full
 */

const puppeteer = require('puppeteer');
const path = require('path');

const url = process.argv[2];
const output = process.argv[3] || 'screenshot.png';
const isFullPage = process.argv.includes('--full');

if (!url) {
  console.error('Usage: node screenshot.js <url> [output.png] [--full]');
  console.error('  --full  Capture the entire scrollable page');
  process.exit(1);
}

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  // Set viewport
  await page.setViewport({ width: 1280, height: 800 });
  
  console.error(`Capturing: ${url}`);
  
  await page.goto(url, { 
    waitUntil: 'networkidle2',
    timeout: 30000 
  });
  
  // Wait for any animations/images
  await new Promise(r => setTimeout(r, 500));
  
  await page.screenshot({
    path: output,
    fullPage: isFullPage,
    type: 'png'
  });
  
  console.error(`Screenshot saved to: ${output}`);
  
  await browser.close();
  process.exit(0);
})().catch(err => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});