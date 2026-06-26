import process from 'node:process';
import { mkdir } from 'node:fs/promises';
import {
  CHROME_CANDIDATES,
  CdpConnection,
  getDefaultProfileDir,
  launchChrome,
  sleep,
  waitForChromeDebugPort,
} from './xhs-utils.js';

const XHS_PUBLISH_URL = 'https://creator.xiaohongshu.com/publish/publish';

async function main() {
  const profileDir = getDefaultProfileDir();
  await mkdir(profileDir, { recursive: true });

  console.log(`[probe] Launching Chrome to ${XHS_PUBLISH_URL}`);
  const launched = await launchChrome(XHS_PUBLISH_URL, profileDir, CHROME_CANDIDATES);
  const { port, chrome } = launched;

  console.log(`[probe] Chrome launched on port ${port}`);

  const wsUrl = await waitForChromeDebugPort(port, 30_000, { includeLastError: true });
  const cdp = await CdpConnection.connect(wsUrl, 30_000, { defaultTimeoutMs: 15_000 });

  const targets = await cdp.send<{ targetInfos: Array<{ targetId: string; url: string; type: string }> }>('Target.getTargets');
  let xhsPage = targets.targetInfos.find(
    (t) => t.type === 'page' && t.url.includes('creator.xiaohongshu.com')
  );

  if (!xhsPage) {
    // Wait for redirect/load
    console.log('[probe] Waiting for XHS page to load...');
    await sleep(5000);
    const targets2 = await cdp.send<{ targetInfos: Array<{ targetId: string; url: string; type: string }> }>('Target.getTargets');
    xhsPage = targets2.targetInfos.find(
      (t) => t.type === 'page' && (t.url.includes('creator.xiaohongshu.com') || t.url.includes('xiaohongshu.com'))
    );
    if (!xhsPage) {
      console.log('[probe] Available targets:');
      targets2.targetInfos.filter(t => t.type === 'page').forEach(t => console.log(`  ${t.url}`));
      cdp.close();
      chrome.unref();
      process.exit(1);
    }
  }

  console.log(`[probe] Found page: ${xhsPage.url}`);

  const { sessionId } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', {
    targetId: xhsPage.targetId,
    flatten: true,
  });

  await cdp.send('Page.enable', {}, { sessionId });
  await cdp.send('Runtime.enable', {}, { sessionId });
  await cdp.send('DOM.enable', {}, { sessionId });

  // Wait for page to fully load
  console.log('[probe] Waiting for full page load...');
  await sleep(5000);

  // Check current URL (may need login)
  const urlResult = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: 'window.location.href',
    returnByValue: true,
  }, { sessionId });
  console.log(`[probe] Current URL: ${urlResult.result.value}`);

  if (urlResult.result.value.includes('login') || urlResult.result.value.includes('passport')) {
    console.log('[probe] ⚠️ Need login! Please scan QR code in the browser window.');
    console.log('[probe] Waiting up to 60s for login...');
    const start = Date.now();
    while (Date.now() - start < 60_000) {
      await sleep(3000);
      const url = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
        expression: 'window.location.href',
        returnByValue: true,
      }, { sessionId });
      console.log(`[probe] URL: ${url.result.value}`);
      if (url.result.value.includes('/publish/publish') || url.result.value.includes('creator.xiaohongshu.com')) {
        if (!url.result.value.includes('login') && !url.result.value.includes('passport')) {
          console.log('[probe] Logged in!');
          break;
        }
      }
    }
    await sleep(3000);

    // Navigate to publish page
    await cdp.send('Page.navigate', { url: XHS_PUBLISH_URL }, { sessionId });
    await sleep(5000);
  }

  // === PROBING ===
  
  console.log('\n========== DOM PROBE ==========\n');

  // 1. Current URL
  const finalUrl = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: 'window.location.href',
    returnByValue: true,
  }, { sessionId });
  console.log(`URL: ${finalUrl.result.value}`);

  // 2. File inputs
  console.log('\n--- FILE INPUTS ---');
  const fileInputs = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      JSON.stringify(Array.from(document.querySelectorAll('input[type="file"]')).map((el, i) => ({
        i,
        accept: el.accept,
        multiple: el.multiple,
        className: el.className?.slice?.(0, 120) || '',
        parentTag: el.parentElement?.tagName,
        parentClass: el.parentElement?.className?.slice?.(0, 120) || '',
        gpTag: el.parentElement?.parentElement?.tagName,
        gpClass: el.parentElement?.parentElement?.className?.slice?.(0, 120) || '',
        display: getComputedStyle(el).display,
        offsetW: el.offsetWidth,
        offsetH: el.offsetHeight,
      })), null, 2)
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(fileInputs.result.value);

  // 3. Upload-related elements by text
  console.log('\n--- UPLOAD ELEMENTS (by text) ---');
  const uploadEls = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      JSON.stringify(Array.from(document.querySelectorAll('*')).filter(el => {
        const t = el.textContent?.trim();
        return t && (t === '上传笔片' || t === '上传图片' || t === '文字笔图' || t === '文字配图' || t.match(/^上传.{0,4}$/));
      }).map(el => ({
        tag: el.tagName,
        text: el.textContent?.trim().slice(0, 40),
        className: el.className?.toString?.()?.slice?.(0, 120) || '',
        id: el.id || '',
        parentClass: el.parentElement?.className?.toString?.()?.slice?.(0, 80) || '',
      })).slice(0, 15), null, 2)
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(uploadEls.result.value);

  // 4. Tabs
  console.log('\n--- TABS ---');
  const tabs = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      JSON.stringify(Array.from(document.querySelectorAll('*')).filter(el => {
        const t = el.textContent?.trim();
        return t && el.children.length <= 2 && (t === '上传图文' || t === '上传视频' || t === '写长文');
      }).map(el => ({
        tag: el.tagName,
        text: el.textContent?.trim(),
        className: el.className?.toString?.()?.slice?.(0, 120) || '',
        id: el.id || '',
        role: el.getAttribute('role') || '',
        dataType: el.getAttribute('data-type') || el.dataset?.type || '',
      })).slice(0, 10), null, 2)
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(tabs.result.value);

  // 5. Upload area HTML
  console.log('\n--- UPLOAD AREA HTML ---');
  const uploadHtml = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const fileInput = document.querySelector('input[type="file"]');
        if (!fileInput) return 'NO FILE INPUT FOUND';
        let parent = fileInput;
        for (let i = 0; i < 6 && parent.parentElement; i++) parent = parent.parentElement;
        return parent.outerHTML.slice(0, 3000);
      })()
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(uploadHtml.result.value);

  // 6. After-upload form elements (title, content)
  console.log('\n--- FORM ELEMENTS ---');
  const formEls = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      JSON.stringify({
        inputs: Array.from(document.querySelectorAll('input:not([type="file"]):not([type="hidden"])')).map(el => ({
          type: el.type, placeholder: el.placeholder?.slice(0, 50), className: el.className?.slice?.(0, 80), id: el.id, maxLength: el.maxLength, name: el.name,
        })).slice(0, 10),
        textareas: Array.from(document.querySelectorAll('textarea')).map(el => ({
          placeholder: el.placeholder?.slice(0, 50), className: el.className?.slice?.(0, 80), id: el.id, name: el.name,
        })).slice(0, 10),
        contenteditables: Array.from(document.querySelectorAll('[contenteditable="true"]')).map(el => ({
          tag: el.tagName, className: el.className?.slice?.(0, 80), id: el.id, role: el.getAttribute('role'),
          text: el.textContent?.trim().slice(0, 30),
        })).slice(0, 10),
        buttons: Array.from(document.querySelectorAll('button')).map(el => ({
          text: el.textContent?.trim().slice(0, 30), className: el.className?.slice?.(0, 80), id: el.id, type: el.type, disabled: el.disabled,
        })).filter(b => b.text).slice(0, 15),
      }, null, 2)
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(formEls.result.value);

  console.log('\n========== PROBE DONE ==========');
  
  cdp.close();
  chrome.unref();
  console.log('[probe] Chrome left open for inspection.');
}

await main().catch(err => {
  console.error(`Error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
