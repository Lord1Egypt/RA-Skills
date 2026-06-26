export function toText(content) {
  if (!content) return "";
  if (typeof content === "string") return content;
  if (!Array.isArray(content)) return "";
  return content.reduce((out, block) => {
    if (block?.type !== "text" || !block.text) return out;
    return out ? `${out} ${block.text}` : block.text;
  }, "");
}

/* ------------------------------------------------------------------ */
/*  Session reset prompt detection                                     */
/* ------------------------------------------------------------------ */

export const BARE_SESSION_RESET_PROMPT =
  "A new session was started via /new or /reset. Execute your Session Startup sequence now - read the required files before responding to the user. Then greet the user in your configured persona, if one is provided. Be yourself - use your defined voice, mannerisms, and mood. Keep it to 1-3 sentences and ask what they want to do. If the runtime model differs from default_model in the system prompt, mention the default model. Do not mention internal steps, files, tools, or reasoning.";

/** Levenshtein edit distance (space-optimised O(m*n) time, O(n) space) */
function levenshtein(a, b) {
  const m = a.length;
  const n = b.length;
  const prev = Array.from({ length: n + 1 }, (_, i) => i);
  const curr = new Array(n + 1);
  for (let i = 1; i <= m; i++) {
    curr[0] = i;
    for (let j = 1; j <= n; j++) {
      curr[j] = a[i - 1] === b[j - 1]
        ? prev[j - 1]
        : 1 + Math.min(prev[j - 1], prev[j], curr[j - 1]);
    }
    prev.splice(0, n + 1, ...curr);
  }
  return prev[n];
}

/**
 * Returns true when the query is within 20% length of BARE_SESSION_RESET_PROMPT
 * AND the edit-distance ratio is below 0.20 (i.e. >=80% similar).
 */
export function isSessionResetPrompt(query) {
  if (!query) return false;
  const promptLen = BARE_SESSION_RESET_PROMPT.length;
  const queryLen = query.length;
  if (Math.abs(queryLen - promptLen) / promptLen > 0.20) return false;
  const dist = levenshtein(query, BARE_SESSION_RESET_PROMPT);
  return dist / Math.max(queryLen, promptLen) < 0.20;
}
