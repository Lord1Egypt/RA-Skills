import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

import { logger } from './logger.js';
import { fetch_with_timeout, resolve_proxy, sleep } from './http.js';
import { type CookieMap, write_cookie_file } from './cookie-file.js';
import { resolveFlowWebCookiePath, resolveFlowWebDataDir } from './paths.js';

const DEFAULT_CDP_PORT = 9222;
const DEFAULT_WSL_CMD_EXE = '/mnt/c/Windows/System32/cmd.exe';
const DEFAULT_WSL_CHROME_EXE = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const DEFAULT_WSL_USER_DATA_DIR = 'C:\\chrome-debug-openclaw';

type CdpSendOptions = { sessionId?: string; timeoutMs?: number };

export class CdpConnection {
  private ws: WebSocket;
  private nextId = 0;
  private pending = new Map<
    number,
    { resolve: (v: unknown) => void; reject: (e: Error) => void; timer: ReturnType<typeof setTimeout> | null }
  >();

  private constructor(ws: WebSocket) {
    this.ws = ws;
    this.ws.addEventListener('message', (event) => {
      try {
        const data = typeof event.data === 'string' ? event.data : new TextDecoder().decode(event.data as ArrayBuffer);
        const msg = JSON.parse(data) as { id?: number; result?: unknown; error?: { message?: string } };
        if (msg.id) {
          const p = this.pending.get(msg.id);
          if (p) {
            this.pending.delete(msg.id);
            if (p.timer) clearTimeout(p.timer);
            if (msg.error?.message) p.reject(new Error(msg.error.message));
            else p.resolve(msg.result);
          }
        }
      } catch {}
    });
    this.ws.addEventListener('close', () => {
      for (const [id, p] of this.pending.entries()) {
        this.pending.delete(id);
        if (p.timer) clearTimeout(p.timer);
        p.reject(new Error('CDP connection closed.'));
      }
    });
  }

  static async connect(url: string, timeoutMs: number): Promise<CdpConnection> {
    const ws = new WebSocket(url);
    await new Promise<void>((resolve, reject) => {
      const t = setTimeout(() => reject(new Error('CDP connection timeout.')), timeoutMs);
      ws.addEventListener('open', () => {
        clearTimeout(t);
        resolve();
      });
      ws.addEventListener('error', () => {
        clearTimeout(t);
        reject(new Error('CDP connection failed.'));
      });
    });
    return new CdpConnection(ws);
  }

  async send<T = unknown>(method: string, params?: Record<string, unknown>, opts?: CdpSendOptions): Promise<T> {
    const id = ++this.nextId;
    const msg: Record<string, unknown> = { id, method };
    if (params) msg.params = params;
    if (opts?.sessionId) msg.sessionId = opts.sessionId;

    const timeoutMs = opts?.timeoutMs ?? 15_000;
    const out = await new Promise<unknown>((resolve, reject) => {
      const t =
        timeoutMs > 0
          ? setTimeout(() => {
              this.pending.delete(id);
              reject(new Error(`CDP timeout: ${method}`));
            }, timeoutMs)
          : null;
      this.pending.set(id, { resolve, reject, timer: t });
      this.ws.send(JSON.stringify(msg));
    });
    return out as T;
  }

  close(): void {
    try {
      this.ws.close();
    } catch {}
  }
}

function get_cdp_port(): number {
  const envPort = parseInt(process.env.FLOW_WEB_DEBUG_PORT || process.env.AGENT_BROWSER_CDP_PORT || '', 10);
  if (envPort > 0) return envPort;
  return DEFAULT_CDP_PORT;
}

function is_wsl(): boolean {
  return !!process.env.WSL_DISTRO_NAME;
}

function parse_extra_args(raw: string | undefined): string[] {
  return (raw || '')
    .split(/[\r\n,]+/)
    .map((value) => value.trim())
    .filter(Boolean);
}

function resolve_local_chrome_path(): string | null {
  return process.env.FLOW_WEB_CHROME_PATH?.trim() || process.env.CHROME_PATH?.trim() || null;
}

function resolve_local_user_data_dir(): string {
  const override = process.env.FLOW_WEB_CHROME_PROFILE_DIR?.trim();
  if (override) return override;
  return path.join(resolveFlowWebDataDir(), 'chrome-debug-openclaw');
}

function start_windows_host_chrome(verbose: boolean): void {
  const cmdExe = process.env.AGENT_BROWSER_CMD_EXE_WSL?.trim() || DEFAULT_WSL_CMD_EXE;
  if (!fs.existsSync(cmdExe)) {
    throw new Error(`Windows cmd.exe bridge not found at: ${cmdExe}`);
  }

  const chromeExe =
    process.env.AGENT_BROWSER_CHROME_EXE_WIN?.trim() ||
    process.env.FLOW_WEB_CHROME_EXE_WIN?.trim() ||
    DEFAULT_WSL_CHROME_EXE;
  const userDataDir =
    process.env.AGENT_BROWSER_USER_DATA_DIR_WIN?.trim() ||
    process.env.FLOW_WEB_CHROME_USER_DATA_DIR_WIN?.trim() ||
    DEFAULT_WSL_USER_DATA_DIR;

  const args = [
    '/c',
    'start',
    '',
    chromeExe,
    `--remote-debugging-port=${get_cdp_port()}`,
    `--user-data-dir=${userDataDir}`,
  ];

  const proxy = resolve_proxy();
  if (proxy) args.push(`--proxy-server=${proxy}`);
  args.push(...parse_extra_args(process.env.FLOW_WEB_CHROME_EXTRA_ARGS || process.env.AGENT_BROWSER_CHROME_EXTRA_ARGS_WIN));

  if (verbose) logger.debug(`Starting host Chrome via cmd.exe with user data dir: ${userDataDir}`);
  const child = spawn(cmdExe, args, { detached: true, stdio: 'ignore' });
  child.unref();
}

function start_local_chrome(verbose: boolean): void {
  const chromePath = resolve_local_chrome_path();
  if (!chromePath) {
    throw new Error('FLOW_WEB_CHROME_PATH is required when not running under WSL.');
  }

  const args = [
    `--remote-debugging-port=${get_cdp_port()}`,
    `--user-data-dir=${resolve_local_user_data_dir()}`,
  ];

  const proxy = resolve_proxy();
  if (proxy) args.push(`--proxy-server=${proxy}`);
  args.push(...parse_extra_args(process.env.FLOW_WEB_CHROME_EXTRA_ARGS));

  if (verbose) logger.debug(`Starting local Chrome at: ${chromePath}`);
  const child = spawn(chromePath, args, { detached: true, stdio: 'ignore' });
  child.unref();
}

async function is_cdp_ready(port: number): Promise<boolean> {
  try {
    const res = await fetch_with_timeout(`http://127.0.0.1:${port}/json/version`, { timeout_ms: 2_000 });
    if (!res.ok) return false;
    const data = (await res.json()) as { webSocketDebuggerUrl?: string };
    return typeof data.webSocketDebuggerUrl === 'string' && data.webSocketDebuggerUrl.length > 0;
  } catch {
    return false;
  }
}

/** Ensure a Chrome CDP endpoint is available for UI automation. */
async function ensure_chrome_cdp(verbose: boolean): Promise<void> {
  const port = get_cdp_port();
  if (await is_cdp_ready(port)) {
    if (verbose) logger.debug(`Chrome CDP already ready on port ${port}`);
    return;
  }

  if (is_wsl()) {
    start_windows_host_chrome(verbose);
    return;
  }

  start_local_chrome(verbose);
}

async function wait_for_chrome_debug_port(port: number, timeoutMs: number): Promise<string> {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const res = await fetch_with_timeout(`http://127.0.0.1:${port}/json/version`, { timeout_ms: 5_000 });
      if (!res.ok) throw new Error(`status=${res.status}`);
      const j = (await res.json()) as { webSocketDebuggerUrl?: string };
      if (j.webSocketDebuggerUrl) return j.webSocketDebuggerUrl;
    } catch {}
    await sleep(200);
  }
  throw new Error(`Chrome debug port ${port} not ready after ${timeoutMs}ms`);
}

export type FlowAuthResult = {
  accessToken: string;
  cookies: CookieMap;
};

/**
 * Extract the OAuth access token from the Flow page.
 * Tries: __NEXT_DATA__ script tag → /fx/api/auth/session API
 */
async function extract_flow_token(
  cdp: CdpConnection,
  sessionId: string,
  verbose: boolean,
): Promise<string | null> {
  // Try __NEXT_DATA__ first
  try {
    const result = await cdp.send<{ result: { value?: string } }>(
      'Runtime.evaluate',
      {
        expression: `(() => {
          try {
            const el = document.getElementById('__NEXT_DATA__');
            if (el) {
              const d = JSON.parse(el.textContent);
              return d?.props?.pageProps?.session?.access_token || d?.props?.pageProps?.session?.accessToken || '';
            }
          } catch {}
          return '';
        })()`,
        returnByValue: true,
      },
      { sessionId, timeoutMs: 10_000 },
    );
    const token = result?.result?.value;
    if (typeof token === 'string' && token.startsWith('ya29.')) {
      if (verbose) logger.debug('Access token extracted from __NEXT_DATA__');
      return token;
    }
  } catch (e) {
    if (verbose) logger.debug(`__NEXT_DATA__ extraction failed: ${e instanceof Error ? e.message : String(e)}`);
  }

  // Fallback: call /fx/api/auth/session via page fetch
  try {
    const result = await cdp.send<{ result: { value?: string } }>(
      'Runtime.evaluate',
      {
        expression: `fetch('https://labs.google/fx/api/auth/session', { credentials: 'include' }).then(r => r.json()).then(d => d.access_token || d.accessToken || '')`,
        awaitPromise: true,
        returnByValue: true,
      },
      { sessionId, timeoutMs: 15_000 },
    );
    const token = result?.result?.value;
    if (typeof token === 'string' && token.startsWith('ya29.')) {
      if (verbose) logger.debug('Access token extracted from /fx/api/auth/session');
      return token;
    }
  } catch (e) {
    if (verbose) logger.debug(`/fx/api/auth/session fallback failed: ${e instanceof Error ? e.message : String(e)}`);
  }

  return null;
}

/**
 * Connect to a Chrome CDP instance, navigate to Flow, and extract auth.
 * The helper will start Chrome if the debug port is not already available.
 */
async function fetch_flow_auth_via_cdp(
  timeoutMs: number,
  verbose: boolean,
): Promise<FlowAuthResult> {
  const port = get_cdp_port();

  // Ensure Chrome is running
  await ensure_chrome_cdp(verbose);

  const wsUrl = await wait_for_chrome_debug_port(port, 30_000);
  const cdp = await CdpConnection.connect(wsUrl, 15_000);

  try {
    // Try to find an existing Flow tab first, else create a new one
    let targetId: string;
    let ownsTarget = false;

    try {
      const targets = await cdp.send<{ targetInfos: Array<{ targetId: string; url: string; type: string }> }>('Target.getTargets');
      const flowTab = targets.targetInfos.find(t => t.type === 'page' && t.url.includes('labs.google/fx'));
      if (flowTab) {
        targetId = flowTab.targetId;
        if (verbose) logger.debug(`Reusing existing Flow tab: ${flowTab.url}`);
      } else {
        const res = await cdp.send<{ targetId: string }>('Target.createTarget', {
          url: 'https://labs.google/fx/',
          newWindow: false,
        });
        targetId = res.targetId;
        ownsTarget = true;
      }
    } catch {
      const res = await cdp.send<{ targetId: string }>('Target.createTarget', {
        url: 'https://labs.google/fx/',
        newWindow: false,
      });
      targetId = res.targetId;
      ownsTarget = true;
    }

    const { sessionId } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', { targetId, flatten: true });
    await cdp.send('Network.enable', {}, { sessionId });
    await cdp.send('Runtime.enable', {}, { sessionId });

    if (verbose) {
      logger.info('Connected to Chrome CDP. Navigating to labs.google/fx/ for auth...');
    }

    const start = Date.now();

    while (Date.now() - start < timeoutMs) {
      await sleep(2000);

      // Grab cookies
      const { cookies } = await cdp.send<{ cookies: Array<{ name: string; value: string }> }>(
        'Network.getCookies',
        { urls: ['https://labs.google/', 'https://labs.google/fx/', 'https://accounts.google.com/'] },
        { sessionId, timeoutMs: 10_000 },
      );

      const m: CookieMap = {};
      for (const c of cookies) {
        if (c?.name && typeof c.value === 'string') m[c.name] = c.value;
      }

      // Try to extract access token
      const token = await extract_flow_token(cdp, sessionId, verbose);
      if (token) {
        // Only close the tab if we created it
        if (ownsTarget) {
          try {
            await cdp.send('Target.closeTarget', { targetId }, { timeoutMs: 5_000 });
          } catch {}
        }
        return { accessToken: token, cookies: m };
      }

      if (verbose) logger.debug('No valid access token yet, retrying...');
    }

    // Clean up tab on timeout (only if we created it)
    if (ownsTarget) {
      try {
        await cdp.send('Target.closeTarget', { targetId }, { timeoutMs: 5_000 });
      } catch {}
    }
    throw new Error('Timed out waiting for a valid Flow session with access token.');
  } finally {
    // Only close the WebSocket — do NOT close the browser
    cdp.close();
  }
}

export async function load_browser_auth(verbose: boolean = true): Promise<FlowAuthResult> {
  const result = await fetch_flow_auth_via_cdp(120_000, verbose);

  const filtered: CookieMap = {};
  for (const [k, v] of Object.entries(result.cookies)) {
    if (typeof v === 'string' && v.length > 0) filtered[k] = v;
  }

  await write_cookie_file(result.accessToken, filtered, resolveFlowWebCookiePath(), 'cdp');
  return { accessToken: result.accessToken, cookies: filtered };
}

export const loadBrowserAuth = load_browser_auth;
export { get_cdp_port, wait_for_chrome_debug_port, ensure_chrome_cdp };
