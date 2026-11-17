import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import test from "node:test";
import { renderEntry, runCli } from "../lib/launch.mjs";

function capture() {
  let text = "";
  return {
    text: () => text,
    write(chunk) {
      text += chunk;
    },
  };
}

function childWith(stderr, code = 0) {
  const child = new EventEmitter();
  child.stdout = new EventEmitter();
  child.stderr = new EventEmitter();
  queueMicrotask(() => {
    if (stderr) child.stderr.emit("data", stderr);
    child.emit("close", code);
  });
  return child;
}

test("renderEntry inlines the Saved config", () => {
  const source = renderEntry({
    config: { command: "saved", query: "海边", outDir: "/tmp/ig" },
    runHref: "file:///opt/ig-run.mjs",
    depsHref: "file:///opt/ig-ego.mjs",
  });
  assert.match(source, /ig-run\.mjs/);
  assert.match(source, /海边/);
});

test("help and a bad count do not spawn ego-browser", async () => {
  const stdout = capture();
  const stderr = capture();
  let spawned = 0;
  const help = await runCli(["--help"], { stdout, stderr, spawn() { spawned += 1; } });
  assert.equal(help, 0);
  assert.match(stdout.text(), /instagram-saved-download/);
  const bad = await runCli(["--count", "0"], { stdout, stderr, spawn() { spawned += 1; } });
  assert.equal(bad, 2);
  assert.equal(spawned, 0);
});

test("runCli maps a login summary to exit 2 and a missing ego binary to exit 1", async () => {
  const stdout = capture();
  const stderr = capture();
  let entry = "";
  const summary = JSON.stringify({ skill: "instagram-saved-download", ok: false, login_required: true, exitCode: 2 });
  const code = await runCli(["--count", "2", "--out", "/tmp/ig"], {
    stdout,
    stderr,
    now: 7,
    resolve: (value) => value,
    mkdtemp: async () => "/tmp",
    fs: {
      writeFile: async (_file, source) => {
        entry = source;
      },
      rm: async () => {},
    },
    spawn() {
      return childWith(`${summary}\nego's nodejs process exited with code 2\n`, 0);
    },
  });
  assert.equal(code, 2);
  assert.match(entry, /instagram-saved-7/);
  assert.match(stdout.text(), /login_required/);

  const missing = await runCli(["list", "--out", "/tmp/ig"], {
    stdout: capture(),
    stderr,
    resolve: (value) => value,
    mkdtemp: async () => "/tmp",
    fs: { writeFile: async () => {}, rm: async () => {} },
    spawn() {
      const child = new EventEmitter();
      child.stdout = new EventEmitter();
      child.stderr = new EventEmitter();
      queueMicrotask(() => child.emit("error", new Error("spawn ego-browser ENOENT")));
      return child;
    },
  });
  assert.equal(missing, 1);
  assert.match(stderr.text(), /ENOENT/);
});
