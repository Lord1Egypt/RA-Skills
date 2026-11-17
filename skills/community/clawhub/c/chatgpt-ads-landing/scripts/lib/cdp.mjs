// Minimal Chrome DevTools Protocol driver — zero dependencies (Node ≥ 22 has
// global WebSocket and fetch). Used by verify.mjs and fetch-official.mjs.
import { spawn } from 'node:child_process';
import { existsSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const CHROME_CANDIDATES = [
  process.env.CHROME_PATH,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
].filter(Boolean);

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let nextPort = 9600 + Math.floor(Math.random() * 300);

/**
 * Launch a throwaway Chrome profile.
 *   proxy:    'http://<your-proxy>' to route through a proxy; null forces a
 *             direct connection (--no-proxy-server), so a system-wide proxy
 *             such as Clash cannot silently change the visitor IP.
 *   headless: false is needed for pages behind a Cloudflare challenge.
 */
export async function launch({ proxy = null, headless = true, lang = 'en-US', profile, keepProfile = false } = {}) {
  const bin = CHROME_CANDIDATES.find((p) => existsSync(p));
  if (!bin) { throw new Error('Chrome not found; set CHROME_PATH'); }
  if (typeof WebSocket !== 'function') { throw new Error('Node ≥ 22 required (global WebSocket)'); }
  const port = nextPort++;
  // A temp profile is deleted on close unless keepProfile (the caller cleans up).
  const ownProfile = !profile && !keepProfile;
  const dir = profile || mkdtempSync(join(tmpdir(), 'lp-verify-'));
  const args = [`--remote-debugging-port=${port}`, `--user-data-dir=${dir}`, '--no-first-run',
    '--no-default-browser-check', `--lang=${lang}`, '--window-size=1400,900'];
  if (headless) { args.push('--headless=new'); }
  if (proxy) { args.push(`--proxy-server=${proxy}`, '--proxy-bypass-list=localhost;127.0.0.1'); } else { args.push('--no-proxy-server'); }
  args.push('about:blank');
  const proc = spawn(bin, args, { stdio: 'ignore' });

  let target;
  for (let i = 0; i < 60 && !target; i++) {
    await sleep(250);
    try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === 'page'); } catch { /* not up yet */ }
  }
  if (!target) { proc.kill(); throw new Error('Chrome did not start'); }

  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.addEventListener('open', r); ws.addEventListener('error', j); });
  let id = 0;
  const pending = new Map();
  const listeners = [];
  ws.addEventListener('message', ({ data }) => {
    const m = JSON.parse(data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); return; }
    if (m.method) { listeners.forEach((fn) => fn(m.method, m.params)); }
  });
  const send = (method, params = {}) => new Promise((res, rej) => {
    const i = ++id;
    const t = setTimeout(() => { pending.delete(i); rej(new Error(`CDP timeout: ${method}`)); }, 60000);
    pending.set(i, (m) => { clearTimeout(t); m.error ? rej(new Error(`${method}: ${m.error.message}`)) : res(m.result); });
    ws.send(JSON.stringify({ id: i, method, params }));
  });
  const evaluate = async (expression) => {
    const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) { throw new Error('page error: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text)); }
    return r.result.value;
  };
  // Graceful close so the profile (localStorage, cookies) is flushed to disk —
  // a revisit test reuses the profile. Falls back to kill after 5s.
  const close = async () => {
    const exited = new Promise((r) => proc.once('exit', r));
    try { await Promise.race([send('Browser.close'), sleep(3000)]); } catch { /* socket already gone */ }
    await Promise.race([exited, sleep(5000)]);
    if (proc.exitCode === null) { proc.kill(); }
    try { ws.close(); } catch { /* already closed */ }
    if (ownProfile) { rmSync(dir, { recursive: true, force: true }); }
  };
  return { send, evaluate, on: (fn) => listeners.push(fn), close, profile: dir };
}

// Wait for the load event (slow proxy nodes can take > 10s for a page with
// images), then waitMs more for async work such as the pixel SDK.
export async function navigate(page, url, waitMs = 4000, maxLoadMs = 30000) {
  await page.send('Page.enable');
  await page.send('Page.navigate', { url });
  const until = Date.now() + maxLoadMs;
  await sleep(300);
  while (Date.now() < until) {
    let state = '';
    try { state = await page.evaluate('document.readyState'); } catch { state = ''; }
    if (state === 'complete') { break; }
    await sleep(300);
  }
  await sleep(waitMs);
}
