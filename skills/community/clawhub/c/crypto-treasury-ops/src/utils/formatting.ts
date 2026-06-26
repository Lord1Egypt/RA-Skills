import { formatUnits, parseUnits } from "viem";
import type { ToolName, ToolResponse } from "../types.js";

export function formatTokenAmount(rawAmount: bigint, decimals: number): string {
  const raw = formatUnits(rawAmount, decimals);
  const [whole = "0", fraction = ""] = raw.split(".");
  const trimmedFraction = fraction.replace(/0+$/, "");
  return trimmedFraction ? `${whole}.${trimmedFraction}` : whole;
}

export function parseAmountToUnits(amount: string, decimals: number): bigint {
  return parseUnits(amount, decimals);
}

export function buildSuccess<T>(
  tool: ToolName,
  requestId: string,
  status: ToolResponse["status"],
  data: T,
  warnings: string[] = []
): ToolResponse<T> {
  return {
    ok: true,
    tool,
    status,
    requestId,
    timestamp: new Date().toISOString(),
    data,
    warnings: warnings.length > 0 ? warnings : undefined
  };
}

export function buildFailure(
  tool: ToolName,
  requestId: string,
  status: ToolResponse["status"],
  errors: string[],
  data?: Record<string, unknown>,
  warnings: string[] = []
): ToolResponse<Record<string, unknown>> {
  return {
    ok: false,
    tool,
    status,
    requestId,
    timestamp: new Date().toISOString(),
    errors,
    data,
    warnings: warnings.length > 0 ? warnings : undefined
  };
}

export function toErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }

  if (typeof error === "string") {
    return error;
  }

  return "Unknown error";
}
