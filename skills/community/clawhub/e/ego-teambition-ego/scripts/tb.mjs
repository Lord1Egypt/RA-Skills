#!/usr/bin/env node
// CLI router. task and project stay on FUTURE_DOMAINS until a later milestone.
import path from "node:path";
import { pathToFileURL } from "node:url";
import { runTestcaseCli } from "./lib/domains/testcase.mjs";
import { FUTURE_DOMAINS, USAGE } from "./lib/pure.mjs";

export const DOMAIN_REGISTRY = {
  testcase: {
    phase: "2a",
    summary: "Read test plans and write one test case at a time through the browser session",
    run: runTestcaseCli,
  },
};

export async function dispatch(argv, deps = {}) {
  const args = argv || [];
  const registry = deps.registry || DOMAIN_REGISTRY;
  const future = deps.future || FUTURE_DOMAINS;
  const domain = args[0];
  if (!domain || domain === "--help" || domain === "-h") {
    return { exitCode: domain ? 0 : 1, stdout: USAGE, stderr: "" };
  }
  if (future.includes(domain)) {
    return {
      exitCode: 1,
      stdout: "",
      stderr: `错误: domain ${domain} 尚未实现（已实现的 domain 只有 testcase）。\n`,
    };
  }
  const entry = registry[domain];
  if (!entry || typeof entry.run !== "function") {
    const names = Object.keys(registry).join(", ") || "(none)";
    return {
      exitCode: 1,
      stdout: "",
      stderr: `错误: 未知 domain: ${domain}。可用: ${names}。\n${USAGE}`,
    };
  }
  return entry.run(args.slice(1), deps);
}

export async function main(argv, deps = {}) {
  const stdout = deps.stdout || process.stdout;
  const stderr = deps.stderr || process.stderr;
  const result = await dispatch(argv, deps);
  if (result.stdout) stdout.write(result.stdout);
  if (result.stderr) stderr.write(result.stderr);
  return result.exitCode ?? 1;
}

const entry = process.argv[1];
if (entry && import.meta.url === pathToFileURL(path.resolve(entry)).href) {
  main(process.argv.slice(2))
    .then((code) => process.exit(code))
    .catch((error) => {
      console.error(error && error.stack ? error.stack : error);
      process.exit(1);
    });
}
