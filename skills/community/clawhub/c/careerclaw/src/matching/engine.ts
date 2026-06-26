/**
 * matching/engine.ts — Matching engine orchestrator.
 *
 * `rankJobs()` is the single entry point for the briefing pipeline's
 * ranking step. It scores every job against the user profile, filters
 * out irrelevant jobs via the signal gate, sorts descending by composite
 * score, and returns the top-K results as `ScoredJob[]`.
 *
 * Two-stage retrieval pipeline:
 *   Stage 1 (Multiplier): compositeScore() — keyword overlap gates the
 *     magnitude of the total score. Zero keyword overlap → score of 0.0.
 *   Stage 2 (Gate): minKeywordScore filter — hard boundary that removes
 *     any job below the minimum technical relevance threshold before
 *     ranking. Prevents irrelevant jobs floating on neutral dimension
 *     scores (the "dentist problem").
 *
 * Downstream layers (gap analysis, drafting, tracking) only consume
 * `ScoredJob[]` — they are score-agnostic.
 */

import type { NormalizedJob, UserProfile, ScoredJob } from "../models.js";
import { DEFAULT_TOP_K } from "../config.js";
import { compositeScore } from "./scoring.js";

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Score, filter, and rank jobs against a user profile.
 *
 * @param jobs           - Raw normalised jobs from source adapters
 * @param profile        - User profile to rank against
 * @param limit          - Maximum results to return (default: DEFAULT_TOP_K)
 * @param minKeywordScore - Signal gate threshold; jobs with keyword score
 *                         below this are dropped before ranking (default: 0.01)
 */
export function rankJobs(
  jobs: NormalizedJob[],
  profile: UserProfile,
  limit: number = DEFAULT_TOP_K,
  minKeywordScore: number = 0.01
): ScoredJob[] {
  return jobs
    .map((job): ScoredJob => {
      const { total, breakdown, matched, gaps } = compositeScore(profile, job);
      return {
        job,
        score: total,
        breakdown,
        matched_keywords: matched,
        gap_keywords: gaps,
      };
    })
    // Stage 2: drop jobs that fail the technical relevance gate
    .filter((scored) => scored.breakdown.keyword >= minKeywordScore)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);
}
