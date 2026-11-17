#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { args } from "./lib/arguments.mjs";
import { statePath, withStateLock, writeState, runId } from "./lib/run_store.mjs";
function main() {
  const raw = process.argv.slice(2);
  if (raw.includes("--help"))
    return {
      usage:
        "handle_completion.mjs --run-id ID --result-json FILE [--state-dir DIR]; result object requires matching run_id, ok:boolean, status:proposal_ready|completed|failed",
    };
  const a = args(raw, ["state", "state-dir", "run-id", "result-json"]);
  if (a._.length) throw new Error("unexpected arguments");
  const id = runId(a["run-id"]),
    file = statePath(a);
  return withStateLock(file, (s) => {
    if (!Object.hasOwn(s.runs, id)) return { ok: true, status: "stale_or_duplicate", run_id: id };
    const run = s.runs[id];
    if (run.status !== "running") throw new Error("run is not running");
    if (!a["result-json"]) throw new Error("--result-json required");
    const resultFile = path.resolve(a["result-json"]);
    if (fs.statSync(resultFile).size > 16 * 1024 * 1024) throw new Error("result exceeds 16 MiB");
    const result = JSON.parse(fs.readFileSync(resultFile, "utf8"));
    if (
      !result ||
      Array.isArray(result) ||
      result.run_id !== id ||
      typeof result.ok !== "boolean" ||
      !["proposal_ready", "completed", "failed"].includes(result.status)
    )
      throw new Error("result does not match run/result contract");
    if (!result.ok || result.status === "failed") {
      run.status = "failed";
      run.result_file = resultFile;
      writeState(file, s);
      process.exitCode = 1;
      return { ok: false, status: "failed", run_id: id };
    }
    s.completed[id] = { completed_at: new Date().toISOString(), result_file: resultFile };
    delete s.runs[id];
    writeState(file, s);
    return { ok: true, status: "completed", run_id: id, task: run.task, result };
  });
}
try {
  console.log(JSON.stringify(main()));
} catch (e) {
  console.error(e.message);
  process.exitCode = 1;
}
