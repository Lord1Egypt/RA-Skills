import process from 'node:process';
import {
  CdpConnection,
  getDefaultProfileDir,
  findExistingChromeDebugPort,
  waitForChromeDebugPort,
  sleep,
} from './xhs-utils.js';

async function main() {
  const profileDir = getDefaultProfileDir();
  const port = await findExistingChromeDebugPort(profileDir);
  if (!port) { console.error('[probe] No Chrome found.'); process.exit(1); }

  const wsUrl = await waitForChromeDebugPort(port, 10_000, { includeLastError: true });
  const cdp = await CdpConnection.connect(wsUrl, 10_000, { defaultTimeoutMs: 15_000 });

  const targets = await cdp.send<{ targetInfos: Array<{ targetId: string; url: string; type: string }> }>('Target.getTargets');
  const xhsPage = targets.targetInfos.find(t => t.type === 'page' && t.url.includes('creator.xiaohongshu.com'));
  if (!xhsPage) { console.error('[probe] No XHS page.'); cdp.close(); process.exit(1); }

  const { sessionId } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', { targetId: xhsPage.targetId, flatten: true });
  await cdp.send('Runtime.enable', {}, { sessionId });
  await cdp.send('DOM.enable', {}, { sessionId });
  await cdp.send('Page.enable', {}, { sessionId });

  // Step 1: Click "上传图文" tab
  console.log('[probe] Clicking "上传图文" tab...');
  const clickResult = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const tabs = document.querySelectorAll('.creator-tab');
        for (const tab of tabs) {
          const title = tab.querySelector('.title');
          const text = title?.textContent?.trim();
          // Skip hidden tabs (positioned off-screen)
          const style = getComputedStyle(tab);
          if (style.position === 'absolute' && style.left === '-9999px') continue;
          if (text === '上传图文') {
            tab.click();
            return 'clicked: ' + text + ' (class=' + tab.className + ')';
          }
        }
        return 'not found';
      })()
    `,
    returnByValue: true,
    userGesture: true,
  }, { sessionId });
  console.log(clickResult.result.value);

  await sleep(3000);

  // Step 2: Probe file inputs after tab switch
  console.log('\n--- FILE INPUTS (after tab switch) ---');
  const fileInputs = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      JSON.stringify(Array.from(document.querySelectorAll('input[type="file"]')).map((el, i) => ({
        i,
        accept: el.accept,
        multiple: el.multiple,
        className: el.className?.slice?.(0, 120) || '',
        parentClass: el.parentElement?.className?.slice?.(0, 120) || '',
        gpClass: el.parentElement?.parentElement?.className?.slice?.(0, 120) || '',
        display: getComputedStyle(el).display,
        offsetW: el.offsetWidth,
      })), null, 2)
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(fileInputs.result.value);

  // Step 3: Active tab check
  console.log('\n--- ACTIVE TAB ---');
  const activeTab = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      JSON.stringify(Array.from(document.querySelectorAll('.creator-tab')).map(t => ({
        text: t.querySelector('.title')?.textContent?.trim(),
        active: t.classList.contains('active'),
        hidden: getComputedStyle(t).position === 'absolute' && getComputedStyle(t).left === '-9999px',
      })), null, 2)
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(activeTab.result.value);

  // Step 4: Upload area HTML for image tab
  console.log('\n--- IMAGE UPLOAD AREA HTML ---');
  const uploadHtml = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        // Find image file input (accept includes image formats)
        const inputs = document.querySelectorAll('input[type="file"]');
        for (const inp of inputs) {
          if (inp.accept.includes('png') || inp.accept.includes('jpg') || inp.accept.includes('image')) {
            let parent = inp;
            for (let i = 0; i < 4 && parent.parentElement; i++) parent = parent.parentElement;
            return parent.outerHTML.slice(0, 3000);
          }
        }
        // If no image input yet, look at upload-content
        const uc = document.querySelector('.upload-content');
        if (uc) return uc.outerHTML.slice(0, 3000);
        return 'No image upload area found';
      })()
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(uploadHtml.result.value);

  // Step 5: Upload elements by text after tab switch
  console.log('\n--- UPLOAD BUTTONS (after tab switch) ---');
  const btns = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      JSON.stringify(Array.from(document.querySelectorAll('button, [role="button"]')).filter(el => {
        const t = el.textContent?.trim();
        return t && t.length < 30;
      }).map(el => ({
        tag: el.tagName,
        text: el.textContent?.trim(),
        className: el.className?.toString()?.slice?.(0, 120) || '',
      })).slice(0, 15), null, 2)
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(btns.result.value);

  // Step 6: All visible text on page
  console.log('\n--- PAGE TEXT SUMMARY ---');
  const pageText = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const texts = [];
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while (node = walker.nextNode()) {
          const t = node.textContent?.trim();
          if (t && t.length > 1 && t.length < 60) {
            const parent = node.parentElement;
            if (parent && getComputedStyle(parent).display !== 'none' && getComputedStyle(parent).visibility !== 'hidden') {
              texts.push(t);
            }
          }
        }
        return [...new Set(texts)].slice(0, 40).join('\\n');
      })()
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(pageText.result.value);

  cdp.close();
  console.log('\n[probe] Done.');
}

await main().catch(err => {
  console.error(`Error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
