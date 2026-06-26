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
  console.log(`[probe] Profile dir: ${profileDir}`);

  const port = await findExistingChromeDebugPort(profileDir);
  if (!port) {
    console.error('[probe] No running Chrome with debug port found. Make sure Chrome is launched with the right profile.');
    process.exit(1);
  }
  console.log(`[probe] Found Chrome on port ${port}`);

  const wsUrl = await waitForChromeDebugPort(port, 10_000, { includeLastError: true });
  const cdp = await CdpConnection.connect(wsUrl, 10_000, { defaultTimeoutMs: 15_000 });

  const targets = await cdp.send<{ targetInfos: Array<{ targetId: string; url: string; type: string }> }>('Target.getTargets');
  const xhsPage = targets.targetInfos.find(
    (t) => t.type === 'page' && t.url.includes('creator.xiaohongshu.com')
  );

  if (!xhsPage) {
    console.error('[probe] No XHS creator page found. Open https://creator.xiaohongshu.com/publish/publish first.');
    cdp.close();
    process.exit(1);
  }

  console.log(`[probe] Found XHS page: ${xhsPage.url}`);

  const { sessionId } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', {
    targetId: xhsPage.targetId,
    flatten: true,
  });

  await cdp.send('Runtime.enable', {}, { sessionId });
  await cdp.send('DOM.enable', {}, { sessionId });

  // 1. Probe tabs
  console.log('\n=== TABS ===');
  const tabsResult = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const results = [];
        // Look for tab-like elements
        document.querySelectorAll('[class*="tab"], [class*="Tab"], [role="tab"], [class*="publish-type"]').forEach((el, i) => {
          results.push({
            i,
            tag: el.tagName,
            text: el.textContent?.trim().slice(0, 40),
            className: el.className?.slice?.(0, 80) || '',
            isActive: el.classList?.contains('active') || el.getAttribute('aria-selected') === 'true',
          });
        });
        return JSON.stringify(results, null, 2);
      })()
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(tabsResult.result.value);

  // 2. Probe file inputs
  console.log('\n=== FILE INPUTS ===');
  const fileInputResult = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const results = [];
        document.querySelectorAll('input[type="file"]').forEach((el, i) => {
          results.push({
            i,
            accept: el.accept,
            multiple: el.multiple,
            className: el.className?.slice?.(0, 80) || '',
            parentClass: el.parentElement?.className?.slice?.(0, 80) || '',
            grandparentClass: el.parentElement?.parentElement?.className?.slice?.(0, 80) || '',
            display: getComputedStyle(el).display,
            visibility: getComputedStyle(el).visibility,
            offsetWidth: el.offsetWidth,
          });
        });
        return JSON.stringify(results, null, 2);
      })()
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(fileInputResult.result.value);

  // 3. Probe upload buttons
  console.log('\n=== UPLOAD BUTTONS ===');
  const uploadBtnResult = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const results = [];
        document.querySelectorAll('button, [role="button"], [class*="btn"], [class*="upload"]').forEach((el, i) => {
          const text = el.textContent?.trim();
          if (text && text.length < 30 && (text.includes('上传') || text.includes('upload') || text.includes('笔片') || text.includes('图片'))) {
            results.push({
              i,
              tag: el.tagName,
              text,
              className: el.className?.slice?.(0, 120) || '',
              id: el.id || '',
            });
          }
        });
        return JSON.stringify(results, null, 2);
      })()
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(uploadBtnResult.result.value);

  // 4. Probe all interactive elements with "上传" text
  console.log('\n=== ELEMENTS WITH 上传 TEXT ===');
  const uploadTextResult = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const results = [];
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
        let node;
        while (node = walker.nextNode()) {
          const text = node.textContent?.trim();
          if (text && text.includes('上传') && text.length < 50 && node.children.length <= 3) {
            results.push({
              tag: node.tagName,
              text: text.slice(0, 50),
              className: node.className?.slice?.(0, 100) || '',
              id: node.id || '',
              childCount: node.children.length,
            });
          }
        }
        return JSON.stringify(results.slice(0, 20), null, 2);
      })()
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(uploadTextResult.result.value);

  // 5. Probe the main content area structure
  console.log('\n=== MAIN CONTENT AREA ===');
  const mainAreaResult = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const results = [];
        // Get top-level structure
        const main = document.querySelector('main, [class*="content"], [class*="publish"], #app');
        if (!main) return 'No main area found';
        
        function walk(el, depth) {
          if (depth > 4) return;
          const info = {
            tag: el.tagName,
            className: (el.className?.slice?.(0, 80) || ''),
            id: el.id || undefined,
            text: el.children.length === 0 ? el.textContent?.trim().slice(0, 40) : undefined,
            childCount: el.children.length,
          };
          if (info.className || info.id || info.text) results.push('  '.repeat(depth) + JSON.stringify(info));
          for (const child of el.children) {
            walk(child, depth + 1);
          }
        }
        
        // Only show the publish area, not the whole page
        const publishArea = document.querySelector('[class*="publish"], [class*="creator"], [class*="editor"]') || main;
        walk(publishArea, 0);
        return results.slice(0, 60).join('\\n');
      })()
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(mainAreaResult.result.value);

  // 6. Full page outerHTML snippet (upload area only)
  console.log('\n=== UPLOAD AREA HTML SNIPPET ===');
  const htmlResult = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        // Find the upload area container
        const selectors = [
          '[class*="upload-wrapper"]',
          '[class*="upload-area"]',
          '[class*="drag-over"]',
          '[class*="image-upload"]',
          '[class*="publish-upload"]',
          '[class*="upload-container"]',
        ];
        for (const sel of selectors) {
          const el = document.querySelector(sel);
          if (el) return el.outerHTML.slice(0, 2000);
        }
        
        // Fallback: find parent of file input
        const fileInput = document.querySelector('input[type="file"]');
        if (fileInput) {
          let parent = fileInput;
          for (let i = 0; i < 5 && parent.parentElement; i++) {
            parent = parent.parentElement;
          }
          return parent.outerHTML.slice(0, 2000);
        }
        return 'No upload area found';
      })()
    `,
    returnByValue: true,
  }, { sessionId });
  console.log(htmlResult.result.value);

  cdp.close();
  console.log('\n[probe] Done.');
}

await main().catch(err => {
  console.error(`Error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
