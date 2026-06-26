#!/usr/bin/env node
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";

function hasProjectArg(args) {
  return args.some((arg) => arg === "--project" || arg.startsWith("--project="));
}

function resolveInstalledSkillNamespace() {
  const explicit = process.env.IMAGE_SKILL_NAMESPACE?.trim();
  if (explicit) return explicit;

  const packageJsonDir = process.env.npm_package_json
    ? path.basename(path.dirname(process.env.npm_package_json))
    : "";
  if (packageJsonDir) return packageJsonDir;

  const cwdBase = path.basename(process.cwd()).trim();
  if (cwdBase) return cwdBase;

  return process.env.npm_package_name?.trim() || "";
}

const [entryArg, ...forwardedArgs] = process.argv.slice(2);
if (!entryArg) {
  console.error("Usage: node ./run-generate.mjs <entry-script> [generate args...]");
  process.exit(1);
}

const entryScript = path.resolve(process.cwd(), entryArg);
const projectRoot = (process.env.IMAGE_PROJECT_ROOT || process.env.INIT_CWD || process.cwd()).trim();
const skillNamespace = resolveInstalledSkillNamespace();
const args = hasProjectArg(forwardedArgs)
  ? forwardedArgs
  : [...forwardedArgs, "--project", projectRoot];

const npxCommand = process.platform === "win32" ? "npx.cmd" : "npx";
const result = spawnSync(npxCommand, ["-y", "bun", entryScript, ...args], {
  stdio: "inherit",
  env: {
    ...process.env,
    IMAGE_PROJECT_ROOT: projectRoot,
    IMAGE_SKILL_NAMESPACE: skillNamespace || process.env.IMAGE_SKILL_NAMESPACE,
    IMAGE_SKILL_LABEL: process.env.IMAGE_SKILL_LABEL || skillNamespace,
  },
});

process.exit(result.status ?? 1);
