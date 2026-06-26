/**
 * gap.ts — Gap analysis engine.
 *
 * `gapAnalysis()` compares resume intelligence against job requirements
 * to produce:
 *   - fit_score         (weighted: rewards high-weight resume keywords)
 *   - fit_score_unweighted (Jaccard overlap — raw coverage)
 *   - signals           (resume keywords/phrases present in the job)
 *   - gaps              (job keywords/phrases absent from the resume)
 *   - summary           (top-5 of each for display)
 *
 * This is a Pro tier feature. It is called after `rankJobs()` and its
 * output supplements the `ScoredJob` with resume-specific insight.
 *
 * Fit score interpretation (from README):
 *   >= 40% — strong match
 *   Practical ceiling ~50% due to company/location tokens in denominator
 */

import type { NormalizedJob, ResumeIntelligence, GapAnalysisResult } from "./models.js";
import { extractJobRequirements } from "./requirements.js";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const TOP_N = 5;

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Run gap analysis between resume intelligence and a job posting.
 *
 * @param intel - Output of `buildResumeIntelligence()`
 * @param job   - The job to analyse against
 */
export function gapAnalysis(
  intel: ResumeIntelligence,
  job: NormalizedJob
): GapAnalysisResult {
  const requirements = extractJobRequirements(job);

  const jobKeywordSet = new Set(requirements.keywords);
  const jobPhraseSet = new Set(requirements.phrases);
  const resumeKeywordSet = new Set(intel.extracted_keywords);
  const resumePhraseSet = new Set(intel.extracted_phrases);

  // ---- Signals (resume ∩ job) ----
  const signalKeywords = intel.extracted_keywords.filter((k) => jobKeywordSet.has(k));
  const signalPhrases = intel.extracted_phrases.filter((p) => jobPhraseSet.has(p));

  // ---- Gaps (job − resume) ----
  const gapKeywords = requirements.keywords.filter((k) => !resumeKeywordSet.has(k));
  const gapPhrases = requirements.phrases.filter((p) => !resumePhraseSet.has(p));

  // ---- Fit score (weighted) ----
  // Sum the keyword_weight of each matched keyword / total job keyword count
  const jobKeywordCount = requirements.keywords.length;
  let weightedMatchSum = 0;
  for (const kw of signalKeywords) {
    weightedMatchSum += intel.keyword_weights[kw] ?? 0;
  }
  const fit_score =
    jobKeywordCount > 0
      ? roundScore(weightedMatchSum / jobKeywordCount)
      : 0;

  // ---- Fit score (unweighted / Jaccard) ----
  const unionSize = new Set([
    ...intel.extracted_keywords,
    ...requirements.keywords,
  ]).size;
  const fit_score_unweighted =
    unionSize > 0 ? roundScore(signalKeywords.length / unionSize) : 0;

  return {
    fit_score,
    fit_score_unweighted,
    signals: {
      keywords: signalKeywords,
      phrases: signalPhrases,
    },
    gaps: {
      keywords: gapKeywords,
      phrases: gapPhrases,
    },
    summary: {
      top_signals: {
        keywords: signalKeywords.slice(0, TOP_N),
        phrases: signalPhrases.slice(0, TOP_N),
      },
      top_gaps: {
        keywords: gapKeywords.slice(0, TOP_N),
        phrases: gapPhrases.slice(0, TOP_N),
      },
    },
  };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function roundScore(n: number): number {
  return Math.round(n * 10_000) / 10_000;
}
