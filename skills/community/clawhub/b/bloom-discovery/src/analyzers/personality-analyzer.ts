/**
 * Personality Analyzer V2 — 2-Axis Dimension System
 *
 * Calculates two independent dimensions (Conviction/Intuition) and contribution score
 * to determine supporter personality type through a 2x2 quadrant classification.
 */

import { PersonalityType } from '../types/personality';
import { CATEGORY_KEYWORDS } from '../types/categories';
import {
  TasteSpectrums,
  HiddenPatternInsight,
  AiPlaybook,
  LEARNING_TRY_FIRST_KEYWORDS,
  LEARNING_STUDY_FIRST_KEYWORDS,
  DECISION_GUT_KEYWORDS,
  DECISION_DELIBERATE_KEYWORDS,
  NOVELTY_EARLY_KEYWORDS,
  NOVELTY_WAIT_KEYWORDS,
  RISK_BOLD_KEYWORDS,
  RISK_CAUTIOUS_KEYWORDS,
  STRENGTH_PATTERNS,
  EPISODE_PATTERNS,
  EpisodePattern,
} from '../types/taste-dimensions';

export interface UserData {
  sources: string[];
  twitter?: {
    following: string[];
    tweets: any[];
    bio: string;
  };
  farcaster?: {
    casts: any[];
    channels: string[];
    bio: string;
  };
  wallet?: {
    transactions: any[];
    nfts: any[];
    tokens: any[];
    contracts: string[]; // Unique contracts interacted with
  };
  conversationMemory?: {
    topics: string[];
    interests: string[];
    preferences: string[];
    history: string[];
  };
  userMdContent?: string; // Raw USER.md text for keyword + episodic extraction
}

export interface DimensionScores {
  conviction: number;    // 0-100: Conviction (high) ← → Curiosity (low)
  intuition: number;     // 0-100: Intuition (high) ← → Analysis (low)
  contribution: number;  // 0-100: Contribution behavior score
  tasteSpectrums?: TasteSpectrums;
}

export interface PersonalityAnalysis {
  personalityType: PersonalityType;
  tagline: string;
  description: string;          // Short (2-3 sentences) — for card view with limited space
  longDescription: string;      // Full (4-5 sentences) — for dashboard with no space limit
  detectedInterests: string[];
  detectedCategories: string[]; // Top categories for tagline generation
  dimensions: DimensionScores;
  strengths?: string[];
  hiddenInsight?: HiddenPatternInsight;
  aiPlaybook?: AiPlaybook;
  confidence: number;
}

// Minimum keyword frequency score to qualify as a detected category
const MIN_CATEGORY_SCORE = 2;

/**
 * Tagline templates by personality type
 */
const TAGLINE_TEMPLATES = {
  [PersonalityType.THE_VISIONARY]: (category: string) => `The ${category} Pioneer`,
  [PersonalityType.THE_EXPLORER]: (category: string) => `The ${category} Nomad`,
  [PersonalityType.THE_CULTIVATOR]: (category: string) => `The ${category} Gardener`,
  [PersonalityType.THE_OPTIMIZER]: (category: string) => `The ${category} Analyst`,
  [PersonalityType.THE_INNOVATOR]: (category: string) => `The ${category} Architect`,
};

export class PersonalityAnalyzer {
  /**
   * Main analysis method — calculates dimensions and determines personality
   *
   * @param nudges Optional dimension adjustments from USER.md signal merger (-15 to +15 each)
   */
  async analyze(
    userData: UserData,
    nudges?: {
      conviction: number;
      intuition: number;
      contribution: number;
      learning?: number;
      decision?: number;
      novelty?: number;
      risk?: number;
    },
  ): Promise<PersonalityAnalysis> {
    console.log('🤖 Analyzing user data for 2-axis personality classification...');

    // Step 1: Calculate dimension scores
    const dimensions = this.calculateDimensions(userData);

    // Step 1a: Calculate taste spectrums
    const { final: tasteSpectrums, keywordOnly: keywordSpectrums, episodeLabelCounts } = this.calculateTasteSpectrums(userData);
    dimensions.tasteSpectrums = tasteSpectrums;

    // Step 1b: Detect strengths
    const strengths = this.detectStrengths(userData);

    // Step 1.5: Apply dimension nudges from USER.md (if present)
    if (nudges) {
      dimensions.conviction = Math.min(Math.max(dimensions.conviction + nudges.conviction, 0), 100);
      dimensions.intuition = Math.min(Math.max(dimensions.intuition + nudges.intuition, 0), 100);
      dimensions.contribution = Math.min(Math.max(dimensions.contribution + nudges.contribution, 0), 100);

      // Apply taste spectrum nudges if present
      if (nudges.learning !== undefined) {
        dimensions.tasteSpectrums.learning = Math.min(Math.max(dimensions.tasteSpectrums.learning + nudges.learning, 0), 100);
      }
      if (nudges.decision !== undefined) {
        dimensions.tasteSpectrums.decision = Math.min(Math.max(dimensions.tasteSpectrums.decision + nudges.decision, 0), 100);
      }
      if (nudges.novelty !== undefined) {
        dimensions.tasteSpectrums.novelty = Math.min(Math.max(dimensions.tasteSpectrums.novelty + nudges.novelty, 0), 100);
      }
      if (nudges.risk !== undefined) {
        dimensions.tasteSpectrums.risk = Math.min(Math.max(dimensions.tasteSpectrums.risk + nudges.risk, 0), 100);
      }

      console.log(`📊 Nudges applied: conviction ${nudges.conviction >= 0 ? '+' : ''}${nudges.conviction}, intuition ${nudges.intuition >= 0 ? '+' : ''}${nudges.intuition}, contribution ${nudges.contribution >= 0 ? '+' : ''}${nudges.contribution}`);
    }
    console.log(`📊 Dimensions: Conviction=${dimensions.conviction}, Intuition=${dimensions.intuition}, Contribution=${dimensions.contribution}`);
    console.log(`📊 MentalOS: Learning=${tasteSpectrums.learning}, Decision=${tasteSpectrums.decision}, Novelty=${tasteSpectrums.novelty}, Risk=${tasteSpectrums.risk}`);
    if (strengths.length > 0) {
      console.log(`💪 Detected strengths: ${strengths.join(', ')}`);
    }

    // Step 2: Classify personality type (contribution override logic)
    const personalityType = this.classifyPersonality(dimensions);
    console.log(`✨ Personality Type: ${personalityType}`);

    // Step 3: Detect categories for tagline
    const detectedCategories = this.detectCategories(userData);
    const topCategory = detectedCategories[0] || 'Tech';

    // Step 4: Generate dynamic tagline
    const tagline = TAGLINE_TEMPLATES[personalityType](topCategory);

    // Step 5: Extract detailed interests (needed by description composer)
    const detectedInterests = this.extractInterests(userData);

    // Step 6: Generate personalized description (behavioral insights from spectrums + strengths + preferences)
    const preferences = userData.conversationMemory?.preferences || [];
    const { description, longDescription } = this.composeTasteDescription(personalityType, dimensions, strengths, preferences);

    // Step 7: Calculate confidence (based on data sources)
    const confidence = this.calculateConfidence(userData);

    // Step 8: Detect hidden pattern insight (skip if low confidence)
    let hiddenInsight: HiddenPatternInsight | undefined;
    if (confidence > 30) {
      hiddenInsight = this.detectHiddenInsight(
        dimensions,
        personalityType,
        strengths,
        keywordSpectrums,
        tasteSpectrums,
        episodeLabelCounts,
      );
      if (hiddenInsight) {
        console.log(`🔍 Hidden insight: [${hiddenInsight.patternType}] ${hiddenInsight.brief}`);
      }
    }

    // Step 9: Generate AI-era playbook
    const aiPlaybook = this.generateAiPlaybook(personalityType, tasteSpectrums, strengths);

    return {
      personalityType,
      tagline,
      description,
      longDescription,
      detectedInterests,
      detectedCategories,
      dimensions,
      strengths: strengths.length > 0 ? strengths : undefined,
      hiddenInsight,
      aiPlaybook,
      confidence,
    };
  }

  /**
   * Calculate all three dimension scores (0-100 each)
   */
  private calculateDimensions(userData: UserData): DimensionScores {
    const conviction = this.calculateConviction(userData);
    const intuition = this.calculateIntuition(userData);
    const contribution = this.calculateContribution(userData);

    return {
      conviction: Math.min(Math.max(Math.round(conviction), 0), 100),
      intuition: Math.min(Math.max(Math.round(intuition), 0), 100),
      contribution: Math.min(Math.max(Math.round(contribution), 0), 100),
    };
  }

  /**
   * Calculate Conviction (0-100)
   * High = Few deep commitments, focused topics, repeated themes
   * Low = Diverse interests, many topics, always exploring
   */
  private calculateConviction(userData: UserData): number {
    let score = 50; // Start at midpoint

    // Factor 0: Conversation topic focus (primary signal for conversation-only)
    if (userData.conversationMemory) {
      const topicCount = userData.conversationMemory.topics.length;

      // Fewer topics = more focused = higher conviction
      if (topicCount <= 1) score += 15;
      else if (topicCount <= 2) score += 5;
      else if (topicCount <= 3) score += 0;
      else if (topicCount >= 6) score -= 10;
      else if (topicCount >= 8) score -= 20;

      // Topic dominance: use all available text (history + topics + interests)
      const history = this.extractAllText(userData).toLowerCase();
      const topicMentions = userData.conversationMemory.topics.map(topic => {
        // Count how many times each topic's keywords appear in history
        const topicWord = topic.toLowerCase().split(' ')[0];
        const regex = new RegExp(topicWord, 'g');
        return { topic, count: (history.match(regex) || []).length };
      });
      topicMentions.sort((a, b) => b.count - a.count);

      if (topicMentions.length >= 2) {
        const topCount = topicMentions[0].count;
        const secondCount = topicMentions[1].count;
        // Dominant topic = focused person = high conviction
        if (topCount >= 3 * secondCount && topCount >= 3) score += 20;
        else if (topCount >= 2 * secondCount && topCount >= 2) score += 10;
        // Even spread across many topics = explorer = low conviction
        else if (topCount <= secondCount + 1) score -= 10;
      }

      // Many topics + even spread = strong explorer signal
      if (topicCount >= 4 && topicMentions.length >= 2) {
        const topCount = topicMentions[0].count;
        const bottomCount = topicMentions[topicMentions.length - 1].count;
        // If top and bottom topics have similar mentions, very even = explorer
        if (topCount <= bottomCount * 2) score -= 10;
      }

      // Explorer language detection: curiosity/exploration words lower conviction
      // These signal someone who explores broadly rather than commits deeply
      const explorerKeywords = [
        'curious', 'explore', 'exploring', 'explorer', 'discovery', 'discover',
        'experiment', 'experimenting', 'variety', 'diverse', 'try new',
        'always looking', 'different', 'comparing', 'new things', 'so many things',
        'rabbit hole', 'stumble upon',
      ];
      const convictionKeywords = [
        'committed', 'dedicated', 'focused', 'deep dive', 'specialize',
        'expert', 'obsessed', 'passionate about', 'all in', 'doubled down',
      ];
      const explorerHits = explorerKeywords.filter(kw => history.includes(kw)).length;
      const convictionHits = convictionKeywords.filter(kw => history.includes(kw)).length;
      const explorerNet = explorerHits - convictionHits;
      if (explorerNet >= 4) score -= 25;
      else if (explorerNet >= 2) score -= 15;
      else if (explorerNet >= 1) score -= 5;
      else if (explorerNet <= -2) score += 10;
    }

    if (userData.wallet) {
      const { transactions = [], contracts = [], tokens = [] } = userData.wallet;

      // Portfolio concentration (fewer contracts = higher conviction)
      const uniqueContracts = new Set(contracts).size;
      if (uniqueContracts > 0) {
        if (uniqueContracts <= 5) score += 20;
        else if (uniqueContracts <= 10) score += 10;
        else if (uniqueContracts > 30) score -= 20;
      }

      // Repeat interactions
      const contractCounts = contracts.reduce((acc, addr) => {
        acc[addr] = (acc[addr] || 0) + 1;
        return acc;
      }, {} as Record<string, number>);
      const avgInteractionsPerContract = Object.values(contractCounts).reduce((a, b) => a + b, 0) / uniqueContracts;
      if (avgInteractionsPerContract > 5) score += 15;
      else if (avgInteractionsPerContract > 2) score += 5;
      else if (avgInteractionsPerContract < 1.5) score -= 10;

      // Token holding
      const uniqueTokens = new Set(tokens.map((t: any) => t.symbol)).size;
      if (uniqueTokens > 20) score -= 15;
      else if (uniqueTokens < 5) score += 10;
    }

    // Social signals
    if (userData.twitter) {
      const followingCount = userData.twitter.following.length;
      if (followingCount < 100) score += 5;
      else if (followingCount > 500) score -= 5;
    }

    return score;
  }

  /**
   * Calculate Intuition (0-100)
   * High = Vision-driven, backs pre-launch, trend-spotter
   * Low = Data-driven, waits for metrics, mature protocols
   */
  private calculateIntuition(userData: UserData): number {
    let score = 50; // Start at midpoint

    const allText = this.extractAllText(userData).toLowerCase();

    // Factor 1: Vision/narrative language vs data/metrics language
    const visionKeywords = ['vision', 'future', 'believe', 'potential', 'revolutionary', 'paradigm', 'early', 'first'];
    const analysisKeywords = ['data', 'metrics', 'roi', 'tvl', 'apy', 'analysis', 'performance', 'track record'];

    const visionScore = visionKeywords.filter(k => allText.includes(k)).length;
    const analysisScore = analysisKeywords.filter(k => allText.includes(k)).length;

    score += (visionScore - analysisScore) * 5;

    // Factor 2: Wallet activity - pre-launch vs established protocols
    if (userData.wallet) {
      const { transactions = [] } = userData.wallet;

      // Pre-launch signals: interacting with new contracts (deployed < 30 days ago)
      // Established signals: using high-TVL mature protocols
      // Note: In production, this would call blockchain APIs to check contract age and TVL
      // For hackathon, we'll use heuristics

      const establishedProtocols = ['uniswap', 'aave', 'compound', 'curve', 'maker'];
      const establishedTxCount = transactions.filter((tx: any) =>
        establishedProtocols.some(p => tx.to?.toLowerCase().includes(p))
      ).length;

      if (establishedTxCount > 10) score -= 10; // Prefers mature protocols
      else if (establishedTxCount < 3) score += 10; // Avoids established

      // High transaction count = willing to experiment early
      if (transactions.length > 100) score += 5;
    }

    // Factor 3: Social behavior - talks about trends vs analysis
    if (userData.twitter) {
      const tweets = userData.twitter.tweets || [];
      const trendKeywords = ['trend', 'new', 'launch', 'alpha', 'early'];
      const trendMentions = tweets.filter((t: any) =>
        trendKeywords.some(k => t.text?.toLowerCase().includes(k))
      ).length;

      score += trendMentions * 2;
    }

    return score;
  }

  /**
   * Calculate Contribution (0-100)
   * >65 = The Cultivator (override personality classification)
   * Detects: content creation, feedback, referrals, governance
   */
  private calculateContribution(userData: UserData): number {
    let score = 0;

    const allText = this.extractAllText(userData).toLowerCase();

    // Factor 1: Content creation
    const contentKeywords = ['wrote', 'published', 'created', 'shared', 'tutorial', 'guide', 'review'];
    score += contentKeywords.filter(k => allText.includes(k)).length * 5;

    // Factor 2: Community engagement
    const engagementKeywords = ['feedback', 'suggestion', 'improvement', 'helped', 'support', 'community'];
    score += engagementKeywords.filter(k => allText.includes(k)).length * 5;

    // Factor 3: Referrals and evangelism
    const referralKeywords = ['recommend', 'check out', 'try this', 'using', 'love this'];
    score += referralKeywords.filter(k => allText.includes(k)).length * 3;

    // Factor 4: Governance participation
    if (userData.wallet) {
      const { transactions = [] } = userData.wallet;
      const governanceTxs = transactions.filter((tx: any) =>
        tx.method?.includes('vote') || tx.method?.includes('propose')
      ).length;
      score += governanceTxs * 10;
    }

    // Factor 5: Twitter/Farcaster engagement volume
    if (userData.twitter) {
      const tweets = userData.twitter.tweets || [];
      if (tweets.length > 100) score += 10;
      else if (tweets.length > 50) score += 5;
    }

    if (userData.farcaster) {
      const casts = userData.farcaster.casts || [];
      if (casts.length > 100) score += 10;
      else if (casts.length > 50) score += 5;
    }

    return Math.min(score, 100);
  }

  /**
   * Classify personality based on 2x2 quadrant + contribution override
   */
  private classifyPersonality(dimensions: DimensionScores): PersonalityType {
    const { conviction, intuition, contribution } = dimensions;

    // Override: If contribution > 55, user is The Cultivator
    if (contribution > 55) {
      return PersonalityType.THE_CULTIVATOR;
    }

    // 2x2 Quadrant Classification:
    // Conviction ≥ 50 AND Intuition ≥ 50 → The Visionary 💜
    // Conviction < 50 AND Intuition ≥ 50 → The Explorer 💚
    // Conviction ≥ 50 AND Intuition < 50 → The Optimizer 🧡
    // Conviction < 50 AND Intuition < 50 → The Innovator 💙

    if (conviction >= 50 && intuition >= 50) {
      return PersonalityType.THE_VISIONARY;
    } else if (conviction < 50 && intuition >= 50) {
      return PersonalityType.THE_EXPLORER;
    } else if (conviction >= 50 && intuition < 50) {
      return PersonalityType.THE_OPTIMIZER;
    } else {
      return PersonalityType.THE_INNOVATOR;
    }
  }

  /**
   * Detect top categories from user data
   *
   * Uses frequency-weighted scoring: counts total keyword hits per category.
   * A category must reach MIN_CATEGORY_SCORE to qualify — a single passing
   * mention of "blockchain" won't label someone as a Crypto person.
   */
  private detectCategories(userData: UserData): string[] {
    const allText = this.extractAllText(userData).toLowerCase();
    const categoryScores: Record<string, number> = {};

    for (const [category, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
      let score = 0;
      for (const keyword of keywords) {
        // Use word boundary for short keywords to avoid false matches
        const pattern = keyword.length <= 3 ? `\\b${keyword}\\b` : keyword;
        const regex = new RegExp(pattern, 'gi');
        const matches = allText.match(regex);
        if (matches) {
          score += matches.length;
        }
      }
      categoryScores[category] = score;
    }

    // Filter by minimum score, then sort by score descending
    const qualified = Object.entries(categoryScores)
      .filter(([, score]) => score >= MIN_CATEGORY_SCORE)
      .sort(([, a], [, b]) => b - a)
      .map(([category]) => category);

    // Always return at least 1 category (fallback to highest scoring)
    if (qualified.length === 0) {
      const fallback = Object.entries(categoryScores)
        .sort(([, a], [, b]) => b - a)
        .map(([category]) => category);
      return fallback.slice(0, 1);
    }

    return qualified.slice(0, 3);
  }

  /**
   * Extract episodic memory signals from user text.
   *
   * Looks for narrative sentences ("I switched from X to Y", "we built X together")
   * that reveal decisions, pivots, and experiences — much stronger signals than
   * individual keyword hits.
   *
   * Returns aggregated spectrum adjustments from all matched episodes.
   */
  private extractEpisodes(allText: string): { learning: number; decision: number; novelty: number; risk: number; count: number; labelCounts: Record<string, number> } {
    const totals = { learning: 0, decision: 0, novelty: 0, risk: 0, count: 0 };
    const labelCounts: Record<string, number> = {};

    for (const ep of EPISODE_PATTERNS) {
      // Use global regex to count multiple matches
      const globalPattern = new RegExp(ep.pattern.source, ep.pattern.flags.includes('g') ? ep.pattern.flags : ep.pattern.flags + 'g');
      const matches = allText.match(globalPattern);
      if (matches) {
        const hitCount = matches.length;
        totals.count += hitCount;
        labelCounts[ep.label] = (labelCounts[ep.label] || 0) + hitCount;
        if (ep.signals.learning !== undefined) totals.learning += ep.signals.learning * hitCount;
        if (ep.signals.decision !== undefined) totals.decision += ep.signals.decision * hitCount;
        if (ep.signals.novelty !== undefined) totals.novelty += ep.signals.novelty * hitCount;
        if (ep.signals.risk !== undefined) totals.risk += ep.signals.risk * hitCount;
      }
    }

    return { ...totals, labelCounts };
  }

  /**
   * Calculate taste spectrum scores (0-100 each)
   *
   * Two signal layers:
   *   1. Keywords (shallow): vocabulary matching, ±5 per net keyword hit
   *   2. Episodes (deep):    narrative pattern matching, ±8 per weighted episode
   *
   * Episodes carry more weight because they represent actual behaviors/decisions,
   * not just vocabulary preferences.
   */
  private calculateTasteSpectrums(userData: UserData): { final: TasteSpectrums; keywordOnly: TasteSpectrums; episodeLabelCounts: Record<string, number> } {
    const allText = this.extractAllText(userData).toLowerCase();

    // Layer 1: Keyword scoring (±7 per net hit — enough signal to escape the 40-60 band)
    const KW_WEIGHT = 7;
    const tryHits = LEARNING_TRY_FIRST_KEYWORDS.filter(k => allText.includes(k)).length;
    const studyHits = LEARNING_STUDY_FIRST_KEYWORDS.filter(k => allText.includes(k)).length;
    const gutHits = DECISION_GUT_KEYWORDS.filter(k => allText.includes(k)).length;
    const deliberateHits = DECISION_DELIBERATE_KEYWORDS.filter(k => allText.includes(k)).length;
    const earlyHits = NOVELTY_EARLY_KEYWORDS.filter(k => allText.includes(k)).length;
    const waitHits = NOVELTY_WAIT_KEYWORDS.filter(k => allText.includes(k)).length;
    const boldHits = RISK_BOLD_KEYWORDS.filter(k => allText.includes(k)).length;
    const cautiousHits = RISK_CAUTIOUS_KEYWORDS.filter(k => allText.includes(k)).length;

    let learning = 50 + (studyHits - tryHits) * KW_WEIGHT;
    let decision = 50 + (deliberateHits - gutHits) * KW_WEIGHT;
    let novelty = 50 + (waitHits - earlyHits) * KW_WEIGHT;
    let risk = 50 + (cautiousHits - boldHits) * KW_WEIGHT;

    const clamp = (v: number) => Math.min(Math.max(Math.round(v), 0), 100);

    // Save keyword-only values before episode adjustment
    const keywordOnly: TasteSpectrums = {
      learning: clamp(learning),
      decision: clamp(decision),
      novelty: clamp(novelty),
      risk: clamp(risk),
    };

    // Layer 2: Episodic memory scoring (±8 per weighted signal)
    const episodes = this.extractEpisodes(allText);
    if (episodes.count > 0) {
      const EPISODE_WEIGHT = 8;
      learning += episodes.learning * EPISODE_WEIGHT;
      decision += episodes.decision * EPISODE_WEIGHT;
      novelty += episodes.novelty * EPISODE_WEIGHT;
      risk += episodes.risk * EPISODE_WEIGHT;
      console.log(`🧠 Episodic signals: ${episodes.count} episodes found (L:${episodes.learning.toFixed(1)} D:${episodes.decision.toFixed(1)} N:${episodes.novelty.toFixed(1)} R:${episodes.risk.toFixed(1)})`);
    }

    const final: TasteSpectrums = { learning: clamp(learning), decision: clamp(decision), novelty: clamp(novelty), risk: clamp(risk) };
    return { final, keywordOnly, episodeLabelCounts: episodes.labelCounts };
  }

  /**
   * Detect user strengths from text patterns
   * Looks for "I built/created/wrote/taught" + topic patterns
   */
  private detectStrengths(userData: UserData): string[] {
    const allText = this.extractAllText(userData);
    const found = new Set<string>();

    for (const { pattern, label } of STRENGTH_PATTERNS) {
      if (pattern.test(allText)) {
        found.add(label);
      }
    }

    // Return top 5 strength labels
    return Array.from(found).slice(0, 5);
  }

  /**
   * Compose dynamic 4-sentence behavioral description from personality type,
   * dimension spectrums, strengths, and preferences.
   *
   * Sentence structure:
   *   1. How you make decisions  (decision spectrum, 40/60 thresholds, preference-differentiated mid)
   *   2. How you learn           (learning spectrum, 40/60 thresholds, preference-differentiated mid)
   *   3. Attitude toward uncertainty (novelty × risk quadrant, 50 threshold, 45–55 center band)
   *   4. AI age positioning      (PersonalityType + top strength)
   */
  private composeTasteDescription(
    type: PersonalityType,
    dimensions: DimensionScores,
    strengths: string[],
    preferences: string[],
  ): { description: string; longDescription: string } {
    const spectrums = dimensions.tasteSpectrums || { learning: 50, decision: 50, novelty: 50, risk: 50 };
    const topStrength = strengths[0];

    // Helper: check if user has any of the given preference keywords
    const hasPref = (...keys: string[]) =>
      preferences.some(p => keys.some(k => p.toLowerCase().includes(k.toLowerCase())));

    // --- Sentence 1: Decision-making (threshold 40/60) ---
    let sentence1: string;
    if (spectrums.decision < 40) {
      sentence1 = "You decide fast and adjust on the fly — instinct-first, unbothered by analysis paralysis.";
    } else if (spectrums.decision > 60) {
      sentence1 = "You don't decide until you've mapped every angle — a deliberate approach that means your commitments rarely miss.";
    } else {
      // Mid-range: differentiate by preference
      if (hasPref('data-driven', 'data driven')) {
        sentence1 = "You blend gut instinct with data — but when the numbers speak clearly, you listen.";
      } else if (hasPref('community-driven', 'community driven', 'community')) {
        sentence1 = "Your decisions are shaped by the people around you — you listen first, then commit with confidence.";
      } else if (hasPref('innovative', 'early stage', 'early-stage')) {
        sentence1 = "You decide by vision more than convention — when the data is ambiguous, you trust your creative instincts.";
      } else if (hasPref('user-friendly', 'user friendly', 'ux', 'user experience')) {
        sentence1 = "You decide with the end user in mind — if it doesn't serve them, the data doesn't matter.";
      } else if (hasPref('technical', 'open source', 'open-source')) {
        sentence1 = "You let architecture guide your decisions — good systems design answers most questions before they arise.";
      } else {
        sentence1 = "You have a rare gear-shifting ability in decisions: gut call when speed matters, careful analysis when stakes are high.";
      }
    }

    // --- Sentence 2: Learning style (threshold 40/60) ---
    let sentence2: string;
    if (spectrums.learning < 40) {
      sentence2 = "You learn by building — prototypes teach you more in an afternoon than documentation does in a week.";
    } else if (spectrums.learning > 60) {
      sentence2 = "You study systems at a depth most people skip — by the time you act, you understand the mechanics others never notice.";
    } else {
      // Mid-range: differentiate by preference
      if (hasPref('data-driven', 'data driven')) {
        sentence2 = "You learn through measurement — every experiment has a hypothesis, and the results reshape your mental model.";
      } else if (hasPref('community-driven', 'community driven', 'community')) {
        sentence2 = "You learn best through dialogue — other people's perspectives accelerate your understanding faster than solo study.";
      } else if (hasPref('innovative', 'early stage', 'early-stage')) {
        sentence2 = "You learn by pushing boundaries — the edge cases and failure modes teach you what textbooks skip.";
      } else if (hasPref('user-friendly', 'user friendly', 'ux', 'user experience')) {
        sentence2 = "You learn by using — hands-on experience with the end product tells you what documentation can't.";
      } else if (hasPref('technical', 'open source', 'open-source')) {
        sentence2 = "You learn by reading the source — understanding the internals is how you build real mastery.";
      } else {
        sentence2 = "You toggle between hands-on experiments and deep research, picking whichever gets you to understanding faster.";
      }
    }

    // --- Sentence 3: Timing × Concentration quadrant (novelty × risk) ---
    // novelty = when you adopt (pioneer vs pragmatist)
    // risk = how you commit (all-in vs diversified)
    let sentence3: string;
    const noveltyCenter = spectrums.novelty >= 45 && spectrums.novelty <= 55;
    const riskCenter = spectrums.risk >= 45 && spectrums.risk <= 55;

    if (noveltyCenter && riskCenter) {
      // True Center
      sentence3 = "You adapt your timing and commitment to each situation — no default setting, just pattern-matching the stakes in real time.";
    } else if (spectrums.novelty < 50 && spectrums.risk < 50) {
      // Pioneer + All-in: tries new things early AND goes deep
      sentence3 = "You adopt early and go deep — when something catches your eye, you don't dabble, you commit before the crowd even notices.";
    } else if (spectrums.novelty < 50 && spectrums.risk >= 50) {
      // Pioneer + Diversified: tries new things early but spreads bets
      sentence3 = "You show up early to everything, but you spread your bets — first to explore five new tools, keeping options open until one clearly wins.";
    } else if (spectrums.novelty >= 50 && spectrums.risk < 50) {
      // Pragmatist + All-in: waits for proof, then goes hard
      sentence3 = "You wait for the noise to settle, then go all-in — a patient entry paired with total conviction once you see the signal.";
    } else {
      // Pragmatist + Diversified: waits AND spreads
      sentence3 = "You let others beta-test the hype while you maintain a diversified portfolio — when you finally add something, it's earned its place among many.";
    }

    // --- Sentence 4: AI age positioning (PersonalityType + strength) ---
    let sentence4: string;
    const strengthLabel = topStrength || '';
    // Pick correct article (a/an) for the strength label
    const article = /^[aeiou]/i.test(strengthLabel) ? 'An' : 'A';

    const withStrength: Record<string, string> = {
      [PersonalityType.THE_VISIONARY]: `${article} ${strengthLabel} in the AI age with a rare edge — you'll back the right tools before the crowd validates them, and that head start compounds.`,
      [PersonalityType.THE_EXPLORER]: `${article} ${strengthLabel} built for the AI age — your cross-domain curiosity means you'll connect tools and ideas that specialists would never pair.`,
      [PersonalityType.THE_CULTIVATOR]: `${article} ${strengthLabel} with the AI age's scarcest skill — growing trust around tools that no model can replicate on its own.`,
      [PersonalityType.THE_OPTIMIZER]: `${article} ${strengthLabel} primed for the AI age — when every field is flooded with options, your ability to filter ruthlessly turns noise into signal.`,
      [PersonalityType.THE_INNOVATOR]: `${article} ${strengthLabel} who spots structural patterns before they're obvious — in an AI-saturated landscape, that timing is everything.`,
    };

    const withoutStrength: Record<string, string> = {
      [PersonalityType.THE_VISIONARY]: "In the AI age, your conviction-plus-intuition combination is rare capital — you'll back the right tools before the crowd validates them.",
      [PersonalityType.THE_EXPLORER]: "The AI age rewards breadth disguised as depth — your cross-domain curiosity means you'll connect tools and ideas specialists would never pair.",
      [PersonalityType.THE_CULTIVATOR]: "AI amplifies builders, but it can't replace the person who grows trust around a tool — your community instinct is the moat no model can replicate.",
      [PersonalityType.THE_OPTIMIZER]: "When AI floods every field with options, the edge goes to whoever filters ruthlessly — your data-driven discipline is that edge.",
      [PersonalityType.THE_INNOVATOR]: "You spot structural patterns before they're obvious — in an AI-saturated landscape, that timing sense is the difference between riding a wave and being the one who called it.",
    };

    if (topStrength) {
      sentence4 = withStrength[type] || withStrength[PersonalityType.THE_INNOVATOR];
    } else {
      sentence4 = withoutStrength[type] || withoutStrength[PersonalityType.THE_INNOVATOR];
    }

    // Card view: concise 2 sentences (decision + learning) — fits line-clamp-3
    const description = `${sentence1} ${sentence2}`;
    // Dashboard: full 4 sentences with behavioral depth
    const longDescription = `${sentence1} ${sentence2} ${sentence3} ${sentence4}`;

    return { description, longDescription };
  }

  /**
   * Detect the most interesting hidden pattern from computed analysis data.
   *
   * Priority order (most memorable first, catch-alls last):
   *   1. Layer Mismatch    — self-image vs behavior conflict (rare, high impact)
   *   2. Spectrum Extreme   — any spectrum < 15 or > 85 (dramatic, memorable)
   *   3. Episode Dominance  — one behavioral pattern dominates (story-driven)
   *   4. Stealth Contributor — high contribution without Cultivator label
   *   5. Strength Synergy   — known powerful strength combos
   *   6. Boundary Dweller   — conviction/intuition within ±8 of threshold (catch-all)
   */
  private detectHiddenInsight(
    dimensions: DimensionScores,
    personalityType: PersonalityType,
    strengths: string[],
    keywordSpectrums: TasteSpectrums,
    finalSpectrums: TasteSpectrums,
    episodeLabelCounts: Record<string, number>,
  ): HiddenPatternInsight | undefined {
    const spectrumKeys = ['learning', 'decision', 'novelty', 'risk'] as const;
    const spectrumLabels: Record<string, [string, string]> = {
      learning: ['hands-on learner', 'methodical researcher'],
      decision: ['gut-instinct decider', 'deliberate analyst'],
      novelty: ['pioneer', 'pragmatist'],
      risk: ['all-in concentrator', 'diversified strategist'],
    };

    // 1. Layer Mismatch — keyword vs episode spectrums disagree by >15 points
    for (const key of spectrumKeys) {
      const diff = Math.abs(keywordSpectrums[key] - finalSpectrums[key]);
      if (diff > 15) {
        const kwLabel = keywordSpectrums[key] > 50 ? spectrumLabels[key][1] : spectrumLabels[key][0];
        const epLabel = finalSpectrums[key] > 50 ? spectrumLabels[key][1] : spectrumLabels[key][0];
        if (kwLabel !== epLabel) {
          return {
            brief: `You describe yourself as a ${kwLabel}, but your actions say ${epLabel}`,
            narrative: `Your vocabulary leans ${kwLabel}, but when we look at your actual decisions and experiences, the pattern flips — you consistently act like a ${epLabel}. This gap between self-image and behavior is rare and often signals someone in an exciting transition phase.`,
            patternType: 'layer-mismatch',
          };
        }
      }
    }

    // 2. Spectrum Extreme — any spectrum < 15 or > 85
    for (const key of spectrumKeys) {
      const val = finalSpectrums[key];
      if (val < 15 || val > 85) {
        const label = val < 15 ? spectrumLabels[key][0] : spectrumLabels[key][1];
        return {
          brief: `Your ${key} style is off the charts — pure ${label}`,
          narrative: `With a ${key} score of ${val}/100, you're in the extreme end of the spectrum. While most people cluster around the middle, you've committed fully to the ${label} approach. This clarity of style is a strength — you know exactly how you operate.`,
          patternType: 'spectrum-extreme',
        };
      }
    }

    // 3. Episode Dominance — one episode label dominates (>= 3 occurrences and > 50% of total)
    const totalEpisodes = Object.values(episodeLabelCounts).reduce((a, b) => a + b, 0);
    if (totalEpisodes >= 3) {
      const sorted = Object.entries(episodeLabelCounts).sort(([, a], [, b]) => b - a);
      const [topLabel, topCount] = sorted[0];
      if (topCount >= 3 && topCount / totalEpisodes > 0.5) {
        const episodeDescriptions: Record<string, string> = {
          pivot: "You've pivoted multiple times recently — you chase change and aren't afraid to restart",
          shipped: 'You keep shipping — completion is your default mode',
          bold: 'You repeatedly take bold leaps — calculated risk is your comfort zone',
          study: 'You invest deeply in understanding before acting — knowledge is your foundation',
          'hands-on': "You learn by doing, again and again — theory can't keep up with your prototyping",
          'early-adopter': "You're always first in line — your timing instinct outpaces the mainstream",
          decision: 'You make deliberate choices — every move is considered',
          cautious: 'You play the long game — patience and protection are your strategy',
          'wait-and-see': 'You watch, wait, and move only when the timing is right — patience is your strategy',
          exploring: "You're always exploring — curiosity drives you to cover new ground constantly",
          discovery: 'Serendipity is your superpower — you keep finding things others miss',
          'goal-setting': 'You set clear targets and work toward them — structure is your compass',
          achieved: 'You hit what you aim for — your track record of completion speaks for itself',
        };
        const desc = episodeDescriptions[topLabel] || `Your "${topLabel}" pattern dominates your story`;
        return {
          brief: desc,
          narrative: `Out of ${totalEpisodes} behavioral episodes we detected, ${topCount} follow the "${topLabel}" pattern. This isn't random — it's a core part of how you operate. Most people show a mix of patterns, but your consistency here reveals a deep-seated approach to challenges.`,
          patternType: 'episode-dominance',
        };
      }
    }

    // 4. Stealth Contributor — contribution > 40 but NOT classified as Cultivator
    if (dimensions.contribution > 40 && personalityType !== PersonalityType.THE_CULTIVATOR) {
      return {
        brief: "You're a stealth community builder — contributing more than you realize",
        narrative: `Your contribution score (${dimensions.contribution}/100) is surprisingly high for ${personalityType.replace(/^The /, 'a ')}. You're quietly building community value through content, feedback, and engagement — even though it's not your primary identity. Many teams would love to have this kind of organic contributor.`,
        patternType: 'stealth-contributor',
      };
    }

    // 5. Strength Synergy — known powerful combos
    const synergies: [string, string, string][] = [
      ['Builder', 'Designer', 'Builder + Designer is rare — you can envision AND ship'],
      ['Analyst', 'Writer', 'Analyst + Writer means you can decode complexity and explain it clearly'],
      ['Founder', 'Community Builder', 'Founder + Community Builder — you build products AND the people around them'],
      ['Builder', 'Teacher', 'Builder + Teacher — you create things and help others learn to do the same'],
      ['Optimizer', 'Founder', 'Optimizer + Founder — you build lean and iterate fast'],
      ['Designer', 'Writer', 'Designer + Writer — you craft experiences in both visual and verbal form'],
    ];
    if (strengths.length >= 2) {
      for (const [a, b, brief] of synergies) {
        if (strengths.includes(a) && strengths.includes(b)) {
          return {
            brief,
            narrative: `Having both ${a} and ${b} strengths is an uncommon combination. Most people excel at one or the other — you bridge both worlds, which means you can take a project from concept to completion in ways others can't.`,
            patternType: 'strength-synergy',
          };
        }
      }
    }

    // 6. Balanced Versatility — conviction or intuition near center (45-55)
    // Instead of confusing "X points from Type Y", highlight adaptability as a strength
    const balancedDims: string[] = [];
    if (Math.abs(dimensions.conviction - 50) <= 8) balancedDims.push('conviction');
    if (Math.abs(dimensions.intuition - 50) <= 8) balancedDims.push('intuition');

    if (balancedDims.length > 0) {
      const dimLabel = balancedDims.length === 2
        ? 'both conviction and intuition'
        : balancedDims[0];
      const versatileDescriptions: Record<number, { brief: string; narrative: string }> = {
        2: {
          brief: 'You operate in the center of both axes — a rare generalist who can flex in any direction',
          narrative: `Your conviction and intuition scores both sit near the midpoint. While others are locked into one quadrant, you can shift between focused specialist and broad explorer, between gut decisions and careful analysis. This versatility is rare — most people are firmly one or the other. You're the person teams call when they need someone who can adapt.`,
        },
        1: {
          brief: `Your ${balancedDims[0]} sits right at the center — you can flex between both styles at will`,
          narrative: `Your ${balancedDims[0]} score is balanced (${balancedDims[0] === 'conviction' ? dimensions.conviction : dimensions.intuition}/100), meaning you're not locked into one approach. You can switch between ${balancedDims[0] === 'conviction' ? 'deep focus and broad exploration' : 'gut instinct and careful analysis'} depending on what the situation demands. This adaptability is your edge.`,
        },
      };
      const desc = versatileDescriptions[balancedDims.length] || versatileDescriptions[1];
      return {
        brief: desc.brief,
        narrative: desc.narrative,
        patternType: 'boundary-dweller', // Keep type for backwards compatibility
      };
    }

    return undefined;
  }

  /**
   * Generate AI-era playbook based on personality profile.
   * Returns leverage / watchOut / nextMove for the dashboard.
   */
  private generateAiPlaybook(
    personalityType: PersonalityType,
    spectrums: TasteSpectrums,
    strengths: string[],
  ): AiPlaybook {
    // Leverage: based on learning style + strengths
    let leverage: string;
    const topStrength = strengths[0];
    if (spectrums.learning < 35) {
      leverage = topStrength
        ? `Your try-first learning style combined with your ${topStrength} strength means you can prototype with AI tools faster than most — use that speed to test ideas others are still planning.`
        : 'Your try-first learning style means you\'ll adapt to AI tools faster than most — start using them as prototyping partners before waiting for the perfect workflow.';
    } else if (spectrums.learning > 65) {
      leverage = topStrength
        ? `Your deep-research approach as a ${topStrength} means you\'ll understand AI capabilities at a level others won\'t — you\'ll know exactly when to trust AI output and when to override it.`
        : 'Your research-first approach means you\'ll understand AI capabilities at a level others won\'t — you\'ll know the limits before you hit them.';
    } else {
      leverage = topStrength
        ? `Your balanced learning style as a ${topStrength} lets you both experiment with AI tools quickly and understand them deeply — that\'s a rare combination.`
        : 'Your balanced learning style lets you both experiment quickly and understand deeply — you can pick up AI tools fast without falling for hype.';
    }

    // Watch out: based on decision style
    let watchOut: string;
    if (spectrums.decision < 35) {
      watchOut = 'As a gut decider, you might skip evaluating AI output quality. Build a quick review habit — AI is confident even when wrong.';
    } else if (spectrums.decision > 65) {
      watchOut = 'Your deliberate decision-making is a strength, but AI moves fast. Don\'t over-analyze every tool — sometimes a 10-minute test beats an hour of research.';
    } else {
      watchOut = 'You naturally switch between gut calls and careful analysis. With AI, be intentional about which mode you\'re in — quick experiments need less review, high-stakes outputs need more.';
    }

    // Next move: personality type sets the base, spectrums differentiate
    let nextMove: string;

    // Cross personality type × learning style × risk style for unique combos
    if (spectrums.learning < 35 && spectrums.risk < 35) {
      // Try-first + bold → speed runner
      nextMove = topStrength
        ? `Pick an AI tool, skip the tutorial, and build something with your ${topStrength} skills today. Your instinct-first + bold combo means you learn fastest by shipping.`
        : 'Pick an AI tool, skip the tutorial, and build something today. You learn fastest by shipping — let your instinct lead.';
    } else if (spectrums.learning > 65 && spectrums.risk > 65) {
      // Study-first + cautious → strategic evaluator
      nextMove = 'Read 3 comparison reviews of AI tools in your field, then pick the most proven one for a low-stakes task. Your methodical approach will pay off — you\'ll avoid the tools that flame out in 6 months.';
    } else if (spectrums.learning < 35 && spectrums.risk > 65) {
      // Try-first + cautious → careful experimenter
      nextMove = 'Spin up a sandbox project with an AI tool — no production stakes. Your hands-on instinct wants to try, your caution wants safety. A sandbox gives you both.';
    } else if (spectrums.learning > 65 && spectrums.risk < 35) {
      // Study-first + bold → informed risk-taker
      nextMove = 'Deep-dive into one AI tool\'s documentation, then go all-in on a real project. You\'ll understand it better than anyone, and your boldness means you\'ll actually ship with it.';
    } else {
      // Balanced — fall back to personality type
      const typeNextMoves: Record<string, string> = {
        [PersonalityType.THE_VISIONARY]: 'Pick one AI tool in your focus area and go deep for a week. Your conviction means you\'ll find uses others miss.',
        [PersonalityType.THE_EXPLORER]: 'Try a different AI tool for each of your interest areas this week. Cross-pollinate what you learn — your breadth is the edge.',
        [PersonalityType.THE_CULTIVATOR]: 'Test 2 AI tools, then write a honest comparison for your community. You\'re a natural filter — help others skip the hype.',
        [PersonalityType.THE_OPTIMIZER]: 'Map your current workflow, find the one bottleneck AI could 10x, and set up that integration. Efficiency is your game.',
        [PersonalityType.THE_INNOVATOR]: 'Find the newest AI tool in your space and stress-test it before anyone writes about it. Your pattern-spotting will see what others miss.',
      };
      nextMove = typeNextMoves[personalityType] || typeNextMoves[PersonalityType.THE_INNOVATOR];
    }

    // Novelty-based modifier (pioneer vs pragmatist)
    if (spectrums.novelty < 20) {
      nextMove += ' You\'re wired to move first — trust that instinct, the early-mover advantage in AI is real.';
    } else if (spectrums.novelty > 80) {
      nextMove += ' No rush — the AI tools that survive the next 6 months are the ones worth your time.';
    }

    // Risk-based modifier (all-in vs diversified)
    if (spectrums.risk < 20) {
      nextMove += ' When you find the right tool, go deep — your focus is your edge.';
    } else if (spectrums.risk > 80) {
      nextMove += ' Keep your toolkit broad — optionality is your superpower in a fast-moving space.';
    }

    return { leverage, watchOut, nextMove };
  }

  /**
   * Extract all text from user data
   */
  private extractAllText(userData: UserData): string {
    const textParts: string[] = [];

    if (userData.twitter) {
      textParts.push(userData.twitter.bio);
      textParts.push(...userData.twitter.tweets.map(t => t.text || ''));
      textParts.push(...userData.twitter.following);
    }

    if (userData.farcaster) {
      textParts.push(userData.farcaster.bio);
      textParts.push(...userData.farcaster.casts.map(c => c.text || ''));
      textParts.push(...userData.farcaster.channels);
    }

    if (userData.conversationMemory) {
      textParts.push(...userData.conversationMemory.topics);
      textParts.push(...userData.conversationMemory.interests);
      textParts.push(...userData.conversationMemory.preferences);
      textParts.push(...userData.conversationMemory.history);
    }

    // USER.md raw text — first-class signal source
    if (userData.userMdContent) {
      textParts.push(userData.userMdContent);
    }

    return textParts.join(' ');
  }

  /**
   * Extract specific interests
   */
  private extractInterests(userData: UserData): string[] {
    const interests = new Set<string>();
    const allText = this.extractAllText(userData).toLowerCase();

    const interestKeywords = [
      'AI Tools', 'Machine Learning', 'Crypto', 'DeFi', 'NFTs',
      'Education', 'Wellness', 'Fitness', 'Productivity', 'Meditation',
      'Web3', 'DAOs', 'Gaming', 'Art', 'Music', 'Writing',
      'Coding', 'Design', 'Marketing', 'Finance', 'Health',
    ];

    for (const keyword of interestKeywords) {
      if (allText.includes(keyword.toLowerCase())) {
        interests.add(keyword);
      }
    }

    return Array.from(interests).slice(0, 10);
  }

  /**
   * Calculate confidence based on data quality
   */
  private calculateConfidence(userData: UserData): number {
    let confidence = 30; // Base confidence

    if (userData.twitter && userData.twitter.tweets.length > 10) confidence += 20;
    if (userData.farcaster && userData.farcaster.casts.length > 10) confidence += 15;
    if (userData.wallet && userData.wallet.transactions.length > 20) confidence += 25;
    if (userData.conversationMemory && userData.conversationMemory.history.length > 5) confidence += 10;

    return Math.min(confidence, 100);
  }
}
