/**
 * Keyword-based intent classifier that maps a task description to an employee role.
 */

import { ROLE_KEYWORDS } from "./config.js";

/**
 * Return the best-matching role for {@link taskDescription}.
 *
 * Scoring is done by counting how many keywords from each role's keyword list
 * appear (case-insensitively, whole-word) in the task description.  The role
 * with the highest score wins.  Ties are broken by the iteration order of
 * {@link ROLE_KEYWORDS} (i.e. earlier roles win).  If no keyword matches at
 * all, `"NVC Specialist"` is returned as the safe default.
 */
export function classifyRole(taskDescription: string): string {
  if (!taskDescription) return "NVC Specialist";

  const lowered = taskDescription.toLowerCase();
  const scores: Record<string, number> = Object.fromEntries(
    Object.keys(ROLE_KEYWORDS).map((role) => [role, 0]),
  );

  for (const [role, keywords] of Object.entries(ROLE_KEYWORDS)) {
    for (const kw of keywords) {
      const pattern = new RegExp(`\\b${kw.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`);
      if (pattern.test(lowered)) {
        scores[role]++;
      }
    }
  }

  const bestRole = Object.keys(scores).reduce((a, b) =>
    scores[a] >= scores[b] ? a : b,
  );

  return scores[bestRole] === 0 ? "NVC Specialist" : bestRole;
}
