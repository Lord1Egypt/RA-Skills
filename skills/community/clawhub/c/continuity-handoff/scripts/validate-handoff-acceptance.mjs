#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

function fail(code, detail) {
  throw new Error(`${code}: ${detail}`);
}

function parseArgs(argv) {
  const allowed = new Set([
    "sourceThreadId", "targetThreadId", "ackFile", "projectBindingFile",
    "codexHome", "rolloutPath", "query",
  ]);
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const option = argv[index];
    if (!option.startsWith("--")) fail("invalid_argument", `Unexpected argument: ${option}`);
    const key = option.slice(2).replace(/-([a-z])/g, (_, char) => char.toUpperCase());
    if (!allowed.has(key)) fail("invalid_argument", `Unknown option: ${option}`);
    const value = argv[++index];
    if (!value || value.startsWith("--")) fail("invalid_argument", `${option} requires a value`);
    args[key] = value;
  }
  for (const key of allowed) {
    if (!args[key]) fail("acceptance_evidence_missing", `--${key.replace(/[A-Z]/g, (char) => `-${char.toLowerCase()}`)} is required`);
  }
  return args;
}

function runRecall(args) {
  const script = fileURLToPath(new URL("./recall-codex-history.mjs", import.meta.url));
  try {
    const output = execFileSync(process.execPath, [
      script,
      "--codex-home", args.codexHome,
      "--thread-id", args.sourceThreadId,
      "--rollout-path", args.rolloutPath,
      "--query", args.query,
    ], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
    return JSON.parse(output);
  } catch (error) {
    const detail = String(error?.stderr || error?.message || "recall failed").trim();
    fail("acceptance_recall_failed", detail);
  }
}

function readEvidence(filePath, label) {
  const resolved = path.resolve(filePath);
  let value;
  try {
    value = JSON.parse(fs.readFileSync(resolved, "utf8"));
  } catch {
    fail("acceptance_evidence_invalid", `${label} is not readable JSON: ${resolved}`);
  }
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    fail("acceptance_evidence_invalid", `${label} must contain a JSON object`);
  }
  return { path: resolved, value };
}

function nonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function directoryExists(directory) {
  try {
    return fs.statSync(directory).isDirectory();
  } catch {
    return false;
  }
}

function isWithin(parent, candidate) {
  const relative = path.relative(parent, candidate);
  return relative === "" || (relative !== ".." && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative));
}

function samePath(left, right) {
  const resolvedLeft = path.resolve(left);
  const resolvedRight = path.resolve(right);
  return process.platform === "win32"
    ? resolvedLeft.toLowerCase() === resolvedRight.toLowerCase()
    : resolvedLeft === resolvedRight;
}

function validateProjectBinding(value, targetThreadId) {
  if (value.valid !== true || value.target_thread_id !== targetThreadId) return false;
  if (!nonEmptyString(value.project_binding)) return false;
  if (!["single-root", "project-root-with-nested-repo"].includes(value.binding_model)) return false;
  if (![value.codex_project_root, value.canonical_repo_root, value.operational_cwd].every(nonEmptyString)) return false;

  const projectRoot = path.resolve(value.codex_project_root);
  const repoRoot = path.resolve(value.canonical_repo_root);
  const operationalCwd = path.resolve(value.operational_cwd);
  if (![projectRoot, repoRoot, operationalCwd].every(directoryExists)) return false;
  if (!fs.existsSync(path.join(repoRoot, ".git"))) return false;
  if (!isWithin(projectRoot, repoRoot) || !isWithin(repoRoot, operationalCwd)) return false;
  if (value.binding_model === "single-root" && !samePath(projectRoot, repoRoot)) return false;
  if (value.binding_model === "project-root-with-nested-repo" && samePath(projectRoot, repoRoot)) return false;
  return true;
}

export function run(argv) {
  const args = parseArgs(argv);
  if (args.sourceThreadId === args.targetThreadId) {
    fail("target_thread_not_fresh", "Target Thread ID must differ from Source Thread ID");
  }
  const acknowledgement = readEvidence(args.ackFile, "acknowledgement evidence");
  const projectBinding = readEvidence(args.projectBindingFile, "project binding evidence");
  const recall = runRecall(args);
  const gates = {
    acknowledged: acknowledgement.value.acknowledged === true
      && acknowledgement.value.target_thread_id === args.targetThreadId,
    recall_completed: recall.mode === "bounded_read_only_recall"
      && recall.identity?.thread_id === args.sourceThreadId
      && Number(recall.scope?.matched_windows) > 0,
    project_binding_valid: validateProjectBinding(projectBinding.value, args.targetThreadId),
    source_unchanged: recall.source_proof?.unchanged === true,
  };
  const failed = Object.entries(gates).filter(([, passed]) => !passed).map(([name]) => name);
  if (failed.length > 0) fail("handoff_not_accepted", `Failed gates: ${failed.join(", ")}`);

  process.stdout.write(`${JSON.stringify({
    status: "handoff_accepted",
    source_thread_id: args.sourceThreadId,
    target_thread_id: args.targetThreadId,
    target_identity_is_fresh: true,
    gates,
    evidence_files: {
      acknowledgement: acknowledgement.path,
      project_binding: projectBinding.path,
    },
    project_binding: {
      binding_model: projectBinding.value.binding_model,
      codex_project_root: projectBinding.value.codex_project_root,
      canonical_repo_root: projectBinding.value.canonical_repo_root,
      operational_cwd: projectBinding.value.operational_cwd,
    },
    recall_proof: recall.source_proof,
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
