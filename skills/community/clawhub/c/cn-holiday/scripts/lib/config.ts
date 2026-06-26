export const API_BASE_URL = "https://timor.tech/api/holiday";

export const DEFAULT_TIMEOUT_MS = 15_000;
export const DEFAULT_RETRY_COUNT = 2;
export const DEFAULT_BACKOFF_MS = 200;

export enum ExitCode {
  OK = 0,
  PARAM_OR_CONFIG = 2,
  NETWORK = 3,
  API_BUSINESS = 4,
  INTERNAL = 5,
}

export interface CliErrorOptions {
  cause?: unknown;
  rawResponse?: unknown;
}

export class CliError extends Error {
  public readonly exitCode: ExitCode;
  public readonly rawResponse?: unknown;

  constructor(message: string, exitCode: ExitCode, options: CliErrorOptions = {}) {
    super(message, { cause: options.cause });
    this.name = "CliError";
    this.exitCode = exitCode;
    this.rawResponse = options.rawResponse;
  }
}

export function toErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  return String(error);
}

export function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}
