#!/usr/bin/env node

/**
 * extract.js — Extract clean article text from a web page
 *
 * Usage: node extract.js <url>
 * Output: JSON to stdout
 *
 * Uses Castreader's 3-layer extraction pipeline:
 *   1. Special extractors (15+ site-specific)
 *   2. Site rules (CSS selector rules, auto-learned)
 *   3. Visible-Text-Block (generic fallback)
 */

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const BUNDLE_PATH = path.resolve(__dirname, '../dist/extractor-bundle.js');

async function extract(url) {
  // Verify bundle exists
  if (!fs.existsSync(BUNDLE_PATH)) {
    console.error('Error: Extractor bundle not found at', BUNDLE_PATH);
    console.error('Reinstall: clawhub install castreader');
    process.exit(1);
  }

  const bundle = fs.readFileSync(BUNDLE_PATH, 'utf-8');

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  try {
    const page = await browser.newPage();

    // Set a reasonable viewport and user agent
    await page.setViewport({ width: 1280, height: 800 });
    await page.setUserAgent(
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    );

    // Navigate and wait for content
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });

    // Inject extractor bundle (defines window.__castreaderExtract)
    await page.evaluate(bundle);

    // Run extraction
    const result = await page.evaluate(async () => {
      const fn = window.__castreaderExtract;
      if (!fn) throw new Error('Extractor not loaded');
      return await fn();
    });

    return {
      success: result.success,
      title: result.title,
      paragraphs: result.paragraphs.map((p) => p.text),
      language: result.language,
      method: result.method,
      totalParagraphs: result.totalParagraphs,
      totalCharacters: result.totalCharacters,
      error: result.error || undefined,
    };
  } finally {
    await browser.close();
  }
}

// CLI entry point
const url = process.argv[2];
if (!url) {
  console.error('Usage: node extract.js <url>');
  process.exit(1);
}

extract(url)
  .then((result) => {
    console.log(JSON.stringify(result, null, 2));
  })
  .catch((err) => {
    console.error('Extraction failed:', err.message);
    process.exit(1);
  });
