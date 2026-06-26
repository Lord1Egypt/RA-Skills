type ScopeState = {
  queue: Promise<void>;
  nextAllowedAt: number;
};

type FetchWithRetryInput = {
  scope: string;
  url: string;
  init: RequestInit;
  timeoutMs: number;
  maxAttempts: number;
  baseDelayMs: number;
  maxDelayMs: number;
  minIntervalMs: number;
  label: string;
  onEvent?: (event: ZhipuHttpProgressEvent) => void;
};

export type ZhipuHttpProgressEvent = {
  source: "zhipu-http";
  event: "http.retry_scheduled" | "http.cooldown_wait" | "http.retry_exhausted";
  stage: "zhipu_http";
  status: "retrying" | "waiting" | "failed";
  scope: string;
  label: string;
  attempt: number;
  max_attempts: number;
  delay_ms: number;
  status_code: number | null;
  retry_after_ms: number | null;
  message: string;
};

const scopeStates = new Map<string, ScopeState>();

function sleep(ms: number): Promise<void> {
  if (ms <= 0) {
    return Promise.resolve();
  }
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function getScopeState(scope: string): ScopeState {
  const existing = scopeStates.get(scope);
  if (existing) {
    return existing;
  }

  const created: ScopeState = {
    queue: Promise.resolve(),
    nextAllowedAt: 0
  };
  scopeStates.set(scope, created);
  return created;
}

async function withScopeThrottle<T>(
  scope: string,
  task: (state: ScopeState) => Promise<T>
): Promise<T> {
  const state = getScopeState(scope);
  const previous = state.queue;
  let release: (() => void) | undefined;
  const current = new Promise<void>((resolve) => {
    release = resolve;
  });
  state.queue = current;

  await previous;

  try {
    return await task(state);
  } finally {
    release?.();
  }
}

function parseRetryAfterMs(headers: Headers): number | null {
  const rawValue = headers.get("retry-after");
  if (!rawValue) {
    return null;
  }

  const seconds = Number.parseInt(rawValue, 10);
  if (Number.isFinite(seconds) && seconds >= 0) {
    return seconds * 1000;
  }

  const retryDate = Date.parse(rawValue);
  if (!Number.isNaN(retryDate)) {
    return Math.max(0, retryDate - Date.now());
  }

  return null;
}

function computeBackoffDelayMs(input: {
  attempt: number;
  baseDelayMs: number;
  maxDelayMs: number;
  retryAfterMs: number | null;
}): number {
  if (input.retryAfterMs !== null && input.retryAfterMs >= 0) {
    return Math.min(input.maxDelayMs, input.retryAfterMs);
  }

  const cappedAttempt = Math.max(0, input.attempt - 1);
  const exponential = Math.min(
    input.maxDelayMs,
    input.baseDelayMs * 2 ** cappedAttempt
  );
  const jitter = Math.floor(exponential * 0.25 * Math.random());
  return Math.min(input.maxDelayMs, exponential + jitter);
}

function isRetryableStatus(status: number): boolean {
  return status === 429 || status >= 500;
}

function isRetryableTransportError(error: unknown): error is Error {
  if (!(error instanceof Error)) {
    return false;
  }
  return (
    error.name === "TimeoutError" ||
    error.name === "AbortError" ||
    typeof (error as Error & { code?: string }).code === "string" ||
    error.cause !== undefined
  );
}

function buildResponseErrorMessage(input: {
  label: string;
  status: number;
  rawText: string;
}): string {
  const trimmed = input.rawText.trim();
  if (!trimmed) {
    return `${input.label} failed (${input.status}).`;
  }

  const collapsed = trimmed.replace(/\s+/gu, " ").trim();
  const detail =
    collapsed.length <= 400 ? collapsed : `${collapsed.slice(0, 397)}...`;
  return `${input.label} failed (${input.status}): ${detail}`;
}

function normalizeIntegerEnv(name: string, fallback: number): number {
  const parsed = Number.parseInt(process.env[name]?.trim() ?? "", 10);
  if (!Number.isFinite(parsed) || parsed < 0) {
    return fallback;
  }
  return parsed;
}

export function getZhipuHttpRetryConfig() {
  const maxAttempts = normalizeIntegerEnv("CAIXU_ZHIPU_HTTP_MAX_ATTEMPTS", 4);
  const baseDelayMs = normalizeIntegerEnv("CAIXU_ZHIPU_HTTP_BASE_DELAY_MS", 2_000);
  const maxDelayMs = normalizeIntegerEnv("CAIXU_ZHIPU_HTTP_MAX_DELAY_MS", 20_000);
  const minIntervalMs = normalizeIntegerEnv("CAIXU_ZHIPU_MIN_INTERVAL_MS", 1_500);

  return {
    maxAttempts: Math.max(1, maxAttempts),
    baseDelayMs,
    maxDelayMs: Math.max(baseDelayMs, maxDelayMs),
    minIntervalMs
  };
}

export async function fetchWithZhipuRetry(
  input: FetchWithRetryInput
): Promise<Response> {
  let lastError: Error | null = null;
  let lastStatusCode: number | null = null;
  let lastRetryAfterMs: number | null = null;
  let lastDelayMs = 0;

  for (let attempt = 1; attempt <= input.maxAttempts; attempt += 1) {
    const result = await withScopeThrottle(input.scope, async (state) => {
      const waitMs = Math.max(0, state.nextAllowedAt - Date.now());
      if (waitMs > 0) {
        input.onEvent?.({
          source: "zhipu-http",
          event: "http.cooldown_wait",
          stage: "zhipu_http",
          status: "waiting",
          scope: input.scope,
          label: input.label,
          attempt,
          max_attempts: input.maxAttempts,
          delay_ms: waitMs,
          status_code: null,
          retry_after_ms: null,
          message: `Waiting ${waitMs}ms before retrying ${input.label}.`
        });
      }
      await sleep(waitMs);

      let response: Response;
      try {
        response = await fetch(input.url, {
          ...input.init,
          signal:
            typeof AbortSignal !== "undefined"
              ? AbortSignal.timeout(input.timeoutMs)
              : input.init.signal
        });
      } catch (error) {
        if (!isRetryableTransportError(error)) {
          return {
            kind: "transport-error" as const,
            retryable: false,
            error:
              error instanceof Error
                ? error
                : new Error(`${input.label} request failed.`)
          };
        }

        const shouldRetry = attempt < input.maxAttempts;
        const delayMs = computeBackoffDelayMs({
          attempt,
          baseDelayMs: input.baseDelayMs,
          maxDelayMs: input.maxDelayMs,
          retryAfterMs: null
        });
        lastStatusCode = null;
        lastRetryAfterMs = null;
        lastDelayMs = delayMs;
        if (shouldRetry) {
          state.nextAllowedAt = Math.max(
            state.nextAllowedAt,
            Date.now() + Math.max(delayMs, input.minIntervalMs)
          );
          input.onEvent?.({
            source: "zhipu-http",
            event: "http.retry_scheduled",
            stage: "zhipu_http",
            status: "retrying",
            scope: input.scope,
            label: input.label,
            attempt,
            max_attempts: input.maxAttempts,
            delay_ms: delayMs,
            status_code: null,
            retry_after_ms: null,
            message: `Retry scheduled for ${input.label} after transport error.`
          });
          input.onEvent?.({
            source: "zhipu-http",
            event: "http.cooldown_wait",
            stage: "zhipu_http",
            status: "waiting",
            scope: input.scope,
            label: input.label,
            attempt,
            max_attempts: input.maxAttempts,
            delay_ms: delayMs,
            status_code: null,
            retry_after_ms: null,
            message: `Cooldown wait ${delayMs}ms before retrying ${input.label}.`
          });
        }
        return {
          kind: "transport-error" as const,
          retryable: true,
          error:
            error instanceof Error
              ? error
              : new Error(`${input.label} request failed.`)
        };
      }

      if (response.ok) {
        state.nextAllowedAt = Math.max(
          state.nextAllowedAt,
          Date.now() + input.minIntervalMs
        );
        return {
          kind: "success" as const,
          response
        };
      }

      const rawText = await response.text();
      const retryable = isRetryableStatus(response.status);
      const retryAfterMs = parseRetryAfterMs(response.headers);
      const delayMs = retryable
        ? computeBackoffDelayMs({
            attempt,
            baseDelayMs: input.baseDelayMs,
            maxDelayMs: input.maxDelayMs,
            retryAfterMs
          })
        : 0;
      const shouldRetry = retryable && attempt < input.maxAttempts;

      if (retryable) {
        lastStatusCode = response.status;
        lastRetryAfterMs = retryAfterMs;
        lastDelayMs = delayMs;
        if (shouldRetry) {
          state.nextAllowedAt = Math.max(
            state.nextAllowedAt,
            Date.now() + Math.max(delayMs, input.minIntervalMs)
          );
          input.onEvent?.({
            source: "zhipu-http",
            event: "http.retry_scheduled",
            stage: "zhipu_http",
            status: "retrying",
            scope: input.scope,
            label: input.label,
            attempt,
            max_attempts: input.maxAttempts,
            delay_ms: delayMs,
            status_code: response.status,
            retry_after_ms: retryAfterMs,
            message: `Retry scheduled for ${input.label} after HTTP ${response.status}.`
          });
          input.onEvent?.({
            source: "zhipu-http",
            event: "http.cooldown_wait",
            stage: "zhipu_http",
            status: "waiting",
            scope: input.scope,
            label: input.label,
            attempt,
            max_attempts: input.maxAttempts,
            delay_ms: delayMs,
            status_code: response.status,
            retry_after_ms: retryAfterMs,
            message: `Cooldown wait ${delayMs}ms before retrying ${input.label}.`
          });
        }
      } else {
        state.nextAllowedAt = Math.max(
          state.nextAllowedAt,
          Date.now() + input.minIntervalMs
        );
      }

      return {
        kind: "http-error" as const,
        retryable,
        error: new Error(
          buildResponseErrorMessage({
            label: input.label,
            status: response.status,
            rawText
          })
        )
      };
    });

    if (result.kind === "success") {
      return result.response;
    }

    lastError = result.error;
    if (!result.retryable || attempt >= input.maxAttempts) {
      input.onEvent?.({
        source: "zhipu-http",
        event: "http.retry_exhausted",
        stage: "zhipu_http",
        status: "failed",
        scope: input.scope,
        label: input.label,
        attempt,
        max_attempts: input.maxAttempts,
        delay_ms: lastDelayMs,
        status_code: lastStatusCode,
        retry_after_ms: lastRetryAfterMs,
        message: lastError.message
      });
      throw lastError;
    }
  }

  throw lastError ?? new Error(`${input.label} failed without a detailed error.`);
}
