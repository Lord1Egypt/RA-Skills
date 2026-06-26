import type { Finding, FindingsCount, RiskGrade } from "../types.js";

const SEVERITY_WEIGHTS = {
  critical: 30,
  high: 15,
  medium: 7,
  low: 3,
} as const;

export function calculateRiskScore(findings: Finding[]): number {
  let score = 0;
  for (const f of findings) {
    score += SEVERITY_WEIGHTS[f.severity] * (f.confidence ?? 1.0);
  }
  return Math.min(score, 100);
}

export function getRiskGrade(score: number): RiskGrade {
  if (score <= 10) return "A";
  if (score <= 25) return "B";
  if (score <= 50) return "C";
  if (score <= 75) return "D";
  return "F";
}

export function countFindings(findings: Finding[]): FindingsCount {
  const counts: FindingsCount = { critical: 0, high: 0, medium: 0, low: 0 };
  for (const f of findings) {
    counts[f.severity]++;
  }
  return counts;
}
