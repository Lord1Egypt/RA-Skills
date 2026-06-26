// domain-screenshot.js
// Optional helper: take a website screenshot for a domain.
// IMPORTANT: This script must be safe to call even when Playwright/Chromium is not installed.
// In that case it should exit 0 ("skipped"), not fail.

const path = require('path');
const fs = require('fs');

function skip(reason) {
  // Keep default behavior quiet; enable logs only when explicitly requested.
  if (process.env.DOMAININFO_SCREENSHOT_DEBUG) {
    console.error(reason);
  }
  process.exit(0);
}

function fail(reason) {
  console.error(reason);
  process.exit(1);
}

(async () => {
  const domain = process.argv[2] || 'example.com';

  // Default output path relative to script directory
  const defaultOutput = 'screenshots/domain-screenshot.png';
  const outputArg = process.argv[3];
  // Restrict output to the skill root (one level above this scripts/ folder)
  const baseDir = path.resolve(__dirname, '..');

  // Security: Validate domain - only allow alphanumeric, hyphen, dot
  const safeDomain = domain.replace(/[^a-zA-Z0-9.-]/g, '');
  if (safeDomain !== domain) {
    fail('Screenshot failed: Invalid characters in domain');
  }

  // Build output path relative to script directory
  const outputPath = outputArg
    ? (path.isAbsolute(outputArg) ? outputArg : path.resolve(baseDir, outputArg))
    : path.resolve(baseDir, defaultOutput);

  // Security: Ensure output path is within baseDir
  if (!outputPath.startsWith(baseDir)) {
    fail('Screenshot failed: Path traversal attempt detected');
  }

  // Ensure output directory exists
  const dir = path.dirname(outputPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  // Playwright is optional: skip if missing
  let chromium;
  try {
    const pw = require('playwright');
    chromium = pw && pw.chromium;
  } catch (e) {
    skip('Screenshot skipped: Playwright is not available');
  }

  if (!chromium) {
    skip('Screenshot skipped: Playwright chromium is not available');
  }

  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    await page.setViewportSize({ width: 1280, height: 1024 });

    // Try https first, then http
    const urls = ['https://' + safeDomain, 'http://' + safeDomain];
    let navigated = false;

    for (const url of urls) {
      try {
        await page.goto(url, { waitUntil: 'load', timeout: 30000 });
        navigated = true;
        break;
      } catch (_) {
        // try next
      }
    }

    if (!navigated) {
      skip('Screenshot skipped: Navigation failed');
    }

    // Wait for slow sites to render
    await page.waitForTimeout(3000);

    await page.screenshot({ path: outputPath, fullPage: false });

    // Print the output path (useful for callers)
    console.log('Screenshot saved to ' + outputPath);
  } catch (err) {
    const msg = err && err.message ? err.message : String(err);

    // If the browser runtime isn't installed, treat as a skip (optional feature).
    // Common Playwright message: "Executable doesn't exist".
    if (/executable\s+does\s+not\s+exist/i.test(msg) || /browser.*not.*found/i.test(msg)) {
      skip('Screenshot skipped: Chromium runtime not available');
    }

    // Anything else is a real failure.
    fail('Screenshot failed: ' + msg);
  } finally {
    if (browser) {
      try {
        await browser.close();
      } catch (_) {
        // ignore
      }
    }
  }
})();
