#!/usr/bin/env node
import { args } from "./lib/arguments.mjs";
import { readState, statePath, withStateLock, writeState, runId } from "./lib/run_store.mjs";
function main() {
  const raw = process.argv.slice(2);
  if (raw.includes("--help") || !raw.length)
    return {
      usage:
        "run_state.mjs <upsert|get|list|fail> --run-id ID [--session-key HANDLE --task TEXT] [--state-dir DIR]",
    };
  const command = raw.shift();
  if (!["upsert", "get", "list", "fail"].includes(command))
    throw new Error("supported commands: upsert/get/list/fail");
  const a = args(raw, ["state", "state-dir", "run-id", "session-key", "task", "error"]);
  if (a._.length) throw new Error("unexpected arguments");
  const file = statePath(a),
    id = command === "list" ? null : runId(a["run-id"]);
  if (command === "list") return { ok: true, ...readState(file) };
  if (command === "get") return { ok: true, run: readState(file).runs[id] || null };
  return withStateLock(file, (s) => {
    if (command === "fail") {
      if (!Object.hasOwn(s.runs, id) || !a.error) throw new Error("run and error required");
      s.runs[id].status = "failed";
      s.runs[id].error = a.error;
    } else {
      if (Object.hasOwn(s.runs, id) || Object.hasOwn(s.completed, id))
        throw new Error("run id already used");
      if (!a["session-key"] || !a.task) throw new Error("session-key and task required");
      s.runs[id] = {
        run_id: id,
        session_key: a["session-key"],
        task: a.task,
        status: "running",
        created_at: new Date().toISOString(),
      };
    }
    writeState(file, s);
    return { ok: true, run: s.runs[id] };
  });
}
try {
  console.log(JSON.stringify(main()));
} catch (e) {
  console.error(e.message);
  process.exitCode = 1;
}
