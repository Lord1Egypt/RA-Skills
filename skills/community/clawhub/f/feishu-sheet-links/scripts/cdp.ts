import { spawn, type ChildProcess } from "node:child_process";
import fs from "node:fs";
import { mkdir } from "node:fs/promises";
import net from "node:net";
import os from "node:os";
import path from "node:path";
import process from "node:process";

// Chrome profile stored independently of baoyu-url-to-markdown
export function getChromeProfileDir(): string {
  const override = process.env.FEISHU_CHROME_PROFILE?.trim();
  if (override) return path.resolve(override);
  const base =
    process.platform === "darwin"
      ? path.join(os.homedir(), "Library", "Application Support")
      : process.env.XDG_DATA_HOME ?? path.join(os.homedir(), ".local", "share");
  return path.join(base, "feishu-sheet-links", "chrome-profile");
}

export function findChrome(): string {
  const override = process.env.FEISHU_CHROME_PATH?.trim();
  if (override && fs.existsSync(override)) return override;
  const candidates =
    process.platform === "darwin"
      ? [
          "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
          "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
          "/Applications/Chromium.app/Contents/MacOS/Chromium",
          "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        ]
      : process.platform === "win32"
      ? [
          "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
          "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        ]
      : ["/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"];
  for (const p of candidates) {
    if (fs.existsSync(p)) return p;
  }
  throw new Error("Chrome not found. Set FEISHU_CHROME_PATH env var.");
}

export async function getFreePort(): Promise<number> {
  return new Promise((resolve, reject) => {
    const srv = net.createServer();
    srv.unref();
    srv.on("error", reject);
    srv.listen(0, "127.0.0.1", () => {
      const addr = srv.address() as net.AddressInfo;
      srv.close((err) => (err ? reject(err) : resolve(addr.port)));
    });
  });
}

export async function launchChrome(url: string, port: number): Promise<ChildProcess> {
  const profileDir = getChromeProfileDir();
  await mkdir(profileDir, { recursive: true });
  const chrome = findChrome();
  return spawn(
    chrome,
    [
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${profileDir}`,
      "--no-first-run",
      "--no-default-browser-check",
      "--disable-popup-blocking",
      url,
    ],
    { stdio: "ignore" }
  );
}

export function killChrome(chrome: ChildProcess): void {
  try { chrome.kill("SIGTERM"); } catch {}
  setTimeout(() => {
    if (!chrome.killed) { try { chrome.kill("SIGKILL"); } catch {} }
  }, 2_000).unref?.();
}

async function fetchJson<T>(url: string, timeoutMs = 5_000): Promise<T | null> {
  try {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), timeoutMs);
    const res = await fetch(url, { signal: ctl.signal });
    clearTimeout(t);
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

export async function waitForDebugPort(port: number, timeoutMs = 30_000): Promise<string> {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const info = await fetchJson<{ webSocketDebuggerUrl?: string }>(
      `http://127.0.0.1:${port}/json/version`
    );
    if (info?.webSocketDebuggerUrl) return info.webSocketDebuggerUrl;
    await new Promise((r) => setTimeout(r, 300));
  }
  throw new Error(`Chrome debug port ${port} not ready after ${timeoutMs}ms`);
}

// Try connecting to an already-running Chrome on known ports
export async function findExistingChrome(
  ports = [64023, 9222, 9229]
): Promise<string | null> {
  for (const port of ports) {
    const info = await fetchJson<{ webSocketDebuggerUrl?: string }>(
      `http://127.0.0.1:${port}/json/version`,
      2_000
    );
    if (info?.webSocketDebuggerUrl) {
      return info.webSocketDebuggerUrl;
    }
  }
  return null;
}

// Minimal CDP connection
export class CdpSession {
  private ws: WebSocket;
  private nextId = 0;
  private pending = new Map<
    number,
    { resolve: (v: unknown) => void; reject: (e: Error) => void; timer: ReturnType<typeof setTimeout> | null }
  >();

  private constructor(ws: WebSocket) {
    this.ws = ws;
    this.ws.addEventListener("message", (event) => {
      try {
        const msg = JSON.parse(
          typeof event.data === "string" ? event.data : new TextDecoder().decode(event.data as ArrayBuffer)
        ) as { id?: number; result?: unknown; error?: { message?: string }; sessionId?: string };
        if (msg.id != null) {
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
    this.ws.addEventListener("close", () => {
      for (const [id, p] of this.pending.entries()) {
        this.pending.delete(id);
        if (p.timer) clearTimeout(p.timer);
        p.reject(new Error("CDP connection closed"));
      }
    });
  }

  static async connect(wsUrl: string, timeoutMs = 10_000): Promise<CdpSession> {
    const ws = new WebSocket(wsUrl);
    await new Promise<void>((resolve, reject) => {
      const t = setTimeout(() => reject(new Error("CDP connect timeout")), timeoutMs);
      ws.addEventListener("open", () => { clearTimeout(t); resolve(); });
      ws.addEventListener("error", () => { clearTimeout(t); reject(new Error("CDP connect failed")); });
    });
    return new CdpSession(ws);
  }

  async send<T = unknown>(
    method: string,
    params: Record<string, unknown> = {},
    opts: { sessionId?: string; timeoutMs?: number } = {}
  ): Promise<T> {
    const id = ++this.nextId;
    const msg: Record<string, unknown> = { id, method, params };
    if (opts.sessionId) msg.sessionId = opts.sessionId;
    const timeoutMs = opts.timeoutMs ?? 20_000;
    const result = await new Promise<unknown>((resolve, reject) => {
      const t = timeoutMs > 0
        ? setTimeout(() => { this.pending.delete(id); reject(new Error(`CDP timeout: ${method}`)); }, timeoutMs)
        : null;
      this.pending.set(id, { resolve, reject, timer: t });
      this.ws.send(JSON.stringify(msg));
    });
    return result as T;
  }

  close(): void {
    try { this.ws.close(); } catch {}
  }
}

export async function evaluate<T>(
  cdp: CdpSession,
  sessionId: string,
  expression: string,
  timeoutMs = 20_000
): Promise<T | null> {
  const result = await cdp.send<{ result: { value?: T } }>(
    "Runtime.evaluate",
    { expression, returnByValue: true, awaitPromise: true },
    { sessionId, timeoutMs }
  );
  return (result.result.value ?? null) as T | null;
}
