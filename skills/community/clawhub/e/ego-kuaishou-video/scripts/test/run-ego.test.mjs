import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import test from "node:test";
import { runEgoFile } from "../lib/run-ego.mjs";

function capture() {
  let text = "";
  return {
    text: () => text,
    write(chunk) {
      text += chunk;
    },
  };
}

function childWith({ stdout = "", stderr = "", code = 0, error } = {}) {
  const child = new EventEmitter();
  child.stdout = new EventEmitter();
  child.stderr = new EventEmitter();
  queueMicrotask(() => {
    if (error) {
      child.emit("error", error);
      return;
    }
    if (stdout) child.stdout.emit("data", stdout);
    if (stderr) child.stderr.emit("data", stderr);
    child.emit("close", code);
  });
  return child;
}

test("a missing script or missing ego-browser does not spawn the file", async () => {
  let spawned = 0;
  const usage = {
    stdout: capture(),
    stderr: capture(),
    whichEgo: () => "ego-browser",
    spawn() {
      spawned += 1;
    },
  };
  assert.equal(await runEgoFile("", usage), 1);
  assert.match(usage.stderr.text(), /usage/);

  const missing = {
    stdout: capture(),
    stderr: capture(),
    whichEgo: () => null,
    command: "comment",
    spawn() {
      throw new Error("should not spawn");
    },
  };
  assert.equal(await runEgoFile("/tmp/comment.js", missing), 2);
  assert.match(missing.stdout.text(), /ego-browser not found/);
  assert.match(missing.stdout.text(), /"command": "comment"/);
  assert.equal(spawned, 0);
});

test("runEgoFile forwards publish JSON and maps exit codes", async () => {
  let args = [];
  const ok = {
    stdout: capture(),
    stderr: capture(),
    whichEgo: () => "ego-browser",
    spawn(...spawnArgs) {
      args = spawnArgs;
      return childWith({
        stdout: `${JSON.stringify({ ok: true, status: "审核中" })}\n`,
        stderr: "上传完成",
        code: 0,
      });
    },
  };
  assert.equal(await runEgoFile("/tmp/publish.js", ok), 0);
  assert.equal(args[0], "ego-browser");
  assert.match(args[1][2], /publish\.js/);
  assert.match(ok.stdout.text(), /审核中/);
  assert.match(ok.stderr.text(), /上传完成/);

  const login = {
    stdout: capture(),
    stderr: capture(),
    whichEgo: () => "ego-browser",
    spawn() {
      return childWith({
        stdout: JSON.stringify({ ok: false, exitCode: 2, login_required: true }),
        code: 0,
      });
    },
  };
  assert.equal(await runEgoFile("/tmp/publish.js", login), 2);

  const wrapped = {
    stdout: capture(),
    stderr: capture(),
    whichEgo: () => "ego-browser",
    spawn() {
      return childWith({ stderr: "nodejs process exited with code 1", code: 0 });
    },
  };
  assert.equal(await runEgoFile("/tmp/publish.js", wrapped), 1);

  const crashed = {
    stdout: capture(),
    stderr: capture(),
    whichEgo: () => "ego-browser",
    spawn() {
      return childWith({ error: new Error("spawn ego-browser ENOENT") });
    },
  };
  assert.equal(await runEgoFile("/tmp/publish.js", crashed), 1);
  assert.match(crashed.stderr.text(), /ENOENT/);

  const bare = {
    stdout: capture(),
    stderr: capture(),
    whichEgo: () => "ego-browser",
    spawn() {
      const child = new EventEmitter();
      queueMicrotask(() => child.emit("close", 0));
      return child;
    },
  };
  assert.equal(await runEgoFile("/tmp/publish.js", bare), 0);
});
