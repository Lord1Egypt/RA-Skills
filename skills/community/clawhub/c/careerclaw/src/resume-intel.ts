/**
 * resume-intel.ts — Section-aware resume intelligence builder.
 *
 * `buildResumeIntelligence()` extracts a weighted keyword/phrase corpus
 * from multiple resume/profile inputs. Each source has a section weight
 * (from SECTION_WEIGHTS) that determines how important its tokens are
 * for gap analysis.
 *
 * Key design from PR-E: UserProfile.skills are injected as a synthetic
 * "skills" section at weight 1.0 — the highest weight. This prevents
 * skills the user explicitly listed from appearing as gaps.
 *
 * Output schema is JSON-compatible with Python careerclaw so
 * `.careerclaw/resume_intel.json` files are portable across
 * implementations.
 */

import type { ResumeIntelligence } from "./models.js";
import {
  tokenizeUnique,
  extractPhrasesFromText,
  SECTION_WEIGHTS,
} from "./core/text-processing.js";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface ResumeIntelligenceParams {
  /** Short free-text summary from UserProfile.resume_summary. */
  resume_summary: string;
  /** Full resume text from resume.txt or PDF extraction (optional). */
  resume_text?: string;
  /** UserProfile.skills — injected as a synthetic skills section (PR-E fix). */
  skills?: string[];
  /** UserProfile.target_roles — injected at summary weight. */
  target_roles?: string[];
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Build section-aware resume intelligence from available inputs.
 *
 * Sections processed (highest weight first):
 *   1. skills        (weight 1.0)  — UserProfile.skills list
 *   2. summary       (weight 0.8)  — resume_summary + target_roles
 *   3. experience    (weight 0.6)  — resume_text (if provided)
 *
 * For each keyword, the final keyword_weight is the maximum weight
 * across all sections in which it appeared.
 */
export function buildResumeIntelligence(
  params: ResumeIntelligenceParams
): ResumeIntelligence {
  const { resume_summary, resume_text, skills = [], target_roles = [] } = params;

  // Determine source flag
  const hasSkills = skills.length > 0 || target_roles.length > 0;
  const hasResumeText = !!resume_text?.trim();
  const source: ResumeIntelligence["source"] = hasSkills
    ? "skills_injected"
    : hasResumeText
    ? "resume_text"
    : "summary_only";

  // Collect (tokens, weight) pairs per section
  const sections: Array<{ tokens: string[]; weight: number }> = [];

  // Section 1: skills (weight 1.0)
  if (skills.length > 0) {
    sections.push({
      tokens: tokenizeUnique(skills.join(" ")),
      weight: SECTION_WEIGHTS["skills"] ?? 1.0,
    });
  }

  // Section 2: summary + target_roles (weight 0.8)
  const summaryText = [resume_summary, ...target_roles].join(" ");
  if (summaryText.trim()) {
    sections.push({
      tokens: tokenizeUnique(summaryText),
      weight: SECTION_WEIGHTS["summary"] ?? 0.8,
    });
  }

  // Section 3: full resume text (weight 0.6)
  if (hasResumeText) {
    sections.push({
      tokens: tokenizeUnique(resume_text!),
      weight: SECTION_WEIGHTS["experience"] ?? 0.6,
    });
  }

  // Build keyword_weights: max weight across sections
  const keyword_weights: Record<string, number> = {};
  const keyword_stream: string[] = [];

  for (const { tokens, weight } of sections) {
    for (const token of tokens) {
      const existing = keyword_weights[token] ?? 0;
      if (existing === 0) keyword_stream.push(token); // first appearance
      keyword_weights[token] = Math.max(existing, weight);
    }
  }

  // extracted_keywords = unique set (insertion order)
  const extracted_keywords = [...new Set(keyword_stream)];

  // impact_signals = keywords with weight >= 0.8 (skills + summary section)
  const impact_signals = extracted_keywords.filter(
    (k) => (keyword_weights[k] ?? 0) >= 0.8
  );

  // Phrases: extract from combined text of all sections
  const allText = [
    skills.join(" "),
    target_roles.join(" "),
    resume_summary,
    resume_text ?? "",
  ]
    .filter(Boolean)
    .join(" ");

  const phrase_stream = extractPhrasesFromText(allText);
  const extracted_phrases = [...new Set(phrase_stream)];

  // phrase_weights: use the weight of the lower-weight component token
  // (conservative — a phrase is only as strong as its weakest token)
  const phrase_weights: Record<string, number> = {};
  for (const phrase of extracted_phrases) {
    const parts = phrase.split(" ");
    const minWeight = Math.min(
      ...parts.map((p) => keyword_weights[p] ?? SECTION_WEIGHTS["other"] ?? 0.3)
    );
    phrase_weights[phrase] = minWeight;
  }

  return {
    extracted_keywords,
    extracted_phrases,
    keyword_stream,
    phrase_stream,
    impact_signals,
    keyword_weights,
    phrase_weights,
    source,
  };
}
