import chalk from "chalk";
import type { ScanResult, Finding, Severity } from "@clawvet/shared";

const SEVERITY_COLORS: Record<Severity, (s: string) => string> = {
  critical: chalk.bgRed.white.bold,
  high: chalk.red.bold,
  medium: chalk.yellow,
  low: chalk.blue,
};

const GRADE_COLORS: Record<string, (s: string) => string> = {
  A: chalk.green.bold,
  B: chalk.greenBright,
  C: chalk.yellow.bold,
  D: chalk.redBright.bold,
  F: chalk.bgRed.white.bold,
};

export function printScanResult(result: ScanResult): void {
  console.log();
  console.log(chalk.bold("━".repeat(60)));
  console.log(chalk.bold("  ClawVet Scan Report"));
  console.log(chalk.bold("━".repeat(60)));
  console.log();

  console.log(`  Skill:   ${chalk.bold(result.skillName)}`);
  if (result.skillVersion) {
    console.log(`  Version: ${result.skillVersion}`);
  }
  console.log();

  // Risk score
  const gradeColor = GRADE_COLORS[result.riskGrade] || chalk.white;
  console.log(
    `  Risk Score: ${gradeColor(`${result.riskScore}/100`)}  Grade: ${gradeColor(result.riskGrade)}`
  );
  console.log();

  // Findings summary
  const fc = result.findingsCount;
  console.log("  Findings:");
  if (fc.critical)
    console.log(
      `    ${SEVERITY_COLORS.critical(` CRITICAL `)} ${fc.critical}`
    );
  if (fc.high)
    console.log(`    ${SEVERITY_COLORS.high("HIGH")}     ${fc.high}`);
  if (fc.medium)
    console.log(`    ${SEVERITY_COLORS.medium("MEDIUM")}   ${fc.medium}`);
  if (fc.low) console.log(`    ${SEVERITY_COLORS.low("LOW")}      ${fc.low}`);
  if (!fc.critical && !fc.high && !fc.medium && !fc.low) {
    console.log(`    ${chalk.green("No findings — skill looks clean!")}`);
  }
  console.log();

  // Detailed findings
  if (result.findings.length > 0) {
    console.log(chalk.bold("  Details:"));
    console.log();
    for (const f of result.findings) {
      const color = SEVERITY_COLORS[f.severity];
      const confStr = f.confidence != null ? ` ${Math.round(f.confidence * 100)}%` : "";
      console.log(`  ${color(`[${f.severity.toUpperCase()}${confStr}]`)} ${f.title}`);
      console.log(`    ${chalk.dim(f.description)}`);
      if (f.evidence) {
        console.log(`    Evidence: ${chalk.italic(f.evidence)}`);
      }
      if (f.lineNumber) {
        console.log(`    Line: ${f.lineNumber}`);
      }
      if (f.fix) {
        console.log(`    Fix: ${chalk.green(f.fix)}`);
      }
      console.log();
    }
  }

  // Recommendation
  const recColors: Record<string, (s: string) => string> = {
    block: chalk.bgRed.white.bold,
    warn: chalk.bgYellow.black.bold,
    approve: chalk.bgGreen.black.bold,
  };
  const rec = result.recommendation || "approve";
  console.log(
    `  Recommendation: ${(recColors[rec] || chalk.white)(` ${rec.toUpperCase()} `)}`
  );
  console.log();
  console.log(chalk.bold("━".repeat(60)));
  console.log();
}
