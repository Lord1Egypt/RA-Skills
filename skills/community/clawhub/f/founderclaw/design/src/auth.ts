/**
 * Design tool auth — uses OPENAI_API_KEY env var only.
 * No file-based key storage.
 */
export function getApiKey(): string {
  const key = process.env.OPENAI_API_KEY;
  if (!key) {
    throw new Error(
      "OPENAI_API_KEY environment variable not set.\n" +
      "Set it: export OPENAI_API_KEY='sk-...'"
    );
  }
  return key;
}
