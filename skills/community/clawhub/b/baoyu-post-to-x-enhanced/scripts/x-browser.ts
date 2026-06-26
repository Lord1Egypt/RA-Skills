import fs from 'node:fs';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import {
  CHROME_CANDIDATES_FULL,
  CdpConnection,
  copyImageToClipboard,
  findExistingChromeDebugPort,
  getDefaultProfileDir,
  launchChrome,
  openPageSession,
  pasteFromClipboard,
  sleep,
  waitForXSessionPersistence,
  waitForChromeDebugPort,
} from './x-utils.js';

const X_COMPOSE_URL = 'https://x.com/compose/post';

async function waitForUserPostOrClose(
  cdp: CdpConnection,
  sessionId: string,
  maxWaitMs: number,
): Promise<'posted' | 'browser_closed' | 'timeout'> {
  const t0 = Date.now();
  while (Date.now() - t0 < maxWaitMs) {
    await sleep(3000);
    try {
      const state = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
        expression: `(function() {
          const url = location.href;
          if (!url.includes('x.com')) return 'navigated';
          // Compose dialog gone = post was sent
          const editor = document.querySelector('[data-testid="tweetTextarea_0"]');
          const composeDialog = document.querySelector('[data-testid="tweetButton"]');
          if (!editor && !composeDialog) return 'posted';
          // Toast/success indicator
          const toasts = document.querySelectorAll('[data-testid="toast"], [role="alert"]');
          for (const t of toasts) {
            const txt = t.textContent || '';
            if (txt.includes('post') || txt.includes('sent') || txt.includes('Your post')) return 'posted';
          }
          return 'editing';
        })()`,
        returnByValue: true,
      }, { sessionId });
      const val = state.result.value;
      if (val === 'posted' || val === 'navigated') return 'posted';
    } catch {
      return 'browser_closed';
    }
  }
  return 'timeout';
}

interface XBrowserOptions {
  text?: string;
  images?: string[];
  submit?: boolean;
  timeoutMs?: number;
  profileDir?: string;
  chromePath?: string;
}

export async function postToX(options: XBrowserOptions): Promise<void> {
  const { text, images = [], submit = false, timeoutMs = 120_000, profileDir = getDefaultProfileDir() } = options;

  await mkdir(profileDir, { recursive: true });

  const existingPort = await findExistingChromeDebugPort(profileDir);
  const reusing = existingPort !== null;
  let port = existingPort ?? 0;
  let chrome: Awaited<ReturnType<typeof launchChrome>>['chrome'] | null = null;
  if (!reusing) {
    const launched = await launchChrome(X_COMPOSE_URL, profileDir, CHROME_CANDIDATES_FULL, options.chromePath);
    port = launched.port;
    chrome = launched.chrome;
  }

  if (reusing) console.log(`[x-browser] Reusing existing Chrome on port ${port}`);
  else console.log(`[x-browser] Launching Chrome (profile: ${profileDir})`);

  let cdp: CdpConnection | null = null;
  let sessionId: string | null = null;
  let loggedInDuringRun = false;

  try {
    const wsUrl = await waitForChromeDebugPort(port, 30_000, { includeLastError: true });
    cdp = await CdpConnection.connect(wsUrl, 30_000, { defaultTimeoutMs: 15_000 });

    const page = await openPageSession({
      cdp,
      reusing,
      url: X_COMPOSE_URL,
      matchTarget: (target) => target.type === 'page' && target.url.includes('x.com'),
      enablePage: true,
      enableRuntime: true,
      enableNetwork: true,
    });
    const activeSessionId = page.sessionId;
    sessionId = activeSessionId;
    await cdp.send('Input.setIgnoreInputEvents', { ignore: false }, { sessionId: activeSessionId });

    // Disable beforeunload dialogs — X's SPA triggers "Leave this page?" on navigate
    await cdp.send('Page.enable', {}, { sessionId: activeSessionId }).catch(() => {});
    cdp.on('Page.javascriptDialogOpening', async () => {
      try {
        await cdp!.send('Page.handleJavaScriptDialog', { accept: true }, { sessionId: activeSessionId });
        console.log('[x-browser] Auto-dismissed beforeunload dialog');
      } catch {}
    });
    // Also strip existing beforeunload handlers from the page
    await cdp.send('Runtime.evaluate', {
      expression: `window.onbeforeunload = null; window.removeEventListener('beforeunload', window.onbeforeunload);`,
    }, { sessionId: activeSessionId }).catch(() => {});

    // ── SMART RESET when reusing Chrome ──
    // Only do about:blank reset if editor has stale content.
    // Unconditional reset destroys a working x.com session — if network
    // is unstable, we can't get it back.
    if (reusing) {
      // First check: is compose page loaded and editor present?
      const pageCheck = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
        expression: `(function() {
          if (!location.href.includes('x.com')) return 'wrong_page';
          var ed = document.querySelector('[data-testid="tweetTextarea_0"]');
          if (!ed) return 'no_editor';
          var txt = (ed.textContent || '').trim();
          return txt.length > 0 ? 'stale:' + txt.length : 'clean';
        })()`,
        returnByValue: true,
      }, { sessionId: activeSessionId });
      const pageState = pageCheck.result.value;
      console.log(`[x-browser] Reusing Chrome — editor state: ${pageState}`);

      if (pageState === 'clean') {
        // Editor is already clean and on compose page — no reset needed
        console.log('[x-browser] Editor clean, skipping reset');
      } else if (pageState.startsWith('stale:')) {
        // Has residual content — try keyboard cleanup first, about:blank only as last resort
        console.log('[x-browser] Editor has stale content, trying keyboard cleanup...');
        const mod = process.platform === 'darwin' ? 4 : 2;
        for (let i = 0; i < 3; i++) {
          await cdp.send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key: 'a', code: 'KeyA', modifiers: mod, windowsVirtualKeyCode: 65 }, { sessionId: activeSessionId });
          await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'a', code: 'KeyA' }, { sessionId: activeSessionId });
          await sleep(200);
          await cdp.send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key: 'Backspace', code: 'Backspace', windowsVirtualKeyCode: 8 }, { sessionId: activeSessionId });
          await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Backspace', code: 'Backspace' }, { sessionId: activeSessionId });
          await sleep(300);
          const chk = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
            expression: `(document.querySelector('[data-testid="tweetTextarea_0"]')?.textContent || '').trim()`,
            returnByValue: true,
          }, { sessionId: activeSessionId });
          if (!chk.result.value) { console.log('[x-browser] Keyboard cleanup succeeded'); break; }
          if (i === 2) {
            // Keyboard failed — about:blank as last resort
            console.warn('[x-browser] Keyboard cleanup failed, about:blank reset (last resort)...');
            await cdp.send('Page.navigate', { url: 'about:blank' }, { sessionId: activeSessionId, timeoutMs: 10_000 });
            await sleep(1500);
            await cdp.send('Page.navigate', { url: X_COMPOSE_URL }, { sessionId: activeSessionId, timeoutMs: 45_000 });
            await sleep(4000);
          }
        }
      } else {
        // wrong_page or no_editor — navigate to compose (try SPA route first)
        console.log('[x-browser] Not on compose page, navigating...');
        await cdp.send('Page.navigate', { url: X_COMPOSE_URL }, { sessionId: activeSessionId, timeoutMs: 45_000 });
        await sleep(4000);
      }
    }

    console.log('[x-browser] Waiting for X editor...');
    await sleep(3000);

    const waitForEditor = async (): Promise<boolean> => {
      const start = Date.now();
      while (Date.now() - start < timeoutMs) {
        const result = await cdp!.send<{ result: { value: boolean } }>('Runtime.evaluate', {
          expression: `!!document.querySelector('[data-testid="tweetTextarea_0"]')`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        if (result.result.value) return true;
        await sleep(1000);
      }
      return false;
    };

    const editorFound = await waitForEditor();
    if (!editorFound) {
      console.log('[x-browser] Editor not found. Please log in to X in the browser window.');
      console.log('[x-browser] Waiting for login...');
      const loggedIn = await waitForEditor();
      if (!loggedIn) throw new Error('Timed out waiting for X editor. Please log in first.');
      loggedInDuringRun = true;
    }

    // ── PRE-UPLOAD EDITOR CLEANUP ──
    // Verify editor is empty. If not (e.g. stale content survived page load), force a fresh navigate.
    const editorContent = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
      expression: `(document.querySelector('[data-testid="tweetTextarea_0"]')?.textContent || '').trim()`,
      returnByValue: true,
    }, { sessionId: activeSessionId });
    if (editorContent.result.value) {
      console.warn(`[x-browser] Editor has stale content (${editorContent.result.value.length} chars), about:blank reset...`);
      await cdp!.send('Page.navigate', { url: 'about:blank' }, { sessionId: activeSessionId, timeoutMs: 10_000 });
      await sleep(1500);
      await cdp!.send('Page.navigate', { url: X_COMPOSE_URL }, { sessionId: activeSessionId, timeoutMs: 45_000 });
      await sleep(4000);
      const reFresh = await waitForEditor();
      if (!reFresh) throw new Error('Editor not found after forced navigation');
      // Verify it's actually clean now
      const recheck = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
        expression: `(document.querySelector('[data-testid="tweetTextarea_0"]')?.textContent || '').trim()`,
        returnByValue: true,
      }, { sessionId: activeSessionId });
      if (recheck.result.value) {
        console.error(`[x-browser] Editor STILL has content after fresh navigate (${recheck.result.value.length} chars). Aborting.`);
        throw new Error('Cannot clear editor — stale content persists after fresh navigation');
      }
      console.log('[x-browser] Editor cleaned via two-step navigation');
    } else {
      console.log('[x-browser] Editor is clean');
    }

    // ── PHASE 1: Upload images FIRST (before typing text) ──
    // DOM.setFileInputFiles can leak file paths into the editor as text on some X/React versions.
    // By uploading images first and clearing leaked paths, we ensure clean text input later.
    const MAX_IMAGES = 4;
    const imagesToUpload = images.slice(0, MAX_IMAGES);
    console.log(`[x-browser] Uploading ${imagesToUpload.length} image(s) (max ${MAX_IMAGES})...`);
    const phase1Start = Date.now();
    for (let imgIdx = 0; imgIdx < imagesToUpload.length; imgIdx++) {
      const imagePath = imagesToUpload[imgIdx]!;
      console.log(`[x-browser] [${imgIdx + 1}/${imagesToUpload.length}] Starting image upload... (elapsed ${((Date.now() - phase1Start) / 1000).toFixed(0)}s)`);
      if (!fs.existsSync(imagePath)) {
        console.warn(`[x-browser] Image not found: ${imagePath}`);
        continue;
      }

      const absPath = path.isAbsolute(imagePath) ? imagePath : path.resolve(process.cwd(), imagePath);
      console.log(`[x-browser] Uploading image: ${absPath}`);

      const imgCountBefore = await cdp.send<{ result: { value: number } }>('Runtime.evaluate', {
        expression: `document.querySelectorAll('img[src^="blob:"]').length`,
        returnByValue: true,
      }, { sessionId: activeSessionId });
      const expectedImgCount = imgCountBefore.result.value + 1;
      let imgUploadOk = false;

      // Strategy 1 (preferred): DOM.setFileInputFiles — no clipboard, no anti-automation risk
      console.log('[x-browser] Trying DOM.setFileInputFiles (preferred)...');
      try {
        const fileInputResult = await cdp!.send<{ result: { objectId?: string; subtype?: string } }>('Runtime.evaluate', {
          expression: `document.querySelector('input[type="file"][data-testid="fileInput"], input[type="file"][accept*="image"], input[type="file"]')`,
          returnByValue: false,
        }, { sessionId: activeSessionId });

        if (fileInputResult.result.objectId) {
          await cdp!.send('DOM.setFileInputFiles', {
            files: [absPath],
            objectId: fileInputResult.result.objectId,
          }, { sessionId: activeSessionId });
          console.log('[x-browser] Files set via DOM.setFileInputFiles');

          const domWaitStart = Date.now();
          while (Date.now() - domWaitStart < 12_000) {
            const r = await cdp!.send<{ result: { value: number } }>('Runtime.evaluate', {
              expression: `document.querySelectorAll('img[src^="blob:"]').length`,
              returnByValue: true,
            }, { sessionId: activeSessionId });
            if (r.result.value >= expectedImgCount) {
              imgUploadOk = true;
              console.log('[x-browser] Image upload verified (DOM.setFileInputFiles)');
              break;
            }
            await sleep(1000);
          }
        } else {
          console.warn('[x-browser] No file input element found');
        }
      } catch (domErr) {
        console.warn(`[x-browser] DOM.setFileInputFiles failed: ${domErr instanceof Error ? domErr.message : String(domErr)}`);
      }

      // Strategy 2 (fallback): Clipboard paste
      if (!imgUploadOk) {
        console.log('[x-browser] Falling back to clipboard paste...');
        if (copyImageToClipboard(absPath)) {
          await sleep(500);
          await cdp!.send('Runtime.evaluate', {
            expression: `document.querySelector('[data-testid="tweetTextarea_0"]')?.focus()`,
          }, { sessionId: activeSessionId });
          await sleep(200);

          const pasteSuccess = pasteFromClipboard('Google Chrome', 5, 500);
          if (!pasteSuccess) {
            const modifiers = process.platform === 'darwin' ? 4 : 2;
            await cdp!.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'v', code: 'KeyV', modifiers, windowsVirtualKeyCode: 86 }, { sessionId: activeSessionId });
            await cdp!.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'v', code: 'KeyV', modifiers, windowsVirtualKeyCode: 86 }, { sessionId: activeSessionId });
          }

          const pasteWaitStart = Date.now();
          while (Date.now() - pasteWaitStart < 15_000) {
            const r = await cdp!.send<{ result: { value: number } }>('Runtime.evaluate', {
              expression: `document.querySelectorAll('img[src^="blob:"]').length`,
              returnByValue: true,
            }, { sessionId: activeSessionId });
            if (r.result.value >= expectedImgCount) {
              imgUploadOk = true;
              console.log('[x-browser] Image upload verified (clipboard paste)');
              break;
            }
            await sleep(1000);
          }
        } else {
          console.warn(`[x-browser] Failed to copy image to clipboard: ${absPath}`);
        }
      }

      if (!imgUploadOk) {
        console.warn('[x-browser] ⚠️ Image upload not detected after all strategies');
        continue;
      }

      // ── UNCONDITIONAL editor cleanup after image upload ──
      // DOM.setFileInputFiles on X's React app leaks file paths into the editor.
      // Always clear the editor after each image upload — do NOT rely on pattern detection.
      console.log('[x-browser] Force-clearing editor after image upload...');
      for (let clearAttempt = 0; clearAttempt < 3; clearAttempt++) {
        await cdp!.send('Runtime.evaluate', {
          expression: `(function() {
            var el = document.querySelector('[data-testid="tweetTextarea_0"]');
            if (!el) return;
            el.focus();
            document.execCommand('selectAll');
            document.execCommand('delete');
          })()`,
        }, { sessionId: activeSessionId });
        await sleep(300);
        const checkEmpty = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
          expression: `(document.querySelector('[data-testid="tweetTextarea_0"]')?.textContent || '').trim()`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        if (!checkEmpty.result.value) {
          console.log('[x-browser] Editor cleared successfully');
          break;
        }
        if (clearAttempt === 2) {
          console.warn(`[x-browser] ⚠️ Editor not empty after 3 clear attempts: "${checkEmpty.result.value.substring(0, 60)}..."`);
        }
      }

      // ── Wait for X to finish processing the image ──
      console.log('[x-browser] Waiting for X to process image...');
      const processingStart = Date.now();
      let imageReady = false;
      while (Date.now() - processingStart < 30_000) {
        const status = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
          expression: `(function() {
            var btn = document.querySelector('[data-testid="tweetButton"]');
            if (!btn) return 'no_btn';
            if (btn.getAttribute('aria-disabled') === 'true' || btn.disabled) return 'disabled';
            var progress = document.querySelector('[role="progressbar"]');
            if (progress) return 'processing';
            return 'ready';
          })()`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        if (status.result.value === 'ready') {
          imageReady = true;
          console.log('[x-browser] Image processing complete, Post button ready');
          break;
        }
        if (status.result.value === 'no_btn') {
          console.warn('[x-browser] Post button not found');
          break;
        }
        await sleep(1000);
      }
      if (!imageReady) {
        console.warn('[x-browser] ⚠️ Image processing did not complete within 30s');
      }
    }
    console.log(`[x-browser] Phase 1 complete: ${imagesToUpload.length} image(s) processed in ${((Date.now() - phase1Start) / 1000).toFixed(1)}s`);

    // ── PHASE 2: Type text AFTER all images are uploaded and editor is clean ──
    // Hard-limit hashtags to MAX_HASHTAGS to prevent X rejection
    const MAX_HASHTAGS = 3;
    let finalText = text;
    if (finalText) {
      // Unicode-aware hashtag regex — matches CJK, Hangul, Kana, Latin, etc.
      const hashtagRe = /#[\p{L}\p{N}_]+/gu;
      const allHashtags = finalText.match(hashtagRe) || [];
      if (allHashtags.length > MAX_HASHTAGS) {
        console.warn(`[x-browser] Hashtag count ${allHashtags.length} exceeds limit ${MAX_HASHTAGS}, truncating...`);
        const keep = new Set(allHashtags.slice(0, MAX_HASHTAGS));
        let kept = 0;
        finalText = finalText.replace(hashtagRe, (tag) => {
          if (keep.has(tag) && kept < MAX_HASHTAGS) { kept++; return tag; }
          return '';
        }).replace(/  +/g, ' ').replace(/\n /g, '\n').trim();
        console.log(`[x-browser] Truncated to ${MAX_HASHTAGS} hashtags: ${[...keep].join(' ')}`);
      }
    }
    if (finalText) {
      // UNCONDITIONAL cleanup before typing — always ensure editor is empty
      console.log('[x-browser] Final editor cleanup before typing...');
      let editorClean = false;
      // Try keyboard-based cleanup first (Cmd+A + Backspace via CDP)
      for (let clearAttempt = 0; clearAttempt < 3; clearAttempt++) {
        await cdp!.send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key: 'a', code: 'KeyA', windowsVirtualKeyCode: 65, modifiers: process.platform === 'darwin' ? 4 : 2 }, { sessionId: activeSessionId });
        await cdp!.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'a', code: 'KeyA', windowsVirtualKeyCode: 65 }, { sessionId: activeSessionId });
        await sleep(200);
        await cdp!.send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key: 'Backspace', code: 'Backspace', windowsVirtualKeyCode: 8 }, { sessionId: activeSessionId });
        await cdp!.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Backspace', code: 'Backspace', windowsVirtualKeyCode: 8 }, { sessionId: activeSessionId });
        await sleep(300);
        const checkEmpty = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
          expression: `(document.querySelector('[data-testid="tweetTextarea_0"]')?.textContent || '').trim()`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        if (!checkEmpty.result.value) { editorClean = true; break; }
        console.warn(`[x-browser] Cleanup attempt ${clearAttempt + 1}/3: still ${checkEmpty.result.value.length} chars`);
      }
      // Nuclear option: two-step navigate to fresh page + re-upload images
      if (!editorClean && images.length > 0) {
        console.warn('[x-browser] Keyboard cleanup failed, about:blank reset...');
        await cdp!.send('Page.navigate', { url: 'about:blank' }, { sessionId: activeSessionId, timeoutMs: 10_000 });
        await sleep(1500);
        await cdp!.send('Page.navigate', { url: X_COMPOSE_URL }, { sessionId: activeSessionId, timeoutMs: 45_000 });
        await sleep(4000);
        const freshEditor = await waitForEditor();
        if (!freshEditor) throw new Error('Editor not found after nuclear cleanup');
        // Re-upload images on the fresh page
        console.log(`[x-browser] Re-uploading ${imagesToUpload.length} images after cleanup reset...`);
        for (const imgPath of imagesToUpload) {
          const inputResult = await cdp!.send<{ result: { value: string | null } }>('Runtime.evaluate', {
            expression: `(function() { var el = document.querySelector('input[type="file"][accept*="image"]'); return el ? 'found' : null; })()`,
            returnByValue: true,
          }, { sessionId: activeSessionId });
          if (inputResult.result.value) {
            const objRes = await cdp!.send<{ result: { objectId?: string } }>('Runtime.evaluate', {
              expression: `document.querySelector('input[type="file"][accept*="image"]')`,
              returnByValue: false,
            }, { sessionId: activeSessionId });
            if (objRes.result.objectId) {
              await cdp!.send('DOM.setFileInputFiles', { files: [imgPath], objectId: objRes.result.objectId }, { sessionId: activeSessionId });
              await sleep(3000);
            }
          }
        }
        console.log('[x-browser] Images re-uploaded after cleanup reset');
      }

      // Helper: check if Post button is enabled (Draft.js accepted the text)
      const isPostButtonEnabled = async (): Promise<boolean> => {
        const r = await cdp!.send<{ result: { value: boolean } }>('Runtime.evaluate', {
          expression: `(() => {
            const btn = document.querySelector('[data-testid="tweetButton"]');
            return btn ? btn.getAttribute('aria-disabled') !== 'true' && !btn.disabled : false;
          })()`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        return r.result.value;
      };

      // Helper: click editor with real mouse event to establish trusted focus
      const clickEditorWithMouse = async (): Promise<void> => {
        const pos = await cdp!.send<{ result: { value: { x: number; y: number } | null } }>('Runtime.evaluate', {
          expression: `(() => {
            const el = document.querySelector('[data-testid="tweetTextarea_0"]');
            if (!el) return null;
            const r = el.getBoundingClientRect();
            return { x: r.x + r.width / 2, y: r.y + r.height / 3 };
          })()`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        if (pos.result.value) {
          const { x, y } = pos.result.value;
          await cdp!.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }, { sessionId: activeSessionId });
          await sleep(50);
          await cdp!.send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 }, { sessionId: activeSessionId });
          await sleep(40);
          await cdp!.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 }, { sessionId: activeSessionId });
          await sleep(300);
        }
      };

      // Helper: clear editor with keyboard events
      const clearEditorKeyboard = async (): Promise<void> => {
        const mod = process.platform === 'darwin' ? 4 : 2;
        await cdp!.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'a', code: 'KeyA', modifiers: mod, windowsVirtualKeyCode: 65 }, { sessionId: activeSessionId });
        await cdp!.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'a', code: 'KeyA', modifiers: mod, windowsVirtualKeyCode: 65 }, { sessionId: activeSessionId });
        await sleep(200);
        await cdp!.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Backspace', code: 'Backspace', windowsVirtualKeyCode: 8 }, { sessionId: activeSessionId });
        await cdp!.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Backspace', code: 'Backspace', windowsVirtualKeyCode: 8 }, { sessionId: activeSessionId });
        await sleep(300);
      };

      // Helper: verify text in editor
      const verifyEditorText = async (): Promise<{ ok: boolean; typed: string }> => {
        // Use innerText (preserves line breaks) instead of textContent (may lose structure)
        const typedText = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
          expression: `(function() {
            const el = document.querySelector('[data-testid="tweetTextarea_0"]');
            if (!el) return '';
            // Collect text from all child divs to preserve paragraph structure
            const divs = el.querySelectorAll(':scope > div');
            if (divs.length > 0) return Array.from(divs).map(d => d.textContent || '').join('\\n');
            return el.innerText || el.textContent || '';
          })()`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        const typed = typedText.result.value;
        const hasFilePaths = typed.includes('.png') || typed.includes('.jpg') || typed.includes('.jpeg') || typed.includes('/media/') || typed.includes('\\media\\') || typed.includes('blob:');
        const hashtags = typed.match(/#[\p{L}\p{N}_]+/gu) || [];
        const uniqueHashtags = new Set(hashtags);
        const hasDuplicateHashtags = hashtags.length > uniqueHashtags.size;
        const tooManyHashtags = uniqueHashtags.size > MAX_HASHTAGS;
        // Compare without newlines — Draft.js may add/remove whitespace
        const typedNorm = typed.replace(/\s+/g, ' ').trim();
        const expectedNorm = finalText.replace(/\s+/g, ' ').trim();
        const charRatio = expectedNorm.length > 0 ? typedNorm.length / expectedNorm.length : 1;
        const charCountOk = charRatio >= 0.7 && charRatio <= 1.3;
        console.log(`[x-browser] Verify: ${typedNorm.length} chars in editor, expected ~${expectedNorm.length}, ratio=${charRatio.toFixed(2)}, ok=${charCountOk}`);
        return { ok: !hasFilePaths && !hasDuplicateHashtags && !tooManyHashtags && charCountOk, typed };
      };

      let textInserted = false;

      // ── Strategy 1: Mouse-click focus + CDP Input.insertText (line-by-line) ──
      console.log('[x-browser] Strategy 1: Mouse-click focus + Input.insertText...');

      // Wait for image processing overlay to clear before clicking editor
      // X shows a processing spinner that steals focus from the editor
      if (imagesToUpload.length > 0) {
        console.log('[x-browser] Waiting for image processing to settle before typing...');
        await sleep(2000);
        const imgStable = await cdp!.send<{ result: { value: boolean } }>('Runtime.evaluate', {
          expression: `!document.querySelector('[data-testid="attachments"] [role="progressbar"]')`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        if (!imgStable.result.value) {
          console.warn('[x-browser] Image still processing, waiting extra 5s...');
          await sleep(5000);
        }
      }

      // Click editor and verify focus is actually inside it (retry up to 3 times)
      let editorFocused = false;
      for (let focusTry = 0; focusTry < 3; focusTry++) {
        await clickEditorWithMouse();
        await sleep(300);
        const focusCheck = await cdp!.send<{ result: { value: boolean } }>('Runtime.evaluate', {
          expression: `(() => {
            const el = document.querySelector('[data-testid="tweetTextarea_0"]');
            if (!el) return false;
            return el.contains(document.activeElement) || el === document.activeElement;
          })()`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        if (focusCheck.result.value) { editorFocused = true; break; }
        console.warn(`[x-browser] Focus attempt ${focusTry + 1}/3: editor not focused, retrying...`);
        // Try clicking deeper into the contenteditable
        await cdp!.send('Runtime.evaluate', {
          expression: `document.querySelector('[data-testid="tweetTextarea_0"] [contenteditable="true"]')?.focus()`,
        }, { sessionId: activeSessionId });
        await sleep(200);
      }
      if (!editorFocused) {
        console.warn('[x-browser] Could not focus editor after 3 attempts, proceeding anyway...');
      }

      // Split by newlines and insert each line separately with Enter key events
      const lines = finalText.split('\n');
      for (let li = 0; li < lines.length; li++) {
        const line = lines[li]!;
        if (line.length > 0) {
          await cdp!.send('Input.insertText', { text: line }, { sessionId: activeSessionId });
          await sleep(50);
        }
        if (li < lines.length - 1) {
          await cdp!.send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 }, { sessionId: activeSessionId });
          await cdp!.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 }, { sessionId: activeSessionId });
          await sleep(50);
        }
      }
      console.log(`[x-browser] Inserted ${lines.length} lines via line-by-line Input.insertText`);
      await sleep(1000);

      const s1verify = await verifyEditorText();
      const s1btnOk = await isPostButtonEnabled();
      if (s1verify.ok && s1btnOk) {
        console.log(`[x-browser] Strategy 1 SUCCESS: text verified (${s1verify.typed.length} chars), Post button enabled`);
        textInserted = true;
      } else if (s1verify.ok && !s1btnOk) {
        console.warn(`[x-browser] Strategy 1 PARTIAL: text in DOM (${s1verify.typed.length} chars) but Post button disabled — Draft.js did not accept`);
      } else {
        console.warn(`[x-browser] Strategy 1 FAILED: text verification failed (got ${s1verify.typed.length} chars)`);
      }

      // ── Strategy 1b: If insertText yielded 0 chars, try execCommand('insertText') ──
      if (!textInserted && s1verify.typed.length === 0) {
        console.log('[x-browser] Strategy 1b: execCommand insertText fallback...');
        await clickEditorWithMouse();
        await sleep(200);
        // Insert line-by-line using execCommand, with insertParagraph for newlines
        const s1bLines = finalText.split('\n');
        for (let li = 0; li < s1bLines.length; li++) {
          const line = s1bLines[li]!;
          if (line.length > 0) {
            await cdp!.send('Runtime.evaluate', {
              expression: `document.execCommand('insertText', false, ${JSON.stringify(line)})`,
            }, { sessionId: activeSessionId });
            await sleep(80);
          }
          if (li < s1bLines.length - 1) {
            // insertParagraph creates a proper block-level break in Draft.js
            await cdp!.send('Runtime.evaluate', {
              expression: `document.execCommand('insertParagraph', false, null)`,
            }, { sessionId: activeSessionId });
            await sleep(80);
          }
        }
        console.log(`[x-browser] Strategy 1b: inserted ${s1bLines.length} lines via execCommand`);
        await sleep(1000);
        const s1bverify = await verifyEditorText();
        const s1bbtnOk = await isPostButtonEnabled();
        if (s1bverify.ok && s1bbtnOk) {
          console.log(`[x-browser] Strategy 1b SUCCESS: ${s1bverify.typed.length} chars, Post enabled`);
          textInserted = true;
        } else if (s1bverify.typed.length > 0 && s1bbtnOk) {
          // Partial text but Post is enabled — accept if ratio > 0.8
          const partialRatio = s1bverify.typed.length / finalText.replace(/\s+/g, ' ').trim().length;
          if (partialRatio >= 0.8) {
            console.warn(`[x-browser] Strategy 1b ACCEPTED: ${s1bverify.typed.length} chars (${(partialRatio * 100).toFixed(0)}%), Post enabled`);
            textInserted = true;
          } else {
            console.warn(`[x-browser] Strategy 1b partial: ${s1bverify.typed.length} chars (${(partialRatio * 100).toFixed(0)}%), too low`);
          }
        }
      }

      // ── Strategy 2: osascript keystroke (real keyboard, undetectable) ──
      if (!textInserted && process.platform === 'darwin') {
        console.log('[x-browser] Strategy 2: osascript real keyboard typing...');

        // Smart reset: keyboard cleanup + SPA navigate, avoid about:blank if possible
        console.log('[x-browser] Strategy 2: clearing editor for fresh start...');
        await clickEditorWithMouse();
        await clearEditorKeyboard();
        await sleep(300);
        // Check if we're still on compose page — if so, just verify editor is clean
        const s2PageCheck = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
          expression: `(function() {
            if (!location.href.includes('x.com/compose')) return 'wrong_page';
            var ed = document.querySelector('[data-testid="tweetTextarea_0"]');
            if (!ed) return 'no_editor';
            var txt = (ed.textContent || '').trim();
            return txt.length > 0 ? 'stale:' + txt.length : 'clean';
          })()`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        console.log(`[x-browser] Strategy 2 page state: ${s2PageCheck.result.value}`);
        if (s2PageCheck.result.value !== 'clean') {
          // Navigate within x.com SPA (no about:blank — preserve the session)
          console.log('[x-browser] Strategy 2: SPA navigate to fresh compose...');
          await cdp!.send('Page.navigate', { url: X_COMPOSE_URL }, { sessionId: activeSessionId, timeoutMs: 45_000 });
          await sleep(4000);
        }
        const editorReady = await (async () => {
          const start = Date.now();
          while (Date.now() - start < 15_000) {
            const r = await cdp!.send<{ result: { value: boolean } }>('Runtime.evaluate', {
              expression: `!!document.querySelector('[data-testid="tweetTextarea_0"]')`,
              returnByValue: true,
            }, { sessionId: activeSessionId });
            if (r.result.value) return true;
            await sleep(1000);
          }
          return false;
        })();

        if (editorReady) {
          // Re-upload images on the fresh page
          if (imagesToUpload.length > 0) {
            console.log(`[x-browser] Strategy 2: Re-uploading ${imagesToUpload.length} images on fresh page...`);
            for (const imagePath of imagesToUpload) {
              if (!fs.existsSync(imagePath)) continue;
              try {
                const docResult = await cdp!.send<{ result: { root: { nodeId: number } } }>('DOM.getDocument', { depth: 0 }, { sessionId: activeSessionId });
                const inputResult = await cdp!.send<{ result: { nodeId: number } }>('DOM.querySelector', {
                  nodeId: docResult.result.root.nodeId,
                  selector: 'input[type="file"][accept*="image"]',
                }, { sessionId: activeSessionId });
                if (inputResult.result.nodeId) {
                  await cdp!.send('DOM.setFileInputFiles', {
                    nodeId: inputResult.result.nodeId,
                    files: [imagePath],
                  }, { sessionId: activeSessionId });
                  await sleep(2000);
                }
              } catch { /* skip failed image */ }
            }
            await sleep(3000);
          }

          // Click editor with mouse, then type via osascript
          await clickEditorWithMouse();
          await sleep(300);

          // Activate Chrome window and type text via System Events
          const { spawnSync } = await import('node:child_process');
          spawnSync('osascript', ['-e', 'tell application "Google Chrome" to activate'], { timeout: 5000 });
          await sleep(500);

          // Split text into chunks to avoid osascript string length limits
          const CHUNK_SIZE = 50;
          const chunks: string[] = [];
          for (let i = 0; i < finalText.length; i += CHUNK_SIZE) {
            chunks.push(finalText.slice(i, i + CHUNK_SIZE));
          }

          console.log(`[x-browser] Typing ${finalText.length} chars in ${chunks.length} chunks via osascript...`);
          for (let ci = 0; ci < chunks.length; ci++) {
            const chunk = chunks[ci]!;
            // Escape for AppleScript: backslashes and quotes
            const escaped = chunk.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
            spawnSync('osascript', ['-e', `tell application "System Events" to keystroke "${escaped}"`], { timeout: 10000 });
            await sleep(150);
          }
          await sleep(1000);

          const s2verify = await verifyEditorText();
          const s2btnOk = await isPostButtonEnabled();
          if (s2verify.ok && s2btnOk) {
            console.log(`[x-browser] Strategy 2 SUCCESS: text verified (${s2verify.typed.length} chars), Post button enabled`);
            textInserted = true;
          } else if (s2verify.ok && !s2btnOk) {
            console.warn(`[x-browser] Strategy 2 PARTIAL: text (${s2verify.typed.length} chars) but Post still disabled`);
            // One more wait — osascript typing may need extra time for Draft.js to process
            await sleep(2000);
            if (await isPostButtonEnabled()) {
              console.log('[x-browser] Strategy 2 SUCCESS after extra wait');
              textInserted = true;
            }
          } else {
            console.warn(`[x-browser] Strategy 2 FAILED: text verification failed`);
          }
        }
      }

      // ── Strategy 3: Clipboard paste via osascript Cmd+V ──
      if (!textInserted && process.platform === 'darwin') {
        console.log('[x-browser] Strategy 3: Clipboard paste via osascript Cmd+V...');
        const { spawnSync } = await import('node:child_process');

        // Put text in system clipboard
        const pbcopy = spawnSync('pbcopy', { input: finalText, timeout: 5000 });
        if (pbcopy.status === 0) {
          await clickEditorWithMouse();
          await clearEditorKeyboard();
          await sleep(300);

          // Activate Chrome and paste
          spawnSync('osascript', ['-e', 'tell application "Google Chrome" to activate'], { timeout: 5000 });
          await sleep(300);
          spawnSync('osascript', ['-e', 'tell application "System Events" to keystroke "v" using command down'], { timeout: 5000 });
          await sleep(1500);

          const s3verify = await verifyEditorText();
          const s3btnOk = await isPostButtonEnabled();
          if (s3verify.ok && s3btnOk) {
            console.log(`[x-browser] Strategy 3 SUCCESS: text verified (${s3verify.typed.length} chars), Post button enabled`);
            textInserted = true;
          } else {
            console.warn(`[x-browser] Strategy 3 FAILED: DOM=${s3verify.typed.length} chars, Post button enabled=${s3btnOk}`);
          }
        }
      }

      if (!textInserted) {
        console.warn('[x-browser] ⚠️ All text strategies failed. Text is likely in DOM but Draft.js did not accept it.');
        console.warn('[x-browser] Please manually paste text and click Post in the browser window.');
      }
    }

    if (submit) {
      // Verify Post button is clickable before clicking
      const btnCheck = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
        expression: `(function() {
          var btn = document.querySelector('[data-testid="tweetButton"]');
          if (!btn) return 'not_found';
          if (btn.getAttribute('aria-disabled') === 'true' || btn.disabled) return 'disabled';
          return 'ok';
        })()`,
        returnByValue: true,
      }, { sessionId: activeSessionId });

      if (btnCheck.result.value === 'disabled') {
        console.warn('[x-browser] ⚠️ Post button is disabled (image may still be processing). Waiting up to 30s...');
        const disabledWait = Date.now();
        while (Date.now() - disabledWait < 30_000) {
          await sleep(1000);
          const r = await cdp!.send<{ result: { value: boolean } }>('Runtime.evaluate', {
            expression: `!(document.querySelector('[data-testid="tweetButton"]')?.getAttribute('aria-disabled') === 'true')`,
            returnByValue: true,
          }, { sessionId: activeSessionId });
          if (r.result.value) break;
        }
      }

      console.log('[x-browser] Clicking Post button via CDP mouse event...');
      const btnPos = await cdp.send<{ result: { value: { x: number; y: number } | null } }>('Runtime.evaluate', {
        expression: `(() => {
          const btn = document.querySelector('[data-testid="tweetButton"]');
          if (!btn) return null;
          const r = btn.getBoundingClientRect();
          return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
        })()`,
        returnByValue: true,
      }, { sessionId: activeSessionId });

      if (btnPos.result.value) {
        const { x, y } = btnPos.result.value;
        // Full realistic mouse sequence: move → press → release
        // Missing mouseMoved causes X to reject synthetic clicks
        await cdp.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }, { sessionId: activeSessionId });
        await sleep(80);
        await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 }, { sessionId: activeSessionId });
        await sleep(60);
        await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 }, { sessionId: activeSessionId });
        await sleep(500);
        // Fallback: if dialog is still open, try JS .click() + keyboard Enter
        const stillOpen = await cdp.send<{ result: { value: boolean } }>('Runtime.evaluate', {
          expression: `!!document.querySelector('[data-testid="tweetButton"]')`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        if (stillOpen.result.value) {
          console.warn('[x-browser] Post dialog still open after mouse click, trying focus + Enter...');
          await cdp.send('Runtime.evaluate', {
            expression: `document.querySelector('[data-testid="tweetButton"]')?.focus()`,
          }, { sessionId: activeSessionId });
          await sleep(100);
          await cdp.send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 }, { sessionId: activeSessionId });
          await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 }, { sessionId: activeSessionId });
        }
      } else {
        console.warn('[x-browser] Post button not found for mouse click, falling back to .click()');
        await cdp.send('Runtime.evaluate', {
          expression: `document.querySelector('[data-testid="tweetButton"]')?.click()`,
        }, { sessionId: activeSessionId });
      }

      // Verify the compose dialog disappears (= post was actually sent)
      // Also detect error messages like "exceeds the number of allowed hashtags"
      console.log('[x-browser] Verifying post was published...');
      let postVerified = false;
      let hashtagError = false;
      const verifyStart = Date.now();
      while (Date.now() - verifyStart < 15_000) {
        await sleep(1500);
        try {
          const state = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
            expression: `(function() {
              var editor = document.querySelector('[data-testid="tweetTextarea_0"]');
              var btn = document.querySelector('[data-testid="tweetButton"]');
              if (!editor && !btn) return 'posted';
              // Check for error messages (toasts, alerts, inline errors)
              var allText = document.body.innerText || '';
              if (allText.includes('exceeds the number of allowed hashtags')) return 'hashtag_error';
              if (allText.includes('Something went wrong')) return 'error';
              var toasts = document.querySelectorAll('[data-testid="toast"], [role="alert"]');
              for (var i = 0; i < toasts.length; i++) {
                var txt = toasts[i].textContent || '';
                if (txt.includes('post') || txt.includes('sent') || txt.includes('Your post')) return 'posted';
                if (txt.includes('hashtag') || txt.includes('exceeds')) return 'hashtag_error';
              }
              return 'still_editing';
            })()`,
            returnByValue: true,
          }, { sessionId: activeSessionId });
          if (state.result.value === 'posted') {
            postVerified = true;
            break;
          }
          if (state.result.value === 'hashtag_error') {
            hashtagError = true;
            break;
          }
        } catch {
          postVerified = true;
          break;
        }
      }

      // Handle hashtag error: clear editor, strip ALL hashtags, re-insert, re-submit
      if (hashtagError) {
        console.warn('[x-browser] ⚠️ X rejected post: too many hashtags. Stripping all hashtags and retrying...');
        // Navigate to fresh compose page
        await cdp!.send('Page.navigate', { url: 'about:blank' }, { sessionId: activeSessionId, timeoutMs: 10_000 });
        await sleep(1500);
        await cdp!.send('Page.navigate', { url: X_COMPOSE_URL }, { sessionId: activeSessionId, timeoutMs: 45_000 });
        await sleep(4000);
        await waitForEditor();
        // Re-upload images
        if (imagesToUpload.length > 0) {
          for (const imgPath of imagesToUpload) {
            const objRes = await cdp!.send<{ result: { objectId?: string } }>('Runtime.evaluate', {
              expression: `document.querySelector('input[type="file"][accept*="image"]')`,
              returnByValue: false,
            }, { sessionId: activeSessionId });
            if (objRes.result.objectId) {
              await cdp!.send('DOM.setFileInputFiles', { files: [imgPath], objectId: objRes.result.objectId }, { sessionId: activeSessionId });
              await sleep(3000);
            }
          }
        }
        // Strip ALL hashtags from text and re-insert
        const noHashtagText = finalText.replace(/#[\p{L}\p{N}_]+/gu, '').replace(/  +/g, ' ').replace(/\n\s*\n\s*\n/g, '\n\n').trim();
        console.log(`[x-browser] Re-inserting text without hashtags (${noHashtagText.length} chars)...`);
        await clickEditorWithMouse();
        const retryLines = noHashtagText.split('\n');
        for (let li = 0; li < retryLines.length; li++) {
          if (retryLines[li]!.length > 0) {
            await cdp!.send('Input.insertText', { text: retryLines[li]! }, { sessionId: activeSessionId });
            await sleep(50);
          }
          if (li < retryLines.length - 1) {
            await cdp!.send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 }, { sessionId: activeSessionId });
            await cdp!.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 }, { sessionId: activeSessionId });
            await sleep(50);
          }
        }
        await sleep(1000);
        // Re-click Post
        const retryBtnOk = await isPostButtonEnabled();
        if (retryBtnOk) {
          console.log('[x-browser] Re-clicking Post (hashtags removed)...');
          const retryBtnPos = await cdp!.send<{ result: { value: { x: number; y: number } | null } }>('Runtime.evaluate', {
            expression: `(function() { var b = document.querySelector('[data-testid="tweetButton"]'); if (!b) return null; var r = b.getBoundingClientRect(); return { x: r.x + r.width/2, y: r.y + r.height/2 }; })()`,
            returnByValue: true,
          }, { sessionId: activeSessionId });
          if (retryBtnPos.result.value) {
            const { x, y } = retryBtnPos.result.value;
            await cdp!.send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 }, { sessionId: activeSessionId });
            await cdp!.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 }, { sessionId: activeSessionId });
          }
          await sleep(3000);
          console.log('[x-browser] ✅ Retried post without hashtags');
          postVerified = true;
        } else {
          console.warn('[x-browser] ⚠️ Post button still disabled after hashtag removal');
        }
      }

      if (postVerified) {
        console.log('[x-browser] ✅ Post published successfully!');
      } else if (!hashtagError) {
        console.warn('[x-browser] ⚠️ Post button was clicked but compose dialog is still open.');
        console.warn('[x-browser] The post may have been blocked by X (captcha, rate limit, or anti-automation).');
        console.warn('[x-browser] Please check the browser window for any prompts.');
      }
    } else {
      console.log('[x-browser] ✅ Post composed. Browser stays open for your review.');
      console.log('[x-browser] 👀 Waiting for you to review and click the post button...');
      console.log('[x-browser] (Script will auto-detect when you post or close the browser)');

      const waitResult = await waitForUserPostOrClose(cdp, activeSessionId, timeoutMs);
      switch (waitResult) {
        case 'posted':
          console.log('[x-browser] ✅ Post published successfully!');
          break;
        case 'browser_closed':
          console.log('[x-browser] 🔒 Browser was closed. Post was NOT published.');
          break;
        case 'timeout':
          console.log(`[x-browser] ⏰ Wait timeout (${Math.round(timeoutMs / 1000)}s). Browser left open — post manually if needed.`);
          break;
      }
    }
  } finally {
    if (chrome && loggedInDuringRun && cdp && sessionId) {
      console.log('[x-browser] Waiting for X session cookies to persist...');
      await waitForXSessionPersistence({ cdp, sessionId }).catch(() => {});
    }

    if (cdp) {
      cdp.close();
    }
    // Always keep Chrome running for reuse by subsequent invocations.
    // Chrome is launched detached, so it survives bun process termination (including SIGKILL).
    if (chrome) {
      chrome.unref();
      console.log(`[x-browser] Chrome left running on port ${port} for reuse`);
    }
  }
}

function printUsage(): never {
  console.log(`Post to X (Twitter) using real Chrome browser

Usage:
  npx -y bun x-browser.ts [options] [text]

Options:
  --image <path>      Add image (can be repeated, max 4)
  --text-file <path>  Read tweet text from file (avoids shell quoting issues with multiline text)
  --submit            Actually post (default: preview only)
  --profile <dir>     Chrome profile directory
  --help              Show this help

Examples:
  npx -y bun x-browser.ts "Hello from CLI!"
  npx -y bun x-browser.ts --text-file /tmp/tweet.txt --image ./screenshot.png --submit
  npx -y bun x-browser.ts "Post it!" --image a.png --image b.png --submit
`);
  process.exit(0);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) printUsage();

  const images: string[] = [];
  let submit = false;
  let profileDir: string | undefined;
  const textParts: string[] = [];

  let textFromFile: string | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i]!;
    if (arg === '--image' && args[i + 1]) {
      images.push(args[++i]!);
    } else if (arg === '--submit') {
      submit = true;
    } else if (arg === '--profile' && args[i + 1]) {
      profileDir = args[++i];
    } else if ((arg === '--text-file' || arg === '--tf') && args[i + 1]) {
      const fs = await import('node:fs');
      const filePath = args[++i]!;
      if (!fs.existsSync(filePath)) {
        console.error(`Error: text file not found: ${filePath}`);
        process.exit(1);
      }
      textFromFile = fs.readFileSync(filePath, 'utf-8').trim();
      console.log(`[x-browser] Read text from file: ${filePath} (${textFromFile.length} chars)`);
    } else if (!arg.startsWith('-')) {
      textParts.push(arg);
    }
  }

  let text = textFromFile || textParts.join(' ').trim() || undefined;

  // Auto-detect file paths passed as text (common agent mistake)
  if (text && !textFromFile && /^(\/|~\/|\.\/)[^\n]*\.(txt|md)$/i.test(text.trim())) {
    const fs = await import('node:fs');
    const resolvedPath = text.trim().replace(/^~\//, `${process.env.HOME}/`);
    if (fs.existsSync(resolvedPath)) {
      console.warn(`[x-browser] Auto-detected file path as text argument: "${text}"`);
      console.warn(`[x-browser] Reading text from file instead (use --text-file next time)`);
      text = fs.readFileSync(resolvedPath, 'utf-8').trim();
      console.log(`[x-browser] Read ${text.length} chars from ${resolvedPath}`);
    }
  }

  if (!text && images.length === 0) {
    console.error('Error: Provide text or at least one image.');
    process.exit(1);
  }

  await postToX({ text, images, submit, profileDir });
}

await main().catch((err) => {
  console.error(`Error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
