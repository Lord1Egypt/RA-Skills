import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import test from "node:test";
import { renderEntry, runCheckCli } from "../lib/launch-check.mjs";

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

const io = (extra = {}) => ({
  stdout: capture(),
  stderr: capture(),
  whichEgo: () => "ego-browser",
  mkdtemp: async () => "/tmp/ego-wechat-test",
  fs: {
    writeFile: async () => {},
    rm: async () => {},
  },
  ...extra,
});

test("renderEntry inlines keep and the module URLs", () => {
  const source = renderEntry({
    config: { keep: true, taskName: "channels-扫码" },
    runHref: "file:///opt/run-check.mjs",
    depsHref: "file:///opt/ego-deps.mjs",
  });
  assert.match(source, /run-check\.mjs/);
  assert.match(source, /ego-deps\.mjs/);
  assert.match(source, /channels-扫码/);
  assert.match(source, /"keep":true/);
});

test("help and unknown args do not spawn ego-browser", async () => {
  let spawned = 0;
  const help = io({ spawn() { spawned += 1; } });
  assert.equal(await runCheckCli(["--help"], help), 0);
  assert.match(help.stdout.text(), /check-login/);
  const bad = io({ spawn() { spawned += 1; } });
  assert.equal(await runCheckCli(["--nope"], bad), 2);
  assert.match(bad.stderr.text(), /Unknown arg/);
  assert.equal(spawned, 0);
});

test("a missing ego-browser soft-fails with install steps", async () => {
  const deps = io({ whichEgo: () => null, spawn() { throw new Error("should not spawn"); } });
  const code = await runCheckCli([], deps);
  assert.equal(code, 2);
  assert.match(deps.stdout.text(), /ego-browser not found/);
  assert.match(deps.stdout.text(), /how_to_login_zh/);
});

test("runCheckCli maps the child JSON, filters noise, and honors exitCode", async () => {
  let entry = "";
  const summary = JSON.stringify({
    skill: "wechat-channels-video",
    login_required: false,
    exitCode: 0,
    ok: true,
  });
  const deps = io({
    fs: {
      writeFile: async (_file, source) => {
        entry = source;
      },
      rm: async () => {},
    },
    spawn() {
      return childWith({
        stderr: `{ "nope": true }\nnot-json {broken\n${summary}\nbrowser warning\n`,
        code: 7,
      });
    },
  });
  const code = await runCheckCli(["--keep", "--task-name", "channels-1"], deps);
  assert.equal(code, 0);
  assert.match(entry, /channels-1/);
  assert.match(entry, /"keep":true/);
  assert.match(deps.stdout.text(), /"ok": true/);
  assert.match(deps.stderr.text(), /browser warning/);
  assert.match(deps.stderr.text(), /not-json/);
  assert.doesNotMatch(deps.stderr.text(), /"login_required"/);
});

test("without a summary, the CLI forwards stdout and the reported node exit", async () => {
  const plain = io({
    spawn() {
      return childWith({ stdout: "hello from ego\n", code: 0 });
    },
  });
  assert.equal(await runCheckCli([], plain), 0);
  assert.match(plain.stdout.text(), /hello from ego/);

  const reported = io({
    spawn() {
      return childWith({ stderr: "ego's nodejs process exited with code 2\n", code: 0 });
    },
  });
  assert.equal(await runCheckCli([], reported), 2);

  const raw = io({
    spawn() {
      return childWith({ code: 7 });
    },
  });
  assert.equal(await runCheckCli([], raw), 7);

  const crashed = io({
    spawn() {
      return childWith({ error: new Error("spawn ego-browser ENOENT") });
    },
  });
  assert.equal(await runCheckCli([], crashed), 1);
  assert.match(crashed.stderr.text(), /ENOENT/);
});
