/**
 * Result Pattern
 * 
 * A type-safe way to handle operations that can fail.
 * Inspired by Rust's Result type.
 */

// ═══════════════════════════════════════════════════════════════════════════
// RESULT TYPE
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Success result
 */
export interface Ok<T> {
  readonly ok: true;
  readonly value: T;
}

/**
 * Error result
 */
export interface Err<E> {
  readonly ok: false;
  readonly error: E;
}

/**
 * Result type - either Ok or Err
 */
export type Result<T, E = Error> = Ok<T> | Err<E>;

// ═══════════════════════════════════════════════════════════════════════════
// CONSTRUCTORS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Create a success result
 */
export function ok<T>(value: T): Ok<T> {
  return { ok: true, value };
}

/**
 * Create an error result
 */
export function err<E>(error: E): Err<E> {
  return { ok: false, error };
}

/**
 * Create a result from a value that might be null/undefined
 */
export function fromNullable<T>(
  value: T | null | undefined,
  error: Error = new Error('Value is null or undefined')
): Result<T, Error> {
  if (value === null || value === undefined) {
    return err(error);
  }
  return ok(value);
}

/**
 * Wrap a function that might throw into a Result
 */
export function tryCatch<T, E = Error>(
  fn: () => T,
  errorMapper?: (e: unknown) => E
): Result<T, E> {
  try {
    return ok(fn());
  } catch (e) {
    if (errorMapper) {
      return err(errorMapper(e));
    }
    return err(e as E);
  }
}

/**
 * Wrap an async function that might throw into a Result
 */
export async function tryCatchAsync<T, E = Error>(
  fn: () => Promise<T>,
  errorMapper?: (e: unknown) => E
): Promise<Result<T, E>> {
  try {
    const value = await fn();
    return ok(value);
  } catch (e) {
    if (errorMapper) {
      return err(errorMapper(e));
    }
    return err(e as E);
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// TYPE GUARDS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Check if result is Ok
 */
export function isOk<T, E>(result: Result<T, E>): result is Ok<T> {
  return result.ok === true;
}

/**
 * Check if result is Err
 */
export function isErr<T, E>(result: Result<T, E>): result is Err<E> {
  return result.ok === false;
}

// ═══════════════════════════════════════════════════════════════════════════
// OPERATIONS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Map the value if Ok
 */
export function map<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => U
): Result<U, E> {
  if (isOk(result)) {
    return ok(fn(result.value));
  }
  return result;
}

/**
 * Map the error if Err
 */
export function mapErr<T, E, F>(
  result: Result<T, E>,
  fn: (error: E) => F
): Result<T, F> {
  if (isErr(result)) {
    return err(fn(result.error));
  }
  return result;
}

/**
 * Chain results (flatMap)
 */
export function flatMap<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, E>
): Result<U, E> {
  if (isOk(result)) {
    return fn(result.value);
  }
  return result;
}

/**
 * Unwrap the value or throw
 */
export function unwrap<T, E>(result: Result<T, E>): T {
  if (isOk(result)) {
    return result.value;
  }
  throw result.error;
}

/**
 * Unwrap the value or return a default
 */
export function unwrapOr<T, E>(result: Result<T, E>, defaultValue: T): T {
  if (isOk(result)) {
    return result.value;
  }
  return defaultValue;
}

/**
 * Unwrap the value or compute a default
 */
export function unwrapOrElse<T, E>(
  result: Result<T, E>,
  fn: (error: E) => T
): T {
  if (isOk(result)) {
    return result.value;
  }
  return fn(result.error);
}

/**
 * Get the error or throw
 */
export function unwrapErr<T, E>(result: Result<T, E>): E {
  if (isErr(result)) {
    return result.error;
  }
  throw new Error('Called unwrapErr on Ok');
}

/**
 * Match on result (pattern matching)
 */
export function match<T, E, U>(
  result: Result<T, E>,
  handlers: {
    ok: (value: T) => U;
    err: (error: E) => U;
  }
): U {
  if (isOk(result)) {
    return handlers.ok(result.value);
  }
  return handlers.err(result.error);
}

// ═══════════════════════════════════════════════════════════════════════════
// COMBINING RESULTS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Combine multiple results, returning first error or all values
 */
export function all<T, E>(results: Result<T, E>[]): Result<T[], E> {
  const values: T[] = [];
  
  for (const result of results) {
    if (isErr(result)) {
      return result;
    }
    values.push(result.value);
  }
  
  return ok(values);
}

/**
 * Combine results from an object
 */
export function allFromObject<T extends Record<string, Result<unknown, E>>, E>(
  obj: T
): Result<{ [K in keyof T]: T[K] extends Result<infer U, E> ? U : never }, E> {
  const result: Record<string, unknown> = {};
  
  for (const [key, value] of Object.entries(obj)) {
    if (isErr(value)) {
      return value;
    }
    result[key] = value.value;
  }
  
  return ok(result as { [K in keyof T]: T[K] extends Result<infer U, E> ? U : never });
}

/**
 * Return first Ok or last Err
 */
export function any<T, E>(results: Result<T, E>[]): Result<T, E> {
  let lastErr: Err<E> | null = null;
  
  for (const result of results) {
    if (isOk(result)) {
      return result;
    }
    lastErr = result;
  }
  
  return lastErr!;
}

// ═══════════════════════════════════════════════════════════════════════════
// RESULT BUILDER
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Builder for chaining Result operations
 */
export class ResultBuilder<T, E> {
  constructor(private result: Result<T, E>) {}
  
  static from<T, E>(result: Result<T, E>): ResultBuilder<T, E> {
    return new ResultBuilder(result);
  }
  
  static ok<T>(value: T): ResultBuilder<T, never> {
    return new ResultBuilder(ok(value));
  }
  
  static err<E>(error: E): ResultBuilder<never, E> {
    return new ResultBuilder(err(error));
  }
  
  map<U>(fn: (value: T) => U): ResultBuilder<U, E> {
    return new ResultBuilder(map(this.result, fn));
  }
  
  mapErr<F>(fn: (error: E) => F): ResultBuilder<T, F> {
    return new ResultBuilder(mapErr(this.result, fn));
  }
  
  flatMap<U>(fn: (value: T) => Result<U, E>): ResultBuilder<U, E> {
    return new ResultBuilder(flatMap(this.result, fn));
  }
  
  unwrap(): T {
    return unwrap(this.result);
  }
  
  unwrapOr(defaultValue: T): T {
    return unwrapOr(this.result, defaultValue);
  }
  
  unwrapOrElse(fn: (error: E) => T): T {
    return unwrapOrElse(this.result, fn);
  }
  
  match<U>(handlers: { ok: (value: T) => U; err: (error: E) => U }): U {
    return match(this.result, handlers);
  }
  
  toResult(): Result<T, E> {
    return this.result;
  }
}
