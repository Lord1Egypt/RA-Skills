import { readFileSync } from "node:fs";
import type { HanziRecord } from "./types.ts";

export function readHanziRecords(): HanziRecord[] {
  const filePath = new URL("../../data/hanzi.json", import.meta.url);
  return JSON.parse(readFileSync(filePath, "utf8")) as HanziRecord[];
}

export function buildHanziLookup(records: HanziRecord[]): Map<string, HanziRecord> {
  const lookup = new Map<string, HanziRecord>();
  for (const record of records) {
    if (!lookup.has(record.simplified)) {
      lookup.set(record.simplified, record);
    }
    if (record.kangxi && !lookup.has(record.kangxi)) {
      lookup.set(record.kangxi, record);
    }
  }
  return lookup;
}

export function findRecordsOrThrow(text: string, lookup: Map<string, HanziRecord>): HanziRecord[] {
  const records: HanziRecord[] = [];
  const missing: string[] = [];

  for (const ch of text) {
    const record = lookup.get(ch);
    if (!record) {
      missing.push(ch);
      continue;
    }
    records.push(record);
  }

  if (missing.length > 0) {
    throw new Error(`Name contains unsupported character(s): ${missing.join(", ")}`);
  }

  return records;
}
