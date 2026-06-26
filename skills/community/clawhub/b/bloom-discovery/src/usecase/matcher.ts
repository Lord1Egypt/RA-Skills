/**
 * Use Case Matcher
 *
 * Reads installed skills from ~/.openclaw/skills/ and compares them
 * against use case requirements to produce a VerifyResult.
 */

import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import type { UseCase, VerifyResult, MissingCapability } from '../types/usecase';

const OPENCLAW_SKILLS_DIR = path.join(
  os.homedir(),
  '.openclaw',
  'skills'
);

const CLAWHUB_BASE_URL = 'https://clawhub.ai';

/**
 * Get list of installed skill slugs from the local OpenClaw directory.
 */
export function getInstalledSkills(): string[] {
  try {
    if (!fs.existsSync(OPENCLAW_SKILLS_DIR)) {
      return [];
    }
    const entries = fs.readdirSync(OPENCLAW_SKILLS_DIR, {
      withFileTypes: true,
    });
    return entries
      .filter((e) => e.isDirectory())
      .map((e) => e.name);
  } catch {
    return [];
  }
}

/**
 * Match installed skills against a single use case's requirements.
 * Pass pre-computed installedSkills to avoid repeated filesystem reads.
 */
export function matchUseCase(
  useCase: UseCase,
  installedSkills?: Set<string>
): VerifyResult {
  const installed = installedSkills ?? new Set(getInstalledSkills());
  const matchedSkills: string[] = [];
  const missingSkills: string[] = [];
  const missingCapabilities: MissingCapability[] = [];

  for (const skill of useCase.skills) {
    // Check if any of the verifyBy slugs are installed
    const found = skill.verifyBy.some((slug) => installed.has(slug));

    if (found) {
      matchedSkills.push(skill.name);
    } else {
      missingSkills.push(skill.name);
      missingCapabilities.push({
        skillName: skill.name,
        slug: skill.slug,
        clawhubUrl: `${CLAWHUB_BASE_URL}/${skill.slug}`,
        reason: `Required for "${useCase.name}" use case`,
      });
    }
  }

  const totalSkills = useCase.skills.length;
  const matchPercentage =
    totalSkills > 0 ? Math.round((matchedSkills.length / totalSkills) * 100) : 0;

  return {
    useCaseId: useCase.id,
    useCaseName: useCase.name,
    matched: missingSkills.length === 0,
    matchedSkills,
    missingSkills,
    missingCapabilities,
    matchPercentage,
    tier: useCase.tier,
  };
}

/**
 * Match installed skills against multiple use cases.
 * Returns results sorted by match percentage (highest first).
 */
export function matchUseCases(useCases: UseCase[]): VerifyResult[] {
  const installed = new Set(getInstalledSkills());
  return useCases
    .map((uc) => matchUseCase(uc, installed))
    .sort((a, b) => b.matchPercentage - a.matchPercentage);
}
