/**
 * Webpage Screenshot - Full page screenshot with lazy-load support
 * 
 * Usage:
 *   node screenshot.js <url> [output-path] [options]
 * 
 * Options (env vars):
 *   VIEWPORT_WIDTH  - Viewport width (default: 1280)
 *   VIEWPORT_HEIGHT - Viewport height (default: 800)
 *   SCROLL_DELAY    - Delay between scrolls in ms (default: 100)
 *   WAIT_AFTER      - Wait after load in ms (default: 2000)
 */

const puppeteer = require('puppeteer');
const path = require('path');

const wait = (ms) => new Promise(r => setTimeout(r, ms));

async function takeScreenshot(url, outputPath, options = {}) {
  const {
    viewportWidth = parseInt(process.env.VIEWPORT_WIDTH) || 1280,
    viewportHeight = parseInt(process.env.VIEWPORT_HEIGHT) || 800,
    scrollDelay = parseInt(process.env.SCROLL_DELAY) || 100,
    waitAfter = parseInt(process.env.WAIT_AFTER) || 2000,
  } = options;

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    await page.setViewport({ width: viewportWidth, height: viewportHeight });
    
    // Navigate and wait for network idle
    await page.goto(url, { 
      waitUntil: 'networkidle2',
      timeout: 30000 
    });

    // Wait for initial content
    await wait(waitAfter);

    // Scroll to trigger lazy-loaded content
    await page.evaluate(async (delay) => {
      await new Promise((resolve) => {
        let totalHeight = 0;
        const distance = 100;
        const timer = setInterval(() => {
          const scrollHeight = document.body.scrollHeight;
          window.scrollBy(0, distance);
          totalHeight += distance;
          if (totalHeight >= scrollHeight) {
            clearInterval(timer);
            resolve();
          }
        }, delay);
      });
    }, scrollDelay);

    // Wait for lazy content to load
    await wait(waitAfter / 2);

    // Get final page dimensions
    const dimensions = await page.evaluate(() => ({
      width: document.body.scrollWidth,
      height: document.body.scrollHeight
    }));

    // Take full page screenshot
    await page.screenshot({
      path: outputPath,
      fullPage: true
    });

    return {
      success: true,
      path: outputPath,
      width: dimensions.width,
      height: dimensions.height
    };

  } finally {
    await browser.close();
  }
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.error('Usage: node screenshot.js <url> [output-path]');
    console.error('Example: node screenshot.js https://example.com screenshot.png');
    process.exit(1);
  }

  const url = args[0];
  const outputPath = args[1] || './screenshot.png';

  // Validate URL
  try {
    new URL(url);
  } catch (e) {
    console.error('Invalid URL:', url);
    process.exit(1);
  }

  takeScreenshot(url, path.resolve(outputPath))
    .then(result => {
      console.log(JSON.stringify(result));
    })
    .catch(err => {
      console.error(JSON.stringify({ success: false, error: err.message }));
      process.exit(1);
    });
}

module.exports = { takeScreenshot };
