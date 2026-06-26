/**
 * Circuit breaker pattern implementation for external API calls.
 * Prevents cascading failures when a service is down.
 */

export type CircuitState = "closed" | "open" | "half-open";

export interface CircuitBreakerConfig {
	/** Number of failures before opening the circuit */
	threshold: number;
	/** Time in ms before attempting to close the circuit */
	resetTimeMs: number;
	/** Optional callback when state changes */
	onStateChange?: (state: CircuitState) => void;
}

const DEFAULT_CONFIG: CircuitBreakerConfig = {
	threshold: 5,
	resetTimeMs: 60_000, // 1 minute
};

/**
 * Circuit breaker to prevent cascading failures.
 *
 * States:
 * - CLOSED: Normal operation, requests go through
 * - OPEN: Circuit is tripped, requests fail fast
 * - HALF-OPEN: Testing if service is back, single request allowed
 *
 * @example
 * ```typescript
 * const breaker = new CircuitBreaker({ threshold: 5, resetTimeMs: 60000 });
 *
 * const result = await breaker.execute(async () => {
 *   return await fetch('https://api.example.com/data');
 * });
 *
 * if (result === null && breaker.isOpen()) {
 *   console.log('Service is down, using fallback');
 * }
 * ```
 */
export class CircuitBreaker {
	private failures = 0;
	private lastFailureTime = 0;
	private state: CircuitState = "closed";
	private readonly config: CircuitBreakerConfig;

	constructor(config: Partial<CircuitBreakerConfig> = {}) {
		this.config = { ...DEFAULT_CONFIG, ...config };
	}

	/**
	 * Execute a function with circuit breaker protection.
	 * Returns null if the circuit is open (fail fast).
	 */
	async execute<T>(fn: () => Promise<T>): Promise<T | null> {
		// Check if circuit should transition from open to half-open
		if (this.state === "open") {
			if (Date.now() - this.lastFailureTime > this.config.resetTimeMs) {
				this.setState("half-open");
			} else {
				// Fast fail - circuit is still open
				return null;
			}
		}

		try {
			const result = await fn();
			this.onSuccess();
			return result;
		} catch (error) {
			this.onFailure();
			throw error;
		}
	}

	/**
	 * Execute a function and return a fallback value if the circuit is open
	 * or if the function throws.
	 */
	async executeWithFallback<T>(fn: () => Promise<T>, fallback: T): Promise<T> {
		try {
			const result = await this.execute(fn);
			return result ?? fallback;
		} catch {
			return fallback;
		}
	}

	/**
	 * Check if the circuit is currently open
	 */
	isOpen(): boolean {
		return this.state === "open";
	}

	/**
	 * Get the current circuit state
	 */
	getState(): CircuitState {
		return this.state;
	}

	/**
	 * Get failure statistics
	 */
	getStats(): { failures: number; state: CircuitState; lastFailureTime: number } {
		return {
			failures: this.failures,
			state: this.state,
			lastFailureTime: this.lastFailureTime,
		};
	}

	/**
	 * Manually reset the circuit to closed state.
	 * Use with caution - typically for testing or manual recovery.
	 */
	reset(): void {
		this.failures = 0;
		this.lastFailureTime = 0;
		this.setState("closed");
	}

	private onSuccess(): void {
		this.failures = 0;
		if (this.state === "half-open") {
			// Successful request in half-open state closes the circuit
			this.setState("closed");
		}
	}

	private onFailure(): void {
		this.failures++;
		this.lastFailureTime = Date.now();

		if (this.state === "half-open") {
			// Failure in half-open state opens the circuit again
			this.setState("open");
		} else if (this.failures >= this.config.threshold) {
			// Threshold reached, open the circuit
			this.setState("open");
		}
	}

	private setState(newState: CircuitState): void {
		if (this.state !== newState) {
			const oldState = this.state;
			this.state = newState;

			console.log(`Circuit breaker: ${oldState} -> ${newState}`);
			this.config.onStateChange?.(newState);
		}
	}
}

/**
 * Create a circuit breaker with a descriptive name for logging
 */
export function createCircuitBreaker(
	name: string,
	config: Partial<CircuitBreakerConfig> = {},
): CircuitBreaker {
	return new CircuitBreaker({
		...config,
		onStateChange: (state) => {
			console.warn(`[${name}] Circuit breaker state: ${state}`);
			config.onStateChange?.(state);
		},
	});
}
