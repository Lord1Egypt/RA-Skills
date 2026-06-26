import { readFileSync, existsSync, statSync } from "node:fs";
import { resolve, join } from "node:path";
import chalk from "chalk";
import { scanSkill } from "@clawvet/shared";
import { printScanResult } from "../output/terminal.js";
import { printJsonResult } from "../output/json.js";
import { printSarifResult } from "../output/sarif.js";
import { sendTelemetry, hasBeenAsked, setTelemetry, isTelemetryEnabled, getScanCount } from "../telemetry.js";

export interface ScanOptions {
  format?: "terminal" | "json" | "sarif";
  failOn?: "critical" | "high" | "medium" | "low";
  semantic?: boolean;
  remote?: boolean;
  quiet?: boolean;
}

async function fetchRemoteSkill(slug: string): Promise<string> {
  const urls = [
    `https://raw.githubusercontent.com/openclaw/skills/main/${slug}/SKILL.md`,
    `https://clawhub.ai/api/v1/skills/${slug}/raw`,
  ];

  for (const url of urls) {
    try {
      const res = await fetch(url, { signal: AbortSignal.timeout(10000) });
      if (res.ok) {
        return await res.text();
      }
    } catch {
      // try next
    }
  }

  throw new Error(
    `Could not fetch skill "${slug}" from ClawHub. Check the skill name and try again.`
  );
}

export async function scanCommand(
  target: string,
  options: ScanOptions
): Promise<void> {
  let content: string;

  if (options.remote) {
    try {
      process.stderr.write(`Fetching "${target}" from ClawHub...\n`);
      content = await fetchRemoteSkill(target);
    } catch (err) {
      console.error(
        err instanceof Error ? err.message : "Failed to fetch remote skill"
      );
      process.exit(1);
    }
  } else {
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
      console.error(`Hint: If this is a directory of skills, use 'clawvet audit --dir ${target}' instead.`);
      process.exit(1);
    }

    content = readFileSync(skillFile, "utf-8");
  }

  // Load .clawvetban — block skills by name, author, or slug
  const banFile = join(process.cwd(), ".clawvetban");
  if (existsSync(banFile)) {
    const banEntries = readFileSync(banFile, "utf-8")
      .split("\n")
      .map((l) => l.trim().toLowerCase())
      .filter((l) => l && !l.startsWith("#"));

    // Quick parse frontmatter to check name/author before full scan
    const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (fmMatch) {
      const fmText = fmMatch[1].toLowerCase();
      for (const ban of banEntries) {
        const targetLower = target.toLowerCase();
        if (
          targetLower.includes(ban) ||
          fmText.includes(`name: ${ban}`) ||
          fmText.includes(`author: ${ban}`) ||
          fmText.includes(`slug: ${ban}`)
        ) {
          console.error(
            chalk.bgRed.white.bold(` BANNED `) +
            chalk.red(` Skill matches ban list entry: ${ban}`)
          );
          console.error(chalk.dim(`  Source: ${banFile}`));
          process.exit(1);
        }
      }
    }
  }

  // Load .clawvetignore
  const ignoreFile = join(process.cwd(), ".clawvetignore");
  const ignorePatterns: string[] = [];
  if (existsSync(ignoreFile)) {
    const lines = readFileSync(ignoreFile, "utf-8").split("\n");
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith("#")) {
        ignorePatterns.push(trimmed);
      }
    }
  }

  const result = await scanSkill(content, {
    semantic: options.semantic ?? false,
    ignorePatterns: ignorePatterns.length ? ignorePatterns : undefined,
  });

  if (!options.quiet) {
    if (options.format === "sarif") {
      printSarifResult(result);
    } else if (options.format === "json") {
      printJsonResult(result);
    } else {
      printScanResult(result);
    }
  }

  // Telemetry: first-run opt-in prompt (only in interactive TTY)
  const isInteractive = !options.quiet && options.format !== "json" && options.format !== "sarif";
  if (isInteractive) {
    if (!hasBeenAsked() && !isTelemetryEnabled() && process.stdin.isTTY) {
      const readline = await import("node:readline");
      const rl = readline.createInterface({ input: process.stdin, output: process.stderr });
      const answer = await new Promise<string>((resolve) => {
        rl.question(
          chalk.dim("Help improve ClawVet — send anonymous usage stats? (y/n) "),
          (a) => { rl.close(); resolve(a.trim().toLowerCase()); }
        );
      });
      setTelemetry(answer === "y" || answer === "yes");
    }

  }

  // Await telemetry so it completes before any process.exit()
  await sendTelemetry(result);

  // Show Tally CTA every 5th scan (after increment)
  if (isInteractive && getScanCount() % 5 === 0) {
    console.log(
      chalk.dim("  ") +
      chalk.cyan("Got feedback? Want threat alerts? → ") +
      chalk.underline.cyan("https://tally.so/r/jaMdaa")
    );
    console.log();
  }

  const failOn = options.failOn || (options.quiet ? "high" : undefined);
  if (failOn) {
    const severityOrder = ["low", "medium", "high", "critical"];
    const threshold = severityOrder.indexOf(failOn);
    const hasFailure = result.findings.some(
      (f) => severityOrder.indexOf(f.severity) >= threshold
    );
    if (hasFailure) {
      process.exit(1);
    }
  }
}
