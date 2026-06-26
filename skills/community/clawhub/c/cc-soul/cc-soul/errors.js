const RETRYABLE_PATTERNS = /timeout|ETIMEDOUT|ECONNREFUSED|ECONNRESET|SQLITE_BUSY|rate.?limit|ENOTFOUND|socket hang up/i;
const FATAL_PATTERNS = /TypeError|ReferenceError|SyntaxError|Cannot read|is not a function|is not defined|required|validation failed/i;
const DEGRADABLE_CONTEXTS = ["body", "persona", "emotion", "flow", "epistemic", "behavior", "deep-understand", "cin", "avatar", "absence", "prospective", "lorebook"];
function classifyError(err, context) {
  const msg = err?.message || String(err);
  if (RETRYABLE_PATTERNS.test(msg)) return "retryable";
  if (FATAL_PATTERNS.test(msg)) return "fatal";
  if (DEGRADABLE_CONTEXTS.some((c) => context.includes(c))) return "degraded";
  return "degraded";
}
function handleError(err, context) {
  const category = classifyError(err, context);
  switch (category) {
    case "retryable":
      console.warn(`[cc-soul][${context}] \u27F3 retryable: ${err?.message || err}`);
      break;
    case "fatal":
      console.error(`[cc-soul][${context}] \u2717 FATAL: ${err?.message || err}`);
      break;
    case "degraded":
      console.log(`[cc-soul][${context}] \u2193 degraded: ${err?.message || err}`);
      break;
  }
  return category;
}
export {
  classifyError,
  handleError
};
