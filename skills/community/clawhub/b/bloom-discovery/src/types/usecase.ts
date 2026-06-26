/**
 * Use Case Types
 *
 * Defines the use case model for intent-driven skill discovery.
 * A use case is a curated combination of skills that solve a real problem.
 */

export interface UseCaseSkill {
  id: string;
  name: string;
  slug: string;
  verifyBy: string[]; // clawhub slugs to check in ~/.openclaw/skills/
}

export interface UseCase {
  id: string;
  name: string;
  description: string;
  category: string;
  skills: UseCaseSkill[];
  tier: 1 | 2 | 3; // 1 = essential, 2 = advanced, 3 = experimental
  claimCount: number;
  tags: string[];
  createdAt: string;
}

export interface MissingCapability {
  skillName: string;
  slug: string;
  clawhubUrl: string;
  downloadCount?: number;
  reason: string;
}

export interface VerifyResult {
  useCaseId: string;
  useCaseName: string;
  matched: boolean;
  matchedSkills: string[];
  missingSkills: string[];
  missingCapabilities: MissingCapability[];
  matchPercentage: number;
  tier: 1 | 2 | 3;
}

export interface UseCaseRecommendation {
  useCase: UseCase;
  score: number;
  reasons: string[];
  verifyResult?: VerifyResult;
}

export interface ClaimRequest {
  useCaseId: string;
  walletAddress?: string;
}

export interface ClaimResponse {
  success: boolean;
  method: 'mint' | 'web-link';
  mintTx?: string;
  webUrl?: string;
  message: string;
}

export interface UsageMetric {
  skillName: string;
  slug: string;
  installDays: number;
  usageCount: number;
  lastUsed?: string;
}

export interface MetricsPayload {
  userId: string;
  metrics: UsageMetric[];
  reportedAt: string;
}
