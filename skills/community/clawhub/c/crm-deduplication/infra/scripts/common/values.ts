// The value coercions both object paths share. A CRM property is whatever the
// CRM felt like sending, so it is read through here once and nothing downstream
// compares raw CRM data.

/**
 * A property as text. HubSpot sends an unset property as `""` about as often as
 * it omits it, and this is the one place that collapses the two.
 */
export const asText = (value: unknown): string | undefined => {
  if (value === null || value === undefined) {
    return undefined;
  }

  const text = String(value).trim();
  return text === "" ? undefined : text;
};

/** A property as a count, where anything unreadable counts as none. */
export const asNumber = (value: unknown): number => {
  return Number.isFinite(Number(value)) ? Number(value) : 0;
};

/** The values in order, first occurrence kept. */
export const unique = <T>(values: T[]): T[] => {
  return values.filter((value, index) => values.indexOf(value) === index);
};

/**
 * Whether two records agree on an identity key. An absent key never matches:
 * two records that both know nothing are not the same record.
 */
export const sameKey = (
  left: string | undefined,
  right: string | undefined,
): boolean => {
  return left !== undefined && left === right;
};
