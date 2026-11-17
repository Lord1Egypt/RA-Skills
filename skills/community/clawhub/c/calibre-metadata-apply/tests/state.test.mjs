import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync, spawn } from "node:child_process";
const base = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../scripts");
function fixture(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "calibre-state-test-"));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const run = (name, args) =>
    spawnSync(process.execPath, [path.join(base, name), ...args, "--state-dir", dir], {
      encoding: "utf8",
      env: { PATH: process.env.PATH, HOME: dir },
    });
  return { dir, run };
}
test("failed/corrupt/wrong-run results do not silently consume active state", (t) => {
  const f = fixture(t);
  assert.equal(
    f.run("run_state.mjs", ["upsert", "--run-id", "r1", "--session-key", "s", "--task", "test"])
      .status,
    0,
  );
  const result = path.join(f.dir, "result.json");
  fs.writeFileSync(result, JSON.stringify({ run_id: "wrong", ok: true, status: "proposal_ready" }));
  assert.notEqual(
    f.run("handle_completion.mjs", ["--run-id", "r1", "--result-json", result]).status,
    0,
  );
  assert.ok(JSON.parse(fs.readFileSync(path.join(f.dir, "runs.json"))).runs.r1);
  fs.writeFileSync(path.join(f.dir, "runs.json"), "{broken");
  assert.notEqual(f.run("run_state.mjs", ["list"]).status, 0);
  assert.equal(fs.readFileSync(path.join(f.dir, "runs.json"), "utf8"), "{broken");
});
test("concurrent duplicate completion returns one completed result", async (t) => {
  const f = fixture(t);
  assert.equal(
    f.run("run_state.mjs", ["upsert", "--run-id", "r1", "--session-key", "s", "--task", "test"])
      .status,
    0,
  );
  const result = path.join(f.dir, "result.json");
  fs.writeFileSync(result, JSON.stringify({ run_id: "r1", ok: true, status: "proposal_ready" }));
  const launch = () =>
    new Promise((resolve) => {
      const p = spawn(
        process.execPath,
        [
          path.join(base, "handle_completion.mjs"),
          "--state-dir",
          f.dir,
          "--run-id",
          "r1",
          "--result-json",
          result,
        ],
        { env: { PATH: process.env.PATH, HOME: f.dir } },
      );
      let out = "";
      p.stdout.on("data", (x) => (out += x));
      p.on("close", (code) => resolve({ code, out }));
    });
  const results = await Promise.all([launch(), launch()]);
  assert.equal(
    results.filter((r) => r.code === 0 && JSON.parse(r.out).status === "completed").length,
    1,
  );
  assert.equal(
    f.run("handle_completion.mjs", ["--run-id", "r1", "--result-json", "/missing"]).status,
    0,
  );
  assert.notEqual(
    f.run("run_state.mjs", ["upsert", "--run-id", "r1", "--session-key", "s", "--task", "test"])
      .status,
    0,
  );
});
