import { readFileSync, existsSync, watch } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import chalk from "chalk";
import { scanSkill } from "@clawvet/shared";
import { printScanResult } from "../output/terminal.js";

const DEFAULT_SKILL_DIRS = [
  join(homedir(), ".openclaw", "skills"),
  join(homedir(), ".openclaw", "workspace", "skills"),
];

export async function watchCommand(options: {
  threshold?: number;
  dir?: string;
}): Promise<void> {
  const threshold = options.threshold || 50;
  const SKILL_DIRS = options.dir ? [options.dir] : DEFAULT_SKILL_DIRS;
  console.log(
    chalk.bold(
      `\nClawVet Watch — monitoring skill directories (threshold: ${threshold})\n`
    )
  );

  const watchDirs: string[] = [];
  for (const dir of SKILL_DIRS) {
    if (existsSync(dir)) {
      watchDirs.push(dir);
    }
  }

  if (watchDirs.length === 0) {
    console.log(
      chalk.yellow(
        "No OpenClaw skill directories found. Watching will start when directories are created.\n"
      )
    );
    console.log(chalk.dim("Expected directories:"));
    for (const dir of SKILL_DIRS) {
      console.log(chalk.dim(`  ${dir}`));
    }
    console.log();
    process.exit(1);
  }

  console.log(chalk.dim("Watching:"));
  for (const dir of watchDirs) {
    console.log(chalk.dim(`  ${dir}`));
  }
  console.log();

  for (const dir of watchDirs) {
    const watcher = watch(dir, { recursive: true }, async (event, filename) => {
      if (!filename?.endsWith("SKILL.md")) return;

      const skillFile = join(dir, filename);
      if (!existsSync(skillFile)) return;

      console.log(chalk.dim(`\nDetected change: ${filename}`));

      try {
        const content = readFileSync(skillFile, "utf-8");
        const result = await scanSkill(content);

        if (result.cached) {
          console.log(chalk.dim("(cached)"));
        }
        printScanResult(result);

        if (result.riskScore > threshold) {
          console.log(
            chalk.bgRed.white.bold(
              ` BLOCKED — Risk score ${result.riskScore} exceeds threshold ${threshold} `
            )
          );
          console.log(
            chalk.red(
              `This skill should not be installed. Run 'clawvet scan ${skillFile}' for details.\n`
            )
          );
        }
      } catch (err) {
        console.error(chalk.red(`Error scanning ${filename}:`), err);
      }
    });

    process.on("SIGINT", () => {
      watcher.close();
      console.log(chalk.dim("\nWatch stopped."));
      process.exit(0);
    });
  }

  console.log(chalk.dim("Press Ctrl+C to stop watching.\n"));
  await new Promise(() => {});
}
