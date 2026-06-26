/**
 * Base error class for EdgeBets SDK
 */
export class EdgeBetsError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode?: number,
    public details?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'EdgeBetsError';
    Object.setPrototypeOf(this, EdgeBetsError.prototype);
  }
}

/**
 * Payment required error (402)
 */
export class PaymentRequiredError extends EdgeBetsError {
  constructor(
    public paymentInfo: {
      amount: number;
      recipient: string;
      currency: string;
      network: string;
    }
  ) {
    super(
      `Payment required: ${paymentInfo.amount / 1000000} ${paymentInfo.currency}`,
      'PAYMENT_REQUIRED',
      402,
      paymentInfo
    );
    this.name = 'PaymentRequiredError';
    Object.setPrototypeOf(this, PaymentRequiredError.prototype);
  }
}

/**
 * Insufficient balance error
 */
export class InsufficientBalanceError extends EdgeBetsError {
  constructor(
    public required: number,
    public available: number
  ) {
    super(
      `Insufficient USDC balance: required ${required}, available ${available}`,
      'INSUFFICIENT_BALANCE',
      undefined,
      { required, available }
    );
    this.name = 'InsufficientBalanceError';
    Object.setPrototypeOf(this, InsufficientBalanceError.prototype);
  }
}

/**
 * Wallet not configured error
 */
export class WalletNotConfiguredError extends EdgeBetsError {
  constructor() {
    super(
      'Wallet not configured. Pass a wallet to EdgeBetsClient constructor.',
      'WALLET_NOT_CONFIGURED'
    );
    this.name = 'WalletNotConfiguredError';
    Object.setPrototypeOf(this, WalletNotConfiguredError.prototype);
  }
}

/**
 * Polling timeout error
 */
export class PollingTimeoutError extends EdgeBetsError {
  constructor(jobId: string, timeout: number) {
    super(
      `Simulation polling timed out after ${timeout}ms`,
      'POLLING_TIMEOUT',
      undefined,
      { jobId, timeout }
    );
    this.name = 'PollingTimeoutError';
    Object.setPrototypeOf(this, PollingTimeoutError.prototype);
  }
}

/**
 * Simulation failed error
 */
export class SimulationFailedError extends EdgeBetsError {
  constructor(jobId: string, reason?: string) {
    super(
      reason || 'Simulation failed',
      'SIMULATION_FAILED',
      undefined,
      { jobId, reason }
    );
    this.name = 'SimulationFailedError';
    Object.setPrototypeOf(this, SimulationFailedError.prototype);
  }
}

/**
 * API error (non-402 HTTP errors)
 */
export class ApiError extends EdgeBetsError {
  constructor(message: string, statusCode: number, details?: Record<string, unknown>) {
    super(message, 'API_ERROR', statusCode, details);
    this.name = 'ApiError';
    Object.setPrototypeOf(this, ApiError.prototype);
  }
}

/**
 * Network/connection error
 */
export class NetworkError extends EdgeBetsError {
  constructor(message: string, cause?: Error) {
    super(message, 'NETWORK_ERROR', undefined, { cause: cause?.message });
    this.name = 'NetworkError';
    Object.setPrototypeOf(this, NetworkError.prototype);
  }
}
