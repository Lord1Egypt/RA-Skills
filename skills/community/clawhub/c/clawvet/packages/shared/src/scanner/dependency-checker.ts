import type { Finding, ParsedSkill } from "../types.js";

const NPX_AUTO_INSTALL_RE = /npx\s+-y\s+/gi;
const NPM_INSTALL_RE = /npm\s+install\s+(-g\s+)?(\S+)/gi;

export function checkDependencies(skill: ParsedSkill): Finding[] {
  const findings: Finding[] = [];
  const pass = "dependency-checker";

  let match: RegExpExecArray | null;
  const npxRe = new RegExp(NPX_AUTO_INSTALL_RE.source, NPX_AUTO_INSTALL_RE.flags);

  while ((match = npxRe.exec(skill.rawContent)) !== null) {
    const before = skill.rawContent.slice(0, match.index);
    const lineNumber = before.split("\n").length;

    findings.push({
      category: "dependency_risk",
      severity: "medium",
      title: "npx auto-install (-y flag)",
      description: "Uses 'npx -y' which auto-installs packages without user confirmation.",
      evidence: match[0],
      lineNumber,
      analysisPass: pass,
      fix: "Remove the `-y` flag from npx to require user confirmation before installing.",
    });
  }

  const npmRe = new RegExp(NPM_INSTALL_RE.source, NPM_INSTALL_RE.flags);
  while ((match = npmRe.exec(skill.rawContent)) !== null) {
    if (match[1]) {
      findings.push({
        category: "dependency_risk",
        severity: "medium",
        title: "Global npm package install",
        description: `Installs npm package globally: ${match[2]}`,
        evidence: match[0],
        analysisPass: pass,
        fix: "Use a local install (`npm install` without `-g`) or declare the dependency in requires.bins.",
      });
    }
  }

  return findings;
}
