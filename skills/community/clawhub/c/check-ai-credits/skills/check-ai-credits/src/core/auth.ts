/** Login URLs + auth-error detection — ported from usage-logger.py. */

export const LOGIN_URLS: Record<string, string> = {
  mimo: "https://platform.xiaomimimo.com/#/console/balance",
  kimi: "https://www.kimi.com/code/console",
  claude: "https://claude.ai",
  gemini: "https://aistudio.google.com",
  grok: "https://grok.com",
  codex: "https://chatgpt.com",
  deepseek: "https://platform.deepseek.com",
  deepinfra: "https://deepinfra.com/dash",
  openrouter: "https://openrouter.ai/settings/keys",
  apikeyfun: "https://apikey.fun",
};

/** Case-insensitive substring patterns that mean "credentials expired". */
export const AUTH_ERROR_PATTERNS: string[] = [
  "login required",
  "browser session expired",
  "auth token is invalid",
  "auth token is expired",
  "session expired",
  "api key rejected",
  "no access_token",
  "credentials missing",
  "http 401",
  "http 403",
];

/** Return the provider's login URL if the error/identity indicates expired auth. */
export function detectAuthError(item: Record<string, unknown>): string | null {
  const provider = String(item.provider ?? "");
  const err = item.error;
  if (typeof err === "string") {
    const lower = err.toLowerCase();
    for (const pattern of AUTH_ERROR_PATTERNS) {
      if (lower.includes(pattern)) return LOGIN_URLS[provider] ?? null;
    }
  }
  const usage = item.usage as Record<string, unknown> | undefined;
  const identity = usage?.identity as Record<string, unknown> | undefined;
  const loginMethod = identity?.loginMethod;
  if (
    typeof loginMethod === "string" &&
    ["expired", "invalid", "none"].includes(loginMethod)
  ) {
    return LOGIN_URLS[provider] ?? null;
  }
  return null;
}
