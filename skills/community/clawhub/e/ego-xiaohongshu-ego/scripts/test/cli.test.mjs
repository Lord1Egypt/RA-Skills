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

test("the bins print help and reject a missing cover without uploading", () => {
  for (const file of ["check-login.mjs", "post-video.mjs", "cleanup.mjs", "edit-cover.mjs"]) {
    const result = run(file, ["--help"]);
    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /--yes/);
  }
  const missing = run("post-video.mjs", []);
  assert.equal(missing.status, 1);
  assert.match(missing.stderr, /Missing --video/);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "xhs-cli-"));
  const video = path.join(dir, "clip.mp4");
  const cover = path.join(dir, "cover-3x4.png");
  fs.writeFileSync(video, "mp4");
  const result = run("post-video.mjs", [
    "--video", video, "--title", "标题", "--desc", "正文", "--cover", cover,
  ]);
  assert.equal(result.status, 1);
  assert.match(result.stdout, /--cover not found/);
  assert.doesNotMatch(`${result.stdout}\n${result.stderr}`, /clicked_publish":true/);
  const edit = run("edit-cover.mjs", ["--note-id", "nope", "--cover", video]);
  assert.equal(edit.status, 1);
  assert.match(edit.stdout, /note-id|png|jpg/);
  fs.rmSync(dir, { recursive: true, force: true });
});
