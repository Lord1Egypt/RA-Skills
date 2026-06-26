import { readdirSync, existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import { scanSkill } from "@clawvet/shared";
import { printScanResult } from "../output/terminal.js";
import chalk from "chalk";

const DEFAULT_SKILL_DIRS = [
  join(homedir(), ".openclaw", "skills"),
  join(homedir(), ".openclaw", "workspace", "skills"),
];

export async function auditCommand(options: { dir?: string } = {}): Promise<void> {
  const SKILL_DIRS = options.dir ? [options.dir] : DEFAULT_SKILL_DIRS;
  console.log(chalk.bold("\nClawVet Audit — Scanning all installed skills\n"));

  let totalScanned = 0;
  let totalThreats = 0;

  for (const dir of SKILL_DIRS) {
    if (!existsSync(dir)) {
      if (options.dir) {
        console.error(chalk.yellow(`Warning: Directory not found: ${dir}\n`));
        process.exit(1);
      }
      continue;
    }

    // If the dir itself contains a SKILL.md, scan it directly
    const directSkillFile = join(dir, "SKILL.md");
    if (existsSync(directSkillFile)) {
      const content = readFileSync(directSkillFile, "utf-8");
      const result = await scanSkill(content);
      totalScanned++;
      totalThreats += result.findings.length;
      printScanResult(result);
      continue;
    }

    const entries = readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const skillFile = join(dir, entry.name, "SKILL.md");
      if (!existsSync(skillFile)) continue;

      const content = readFileSync(skillFile, "utf-8");
      const result = await scanSkill(content);
      totalScanned++;
      totalThreats += result.findings.length;

      printScanResult(result);
    }
  }

  console.log(chalk.bold(`\nAudit complete: ${totalScanned} skills scanned, ${totalThreats} findings\n`));
}
