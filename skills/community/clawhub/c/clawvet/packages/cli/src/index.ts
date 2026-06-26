import { Command } from "commander";
import { scanCommand } from "./commands/scan.js";
import { auditCommand } from "./commands/audit.js";
import { watchCommand } from "./commands/watch.js";
import { badgeCommand } from "./commands/badge.js";

const program = new Command();

program
  .name("clawvet")
  .description("Skill vetting & supply chain security for OpenClaw")
  .version("0.6.0");

program
  .command("scan")
  .description("Scan a skill for security threats")
  .argument("<target>", "Path to skill folder or SKILL.md file")
  .option("--format <format>", "Output format: terminal, json, or sarif", "terminal")
  .option("--fail-on <severity>", "Exit 1 if findings at this severity or above")
  .option("--semantic", "Enable AI semantic analysis (requires ANTHROPIC_API_KEY)")
  .option("--remote", "Fetch skill from ClawHub by name instead of local path")
  .option("-q, --quiet", "Suppress all output, exit code only (0=pass, 1=fail)")
  .option("--subscribe", "Open the ClawVet feedback & alerts form")
  .action(async (target, opts) => {
    if (opts.subscribe) {
      const url = "https://tally.so/r/jaMdaa";
      console.log(`Opening ${url} ...`);
      const { exec } = await import("node:child_process");
      const cmd = process.platform === "win32" ? `start ${url}` : process.platform === "darwin" ? `open ${url}` : `xdg-open ${url}`;
      exec(cmd);
    }
    await scanCommand(target, {
      format: opts.format,
      failOn: opts.failOn,
      semantic: opts.semantic,
      remote: opts.remote,
      quiet: opts.quiet,
    });
  });

program
  .command("audit")
  .description("Scan all installed OpenClaw skills")
  .option("--dir <path>", "Custom skills directory to scan")
  .action(async (opts) => {
    await auditCommand({ dir: opts.dir });
  });

program
  .command("watch")
  .description("Pre-install hook — blocks risky skill installs")
  .option("--threshold <score>", "Risk score threshold (default 50)", "50")
  .option("--dir <path>", "Custom skills directory to watch")
  .action(async (opts) => {
    await watchCommand({ threshold: parseInt(opts.threshold), dir: opts.dir });
  });

program
  .command("badge")
  .description("Generate a trust badge for a skill's README")
  .argument("<target>", "Path to skill folder or SKILL.md file")
  .option("--md", "Output only the markdown snippet")
  .action(async (target, opts) => {
    await badgeCommand(target, { markdown: opts.md });
  });

program
  .command("feedback")
  .description("Open the ClawVet feedback & threat alerts form")
  .action(async () => {
    const url = "https://tally.so/r/jaMdaa";
    console.log(`Opening ${url} ...`);
    const { exec } = await import("node:child_process");
    const cmd = process.platform === "win32" ? `start ${url}` : process.platform === "darwin" ? `open ${url}` : `xdg-open ${url}`;
    exec(cmd);
  });

program.parse();
