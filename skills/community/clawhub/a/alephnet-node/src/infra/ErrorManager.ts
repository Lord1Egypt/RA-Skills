import { RetryConfig, DEFAULT_RETRY_CONFIG, withRetry } from '../common/async';

export type ErrorCategory =
  | 'NETWORK' | 'CONSENSUS' | 'SRIA' | 'SERVICE' | 'STORAGE' | 'AUTH' | 'VALIDATION' | 'RESOURCE' | 'INTERNAL';

export abstract class AlephError extends Error {
  abstract readonly code: string;
  abstract readonly category: ErrorCategory;
  abstract readonly recoverable: boolean;
  abstract readonly retryable: boolean;
  
  readonly timestamp: number = Date.now();
  nodeId?: string;
  conversationId?: string;
  
  constructor(message: string) {
      super(message);
      Object.setPrototypeOf(this, new.target.prototype); // restore prototype chain
  }

  toJSON(): object {
    return {
      code: this.code,
      category: this.category,
      message: this.message,
      recoverable: this.recoverable,
      retryable: this.retryable,
      timestamp: this.timestamp,
      nodeId: this.nodeId,
      conversationId: this.conversationId,
      stack: this.stack
    };
  }
}

export class NetworkError extends AlephError {
  readonly category = 'NETWORK';
  constructor(
    readonly code: string,
    message: string,
    readonly targetNode?: string,
    readonly recoverable = true,
    readonly retryable = true
  ) { super(message); }
}

export class ConsensusError extends AlephError {
  readonly category = 'CONSENSUS';
  constructor(
    readonly code: string,
    message: string,
    readonly proposal?: any,
    readonly votes?: any[],
    readonly recoverable = true,
    readonly retryable = false
  ) { super(message); }
}

export class SRIAError extends AlephError {
  readonly category = 'SRIA';
  constructor(
    readonly code: string,
    message: string,
    readonly sessionId?: string,
    readonly lifecycleState?: string,
    readonly recoverable = true,
    readonly retryable = true
  ) { super(message); }
}

export class ServiceError extends AlephError {
  readonly category = 'SERVICE';
  constructor(
    readonly code: string,
    message: string,
    readonly serviceId?: string,
    readonly endpoint?: string,
    readonly recoverable = true,
    readonly retryable = true
  ) { super(message); }
}

export class InternalError extends AlephError {
    readonly category = 'INTERNAL';
    constructor(
        readonly code: string,
        message: string,
        readonly operationName?: string,
        readonly originalError?: any,
        readonly recoverable = false,
        readonly retryable = false
    ) { super(message); }
}

// --- Retry Logic ---

// Imported from common/async

// --- Circuit Breaker ---

export interface CircuitBreakerConfig {
  failureThreshold: number;
  recoveryTimeout: number;
  halfOpenRequests: number;
}

export type CircuitState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

export class CircuitBreaker {
  private state: CircuitState = 'CLOSED';
  private failures = 0;
  private lastFailure: number = 0;
  private halfOpenSuccesses = 0;
  
  constructor(
    private name: string,
    private config: CircuitBreakerConfig = {
      failureThreshold: 5,
      recoveryTimeout: 30000,
      halfOpenRequests: 3
    }
  ) {}
  
  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailure > this.config.recoveryTimeout) {
        this.state = 'HALF_OPEN';
        this.halfOpenSuccesses = 0;
      } else {
        throw new ServiceError('E_CIRCUIT_OPEN', `Circuit breaker ${this.name} is open`);
      }
    }
    
    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  private onSuccess(): void {
    if (this.state === 'HALF_OPEN') {
      this.halfOpenSuccesses++;
      if (this.halfOpenSuccesses >= this.config.halfOpenRequests) {
        this.state = 'CLOSED';
        this.failures = 0;
      }
    } else {
      this.failures = 0;
    }
  }
  
  private onFailure(): void {
    this.failures++;
    this.lastFailure = Date.now();
    
    if (this.state === 'HALF_OPEN' || this.failures >= this.config.failureThreshold) {
      this.state = 'OPEN';
    }
  }
}

// --- Error Manager ---

export class ErrorManager {
    static normalizeError(
        error: any, 
        context: { conversationId?: string; nodeId?: string; operationName: string }
    ): AlephError {
        if (error instanceof AlephError) {
            error.conversationId = context.conversationId;
            error.nodeId = context.nodeId;
            return error;
        }
        
        return new InternalError(
            'E_INTERNAL_UNKNOWN',
            error?.message || 'Unknown error',
            context.operationName,
            error
        );
    }

    static async logError(error: AlephError) {
        // In real impl, would write to log stream or Gun
        console.error(`[AlephError] ${error.category}/${error.code}: ${error.message}`, error.toJSON());
    }
}
