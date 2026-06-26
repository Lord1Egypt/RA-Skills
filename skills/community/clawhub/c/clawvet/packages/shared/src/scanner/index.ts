import type { Finding, ScanResult } from "../types.js";
import { parseSkill } from "./skill-parser.js";
import { runStaticAnalysis } from "./static-analysis.js";
import { validateMetadata } from "./metadata-validator.js";
import { checkDependencies } from "./dependency-checker.js";
import { detectTyposquats } from "./typosquat-detector.js";
import { calculateRiskScore, getRiskGrade, countFindings } from "./risk-scorer.js";
import { getCached, setCached } from "./cache.js";

export interface ScanOptions {
  semantic?: boolean;
  semanticAnalyzer?: (content: string) => Promise<Finding[]>;
  ignorePatterns?: string[];
  skipCache?: boolean;
}

export async function scanSkill(
  content: string,
  options: ScanOptions = {}
): Promise<ScanResult> {
  if (!options.skipCache) {
    const cached = getCached(content);
    if (cached) {
      return { ...cached, cached: true };
    }
  }

  const skill = parseSkill(content);
  const allFindings: Finding[] = [];

  allFindings.push(...runStaticAnalysis(skill));
  allFindings.push(...validateMetadata(skill));

  if (options.semantic && options.semanticAnalyzer) {
    const semanticFindings = await options.semanticAnalyzer(content);
    allFindings.push(...semanticFindings);
  }

  allFindings.push(...checkDependencies(skill));

  if (skill.frontmatter.name) {
    allFindings.push(...detectTyposquats(skill.frontmatter.name));
  }

  // Filter out ignored patterns
  const filteredFindings = options.ignorePatterns?.length
    ? allFindings.filter(
        (f) => !options.ignorePatterns!.some((ig) => f.title === ig || f.category === ig)
      )
    : allFindings;

  const riskScore = calculateRiskScore(filteredFindings);
  const riskGrade = getRiskGrade(riskScore);
  const findingsCount = countFindings(filteredFindings);

  const recommendation =
    riskScore >= 76 ? "block" : riskScore >= 26 ? "warn" : "approve";

  const result: ScanResult = {
    skillName: skill.frontmatter.name || "unknown",
    skillVersion: skill.frontmatter.version,
    skillSource: "local",
    status: "complete",
    riskScore,
    riskGrade,
    findingsCount,
    findings: filteredFindings,
    recommendation,
  };

  if (!options.skipCache) {
    setCached(content, result);
  }

  return result;
}

export { parseSkill } from "./skill-parser.js";
export { runStaticAnalysis } from "./static-analysis.js";
export { validateMetadata } from "./metadata-validator.js";
export { checkDependencies } from "./dependency-checker.js";
export { detectTyposquats } from "./typosquat-detector.js";
export { calculateRiskScore, getRiskGrade, countFindings } from "./risk-scorer.js";
