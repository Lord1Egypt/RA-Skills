import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const scripts = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function run(file, args) {
  return spawnSync(process.execPath, [path.join(scripts, file), ...args], { encoding: "utf8" });
}

test("the bins print help without posting", () => {
  for (const file of ["check-login.mjs", "post.mjs", "cleanup.mjs"]) {
    const result = run(file, ["--help"]);
    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /--yes/);
  }
  const missing = run("post.mjs", []);
  assert.equal(missing.status, 1);
  assert.match(missing.stderr, /Missing --text/);
});

test("the post bin rejects a missing image and does not upload a dry-run", () => {
  const missing = run("post.mjs", ["--text", "hi", "--image", "/tmp/does-not-exist-x-post.png"]);
  assert.equal(missing.status, 1, missing.stderr);
  assert.match(missing.stderr, /Image not found/);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "x-post-bin-"));
  const file = path.join(dir, "card.png");
  fs.writeFileSync(file, Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]));
  const draft = run("post.mjs", ["--text", "hi", "--image", file]);
  assert.ok(draft.status === 2 || draft.status === 3, draft.stderr);
  assert.match(draft.stdout, /md5/);
  assert.doesNotMatch(draft.stdout, /media_id/);
});
