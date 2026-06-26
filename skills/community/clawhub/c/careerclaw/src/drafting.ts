/**
 * drafting.ts — Deterministic outreach draft generator (Free tier).
 *
 * `draftOutreach()` produces a professional outreach email from a fixed
 * template. It is the Free tier baseline and always runs as the fallback
 * when LLM enhancement is unavailable or fails.
 *
 * Template is ported directly from the Python careerclaw implementation
 * so output format is consistent across both runtimes.
 *
 * Design constraints (from MVP Feature Contract):
 *   - 150–250 word body
 *   - Professional and concise tone
 *   - Inserts job title, company name, matched skill highlights
 *   - No external dependencies, fully deterministic
 *   - llm_enhanced is always false
 */

import type { NormalizedJob, UserProfile, OutreachDraft } from "./models.js";

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Generate a deterministic outreach draft for a ranked job.
 *
 * @param job             - The job to draft for
 * @param profile         - User profile (experience_years used in body)
 * @param matchedKeywords - Matched keywords from ScoredJob or GapAnalysis
 *                          (up to 3 are highlighted in the body)
 */
export function draftOutreach(
  job: NormalizedJob,
  profile: UserProfile,
  matchedKeywords: string[] = []
): OutreachDraft {
  const subject = buildSubject(job);
  const body = buildBody(job, profile, matchedKeywords);

  return {
    job_id: job.job_id,
    subject,
    body,
    llm_enhanced: false,
  };
}

// ---------------------------------------------------------------------------
// Template builders
// ---------------------------------------------------------------------------

function buildSubject(job: NormalizedJob): string {
  return `Interest in ${job.title} at ${job.company}`;
}

function buildBody(
  job: NormalizedJob,
  profile: UserProfile,
  matchedKeywords: string[]
): string {
  const experienceClause = buildExperienceClause(profile);
  const highlightsClause = buildHighlightsClause(matchedKeywords, job);

  return [
    `Hi ${job.company} team,`,
    "",
    `I'm reaching out to express interest in the ${job.title} role at ${job.company}. ` +
      `I have ${experienceClause} building production systems end-to-end, with a consistent ` +
      `focus on code quality, system reliability, and close collaboration with product and ` +
      `design stakeholders. I've worked across the full lifecycle from early architecture ` +
      `through operational ownership.`,
    "",
    highlightsClause,
    "",
    "That aligns well with my background, including:",
    "- Delivering production-ready features with strong ownership and " +
      "attention to reliability",
    "- Writing clear, maintainable code and collaborating closely with " +
      "stakeholders",
    "- Diagnosing issues quickly and improving systems through good " +
      "instrumentation and feedback loops",
    "",
    "If helpful, I can share a brief summary of relevant work and walk " +
      "you through how I'd approach the first 30 days in this role. " +
      "I'm happy to answer any questions about my background. " +
      "Thanks for your time — I'd love to connect.",
    "",
    "Best regards,",
    "[Your Name]",
  ].join("\n");
}

/**
 * Build the experience clause from profile.experience_years.
 * Falls back to "extensive experience" when not set.
 */
function buildExperienceClause(profile: UserProfile): string {
  if (profile.experience_years === null || profile.experience_years === undefined) {
    return "extensive experience";
  }
  return `${profile.experience_years}+ years of experience`;
}

/**
 * Build the skill highlights sentence from matched keywords.
 * Uses up to 3 keywords. Falls back to a generic sentence if none.
 */
function buildHighlightsClause(
  matchedKeywords: string[],
  job: NormalizedJob
): string {
  const highlights = matchedKeywords.slice(0, 3);

  if (highlights.length === 0) {
    return (
      `My background includes skills directly relevant to the ${job.title} ` +
      `role, and I believe my experience would translate well to the ` +
      `challenges your team is working on.`
    );
  }

  const formatted = formatList(highlights);
  return `My background includes direct experience with ${formatted}, ` +
    `which maps well to what you're building at ${job.company}.`;
}

/**
 * Format a list of strings as natural language.
 * ["a"] → "a"
 * ["a", "b"] → "a and b"
 * ["a", "b", "c"] → "a, b, and c"
 */
function formatList(items: string[]): string {
  if (items.length === 0) return "";
  if (items.length === 1) return items[0]!;
  if (items.length === 2) return `${items[0]} and ${items[1]}`;
  return `${items.slice(0, -1).join(", ")}, and ${items[items.length - 1]}`;
}
