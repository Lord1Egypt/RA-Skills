import type { Finding, ParsedSkill } from "../types.js";

const SEMVER_RE = /^\d+\.\d+\.\d+/;

const KNOWN_BINS = [
  "curl", "wget", "git", "python", "python3", "node", "npm", "npx",
  "brew", "apt", "pip", "docker", "kubectl", "ssh", "scp", "rsync",
  "ffmpeg", "jq", "sed", "awk", "grep", "find",
];

export function validateMetadata(skill: ParsedSkill): Finding[] {
  const findings: Finding[] = [];
  const fm = skill.frontmatter;
  const pass = "metadata-validator";

  if (!fm.name) {
    findings.push({
      category: "metadata",
      severity: "medium",
      title: "Missing skill name",
      description: "SKILL.md frontmatter does not declare a name.",
      analysisPass: pass,
      fix: "Add `name:` to the YAML frontmatter.",
    });
  }

  if (!fm.description) {
    findings.push({
      category: "metadata",
      severity: "medium",
      title: "Missing description",
      description: "SKILL.md frontmatter does not declare a description.",
      analysisPass: pass,
      fix: "Add `description:` to the YAML frontmatter.",
    });
  } else if (fm.description.length < 10) {
    findings.push({
      category: "metadata",
      severity: "low",
      title: "Vague description",
      description: "Skill description is suspiciously short.",
      evidence: fm.description,
      analysisPass: pass,
      fix: "Write a more detailed description (at least 10 characters).",
    });
  }

  if (fm.version && !SEMVER_RE.test(fm.version)) {
    findings.push({
      category: "metadata",
      severity: "low",
      title: "Invalid version format",
      description: "Version does not follow semver format.",
      evidence: fm.version,
      analysisPass: pass,
      fix: "Use semver format: `version: X.Y.Z` (e.g., `1.0.0`).",
    });
  }

  const declaredBins = new Set(fm.metadata?.openclaw?.requires?.bins || []);

  for (const bin of KNOWN_BINS) {
    const binRe = new RegExp(`\\b${bin}\\b`, "i");
    if (binRe.test(skill.rawContent) && !declaredBins.has(bin)) {
      const usedInCode = skill.codeBlocks.some((cb) => binRe.test(cb.content));
      if (usedInCode) {
        findings.push({
          category: "metadata",
          severity: "low",
          title: `Undeclared binary: ${bin}`,
          description: `Skill uses '${bin}' in code but does not declare it in requires.bins.`,
          analysisPass: pass,
          fix: `Add '${bin}' to \`metadata.openclaw.requires.bins\` in frontmatter.`,
        });
      }
    }
  }

  const declaredEnv = new Set(fm.metadata?.openclaw?.requires?.env || []);
  const envRe = /\$\{?([A-Z][A-Z0-9_]+)\}?/g;
  let match: RegExpExecArray | null;

  while ((match = envRe.exec(skill.rawContent)) !== null) {
    const envVar = match[1];
    if (!declaredEnv.has(envVar) && envVar.length > 2) {
      findings.push({
        category: "metadata",
        severity: "low",
        title: `Undeclared env var: ${envVar}`,
        description: `References environment variable $${envVar} but does not declare it in requires.env.`,
        evidence: match[0],
        analysisPass: pass,
        fix: `Add '${envVar}' to \`metadata.openclaw.requires.env\` in frontmatter.`,
      });
    }
  }

  return findings;
}
