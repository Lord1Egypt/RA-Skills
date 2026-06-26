import { readFileSync, existsSync, statSync } from "node:fs";
import { resolve, join } from "node:path";
import chalk from "chalk";
import { scanSkill } from "@clawvet/shared";
import type { RiskGrade } from "@clawvet/shared";

const GRADE_COLORS: Record<RiskGrade, string> = {
  A: "brightgreen",
  B: "green",
  C: "yellow",
  D: "orange",
  F: "red",
};

const GRADE_LABELS: Record<RiskGrade, string> = {
  A: "safe",
  B: "safe",
  C: "review",
  D: "risky",
  F: "dangerous",
};

export async function badgeCommand(
  target: string,
  options: { markdown?: boolean }
): Promise<void> {
  const skillPath = resolve(target);
  let skillFile = skillPath;

  if (
    existsSync(skillPath) &&
    !skillPath.endsWith(".md") &&
    existsSync(join(skillPath, "SKILL.md"))
  ) {
    skillFile = join(skillPath, "SKILL.md");
  }

  if (!existsSync(skillFile) || statSync(skillFile).isDirectory()) {
    console.error(`Error: Cannot find SKILL.md at ${skillFile}`);
    process.exit(1);
  }

  const content = readFileSync(skillFile, "utf-8");
  const result = await scanSkill(content);

  const label = GRADE_LABELS[result.riskGrade];
  const color = GRADE_COLORS[result.riskGrade];
  const badgeUrl = `https://img.shields.io/badge/clawvet-${result.riskGrade}%20${label}-${color}`;
  const linkUrl = "https://github.com/MohibShaikh/clawvet";

  if (options.markdown) {
    console.log(`[![ClawVet ${result.riskGrade}](${badgeUrl})](${linkUrl})`);
  } else {
    console.log();
    console.log(chalk.bold("  ClawVet Trust Badge"));
    console.log();
    console.log(`  Skill:  ${chalk.bold(result.skillName)}`);
    console.log(`  Grade:  ${result.riskGrade} (${label})`);
    console.log(`  Score:  ${result.riskScore}/100`);
    console.log();
    console.log(chalk.dim("  Markdown (paste in README):"));
    console.log();
    console.log(`  [![ClawVet ${result.riskGrade}](${badgeUrl})](${linkUrl})`);
    console.log();
    console.log(chalk.dim("  HTML:"));
    console.log();
    console.log(`  <a href="${linkUrl}"><img src="${badgeUrl}" alt="ClawVet ${result.riskGrade}"></a>`);
    console.log();
  }
}
