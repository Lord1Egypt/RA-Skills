/**
 * Bloom Identity Card Generator - OpenClaw Skill v2
 *
 * Enhanced version with:
 * - Permission handling
 * - Manual Q&A fallback
 * - Focus on Twitter/X integration
 * - Graceful degradation
 */

import { promises as fs } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { PersonalityAnalyzer } from './analyzers/personality-analyzer';
import { EnhancedDataCollector } from './analyzers/data-collector-enhanced';
import { ManualQAFallback, ManualAnswer } from './analyzers/manual-qa-fallback';
import { CategoryMapper } from './analyzers/category-mapper';
import { PersonalityType } from './types/personality';
import { HiddenPatternInsight, AiPlaybook } from './types/taste-dimensions';
import { refreshRecommendations, SkillRecommendation } from './recommendation-pipeline';
import { DISPLAY_CATEGORIES, DISPLAY_CATEGORY_MAP } from './types/categories';
import { syncDiscoveries, DiscoveryEntry } from './discovery-sync';
import { parseUserMd, UserMdSignals } from './parsers/user-md-parser';
import { mergeSignals, MergedSignals, FeedbackData } from './analyzers/signal-merger';
import { privatizeSpectrums, conversationFingerprint } from './utils/privacy';

// ── Local identity persistence ──────────────────────────────────────

const BLOOM_DIR = join(homedir(), '.bloom');
const AGENT_ID_FILE = join(BLOOM_DIR, 'agent-id.json');

interface StoredAgent {
  agentUserId: number;
  userId?: string;
  savedAt?: string;
  // Agent registration (self-registration via POST /agent/register)
  agentId?: string;       // e.g. "agent_123456789"
  assignedTribe?: string; // "build" | "raise" | "grow"
}

/** Load stored identity file including userId for consistency check */
async function loadStoredIdentityFile(): Promise<StoredAgent | null> {
  try {
    const data = await fs.readFile(AGENT_ID_FILE, 'utf-8');
    const parsed = JSON.parse(data);
    return typeof parsed.agentUserId === 'number' ? parsed : null;
  } catch {
    return null;
  }
}

/** Persist agent data locally for returning user detection (atomic write, 0o600) */
async function saveAgentId(agentUserId: number, userId: string, extra?: Partial<StoredAgent>): Promise<void> {
  try {
    await fs.mkdir(BLOOM_DIR, { recursive: true, mode: 0o700 });
    const tmpFile = `${AGENT_ID_FILE}.${process.pid}.tmp`;
    await fs.writeFile(
      tmpFile,
      JSON.stringify({
        agentUserId,
        userId,
        savedAt: new Date().toISOString(),
        ...extra,
      }),
      { mode: 0o600 },
    );
    await fs.rename(tmpFile, AGENT_ID_FILE); // atomic on same filesystem
  } catch (err) {
    console.debug('[agent-id] Failed to save:', err instanceof Error ? err.message : err);
  }
}


/** Fetch existing identity from backend by agentUserId */
async function fetchExistingIdentity(agentUserId: number): Promise<any | null> {
  try {
    const apiBase = process.env.BLOOM_API_URL || 'https://api.bloomprotocol.ai';
    const res = await fetch(`${apiBase}/x402/agent/${agentUserId}`, { signal: AbortSignal.timeout(3000) });
    if (!res.ok) return null;
    const body = await res.json();
    return body.data || null;
  } catch {
    return null;
  }
}

// Re-export for backwards compatibility
export { PersonalityType };
export type { SkillRecommendation, FeedbackData, UserMdSignals };

export interface IdentityData {
  personalityType: PersonalityType;
  customTagline: string;
  customDescription: string;          // Short (2-3 sentences) — card view
  customLongDescription?: string;     // Full (4-5 sentences) — dashboard view
  mainCategories: string[];
  subCategories: string[];
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
  strengths?: string[];
  hiddenInsight?: HiddenPatternInsight;
  aiPlaybook?: AiPlaybook;
}

/**
 * Display-friendly labels for consuming agents (i18n + clarity).
 * Consuming agents (OpenClaw bot, etc.) should use these labels
 * instead of guessing from field names.
 */
export const DISPLAY_LABELS = {
  // Section headers
  personalityType: { en: 'Personality Type', zh: '你的建造者類型' },
  tagline: { en: 'Tagline', zh: '一句話描述' },
  dimensions: { en: 'Core Dimensions', zh: '核心維度' },
  tasteSpectrums: { en: 'How You Operate', zh: '你的操作風格' },
  hiddenInsight: { en: 'Hidden Pattern', zh: '獨特發現' },
  aiPlaybook: { en: 'Your AI Edge', zh: '你的 AI 優勢指南' },
  recommendations: { en: 'Recommended Skills', zh: '推薦技能' },
  strengths: { en: 'Strengths', zh: '你的強項' },

  // Dimension labels
  conviction: { en: 'Conviction', zh: '信念' },
  intuition: { en: 'Intuition', zh: '直覺' },
  contribution: { en: 'Contribution', zh: '社群貢獻' },

  // Spectrum labels (low → high)
  learning: { en: 'Learning', zh: '學習風格', low: { en: 'try-first', zh: '動手派' }, high: { en: 'study-first', zh: '研究派' } },
  decision: { en: 'Decision', zh: '決策風格', low: { en: 'gut', zh: '直覺決策' }, high: { en: 'deliberate', zh: '深思熟慮' } },
  novelty:  { en: 'Timing', zh: '採用時機', low: { en: 'pioneer', zh: '先鋒' }, high: { en: 'pragmatist', zh: '務實派' } },
  risk:     { en: 'Focus', zh: '投入方式', low: { en: 'all-in', zh: '全力投入' }, high: { en: 'diversified', zh: '分散佈局' } },

  // Playbook sub-fields
  leverage: { en: 'Your edge', zh: '你的優勢' },
  watchOut: { en: 'Watch out', zh: '注意事項' },
  nextMove: { en: 'Try this', zh: '下一步行動' },
} as const;

/**
 * Execution mode
 */
export enum ExecutionMode {
  AUTO = 'auto',           // Try data collection, fallback to Q&A if insufficient
  MANUAL = 'manual',       // Skip data collection, go straight to Q&A
  DATA_ONLY = 'data_only', // Only use data collection, fail if insufficient
}

/**
 * Main Bloom Identity Skill v2
 */
export class BloomIdentitySkillV2 {
  private personalityAnalyzer: PersonalityAnalyzer;
  private dataCollector: EnhancedDataCollector;
  private manualQA: ManualQAFallback;
  private categoryMapper: CategoryMapper;

  constructor() {
    this.personalityAnalyzer = new PersonalityAnalyzer();
    this.dataCollector = new EnhancedDataCollector();
    this.manualQA = new ManualQAFallback();
    this.categoryMapper = new CategoryMapper();
  }

  /**
   * Main skill execution with intelligent fallback
   */
  async execute(
    userId: string,
    options?: {
      mode?: ExecutionMode;
      skipShare?: boolean; // Twitter share is optional
      manualAnswers?: ManualAnswer[]; // If already collected
      conversationText?: string; // ⭐ NEW: Direct conversation text from OpenClaw bot
      userMdPath?: string;       // Path to USER.md, default ~/.config/claude/USER.md
      feedback?: FeedbackData;   // Feedback signals from recommendation interactions
      forceRegenerate?: boolean; // Skip returning user check, regenerate from scratch
    }
  ): Promise<{
    success: boolean;
    mode: 'data' | 'manual' | 'hybrid';
    identityData?: IdentityData;
    recommendations?: SkillRecommendation[];
    discoveries?: DiscoveryEntry[];
    dashboardUrl?: string;
    cardUrl?: string;     // Lightweight card-only view
    claimUrl?: string;    // Direct URL to save card via email registration
    discoverUrl?: string;
    dataQuality?: number;
    dimensions?: {
      conviction: number;
      intuition: number;
      contribution: number;
    };
    displayLabels?: typeof DISPLAY_LABELS;
    actions?: {
      share?: {
        url: string;
        text: string;
        hashtags: string[];
      };
      save?: {
        prompt: string;
        claimUrl: string;   // Dashboard with ?intent=save — auto-opens email capture
        registerUrl: string;
        loginUrl: string;
      };
    };
    registration?: {
      agentId: string;
      assignedTribe: string;
      isNew: boolean; // true if just registered, false if already registered
    };
    isReturningUser?: boolean;
    error?: string;
    needsManualInput?: boolean;
    manualQuestions?: string;
  }> {
    try {
      console.log(`🎴 Generating Bloom Identity for user: ${userId}`);

      const mode = options?.mode || ExecutionMode.AUTO;

      // Step 0: Check for returning user — skip full generation if identity exists
      const IDENTITY_TTL_MS = 30 * 24 * 60 * 60 * 1000; // 30 days
      const storedFile = options?.forceRegenerate ? null : await loadStoredIdentityFile();
      const storedAgentId = storedFile?.agentUserId ?? null;

      if (storedAgentId) {
        // Validate userId consistency (different user on same machine?)
        if (storedFile?.userId && storedFile.userId !== userId) {
          console.log(`⚠️  Different user detected (stored=${storedFile.userId}, current=${userId}), regenerating...`);
        // Check TTL — regenerate if identity is older than 30 days
        } else if (storedFile?.savedAt && (Date.now() - new Date(storedFile.savedAt).getTime()) > IDENTITY_TTL_MS) {
          console.log('⏰ Identity expired (>30 days), regenerating...');
        } else {
          console.debug(`[agent-id] Found stored agent ID: ${storedAgentId}, checking backend...`);
          const existing = await fetchExistingIdentity(storedAgentId);
          const ed = existing?.identityData;

          // Validate backend response has all required fields
          if (
            ed?.personalityType &&
            Object.values(PersonalityType).includes(ed.personalityType as PersonalityType) &&
            Array.isArray(ed.mainCategories) && ed.mainCategories.length > 0 &&
            ed.tagline && ed.description
          ) {
            console.log(`✅ Returning user: ${ed.personalityType}`);

            // Reconstruct identity from stored data
            // Prefer raw spectrums from dimensions (pre-LDP) over top-level (post-LDP noised)
            const rawSpectrums = ed.dimensions?.tasteSpectrums || ed.tasteSpectrums;
            const existingIdentity: IdentityData = {
              personalityType: ed.personalityType as PersonalityType,
              customTagline: ed.tagline,
              customDescription: ed.description,
              customLongDescription: ed.longDescription,
              mainCategories: ed.mainCategories,
              subCategories: ed.subCategories || [],
              dimensions: ed.dimensions,
              tasteSpectrums: rawSpectrums,
              strengths: ed.strengths,
              hiddenInsight: ed.hiddenInsight,
              aiPlaybook: ed.aiPlaybook,
            };

            // Refresh recommendations with latest signals (graceful failure)
            const userMdSignals = parseUserMd(options?.userMdPath);
            const merged = (userMdSignals || options?.feedback)
              ? mergeSignals(
                  existingIdentity.mainCategories,
                  existingIdentity.dimensions || { conviction: 50, intuition: 50, contribution: 50 },
                  userMdSignals,
                  options?.feedback ?? null,
                )
              : null;
            // Refresh recommendations + sync discoveries IN PARALLEL
            let recommendations: SkillRecommendation[] = [];
            let discoveries: DiscoveryEntry[] = [];

            const [recsResult, discResult] = await Promise.allSettled([
              this.recommendSkills(existingIdentity, merged),
              Promise.race([
                syncDiscoveries(storedAgentId),
                new Promise<never>((_, reject) => setTimeout(() => reject(new Error('timeout')), 2000)),
              ]),
            ]);

            if (recsResult.status === 'fulfilled') {
              recommendations = recsResult.value;
              console.log(`✅ Refreshed ${recommendations.length} recommendations`);
            } else {
              console.warn('[recommendations] failed for returning user:', recsResult.reason?.message || recsResult.reason);
            }

            if (discResult.status === 'fulfilled') {
              discoveries = discResult.value.newEntries;
            } else {
              console.debug('[discovery-sync] failed:', discResult.reason?.message || discResult.reason);
            }

            const baseUrl = process.env.DASHBOARD_URL || 'https://bloomprotocol.ai';
            const dashboardUrl = `${baseUrl}/agents/${storedAgentId}`;
            const tribe = getRecommendedTribe(existingIdentity.mainCategories);
            const discoverUrl = `${baseUrl}/discover/${tribe.id}`;

            // Return stored registration if available
            const storedReg = storedFile?.agentId
              ? { agentId: storedFile.agentId, assignedTribe: storedFile.assignedTribe || 'build', isNew: false }
              : undefined;

            const claimUrl = `${dashboardUrl}?intent=save`;

            return {
              success: true,
              mode: (ed.mode as 'data' | 'manual') || 'data',
              identityData: existingIdentity,
              recommendations,
              discoveries,
              dashboardUrl,
              cardUrl: `${dashboardUrl}?view=card`,
              claimUrl,
              discoverUrl,
              dataQuality: ed.confidence || 0,
              isReturningUser: true,
              dimensions: existingIdentity.dimensions,
              displayLabels: DISPLAY_LABELS,
              registration: storedReg,
              actions: {
                share: {
                  url: dashboardUrl,
                  text: `Check out my Bloom Identity: ${existingIdentity.personalityType}! 🌸`,
                  hashtags: ['BloomProtocol', 'BloomDiscovery', 'OpenClaw'],
                },
                save: {
                  prompt: 'Register with email to claim your Bloom Identity Card',
                  claimUrl,
                  registerUrl: `${baseUrl}/register?return=${encodeURIComponent(claimUrl)}`,
                  loginUrl: `${baseUrl}/login?return=${encodeURIComponent(claimUrl)}`,
                },
              },
            };
          } else {
            console.log('⚠️  Stored identity incomplete or invalid, regenerating...');
          }
        }
      }

      // Capture raw conversation text for fingerprinting (hash only — never sent raw)
      const rawConversationText = options?.conversationText;

      // Step 1: Try data collection (unless manual mode)
      let identityData: IdentityData | null = null;
      let dataQuality = 0;
      let usedManualQA = false;
      let dimensions: { conviction: number; intuition: number; contribution: number } | undefined;

      // Step 1.5: Parse USER.md for static profile signals
      console.log('📋 Step 1.5: Parsing USER.md...');
      const userMdSignals = parseUserMd(options?.userMdPath);
      if (userMdSignals) {
        console.log(`✅ USER.md signals: role=${userMdSignals.role || 'none'}, focus=${userMdSignals.currentFocus?.join(', ') || 'none'}, style=${userMdSignals.workingStyle || 'none'}`);
      } else {
        console.log('📋 No USER.md found (graceful degradation)');
      }

      if (mode !== ExecutionMode.MANUAL) {
        console.log('📊 Step 1: Attempting data collection...');

        // ⭐ NEW: If conversationText is provided, use it directly
        let userData;
        if (options?.conversationText) {
          console.log('✅ Using provided conversation text (OpenClaw bot context)');
          userData = await this.dataCollector.collectFromConversationText(
            userId,
            options.conversationText,
            { skipTwitter: options.skipShare }
          );
        } else {
          // Original: Collect from session files
          userData = await this.dataCollector.collect(userId, {
            // Default: Conversation + Twitter only
          });
        }

        dataQuality = this.dataCollector.getDataQualityScore(userData);
        // Data quality is calculated but not displayed (cleaner output)
        console.log(`📊 Available sources: ${userData.sources.join(', ')}`);

        // ⭐ CRITICAL: Check if we have ANY real data (conversation OR Twitter)
        const hasConversation = userData.conversationMemory && userData.conversationMemory.messageCount > 0;
        const hasTwitter = userData.twitter && (userData.twitter.bio || userData.twitter.tweets.length > 0);

        if (!hasConversation && !hasTwitter) {
          console.log('⚠️  No conversation or Twitter data available');

          // In AUTO mode, fallback to manual Q&A
          if (mode === ExecutionMode.AUTO) {
            console.log('🔄 Falling back to manual Q&A (no data available)...');
            usedManualQA = true;
          } else {
            // DATA_ONLY mode - fail explicitly
            throw new Error('No conversation or Twitter data available and manual Q&A not enabled');
          }
        } else {
          // Check if we have sufficient data quality
          const hasSufficientData = this.dataCollector.hasSufficientData(userData);

          if (hasSufficientData) {
            console.log('✅ Sufficient data available, proceeding with AI analysis...');

            // Pre-compute dimension nudges from USER.md + feedback
            const preNudges = (userMdSignals || options?.feedback)
              ? mergeSignals(
                  [], // categories not needed yet, just computing nudges
                  { conviction: 0, intuition: 0, contribution: 0 },
                  userMdSignals,
                  options?.feedback ?? null,
                )
              : null;

            // Inject USER.md raw text as first-class signal source
            if (userMdSignals?.raw) {
              userData.userMdContent = Object.values(userMdSignals.raw).join('\n');
            }

            // Analyze personality from data (with optional dimension nudges)
            const analysis = await this.personalityAnalyzer.analyze(
              userData,
              preNudges?.dimensionNudges,
            );

            // Build identity from conversation analysis
            const conversationCategories = analysis.detectedCategories.length > 0
              ? analysis.detectedCategories
              : this.categoryMapper.getMainCategories(analysis.personalityType);

            // Step 2.5: Merge signals (conversation + USER.md + feedback)
            const merged = mergeSignals(
              conversationCategories,
              analysis.dimensions,
              userMdSignals,
              options?.feedback ?? null,
            );

            identityData = {
              personalityType: analysis.personalityType,
              customTagline: analysis.tagline,
              customDescription: analysis.description,
              customLongDescription: analysis.longDescription,
              mainCategories: merged.mainCategories,
              subCategories: [...analysis.detectedInterests, ...merged.subCategories.filter(
                s => !analysis.detectedInterests.includes(s),
              )],
              dimensions: analysis.dimensions,
              tasteSpectrums: analysis.dimensions.tasteSpectrums,
              strengths: analysis.strengths,
              hiddenInsight: analysis.hiddenInsight,
              aiPlaybook: analysis.aiPlaybook,
            };

            // ⭐ Capture 2x2 metrics
            dimensions = analysis.dimensions;

            if (userMdSignals || options?.feedback) {
              console.log(`✅ Signals merged: categories=${merged.mainCategories.join(', ')}`);
            }

            console.log(`✅ Analysis complete: ${identityData.personalityType}`);
          } else {
            console.log('⚠️  Insufficient data quality for AI analysis');

            // In AUTO mode, fallback to manual Q&A
            if (mode === ExecutionMode.AUTO) {
              console.log('🔄 Falling back to manual Q&A...');
              usedManualQA = true;
            } else {
              // DATA_ONLY mode - fail
              throw new Error('Insufficient data and manual Q&A not enabled');
            }
          }
        }
      } else {
        // MANUAL mode - go straight to Q&A
        console.log('📝 Manual mode enabled, skipping data collection');
        usedManualQA = true;
      }

      // Step 2: Manual Q&A if needed
      if (usedManualQA) {
        // If we don't have answers yet, request them from user
        if (!options?.manualAnswers) {
          console.log('❓ Manual input required from user');
          return {
            success: false,
            mode: 'manual',
            needsManualInput: true,
            manualQuestions: this.manualQA.formatQuestionsForUser(),
          };
        }

        console.log('🤔 Analyzing manual Q&A responses...');
        const manualResult = await this.manualQA.analyze(options.manualAnswers);

        identityData = {
          personalityType: manualResult.personalityType,
          customTagline: manualResult.tagline,
          customDescription: manualResult.description,
          customLongDescription: manualResult.description, // Manual QA uses same text for both
          mainCategories: manualResult.mainCategories,
          subCategories: manualResult.subCategories,
          tasteSpectrums: manualResult.tasteSpectrums,
        };

        dataQuality = manualResult.confidence;
        console.log(`✅ Manual analysis complete: ${identityData.personalityType}`);
      }

      // Step 3: Recommend OpenClaw Skills
      console.log('🔍 Step 3: Finding matching skills...');
      const merged = (userMdSignals || options?.feedback)
        ? mergeSignals(
            identityData!.mainCategories,
            identityData!.dimensions || { conviction: 50, intuition: 50, contribution: 50 },
            userMdSignals,
            options?.feedback ?? null,
          )
        : null;
      const recommendations = await this.recommendSkills(identityData!, merged);
      console.log(`✅ Found ${recommendations.length} matching skills`);

      // Step 4: Save identity card with Bloom API
      let dashboardUrl: string | undefined;
      let agentUserId: number | undefined;

      const identityPayload = {
        personalityType: identityData!.personalityType,
        tagline: identityData!.customTagline,
        description: identityData!.customDescription,
        longDescription: identityData!.customLongDescription,
        mainCategories: identityData!.mainCategories,
        subCategories: identityData!.subCategories,
        confidence: dataQuality,
        mode: (usedManualQA ? 'manual' : 'data') as 'data' | 'manual',
        dimensions,
        // LDP: noise spectrum scores before transmission (user sees originals)
        tasteSpectrums: identityData!.tasteSpectrums
          ? privatizeSpectrums(identityData!.tasteSpectrums)
          : undefined,
        strengths: identityData!.strengths,
        hiddenInsight: identityData!.hiddenInsight,
        aiPlaybook: identityData!.aiPlaybook,
        recommendations,
        // SHA-256 fingerprint of conversation (irreversible, for deduplication only)
        conversationHash: rawConversationText
          ? conversationFingerprint(rawConversationText)
          : undefined,
        privacyVersion: 'ldp-1.0',
      };

      let registration: { agentId: string; assignedTribe: string; isNew: boolean } | undefined;

      // Step 4: Save identity + sync discoveries IN PARALLEL
      console.log('📝 Step 4: Saving identity + registering agent...');
      const apiBase = process.env.BLOOM_API_URL || 'https://api.bloomprotocol.ai';

      // Fire both requests concurrently — don't wait for save before syncing
      const savePromise = fetch(`${apiBase}/x402/agent-save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agentName: 'Bloom Discovery Agent',
          identityData: identityPayload,
          platform: 'openclaw',
        }),
        signal: AbortSignal.timeout(6000),
      }).then(async response => {
        const body = await response.json();
        if (response.ok && body.data?.agentUserId) {
          agentUserId = body.data.agentUserId;
          console.log(`✅ Identity saved! Agent: ${agentUserId}`);

          if (body.data.assignedTribe) {
            registration = {
              agentId: `agent_${agentUserId}`,
              assignedTribe: body.data.assignedTribe,
              isNew: true,
            };
            console.log(`🔑 Registered → tribe ${body.data.assignedTribe}`);
            await saveAgentId(agentUserId, userId, {
              agentId: registration.agentId,
              assignedTribe: registration.assignedTribe,
            });
          } else {
            await saveAgentId(agentUserId, userId);
          }
        } else {
          console.error(`❌ API save failed: ${response.status}`, body.error || '');
        }
      }).catch(saveError => {
        console.error('❌ Identity save failed:', saveError instanceof Error ? saveError.message : saveError);
      });

      // Discovery sync runs in parallel with save (uses previous agentId if available)
      let discoveries: DiscoveryEntry[] = [];
      const storedIdForSync = (await loadStoredIdentityFile())?.agentUserId;

      const discoverPromise = storedIdForSync
        ? Promise.race([
            syncDiscoveries(storedIdForSync),
            new Promise<never>((_, reject) => setTimeout(() => reject(new Error('timeout')), 2000)),
          ]).then(syncResult => { discoveries = syncResult.newEntries; })
            .catch(err => { console.debug('[discovery-sync] failed:', err instanceof Error ? err.message : err); })
        : Promise.resolve();

      // Wait for both to finish
      await Promise.all([savePromise, discoverPromise]);

      if (agentUserId) {
        const baseUrl = process.env.DASHBOARD_URL || 'https://bloomprotocol.ai';
        dashboardUrl = `${baseUrl}/agents/${agentUserId}`;
        console.log(`✅ Dashboard: ${dashboardUrl}`);
      }

      // Step 5: Build discover URL (tribe-based, replaces legacy curated list)
      let discoverUrl: string | undefined;
      if (identityData) {
        const tribe = getRecommendedTribe(identityData.mainCategories);
        const baseUrl = process.env.DASHBOARD_URL || 'https://bloomprotocol.ai';
        discoverUrl = `${baseUrl}/discover/${tribe.id}`;
      }

      console.log('🎉 Bloom Identity generation complete!');

      // Prepare share data for frontend buttons
      const shareData = dashboardUrl ? {
        url: dashboardUrl,
        text: `Just discovered my Bloom Identity: ${identityData!.personalityType}! 🌸\n\nCheck out my personalized skill recommendations on @bloomprotocol 🚀`,
        hashtags: ['BloomProtocol', 'BloomDiscovery', 'OpenClaw'],
      } : undefined;

      // Card URL = lightweight embed (faster render), Dashboard URL = full page
      const cardUrl = dashboardUrl ? `${dashboardUrl}?view=card` : undefined;
      const claimUrl = dashboardUrl ? `${dashboardUrl}?intent=save` : undefined;

      return {
        success: true,
        mode: usedManualQA ? 'manual' : 'data',
        identityData: identityData!,
        recommendations,
        discoveries,
        dashboardUrl,
        cardUrl,     // Lighter card-only view (faster load)
        claimUrl,    // Direct URL to email registration + card save
        discoverUrl,
        dataQuality,
        dimensions,
        displayLabels: DISPLAY_LABELS,
        actions: {
          share: shareData,
          save: claimUrl ? {
            prompt: 'Register with email to claim your Bloom Identity Card',
            claimUrl,
            registerUrl: `${process.env.DASHBOARD_URL || 'https://bloomprotocol.ai'}/register?return=${encodeURIComponent(claimUrl)}`,
            loginUrl: `${process.env.DASHBOARD_URL || 'https://bloomprotocol.ai'}/login?return=${encodeURIComponent(claimUrl)}`,
          } : undefined,
        },
        registration,
      };
    } catch (error) {
      console.error('❌ Error generating Bloom Identity:', error);
      return {
        success: false,
        mode: 'data',
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  /**
   * Recommend skills grouped by user's main categories
   *
   * Delegates to the extracted recommendation-pipeline module so that
   * the same logic can be reused by the backend Bull queue refresh job.
   */
  private async recommendSkills(
    identity: IdentityData,
    merged?: MergedSignals | null,
  ): Promise<SkillRecommendation[]> {
    return refreshRecommendations({
      mainCategories: identity.mainCategories,
      subCategories: identity.subCategories,
      personalityType: identity.personalityType,
      dimensions: identity.dimensions,
      tasteSpectrums: identity.tasteSpectrums,
      feedback: merged ? {
        categoryWeights: merged.categoryWeights,
        excludeSkillIds: merged.excludedSkillIds,
      } : undefined,
    });
  }
}

// ── Tribe mapping ───────────────────────────────────────────────────

/** Map identity categories to the best-fit tribe. */
function getRecommendedTribe(categories: string[]): { id: string; name: string; tagline: string } {
  const catSet = new Set(categories.map(c => c.toLowerCase()));

  // Grow: marketing, design, productivity, wellness, education, lifestyle
  if (['marketing', 'design', 'productivity', 'wellness', 'education', 'lifestyle'].some(c => catSet.has(c))) {
    return { id: 'grow', name: 'Grow', tagline: 'Content, SEO, GEO, distribution — being found, getting chosen' };
  }
  // Raise: finance, crypto, prediction market
  if (['finance', 'crypto', 'prediction market'].some(c => catSet.has(c))) {
    return { id: 'raise', name: 'Raise', tagline: 'Agent-powered project evaluation and community signal' };
  }
  // Build: agent framework, context engineering, mcp ecosystem, coding assistant, ai tools, development (default)
  return { id: 'build', name: 'Build', tagline: 'From zero to production agent — setup, skills, workflows' };
}

// ── Discovery mode helpers ──────────────────────────────────────────

/** Detect which mode the user wants based on their trigger / message text. */
function detectMode(text: string): 'identity' | 'browse' | 'categories' {
  const lower = text.toLowerCase();
  if (/categor/i.test(lower)) return 'categories';
  if (/show|find|search|browse|recommend|available|skills?\s*(for|about|in)/i.test(lower))
    return 'browse';
  return 'identity';
}

/** Extract category + freetext search from a natural-language query. */
function parseSearchIntent(text: string): { category?: string; search?: string } {
  const lower = text.toLowerCase();
  // Try exact display category match first (e.g. "Agent & MCP", "AI Tools")
  for (const cat of DISPLAY_CATEGORIES) {
    if (lower.includes(cat.toLowerCase())) return { category: cat };
  }
  // Common aliases → display categories
  if (/\bmcp\b/i.test(lower)) return { category: 'Agent & MCP' };
  if (/\bagent\b/i.test(lower)) return { category: 'Agent & MCP' };
  if (/\brag\b|\bembedding/i.test(lower)) return { category: 'Agent & MCP' };
  if (/\bai\b/i.test(lower)) return { category: 'AI Tools' };
  if (/\bdev\b|coding|code\b/i.test(lower)) return { category: 'Development' };
  if (/\bcrypto|web3|defi\b/i.test(lower)) return { category: 'Crypto' };
  if (/\bdesign|figma|ui\b/i.test(lower)) return { category: 'Design' };
  if (/\bmarketing|seo|growth\b/i.test(lower)) return { category: 'Marketing' };
  if (/\bfinance|trading|invest/i.test(lower)) return { category: 'Finance' };
  if (/\bwellness|health|meditat/i.test(lower)) return { category: 'Wellness' };
  if (/\beducat|learn|course/i.test(lower)) return { category: 'Education' };
  if (/\bproductiv|automat|workflow/i.test(lower)) return { category: 'Productivity' };
  // Fallback: extract freetext after common verbs
  const match = lower.match(/(?:find|search|show me|browse)\s+(?:skills?\s+)?(?:for\s+|about\s+|in\s+)?(.+)/i);
  if (match) return { search: match[1].trim() };
  return {};
}

/** Call GET /skills with optional filters. */
async function browseSkills(intent: { category?: string; search?: string }): Promise<string> {
  const apiBase = process.env.BLOOM_API_URL || 'https://api.bloomprotocol.ai';
  const params = new URLSearchParams();
  if (intent.category) params.set('category', intent.category);
  if (intent.search) params.set('search', intent.search);
  params.set('limit', '10');
  params.set('sort', 'score');

  const res = await fetch(`${apiBase}/skills?${params}`, { signal: AbortSignal.timeout(10000) });
  if (!res.ok) throw new Error(`Skills API returned ${res.status}`);
  const body = await res.json() as any;
  const skills: Array<{ name: string; slug: string; description: string; stars: number; source: string; url: string }> = body.data?.skills || [];

  return formatBrowseResults(skills, intent);
}

/** Call GET /skills/categories. */
async function fetchCategories(): Promise<string> {
  const apiBase = process.env.BLOOM_API_URL || 'https://api.bloomprotocol.ai';
  const res = await fetch(`${apiBase}/skills/categories`, { signal: AbortSignal.timeout(10000) });
  if (!res.ok) throw new Error(`Categories API returned ${res.status}`);
  const body = await res.json() as any;
  const categories: Array<{ name: string; count: number }> = body.data?.categories || [];

  return formatCategoriesList(categories);
}

function formatBrowseResults(
  skills: Array<{ name: string; slug: string; description: string; stars: number; source: string; url: string }>,
  intent: { category?: string; search?: string },
): string {
  if (skills.length === 0) {
    const query = intent.search || intent.category || 'your search';
    return `No skills found for "${query}". Try browsing by category — say "skill categories" to see what's available.`;
  }

  const heading = intent.category
    ? `**${intent.category}** skills`
    : intent.search
      ? `Skills matching "${intent.search}"`
      : 'Top skills';

  let msg = `🔍 ${heading} (${skills.length} results)\n`;
  for (const s of skills) {
    const stars = s.stars > 0 ? ` ⭐ ${s.stars}` : '';
    msg += `\n- **${s.name}**${stars}\n  ${s.description?.slice(0, 120) || ''}\n  ${s.url}`;
  }

  msg += `\n\n💡 Say "show me [category]" to filter, or "generate my bloom identity" to get personalized recommendations.`;
  return msg;
}

function formatCategoriesList(
  categories: Array<{ name: string; count: number }>,
): string {
  if (categories.length === 0) return 'No categories available yet.';

  let msg = '📂 **Skill Categories**\n';
  for (const c of categories.sort((a, b) => b.count - a.count)) {
    msg += `\n- **${c.name}** — ${c.count} skills`;
  }
  msg += `\n\n💡 Say "show me [category name]" to browse skills in a category.`;
  return msg;
}

// ── Skill registration for OpenClaw ─────────────────────────────────

export const bloomDiscoverySkill = {
  name: 'bloom-discovery',
  description: 'Generate your personalized Bloom Identity Card, browse skills, and discover matching projects',
  version: '4.0.1',
  aliases: ['bloom-identity'],

  triggers: [
    // Identity triggers (existing)
    'generate my bloom identity',
    'create my identity card',
    'analyze my supporter profile',
    'create my bloom card',
    'discover my personality',
    'regenerate my bloom identity',
    'reset my bloom identity',
    // Browse triggers (new)
    'show me skills',
    'find skills',
    'search skills',
    'browse skills',
    'recommend skills',
    'what skills are available',
    // Category triggers (new)
    'skill categories',
    'list categories',
    'what categories',
  ],

  async execute(context: any) {
    const mode = detectMode(context.trigger || context.message || '');

    // ── Categories mode ──
    if (mode === 'categories') {
      try {
        const msg = await fetchCategories();
        return { message: msg, data: { mode: 'categories' } };
      } catch (err: any) {
        return { message: `Failed to fetch categories: ${err.message}`, data: { mode: 'categories', error: true } };
      }
    }

    // ── Browse mode ──
    if (mode === 'browse') {
      try {
        const intent = parseSearchIntent(context.trigger || context.message || '');
        const msg = await browseSkills(intent);
        return { message: msg, data: { mode: 'browse', ...intent } };
      } catch (err: any) {
        return { message: `Failed to browse skills: ${err.message}`, data: { mode: 'browse', error: true } };
      }
    }

    // ── Identity mode ──
    // OpenClaw writes conversation history to session files on disk
    // (~/.openclaw/agents/main/sessions/). The skill reads those files
    // via collect() → collectConversationMemory() to get ~120 messages
    // of past conversation. We intentionally do NOT pass conversationText
    // here — session files contain richer historical data.
    const skill = new BloomIdentitySkillV2();

    const manualAnswers = context.manualAnswers;
    // Detect regeneration intent from trigger text (e.g. "regenerate my bloom identity")
    const triggerText = context.trigger || context.message || '';
    const wantsRegenerate = context.forceRegenerate || /\b(regenerate|redo|reset|refresh)\b/i.test(triggerText);

    const result = await skill.execute(context.userId, {
      mode: ExecutionMode.AUTO,
      skipShare: !context.enableShare,
      manualAnswers,
      forceRegenerate: wantsRegenerate,
      feedback: context.feedback,
      userMdPath: context.userMdPath,
    });

    if (!result.success) {
      if (result.needsManualInput) {
        // Return questions to user
        return {
          message: result.manualQuestions,
          data: { awaitingManualInput: true, mode: 'identity' },
        };
      }

      return {
        message: `❌ Failed to generate identity: ${result.error}`,
        data: { ...result, mode: 'identity' },
      };
    }

    return {
      message: formatSuccessMessage(result),
      data: { ...result, mode: 'identity' },
    };
  },
};

/** @deprecated Use bloomDiscoverySkill instead */
export const bloomIdentitySkillV2 = bloomDiscoverySkill;

/**
 * Format success message for OpenClaw agent reply.
 *
 * Structure:
 *   1. Card link (most important)
 *   2. Personality + tagline + description
 *   3. MentalOS Spectrum (4 axes)
 *   4. Hidden insight
 *   5. AI Playbook (actionable advice)
 *   6. Skill recommendations (inline top 3 + discover link)
 */
function formatSuccessMessage(result: any): string {
  const { identityData, recommendations } = result;
  const emoji = getPersonalityEmoji(identityData.personalityType);

  let msg = '';

  // 1. Card link — always first, with returning user greeting
  if (result.isReturningUser && result.dashboardUrl) {
    msg += `🌸 **Welcome back, ${identityData.personalityType}!**`;
    msg += `\n🔗 ${result.dashboardUrl}`;
    if (result.discoveries?.length > 0) {
      msg += `\n📊 ${result.discoveries.length} new skill${result.discoveries.length > 1 ? 's' : ''} discovered since last visit`;
    }
    msg += `\n`;
  } else if (result.dashboardUrl) {
    msg += `🌸 **Your Bloom Identity Card is ready!**`;
    msg += `\n🔗 ${result.dashboardUrl}`;
    msg += `\n`;
  } else {
    msg += `🌸 **Bloom Identity generated!**\n`;
  }

  // 2. Personality + description
  msg += `\n${emoji} **${identityData.personalityType}** — "${identityData.customTagline}"`;
  msg += `\n\n${identityData.customLongDescription || identityData.customDescription}`;

  // 3. MentalOS Spectrum
  if (identityData.tasteSpectrums) {
    const s = identityData.tasteSpectrums;
    msg += `\n\n🧠 **MentalOS**`;
    msg += `\n├ Learning: ${formatSpectrum(s.learning, 'Try First', 'Study First')}`;
    msg += `\n├ Decision: ${formatSpectrum(s.decision, 'Gut', 'Analytical')}`;
    msg += `\n├ Novelty:  ${formatSpectrum(s.novelty, 'Early Adopter', 'Proven First')}`;
    msg += `\n└ Risk:     ${formatSpectrum(s.risk, 'All In', 'Measured')}`;
  }

  // 4. Hidden insight
  if (identityData.hiddenInsight) {
    msg += `\n\n🔍 *${identityData.hiddenInsight.brief}*`;
  }

  // 5. AI Playbook
  if (identityData.aiPlaybook) {
    msg += `\n\n📖 **Your AI Playbook**`;
    msg += `\n⚡ **Leverage:** ${identityData.aiPlaybook.leverage}`;
    msg += `\n⚠️ **Watch out:** ${identityData.aiPlaybook.watchOut}`;
    msg += `\n🎯 **Next move:** ${identityData.aiPlaybook.nextMove}`;
  }

  // 6. Categories
  msg += `\n\n🏷️ ${identityData.mainCategories.join(' • ')}`;

  // 7. Skill recommendations
  if (recommendations?.length > 0) {
    if (result.discoverUrl) {
      // Show top 3 inline + full list link
      msg += `\n\n🔍 **${recommendations.length} skills matched to your profile:**`;
      for (const r of recommendations.slice(0, 3)) {
        msg += `\n- ${r.skillName} (${r.matchScore}pts)`;
      }
      if (recommendations.length > 3) {
        msg += `\n- ...and ${recommendations.length - 3} more`;
      }
      msg += `\n🔗 ${result.discoverUrl}`;
    } else {
      // No curated list link — show top 5 inline
      msg += `\n\n🔍 **Top skills for you:**`;
      for (const r of recommendations.slice(0, 5)) {
        msg += `\n- [${r.skillName}](${r.url}) — ${r.matchScore}pts`;
      }
    }
  }

  // 8. Email registration CTA — the key conversion action
  if (result.claimUrl) {
    msg += `\n\n📧 **Claim your card** — register with email to save it to your Bloom collection:`;
    msg += `\n→ ${result.claimUrl}`;
  }

  // 9. Registration status
  if (result.registration) {
    const reg = result.registration;
    const tribeName = reg.assignedTribe.charAt(0).toUpperCase() + reg.assignedTribe.slice(1);
    if (reg.isNew) {
      msg += `\n\n🏛 **Tribe: ${tribeName}** — your agent is registered and will be recognized next time.`;
    } else {
      msg += `\n\n🏛 Tribe: **${tribeName}**`;
    }
  } else {
    // Still show tribe recommendation even without registration
    const tribe = getRecommendedTribe(identityData.mainCategories);
    msg += `\n\n🏛 **Your tribe: ${tribe.name}** — ${tribe.tagline}`;
  }

  return msg;
}

/** Format a spectrum value as a visual bar */
function formatSpectrum(value: number, lowLabel: string, highLabel: string): string {
  const position = Math.round(value / 10);
  const bar = '─'.repeat(position) + '●' + '─'.repeat(10 - position);
  const label = value < 35 ? lowLabel : value > 65 ? highLabel : 'Balanced';
  return `[${bar}] ${value} — ${label}`;
}

function getPersonalityEmoji(type: PersonalityType): string {
  const emojiMap = {
    [PersonalityType.THE_VISIONARY]: '💜',
    [PersonalityType.THE_EXPLORER]: '💚',
    [PersonalityType.THE_CULTIVATOR]: '🩵',
    [PersonalityType.THE_OPTIMIZER]: '🧡',
    [PersonalityType.THE_INNOVATOR]: '💙',
  };
  return emojiMap[type] || '🎴';
}

export default bloomDiscoverySkill;
