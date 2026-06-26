import { resolve } from "node:path";
import { existsSync } from "node:fs";

const USAGE = `Usage: skill-review [options] <skill-dir>

Perform a 7-layer security analysis on a Claude Code Skill package.

Arguments:
  skill-dir              Path to the skill directory to analyze

Options:
  --config <path>        Path to a JSON config file
  --pre                  Only run prescan (skip LLM analysis)
  --lang <lang>          Output language for human-readable text (default: English)
  --json                 Output raw JSON instead of a text report
  -o, --output <file>    Write final report to a file (default: stdout)
  -v, --verbose          Show detailed logs (tool calls, model output) to stderr
  --log <file>           Save detailed logs to a file (implies verbose, independent of -v)
  -h, --help             Show this help message

Output routing:
  Final report  → stdout (default) or -o <file>
  Status        → stderr (always: scanning progress, phase headers, errors)
  Detailed logs → stderr (-v) and/or file (--log), can be combined

Examples:
  skill-review ./my-skill
  skill-review --lang zh ./my-skill
  skill-review --json -o report.json ./my-skill
  skill-review -v ./my-skill                        # stream logs to terminal
  skill-review --log scan.log ./my-skill             # save logs to file
  skill-review -v --log scan.log -o report.json ./my-skill  # all outputs separated`;

export function parseArgs(argv = process.argv.slice(2)) {
  let configFile = null;
  let pre = false;
  let lang = "English";
  let jsonOutput = false;
  let outputFile = null;
  let logFile = null;
  let verbose = false;
  let skillDir = null;

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "-h" || arg === "--help") {
      console.log(USAGE);
      process.exit(0);
    } else if (arg === "--config") {
      configFile = argv[++i];
      if (!configFile) {
        console.error("Error: --config requires a file path");
        process.exit(1);
      }
    } else if (arg === "--pre") {
      pre = true;
    } else if (arg === "--json") {
      jsonOutput = true;
    } else if (arg === "-o" || arg === "--output") {
      outputFile = argv[++i];
      if (!outputFile) {
        console.error("Error: -o/--output requires a file path");
        process.exit(1);
      }
    } else if (arg === "--log") {
      logFile = argv[++i];
      if (!logFile) {
        console.error("Error: --log requires a file path");
        process.exit(1);
      }
    } else if (arg === "-v" || arg === "--verbose") {
      verbose = true;
    } else if (arg === "--lang") {
      lang = argv[++i];
      if (!lang) {
        console.error("Error: --lang requires a value (e.g. --lang zh)");
        process.exit(1);
      }
    } else if (arg.startsWith("-")) {
      console.error(`Unknown option: ${arg}\n`);
      console.error(USAGE);
      process.exit(1);
    } else {
      skillDir = arg;
    }
  }

  if (!skillDir) {
    console.error(USAGE);
    process.exit(1);
  }

  skillDir = resolve(skillDir);

  if (!existsSync(skillDir)) {
    console.error(`Error: directory not found: ${skillDir}`);
    process.exit(1);
  }

  return { configFile, pre, lang, jsonOutput, outputFile, logFile, verbose, skillDir };
}
