/**
 * Configuration Verifier
 *
 * Verifies installed skills against use case requirements
 * and recommends missing skills with ClawHub links.
 */

import type { UseCase, VerifyResult, MissingCapability } from '../types/usecase';
import { matchUseCase, matchUseCases } from './matcher';

export interface VerificationReport {
  useCaseId: string;
  useCaseName: string;
  result: VerifyResult;
  recommendations: SkillRecommendation[];
  summary: string;
}

export interface SkillRecommendation {
  name: string;
  slug: string;
  clawhubUrl: string;
  installCommand: string;
  downloadCount?: number;
  reason: string;
}

/**
 * Build install recommendations from missing capabilities.
 */
function buildRecommendations(
  missing: MissingCapability[]
): SkillRecommendation[] {
  return missing.map((cap) => ({
    name: cap.skillName,
    slug: cap.slug,
    clawhubUrl: cap.clawhubUrl,
    installCommand: `clawhub install ${cap.slug}`,
    downloadCount: cap.downloadCount,
    reason: cap.reason,
  }));
}

/**
 * Generate a human-readable summary of the verification result.
 */
function buildSummary(result: VerifyResult): string {
  if (result.matched) {
    return `All ${result.matchedSkills.length} required skills are installed. You're ready to claim the "${result.useCaseName}" SBT.`;
  }

  const total = result.matchedSkills.length + result.missingSkills.length;
  return (
    `${result.matchPercentage}% complete (${result.matchedSkills.length}/${total} skills installed). ` +
    `Missing: ${result.missingSkills.join(', ')}. ` +
    `Install them to unlock the "${result.useCaseName}" use case.`
  );
}

/**
 * Verify a single use case and produce a full report.
 */
export function verifyUseCase(useCase: UseCase): VerificationReport {
  const result = matchUseCase(useCase);
  const recommendations = buildRecommendations(result.missingCapabilities);
  const summary = buildSummary(result);

  return {
    useCaseId: useCase.id,
    useCaseName: useCase.name,
    result,
    recommendations,
    summary,
  };
}

/**
 * Quick check: which use cases does the user fully satisfy?
 */
export function getReadyUseCases(useCases: UseCase[]): UseCase[] {
  const results = matchUseCases(useCases);
  const readyIds = new Set(
    results.filter((r) => r.matched).map((r) => r.useCaseId)
  );
  return useCases.filter((uc) => readyIds.has(uc.id));
}
