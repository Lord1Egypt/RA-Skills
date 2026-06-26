#!/usr/bin/env node
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";

function hasProjectArg(args) {
  return args.some((arg) => arg === "--project" || arg.startsWith("--project="));
}

const [entryArg, ...forwardedArgs] = process.argv.slice(2);
if (!entryArg) {
  console.error("Usage: node ./run-generate.mjs <entry-script> [generate args...]");
  process.exit(1);
}

const entryScript = path.resolve(process.cwd(), entryArg);
const projectRoot = (process.env.IMAGE_PROJECT_ROOT || process.env.INIT_CWD || process.cwd()).trim();
const args = hasProjectArg(forwardedArgs)
  ? forwardedArgs
  : [...forwardedArgs, "--project", projectRoot];

const npxCommand = process.platform === "win32" ? "npx.cmd" : "npx";
const result = spawnSync(npxCommand, ["-y", "bun", entryScript, ...args], {
  stdio: "inherit",
  env: {
    ...process.env,
    IMAGE_PROJECT_ROOT: projectRoot,
  },
});

process.exit(result.status ?? 1);
