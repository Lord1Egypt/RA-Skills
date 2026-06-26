export class FlowError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'FlowError';
  }
}

export class AuthError extends FlowError {
  constructor(message: string) {
    super(message);
    this.name = 'AuthError';
  }
}

export class TimeoutError extends FlowError {
  constructor(message: string) {
    super(message);
    this.name = 'TimeoutError';
  }
}

export class QuotaExceeded extends FlowError {
  constructor(message: string) {
    super(message);
    this.name = 'QuotaExceeded';
  }
}

export class GenerationError extends FlowError {
  constructor(message: string) {
    super(message);
    this.name = 'GenerationError';
  }
}
