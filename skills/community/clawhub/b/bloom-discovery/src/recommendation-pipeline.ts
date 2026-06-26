/**
 * Recommendation Pipeline (Standalone)
 *
 * Fetches skills from the Bloom backend catalog (GET /skills?sort=score&limit=200),
 * then applies personality-based scoring, deduplication, feedback filtering,
 * and category grouping.
 *
 * Stateless — safe to call from both the identity skill and backend Bull workers.
 */

import { PersonalityType } from './types/personality';
import {
  CANONICAL_CATEGORIES,
  CATEGORY_KEYWORDS,
  DEFAULT_FALLBACK_CATEGORIES,
} from './types/categories';

export interface RefreshIdentityInput {
  mainCategories: string[];
  subCategories: string[];
  personalityType: string;
  dimensions?: {
    conviction: number;
    intuition: number;
    contribution: number;
  };
  tasteSpectrums?: {
    learning: number;
    decision: number;
    novelty: number;
    risk: number;
  };
  feedback?: {
    categoryWeights?: Record<string, number>;
    excludeSkillIds?: string[];
  };
}

export interface SkillRecommendation {
  skillId: string;
  skillName: string;
  description: string;
  url: string;
  categories: string[];
  matchScore: number;
  reason?: string;
  creator?: string;
  creatorUserId?: number | string;
  source?: 'catalog';
  stars?: number;
  downloads?: number;
  language?: string;
  categoryGroup?: string;
}

// ─── Catalog skill shape (from GET /skills) ─────────────────────────────

interface CatalogSkill {
  slug: string;
  name: string;
  description: string;
  url: string;
  categories: string[];
  stars: number;
  downloads: number;
  autoScore: number;
  creator?: string;
  language?: string;
}

// ─── Internal scored skill ──────────────────────────────────────────────

interface ScoredSkill {
  id: string;
  name: string;
  description: string;
  url: string;
  categories: string[];
  stars: number;
  downloads: number;
  rawScore: number;
  personalityBoost: number;
  finalScore: number;
  creator?: string;
  language?: string;
}

// ─── Category helpers ───────────────────────────────────────────────────

/**
 * Normalize free-form category strings to canonical categories.
 * Falls back to DEFAULT_FALLBACK_CATEGORIES if nothing matches.
 */
function normalizeToCanonical(categories: string[]): string[] {
  const matched = new Set<string>();

  for (const cat of categories) {
    const lower = cat.toLowerCase().trim();

    const direct = CANONICAL_CATEGORIES.find(c => c.toLowerCase() === lower);
    if (direct) {
      matched.add(direct);
      continue;
    }

    for (const [canonical, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
      if (keywords.some(kw => lower.includes(kw) || kw.includes(lower))) {
        matched.add(canonical);
        break;
      }
    }
  }

  if (matched.size === 0) {
    return [...DEFAULT_FALLBACK_CATEGORIES];
  }

  return Array.from(matched);
}

// ─── Pipeline timeout ────────────────────────────────────────────────────

const PIPELINE_TIMEOUT_MS = 8_000;

// ─── Main pipeline ──────────────────────────────────────────────────────

/**
 * Run the full recommendation pipeline: fetch, score, deduplicate, group.
 */
export async function refreshRecommendations(
  identity: RefreshIdentityInput,
): Promise<SkillRecommendation[]> {
  // Wrap entire pipeline in a timeout — graceful degradation on slow networks
  let timer: ReturnType<typeof setTimeout>;
  const innerPromise = refreshRecommendationsInner(identity);

  // Prevent unhandled rejection if inner rejects after timeout wins
  innerPromise.catch(() => {});

  const timeoutPromise = new Promise<SkillRecommendation[]>(resolve => {
    timer = setTimeout(() => {
      console.warn(`[recommendation-pipeline] Timed out after ${PIPELINE_TIMEOUT_MS / 1000}s — returning empty`);
      resolve([]);
    }, PIPELINE_TIMEOUT_MS);
  });

  const result = await Promise.race([innerPromise, timeoutPromise]);
  clearTimeout(timer!);
  return result;
}

async function refreshRecommendationsInner(
  identity: RefreshIdentityInput,
): Promise<SkillRecommendation[]> {
  // Normalize categories before anything else
  const normalizedCategories = normalizeToCanonical(identity.mainCategories);
  const normalizedIdentity: RefreshIdentityInput = {
    ...identity,
    mainCategories: normalizedCategories,
  };

  console.log(
    `[recommendation-pipeline] Searching for ${identity.personalityType}...` +
    ` (categories: ${identity.mainCategories.join(', ')} → ${normalizedCategories.join(', ')})`,
  );

  try {
    // Fetch skills from backend catalog
    const catalogSkills = await fetchCatalogSkills();

    if (catalogSkills.length === 0) {
      console.warn('[recommendation-pipeline] No skills returned from catalog');
      return [];
    }

    // Map to internal ScoredSkill and compute personality boost + engagement
    const scored: ScoredSkill[] = catalogSkills.map(s => {
      const { boost } = calculatePersonalityBoost(
        { description: s.description, categories: s.categories, stars: s.stars },
        normalizedIdentity,
      );
      const rawScore = s.autoScore || 0;

      // Engagement signal: reward real usage (downloads from ClawHub, stars from GitHub)
      // log2 scale so 10k stars ≈ 13, 1k downloads ≈ 13, avoids linear domination
      const engagement = Math.min(
        Math.log2(1 + (s.downloads || 0) * 10 + (s.stars || 0)) * 2,
        20,
      );

      // Blend: autoScore × 0.65 + personalityBoost + engagement (capped at 100)
      const finalScore = Math.min(
        Math.round(rawScore * 0.65 + boost + engagement),
        100,
      );

      return {
        id: s.slug,
        name: s.name,
        description: s.description,
        url: s.url,
        categories: s.categories,
        stars: s.stars,
        downloads: s.downloads,
        rawScore,
        personalityBoost: boost,
        finalScore,
        creator: s.creator,
        language: s.language,
      };
    });

    // Convert to SkillRecommendation format
    const typeName = normalizedIdentity.personalityType.replace(/^The /, '');
    let recommendations: SkillRecommendation[] = scored.map(s => {
      const searchText = `${s.name} ${s.description} ${s.categories.join(' ')}`.toLowerCase();
      const matchedCategory = [...normalizedIdentity.mainCategories, ...normalizedIdentity.subCategories]
        .find(c => searchText.includes(c.toLowerCase()));

      const { matchedKeywords } = calculatePersonalityBoost(
        { description: s.description, categories: s.categories, stars: s.stars },
        normalizedIdentity,
      );

      // Show the most meaningful engagement metric
      const engagementDisplay = s.downloads > 0
        ? (s.downloads >= 1000 ? `${(s.downloads / 1000).toFixed(1)}k downloads` : `${s.downloads} downloads`)
        : s.stars > 0
          ? (s.stars >= 1000 ? `${(s.stars / 1000).toFixed(1)}k ★` : `${s.stars} ★`)
          : 'new';

      // Build a varied, informative reason — avoid repeating category (shown in group header)
      const rawDesc = (s.description || '').split(/[.!?—]/)[0].trim();
      // Truncate at word boundary to avoid mid-word cuts
      const shortDesc = rawDesc.length > 65
        ? rawDesc.slice(0, 65).replace(/\s+\S*$/, '')
        : rawDesc;
      let reason: string;
      if (matchedKeywords.length >= 2) {
        reason = `Matches: ${matchedKeywords.slice(0, 3).join(', ')} — ${engagementDisplay}`;
      } else if (shortDesc && shortDesc.length > 15) {
        reason = `${shortDesc} — ${engagementDisplay}`;
      } else {
        reason = engagementDisplay;
      }

      return {
        skillId: s.id,
        skillName: s.name,
        description: s.description,
        url: s.url,
        categories: s.categories,
        matchScore: s.finalScore,
        reason,
        creator: s.creator,
        source: 'catalog' as const,
        stars: s.stars,
        downloads: s.downloads,
        language: s.language,
      };
    });

    // Deduplicate by URL — keep highest-scoring entry
    const byUrl = new Map<string, SkillRecommendation>();
    for (const rec of recommendations) {
      const key = rec.url.toLowerCase().replace(/\/+$/, '');
      const existing = byUrl.get(key);
      if (!existing || rec.matchScore > existing.matchScore) {
        byUrl.set(key, rec);
      }
    }
    let deduplicated = Array.from(byUrl.values());

    // Apply feedback filters: exclude dismissed skills
    if (identity.feedback?.excludeSkillIds?.length) {
      const excludeSet = new Set(identity.feedback.excludeSkillIds.map(id => id.toLowerCase()));
      const before = deduplicated.length;
      deduplicated = deduplicated.filter(s => !excludeSet.has(s.skillId.toLowerCase()));
      if (before !== deduplicated.length) {
        console.log(`[recommendation-pipeline] Excluded ${before - deduplicated.length} dismissed skills`);
      }
    }

    // Apply feedback category weights as score multiplier
    if (identity.feedback?.categoryWeights) {
      const weights = identity.feedback.categoryWeights;
      for (const skill of deduplicated) {
        for (const cat of skill.categories) {
          const w = weights[cat];
          if (w !== undefined && w !== 1.0) {
            skill.matchScore = Math.min(Math.round(skill.matchScore * w), 100);
            break;
          }
        }
      }
    }

    // Group by normalized categories (3-5 per category)
    const grouped = groupByCategory(deduplicated, normalizedCategories);

    console.log(
      `[recommendation-pipeline] ${catalogSkills.length} catalog skills => ${grouped.length} grouped`,
    );

    return grouped;
  } catch (error) {
    console.error('[recommendation-pipeline] Failed:', error);
    return [];
  }
}

// ─── Catalog fetch ──────────────────────────────────────────────────────

async function fetchCatalogSkills(): Promise<CatalogSkill[]> {
  const apiBase = process.env.BLOOM_API_URL || 'https://api.bloomprotocol.ai';
  const url = `${apiBase}/skills?sort=score&limit=200`;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 5_000);

  try {
    const res = await fetch(url, {
      signal: controller.signal,
      headers: { 'User-Agent': 'Bloom-Identity-Skill' },
    });

    if (!res.ok) {
      console.error(`[recommendation-pipeline] Catalog fetch failed: ${res.status}`);
      return [];
    }

    const body = await res.json();
    const skills: CatalogSkill[] = body.data?.skills || [];
    return skills;
  } catch (err) {
    console.error('[recommendation-pipeline] Catalog fetch error:', err);
    return [];
  } finally {
    clearTimeout(timer);
  }
}

// ─── Category grouping ──────────────────────────────────────────────────

function groupByCategory(
  skills: SkillRecommendation[],
  mainCategories: string[],
): SkillRecommendation[] {
  const MIN_PER_CATEGORY = 3;
  const MAX_PER_CATEGORY = 5;
  const SCORE_THRESHOLD = 25;

  const buckets = new Map<string, SkillRecommendation[]>();
  for (const cat of mainCategories) {
    buckets.set(cat, []);
  }

  for (const skill of skills) {
    const bestCategory = findBestCategory(skill, mainCategories);
    if (bestCategory) {
      buckets.get(bestCategory)!.push({ ...skill, categoryGroup: bestCategory });
    }
  }

  const result: SkillRecommendation[] = [];
  for (const cat of mainCategories) {
    const bucket = buckets.get(cat)!;
    bucket.sort((a, b) => b.matchScore - a.matchScore);

    let count = bucket.filter(s => s.matchScore >= SCORE_THRESHOLD).length;
    count = Math.max(Math.min(count, MAX_PER_CATEGORY), Math.min(MIN_PER_CATEGORY, bucket.length));

    result.push(...bucket.slice(0, count));
  }

  return result;
}

function findBestCategory(skill: SkillRecommendation, mainCategories: string[]): string | null {
  const skillText = [
    ...skill.categories,
    skill.description,
    skill.skillName,
  ].join(' ').toLowerCase();

  let bestCat: string | null = null;
  let bestScore = 0;

  for (const cat of mainCategories) {
    let score = 0;

    if (skill.categories.some(c => c.toLowerCase() === cat.toLowerCase())) {
      score += 10;
    }

    const keywords = CATEGORY_KEYWORDS[cat as keyof typeof CATEGORY_KEYWORDS] || [];
    for (const kw of keywords) {
      if (skillText.includes(kw)) {
        score += 2;
      }
    }

    if (score > bestScore) {
      bestScore = score;
      bestCat = cat;
    }
  }

  // Don't force-assign to first category when there's no match —
  // return null so the skill is skipped instead of polluting buckets.
  return bestCat;
}

// ─── Personality scoring ────────────────────────────────────────────────

function calculatePersonalityBoost(
  skill: { description: string; categories?: string[]; stars?: number },
  identity: RefreshIdentityInput,
): { boost: number; matchedKeywords: string[] } {
  const personalityKeywords = getPersonalityKeywords(identity.personalityType as PersonalityType);
  const descLower = skill.description.toLowerCase();
  const catText = (skill.categories || []).join(' ').toLowerCase();
  const searchText = `${descLower} ${catText}`;

  const matchedKeywords = personalityKeywords.filter(k => searchText.includes(k));
  let keywordBoost = 0;
  for (let i = 0; i < matchedKeywords.length; i++) {
    if (i < 3) keywordBoost += 3;
    else if (i < 6) keywordBoost += 2;
    else keywordBoost += 1;
  }
  keywordBoost = Math.min(keywordBoost, 15);

  let dimensionBoost = 0;
  const dims = identity.dimensions;
  if (dims) {
    if (dims.conviction > 65) {
      const hasExactCategory = (skill.categories || []).some(c => {
        const lower = c.toLowerCase();
        return identity.mainCategories.some(mc => mc.toLowerCase() === lower) ||
               identity.subCategories.some(sc => sc.toLowerCase() === lower);
      });
      if (hasExactCategory) dimensionBoost += 8;
    }

    if (dims.conviction < 35) {
      const hasNovelCategory = (skill.categories || []).some(c => {
        const lower = c.toLowerCase();
        return !identity.mainCategories.some(mc => mc.toLowerCase() === lower) &&
               !identity.subCategories.some(sc => sc.toLowerCase() === lower);
      });
      if (hasNovelCategory) dimensionBoost += 5;
    }

    if (dims.intuition > 65) {
      const earlyKeywords = /\b(early|beta|alpha|experimental)\b/i;
      const isEarlyStage = (skill.stars != null && skill.stars < 500) ||
        earlyKeywords.test(searchText);
      if (isEarlyStage) dimensionBoost += 6;
    }

    if (dims.intuition < 35) {
      const isEstablished = skill.stars != null && skill.stars > 5000;
      if (isEstablished) dimensionBoost += 6;
    }

    if (dims.contribution > 55) {
      const isCommunity = searchText.includes('community') || searchText.includes('collaborat') ||
        searchText.includes('contribut') || searchText.includes('open-source') || searchText.includes('governance');
      if (isCommunity) dimensionBoost += 6;
    }

    dimensionBoost = Math.min(dimensionBoost, 15);
  }

  // Taste spectrum boosts
  let tasteBoost = 0;
  const taste = identity.tasteSpectrums;
  if (taste) {
    if (taste.learning < 40) {
      if (/\b(tool|template|cli|starter|kit|scaffold|boilerplate)\b/i.test(searchText)) {
        tasteBoost += 6;
      }
    }
    if (taste.learning > 60) {
      if (/\b(tutorial|guide|course|documentation|docs|learn|education)\b/i.test(searchText)) {
        tasteBoost += 6;
      }
    }
    if (taste.decision < 40) {
      if (/\b(tool|template|quick[- ]?start|scaffold|instant|rapid)\b/i.test(searchText)) {
        tasteBoost += 5;
      }
    }
    if (taste.decision > 60) {
      if (/\b(documentation|docs|guide|comparison|benchmark|evaluat|review)\b/i.test(searchText)) {
        tasteBoost += 5;
      }
    }
    if (taste.novelty < 40) {
      if (/\b(beta|new|cutting[- ]?edge|alpha|experimental|preview|early[- ]?access)\b/i.test(searchText)) {
        tasteBoost += 5;
      }
    }
    if (taste.novelty > 60) {
      if (/\b(established|proven|mature|stable|reliable|battle[- ]?tested|mainstream)\b/i.test(searchText)) {
        tasteBoost += 5;
      }
    }
    if (taste.risk < 40) {
      if (/\b(moonshot|experimental|high[- ]?risk|ambitious|disrupt|breakthrough|radical)\b/i.test(searchText)) {
        tasteBoost += 4;
      }
    }
    if (taste.risk > 60) {
      if (/\b(stable|established|safe|reliable|secure|conservative|trusted)\b/i.test(searchText)) {
        tasteBoost += 4;
      }
    }
    tasteBoost = Math.min(tasteBoost, 15);
  }

  return { boost: keywordBoost + dimensionBoost + tasteBoost, matchedKeywords };
}

function getPersonalityKeywords(type: PersonalityType): string[] {
  const keywordMap: Record<string, string[]> = {
    [PersonalityType.THE_VISIONARY]: [
      'innovative', 'early-stage', 'vision', 'future', 'paradigm',
      'pioneer', 'disrupt', 'bold', 'ambitious', 'frontier', 'emerging', 'breakthrough',
    ],
    [PersonalityType.THE_EXPLORER]: [
      'diverse', 'experimental', 'discovery', 'research', 'explore',
      'curiosity', 'variety', 'breadth', 'survey', 'sandbox', 'prototype', 'tinker',
    ],
    [PersonalityType.THE_CULTIVATOR]: [
      'community', 'social', 'collaborate', 'nurture', 'build',
      'ecosystem', 'mentor', 'contribute', 'share', 'governance', 'collective', 'stewardship',
    ],
    [PersonalityType.THE_OPTIMIZER]: [
      'efficiency', 'data-driven', 'optimize', 'systematic', 'analytics',
      'performance', 'metrics', 'roi', 'benchmark', 'refine', 'precision', 'reliable',
    ],
    [PersonalityType.THE_INNOVATOR]: [
      'technology', 'ai', 'automation', 'creative', 'cutting-edge',
      'novel', 'hybrid', 'synthesis', 'interdisciplinary', 'integrate', 'cross-domain', 'generative',
    ],
  };
  return keywordMap[type] || [];
}
