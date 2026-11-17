import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawn, spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { describeImages } from "./media.mjs";
import {
  RESULT_TAG,
  USAGE,
  confirmationSummary,
  draftOf,
  egoMissingSummary,
  extractTaggedJson,
  formatResult,
  parseCheckArgs,
  parseCleanupArgs,
  parsePostArgs,
  resolveProcessExit,
} from "./pure.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

const RUNNERS = {
  check: { exportName: "executeCheck", runModule: "run-check.mjs" },
  post: { exportName: "executePost", runModule: "post-flow.mjs" },
  cleanup: { exportName: "executeCleanup", runModule: "post-flow.mjs" },
};

export function whichEgo(spawnSyncImpl = spawnSync) {
  const probe = spawnSyncImpl("ego-browser", ["--help"], { encoding: "utf8" });
  return probe && probe.error ? null : "ego-browser";
}

export function renderEntry({ config, runHref, depsHref, exportName }) {
  return [
    `import { ${exportName} } from ${JSON.stringify(runHref)};`,
    `import { createEgoBrowser } from ${JSON.stringify(depsHref)};`,
    `const config = ${JSON.stringify(config)};`,
    `const summary = await ${exportName}(config, { browser: createEgoBrowser() });`,
    `console.log(${JSON.stringify(RESULT_TAG)} + JSON.stringify(summary));`,
    `if (summary.exitCode) process.exitCode = summary.exitCode;`,
    "",
  ].join("\n");
}

function parseKind(kind, argv) {
  if (kind === "check") return { args: parseCheckArgs(argv), command: "check-login" };
  if (kind === "cleanup") return { args: parseCleanupArgs(argv), command: "cleanup" };
  return { args: parsePostArgs(argv), command: "post" };
}

export async function runCli(kind, argv, deps = {}) {
  const runner = RUNNERS[kind];
  const io = {
    fs: deps.fs || fs,
    spawn: deps.spawn || spawn,
    spawnSync: deps.spawnSync || spawnSync,
    stdout: deps.stdout || process.stdout,
    stderr: deps.stderr || process.stderr,
    whichEgo: deps.whichEgo || ((impl) => whichEgo(impl)),
    mkdtemp: deps.mkdtemp || ((prefix) => fs.mkdtemp(prefix)),
    tmp: deps.tmp || os.tmpdir(),
    runModule: deps.runModule || (runner ? path.join(here, runner.runModule) : ""),
    egoModule: deps.egoModule || path.join(here, "ego-deps.mjs"),
  };
  if (!runner) {
    io.stderr.write(`Unknown command: ${kind}\n${USAGE}`);
    return 1;
  }

  let parsed;
  try {
    parsed = parseKind(kind, argv);
  } catch (error) {
    io.stderr.write(`${error.message}\n${USAGE}`);
    return 1;
  }
  const args = parsed.args;
  if (args.help) {
    io.stdout.write(USAGE);
    return 0;
  }

  let described = [];
  if (parsed.command === "post" && args.images && args.images.length) {
    try {
      described = await describeImages(args.images);
    } catch (error) {
      io.stderr.write(`${error.message}\n${USAGE}`);
      return 1;
    }
  }
  const draftInput = {
    ...args,
    images: described.map((image) => ({ path: image.path, bytes: image.bytes, md5: image.md5 })),
  };

  if (!io.whichEgo(io.spawnSync)) {
    const summary = egoMissingSummary(parsed.command);
    if (parsed.command === "post" && args.text) summary.draft = draftOf(draftInput);
    io.stdout.write(formatResult(summary, { asJson: true }));
    return 2;
  }
  if (parsed.command === "post" && !args.yes) {
    io.stdout.write(formatResult(confirmationSummary(draftInput), { asJson: Boolean(args.json) }));
    return 3;
  }

  const config = {
    command: parsed.command,
    keep: Boolean(args.keep),
    taskName: args.taskName,
    text: args.text,
    replyTo: args.replyTo,
    yes: Boolean(args.yes),
    long: Boolean(args.long),
    queryId: args.queryId,
    transactionId: args.transactionId,
    images: described.map((image) => image.path),
  };
  const dir = await io.mkdtemp(path.join(io.tmp, "ego-x-post-"));
  const entry = path.join(dir, "entry.mjs");
  let stdoutBuf = "";
  let stderrBuf = "";
  let code = 1;
  try {
    await io.fs.writeFile(entry, renderEntry({
      config,
      runHref: pathToFileURL(io.runModule).href,
      depsHref: pathToFileURL(io.egoModule).href,
      exportName: runner.exportName,
    }));
    const href = pathToFileURL(entry).href;
    const child = io.spawn("ego-browser", ["nodejs", "-e", `await import(${JSON.stringify(href)})`], {
      stdio: ["ignore", "pipe", "pipe"],
    });
    child.stdout.on("data", (chunk) => { stdoutBuf += chunk; });
    child.stderr.on("data", (chunk) => { stderrBuf += chunk; });
    code = await new Promise((resolve) => {
      child.on("error", (error) => {
        stderrBuf += String(error.message || error);
        resolve(1);
      });
      child.on("close", (status) => resolve(status ?? 1));
    });
  } catch (error) {
    stderrBuf += String(error && error.message ? error.message : error);
    code = 1;
  } finally {
    if (io.fs.rm) await io.fs.rm(dir, { recursive: true, force: true }).catch(() => {});
  }

  const combined = `${stdoutBuf}\n${stderrBuf}`;
  const summary = extractTaggedJson(combined);
  if (summary && typeof summary === "object") {
    io.stdout.write(formatResult(summary, { asJson: Boolean(args.json) }));
  } else if (stdoutBuf) {
    io.stdout.write(stdoutBuf.endsWith("\n") ? stdoutBuf : `${stdoutBuf}\n`);
  }
  const noise = stderrBuf
    .split(/\n/)
    .filter((line) => line && !line.includes(RESULT_TAG))
    .join("\n");
  if (noise) io.stderr.write(noise.endsWith("\n") ? noise : `${noise}\n`);
  if (summary && typeof summary.exitCode === "number") return summary.exitCode;
  return resolveProcessExit(combined, code);
}
