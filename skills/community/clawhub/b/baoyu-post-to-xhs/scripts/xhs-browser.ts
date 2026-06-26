import fs from 'node:fs';
import { readdir, mkdir } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

import {
  CHROME_CANDIDATES,
  CdpConnection,
  findExistingChromeDebugPort,
  getDefaultProfileDir,
  launchChrome,
  sleep,
  waitForChromeDebugPort,
  killChrome,
} from './xhs-utils.js';

const XHS_PUBLISH_URL = 'https://creator.xiaohongshu.com/publish/publish?from=tab_switch';

interface XhsBrowserOptions {
  title?: string;
  content?: string;
  images?: string[];
  imagesDir?: string;
  markdownFile?: string;
  topics?: string[];
  submit?: boolean;
  debug?: boolean;
  timeoutMs?: number;
  profileDir?: string;
  chromePath?: string;
}

// ── helpers ──

function parseMarkdownFile(filePath: string): { title: string; content: string } {
  const text = fs.readFileSync(filePath, 'utf-8');
  let title = '';
  const fmMatch = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (fmMatch) {
    const titleMatch = fmMatch[1]!.match(/^title:\s*(.+)$/m);
    if (titleMatch) title = titleMatch[1]!.trim().replace(/^["']|["']$/g, '');
  }
  const bodyText = fmMatch ? text.slice(fmMatch[0].length) : text;
  if (!title) {
    const h1 = bodyText.match(/^#\s+(.+)$/m);
    if (h1) title = h1[1]!.trim();
  }
  const paragraphs: string[] = [];
  for (const line of bodyText.split('\n')) {
    const t = line.trim();
    if (!t || t.startsWith('#') || t.startsWith('![') || t.startsWith('---')) continue;
    paragraphs.push(t);
    if (paragraphs.join('\n').length > 1000) break;
  }
  return { title, content: paragraphs.join('\n') };
}

function compressTitle(title: string, maxLen = 20): string {
  if (title.length <= maxLen) return title;
  for (const p of ['如何', '为什么', '什么是', '怎样', '怎么', '关于']) {
    if (title.startsWith(p) && title.length > maxLen) {
      title = title.slice(p.length);
      if (title.length <= maxLen) return title;
    }
  }
  return title.length > maxLen ? title.slice(0, maxLen) : title;
}

function compressContent(content: string, maxLen = 1000): string {
  if (content.length <= maxLen) return content;
  const result: string[] = [];
  let len = 0;
  for (const line of content.split('\n')) {
    if (len + line.length + 1 > maxLen) {
      const r = maxLen - len - 1;
      if (r > 20) result.push(line.slice(0, r - 3) + '...');
      break;
    }
    result.push(line);
    len += line.length + 1;
  }
  return result.join('\n');
}

async function loadImagesFromDir(dir: string): Promise<string[]> {
  return (await readdir(dir))
    .filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f))
    .sort()
    .map(f => path.join(dir, f));
}

// ── CDP helper: evaluate JS in page ──

type Cdp = CdpConnection;

async function evalPage(cdp: Cdp, sid: string, expr: string, userGesture = false): Promise<string> {
  const r = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: expr,
    returnByValue: true,
    ...(userGesture ? { userGesture: true } : {}),
  }, { sessionId: sid });
  return r.result.value;
}

// ── DOM diagnostic dump ──

async function dumpPageDiag(cdp: Cdp, sid: string, label: string): Promise<void> {
  const diag = await evalPage(cdp, sid, `
    (function() {
      const d = {};
      d.url = location.href;
      d.title_tag = document.title;
      // tabs
      const tabs = [];
      document.querySelectorAll('[class*="tab"], [class*="Tab"], [role="tab"]').forEach(el => {
        tabs.push({ text: el.textContent?.trim()?.slice(0,30), cls: el.className?.slice?.(0,60), tag: el.tagName });
      });
      d.tabs = tabs.slice(0, 10);
      // file inputs
      const fi = [];
      document.querySelectorAll('input[type="file"]').forEach(inp => {
        fi.push({ accept: inp.accept, multiple: inp.multiple, cls: inp.className?.slice?.(0,40), vis: inp.offsetParent !== null });
      });
      d.fileInputs = fi;
      // buttons with text
      const btns = [];
      document.querySelectorAll('button, [role="button"]').forEach(b => {
        const t = b.textContent?.trim();
        if (t && t.length < 30) btns.push({ text: t, cls: b.className?.slice?.(0,40), tag: b.tagName, dis: b.disabled });
      });
      d.buttons = btns.slice(0, 20);
      // visible inputs
      const inputs = [];
      document.querySelectorAll('input:not([type="file"]):not([type="hidden"]), textarea').forEach(inp => {
        const r = inp.getBoundingClientRect();
        if (r.width > 50 && r.height > 10) {
          inputs.push({ tag: inp.tagName, type: inp.type, ph: inp.placeholder?.slice(0,30), cls: inp.className?.slice?.(0,40), maxlen: inp.maxLength });
        }
      });
      d.inputs = inputs.slice(0, 10);
      // contenteditables
      const ces = [];
      document.querySelectorAll('[contenteditable="true"]').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.width > 50) ces.push({ tag: el.tagName, cls: el.className?.slice?.(0,50), w: Math.round(r.width), h: Math.round(r.height) });
      });
      d.contenteditables = ces.slice(0, 5);
      return JSON.stringify(d, null, 2);
    })()
  `);
  console.log(`[xhs-diag] ── ${label} ──\\n${diag}`);
}

// ── wait helpers ──

async function checkPageState(cdp: Cdp, sid: string): Promise<'editing' | 'published' | 'navigated'> {
  const state = await evalPage(cdp, sid, `
    (function() {
      const url = location.href;
      if (!url.includes('creator.xiaohongshu.com')) return 'navigated';
      if (url.includes('/publish/success') || url.includes('/publish/done')) return 'published';
      const all = document.querySelectorAll('[class*="success"], [class*="toast"], [class*="dialog"], [class*="modal"]');
      for (const el of all) {
        const t = el.textContent || '';
        if (t.includes('发布成功') || t.includes('笔记已发布') || t.includes('已发布')) return 'published';
      }
      let hasPublishBtn = false;
      document.querySelectorAll('button').forEach(b => {
        const t = b.textContent?.trim();
        if (t === '发布' || t === '发布笔记') hasPublishBtn = true;
      });
      if (!hasPublishBtn) return 'published';
      return 'editing';
    })()
  `);
  return state as 'editing' | 'published' | 'navigated';
}

async function waitForPublishResult(cdp: Cdp, sid: string, maxWaitMs: number): Promise<boolean> {
  const t0 = Date.now();
  while (Date.now() - t0 < maxWaitMs) {
    await sleep(2000);
    try {
      const state = await checkPageState(cdp, sid);
      if (state === 'published' || state === 'navigated') return true;
    } catch {
      return false;
    }
  }
  return false;
}

async function waitForUserAction(
  cdp: Cdp,
  sid: string,
  maxWaitMs: number,
): Promise<'published' | 'browser_closed' | 'timeout'> {
  const t0 = Date.now();
  while (Date.now() - t0 < maxWaitMs) {
    await sleep(3000);
    try {
      const state = await checkPageState(cdp, sid);
      if (state === 'published' || state === 'navigated') return 'published';
    } catch {
      return 'browser_closed';
    }
  }
  return 'timeout';
}

// ── main logic ──

export async function postToXhs(options: XhsBrowserOptions): Promise<void> {
  const { submit = false, debug = false, timeoutMs = 120_000, profileDir = getDefaultProfileDir(), topics = [] } = options;

  let title = options.title || '';
  let content = options.content || '';
  let images = options.images || [];

  if (options.markdownFile) {
    const p = path.isAbsolute(options.markdownFile) ? options.markdownFile : path.resolve(process.cwd(), options.markdownFile);
    if (!fs.existsSync(p)) throw new Error(`Markdown file not found: ${p}`);
    const meta = parseMarkdownFile(p);
    if (!title) title = meta.title;
    if (!content) content = meta.content;
    console.log(`[xhs-browser] Parsed markdown: title="${meta.title}", content=${meta.content.length} chars`);
  }
  if (options.imagesDir) {
    const d = path.isAbsolute(options.imagesDir) ? options.imagesDir : path.resolve(process.cwd(), options.imagesDir);
    if (!fs.existsSync(d)) throw new Error(`Images dir not found: ${d}`);
    images = await loadImagesFromDir(d);
    console.log(`[xhs-browser] Found ${images.length} images in ${d}`);
  }
  if (title.length > 20) { const o = title; title = compressTitle(title, 20); console.log(`[xhs-browser] Title compressed: "${o}" → "${title}"`); }
  if (content.length > 1000) { const o = content.length; content = compressContent(content, 1000); console.log(`[xhs-browser] Content compressed: ${o} → ${content.length} chars`); }
  if (images.length === 0) throw new Error('At least one image is required (use --image or --images)');
  for (const img of images) { if (!fs.existsSync(img)) throw new Error(`Image not found: ${img}`); }
  if (images.length > 18) { console.warn(`[xhs-browser] ${images.length} images, truncating to 18.`); images = images.slice(0, 18); }

  await mkdir(profileDir, { recursive: true });

  const existingPort = await findExistingChromeDebugPort(profileDir);
  const reusing = existingPort !== null;
  let port = existingPort ?? 0;
  let chrome: Awaited<ReturnType<typeof launchChrome>>['chrome'] | null = null;

  if (!reusing) {
    const launched = await launchChrome(XHS_PUBLISH_URL, profileDir, CHROME_CANDIDATES, options.chromePath);
    port = launched.port;
    chrome = launched.chrome;
  }
  console.log(reusing ? `[xhs-browser] Reusing Chrome on port ${port}` : `[xhs-browser] Launched Chrome (profile: ${profileDir})`);

  let cdp: CdpConnection | null = null;

  try {
    const wsUrl = await waitForChromeDebugPort(port, 30_000, { includeLastError: true });
    cdp = await CdpConnection.connect(wsUrl, 30_000, { defaultTimeoutMs: 15_000 });

    const targets = await cdp.send<{ targetInfos: Array<{ targetId: string; url: string; type: string }> }>('Target.getTargets');
    let pageTarget = targets.targetInfos.find(t => t.type === 'page' && t.url.includes('creator.xiaohongshu.com'));

    if (!pageTarget) {
      const { targetId } = await cdp.send<{ targetId: string }>('Target.createTarget', { url: XHS_PUBLISH_URL });
      pageTarget = { targetId, url: XHS_PUBLISH_URL, type: 'page' };
    }

    let { sessionId: sid } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', { targetId: pageTarget.targetId, flatten: true });
    await cdp.send('Page.enable', {}, { sessionId: sid });
    await cdp.send('Runtime.enable', {}, { sessionId: sid });
    await cdp.send('DOM.enable', {}, { sessionId: sid });

    // Navigate if not on publish page
    const curUrl = await evalPage(cdp, sid, 'location.href');
    if (!curUrl.includes('/publish/publish')) {
      console.log('[xhs-browser] Navigating to publish page...');
      await cdp.send('Page.navigate', { url: XHS_PUBLISH_URL }, { sessionId: sid });
    }

    // Wait for SPA to fully render (XHS creator platform needs 10-15s)
    console.log('[xhs-browser] Waiting for page to fully render...');
    for (let i = 0; i < 20; i++) {
      await sleep(2000);
      const ready = await evalPage(cdp, sid, `
        (function() {
          const url = location.href;
          if (url.includes('login') || url.includes('passport')) return 'login';
          const els = document.querySelectorAll('*');
          if (els.length < 50) return 'loading:' + els.length;
          const hasTab = document.body.innerHTML.includes('上传图文');
          const hasUpload = document.body.innerHTML.includes('上传');
          if (hasTab || hasUpload) return 'ready';
          return 'loading:' + els.length;
        })()
      `);
      console.log(`[xhs-browser] Page state [${i}]: ${ready}`);
      if (ready === 'ready') break;
      if (ready === 'login') break;
    }

    // ══════════════════════════════════════════
    // LOGIN CHECK
    // ══════════════════════════════════════════
    const loginUrl = await evalPage(cdp, sid, 'location.href');
    if (loginUrl.includes('login') || loginUrl.includes('passport')) {
      console.log('[xhs-browser] Not logged in. Scan QR code in the browser window...');
      const t0 = Date.now();
      while (Date.now() - t0 < timeoutMs) {
        await sleep(3000);
        const u = await evalPage(cdp, sid, 'location.href');
        if (!u.includes('login') && !u.includes('passport')) { console.log('[xhs-browser] Logged in!'); break; }
      }
      await cdp.send('Page.navigate', { url: XHS_PUBLISH_URL }, { sessionId: sid });
      // Wait for SPA render after login redirect
      for (let i = 0; i < 15; i++) {
        await sleep(2000);
        const ready = await evalPage(cdp, sid, `document.body.innerHTML.includes('上传图文') ? 'ready' : 'loading'`);
        if (ready === 'ready') break;
      }
    }

    if (debug) await dumpPageDiag(cdp, sid, 'After login / initial load');

    // ══════════════════════════════════════════
    // STEP 1: Ensure "上传图文" tab is active
    // ══════════════════════════════════════════
    console.log('[xhs-browser] Ensuring "上传图文" tab is active...');
    const tabResult = await evalPage(cdp, sid, `
      (function() {
        // Strategy 1: find by text content in any clickable-like element
        const all = document.querySelectorAll('*');
        for (const el of all) {
          if (el.children.length > 2) continue; // skip containers
          const text = el.textContent?.trim();
          if (text === '上传图文') {
            el.click();
            return 'clicked_text:' + el.tagName + '.' + (el.className?.slice?.(0, 30) || '');
          }
        }
        // Strategy 2: look in tab-like containers
        for (const el of document.querySelectorAll('[class*="tab"], [class*="Tab"], [role="tab"], [class*="menu-item"]')) {
          if (el.textContent?.trim()?.includes('上传图文')) {
            el.click();
            return 'clicked_tab:' + el.className?.slice?.(0, 30);
          }
        }
        return 'not_found';
      })()
    `, true);
    console.log(`[xhs-browser] Tab: ${tabResult}`);

    // Wait for image upload area to appear after tab switch
    console.log('[xhs-browser] Waiting for image upload area...');
    for (let i = 0; i < 10; i++) {
      await sleep(2000);
      const uploadReady = await evalPage(cdp, sid, `
        (function() {
          const hasFileInput = document.querySelectorAll('input[type="file"]').length > 0;
          const hasUploadBtn = document.body.innerHTML.includes('上传照片') || document.body.innerHTML.includes('上传图片');
          const hasUploadArea = document.querySelector('[class*="upload"]') !== null;
          return (hasFileInput || hasUploadBtn || hasUploadArea) ? 'ready' : 'waiting';
        })()
      `);
      console.log(`[xhs-browser] Upload area [${i}]: ${uploadReady}`);
      if (uploadReady === 'ready') break;
    }

    if (debug) await dumpPageDiag(cdp, sid, 'After tab click');

    // ══════════════════════════════════════════
    // STEP 2: Upload images
    // ══════════════════════════════════════════
    console.log(`[xhs-browser] Uploading ${images.length} images...`);
    const absolutePaths = images.map(p => path.isAbsolute(p) ? p : path.resolve(process.cwd(), p));

    let uploadSuccess = false;

    // --- PRIMARY: file chooser interception ---
    try {
      await cdp.send('Page.setInterceptFileChooserDialog', { enabled: true }, { sessionId: sid });

      const chooserPromise = new Promise<{ backendNodeId: number }>((resolve, reject) => {
        const timeout = setTimeout(() => reject(new Error('File chooser not opened within 20s')), 20_000);
        cdp!.on('Page.fileChooserOpened', (params: unknown) => {
          clearTimeout(timeout);
          resolve(params as { backendNodeId: number });
        });
      });

      // Click the "上传照片" button by text, which triggers the hidden file input
      const clickUploadResult = await evalPage(cdp, sid, `
        (function() {
          // Strategy 1: find button/element containing "上传照片" text
          const allEls = document.querySelectorAll('button, [role="button"], a, span, div, label');
          for (const el of allEls) {
            const t = el.textContent?.trim();
            if (t === '上传照片' || t === '上传图片') {
              el.click();
              return 'clicked_btn:' + t;
            }
          }
          // Strategy 2: find the red/primary upload button in the upload area
          const btns = document.querySelectorAll('button[class*="upload"], button[class*="Upload"], [class*="uploadBtn"], [class*="upload-btn"]');
          for (const btn of btns) {
            btn.click();
            return 'clicked_cls:' + btn.className?.slice(0, 40);
          }
          // Strategy 3: directly click hidden file input
          const inp = document.querySelector('input[type="file"]');
          if (inp) { inp.click(); return 'clicked_input'; }
          return 'upload_btn_not_found';
        })()
      `, true);
      console.log(`[xhs-browser] Upload trigger: ${clickUploadResult}`);

      if (clickUploadResult === 'upload_btn_not_found') {
        throw new Error('Upload button not found');
      }

      const chooser = await chooserPromise;
      console.log(`[xhs-browser] File chooser opened, setting ${absolutePaths.length} files...`);
      await cdp.send('DOM.setFileInputFiles', { files: absolutePaths, backendNodeId: chooser.backendNodeId }, { sessionId: sid });
      uploadSuccess = true;
      console.log('[xhs-browser] Files set via file chooser.');
      // Extra: dispatch change/input events to ensure React/Vue picks up the files
      await sleep(500);
      await evalPage(cdp, sid, `
        document.querySelectorAll('input[type="file"]').forEach(inp => {
          inp.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
          inp.dispatchEvent(new Event('input', { bubbles: true, cancelable: true }));
        });
      `);
      console.log('[xhs-browser] Dispatched change/input events on file inputs.');
    } catch (err) {
      console.log(`[xhs-browser] File chooser method failed: ${err instanceof Error ? err.message : String(err)}`);
      try { await cdp.send('Page.setInterceptFileChooserDialog', { enabled: false }, { sessionId: sid }); } catch {}
    }

    // --- FALLBACK: direct DOM.setFileInputFiles ---
    if (!uploadSuccess) {
      console.log('[xhs-browser] Trying fallback: direct DOM.setFileInputFiles...');
      const { root } = await cdp.send<{ root: { nodeId: number } }>('DOM.getDocument', {}, { sessionId: sid });

      for (const sel of ['input[type="file"][accept*="image"]', 'input[type="file"][accept*=".jpg"]', 'input[type="file"][accept*=".png"]', 'input[type="file"]']) {
        const r = await cdp.send<{ nodeId: number }>('DOM.querySelector', { nodeId: root.nodeId, selector: sel }, { sessionId: sid });
        if (r.nodeId) {
          console.log(`[xhs-browser] Found file input: ${sel}`);
          await cdp.send('DOM.setFileInputFiles', { nodeId: r.nodeId, files: absolutePaths }, { sessionId: sid });
          await evalPage(cdp, sid, `
            document.querySelectorAll('input[type="file"]').forEach(inp => {
              inp.dispatchEvent(new Event('change', { bubbles: true }));
              inp.dispatchEvent(new Event('input', { bubbles: true }));
            });
          `);
          uploadSuccess = true;
          console.log('[xhs-browser] Files set via fallback.');
          break;
        }
      }
      if (!uploadSuccess) {
        if (debug) await dumpPageDiag(cdp, sid, 'Upload failed');
        throw new Error('No file input found on page. Use --debug for diagnostics.');
      }
    }

    // ══════════════════════════════════════════
    // STEP 3: Verify upload + wait for editor form (with retry)
    // ══════════════════════════════════════════

    // Helper: check current upload / form status
    async function checkUploadStatus(): Promise<{ titleFound: number; editorFound: number; publishBtn: boolean; imgCount: number; allImgCount: number; fileInputFiles: number }> {
      const status = await evalPage(cdp!, sid, `
        (function() {
          const s = {};
          const titleEls = document.querySelectorAll('input[placeholder*="标题"], input[placeholder*="填写标题"], #title, [class*="titleInput"] input, input[maxlength="20"]');
          s.titleFound = titleEls.length;
          const editors = document.querySelectorAll('[contenteditable="true"], textarea[placeholder*="描述"], textarea[placeholder*="正文"], textarea[placeholder*="添加"], .ql-editor');
          s.editorFound = editors.length;
          let publishBtn = false;
          document.querySelectorAll('button').forEach(b => { if (b.textContent?.trim()?.includes('发布')) publishBtn = true; });
          s.publishBtn = publishBtn;
          const imgEls = document.querySelectorAll('[class*="coverImg"], [class*="image-item"], [class*="img-container"], [class*="upload-item"], [class*="imgItem"], [class*="imageItem"], [class*="photo-item"], [class*="uploaded"], [class*="preview-item"], [class*="thumb"]');
          s.imgCount = imgEls.length;
          const allImgs = document.querySelectorAll('img[src*="blob:"], img[src*="xhscdn"], img[src*="sns-img"], img[src*="data:image"]');
          s.allImgCount = allImgs.length;
          // Check if file input actually has files
          const fi = document.querySelector('input[type="file"]');
          s.fileInputFiles = fi && fi.files ? fi.files.length : 0;
          return JSON.stringify(s);
        })()
      `);
      return JSON.parse(status);
    }

    // Helper: re-dispatch events on file input to kick React/Vue
    async function redispatchFileEvents(): Promise<void> {
      await evalPage(cdp!, sid, `
        document.querySelectorAll('input[type="file"]').forEach(inp => {
          ['change', 'input'].forEach(evtName => {
            inp.dispatchEvent(new Event(evtName, { bubbles: true, cancelable: true }));
          });
          // React 16/17+ synthetic event workaround
          const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
          if (nativeInputValueSetter) {
            const ev = new Event('change', { bubbles: true });
            inp.dispatchEvent(ev);
          }
        });
      `);
    }

    const MAX_UPLOAD_RETRIES = 2;
    let formReady = false;

    for (let uploadAttempt = 0; uploadAttempt <= MAX_UPLOAD_RETRIES; uploadAttempt++) {
      if (uploadAttempt > 0) {
        console.log(`[xhs-browser] Upload retry ${uploadAttempt}/${MAX_UPLOAD_RETRIES}: images not detected, re-triggering upload...`);
        // Re-dispatch events first (cheapest fix)
        await redispatchFileEvents();
        await sleep(3000);

        // Check if redispatch worked
        const quickCheck = await checkUploadStatus();
        if (quickCheck.titleFound > 0 || quickCheck.editorFound > 0 || quickCheck.publishBtn || quickCheck.imgCount > 0 || quickCheck.allImgCount > 0) {
          console.log('[xhs-browser] Redispatch worked! Form appeared.');
          formReady = true;
          break;
        }

        // Full retry: re-click upload button and re-set files
        console.log('[xhs-browser] Redispatch insufficient, re-clicking upload and re-setting files...');
        try {
          await cdp.send('Page.setInterceptFileChooserDialog', { enabled: true }, { sessionId: sid });
          const chooserRetry = new Promise<{ backendNodeId: number }>((resolve, reject) => {
            const timeout = setTimeout(() => reject(new Error('Retry file chooser timeout')), 15_000);
            cdp!.on('Page.fileChooserOpened', (params: unknown) => { clearTimeout(timeout); resolve(params as { backendNodeId: number }); });
          });
          await evalPage(cdp, sid, `
            (function() {
              const inp = document.querySelector('input[type="file"]');
              if (inp) { inp.value = ''; inp.click(); return 'clicked'; }
              const btns = document.querySelectorAll('button, [role="button"], span, div, label');
              for (const b of btns) { if (b.textContent?.trim() === '上传照片' || b.textContent?.trim() === '上传图片') { b.click(); return 'clicked_btn'; } }
              return 'not_found';
            })()
          `, true);
          const chooser = await chooserRetry;
          await cdp.send('DOM.setFileInputFiles', { files: absolutePaths, backendNodeId: chooser.backendNodeId }, { sessionId: sid });
          console.log(`[xhs-browser] Retry: files re-set via file chooser.`);
        } catch (retryErr) {
          console.log(`[xhs-browser] Retry file chooser failed: ${retryErr instanceof Error ? retryErr.message : String(retryErr)}`);
          try { await cdp.send('Page.setInterceptFileChooserDialog', { enabled: false }, { sessionId: sid }); } catch {}
          // Try DOM fallback
          try {
            const { root } = await cdp.send<{ root: { nodeId: number } }>('DOM.getDocument', {}, { sessionId: sid });
            for (const sel of ['input[type="file"][accept*="image"]', 'input[type="file"]']) {
              const r = await cdp.send<{ nodeId: number }>('DOM.querySelector', { nodeId: root.nodeId, selector: sel }, { sessionId: sid });
              if (r.nodeId) {
                await cdp.send('DOM.setFileInputFiles', { nodeId: r.nodeId, files: absolutePaths }, { sessionId: sid });
                await redispatchFileEvents();
                console.log(`[xhs-browser] Retry: files re-set via DOM fallback.`);
                break;
              }
            }
          } catch {}
        }
        await sleep(3000);
      }

      // Poll for form readiness
      console.log('[xhs-browser] Waiting for images to process and editor to appear...');
      const pollLimit = uploadAttempt === 0 ? 30 : 15; // shorter poll on retries
      for (let i = 0; i < pollLimit; i++) {
        await sleep(2000);
        const st = await checkUploadStatus();
        console.log(`[xhs-browser] Upload status: title=${st.titleFound} editor=${st.editorFound} publish=${st.publishBtn} imgs=${st.imgCount}/${st.allImgCount} files=${st.fileInputFiles}`);

        if (st.titleFound > 0 || st.editorFound > 0 || st.publishBtn) {
          formReady = true;
          break;
        }

        // If file input has no files after 10s, the set failed silently
        if (i === 5 && st.fileInputFiles === 0 && st.imgCount === 0 && st.allImgCount === 0) {
          console.log('[xhs-browser] File input appears empty after 10s — will retry upload.');
          break;
        }

        // If images are showing but form not ready yet, keep waiting
        if (st.imgCount > 0 || st.allImgCount > 0) {
          console.log('[xhs-browser] Images detected, waiting for form to appear...');
        }
      }

      if (formReady) break;
    }

    if (!formReady) {
      if (debug) await dumpPageDiag(cdp, sid, 'Form not found after upload retries');
      console.warn('[xhs-browser] Editor form not detected after retries. Continuing with best effort...');
    }

    if (debug) await dumpPageDiag(cdp, sid, 'Before filling form');

    await sleep(2000);

    // ══════════════════════════════════════════
    // STEP 4: Fill title
    // ══════════════════════════════════════════
    if (title) {
      console.log(`[xhs-browser] Filling title: "${title}"`);
      const titleResult = await evalPage(cdp, sid, `
        (function() {
          const titleVal = ${JSON.stringify(title)};
          const selectors = [
            'input[placeholder*="标题"]',
            'input[placeholder*="填写标题"]',
            '#title',
            'input[maxlength="20"]',
            '[class*="titleInput"] input',
            '[class*="title-input"] input',
            '.c-input_inner',
          ];
          for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA')) {
              el.focus();
              const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
              if (setter) setter.call(el, titleVal);
              else el.value = titleVal;
              el.dispatchEvent(new Event('input', { bubbles: true }));
              el.dispatchEvent(new Event('change', { bubbles: true }));
              el.dispatchEvent(new Event('blur', { bubbles: true }));
              return 'filled:' + sel;
            }
          }
          // Heuristic: find a prominent input near the top (not file, not hidden, not search)
          const allInputs = document.querySelectorAll('input:not([type="file"]):not([type="hidden"]):not([type="search"]):not([type="checkbox"]):not([type="radio"])');
          for (const inp of allInputs) {
            const rect = inp.getBoundingClientRect();
            if (rect.width > 200 && rect.y < 600) {
              inp.focus();
              const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
              if (setter) setter.call(inp, titleVal);
              else inp.value = titleVal;
              inp.dispatchEvent(new Event('input', { bubbles: true }));
              inp.dispatchEvent(new Event('change', { bubbles: true }));
              return 'heuristic:' + (inp.placeholder || inp.className)?.slice(0, 40);
            }
          }
          return 'not_found';
        })()
      `);
      console.log(`[xhs-browser] Title result: ${titleResult}`);
      await sleep(500);
    }

    // ══════════════════════════════════════════
    // STEP 5: Fill content / description
    // ══════════════════════════════════════════
    if (content) {
      console.log('[xhs-browser] Filling content...');
      const contentResult = await evalPage(cdp, sid, `
        (function() {
          const selectors = [
            '.ql-editor[contenteditable="true"]',
            '[contenteditable="true"][class*="ql-editor"]',
            '[contenteditable="true"][class*="post-content"]',
            '[contenteditable="true"][class*="desc"]',
            '[contenteditable="true"][class*="editor"]',
            '#post-textarea',
            'textarea[placeholder*="描述"]',
            'textarea[placeholder*="正文"]',
            'textarea[placeholder*="内容"]',
            'textarea[placeholder*="添加正文"]',
          ];
          for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (!el) continue;
            if (el.closest('[class*="title"]')) continue;
            const rect = el.getBoundingClientRect();
            if (rect.width < 100 || rect.height < 30) continue;
            el.focus();
            if (el.tagName === 'TEXTAREA' || el.tagName === 'INPUT') {
              const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set
                || Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
              if (setter) setter.call(el, ${JSON.stringify(content)});
              else el.value = ${JSON.stringify(content)};
              el.dispatchEvent(new Event('input', { bubbles: true }));
              el.dispatchEvent(new Event('change', { bubbles: true }));
            } else {
              el.innerHTML = '';
              el.focus();
              document.execCommand('insertText', false, ${JSON.stringify(content)});
            }
            return 'filled:' + sel;
          }
          // Broader: any contenteditable not related to title
          const ces = document.querySelectorAll('[contenteditable="true"]');
          for (const el of ces) {
            if (el.closest('[class*="title"]')) continue;
            const rect = el.getBoundingClientRect();
            if (rect.width < 100 || rect.height < 30) continue;
            el.focus();
            el.innerHTML = '';
            document.execCommand('insertText', false, ${JSON.stringify(content)});
            return 'ce_broad:' + (el.className?.slice?.(0, 40) || el.tagName);
          }
          return 'not_found';
        })()
      `);
      console.log(`[xhs-browser] Content result: ${contentResult}`);

      if (contentResult === 'not_found') {
        console.log('[xhs-browser] Trying keyboard fallback for content...');
        // Click the likely content area first
        await evalPage(cdp, sid, `
          const areas = document.querySelectorAll('[contenteditable="true"], textarea');
          for (const area of areas) {
            if (!area.closest('[class*="title"]')) { area.focus(); area.click(); break; }
          }
        `);
        await sleep(300);
        // Type content line by line
        for (const line of content.split('\n')) {
          if (line) await cdp.send('Input.insertText', { text: line }, { sessionId: sid });
          await cdp.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 }, { sessionId: sid });
          await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 }, { sessionId: sid });
          await sleep(30);
        }
        console.log('[xhs-browser] Content typed via keyboard.');
      }
      await sleep(500);
    }

    // ══════════════════════════════════════════
    // STEP 6: Add topics / hashtags
    // ══════════════════════════════════════════
    if (topics.length > 0) {
      console.log(`[xhs-browser] Adding ${topics.length} topics...`);
      for (const topic of topics) {
        const topicTrigger = await evalPage(cdp, sid, `
          (function() {
            // Find topic/hashtag trigger area
            const candidates = document.querySelectorAll('[class*="topic"], [class*="hashtag"], [class*="tag"], [class*="hash"]');
            for (const el of candidates) {
              if (el.tagName === 'INPUT') { el.focus(); el.click(); return 'input:' + el.className?.slice(0, 30); }
            }
            // Find by text: #, 添加话题, 话题
            const allEls = document.querySelectorAll('span, div, a, button, [role="button"]');
            for (const el of allEls) {
              const t = el.textContent?.trim();
              if (t && (t === '#' || t === '# 添加话题' || t === '添加话题' || t.match(/^#\\s*$/))) {
                el.click();
                return 'text:' + t.slice(0, 20);
              }
            }
            return 'not_found';
          })()
        `, true);
        console.log(`[xhs-browser] Topic trigger: ${topicTrigger}`);
        await sleep(500);

        if (topicTrigger !== 'not_found') {
          await cdp.send('Input.insertText', { text: topic }, { sessionId: sid });
          await sleep(800);
          // Try selecting first suggestion
          const suggestion = await evalPage(cdp, sid, `
            (function() {
              const items = document.querySelectorAll('[class*="suggest"] [class*="item"], [class*="topic-list"] [class*="item"], [class*="search-result"] [class*="item"], [class*="option"], [class*="dropdown"] [class*="item"]');
              if (items.length > 0) { items[0].click(); return 'selected'; }
              return 'no_suggestion';
            })()
          `, true);
          if (suggestion === 'no_suggestion') {
            await cdp.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 }, { sessionId: sid });
            await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 }, { sessionId: sid });
          }
          await sleep(500);
        }
      }
      console.log('[xhs-browser] Topics done.');
    }

    if (debug) await dumpPageDiag(cdp, sid, 'After filling all fields');

    // ══════════════════════════════════════════
    // STEP 7: Submit or wait for user review
    // ══════════════════════════════════════════
    if (submit) {
      console.log('[xhs-browser] Submitting note...');
      const submitResult = await evalPage(cdp, sid, `
        (function() {
          const btns = document.querySelectorAll('button');
          for (const btn of btns) {
            const t = btn.textContent?.trim();
            if (t && (t === '发布' || t === '发布笔记') && !btn.disabled) { btn.click(); return 'clicked:' + t; }
          }
          for (const btn of btns) {
            const t = btn.textContent?.trim();
            if (t && t.includes('发布') && !t.includes('定时') && !btn.disabled) { btn.click(); return 'clicked:' + t; }
          }
          const texts = [];
          btns.forEach(b => { const t = b.textContent?.trim(); if (t && t.length < 20) texts.push(t + (b.disabled ? '(disabled)' : '')); });
          return 'not_found:[' + texts.join(', ') + ']';
        })()
      `, true);
      console.log(`[xhs-browser] Submit: ${submitResult}`);

      console.log('[xhs-browser] Waiting for publish confirmation...');
      const publishConfirmed = await waitForPublishResult(cdp, sid, 30_000);
      if (publishConfirmed) {
        console.log('[xhs-browser] ✅ Note published successfully!');
      } else {
        console.log('[xhs-browser] ⚠️ Publish button clicked but could not confirm result. Check browser.');
      }
    } else {
      console.log('[xhs-browser] ✅ Content filled. Browser stays open for your review.');
      console.log('[xhs-browser] 👀 Waiting for you to review and click "发布"...');
      console.log('[xhs-browser] (Script will auto-detect when you publish or close the browser)');

      const result = await waitForUserAction(cdp, sid, timeoutMs);

      switch (result) {
        case 'published':
          console.log('[xhs-browser] ✅ Note published successfully!');
          break;
        case 'browser_closed':
          console.log('[xhs-browser] 🔒 Browser was closed. Note was NOT published.');
          break;
        case 'timeout':
          console.log(`[xhs-browser] ⏰ Wait timeout (${Math.round(timeoutMs / 1000)}s). Browser left open — publish manually if needed.`);
          break;
      }
    }
  } finally {
    if (cdp) {
      try { cdp.close(); } catch {}
    }
  }
}

// ── CLI ──

function printUsage(): never {
  console.log(`Post image-text notes to Xiaohongshu (小红书)

Usage:
  npx -y bun xhs-browser.ts [options]

Options:
  --title <text>     Note title (max 20 chars, auto-compressed)
  --content <text>   Note description (max 1000 chars)
  --markdown <path>  Markdown file for title/content extraction
  --image <path>     Add image (repeatable, max 18)
  --images <dir>     Directory containing images (PNG/JPG/WEBP)
  --topic <text>     Add topic/hashtag (repeatable)
  --submit           Auto-publish (default: preview only)
  --debug            Dump DOM diagnostics at each step
  --profile <dir>    Chrome profile directory
  --help             Show this help

Examples:
  npx -y bun xhs-browser.ts --title "美食分享" --content "今天做了一道菜" --image ./photo.png
  npx -y bun xhs-browser.ts --markdown article.md --images ./photos/
  npx -y bun xhs-browser.ts --title "旅行" --content "..." --images ./trip/ --topic "旅行" --submit
  npx -y bun xhs-browser.ts --debug --title "测试" --image test.png
`);
  process.exit(0);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) printUsage();

  const images: string[] = [];
  const topics: string[] = [];
  let submit = false, debug = false;
  let profileDir: string | undefined, title: string | undefined, content: string | undefined;
  let markdownFile: string | undefined, imagesDir: string | undefined;

  for (let i = 0; i < args.length; i++) {
    const a = args[i]!;
    if (a === '--image' && args[i + 1]) images.push(args[++i]!);
    else if (a === '--images' && args[i + 1]) imagesDir = args[++i];
    else if (a === '--title' && args[i + 1]) title = args[++i];
    else if (a === '--content' && args[i + 1]) content = args[++i];
    else if (a === '--markdown' && args[i + 1]) markdownFile = args[++i];
    else if (a === '--topic' && args[i + 1]) topics.push(args[++i]!);
    else if (a === '--submit') submit = true;
    else if (a === '--debug') debug = true;
    else if (a === '--profile' && args[i + 1]) profileDir = args[++i];
  }

  if (!markdownFile && images.length === 0 && !imagesDir) {
    console.error('Error: at least one image required (--image or --images)');
    process.exit(1);
  }

  await postToXhs({ title, content, images: images.length > 0 ? images : undefined, imagesDir, markdownFile, topics, submit, debug, profileDir });
}

await main().catch((err) => {
  console.error(`Error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
