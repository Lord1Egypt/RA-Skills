#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { parseArgs, shortError } from "./lib/calibre_common.mjs";
import { hash, statePath, readState, writeState, withStateLock, runId } from "./lib/run_store.mjs";
function main() {
  const raw = process.argv.slice(2);
  if (raw.includes("--help") || !raw.length)
    return {
      usage:
        "run_state.mjs <upsert|get|list|fail> --state FILE --run-id ID [--input-json PREPARED --session-key HANDLE]",
    };
  const command = raw.shift();
  if (!["upsert", "get", "list", "fail"].includes(command))
    throw new Error("supported state commands: upsert/get/list/fail");
  const a = parseArgs(raw, ["state", "run-id", "input-json", "session-key", "error"]);
  if (a._.length) throw new Error("unexpected positional argument");
  const file = statePath(a);
  const id = command === "list" ? null : runId(a["run-id"]);
  if (command === "list") return { ok: true, ...readState(file) };
  if (command === "get") return { ok: true, run: readState(file).runs[id] || null };
  return withStateLock(file, (s) => {
    if (command === "fail") {
      if (!Object.hasOwn(s.runs, id) || !a.error) throw new Error("run and --error required");
      s.runs[id].status = "failed";
      s.runs[id].error = a.error;
      writeState(file, s);
      return { ok: true, status: "failed", run_id: id };
    }
    if (Object.hasOwn(s.runs, id) || Object.hasOwn(s.completed, id))
      throw new Error("run id already registered/completed; never overwrite");
    if (!a["input-json"]) throw new Error("--input-json required");
    const input = path.resolve(a["input-json"]);
    const manifest = JSON.parse(fs.readFileSync(input, "utf8"));
    if (
      manifest.version !== 3 ||
      manifest.run_id !== id ||
      !Number.isSafeInteger(manifest.book_id) ||
      !manifest.book_uuid
    )
      throw new Error("prepared target/run mismatch");
    s.runs[id] = {
      run_id: id,
      status: "running",
      input_json: input,
      input_sha256: hash(input),
      book_id: manifest.book_id,
      library_id: manifest.library_id,
      file_hash: manifest.file_hash,
      lang: manifest.lang,
      session_key: a["session-key"] || null,
      created_at: new Date().toISOString(),
    };
    writeState(file, s);
    return { ok: true, run: s.runs[id] };
  });
}
try {
  console.log(JSON.stringify(main()));
} catch (e) {
  console.error(shortError(e));
  process.exitCode = 1;
}
