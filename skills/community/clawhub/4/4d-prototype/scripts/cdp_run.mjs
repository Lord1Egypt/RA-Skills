#!/usr/bin/env node
// Headless Chrome step runner (Chrome DevTools Protocol, zero dependencies, needs Node 22+ for built-in fetch and WebSocket).
// For full-resolution 1920×1080 screenshots, polling long autoplay runs, collecting console errors and uncaught exceptions, and page sweeps.
//
// Usage: node cdp_run.mjs <out-dir> <steps.json> [--port 9333] [--width 1920] [--height 1080]
// The CHROME environment variable overrides the Chrome executable path.
//
// steps.json is an array executed in order:
//   {"nav": url, "wait"?: ms}            open a page (then wait 1500ms by default)
//   {"eval": js, "log"?: label}          evaluate an expression and print the result; wrapped in an async IIFE if it contains await
//   {"click": selector, "log"?: label}   click an element (prints missing if not found)
//   {"waitFor": js, "timeout"?: ms}      poll until the expression is truthy (default 20000ms)
//   {"wait": ms}                         wait
//   {"shot": name}                       screenshot to <out-dir>/<name>.png
//   {"check": "overflow"}                print whether the page overflows horizontally
// At the end prints "ERRORS n" and the first 20 console errors / warnings / uncaught exceptions.
import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const args = process.argv.slice(2);
const opt = (name, def) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : def;
};
const [outDir, stepsFile] = args.filter((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
if (!outDir || !stepsFile) {
  console.error('usage: node cdp_run.mjs <out-dir> <steps.json> [--port 9333] [--width 1920] [--height 1080]');
  process.exit(2);
}
const port = Number(opt('port', 9333));
const width = Number(opt('width', 1920));
const height = Number(opt('height', 1080));
const steps = JSON.parse(readFileSync(stepsFile, 'utf8'));
mkdirSync(outDir, { recursive: true });

const CANDIDATES = [
  process.env.CHROME,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
].filter(Boolean);
const chromePath = CANDIDATES.find((p) => existsSync(p));
if (!chromePath) {
  console.error('Chrome not found: set its path with the CHROME environment variable');
  process.exit(2);
}

const profile = join(outDir, `.profile-${Date.now()}`);
const chrome = spawn(chromePath, ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, `--window-size=${width},${height}`, 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function cleanup(code) {
  try {
    chrome.kill();
  } catch {
    /* already exited */
  }
  setTimeout(() => {
    try {
      rmSync(profile, { recursive: true, force: true });
    } catch {
      /* ignore */
    }
    process.exit(code);
  }, 300);
}

// A fresh profile can be slow on first start: wait up to 30 s
let ws;
for (let i = 0; i < 150 && !ws; i++) {
  try {
    const list = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
    const page = list.find((t) => t.type === 'page');
    if (page) ws = new WebSocket(page.webSocketDebuggerUrl);
  } catch {
    /* not up yet */
  }
  if (!ws) await sleep(200);
}
if (!ws) {
  console.error(`Chrome did not start on port ${port} (if the port is taken, run: pkill -f "remote-debugging-port=${port}")`);
  cleanup(1);
} else {
  await new Promise((r) => ws.addEventListener('open', r));
  let id = 0;
  const pending = new Map();
  const errors = [];
  ws.addEventListener('message', (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) {
      pending.get(m.id)(m);
      pending.delete(m.id);
    }
    if (m.method === 'Runtime.exceptionThrown') {
      const d = m.params.exceptionDetails;
      errors.push('EXC ' + String(d.exception?.description ?? d.text).slice(0, 400));
    }
    if (m.method === 'Runtime.consoleAPICalled' && (m.params.type === 'error' || m.params.type === 'warning')) {
      errors.push(m.params.type + ' ' + m.params.args.map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 400));
    }
  });
  const send = (method, params = {}) =>
    new Promise((r) => {
      const i = ++id;
      pending.set(i, r);
      ws.send(JSON.stringify({ id: i, method, params }));
    });
  const evaluate = async (expr) => {
    const code = /\bawait\b/.test(expr) && !/^\s*\(async/.test(expr) ? `(async () => { return (${expr}); })()` : expr;
    const r = await send('Runtime.evaluate', { expression: code, awaitPromise: true, returnByValue: true });
    if (r.result?.exceptionDetails) return { error: r.result.exceptionDetails.exception?.description ?? r.result.exceptionDetails.text };
    return { value: r.result?.result?.value };
  };

  await send('Runtime.enable');
  await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false });

  const t0 = Date.now();
  const stamp = () => `${((Date.now() - t0) / 1000).toFixed(1)}s`;
  for (const s of steps) {
    if (s.nav) {
      await send('Page.navigate', { url: s.nav });
      await sleep(s.wait ?? 1500);
      continue;
    }
    if (s.eval) {
      const r = await evaluate(s.eval);
      if (s.log || r.error) console.log(`[${stamp()}] ${s.log ?? 'eval'}`, r.error ? `ERROR ${String(r.error).slice(0, 300)}` : JSON.stringify(r.value));
    }
    if (s.click) {
      const sel = JSON.stringify(s.click);
      const r = await evaluate(`(() => { const e = document.querySelector(${sel}); if (!e) return 'missing ' + ${sel}; e.scrollIntoView({ block: 'center' }); e.click(); return 'ok'; })()`);
      if (s.log || r.value !== 'ok') console.log(`[${stamp()}] click ${s.click}`, r.error ?? r.value);
    }
    if (s.waitFor) {
      const until = Date.now() + (s.timeout ?? 20000);
      let ok = false;
      while (Date.now() < until) {
        const r = await evaluate(`!!(${s.waitFor})`);
        if (r.value) {
          ok = true;
          break;
        }
        await sleep(250);
      }
      console.log(`[${stamp()}] waitFor ${ok ? 'ok' : 'TIMEOUT'}: ${s.waitFor.slice(0, 120)}`);
    }
    if (s.check === 'overflow') {
      const r = await evaluate(`({ scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth })`);
      const v = r.value ?? {};
      console.log(`[${stamp()}] overflow ${v.scrollWidth > v.innerWidth ? 'YES' : 'no'} (${v.scrollWidth}/${v.innerWidth}) ${s.log ?? ''}`);
    }
    if (s.wait && !s.nav) await sleep(s.wait);
    if (s.shot) {
      const r = await send('Page.captureScreenshot', { format: 'png' });
      const file = join(outDir, `${s.shot}.png`);
      writeFileSync(file, Buffer.from(r.result.data, 'base64'));
      console.log(`[${stamp()}] shot ${file}`);
    }
  }
  console.log('ERRORS', errors.length);
  errors.slice(0, 20).forEach((x) => console.log('  ' + x));
  ws.close();
  cleanup(0);
}
