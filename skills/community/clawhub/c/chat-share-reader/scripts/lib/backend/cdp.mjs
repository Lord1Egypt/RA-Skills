// CDP 后端：拉起用户本机的 Chrome（真实二进制、真实指纹），用 DevTools 协议驱动。
// 这是普适方案：零 npm 依赖（Node 22 内置 WebSocket），跨平台，不需要装 opencli。
//
// 关键实测结论：Cloudflare 判定看的是浏览器 profile 的"信誉"，不是 UA。
// 全新 profile 第一次访问 grok.com / perplexity.ai 会停在挑战页，Claude 能直接过。
// 所以这里不假装自己是浏览器，而是遇到挑战时提示用户在弹出的窗口里手动过一次，
// cookie 存进持久 profile，之后就不用再管。
import { spawn, execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { setTimeout as sleep } from 'node:timers/promises';
import { config, norm } from '../config.mjs';

const CHROME_CANDIDATES = [
  process.env.CHROME_BIN,
  norm(config().chromeBin),
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  '/usr/bin/google-chrome',
  '/usr/bin/google-chrome-stable',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
].filter(Boolean);

const CHALLENGE_HINTS = [
  'Just a moment',
  '正在进行安全验证',
  '请稍候',
  'Verifying you are human',
  'Checking your browser',
  '安全服务防护',
];

export function findChrome() {
  for (const p of CHROME_CANDIDATES) if (existsSync(p)) return p;
  return '';
}

export function available() {
  return !!findChrome();
}

export function defaultProfile() {
  return (
    process.env.CSR_PROFILE ||
    norm(config().profile) ||
    path.join(os.homedir(), '.chat-share-reader', 'chrome-profile')
  );
}

export function defaultPort() {
  return Number(process.env.CSR_PORT || config().port || 9333);
}

// 探测端口状态：free 没人监听，chrome 是本插件的调试端点，busy 是别的程序占了
function probePort(port, timeoutMs = 600) {
  return new Promise((resolve) => {
    const sock = net.connect({ port, host: '127.0.0.1' });
    let done = false;
    const finish = (v) => {
      if (done) return;
      done = true;
      sock.destroy();
      resolve(v);
    };
    sock.once('connect', async () => {
      // 能连上，看是不是 Chrome 的调试端口
      try {
        const r = await fetch(`http://127.0.0.1:${port}/json/version`, {
          signal: AbortSignal.timeout(1200),
        });
        const j = await r.json();
        finish(j && j.Browser ? 'chrome' : 'busy');
      } catch {
        finish('busy');
      }
    });
    sock.once('error', (e) => finish(e.code === 'ECONNREFUSED' ? 'free' : 'busy'));
    setTimeout(() => finish('busy'), timeoutMs);
  });
}

// 记住「上一次是我们自己在哪个端口、哪个 profile 起的 Chrome」。
// 只有一个用途：下次复用自己的那个实例，而不是复用别人开着的调试端口。
function markerPath() {
  return path.join(os.homedir(), '.chat-share-reader', 'browser.json');
}

async function readMarker() {
  try {
    const j = JSON.parse(await readFile(markerPath(), 'utf8'));
    return j && typeof j.port === 'number' ? j : null;
  } catch {
    return null;
  }
}

async function writeMarker(port, profile) {
  try {
    await mkdir(path.dirname(markerPath()), { recursive: true });
    await writeFile(markerPath(), JSON.stringify({ port, profile, at: Date.now() }), 'utf8');
  } catch {
    /* 记不住只是下次多起一个浏览器，不影响功能 */
  }
}

// 端口上那个 Chrome 算不算「我们自己的」。抽成纯函数，好单测，也避免以后有人
// 图省事改回「只要端口上有 Chrome 就复用」。
export function isOurChrome({ state, port, profile, mark }) {
  return state === 'chrome' && !!mark && mark.port === port && mark.profile === profile;
}

// 从起始端口往后找一个能用的。被别的程序占住时不硬撞，直接换下一个
async function pickPort(start, profile, span = 20) {
  const mark = await readMarker();
  for (let p = start; p < start + span; p++) {
    const state = await probePort(p);
    // 端点上是 Chrome，但只有「我们上次用同一个 profile 起的」才认。
    // 别人的调试端口一律不碰：连上去等于借用别人的会话和 cookie。
    if (isOurChrome({ state, port: p, profile, mark })) return { port: p, reuse: true };
    if (state === 'chrome') continue;
    if (state === 'free') return { port: p, reuse: false };
    // busy：换个端口继续
  }
  throw new Error(
    `Ports ${start}-${start + span - 1} are all taken.\n` +
      `Set CSR_PORT to a free one, or close whatever is holding them.\n` +
      `端口 ${start} 到 ${start + span - 1} 全被占用。用 CSR_PORT 指定空闲端口，或关掉占用它们的程序。`
  );
}

async function waitForPort(port, tries = 60) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (r.ok) return await r.json();
    } catch {
      /* 还没起来 */
    }
    await sleep(500);
  }
  const state = await probePort(port);
  throw new Error(
    state === 'busy'
      ? `Port ${port} is held by another process, so Chrome could not bind it. Set CSR_PORT to a free port.\n端口 ${port} 被别的程序占用，Chrome 没能起来。用 CSR_PORT 换一个端口。`
      : `Chrome did not answer on port ${port} within 30s. Usual causes: Chrome failed to start, security software blocked it, or the profile is locked by another Chrome instance.\nChrome 调试端口 ${port} 在 30 秒内没响应。常见原因：Chrome 启动失败、被安全软件拦下、或 profile 被另一个 Chrome 实例锁着。`
  );
}

async function launchChrome({ port, profile }) {
  const bin = findChrome();
  if (!bin) throw new Error('Chrome / Edge not found. Set CHROME_BIN to the executable path.\n没找到 Chrome / Edge，可用 CHROME_BIN 指定路径');
  await mkdir(profile, { recursive: true });

  const args = [
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${profile}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-blink-features=AutomationControlled',
    '--window-size=1280,960',
    'about:blank',
  ];
  const proc = spawn(bin, args, { stdio: 'ignore' });
  proc.unref();
  await writeMarker(port, profile);
  return proc;
}

class Conn {
  constructor(ws) {
    this.ws = ws;
    this.seq = 0;
    this.pending = new Map();
    ws.addEventListener('message', (ev) => {
      let msg;
      try {
        msg = JSON.parse(ev.data);
      } catch {
        return;
      }
      const p = msg.id && this.pending.get(msg.id);
      if (!p) return;
      this.pending.delete(msg.id);
      if (msg.error) p.reject(new Error(msg.error.message));
      else p.resolve(msg.result);
    });
  }

  static async open(wsUrl) {
    const ws = new WebSocket(wsUrl);
    await new Promise((res, rej) => {
      ws.addEventListener('open', res, { once: true });
      ws.addEventListener('error', () => rej(new Error('CDP WebSocket 连不上')), { once: true });
    });
    return new Conn(ws);
  }

  send(method, params = {}) {
    const id = ++this.seq;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  close() {
    try {
      this.ws.close();
    } catch {
      /* ignore */
    }
  }
}

export async function createSession({ port, profile, name = 'csr' } = {}) {
  const prof = profile || defaultProfile();

  // 端口可能被别的程序占着（比如另一个 Chrome 实例、别的调试工具），
  // 直接沿用会卡在「端口没起来」这种含糊报错上。先探一遍再决定
  const picked = await pickPort(port || defaultPort(), prof);
  const usePort = picked.port;
  if (!picked.reuse) {
    await launchChrome({ port: usePort, profile: prof });
    await waitForPort(usePort);
  } else if (usePort !== (port || defaultPort())) {
    console.error(`Port ${port || defaultPort()} is not ours to reuse, starting a browser on ${usePort} instead.`);
  }

  let tabId = null;
  let conn = null;
  let told = false;

  async function ensureTab(url) {
    if (conn) {
      conn.close();
      conn = null;
    }
    const r = await fetch(`http://127.0.0.1:${usePort}/json/new?${encodeURIComponent(url)}`, {
      method: 'PUT',
    });
    if (!r.ok) throw new Error('开标签失败：HTTP ' + r.status);
    const tab = await r.json();
    tabId = tab.id;
    conn = await Conn.open(tab.webSocketDebuggerUrl);
    await conn.send('Page.enable').catch(() => {});
    await conn.send('Runtime.enable').catch(() => {});
    return tab;
  }

  return {
    backend: 'cdp',
    name,

    async open(url) {
      await ensureTab(url);
    },

    async eval(code) {
      const r = await conn.send('Runtime.evaluate', {
        expression: code,
        returnByValue: true,
        awaitPromise: true,
      });
      if (r.exceptionDetails) {
        throw new Error(
          '页面脚本报错：' +
            (r.exceptionDetails.exception?.description || r.exceptionDetails.text || '')
        );
      }
      return typeof r.result.value === 'string' ? r.result.value : JSON.stringify(r.result.value);
    },

    async waitReady({ minText = 200, tries = 20, delay = 3000, probe } = {}) {
      for (let i = 0; i < tries; i++) {
        const code =
          probe || 'JSON.stringify({len: document.body.innerText.length, url: location.href})';
        try {
          const out = await this.eval(code);
          const j = JSON.parse(out.slice(out.indexOf('{'), out.lastIndexOf('}') + 1));
          if (probe ? j.ok : j.len >= minText) return j;
          if (!probe) {
            const text = await this.eval('document.body.innerText.slice(0,200)');
            if (!told && CHALLENGE_HINTS.some((h) => text.includes(h))) {
              told = true;
              console.error(
                '[提示] 页面停在安全验证。请在弹出的 Chrome 窗口里手动完成验证，脚本会继续等（最多 1 分钟）。'
              );
            }
          }
        } catch {
          /* 页面还在导航 */
        }
        await sleep(delay);
      }
      throw new Error('页面在超时内没有渲染出内容（可能是安全验证没通过）');
    },

    // 只关标签，不关浏览器：关掉 Chrome 会丢掉用户刚建立的 profile 信誉
    async close() {
      if (conn) {
        conn.close();
        conn = null;
      }
      if (tabId) {
        await fetch(`http://127.0.0.1:${usePort}/json/close/${tabId}`).catch(() => {});
        tabId = null;
      }
    },
  };
}
