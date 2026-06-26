export const DEFAULT_TIMEOUT_MS = 15_000;
export const FIXED_API_BASE = 'https://openapi.cantian.ai/rest';
export const FIXED_SUCCESS_URL_BASE = 'https://asset.cantian.ai/public';
export const SUPPORTED_REPORT_TYPES = ['LIFE', 'LOVE', 'WEALTH', 'CAREER', 'YEAR2026'] as const;
export type ReportType = (typeof SUPPORTED_REPORT_TYPES)[number];
export const SUPPORTED_CHECKOUT_TYPES = ['DEEP', 'YEAR2026'] as const;
export type CheckoutType = (typeof SUPPORTED_CHECKOUT_TYPES)[number];
export const SUPPORTED_PAGE_LOCALES = ['zh', 'en', 'ja', 'ko', 'zh-TW'] as const;
export type PageLocale = (typeof SUPPORTED_PAGE_LOCALES)[number];

export type ApiEnvelope<TData> = {
  code: number;
  message?: string;
  msg?: string;
  error?: string;
  errorMessage?: string;
  errorData?: unknown;
  data: TData;
};

export function fail(message: string): never {
  console.error(`Error: ${message}`);
  process.exit(1);
}

export function parseArgs(argv: string[]): Record<string, string> {
  const output: Record<string, string> = {};

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) {
      fail(`Unexpected token: ${token}`);
    }

    const key = token.slice(2);
    const value = argv[i + 1];
    if (!value || value.startsWith('--')) {
      fail(`Missing value for --${key}`);
    }

    output[key] = value;
    i += 1;
  }

  return output;
}

export function parseBoolean(value: string, key: string): boolean {
  if (value === 'true') {
    return true;
  }
  if (value === 'false') {
    return false;
  }

  fail(`Invalid --${key}: ${value}. Use true or false.`);
}

export function parseNumber(value: string, key: string): number {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    fail(`Invalid --${key}: ${value}. Must be a number.`);
  }

  return parsed;
}

export function parsePositiveNumber(value: string, key: string): number {
  const parsed = parseNumber(value, key);
  if (parsed <= 0) {
    fail(`Invalid --${key}: ${value}. Must be > 0.`);
  }

  return parsed;
}

export function normalizeApiBase(input: string): string {
  return input.endsWith('/') ? input.slice(0, -1) : input;
}

export function deriveReportIds(profileId: string, types: ReportType[]): string[] {
  return types.map((type) => `${profileId}_${type}`);
}

export function expandCheckoutTypeToReportTypes(checkoutType: CheckoutType): ReportType[] {
  if (checkoutType === 'YEAR2026') {
    return ['YEAR2026'];
  }
  return ['LIFE', 'LOVE', 'WEALTH', 'CAREER'];
}

export function deriveCheckoutTypeFromReportTypes(types: ReportType[]): CheckoutType {
  return types.length === 1 && types[0] === 'YEAR2026' ? 'YEAR2026' : 'DEEP';
}

export function normalizePageLocale(input: string | null | undefined): PageLocale {
  if (!input || input.trim().length === 0) {
    return 'zh';
  }

  const normalized = input.trim().replace(/_/g, '-').toLowerCase();

  if (normalized === 'zh-tw' || normalized.startsWith('zh-tw-')) {
    return 'zh-TW';
  }
  if (normalized === 'zh' || normalized === 'zh-cn' || normalized.startsWith('zh-cn-')) {
    return 'zh';
  }
  if (normalized === 'en' || normalized.startsWith('en-')) {
    return 'en';
  }
  if (normalized === 'ja' || normalized.startsWith('ja-')) {
    return 'ja';
  }
  if (normalized === 'ko' || normalized.startsWith('ko-')) {
    return 'ko';
  }

  return 'zh';
}

export function buildSuccessPageUrl(
  locale: string | null | undefined,
  checkoutType: CheckoutType,
  profileId?: string | null,
): string {
  const safeLocale = normalizePageLocale(locale);
  const base = `${FIXED_SUCCESS_URL_BASE}/${safeLocale}/report_paid.html`;
  const params = new URLSearchParams();
  params.set('type', checkoutType);
  if (profileId && profileId.trim().length > 0) {
    params.set('profileId', profileId.trim());
  }
  return `${base}?${params.toString()}`;
}

export function buildCancelPageUrl(locale: string | null | undefined): string {
  const safeLocale = normalizePageLocale(locale);
  return `${FIXED_SUCCESS_URL_BASE}/${safeLocale}/pay_cancel.html`;
}

export function extractBusinessError(responseBody: unknown): string {
  if (!responseBody || typeof responseBody !== 'object') {
    return 'unknown business error';
  }

  const candidate = responseBody as {
    message?: unknown;
    msg?: unknown;
    error?: unknown;
    errorMessage?: unknown;
    errorData?: unknown;
  };

  if (typeof candidate.errorMessage === 'string' && candidate.errorMessage.length > 0) {
    return candidate.errorMessage;
  }
  if (typeof candidate.message === 'string' && candidate.message.length > 0) {
    return candidate.message;
  }
  if (typeof candidate.msg === 'string' && candidate.msg.length > 0) {
    return candidate.msg;
  }
  if (typeof candidate.error === 'string' && candidate.error.length > 0) {
    return candidate.error;
  }
  if (candidate.errorData !== undefined) {
    return `errorData=${JSON.stringify(candidate.errorData)}`;
  }

  return 'business code is not 1';
}

export async function requestApiEnvelope<TData>(
  url: string,
  init: RequestInit,
  timeoutMs: number,
): Promise<ApiEnvelope<TData>> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      ...init,
      signal: controller.signal,
    });

    const text = await response.text();
    let parsed: unknown = null;

    if (text) {
      try {
        parsed = JSON.parse(text);
      } catch {
        fail(`API response is not valid JSON. Status=${response.status}, body=${text}`);
      }
    }

    if (!parsed || typeof parsed !== 'object') {
      fail('API returned empty or invalid JSON payload.');
    }

    if (!response.ok) {
      fail(`API request failed. Status=${response.status}, body=${text}`);
    }

    const result = parsed as ApiEnvelope<TData>;
    if (result.code !== 1) {
      fail(
        `API business error. code=${result.code}, message=${extractBusinessError(parsed)}, body=${text || JSON.stringify(parsed)}`,
      );
    }

    return result;
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      fail(`Request timeout after ${timeoutMs}ms.`);
    }

    fail(`Request failed: ${error instanceof Error ? error.message : String(error)}`);
  } finally {
    clearTimeout(timer);
  }
}
