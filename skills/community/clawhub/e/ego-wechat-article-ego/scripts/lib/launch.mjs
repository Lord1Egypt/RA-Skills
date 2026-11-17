import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawn, spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { prepareArticle } from "./prepare.mjs";
import {
  RESULT_TAG,
  USAGE,
  defaultReceiptDir,
  egoMissingSummary,
  extractTaggedJson,
  formatResult,
  parseCheckArgs,
  parseCleanupArgs,
  parseSaveArgs,
  planOf,
  resolveProcessExit,
} from "./pure.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

const RUNNERS = {
  check: { exportName: "executeCheck", command: "check-login" },
  save: { exportName: "executeSave", command: "save-draft" },
  cleanup: { exportName: "executeCleanup", command: "cleanup" },
};

export function whichEgo(spawnSyncImpl = spawnSync, env = process.env) {
  const probe = spawnSyncImpl("ego-browser", ["--help"], { encoding: "utf8" });
  if (!(probe && probe.error)) return "ego-browser";
  const home = env && (env.HOME || env.USERPROFILE);
  if (!home) return null;
  const fallback = path.join(home, ".local", "bin", "ego-browser");
  const again = spawnSyncImpl(fallback, ["--help"], { encoding: "utf8" });
  if (again && again.error) return null;
  return fallback;
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
  if (kind === "check") return parseCheckArgs(argv);
  if (kind === "cleanup") return parseCleanupArgs(argv);
  return parseSaveArgs(argv);
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
    mkdtemp: deps.mkdtemp || ((prefix) => fs.promises.mkdtemp(prefix)),
    tmp: deps.tmp || os.tmpdir(),
    prepare: deps.prepare || prepareArticle,
    home: deps.home || os.homedir(),
    env: deps.env || process.env,
    runModule: deps.runModule || path.join(here, "editor-flow.mjs"),
    egoModule: deps.egoModule || path.join(here, "ego-deps.mjs"),
  };
  if (!runner) {
    io.stderr.write(`Unknown command: ${kind}\n${USAGE}`);
    return 1;
  }
  let args;
  try {
    args = parseKind(kind, argv);
  } catch (error) {
    io.stderr.write(`${error.message}\n${USAGE}`);
    return 1;
  }
  if (args.help) {
    io.stdout.write(USAGE);
    return 0;
  }

  const receiptDir = args.receiptDir || defaultReceiptDir(io.home, io.env);
  let article = null;
  if (kind === "save") {
    const prepared = await io.prepare({
      markdownPath: args.markdown,
      assetRoot: args.assetRoot,
      assetDir: receiptDir ? path.join(path.dirname(receiptDir), "assets") : path.join(io.tmp, "wechat-article-ego-assets"),
      title: args.title,
      digest: args.digest,
      sourceUrl: args.sourceUrl,
      fetchImpl: deps.fetchImpl,
      fsImpl: io.fs,
    });
    if (!prepared.ok) {
      io.stdout.write(formatResult({
        ok: false,
        exitCode: 1,
        command: runner.command,
        saved: false,
        error: prepared.error,
      }, { asJson: true }));
      return 1;
    }
    article = prepared.article;
  }

  const egoBin = io.whichEgo(io.spawnSync);
  if (!egoBin) {
    const summary = egoMissingSummary(runner.command);
    if (article) summary.plan = planOf(article, "");
    io.stdout.write(formatResult(summary, { asJson: true }));
    return 2;
  }

  const config = {
    command: runner.command,
    yes: Boolean(args.yes),
    expectAccount: args.expectAccount || "",
    receiptDir,
    screenshotDir: args.screenshotDir || "",
    article,
  };
  const dir = await io.mkdtemp(path.join(io.tmp, "ego-wechat-article-"));
  const entry = path.join(dir, "entry.mjs");
  const writeFile = io.fs.promises && io.fs.promises.writeFile
    ? io.fs.promises.writeFile.bind(io.fs.promises)
    : io.fs.writeFile;
  const removeDir = io.fs.promises && io.fs.promises.rm
    ? io.fs.promises.rm.bind(io.fs.promises)
    : io.fs.rm;
  let stdoutBuf = "";
  let stderrBuf = "";
  let code = 1;
  try {
    await writeFile(entry, renderEntry({
      config,
      runHref: pathToFileURL(io.runModule).href,
      depsHref: pathToFileURL(io.egoModule).href,
      exportName: runner.exportName,
    }));
    const href = pathToFileURL(entry).href;
    const child = io.spawn(egoBin, ["nodejs", "-e", `await import(${JSON.stringify(href)})`], {
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
    if (removeDir) await removeDir(dir, { recursive: true, force: true }).catch(() => {});
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
    .filter((line) => line && !line.includes(RESULT_TAG.trim()))
    .join("\n");
  if (noise) io.stderr.write(noise.endsWith("\n") ? noise : `${noise}\n`);
  if (summary && typeof summary.exitCode === "number") return summary.exitCode;
  return resolveProcessExit(combined, code);
}
