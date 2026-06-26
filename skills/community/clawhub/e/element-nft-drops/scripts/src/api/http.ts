import { DEFAULT_NETWORK_TIMEOUT_MS } from "../config";

function summarizeForLog(value: unknown): unknown {
  if (typeof value === "string") {
    return value.length > 4000 ? `${value.slice(0, 4000)}...<truncated>` : value;
  }
  if (Array.isArray(value)) {
    return value.map((item) => summarizeForLog(item));
  }
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value).map(([key, nested]) => [key, summarizeForLog(nested)])
    );
  }
  return value;
}

const DEFAULT_HTTP_TIMEOUT_MS = DEFAULT_NETWORK_TIMEOUT_MS;
const DEFAULT_HTTP_MAX_ATTEMPTS = 3;
const DEFAULT_HTTP_RETRY_DELAY_MS = 1_500;

export class HttpRequestError extends Error {
  readonly method: string;
  readonly url: string;
  readonly status?: number;
  readonly attempts: number;
  readonly maxAttempts: number;
  readonly durationMs: number;
  readonly timedOut: boolean;
  readonly retriable: boolean;
  readonly responseBody?: unknown;

  constructor(input: {
    method: string;
    url: string;
    status?: number;
    attempts: number;
    maxAttempts: number;
    durationMs: number;
    timedOut: boolean;
    retriable: boolean;
    responseBody?: unknown;
    message: string;
    cause?: unknown;
  }) {
    super(input.message, input.cause ? { cause: input.cause } : undefined);
    this.name = "HttpRequestError";
    this.method = input.method;
    this.url = input.url;
    this.status = input.status;
    this.attempts = input.attempts;
    this.maxAttempts = input.maxAttempts;
    this.durationMs = input.durationMs;
    this.timedOut = input.timedOut;
    this.retriable = input.retriable;
    this.responseBody = input.responseBody;
  }
}

function summarizeForMessage(value: unknown): string {
  if (typeof value === "string") {
    return value.length > 500 ? `${value.slice(0, 500)}...<truncated>` : value;
  }
  try {
    return JSON.stringify(summarizeForLog(value));
  } catch {
    return String(value);
  }
}

function logExternalFailure(input: {
  method: string;
  url: string;
  status?: number;
  body?: unknown;
  attempt?: number;
  maxAttempts?: number;
  durationMs?: number;
  timedOut?: boolean;
  retriable?: boolean;
  error?: string;
}) {
  console.error(
    `[element-drop] external response ${JSON.stringify({
      method: input.method,
      url: input.url,
      status: input.status,
      attempt: input.attempt,
      maxAttempts: input.maxAttempts,
      durationMs: input.durationMs,
      timedOut: input.timedOut,
      retriable: input.retriable,
      error: input.error,
      body: summarizeForLog(input.body)
    })}`
  );
}

function isRetryableStatus(status: number): boolean {
  return status === 408 || status === 425 || status === 429 || status >= 500;
}

function shouldRetry(input: { status?: number; timedOut: boolean; error?: unknown }): boolean {
  if (input.timedOut) {
    return true;
  }
  if (typeof input.status === "number") {
    return isRetryableStatus(input.status);
  }
  if (!input.error) {
    return false;
  }
  if (input.error instanceof TypeError) {
    return true;
  }
  if (input.error instanceof Error && input.error.name === "AbortError") {
    return true;
  }
  return false;
}

async function sleep(ms: number): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

async function parseResponseBody(response: Response): Promise<unknown> {
  let body: unknown;
  try {
    body = await response.json();
  } catch {
    body = await response.text();
  }
  return body;
}

async function requestJson<T>(
  url: string,
  init: {
    method: "GET" | "POST";
    headers?: Record<string, string>;
    body?: string;
    timeoutMs?: number;
    maxAttempts?: number;
    retryDelayMs?: number;
  }
): Promise<T> {
  const timeoutMs = init.timeoutMs ?? DEFAULT_HTTP_TIMEOUT_MS;
  const maxAttempts = Math.max(1, init.maxAttempts ?? DEFAULT_HTTP_MAX_ATTEMPTS);
  const retryDelayMs = init.retryDelayMs ?? DEFAULT_HTTP_RETRY_DELAY_MS;
  const startedAt = Date.now();
  let attempt = 0;
  let lastFailure: HttpRequestError | undefined;

  while (attempt < maxAttempts) {
    attempt += 1;
    const controller = new AbortController();
    const timeoutHandle = setTimeout(() => controller.abort(), timeoutMs);
    const attemptStartedAt = Date.now();

    try {
      const response = await fetch(url, {
        method: init.method,
        headers: init.headers,
        body: init.body,
        signal: controller.signal
      });
      clearTimeout(timeoutHandle);
      const body = await parseResponseBody(response);
      if (response.ok) {
        return body as T;
      }

      const retriable = shouldRetry({ status: response.status, timedOut: false });
      const error = new HttpRequestError({
        method: init.method,
        url,
        status: response.status,
        attempts: attempt,
        maxAttempts,
        durationMs: Date.now() - startedAt,
        timedOut: false,
        retriable,
        responseBody: body,
        message: `HTTP ${response.status} for ${url}: ${summarizeForMessage(body)}`
      });
      lastFailure = error;

      logExternalFailure({
        method: init.method,
        url,
        status: response.status,
        body,
        attempt,
        maxAttempts,
        durationMs: Date.now() - attemptStartedAt,
        timedOut: false,
        retriable
      });

      if (!retriable || attempt >= maxAttempts) {
        throw error;
      }
    } catch (error) {
      clearTimeout(timeoutHandle);
      const timedOut = error instanceof Error && error.name === "AbortError";
      const retriable = shouldRetry({ timedOut, error });
      const wrapped =
        error instanceof HttpRequestError
          ? error
          : new HttpRequestError({
              method: init.method,
              url,
              attempts: attempt,
              maxAttempts,
              durationMs: Date.now() - startedAt,
              timedOut,
              retriable,
              message: timedOut
                ? `HTTP timeout after ${timeoutMs}ms for ${url}`
                : `HTTP request failed for ${url}: ${error instanceof Error ? error.message : String(error)}`,
              cause: error
            });
      lastFailure = wrapped;

      if (error instanceof HttpRequestError) {
        throw error;
      }

      logExternalFailure({
        method: init.method,
        url,
        attempt,
        maxAttempts,
        durationMs: Date.now() - attemptStartedAt,
        timedOut,
        retriable,
        error: error instanceof Error ? error.message : String(error)
      });

      if (!retriable || attempt >= maxAttempts) {
        throw wrapped;
      }
    }

    await sleep(retryDelayMs * attempt);
  }

  if (lastFailure) {
    throw lastFailure;
  }

  throw new HttpRequestError({
    method: init.method,
    url,
    attempts: maxAttempts,
    maxAttempts,
    durationMs: Date.now() - startedAt,
    timedOut: false,
    retriable: false,
    message: `HTTP request failed for ${url}`
  });
}

export async function getJson<T>(
  url: string,
  init?: {
    headers?: Record<string, string>;
    timeoutMs?: number;
    maxAttempts?: number;
    retryDelayMs?: number;
  }
): Promise<T> {
  return requestJson<T>(url, {
    method: "GET",
    headers: init?.headers,
    timeoutMs: init?.timeoutMs,
    maxAttempts: init?.maxAttempts,
    retryDelayMs: init?.retryDelayMs
  });
}

export async function postJson<T>(
  url: string,
  init: {
    body: unknown;
    headers?: Record<string, string>;
    timeoutMs?: number;
    maxAttempts?: number;
    retryDelayMs?: number;
  }
): Promise<T> {
  return requestJson<T>(url, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      ...(init.headers ?? {})
    },
    body: JSON.stringify(init.body),
    timeoutMs: init.timeoutMs,
    maxAttempts: init.maxAttempts,
    retryDelayMs: init.retryDelayMs
  });
}
