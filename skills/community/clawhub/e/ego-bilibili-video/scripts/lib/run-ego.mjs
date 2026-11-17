import { spawn, spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";
import { egoMissingSummary, resolveEgoExit } from "./pure.mjs";

function whichEgo() {
  const probe = spawnSync("ego-browser", ["--help"], { encoding: "utf8" });
  return probe.error ? null : "ego-browser";
}

export async function runEgoFile(file, deps = {}) {
  const io = {
    spawn: deps.spawn || spawn,
    stdout: deps.stdout || process.stdout,
    stderr: deps.stderr || process.stderr,
    whichEgo: deps.whichEgo || whichEgo,
    command: deps.command || "publish",
  };

  if (!file) {
    io.stderr.write("usage: run-ego.mjs <script.mjs>\n");
    return 1;
  }

  if (!io.whichEgo()) {
    const summary = egoMissingSummary(io.command);
    io.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
    return 2;
  }

  const href = pathToFileURL(file).href;
  const child = io.spawn("ego-browser", ["nodejs", "-e", `await import(${JSON.stringify(href)})`], {
    stdio: ["ignore", "pipe", "pipe"],
  });
  let stdoutBuf = "";
  let stderrBuf = "";
  if (child.stdout) {
    child.stdout.on("data", (chunk) => {
      stdoutBuf += chunk;
    });
  }
  if (child.stderr) {
    child.stderr.on("data", (chunk) => {
      stderrBuf += chunk;
    });
  }
  const code = await new Promise((resolve) => {
    child.on("error", (error) => {
      stderrBuf += String(error.message || error);
      resolve(1);
    });
    child.on("close", (status) => resolve(status ?? 1));
  });

  if (stdoutBuf) io.stdout.write(stdoutBuf.endsWith("\n") ? stdoutBuf : `${stdoutBuf}\n`);
  if (stderrBuf) io.stderr.write(stderrBuf.endsWith("\n") ? stderrBuf : `${stderrBuf}\n`);
  return resolveEgoExit({ stdout: stdoutBuf, stderr: stderrBuf, code });
}
