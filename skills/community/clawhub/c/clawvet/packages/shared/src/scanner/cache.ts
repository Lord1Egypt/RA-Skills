import { createHash } from "node:crypto";
import type { ScanResult } from "../types.js";

const MAX_ENTRIES = 100;
const cache = new Map<string, ScanResult>();

function hashContent(content: string): string {
  return createHash("sha256").update(content).digest("hex");
}

export function getCached(content: string): ScanResult | undefined {
  const key = hashContent(content);
  const result = cache.get(key);
  if (result) {
    // Move to end (most recently used)
    cache.delete(key);
    cache.set(key, result);
  }
  return result;
}

export function setCached(content: string, result: ScanResult): void {
  const key = hashContent(content);
  if (cache.has(key)) {
    cache.delete(key);
  } else if (cache.size >= MAX_ENTRIES) {
    // Evict oldest (first entry)
    const oldest = cache.keys().next().value!;
    cache.delete(oldest);
  }
  cache.set(key, result);
}
