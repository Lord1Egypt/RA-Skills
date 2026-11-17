import type { Snapshot } from "../types";
import { nowIso } from "./env";

/** Canonical error snapshot — always carries the required schema keys. */
export function errorSnapshot(
  provider: string,
  message: string,
  source = "api",
  authHint?: string,
): Snapshot {
  const snap: Snapshot = {
    provider,
    source,
    timestamp: nowIso(),
    balance: null,
    usedPercent: null,
    resetsAt: null,
    monthCost: null,
    monthPeriod: null,
    error: message,
  };
  if (authHint) snap.authHint = authHint;
  return snap;
}

/** Healthy snapshot skeleton with every required key present. */
export function baseSnapshot(provider: string, source: string): Snapshot {
  return {
    provider,
    source,
    timestamp: nowIso(),
    balance: null,
    usedPercent: null,
    resetsAt: null,
    monthCost: null,
    monthPeriod: null,
    details: null,
    error: null,
  };
}
