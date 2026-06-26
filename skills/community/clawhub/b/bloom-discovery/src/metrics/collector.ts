/**
 * Metrics Collector
 *
 * Reads local OpenClaw skill directory to compute usage statistics.
 * All data stays local until explicitly reported via reporter.ts.
 */

import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import type { UsageMetric } from '../types/usecase';

const OPENCLAW_SKILLS_DIR = path.join(
  os.homedir(),
  '.openclaw',
  'skills'
);

const OPENCLAW_WORKSPACE_DIR = path.join(
  os.homedir(),
  '.openclaw',
  'workspace'
);

/**
 * Compute how many days a skill has been installed,
 * based on directory creation time.
 */
function getInstallDays(dirPath: string): number {
  try {
    const stats = fs.statSync(dirPath);
    const installDate = stats.birthtime;
    const now = new Date();
    const diffMs = now.getTime() - installDate.getTime();
    return Math.max(1, Math.floor(diffMs / (1000 * 60 * 60 * 24)));
  } catch {
    return 0;
  }
}

/**
 * Validate that a slug is safe for path construction (no traversal).
 */
function isValidSlug(slug: string): boolean {
  return !slug.includes('..') && !slug.includes('/') && !slug.includes('\\');
}

/**
 * Estimate usage count from log files or session references.
 * Heuristic: count files modified in the skill workspace directory.
 */
function estimateUsageCount(skillSlug: string): number {
  if (!isValidSlug(skillSlug)) return 0;
  try {
    const workspaceDir = path.join(OPENCLAW_WORKSPACE_DIR, skillSlug);
    if (!fs.existsSync(workspaceDir)) {
      return 0;
    }

    // Count recently modified files as a usage proxy
    const files = fs.readdirSync(workspaceDir);
    let modifiedCount = 0;
    const thirtyDaysAgo = Date.now() - 30 * 24 * 60 * 60 * 1000;

    for (const file of files) {
      try {
        const filePath = path.join(workspaceDir, file);
        const stats = fs.statSync(filePath);
        if (stats.mtimeMs > thirtyDaysAgo) {
          modifiedCount++;
        }
      } catch {
        // skip unreadable files
      }
    }

    return modifiedCount;
  } catch {
    return 0;
  }
}

/**
 * Get the last usage timestamp for a skill.
 */
function getLastUsed(skillSlug: string): string | undefined {
  if (!isValidSlug(skillSlug)) return undefined;
  try {
    const workspaceDir = path.join(OPENCLAW_WORKSPACE_DIR, skillSlug);
    if (!fs.existsSync(workspaceDir)) {
      return undefined;
    }
    const stats = fs.statSync(workspaceDir);
    return stats.mtime.toISOString();
  } catch {
    return undefined;
  }
}

/**
 * Collect usage metrics for all installed skills.
 * Returns only aggregated data: skill name + install days + usage count.
 * No conversation content, no personal data.
 */
export function collectMetrics(): UsageMetric[] {
  const metrics: UsageMetric[] = [];

  try {
    if (!fs.existsSync(OPENCLAW_SKILLS_DIR)) {
      return [];
    }

    const entries = fs.readdirSync(OPENCLAW_SKILLS_DIR, {
      withFileTypes: true,
    });

    for (const entry of entries) {
      if (!entry.isDirectory()) continue;

      const slug = entry.name;
      const skillDir = path.join(OPENCLAW_SKILLS_DIR, slug);

      metrics.push({
        skillName: slug,
        slug,
        installDays: getInstallDays(skillDir),
        usageCount: estimateUsageCount(slug),
        lastUsed: getLastUsed(slug),
      });
    }
  } catch {
    // Silently fail — metrics are opt-in and non-critical
  }

  return metrics;
}
