export const USER_AGENT = "check-ai-credits/0.1 (+https://github.com/mfang0126/check-ai-credits)";

export type HttpResult = [status: number, body: unknown];

/** GET a URL and parse JSON. Never throws on HTTP status; network errors -> [0, "Err: msg"]. */
export async function httpJson(
  url: string,
  headers: Record<string, string> = {},
  timeoutMs = 25_000,
): Promise<HttpResult> {
  try {
    const res = await fetch(url, {
      headers: { Accept: "application/json", "User-Agent": USER_AGENT, ...headers },
      signal: AbortSignal.timeout(timeoutMs),
    });
    const text = await res.text();
    try {
      return [res.status, JSON.parse(text) as unknown];
    } catch {
      return [res.status, text];
    }
  } catch (err) {
    const e = err as Error;
    return [0, `${e.name}: ${e.message}`];
  }
}
