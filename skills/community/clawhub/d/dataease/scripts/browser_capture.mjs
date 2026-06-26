#!/usr/bin/env node

import fs from 'node:fs/promises';

const MAX_DEBUG_LOGS = 20;
const RENDER_SETTLE_POLL_MS = 500;
const RENDER_SETTLE_IDLE_MS = 2000;
const MAX_CAPTURE_VIEWPORT_HEIGHT = 12000;

function printHelp() {
  console.log(`Usage: node scripts/browser_capture.mjs --url <url> --token <x-de-token> --width 1920 --height 1080 --wait-seconds 0 --result-format 0 --output /abs/path/file.jpg

Options:
  --url            DataEase preview URL
  --token          X-DE-TOKEN to inject into localStorage as user.token
  --width          Browser viewport width in pixels
  --height         Browser viewport height in pixels
  --wait-seconds   Extra wait time after canvas is visible
  --result-format  0=jpeg, 1=pdf
  --output         Absolute or relative output path
  -h, --help       Show this help message
`);
}

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];
    if (current === '-h' || current === '--help') {
      args.help = true;
      continue;
    }
    if (!current.startsWith('--')) {
      throw new Error(`Unexpected argument: ${current}`);
    }
    const key = current.slice(2);
    const value = argv[index + 1];
    if (value == null || value.startsWith('--')) {
      throw new Error(`Missing value for --${key}`);
    }
    args[key] = value;
    index += 1;
  }
  return args;
}

function parsePositiveInteger(value, name) {
  const number = Number.parseInt(value, 10);
  if (!Number.isFinite(number) || number <= 0) {
    throw new Error(`${name} must be a positive integer`);
  }
  return number;
}

function parseWaitSeconds(value) {
  const number = Number.parseInt(value ?? '0', 10);
  if (!Number.isFinite(number) || number < 0) {
    throw new Error('wait-seconds must be a non-negative integer');
  }
  return number;
}

async function waitForCanvasReady(page, selector, timeout) {
  const locator = page.locator(selector).first();
  await locator.waitFor({ state: 'visible', timeout });
  await page.waitForFunction(
    targetSelector => {
      const element = document.querySelector(targetSelector);
      if (!element) {
        return false;
      }
      const rect = element.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0;
    },
    selector,
    { timeout }
  );
  await page.waitForTimeout(500);
  return locator;
}

function buildWsCacheItem(value, now = Date.now(), expiresAt = 253402300799000) {
  return JSON.stringify({
    c: now,
    e: expiresAt,
    v: JSON.stringify(value)
  });
}

async function collectDiagnostics(page, debugLogs) {
  const state = await page.evaluate(() => {
    const app = document.querySelector('#app');
    const visible = element => {
      if (!element) {
        return false;
      }
      const style = window.getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== 'none' && style.visibility !== 'hidden' && Number(style.opacity || '1') > 0 && rect.width > 0 && rect.height > 0;
    };
    return {
      href: location.href,
      title: document.title,
      hasCanvas: !!document.querySelector('.canvas-container'),
      hasContent: !!document.querySelector('.content'),
      hasEmpty: !!document.querySelector('.empty-background, .el-empty'),
      visibleLoadingMasks: Array.from(document.querySelectorAll('.el-loading-mask,.ed-loading-mask,.v-loading-mask')).filter(visible).length,
      unfinishedReportLoads: document.querySelectorAll('.report-load:not(.report-load-finish)').length,
      bodyText: (document.body?.innerText || '').slice(0, 400),
      appHtml: (app?.innerHTML || '').slice(0, 1200)
    };
  });
  return {
    ...state,
    logs: debugLogs.slice(-MAX_DEBUG_LOGS)
  };
}

async function getRenderState(page, selector) {
  return page.evaluate(targetSelector => {
    const visible = element => {
      if (!element) {
        return false;
      }
      const style = window.getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== 'none' && style.visibility !== 'hidden' && Number(style.opacity || '1') > 0 && rect.width > 0 && rect.height > 0;
    };
    const canvas = document.querySelector(targetSelector);
    const loadingSelectors = '.el-loading-mask,.ed-loading-mask,.v-loading-mask,[class*="loading-mask"]';
    const visibleLoadingMasks = Array.from(document.querySelectorAll(loadingSelectors)).filter(visible).length;
    const unfinishedReportLoads = document.querySelectorAll('.report-load:not(.report-load-finish)').length;
    const box = canvas?.getBoundingClientRect();
    return {
      hasCanvas: !!canvas,
      visibleLoadingMasks,
      unfinishedReportLoads,
      width: Math.round(box?.width || 0),
      height: Math.round(box?.height || 0)
    };
  }, selector);
}

async function waitForRenderSettled(page, selector, timeout, debugLogs, getPendingRequests) {
  const startedAt = Date.now();
  let stableSince = 0;
  let lastSnapshot = '';

  while (Date.now() - startedAt < timeout) {
    const state = await getRenderState(page, selector);
    const pendingRequests = getPendingRequests();
    const snapshot = JSON.stringify({ ...state, pendingRequests });
    if (snapshot !== lastSnapshot) {
      debugLogs.push(`render-state ${snapshot}`);
      lastSnapshot = snapshot;
    }

    const settled =
      state.hasCanvas &&
      state.width > 0 &&
      state.height > 0 &&
      state.visibleLoadingMasks === 0 &&
      state.unfinishedReportLoads === 0 &&
      pendingRequests === 0;

    if (settled) {
      if (!stableSince) {
        stableSince = Date.now();
      }
      if (Date.now() - stableSince >= RENDER_SETTLE_IDLE_MS) {
        return state;
      }
    } else {
      stableSince = 0;
    }

    await page.waitForTimeout(RENDER_SETTLE_POLL_MS);
  }

  const state = await getRenderState(page, selector);
  throw new Error(
    `render settle timeout: ${JSON.stringify({
      ...state,
      pendingRequests: getPendingRequests()
    })}`
  );
}

async function expandScrollableCapture(page, selector, viewportWidth, viewportHeight) {
  return page.evaluate(
    ({ targetSelector, maxViewportHeight, minViewportHeight, viewportWidth }) => {
      const canvas = document.querySelector(targetSelector);
      if (!canvas) {
        return null;
      }

      const isScrollable = element => {
        if (!element) {
          return false;
        }
        const style = window.getComputedStyle(element);
        const overflowY = style.overflowY;
        return ['auto', 'scroll', 'overlay'].includes(overflowY) && element.scrollHeight - element.clientHeight > 2;
      };

      const applyStyle = (element, key, value) => {
        const styleKey = key;
        element.style[styleKey] = value;
      };

      let scrollableAncestor = null;
      let current = canvas.parentElement;
      while (current && current !== document.body) {
        if (isScrollable(current)) {
          scrollableAncestor = current;
          break;
        }
        current = current.parentElement;
      }

      const scrollingElement = document.scrollingElement || document.documentElement;
      const initialRect = canvas.getBoundingClientRect();

      if (scrollableAncestor) {
        scrollableAncestor.scrollTop = 0;
        applyStyle(scrollableAncestor, 'overflowY', 'visible');
        applyStyle(scrollableAncestor, 'height', `${scrollableAncestor.scrollHeight}px`);
        applyStyle(scrollableAncestor, 'maxHeight', 'none');
      }

      if (scrollingElement) {
        scrollingElement.scrollTop = 0;
      }
      window.scrollTo(0, 0);

      const rect = canvas.getBoundingClientRect();
      const fullHeight = Math.max(
        Math.ceil(rect.height),
        Math.ceil(canvas.scrollHeight || 0),
        Math.ceil(scrollableAncestor?.scrollHeight || 0),
        Math.ceil(document.documentElement.scrollHeight || 0)
      );

      return {
        hadScrollableAncestor: Boolean(scrollableAncestor),
        initialHeight: Math.ceil(initialRect.height),
        finalHeight: Math.ceil(rect.height),
        captureHeight: fullHeight,
        viewportHeight: Math.min(Math.max(fullHeight, minViewportHeight), maxViewportHeight),
        viewportWidth: viewportWidth
      };
    },
    {
      targetSelector: selector,
      maxViewportHeight: MAX_CAPTURE_VIEWPORT_HEIGHT,
      minViewportHeight: viewportHeight,
      viewportWidth: viewportWidth
    }
  );
}

async function toPdfBuffer(pngBytes, PDFDocument) {
  const pdfDoc = await PDFDocument.create();
  const image = await pdfDoc.embedPng(pngBytes);
  const page = pdfDoc.addPage([image.width, image.height]);
  page.drawImage(image, {
    x: 0,
    y: 0,
    width: image.width,
    height: image.height
  });
  const pdfBytes = await pdfDoc.save();
  return Buffer.from(pdfBytes);
}

async function main() {
  let browser;
  let page;
  const debugLogs = [];
  try {
    const args = parseArgs(process.argv.slice(2));
    if (args.help) {
      printHelp();
      return;
    }

    const url = args.url;
    const token = args.token;
    const output = args.output;
    if (!url || !token || !output) {
      throw new Error('url, token and output are required');
    }

    const width = parsePositiveInteger(args.width ?? '1920', 'width');
    const height = parsePositiveInteger(args.height ?? '1080', 'height');
    const waitSeconds = parseWaitSeconds(args['wait-seconds']);
    const resultFormat = Number.parseInt(args['result-format'] ?? '0', 10);
    if (![0, 1].includes(resultFormat)) {
      throw new Error('result-format must be 0 or 1');
    }

    const [{ chromium }, { PDFDocument }] = await Promise.all([
      import('playwright'),
      import('pdf-lib')
    ]);

    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      viewport: { width, height },
      deviceScaleFactor: 1,
      ignoreHTTPSErrors: true,
      extraHTTPHeaders: {
        'X-DE-TOKEN': token
      }
    });
    await context.route('**/de2api/**', async route => {
      const request = route.request();
      const headers = {
        ...request.headers(),
        'X-DE-TOKEN': token
      };
      const url = request.url();
      if (url.includes('/de2api/outerParams/getOuterParamsInfo/')) {
        try {
          const response = await route.fetch({ headers });
          if (response.status() < 500) {
            await route.fulfill({ response });
            return;
          }
          debugLogs.push(`outerParams fallback: ${response.status()} ${url}`);
        } catch (error) {
          debugLogs.push(`outerParams fallback error: ${error?.message || String(error)}`);
        }
        await route.fulfill({
          status: 200,
          contentType: 'application/json;charset=UTF-8',
          body: JSON.stringify({
            code: 0,
            msg: 'success',
            data: {
              outerParamsInfoMap: {},
              outerParamsInfoBaseMap: {}
            }
          })
        });
        return;
      }
      await route.continue({ headers });
    });
    page = await context.newPage();
    const selector = '.canvas-container';
    const timeout = 120000;
    const pendingRequests = new Set();
    const trackRequest = request => {
      const resourceType = request.resourceType();
      if (!['fetch', 'xhr'].includes(resourceType)) {
        return false;
      }
      return request.url().includes('/de2api/');
    };
    page.on('request', request => {
      if (trackRequest(request)) {
        pendingRequests.add(request);
      }
    });
    page.on('requestfinished', request => {
      pendingRequests.delete(request);
    });
    page.on('requestfailed', request => {
      pendingRequests.delete(request);
    });
    page.on('response', response => {
      if (response.status() >= 400 && response.url().includes('/de2api/')) {
        debugLogs.push(`response ${response.status()} ${response.url()}`);
      }
    });
    page.on('pageerror', error => {
      debugLogs.push(`pageerror ${error.message}`);
    });
    page.on('console', message => {
      if (message.type() === 'error') {
        debugLogs.push(`console ${message.text()}`);
      }
    });

    const now = Date.now();
    await page.addInitScript(
      ({ injectedToken, cacheToken, cacheExp, cacheTime }) => {
        localStorage.setItem('user.token', cacheToken);
        localStorage.setItem('user.exp', cacheExp);
        localStorage.setItem('user.time', cacheTime);
        localStorage.setItem('__de_raw_token__', injectedToken);
      },
      {
        injectedToken: token,
        cacheToken: buildWsCacheItem(token, now),
        cacheExp: buildWsCacheItem(now + 3600 * 1000, now),
        cacheTime: buildWsCacheItem(now, now)
      }
    );

    await page.goto(url, { waitUntil: 'domcontentloaded', timeout });
    try {
      await page.waitForLoadState('networkidle', { timeout: 10000 });
    } catch {
      // Preview pages may keep network connections alive; selector checks below are stricter.
    }

    const locator = await waitForCanvasReady(page, selector, timeout);
    const renderState = await waitForRenderSettled(
      page,
      selector,
      timeout,
      debugLogs,
      () => pendingRequests.size
    );
    const expandedCapture = await expandScrollableCapture(page, selector, width, height);
    if (expandedCapture?.captureHeight > height) {
      await page.setViewportSize({
        width,
        height: expandedCapture.viewportHeight
      });
      await page.waitForTimeout(500);
      await waitForRenderSettled(
        page,
        selector,
        timeout,
        debugLogs,
        () => pendingRequests.size
      );
    }
    if (waitSeconds > 0) {
      await page.waitForTimeout(waitSeconds * 1000);
    }
    const box = await locator.boundingBox();
    if (!box || box.width < 1 || box.height < 1) {
      throw new Error('canvas container is empty');
    }

    if (resultFormat === 1) {
      const pngBytes = await locator.screenshot({
        type: 'png',
        animations: 'disabled'
      });
      const pdfBytes = await toPdfBuffer(pngBytes, PDFDocument);
      await fs.writeFile(output, pdfBytes);
        console.log(JSON.stringify({
          ok: true,
          format: 'pdf',
          width: Math.round(box.width),
          height: Math.round(box.height),
          renderState,
          expandedCapture,
          output
        }));
        return;
    }

    await locator.screenshot({
      path: output,
      type: 'jpeg',
      quality: 90,
      animations: 'disabled'
    });
    console.log(JSON.stringify({
      ok: true,
      format: 'jpeg',
      width: Math.round(box.width),
      height: Math.round(box.height),
      renderState,
      expandedCapture,
      output
    }));
  } catch (error) {
    if (error && error.code === 'ERR_MODULE_NOT_FOUND') {
      console.error('Missing runtime dependency. Please run `npm install` and `npx playwright install chromium` first.');
      process.exitCode = 1;
      return;
    }
    try {
      const diagnostics = page
        ? await collectDiagnostics(page, debugLogs)
        : null;
      if (diagnostics) {
        console.error(`${error && error.stack ? error.stack : String(error)}\nDiagnostics: ${JSON.stringify(diagnostics)}`);
      } else {
        console.error(error && error.stack ? error.stack : String(error));
      }
    } catch {
      console.error(error && error.stack ? error.stack : String(error));
    }
    process.exitCode = 1;
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

main();
