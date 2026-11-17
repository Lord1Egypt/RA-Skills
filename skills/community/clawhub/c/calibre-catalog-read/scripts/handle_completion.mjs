#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { parseArgs, shortError } from "./lib/calibre_common.mjs";
import { statePath, writeState, withStateLock, runId } from "./lib/run_store.mjs";
const PIPELINE = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  "run_analysis_pipeline.py",
);
function main() {
  const raw = process.argv.slice(2);
  if (raw.includes("--help"))
    return {
      usage:
        "handle_completion.mjs --run-id ID --analysis-json FILE --proposal-jsonl NEW_FILE [--state FILE]",
    };
  const a = parseArgs(raw, ["run-id", "analysis-json", "proposal-jsonl", "state"]);
  if (a._.length) throw new Error("unexpected positional argument");
  const id = runId(a["run-id"]),
    file = statePath(a);
  return withStateLock(file, (s) => {
    if (!Object.hasOwn(s.runs, id))
      return { ok: true, status: "stale_or_duplicate", run_id: id, remote_work: false };
    const run = s.runs[id];
    if (run.status !== "running")
      throw new Error("run is not running; failed completion is not automatically retried");
    try {
      if (!a["analysis-json"] || !a["proposal-jsonl"])
        throw new Error("--analysis-json and --proposal-jsonl required");
      const cp = spawnSync(
        "python3",
        [
          PIPELINE,
          "complete",
          "--prepared-input",
          run.input_json,
          "--expected-input-sha256",
          run.input_sha256,
          "--analysis-json",
          path.resolve(a["analysis-json"]),
          "--proposal-jsonl",
          path.resolve(a["proposal-jsonl"]),
        ],
        {
          encoding: "utf8",
          timeout: 120000,
          killSignal: "SIGKILL",
          maxBuffer: 2 * 1024 * 1024,
          env: Object.fromEntries(
            ["PATH", "HOME", "LANG", "SYSTEMROOT", "WINDIR"]
              .filter((k) => process.env[k] !== undefined)
              .map((k) => [k, process.env[k]]),
          ),
        },
      );
      if (cp.error || cp.status !== 0)
        throw new Error(shortError(cp.error || cp.stderr || "completion failed"));
      const result = JSON.parse(cp.stdout);
      if (
        !result.ok ||
        result.status !== "proposal_created" ||
        result.run_id !== id ||
        !fs.existsSync(result.proposal_jsonl)
      )
        throw new Error("pipeline did not create a verified proposal");
      s.completed[id] = {
        at: new Date().toISOString(),
        input_sha256: run.input_sha256,
        proposal_jsonl: result.proposal_jsonl,
      };
      delete s.runs[id];
      writeState(file, s);
      return result;
    } catch (e) {
      run.status = "failed";
      run.error = shortError(e);
      writeState(file, s);
      throw e;
    }
  });
}
try {
  console.log(JSON.stringify(main()));
} catch (e) {
  console.error(shortError(e));
  process.exitCode = 1;
}
