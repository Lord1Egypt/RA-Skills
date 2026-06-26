/**
 * Async Utilities
 * 
 * Common async patterns and utilities for the AlephNet codebase.
 * Includes retry logic, timeouts, debouncing, and more.
 */

// ═══════════════════════════════════════════════════════════════════════════
// RETRY LOGIC
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Retry configuration
 */
export interface RetryConfig {
  maxAttempts: number;
  baseDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
  jitterFactor: number;
  retryOn?: (error: Error) => boolean;
}

/**
 * Default retry configuration
 */
export const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxAttempts: 3,
  baseDelayMs: 1000,
  maxDelayMs: 30000,
  backoffMultiplier: 2,
  jitterFactor: 0.1
};

/**
 * Calculate delay for a retry attempt with exponential backoff and jitter
 */
export function calculateRetryDelay(attempt: number, config: RetryConfig): number {
  const baseDelay = config.baseDelayMs * Math.pow(config.backoffMultiplier, attempt - 1);
  const cappedDelay = Math.min(baseDelay, config.maxDelayMs);
  const jitter = cappedDelay * config.jitterFactor * (Math.random() - 0.5);
  return Math.max(0, cappedDelay + jitter);
}

/**
 * Execute an async operation with retry logic
 */
export async function withRetry<T>(
  operation: () => Promise<T>,
  config: Partial<RetryConfig> = {},
  onRetry?: (attempt: number, error: Error, delay: number) => void
): Promise<T> {
  const fullConfig: RetryConfig = { ...DEFAULT_RETRY_CONFIG, ...config };
  let lastError: Error | null = null;
  
  for (let attempt = 1; attempt <= fullConfig.maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error as Error;
      
      // Check if we should retry this error
      if (fullConfig.retryOn && !fullConfig.retryOn(lastError)) {
        throw lastError;
      }
      
      if (attempt < fullConfig.maxAttempts) {
        const delay = calculateRetryDelay(attempt, fullConfig);
        onRetry?.(attempt, lastError, delay);
        await sleep(delay);
      }
    }
  }
  
  throw lastError;
}

// ═══════════════════════════════════════════════════════════════════════════
// TIMEOUT
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Timeout error
 */
export class TimeoutError extends Error {
  constructor(message: string = 'Operation timed out') {
    super(message);
    this.name = 'TimeoutError';
  }
}

/**
 * Execute an async operation with a timeout
 */
export async function withTimeout<T>(
  operation: Promise<T>,
  timeoutMs: number,
  message?: string
): Promise<T> {
  let timeoutId: NodeJS.Timeout;
  
  const timeoutPromise = new Promise<never>((_, reject) => {
    timeoutId = setTimeout(() => {
      reject(new TimeoutError(message || `Operation timed out after ${timeoutMs}ms`));
    }, timeoutMs);
  });
  
  try {
    return await Promise.race([operation, timeoutPromise]);
  } finally {
    clearTimeout(timeoutId!);
  }
}

/**
 * Create a timeout promise
 */
export function timeout(ms: number, message?: string): Promise<never> {
  return new Promise((_, reject) => {
    setTimeout(() => {
      reject(new TimeoutError(message || `Timeout after ${ms}ms`));
    }, ms);
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLEEP & DELAY
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Sleep for a specified duration
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Create a cancellable sleep
 */
export function cancellableSleep(ms: number): { promise: Promise<void>; cancel: () => void } {
  let timeoutId: NodeJS.Timeout;
  let rejectFn: (reason?: Error) => void;
  
  const promise = new Promise<void>((resolve, reject) => {
    rejectFn = reject;
    timeoutId = setTimeout(resolve, ms);
  });
  
  return {
    promise,
    cancel: () => {
      clearTimeout(timeoutId);
      rejectFn(new Error('Sleep cancelled'));
    }
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// DEBOUNCE & THROTTLE
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Debounce a function
 */
export function debounce<T extends (...args: unknown[]) => unknown>(
  fn: T,
  waitMs: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout | null = null;
  
  return (...args: Parameters<T>) => {
    if (timeoutId) clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      fn(...args);
      timeoutId = null;
    }, waitMs);
  };
}

/**
 * Debounce an async function, returning a promise
 */
export function debounceAsync<T extends (...args: unknown[]) => Promise<unknown>>(
  fn: T,
  waitMs: number
): (...args: Parameters<T>) => Promise<ReturnType<T>> {
  let timeoutId: NodeJS.Timeout | null = null;
  let pendingResolve: ((value: ReturnType<T>) => void) | null = null;
  let pendingReject: ((error: Error) => void) | null = null;
  
  return (...args: Parameters<T>): Promise<ReturnType<T>> => {
    return new Promise((resolve, reject) => {
      if (timeoutId) clearTimeout(timeoutId);
      
      pendingResolve = resolve;
      pendingReject = reject;
      
      timeoutId = setTimeout(async () => {
        try {
          const result = await fn(...args);
          pendingResolve!(result as ReturnType<T>);
        } catch (error) {
          pendingReject!(error as Error);
        }
        timeoutId = null;
      }, waitMs);
    });
  };
}

/**
 * Throttle a function
 */
export function throttle<T extends (...args: unknown[]) => unknown>(
  fn: T,
  limitMs: number
): (...args: Parameters<T>) => void {
  let lastRun = 0;
  let timeoutId: NodeJS.Timeout | null = null;
  
  return (...args: Parameters<T>) => {
    const now = Date.now();
    
    if (now - lastRun >= limitMs) {
      fn(...args);
      lastRun = now;
    } else if (!timeoutId) {
      timeoutId = setTimeout(() => {
        fn(...args);
        lastRun = Date.now();
        timeoutId = null;
      }, limitMs - (now - lastRun));
    }
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// BATCH & QUEUE
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Batch processor configuration
 */
export interface BatchConfig {
  maxBatchSize: number;
  maxWaitMs: number;
}

/**
 * Create a batch processor that accumulates items and processes them together
 */
export function createBatchProcessor<T, R>(
  processor: (items: T[]) => Promise<R[]>,
  config: BatchConfig
): (item: T) => Promise<R> {
  const queue: Array<{
    item: T;
    resolve: (result: R) => void;
    reject: (error: Error) => void;
  }> = [];
  
  let timeoutId: NodeJS.Timeout | null = null;
  
  const flush = async () => {
    if (queue.length === 0) return;
    
    const batch = queue.splice(0, config.maxBatchSize);
    const items = batch.map(b => b.item);
    
    try {
      const results = await processor(items);
      batch.forEach((b, i) => b.resolve(results[i]));
    } catch (error) {
      batch.forEach(b => b.reject(error as Error));
    }
    
    // Process remaining items
    if (queue.length > 0) {
      scheduleFlush();
    }
  };
  
  const scheduleFlush = () => {
    if (timeoutId) clearTimeout(timeoutId);
    timeoutId = setTimeout(flush, config.maxWaitMs);
  };
  
  return (item: T): Promise<R> => {
    return new Promise((resolve, reject) => {
      queue.push({ item, resolve, reject });
      
      if (queue.length >= config.maxBatchSize) {
        if (timeoutId) clearTimeout(timeoutId);
        flush();
      } else {
        scheduleFlush();
      }
    });
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// CONCURRENCY CONTROL
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Create a semaphore for limiting concurrent operations
 */
export function createSemaphore(limit: number): {
  acquire: () => Promise<void>;
  release: () => void;
  available: () => number;
} {
  let current = 0;
  const waiting: Array<() => void> = [];
  
  return {
    acquire: () => {
      if (current < limit) {
        current++;
        return Promise.resolve();
      }
      return new Promise<void>(resolve => {
        waiting.push(resolve);
      });
    },
    release: () => {
      current--;
      if (waiting.length > 0) {
        current++;
        const next = waiting.shift()!;
        next();
      }
    },
    available: () => limit - current
  };
}

/**
 * Execute async operations with concurrency limit
 */
export async function mapWithConcurrency<T, R>(
  items: T[],
  fn: (item: T, index: number) => Promise<R>,
  concurrency: number
): Promise<R[]> {
  const semaphore = createSemaphore(concurrency);
  
  return Promise.all(
    items.map(async (item, index) => {
      await semaphore.acquire();
      try {
        return await fn(item, index);
      } finally {
        semaphore.release();
      }
    })
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// DEFERRED
// ═══════════════════════════════════════════════════════════════════════════

/**
 * A deferred promise that can be resolved/rejected externally
 */
export interface Deferred<T> {
  promise: Promise<T>;
  resolve: (value: T) => void;
  reject: (error: Error) => void;
  isPending: () => boolean;
}

/**
 * Create a deferred promise
 */
export function deferred<T>(): Deferred<T> {
  let resolve!: (value: T) => void;
  let reject!: (error: Error) => void;
  let pending = true;
  
  const promise = new Promise<T>((res, rej) => {
    resolve = (value: T) => {
      pending = false;
      res(value);
    };
    reject = (error: Error) => {
      pending = false;
      rej(error);
    };
  });
  
  return {
    promise,
    resolve,
    reject,
    isPending: () => pending
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// MUTEX / LOCK
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Simple async mutex for exclusive access
 */
export class Mutex {
  private locked = false;
  private waiting: Array<() => void> = [];
  
  async acquire(): Promise<void> {
    if (!this.locked) {
      this.locked = true;
      return;
    }
    
    return new Promise<void>(resolve => {
      this.waiting.push(resolve);
    });
  }
  
  release(): void {
    if (this.waiting.length > 0) {
      const next = this.waiting.shift()!;
      next();
    } else {
      this.locked = false;
    }
  }
  
  async runExclusive<T>(fn: () => Promise<T>): Promise<T> {
    await this.acquire();
    try {
      return await fn();
    } finally {
      this.release();
    }
  }
  
  isLocked(): boolean {
    return this.locked;
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// PERIODIC EXECUTION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Execute a function periodically with proper cleanup
 */
export function createInterval(
  fn: () => void | Promise<void>,
  intervalMs: number,
  options?: { immediate?: boolean }
): { start: () => void; stop: () => void; isRunning: () => boolean } {
  let intervalId: NodeJS.Timeout | null = null;
  let running = false;
  
  return {
    start: () => {
      if (running) return;
      running = true;
      
      if (options?.immediate) {
        fn();
      }
      
      intervalId = setInterval(fn, intervalMs);
    },
    stop: () => {
      if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
      }
      running = false;
    },
    isRunning: () => running
  };
}
