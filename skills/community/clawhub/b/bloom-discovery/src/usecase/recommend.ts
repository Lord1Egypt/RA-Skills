/**
 * Use Case Recommender
 *
 * Ranks use cases based on personality spectrum and conversation keywords.
 * Personality-aware: novelty seekers → new use cases, risk-averse → skip DeFi.
 * Keyword frequency threshold: >= 3 mentions to be considered relevant.
 */

import type { TasteSpectrums } from '../types/taste-dimensions';
import type { UseCase, UseCaseRecommendation } from '../types/usecase';
import { matchUseCase, getInstalledSkills } from './matcher';

const KEYWORD_FREQUENCY_THRESHOLD = 3;
const MAX_RECOMMENDATIONS = 10;
const MAX_CONVERSATION_LENGTH = 100_000; // ~100KB safety limit

// Scoring weights
const BASE_SCORE = 50;
const TIER_1_BONUS = 15;
const TIER_2_BONUS = 5;
const MAX_POPULARITY_BOOST = 15;
const NOVELTY_WEIGHT = 0.3;       // moderate influence on ranking
const RISK_PENALTY_WEIGHT = 0.4;  // stronger penalty for risk-averse on DeFi
const KEYWORD_HIT_BONUS = 10;
const TIEBREAK_THRESHOLD = 5;

// Tags that indicate DeFi/high-risk use cases
const DEFI_TAGS = new Set([
  'defi', 'dex', 'lending', 'yield', 'swap', 'liquidity',
  'leverage', 'derivatives', 'perpetual', 'margin',
]);

// Tags that indicate new/experimental use cases
const EXPERIMENTAL_TAGS = new Set([
  'experimental', 'beta', 'alpha', 'new', 'preview',
  'cutting-edge', 'bleeding-edge', 'emerging',
]);

/**
 * Count keyword frequencies from conversation text.
 * Returns a map of keyword -> count.
 */
export function countKeywords(
  conversationText: string,
  keywords: string[]
): Map<string, number> {
  const text = conversationText.toLowerCase();
  const counts = new Map<string, number>();

  for (const kw of keywords) {
    const regex = new RegExp(`\\b${escapeRegex(kw.toLowerCase())}\\b`, 'g');
    const matches = text.match(regex);
    if (matches && matches.length > 0) {
      counts.set(kw, matches.length);
    }
  }

  return counts;
}

function escapeRegex(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Compute a personality-adjusted score for a use case.
 */
function computeScore(
  useCase: UseCase,
  spectrums: TasteSpectrums,
  keywordCounts: Map<string, number>
): { score: number; reasons: string[] } {
  let score = BASE_SCORE;
  const reasons: string[] = [];

  // Tier bonus: essential use cases get a boost
  if (useCase.tier === 1) {
    score += TIER_1_BONUS;
    reasons.push('Essential use case');
  } else if (useCase.tier === 2) {
    score += TIER_2_BONUS;
  }

  // Popularity boost (logarithmic)
  if (useCase.claimCount > 0) {
    const popularityBoost = Math.min(
      Math.log10(useCase.claimCount + 1) * 5,
      MAX_POPULARITY_BOOST
    );
    score += popularityBoost;
    if (useCase.claimCount >= 100) {
      reasons.push(`${useCase.claimCount} builders claimed this`);
    }
  }

  // Novelty spectrum adjustment
  const hasExperimentalTags = useCase.tags.some((t) =>
    EXPERIMENTAL_TAGS.has(t.toLowerCase())
  );
  if (hasExperimentalTags) {
    // novelty: 0 = early adopter (boost), 100 = proven first (penalize)
    const noveltyAdjust = (BASE_SCORE - spectrums.novelty) * NOVELTY_WEIGHT;
    score += noveltyAdjust;
    if (spectrums.novelty < 30) {
      reasons.push('Matches your early-adopter style');
    }
  }

  // Risk spectrum adjustment: penalize DeFi for risk-averse users
  const hasDeFiTags = useCase.tags.some((t) =>
    DEFI_TAGS.has(t.toLowerCase())
  );
  if (hasDeFiTags) {
    // risk: 0 = bold (no penalty), 100 = cautious (heavy penalty)
    const riskPenalty = spectrums.risk * RISK_PENALTY_WEIGHT;
    score -= riskPenalty;
    if (spectrums.risk > 70) {
      reasons.push('DeFi may not match your risk tolerance');
    }
  }

  // Keyword relevance boost
  let keywordHits = 0;
  for (const tag of useCase.tags) {
    const count = keywordCounts.get(tag.toLowerCase()) || 0;
    if (count >= KEYWORD_FREQUENCY_THRESHOLD) {
      keywordHits++;
      score += KEYWORD_HIT_BONUS;
    }
  }
  if (keywordHits > 0) {
    reasons.push(`Mentioned ${keywordHits} related topic(s) in conversation`);
  }

  return { score: Math.max(0, Math.min(100, score)), reasons };
}

/**
 * Recommend use cases based on personality spectrum and conversation context.
 */
export function recommendUseCases(
  useCases: UseCase[],
  spectrums: TasteSpectrums,
  conversationText: string
): UseCaseRecommendation[] {
  // Truncate to prevent excessive CPU on very large inputs
  const truncated = conversationText.slice(0, MAX_CONVERSATION_LENGTH);

  // Collect all tags for keyword counting
  const allTags = Array.from(new Set(useCases.flatMap((uc) => uc.tags)));
  const keywordCounts = countKeywords(truncated, allTags);

  // Pre-compute installed skills once for all use cases
  const installed = new Set(getInstalledSkills());

  const recommendations: UseCaseRecommendation[] = useCases.map((useCase) => {
    const { score, reasons } = computeScore(useCase, spectrums, keywordCounts);
    const verifyResult = matchUseCase(useCase, installed);

    return {
      useCase,
      score,
      reasons,
      verifyResult,
    };
  });

  // Sort by score descending, then by match percentage
  return recommendations
    .sort((a, b) => {
      const scoreDiff = b.score - a.score;
      if (Math.abs(scoreDiff) < TIEBREAK_THRESHOLD) {
        // Tiebreak: prefer use cases the user is closer to completing
        return (
          (b.verifyResult?.matchPercentage || 0) -
          (a.verifyResult?.matchPercentage || 0)
        );
      }
      return scoreDiff;
    })
    .slice(0, MAX_RECOMMENDATIONS);
}
