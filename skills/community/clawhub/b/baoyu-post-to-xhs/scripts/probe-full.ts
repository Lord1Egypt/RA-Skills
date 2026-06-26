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

  console.log(`[probe] Launching Chrome...`);
  const launched = await launchChrome(XHS_PUBLISH_URL, profileDir, CHROME_CANDIDATES);
  const { port, chrome } = launched;

  const wsUrl = await waitForChromeDebugPort(port, 30_000, { includeLastError: true });
  const cdp = await CdpConnection.connect(wsUrl, 30_000, { defaultTimeoutMs: 15_000 });

  const targets = await cdp.send<{ targetInfos: Array<{ targetId: string; url: string; type: string }> }>('Target.getTargets');
  const xhsPage = targets.targetInfos.find(t => t.type === 'page' && t.url.includes('xiaohongshu.com'));
  if (!xhsPage) { console.error('No XHS page'); cdp.close(); chrome.unref(); process.exit(1); }

  const { sessionId } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', { targetId: xhsPage.targetId, flatten: true });
  await cdp.send('Runtime.enable', {}, { sessionId });
  await cdp.send('DOM.enable', {}, { sessionId });
  await cdp.send('Page.enable', {}, { sessionId });

  await sleep(4000);
  console.log('[probe] Page loaded. Clicking "上传图文" tab...');

  // Click "上传图文" tab
  const clickResult = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const tabs = document.querySelectorAll('.creator-tab');
        for (const tab of tabs) {
          const style = getComputedStyle(tab);
          if (style.position === 'absolute' && style.left === '-9999px') continue;
          const title = tab.querySelector('.title');
          if (title?.textContent?.trim() === '上传图文') {
            tab.click();
            return 'clicked';
          }
        }
        return 'not found';
      })()
    `,
    returnByValue: true,
    userGesture: true,
  }, { sessionId });
  console.log(`Tab click: ${clickResult.result.value}`);

  await sleep(3000);

  // Verify tab switch
  console.log('\n=== ACTIVE TAB ===');
  const tabs = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      JSON.stringify(Array.from(document.querySelectorAll('.creator-tab')).filter(t => {
        const s = getComputedStyle(t);
        return !(s.position === 'absolute' && s.left === '-9999px');
      }).map(t => ({
        text: t.querySelector('.title')?.textContent?.trim() || t.textContent?.trim().slice(0, 20),
        active: t.classList.contains('active'),
      })), null, 2)
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(tabs.result.value);

  // File inputs
  console.log('\n=== FILE INPUTS ===');
  const fis = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      JSON.stringify(Array.from(document.querySelectorAll('input[type="file"]')).map((el, i) => ({
        i, accept: el.accept, multiple: el.multiple,
        className: el.className?.slice?.(0, 120),
        parentClass: el.parentElement?.className?.slice?.(0, 120),
        gpClass: el.parentElement?.parentElement?.className?.slice?.(0, 120),
        visible: el.offsetWidth > 0 || el.offsetHeight > 0 || getComputedStyle(el).display !== 'none',
      })), null, 2)
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(fis.result.value);

  // Upload area HTML
  console.log('\n=== UPLOAD AREA HTML ===');
  const html = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const uc = document.querySelector('.upload-content');
        return uc ? uc.outerHTML.slice(0, 4000) : 'no .upload-content';
      })()
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(html.result.value);

  // All buttons
  console.log('\n=== BUTTONS ===');
  const btns = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      JSON.stringify(Array.from(document.querySelectorAll('button')).map(b => ({
        text: b.textContent?.trim().slice(0, 40),
        class: b.className?.slice?.(0, 100),
        disabled: b.disabled,
      })).filter(b => b.text), null, 2)
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(btns.result.value);

  // Key visible texts
  console.log('\n=== KEY VISIBLE TEXTS ===');
  const texts = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const seen = new Set();
        const results = [];
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while (node = walker.nextNode()) {
          const t = node.textContent?.trim();
          if (!t || t.length < 2 || t.length > 80 || seen.has(t)) continue;
          const p = node.parentElement;
          if (!p) continue;
          const s = getComputedStyle(p);
          if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') continue;
          const r = p.getBoundingClientRect();
          if (r.width === 0 && r.height === 0) continue;
          seen.add(t);
          results.push(t);
        }
        return results.slice(0, 50).join('\\n');
      })()
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(texts.result.value);

  cdp.close();
  chrome.unref();
  console.log('\n[probe] Done. Chrome left open.');
}

await main().catch(err => {
  console.error(`Error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
