import process from 'node:process';

export function sleep(ms: number, signal?: AbortSignal): Promise<void> {
  return new Promise((resolve) => {
    const t = setTimeout(() => {
      if (signal) signal.removeEventListener('abort', onAbort);
      resolve();
    }, ms);

    const onAbort = () => {
      clearTimeout(t);
      if (signal) signal.removeEventListener('abort', onAbort);
      resolve();
    };

    if (signal) {
      if (signal.aborted) {
        onAbort();
      } else {
        signal.addEventListener('abort', onAbort, { once: true });
      }
    }
  });
}

export function cookie_header(cookies: Record<string, string>): string {
  return Object.entries(cookies)
    .filter(([, v]) => typeof v === 'string' && v.length > 0)
    .map(([k, v]) => `${k}=${v}`)
    .join('; ');
}

export const cookieHeader = cookie_header;

/**
 * Resolve proxy URL from env vars.
 * Priority: FLOW_WEB_PROXY > HTTPS_PROXY > HTTP_PROXY > AGENT_BROWSER_CHROME_PROXY_SERVER
 */
export function resolve_proxy(): string | null {
  const p =
    process.env.FLOW_WEB_PROXY?.trim() ||
    process.env.HTTPS_PROXY?.trim() ||
    process.env.HTTP_PROXY?.trim() ||
    process.env.https_proxy?.trim() ||
    process.env.http_proxy?.trim() ||
    process.env.AGENT_BROWSER_CHROME_PROXY_SERVER?.trim();
  return p || null;
}

export async function fetch_with_timeout(
  url: string,
  init: RequestInit & { timeout_ms?: number } = {},
): Promise<Response> {
  const { timeout_ms, ...rest } = init;

  // Apply proxy if available (Bun supports the proxy option)
  const proxy = resolve_proxy();
  const fetchOpts: any = { ...rest };
  if (proxy) fetchOpts.proxy = proxy;

  if (!timeout_ms || timeout_ms <= 0) return fetch(url, fetchOpts);

  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), timeout_ms);
  try {
    return await fetch(url, { ...fetchOpts, signal: ctl.signal });
  } finally {
    clearTimeout(t);
  }
}

export const fetchWithTimeout = fetch_with_timeout;
