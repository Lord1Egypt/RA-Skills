import process from "node:process";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const npmCmd = process.platform === "win32" ? "npm.cmd" : "npm";
const npxCmd = process.platform === "win32" ? "npx.cmd" : "npx";

function printHelp() {
  console.log(`Usage:
  node scripts/doctor.mjs [options]

Options:
  --project <path>   Optional project directory for context only
  --json             Print JSON output
  -h, --help         Show help`);
}

function parseArgs(argv) {
  const args = { project: process.cwd(), json: false };
  for (let i = 0; i < argv.length; i++) {
    const current = argv[i];
    if (current === "--project") args.project = argv[++i] ?? args.project;
    else if (current === "--json") args.json = true;
    else if (current === "--help" || current === "-h") {
      printHelp();
      process.exit(0);
    }
  }
  return args;
}

function checkCommand(command, args) {
  const result = spawnSync(command, args, { encoding: "utf8" });
  return {
    available: result.status === 0,
    version: result.status === 0 ? (result.stdout || result.stderr).trim().split("\n")[0] : null,
  };
}

function inspectToolchain() {
  const nodeStatus = checkCommand(process.execPath, ["--version"]);
  const npmStatus = checkCommand(npmCmd, ["--version"]);
  const bunStatus = checkCommand("bun", ["--version"]);
  const npxStatus = checkCommand(npxCmd, ["--version"]);
  const sipsStatus = checkCommand("sips", ["--help"]);
  const cwebpStatus = checkCommand("cwebp", ["-version"]);
  const magickStatus = checkCommand("magick", ["-version"]);
  const convertStatus = checkCommand("convert", ["-version"]);
  return [
    { id: "node", label: "Node.js", required: true, ...nodeStatus },
    { id: "npm", label: "npm", required: true, ...npmStatus },
    { id: "bun", label: "Bun", required: false, ...bunStatus },
    { id: "npx", label: "npx", required: false, ...npxStatus },
    { id: "sips", label: "sips", required: false, ...sipsStatus },
    { id: "cwebp", label: "cwebp", required: false, ...cwebpStatus },
    { id: "magick", label: "ImageMagick", required: false, ...magickStatus },
    { id: "convert", label: "convert", required: false, ...convertStatus },
  ];
}

function toolAvailable(tools, id) {
  return Boolean(tools.find((tool) => tool.id === id)?.available);
}

export function doctorSkill({ projectDir = process.cwd() } = {}) {
  const tools = inspectToolchain();
  const errors = [];
  const warnings = [];
  const suggestions = [];

  const hasNode = toolAvailable(tools, "node");
  const hasNpm = toolAvailable(tools, "npm");
  const hasBun = toolAvailable(tools, "bun");
  const hasNpx = toolAvailable(tools, "npx");
  const hasCompressor =
    toolAvailable(tools, "sips") ||
    toolAvailable(tools, "cwebp") ||
    toolAvailable(tools, "magick") ||
    toolAvailable(tools, "convert");

  if (!hasNode) errors.push("Node.js is required but was not detected");
  if (!hasNpm) errors.push("npm is required but was not detected");
  if (!hasBun && !hasNpx) errors.push("Need Bun or npx so the compression CLI can run");
  if (!hasCompressor) {
    warnings.push("No supported local compression tool was detected");
    suggestions.push("Install at least one of sips, cwebp, or ImageMagick before compressing images");
  }

  return {
    ok: errors.length === 0 && hasCompressor,
    skillDir: path.resolve(path.dirname(fileURLToPath(import.meta.url)), ".."),
    projectDir: path.resolve(projectDir),
    behavior: {
      readOnly: true,
      writesFiles: false,
    },
    tools,
    errors,
    warnings,
    suggestions,
  };
}

function formatText(summary) {
  const lines = [];
  lines.push(`Skill dir: ${summary.skillDir}`);
  lines.push(`Project dir: ${summary.projectDir}`);
  lines.push(`Ready: ${summary.ok ? "yes" : "no"}`);
  if (summary.errors.length) {
    lines.push("Errors:");
    for (const error of summary.errors) lines.push(`- ${error}`);
  }
  if (summary.warnings.length) {
    lines.push("Warnings:");
    for (const warning of summary.warnings) lines.push(`- ${warning}`);
  }
  if (summary.suggestions.length) {
    lines.push("Suggestions:");
    for (const suggestion of summary.suggestions) lines.push(`- ${suggestion}`);
  }
  return lines.join("\n");
}

const isDirectRun =
  process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url));

if (isDirectRun) {
  try {
    const args = parseArgs(process.argv.slice(2));
    const summary = doctorSkill({ projectDir: args.project });
    if (args.json) console.log(JSON.stringify(summary, null, 2));
    else console.log(formatText(summary));
    if (!summary.ok) process.exitCode = 1;
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}
