/**
 * Reading a field whose name the vendor does not document. Fathom, tl;dv,
 * Modjo and Clari Copilot all name their date filter in the reference and
 * leave the meeting object's own timestamp to be discovered from a live
 * response.
 *
 * A single guessed key reads as "no calls" — a clean empty run rather than an
 * error — so those adapters try a candidate list, and a call that resolves to
 * no timestamp is dropped loudly by name. `--dry-run` prints the date each one
 * resolved to, which is where you confirm the right key was found.
 */

/** The first candidate key holding a non-empty string. */
export function pickString(
  record: Record<string, unknown>,
  keys: readonly string[],
): string | undefined {
  for (const key of keys) {
    const value = record[key];
    if (typeof value === "string" && value.trim() !== "") return value;
  }
  return undefined;
}

/**
 * The first candidate key holding something a Date can parse, as ISO. Epoch
 * milliseconds count: Fireflies and Read.ai both hand back numbers where the
 * neighbouring field is a string, and a string-only read would silently skip
 * every call.
 */
export function pickTimestamp(
  record: Record<string, unknown>,
  keys: readonly string[],
): string | undefined {
  for (const key of keys) {
    const value = record[key];
    if (typeof value === "number" && Number.isFinite(value)) {
      return new Date(value).toISOString();
    }
    if (typeof value !== "string" || value.trim() === "") continue;
    const parsed = Date.parse(value);
    if (Number.isFinite(parsed)) return new Date(parsed).toISOString();
  }
  return undefined;
}
