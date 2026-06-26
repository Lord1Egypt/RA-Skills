const fs = require('fs');
const path = require('path');

function canResolve(moduleName) {
  try {
    require.resolve(moduleName);
    return true;
  } catch {
    return false;
  }
}

function isExecutableFile(candidate) {
  try {
    const stat = fs.statSync(candidate);
    return stat.isFile();
  } catch {
    return false;
  }
}

function resolveFromPath(commandName) {
  const pathDirs = (process.env.PATH || '').split(path.delimiter).filter(Boolean);
  for (const dir of pathDirs) {
    const candidate = path.join(dir, commandName);
    if (isExecutableFile(candidate)) return candidate;
  }
  return null;
}

function resolveSystemChromiumPath() {
  const knownPaths = [
    process.env.CHROMIUM_PATH,
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/opt/homebrew/bin/chromium',
    '/usr/local/bin/chromium',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ].filter(Boolean);

  const found = knownPaths.find((candidate) => fs.existsSync(candidate));
  if (found) return found;

  return ['chromium', 'chromium-browser', 'google-chrome', 'google-chrome-stable']
    .map(resolveFromPath)
    .find(Boolean) || null;
}

function ensureRenderRuntimePresent() {
  const hasPlaywright = canResolve('playwright') || canResolve('playwright-core');
  const hasPlaywrightFull = canResolve('playwright');

  const problems = [];
  if (!hasPlaywright) problems.push('Missing dependency: playwright');

  const explicitChromiumPath = process.env.CHROMIUM_PATH;
  if (explicitChromiumPath && !fs.existsSync(explicitChromiumPath)) {
    problems.push(`CHROMIUM_PATH does not exist: ${explicitChromiumPath}`);
  }

  const systemChromiumPath = explicitChromiumPath && fs.existsSync(explicitChromiumPath)
    ? explicitChromiumPath
    : resolveSystemChromiumPath();

  if (!hasPlaywrightFull && !systemChromiumPath) {
    problems.push('Missing browser executable: install Chromium, set CHROMIUM_PATH, or run: npx playwright install chromium');
  }

  if (!problems.length) return { systemChromiumPath };

  throw new Error([
    ...problems,
    'Install the required runtime in the host environment:',
    'npm install playwright',
    'npx playwright install chromium',
  ].join('\n'));
}

function loadPlaywright() {
  const moduleOverride = process.env.PLAYWRIGHT_MODULE_PATH;
  const candidates = moduleOverride ? [moduleOverride, 'playwright', 'playwright-core'] : ['playwright', 'playwright-core'];

  for (const candidate of candidates) {
    try { return require(candidate); } catch {}
  }

  throw new Error(`Playwright module not found. Install playwright or set PLAYWRIGHT_MODULE_PATH. Checked: ${candidates.join(', ')}`);
}

async function renderPage(url, outputPath = path.resolve(process.cwd(), 'figma-pixel-runs/project/run-id/capture/captured-page.png'), width = 1600, height = 900) {
  if (!url) {
    throw new Error('Usage: node scripts/render-page.cjs <url> [capture-output-path] [width] [height]');
  }

  const { systemChromiumPath } = ensureRenderRuntimePresent();
  const { chromium } = loadPlaywright();
  const resolvedOutputPath = path.resolve(outputPath);
  fs.mkdirSync(path.dirname(resolvedOutputPath), { recursive: true });

  const launchOptions = {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
  };
  if (systemChromiumPath) {
    launchOptions.executablePath = systemChromiumPath;
  }
  const browser = await chromium.launch(launchOptions);

  try {
    const page = await browser.newPage({
      viewport: { width: Number(width), height: Number(height) },
      deviceScaleFactor: 1
    });

    const failedRequests = [];
    const badResponses = [];

    page.on('requestfailed', (request) => {
      failedRequests.push({
        url: request.url(),
        error: request.failure()?.errorText || 'unknown'
      });
    });

    page.on('response', (httpResponse) => {
      const status = httpResponse.status();
      if (status >= 400) {
        badResponses.push({ url: httpResponse.url(), status });
      }
    });

    const gotoResponse = await page.goto(url, {
      waitUntil: 'domcontentloaded',
      timeout: 60000
    });

    if (!gotoResponse) throw new Error('No response from page');
    if (gotoResponse.status() >= 400) throw new Error(`Page returned status ${gotoResponse.status()}`);

    await page.waitForLoadState('networkidle', { timeout: 60000 }).catch(() => {});

    await page.evaluate(async () => {
      /* global document */
      if (document.fonts && document.fonts.ready) {
        await document.fonts.ready;
      }

      const images = Array.from(document.images || []);
      await Promise.all(
        images.map((img) => {
          if (img.complete) return Promise.resolve();
          return new Promise((resolve) => {
            img.addEventListener('load', resolve, { once: true });
            img.addEventListener('error', resolve, { once: true });
          });
        })
      );
    });

    await page.addStyleTag({
      content: `
        *,
        *::before,
        *::after {
          animation: none !important;
          transition: none !important;
          caret-color: transparent !important;
        }
        html {
          scroll-behavior: auto !important;
        }
      `
    });

    const pageScrollHeight = await page.evaluate(() => document.documentElement.scrollHeight);

    await page.screenshot({ path: resolvedOutputPath, fullPage: true });

    const report = {
      ok: true,
      url,
      outputPath: resolvedOutputPath,
      viewport: { width: Number(width), height: Number(height) },
      pageScrollHeight,
      pageExceedsViewport: pageScrollHeight > Number(height) * 1.05,
      executablePath: launchOptions.executablePath || 'playwright-bundled',
      failedRequests,
      badResponses
    };

    fs.writeFileSync(
      path.join(path.dirname(resolvedOutputPath), 'render-report.json'),
      JSON.stringify(report, null, 2)
    );

    return report;
  } finally {
    await browser.close();
  }
}

module.exports = { renderPage };
