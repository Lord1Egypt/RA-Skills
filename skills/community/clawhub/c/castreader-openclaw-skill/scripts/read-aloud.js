#!/usr/bin/env node

/**
 * read-aloud.js — Open URL in browser and trigger Castreader to read aloud
 *
 * Usage: node read-aloud.js <url>
 *
 * Launches Chrome with the Castreader extension loaded, navigates to the URL,
 * and triggers the extension to read the page aloud with highlighting.
 *
 * Environment variables:
 *   CASTREADER_EXT_PATH — Path to built extension directory
 *                         (default: ../../.output/chrome-mv3)
 *   CDP_URL             — Connect to existing browser via CDP instead of launching new one
 *   CHROME_PROFILE      — Chrome user data directory for persistent sessions
 */

const path = require('path');
const fs = require('fs');
const puppeteer = require('puppeteer');

const DEFAULT_EXT_PATH = path.resolve(__dirname, '../../.output/chrome-mv3');
const EXT_PATH = process.env.CASTREADER_EXT_PATH || DEFAULT_EXT_PATH;
const CHROME_PROFILE = process.env.CHROME_PROFILE || path.resolve(__dirname, '../.chrome-profile');

/**
 * Try connecting to an existing browser via CDP.
 */
async function tryConnectCDP() {
  const cdpUrl = process.env.CDP_URL;
  if (!cdpUrl) return null;

  process.stderr.write(`Connecting to browser at ${cdpUrl}...\n`);
  try {
    const browser = await puppeteer.connect({
      browserWSEndpoint: cdpUrl.startsWith('ws') ? cdpUrl : undefined,
      browserURL: cdpUrl.startsWith('http') ? cdpUrl : undefined,
    });
    return browser;
  } catch (err) {
    process.stderr.write(`Failed to connect to CDP: ${err.message}\n`);
    return null;
  }
}

/**
 * Launch a new Chrome instance with the Castreader extension loaded.
 */
async function launchWithExtension() {
  if (!fs.existsSync(path.join(EXT_PATH, 'manifest.json'))) {
    console.error(`Error: Extension not found at ${EXT_PATH}`);
    console.error('Run: pnpm build  (in project root)');
    process.exit(1);
  }

  process.stderr.write(`Launching Chrome with extension from ${EXT_PATH}...\n`);

  const browser = await puppeteer.launch({
    headless: false,
    protocolTimeout: 120_000,
    args: [
      `--disable-extensions-except=${EXT_PATH}`,
      `--load-extension=${EXT_PATH}`,
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-popup-blocking',
      '--autoplay-policy=no-user-gesture-required',
      '--disable-blink-features=AutomationControlled',
    ],
    userDataDir: CHROME_PROFILE,
  });

  return browser;
}

/**
 * Find the Castreader extension ID by checking service worker targets.
 */
async function findExtensionId(browser) {
  for (let attempt = 0; attempt < 10; attempt++) {
    await new Promise((r) => setTimeout(r, 1000));
    const targets = browser.targets();
    const extTarget = targets.find(
      (t) => t.type() === 'service_worker' && t.url().includes('chrome-extension://'),
    );
    if (extTarget) {
      const match = extTarget.url().match(/chrome-extension:\/\/([a-z]+)\//);
      if (match) return match[1];
    }
  }

  // Fallback: check chrome://extensions page
  const page = await browser.newPage();
  await page.goto('chrome://extensions/', { waitUntil: 'domcontentloaded' });
  await new Promise((r) => setTimeout(r, 2000));

  const extId = await page.evaluate(() => {
    const manager = document.querySelector('extensions-manager');
    if (!manager?.shadowRoot) return null;
    const itemList = manager.shadowRoot.querySelector('extensions-item-list');
    if (!itemList?.shadowRoot) return null;
    const items = itemList.shadowRoot.querySelectorAll('extensions-item');
    for (const item of items) {
      const name = item.shadowRoot?.querySelector('#name')?.textContent?.trim();
      if (name && (name.toLowerCase().includes('castreader') || name.toLowerCase().includes('readout'))) {
        return item.getAttribute('id');
      }
    }
    for (const item of items) {
      const id = item.getAttribute('id');
      if (id && id.length === 32) return id;
    }
    return null;
  });

  await page.close();
  if (extId) return extId;

  throw new Error('Could not find Castreader extension ID');
}

/**
 * Trigger reading by connecting to the extension's background service worker
 * and calling chrome.tabs.sendMessage to the target tab.
 */
async function triggerReadingViaBgSW(browser, targetPage, extId) {
  // Find the background service worker target
  const targets = browser.targets();
  const swTarget = targets.find(
    (t) => t.type() === 'service_worker' && t.url().includes(`chrome-extension://${extId}/`),
  );

  if (!swTarget) {
    return { success: false, error: 'Background service worker not found' };
  }

  // Connect to the background service worker
  const swCdp = await swTarget.createCDPSession();
  try {
    await swCdp.send('Runtime.enable');

    process.stderr.write(`  Sending TOGGLE_READING to active tab...\n`);

    // In the background SW, query the active tab (doesn't need "tabs" permission)
    // and send TOGGLE_READING. We make sure the target page is focused first.
    const { result, exceptionDetails } = await swCdp.send('Runtime.evaluate', {
      expression: `
        (async () => {
          // Get the currently active tab — doesn't require "tabs" permission
          const [activeTab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
          if (!activeTab || !activeTab.id) {
            const allTabs = await chrome.tabs.query({});
            return JSON.stringify({ success: false, error: 'No active tab found', tabCount: allTabs.length });
          }
          try {
            const response = await chrome.tabs.sendMessage(activeTab.id, { type: 'TOGGLE_READING' });
            return JSON.stringify({ success: true, tabId: activeTab.id, response });
          } catch (e) {
            // Content script not loaded — try injecting it
            try {
              await chrome.scripting.executeScript({
                target: { tabId: activeTab.id },
                files: ['content-scripts/content.js'],
              });
              await new Promise(r => setTimeout(r, 500));
              const response = await chrome.tabs.sendMessage(activeTab.id, { type: 'TOGGLE_READING' });
              return JSON.stringify({ success: true, tabId: activeTab.id, response, injected: true });
            } catch (e2) {
              return JSON.stringify({ success: false, tabId: activeTab.id, error: e2.message });
            }
          }
        })()
      `,
      awaitPromise: true,
      returnByValue: true,
    });

    if (exceptionDetails) {
      return { success: false, error: exceptionDetails.text || JSON.stringify(exceptionDetails) };
    }

    try {
      return JSON.parse(result.value);
    } catch {
      return { success: true, raw: result.value };
    }
  } finally {
    await swCdp.detach();
  }
}

async function main() {
  const url = process.argv[2];
  if (!url) {
    console.error('Usage: node read-aloud.js <url>');
    process.exit(1);
  }

  // Try CDP first, otherwise launch with extension
  let browser = await tryConnectCDP();
  const isConnected = !!browser;

  if (!browser) {
    browser = await launchWithExtension();
  }

  try {
    // Find extension ID
    process.stderr.write('Finding Castreader extension...\n');
    const extId = await findExtensionId(browser);
    process.stderr.write(`Extension ID: ${extId}\n`);

    // Open the target URL in a new tab
    process.stderr.write(`Navigating to ${url}...\n`);
    const targetPage = await browser.newPage();
    await targetPage.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });

    // Wait for content script to load
    process.stderr.write('Waiting for content script to load...\n');
    await new Promise((r) => setTimeout(r, 3000));

    // Bring target page to front so it's the active tab
    await targetPage.bringToFront();
    await new Promise((r) => setTimeout(r, 500));

    // Trigger reading via background service worker CDP
    process.stderr.write('Triggering read aloud via background SW...\n');
    const triggerResult = await triggerReadingViaBgSW(browser, targetPage, extId);

    process.stderr.write(`Trigger result: ${JSON.stringify(triggerResult)}\n`);

    if (!triggerResult.success) {
      console.error('Failed to trigger reading:', triggerResult.error);
      if (triggerResult.contexts) {
        console.error('Available contexts:', JSON.stringify(triggerResult.contexts, null, 2));
      }
      process.exit(1);
    }

    // Monitor playback status
    process.stderr.write('Reading started. Monitoring...\n');

    for (let i = 0; i < 60; i++) {
      await new Promise((r) => setTimeout(r, 3000));

      const status = await targetPage.evaluate(() => {
        const player = document.getElementById('castreader-floating-player');
        if (!player) return 'no-player';
        return 'playing';
      }).catch(() => 'unknown');

      process.stderr.write(`  [${i * 3}s] Status: ${status}\n`);

      if (status === 'no-player' && i > 5) {
        process.stderr.write('Floating player disappeared. Reading may have finished.\n');
        break;
      }
    }

    console.log(JSON.stringify({
      success: true,
      url,
      extensionId: extId,
      message: 'Read-aloud triggered in browser',
    }));

  } finally {
    if (isConnected) {
      browser.disconnect();
    } else {
      process.stderr.write('\nBrowser will remain open. Press Ctrl+C to exit.\n');
      await new Promise(() => {});
    }
  }
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
