import type { DropEdition, DropType } from "./types";

export const DEFAULT_DROP_TYPE = 0 as const;
export const DEFAULT_MAX_SUPPLY = 999;
export const OPEN_EDITION_MAX_SUPPLY = 1_000_000_000;

export function deriveEditionFromMaxSupply(maxSupply: unknown): DropEdition | null {
  if (typeof maxSupply !== "number" || !Number.isFinite(maxSupply)) {
    return null;
  }
  return maxSupply >= OPEN_EDITION_MAX_SUPPLY ? "open" : "limited";
}

export function resolveMaxSupplyForEdition(input: {
  requestedEdition?: DropEdition;
  requestedMaxSupply?: number;
  fallbackMaxSupply?: number;
}): number {
  if (input.requestedEdition === "open") {
    return OPEN_EDITION_MAX_SUPPLY;
  }

  if (input.requestedEdition === "limited" && input.requestedMaxSupply === undefined) {
    throw new Error("limited edition requires an explicit maxSupply");
  }

  return input.requestedMaxSupply ?? input.fallbackMaxSupply ?? DEFAULT_MAX_SUPPLY;
}

export function resolveDropMode(input: {
  requestedEdition?: DropEdition;
  requestedDropType?: DropType;
  requestedMaxSupply?: number;
  fallbackDropType?: DropType;
  fallbackMaxSupply?: number;
}): { dropType: DropType; maxSupply: number } {
  return {
    dropType: input.requestedDropType ?? input.fallbackDropType ?? DEFAULT_DROP_TYPE,
    maxSupply: resolveMaxSupplyForEdition(input)
  };
}
