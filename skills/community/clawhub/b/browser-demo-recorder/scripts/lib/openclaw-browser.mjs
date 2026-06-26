import puppeteer from 'puppeteer-core';

export const DEFAULT_BROWSER_URL = process.env.OPENCLAW_CDP_URL || 'http://127.0.0.1:18800';

export async function connectOpenClawBrowser(browserURL = DEFAULT_BROWSER_URL) {
  return await puppeteer.connect({
    browserURL,
    defaultViewport: null,
  });
}

export async function createPreparedPage(browser, options = {}) {
  const {
    width = 1600,
    height = 1200,
    deviceScaleFactor = 1,
    interactionLog = null,
  } = options;

  const page = await browser.newPage();
  await page.bringToFront();
  await preparePage(page, { width, height, deviceScaleFactor, interactionLog });
  return page;
}

export async function preparePage(page, options = {}) {
  const {
    width = 1600,
    height = 1200,
    deviceScaleFactor = 1,
    interactionLog = null,
  } = options;

  await page.setViewport({ width, height, deviceScaleFactor });

  const viewportMetrics = await page.evaluate(() => ({
    innerWidth: window.innerWidth,
    innerHeight: window.innerHeight,
    outerWidth: window.outerWidth,
    outerHeight: window.outerHeight,
    devicePixelRatio: window.devicePixelRatio,
  }));

  if (interactionLog?.meta) {
    interactionLog.meta.lastPreparedPage = viewportMetrics;
  }

  const installCursorOverlay = () => {
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined,
    });

    window.__demoCursor = window.__demoCursor || null;
    const installCursor = () => {
      if (document.getElementById('__demo_cursor__')) return;
      const cursor = document.createElement('div');
      cursor.id = '__demo_cursor__';
      cursor.style.cssText = [
        'position: fixed',
        'left: 0',
        'top: 0',
        'width: 22px',
        'height: 22px',
        'border-radius: 50%',
        'background: rgba(255, 77, 79, 0.85)',
        'border: 2px solid #fff',
        'box-shadow: 0 0 0 6px rgba(255, 77, 79, 0.18)',
        'pointer-events: none',
        'z-index: 2147483647',
        'transform: translate(-50%, -50%)',
        'transition: transform 0.05s linear',
      ].join(';');
      document.documentElement.appendChild(cursor);
      window.__demoCursor = cursor;
      const move = (x, y) => {
        if (!window.__demoCursor) return;
        window.__demoCursor.style.left = `${x}px`;
        window.__demoCursor.style.top = `${y}px`;
      };
      window.addEventListener('mousemove', (event) => move(event.clientX, event.clientY), true);
      window.addEventListener('mousedown', () => {
        if (window.__demoCursor) window.__demoCursor.style.transform = 'translate(-50%, -50%) scale(0.88)';
      }, true);
      window.addEventListener('mouseup', () => {
        if (window.__demoCursor) window.__demoCursor.style.transform = 'translate(-50%, -50%) scale(1)';
      }, true);
      move(24, 24);
    };

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', installCursor, { once: true });
    } else {
      installCursor();
    }
  };

  await page.evaluateOnNewDocument(installCursorOverlay);
  await page.evaluate(installCursorOverlay).catch(() => {});
  await page.mouse.move(24, 24, { steps: 1 }).catch(() => {});
}

export async function waitForNewPage(browser, options = {}) {
  const {
    width = 1600,
    height = 1200,
    deviceScaleFactor = 1,
    interactionLog = null,
    timeoutMs = 10000,
  } = options;

  return await new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      browser.off('targetcreated', onTargetCreated);
      reject(new Error(`Timed out waiting for new page after ${timeoutMs}ms`));
    }, timeoutMs);

    const onTargetCreated = async (target) => {
      try {
        if (target.type() !== 'page') return;
        clearTimeout(timer);
        browser.off('targetcreated', onTargetCreated);
        const page = await target.page();
        await page.bringToFront();
        await preparePage(page, { width, height, deviceScaleFactor, interactionLog });
        resolve(page);
      } catch (error) {
        clearTimeout(timer);
        browser.off('targetcreated', onTargetCreated);
        reject(error);
      }
    };

    browser.on('targetcreated', onTargetCreated);
  });
}

export async function disconnectBrowser(browser) {
  if (!browser) return;
  try {
    browser.disconnect();
  } catch {}
}
