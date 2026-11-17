import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawn, spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { USAGE, egoMissingSummary, parseCheckArgs, resolveProcessExit } from "./pure.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

export function whichEgo(spawnSyncImpl = spawnSync) {
  const probe = spawnSyncImpl("ego-browser", ["--help"], { encoding: "utf8" });
  return probe && probe.error ? null : "ego-browser";
}

export function renderEntry({ config, runHref, depsHref }) {
  return [
    `import { executeCheck } from ${JSON.stringify(runHref)};`,
    `import { createEgoBrowser } from ${JSON.stringify(depsHref)};`,
    `const config = ${JSON.stringify(config)};`,
    `const summary = await executeCheck(config, { browser: createEgoBrowser() });`,
    `console.log(JSON.stringify(summary));`,
    `if (summary.exitCode) process.exitCode = summary.exitCode;`,
    "",
  ].join("\n");
}

export async function runCheckCli(argv, deps = {}) {
  const io = {
    fs: deps.fs || fs,
    spawn: deps.spawn || spawn,
    spawnSync: deps.spawnSync || spawnSync,
    stdout: deps.stdout || process.stdout,
    stderr: deps.stderr || process.stderr,
    whichEgo: deps.whichEgo || ((impl) => whichEgo(impl)),
    mkdtemp: deps.mkdtemp || ((prefix) => fs.mkdtemp(prefix)),
    tmp: deps.tmp || os.tmpdir(),
    runModule: deps.runModule || path.join(here, "run-check.mjs"),
    egoModule: deps.egoModule || path.join(here, "ego-deps.mjs"),
  };

  let args;
  try {
    args = parseCheckArgs(argv);
  } catch (error) {
    io.stderr.write(`${error.message}\n${USAGE}`);
    return 2;
  }
  if (args.help) {
    io.stdout.write(USAGE);
    return 0;
  }

  if (!io.whichEgo(io.spawnSync)) {
    const summary = egoMissingSummary();
    io.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
    return 2;
  }

  const dir = await io.mkdtemp(path.join(io.tmp, "ego-teambition-"));
  const entry = path.join(dir, "entry.mjs");
  await io.fs.writeFile(
    entry,
    renderEntry({
      config: { keep: args.keep, taskName: args.taskName },
      runHref: pathToFileURL(io.runModule).href,
      depsHref: pathToFileURL(io.egoModule).href,
    }),
  );

  let stdoutBuf = "";
  let stderrBuf = "";
  let code = 1;
  try {
    const href = pathToFileURL(entry).href;
    const child = io.spawn("ego-browser", ["nodejs", "-e", `await import(${JSON.stringify(href)})`], {
      stdio: ["ignore", "pipe", "pipe"],
    });
    child.stdout.on("data", (chunk) => {
      stdoutBuf += chunk;
    });
    child.stderr.on("data", (chunk) => {
      stderrBuf += chunk;
    });
    code = await new Promise((resolve) => {
      child.on("error", (error) => {
        stderrBuf += String(error.message || error);
        resolve(1);
      });
      child.on("close", (status) => resolve(status ?? 1));
    });
  } finally {
    await io.fs.rm(dir, { recursive: true, force: true }).catch(() => {});
  }

  const combined = `${stdoutBuf}\n${stderrBuf}`;
  let summary = null;
  const lines = combined.split(/\n/).map((line) => line.trim()).filter(Boolean).reverse();
  for (const line of lines) {
    if (!line.startsWith("{") || !line.includes("login_required")) continue;
    try {
      summary = JSON.parse(line);
      break;
    } catch {
      // keep scanning
    }
  }
  if (summary) io.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
  else if (stdoutBuf) io.stdout.write(stdoutBuf);
  const noise = stderrBuf
    .split(/\n/)
    .filter((line) => line && !line.trim().startsWith("{") && !line.includes('"login_required"'))
    .join("\n");
  if (noise) io.stderr.write(noise.endsWith("\n") ? noise : `${noise}\n`);

  if (summary && typeof summary.exitCode === "number") return summary.exitCode;
  return resolveProcessExit(combined, code);
}
