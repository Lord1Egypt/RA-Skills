import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { USAGE, exitCodeFor, parseArgs, readSummary, toConfig } from "./pure.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

export function renderEntry({ config, runHref, depsHref }) {
  return [
    `import { execute } from ${JSON.stringify(runHref)};`,
    `import { createEgoBrowser } from ${JSON.stringify(depsHref)};`,
    `import fs from "node:fs/promises";`,
    `import path from "node:path";`,
    `const config = ${JSON.stringify(config)};`,
    `const summary = await execute(config, { browser: createEgoBrowser(), fs, path });`,
    `console.log(JSON.stringify(summary));`,
    `if (summary.exitCode) process.exitCode = summary.exitCode;`,
    "",
  ].join("\n");
}

export async function runCli(argv, deps = {}) {
  const io = {
    fs: deps.fs || fs,
    spawn: deps.spawn || spawn,
    stdout: deps.stdout || process.stdout,
    stderr: deps.stderr || process.stderr,
    resolve: deps.resolve || ((value) => path.resolve(value)),
    home: deps.home || process.env.HOME,
    now: deps.now || Date.now(),
    mkdtemp: deps.mkdtemp || ((prefix) => fs.mkdtemp(prefix)),
    tmp: deps.tmp || os.tmpdir(),
    runModule: deps.runModule || path.join(here, "run.mjs"),
    egoModule: deps.egoModule || path.join(here, "ego-deps.mjs"),
  };
  let args;
  try {
    args = parseArgs(argv);
  } catch (error) {
    io.stderr.write(`${error.message}\n${USAGE}`);
    return 2;
  }
  if (args.help) {
    io.stdout.write(`${USAGE}`);
    return 0;
  }
  let config;
  try {
    config = toConfig(args, { resolve: io.resolve, home: io.home, now: io.now });
  } catch (error) {
    io.stderr.write(`${error.message}\n${USAGE}`);
    return 2;
  }

  const dir = await io.mkdtemp(path.join(io.tmp, "ego-instagram-"));
  const entry = path.join(dir, "entry.mjs");
  const source = renderEntry({
    config,
    runHref: pathToFileURL(io.runModule).href,
    depsHref: pathToFileURL(io.egoModule).href,
  });
  await io.fs.writeFile(entry, source);
  const href = pathToFileURL(entry).href;
  let stdoutBuf = "";
  let stderrBuf = "";
  let code = 1;
  try {
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
  const summary = readSummary(combined);
  if (summary && !readSummary(stdoutBuf)) io.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
  else if (stdoutBuf) io.stdout.write(stdoutBuf);
  if (stderrBuf) io.stderr.write(stderrBuf);
  const matched = combined.match(/nodejs process exited with code (\d+)/);
  const reported = matched ? Number(matched[1]) : code === 0 ? null : code;
  return exitCodeFor(summary, reported);
}
