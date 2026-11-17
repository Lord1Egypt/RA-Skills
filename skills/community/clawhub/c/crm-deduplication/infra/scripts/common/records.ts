// What a CRM search returned, before either object path gives it meaning:
// an ID and the properties that came with it.

import { asText } from "./values";

/** One record a CRM search returned. */
export type CrmRecord = {
  id: string;
  properties: Record<string, unknown>;
  /** Properties the CRM holds a real value for — HubSpot's `""` is not one. */
  filledPropertyCount: number;
};

/**
 * The records the searches returned, one per CRM ID. A record can match several
 * criteria, or be returned by more than one search, and come back repeatedly;
 * its first appearance is the one kept. A record without an ID names nothing to
 * merge, so it is dropped here rather than guarded against downstream.
 */
export const readCrmRecords = (...searchResults: unknown[]): CrmRecord[] => {
  const records = searchResults.flatMap((result) =>
    Array.isArray(result) ? result : [],
  );

  const read = records
    .map((record: unknown) => readCrmRecord(record))
    .filter((record): record is CrmRecord => record !== undefined);

  return read.filter((record, index) => {
    return read.findIndex((other) => other.id === record.id) === index;
  });
};

const readCrmRecord = (record: unknown): CrmRecord | undefined => {
  if (typeof record !== "object" || record === null) {
    return undefined;
  }

  const id = asText("id" in record ? record.id : undefined);
  if (id === undefined) {
    return undefined;
  }

  const rawProperties = "properties" in record ? record.properties : undefined;
  const entries: [string, unknown][] =
    typeof rawProperties === "object" && rawProperties !== null
      ? Object.entries(rawProperties)
      : [];

  return {
    id,
    properties: Object.fromEntries(entries),
    // Counted from the raw values, where HubSpot's empty string is a real
    // "unset" rather than a filled property.
    filledPropertyCount: entries.filter(([, value]) => {
      return value !== null && value !== undefined && value !== "";
    }).length,
  };
};
