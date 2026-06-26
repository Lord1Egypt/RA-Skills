export class ApiError extends Error {
  readonly status: number;

  readonly body: unknown;

  constructor(status: number, body: unknown) {
    super(`API error ${status}`);
    this.status = status;
    this.body = body;
  }
}

export class TimeoutError extends Error {
  constructor(message = "Request timed out") {
    super(message);
  }
}

export class PaymentError extends Error {
  readonly txHash?: string;

  constructor(message: string, txHash?: string) {
    super(message);
    this.txHash = txHash;
  }
}

export class InsufficientBalanceError extends Error {
  readonly required: string;

  readonly available: string;

  constructor(required: string, available: string) {
    super(`Insufficient USDC balance. Required: ${required}, available: ${available}`);
    this.required = required;
    this.available = available;
  }
}
