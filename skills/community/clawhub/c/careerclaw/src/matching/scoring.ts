/**
 * matching/scoring.ts — Pure per-dimension scoring functions.
 *
 * Each dimension function returns a value in [0, 1].
 * Neutral (0.5) is used when data is missing so absent fields neither
 * reward nor penalise the composite score.
 *
 * compositeScore() uses a multiplicative model:
 *
 *   total = sqrt(keyword_score) × qualityBase
 *
 * where qualityBase = weighted sum of experience + salary + work_mode.
 *
 * This means keyword overlap is a signal multiplier, not just another
 * additive term. A job with zero keyword overlap scores 0.0 regardless
 * of how well it matches on salary or work mode — solving the problem
 * of irrelevant jobs floating to the top on neutral dimension scores.
 *
 * sqrt() softens the penalty for partial keyword matches: a job with
 * 25% keyword overlap gets a signal of 0.5 (not 0.25), so genuine
 * partial matches are still surfaced meaningfully.
 *
 * All functions are pure and stateless — safe to unit test in isolation.
 */

import type { NormalizedJob, UserProfile, MatchBreakdown } from "../models.js";
import {
  tokenizeUnique,
  tokenOverlap,
  matchedTokens,
  gapTokens,
} from "../core/text-processing.js";

// ---------------------------------------------------------------------------
// Weights for the quality dimensions (must sum to 1.0)
// ---------------------------------------------------------------------------

/**
 * Quality dimension weights — applied AFTER the keyword signal multiplier.
 * These normalise the three metadata dimensions to a [0, 1] quality base.
 *
 * Originating weights (additive model):
 *   experience 20%, salary 15%, work_mode 15%  →  sum = 50%
 * Normalised to sum to 1.0 for the quality base:
 *   experience 0.4, salary 0.3, work_mode 0.3
 */
const QUALITY_WEIGHTS = {
  experience: 0.4,
  salary: 0.3,
  work_mode: 0.3,
} as const;

// Verify weights sum to 1.0 at module load time
const _weightSum = Object.values(QUALITY_WEIGHTS).reduce((a, b) => a + b, 0);
if (Math.abs(_weightSum - 1.0) > 1e-9) {
  throw new Error(`QUALITY_WEIGHTS must sum to 1.0, got ${_weightSum}`);
}

// ---------------------------------------------------------------------------
// Keyword score
// ---------------------------------------------------------------------------

/**
 * Score keyword overlap between the user profile and a job posting.
 *
 * Profile corpus: skills + target_roles + resume_summary tokens (combined).
 * Job corpus:     title + description tokens.
 *
 * Returns Jaccard-like intersection/union in [0, 1].
 * Returns 0.0 if either corpus tokenises to empty.
 */
export function scoreKeyword(
  profile: UserProfile,
  job: NormalizedJob
): { score: number; matched: string[]; gaps: string[] } {
  const profileText = [
    ...profile.skills,
    ...profile.target_roles,
    profile.resume_summary ?? "",
  ].join(" ");

  const profileTokens = tokenizeUnique(profileText);
  const jobTokens = tokenizeUnique(`${job.title} ${job.description}`);

  if (profileTokens.length === 0 || jobTokens.length === 0) {
    return { score: 0.0, matched: [], gaps: [] };
  }

  return {
    score: tokenOverlap(profileTokens, jobTokens),
    matched: matchedTokens(profileTokens, jobTokens),
    gaps: gapTokens(jobTokens, profileTokens),
  };
}

// ---------------------------------------------------------------------------
// Experience score
// ---------------------------------------------------------------------------

/**
 * Score alignment between user experience years and job requirements.
 *
 * - Returns neutral 0.5 if either side has no data.
 * - Returns 1.0 if the job requires 0 years.
 * - Clamped linear: user_years / job_years, capped at 1.0.
 *   Over-qualified candidates are not penalised.
 */
export function scoreExperience(
  profile: UserProfile,
  job: NormalizedJob
): number {
  const userYears = profile.experience_years;
  const jobYears = job.experience_years;

  if (userYears === null || userYears === undefined) return 0.5;
  if (jobYears === null || jobYears === undefined) return 0.5;
  if (jobYears === 0) return 1.0;

  return Math.min(userYears / jobYears, 1.0);
}

// ---------------------------------------------------------------------------
// Salary score
// ---------------------------------------------------------------------------

/**
 * Score alignment between user salary expectations and the job's posted range.
 *
 * - Returns neutral 0.5 if either side has no data.
 * - Returns 1.0 if job minimum meets or exceeds user minimum.
 * - Proportional score if job pays less, clamped to [0, 1].
 */
export function scoreSalary(
  profile: UserProfile,
  job: NormalizedJob
): number {
  const userMin = profile.salary_min;
  const jobMin = job.salary_min;

  if (userMin === null || userMin === undefined) return 0.5;
  if (jobMin === null || jobMin === undefined) return 0.5;
  if (userMin === 0) return 1.0;
  if (jobMin >= userMin) return 1.0;

  return Math.max(jobMin / userMin, 0.0);
}

// ---------------------------------------------------------------------------
// Work mode score
// ---------------------------------------------------------------------------

/**
 * Score alignment between user work mode preference and job work mode.
 *
 * - Returns 1.0 on exact match.
 * - Returns 0.5 if either side is null (insufficient data).
 * - Returns 0.5 if one side is hybrid (partial compatibility).
 * - Returns 0.0 on hard mismatch (remote vs onsite).
 */
export function scoreWorkMode(
  profile: UserProfile,
  job: NormalizedJob
): number {
  const userMode = profile.work_mode;
  const jobMode = job.work_mode;

  if (userMode === null || userMode === undefined) return 0.5;
  if (jobMode === null || jobMode === undefined) return 0.5;
  if (userMode === jobMode) return 1.0;
  if (userMode === "hybrid" || jobMode === "hybrid") return 0.5;

  return 0.0;
}

// ---------------------------------------------------------------------------
// Composite score — multiplicative model
// ---------------------------------------------------------------------------

/**
 * Compute the weighted composite score.
 *
 * Formula:
 *   qualityBase = (experience × 0.4) + (salary × 0.3) + (work_mode × 0.3)
 *   total       = sqrt(keyword) × qualityBase
 *
 * The keyword score acts as a signal multiplier:
 *   - keyword = 0.0 → total = 0.0 always (the "dentist fix")
 *   - keyword = 1.0 → total = qualityBase
 *   - keyword = 0.25 → signal = 0.5 (sqrt softens partial-match penalty)
 */
export function compositeScore(
  profile: UserProfile,
  job: NormalizedJob
): { total: number; breakdown: MatchBreakdown; matched: string[]; gaps: string[] } {
  const kw = scoreKeyword(profile, job);
  const experience = scoreExperience(profile, job);
  const salary = scoreSalary(profile, job);
  const work_mode = scoreWorkMode(profile, job);

  const qualityBase =
    experience * QUALITY_WEIGHTS.experience +
    salary     * QUALITY_WEIGHTS.salary +
    work_mode  * QUALITY_WEIGHTS.work_mode;

  const signal = Math.sqrt(kw.score);
  const total = roundScore(signal * qualityBase);

  return {
    total,
    breakdown: { keyword: kw.score, experience, salary, work_mode },
    matched: kw.matched,
    gaps: kw.gaps,
  };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function roundScore(n: number): number {
  return Math.round(n * 10_000) / 10_000;
}
