/**
 * Retry utility with exponential backoff for external API calls.
 */

import { ApiError } from "../types";

/**
 * Configuration for retry behavior
 */
export interface RetryConfig {
	/** Maximum number of retry attempts */
	maxRetries: number;
	/** Initial delay in milliseconds */
	baseDelayMs: number;
	/** Maximum delay cap in milliseconds */
	maxDelayMs: number;
	/** Function to determine if an error is retryable */
	shouldRetry: (error: unknown) => boolean;
}

/**
 * Default retry configuration
 */
export const DEFAULT_RETRY_CONFIG: RetryConfig = {
	maxRetries: 3,
	baseDelayMs: 500,
	maxDelayMs: 8000,
	shouldRetry: (error: unknown): boolean => {
		// ApiError with retryable flag
		if (error instanceof ApiError) {
			return error.retryable || (error.status >= 500 && error.status < 600);
		}

		// Standard Error - check message for common transient issues
		if (error instanceof Error) {
			const message = error.message.toLowerCase();
			return (
				error.name === "AbortError" ||
				message.includes("timeout") ||
				message.includes("econnreset") ||
				message.includes("econnrefused") ||
				message.includes("network") ||
				message.includes("fetch failed")
			);
		}

		return false;
	},
};

/**
 * Execute a function with retry logic and exponential backoff.
 *
 * @param fn - The async function to execute
 * @param config - Retry configuration (uses defaults if not provided)
 * @returns The result of the function
 * @throws The last error if all retries fail
 *
 * @example
 * ```typescript
 * const result = await withRetry(
 *   () => fetch(url, { signal: AbortSignal.timeout(10000) }),
 *   { maxRetries: 3, baseDelayMs: 500 }
 * );
 * ```
 */
export async function withRetry<T>(
	fn: () => Promise<T>,
	config: Partial<RetryConfig> = {},
): Promise<T> {
	const finalConfig: RetryConfig = { ...DEFAULT_RETRY_CONFIG, ...config };
	let lastError: unknown;

	for (let attempt = 0; attempt <= finalConfig.maxRetries; attempt++) {
		try {
			return await fn();
		} catch (error) {
			lastError = error;

			// Check if we should retry
			if (!finalConfig.shouldRetry(error) || attempt === finalConfig.maxRetries) {
				throw error;
			}

			// Calculate delay with exponential backoff and jitter
			const baseDelay = finalConfig.baseDelayMs * 2 ** attempt;
			const jitter = Math.random() * 0.2 * baseDelay; // 0-20% jitter
			const delay = Math.min(baseDelay + jitter, finalConfig.maxDelayMs);

			console.log(
				`Retry attempt ${attempt + 1}/${finalConfig.maxRetries} after ${delay.toFixed(0)}ms`,
			);

			await sleep(delay);
		}
	}

	throw lastError;
}

/**
 * Sleep for a given number of milliseconds
 */
function sleep(ms: number): Promise<void> {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Create a retryable fetch wrapper with timeout
 *
 * @param url - URL to fetch
 * @param options - Fetch options
 * @param timeoutMs - Timeout in milliseconds
 * @param retryConfig - Optional retry configuration
 * @returns Response
 *
 * @example
 * ```typescript
 * const response = await retryableFetch(
 *   'https://api.example.com/data',
 *   { method: 'GET' },
 *   10000
 * );
 * ```
 */
export async function retryableFetch(
	url: string,
	options: RequestInit,
	timeoutMs: number,
	retryConfig: Partial<RetryConfig> = {},
): Promise<Response> {
	return withRetry(async () => {
		const response = await fetch(url, {
			...options,
			signal: AbortSignal.timeout(timeoutMs),
		});

		// Convert HTTP errors to ApiError for proper retry handling
		if (!response.ok) {
			const isRetryable = response.status >= 500 && response.status < 600;
			throw new ApiError(
				`HTTP ${response.status}: ${response.statusText}`,
				response.status,
				isRetryable,
			);
		}

		return response;
	}, retryConfig);
}
