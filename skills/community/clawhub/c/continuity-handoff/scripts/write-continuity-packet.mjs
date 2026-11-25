#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const SECRET_PATTERNS = [
  ["private_key", /-----BEGIN (?:OPENSSH|RSA|EC|DSA|PGP) PRIVATE KEY-----/],
  ["github_token", /\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b/],
  ["openai_key", /\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b/],
  ["aws_access_key", /\b(?:AKIA|ASIA)[A-Z0-9]{16}\b/],
  ["npm_token", /\bnpm_[A-Za-z0-9]{30,}\b/],
  ["slack_token", /\bxox[baprs]-[A-Za-z0-9-]{20,}\b/],
  ["bearer_token", /\bAuthorization\s*:\s*Bearer\s+[A-Za-z0-9._~+\/-]{20,}\b/i],
  ["named_secret", /\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*["']?[A-Za-z0-9+/_=-]{20,}/i],
];

function fail(code, detail) {
  const error = new Error(`${code}: ${detail}`);
  error.code = code;
  throw error;
}

function parseArgs(argv) {
  const args = { projectRoot: process.cwd() };
  const allowed = new Set(["packetFile", "projectRoot", "workSlug", "output"]);
  for (let index = 0; index < argv.length; index += 1) {
    const option = argv[index];
    if (!option.startsWith("--")) fail("invalid_argument", `Unexpected argument: ${option}`);
    const key = option.slice(2).replace(/-([a-z])/g, (_, char) => char.toUpperCase());
    if (!allowed.has(key)) fail("invalid_argument", `Unknown option: ${option}`);
    const value = argv[++index];
    if (!value || value.startsWith("--")) fail("invalid_argument", `${option} requires a value`);
    args[key] = value;
  }
  if (!args.packetFile) fail("invalid_argument", "--packet-file is required");
  if (!args.workSlug && !args.output) fail("invalid_argument", "--work-slug is required without --output");
  if (args.workSlug && !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(args.workSlug)) {
    fail("invalid_work_slug", "Use lowercase letters, numbers, and single hyphens");
  }
  return args;
}

function git(projectRoot, args, options = {}) {
  return execFileSync("git", ["-C", projectRoot, ...args], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", options.allowFailure ? "pipe" : "inherit"],
  }).trim();
}

function gitRoot(projectRoot) {
  try {
    return git(projectRoot, ["rev-parse", "--show-toplevel"]);
  } catch {
    fail("git_project_required", `${projectRoot} is not inside a Git worktree; pass --output for an explicit durable path`);
  }
}

function detectSecrets(contents) {
  return SECRET_PATTERNS
    .filter(([, pattern]) => pattern.test(contents))
    .map(([kind]) => kind);
}

function ensureVersionable(root, outputPath) {
  const relative = path.relative(root, outputPath);
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    fail("packet_outside_project", `Default packet path escaped Git root: ${outputPath}`);
  }
  try {
    execFileSync("git", ["-C", root, "check-ignore", "--no-index", "--quiet", "--", relative]);
    fail("packet_path_ignored", `${relative} is ignored; do not write or change .gitignore automatically`);
  } catch (error) {
    if (error?.code === "packet_path_ignored") throw error;
    if (error?.status !== 1) throw error;
  }
  return relative;
}

function rejectSymlinkBoundary(root, outputPath) {
  const relative = path.relative(root, outputPath);
  let current = root;
  for (const part of relative.split(path.sep).slice(0, -1)) {
    current = path.join(current, part);
    if (!fs.existsSync(current)) break;
    if (fs.lstatSync(current).isSymbolicLink()) {
      fail("packet_symlink_boundary", `${current} is a symlink; refusing a redirected continuity destination`);
    }
  }
  if (fs.existsSync(outputPath) && fs.lstatSync(outputPath).isSymbolicLink()) {
    fail("packet_symlink_boundary", `${outputPath} is a symlink; refusing a redirected continuity destination`);
  }
}

function atomicWrite(outputPath, contents) {
  const outputDirectory = path.dirname(outputPath);
  fs.mkdirSync(outputDirectory, { recursive: true });
  const temporaryDirectory = fs.mkdtempSync(path.join(outputDirectory, `.${path.basename(outputPath)}.`));
  const temporaryPath = path.join(temporaryDirectory, "packet.tmp");
  try {
    fs.writeFileSync(temporaryPath, contents, { encoding: "utf8", mode: 0o600, flag: "wx" });
    fs.renameSync(temporaryPath, outputPath);
  } finally {
    if (fs.existsSync(temporaryPath)) fs.unlinkSync(temporaryPath);
    fs.rmdirSync(temporaryDirectory);
  }
}

export function run(argv) {
  const args = parseArgs(argv);
  const packetFile = path.resolve(args.packetFile);
  if (!fs.existsSync(packetFile)) fail("packet_source_unavailable", packetFile);
  const contents = fs.readFileSync(packetFile, "utf8");
  const secretTypes = detectSecrets(contents);
  if (secretTypes.length > 0) {
    fail("packet_secret_detected", `Refusing to write; detected ${secretTypes.join(", ")}. Ask the operator whether to remove the secret or choose another packet.`);
  }

  const projectRoot = path.resolve(args.projectRoot);
  const root = args.output ? null : gitRoot(projectRoot);
  const outputPath = args.output
    ? path.resolve(args.output)
    : path.join(root, ".traverse", "continuity", `${args.workSlug}.md`);
  if (args.output && (outputPath === "/private/tmp" || outputPath.startsWith("/private/tmp/"))) {
    fail("temporary_final_path", "A final continuity packet cannot live under /private/tmp");
  }
  if (root) rejectSymlinkBoundary(root, outputPath);
  const relative = root ? ensureVersionable(root, outputPath) : null;

  atomicWrite(outputPath, contents);

  let gitState = "explicit_output_not_checked";
  if (root) {
    const status = git(root, ["status", "--porcelain=v1", "--untracked-files=all", "--", relative]);
    if (status) {
      gitState = "visible_in_git_status";
    } else {
      try {
        git(root, ["ls-files", "--error-unmatch", "--", relative]);
        gitState = "tracked_unchanged";
      } catch {
        fs.unlinkSync(outputPath);
        fail("packet_not_versionable", `${relative} is neither visible in git status nor tracked`);
      }
    }
  }

  process.stdout.write(`${JSON.stringify({
    status: "packet_written",
    path: outputPath,
    git_state: gitState,
    auto_committed: false,
    source_thread_mutated: false,
  }, null, 2)}\n`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    run(process.argv.slice(2));
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}
