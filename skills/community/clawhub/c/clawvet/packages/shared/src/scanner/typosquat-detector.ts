import { distance } from "fastest-levenshtein";
import { POPULAR_SKILLS } from "../patterns.js";
import type { Finding } from "../types.js";

const MAX_EDIT_DISTANCE = 2;

export function detectTyposquats(skillName: string): Finding[] {
  if (!skillName) return [];

  const findings: Finding[] = [];
  const normalized = skillName.toLowerCase().trim();

  for (const popular of POPULAR_SKILLS) {
    if (normalized === popular) continue;

    const d = distance(normalized, popular);
    if (d > 0 && d <= MAX_EDIT_DISTANCE) {
      findings.push({
        category: "typosquatting",
        severity: "high",
        title: `Possible typosquat of "${popular}"`,
        description: `Skill name "${skillName}" is ${d} edit(s) away from popular skill "${popular}". This may be an attempt to impersonate a trusted skill.`,
        evidence: `"${skillName}" ≈ "${popular}" (distance: ${d})`,
        analysisPass: "typosquat-detector",
      });
    }
  }

  const patterns = [
    { re: /-{2,}/, desc: "extra hyphens" },
    { re: /(.)\1{2,}/, desc: "repeated characters" },
  ];

  for (const p of patterns) {
    if (p.re.test(normalized) && !POPULAR_SKILLS.includes(normalized)) {
      findings.push({
        category: "typosquatting",
        severity: "medium",
        title: `Suspicious naming pattern: ${p.desc}`,
        description: `Skill name "${skillName}" has ${p.desc}, which is a common typosquatting technique.`,
        analysisPass: "typosquat-detector",
      });
    }
  }

  return findings;
}
