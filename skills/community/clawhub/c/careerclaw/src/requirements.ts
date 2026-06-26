/**
 * requirements.ts — Job requirements extractor.
 *
 * Extracts a structured keyword + phrase corpus from a job posting's
 * title and description. This corpus is the "job side" input for
 * gap analysis (Phase 5) and is distinct from the full tokenisation
 * used by the matching engine — here we want raw coverage, not scoring.
 *
 * No heuristics beyond tokenisation: STOPWORDS filtering already removes
 * boilerplate (apply, candidate, competitive, etc.) so the resulting
 * keyword list reflects genuine technical and role signals.
 */

import type { NormalizedJob, JobRequirements } from "./models.js";
import { tokenizeUnique, extractPhrasesFromText } from "./core/text-processing.js";

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Extract requirements corpus from a job posting.
 *
 * Combines title and description into a single text corpus, then
 * tokenises and extracts bigram/trigram phrases. Both lists are
 * deduplicated (insertion order preserved).
 */
export function extractJobRequirements(job: NormalizedJob): JobRequirements {
  const text = `${job.title} ${job.description}`;
  const keywords = tokenizeUnique(text);
  const phrases = extractPhrasesFromText(text);
  return { keywords, phrases };
}
