import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { renderEntry, runCli } from "../lib/launch.mjs";

function capture() {
  let text = "";
  return { text: () => text, write(chunk) { text += chunk; } };
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

test("renderEntry inlines config and absolute module URLs", () => {
  const source = renderEntry({
    config: { command: "search", query: "壁纸", outDir: "/tmp/pins" },
    runHref: "file:///opt/run.mjs",
    depsHref: "file:///opt/ego-deps.mjs",
  });
  assert.match(source, /file:\/\/\/opt\/run\.mjs/);
  assert.match(source, /壁纸/);
  assert.match(source, /createEgoBrowser/);
});

test("help and invalid args do not spawn ego-browser", async () => {
  const stdout = capture();
  const stderr = capture();
  let spawned = 0;
  const code = await runCli(["--help"], { stdout, stderr, spawn() { spawned += 1; } });
  assert.equal(code, 0);
  assert.match(stdout.text(), /pinterest-download/);
  assert.equal(spawned, 0);
  const bad = await runCli(["--query"], { stdout, stderr, spawn() { spawned += 1; } });
  assert.equal(bad, 2);
  assert.match(stderr.text(), /Missing value/);
  assert.equal(spawned, 0);
});

test("runCli mirrors stderr JSON and maps login_required to exit 2", async () => {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "ego-launch-"));
  const stdout = capture();
  const stderr = capture();
  let entry = "";
  const summary = JSON.stringify({ skill: "pinterest-download", ok: false, login_required: true, exitCode: 2 });
  const code = await runCli(["--query", "wallpaper", "--count", "2", "--out", dir], {
    stdout,
    stderr,
    now: 42,
    resolve: (value) => value,
    mkdtemp: async () => dir,
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
  assert.match(entry, /wallpaper/);
  assert.match(entry, /pinterest-download-42/);
  assert.match(stdout.text(), /login_required/);
  assert.match(stderr.text(), /exited with code 2/);
});

test("bad config is rejected before ego-browser starts", async () => {
  const stderr = capture();
  let spawned = 0;
  const code = await runCli(["--size", "huge", "--query", "wallpaper", "--out", "/tmp/pins"], {
    stdout: capture(),
    stderr,
    resolve: (value) => value,
    spawn() {
      spawned += 1;
    },
  });
  assert.equal(code, 2);
  assert.match(stderr.text(), /--size/);
  assert.equal(spawned, 0);
});

test("stdout from ego is forwarded when it already contains the summary", async () => {
  const stdout = capture();
  const payload = JSON.stringify({ skill: "pinterest-download", ok: true, exitCode: 0 });
  const code = await runCli(["--query", "wallpaper", "--out", "/tmp/pins"], {
    stdout,
    stderr: capture(),
    resolve: (value) => value,
    mkdtemp: async () => "/tmp",
    fs: { writeFile: async () => {}, rm: async () => {} },
    spawn() {
      const child = new EventEmitter();
      child.stdout = new EventEmitter();
      child.stderr = new EventEmitter();
      queueMicrotask(() => {
        child.stdout.emit("data", payload);
        child.emit("close", 0);
      });
      return child;
    },
  });
  assert.equal(code, 0);
  assert.match(stdout.text(), /"ok":true/);
});

test("runCli returns 0 when the summary says ok, and 1 when ego is missing", async () => {
  const stdout = capture();
  const stderr = capture();
  const ok = await runCli(["download", "--url", "https://i.pinimg.com/a.jpg", "--out", "/tmp/pins", "--allow-anonymous"], {
    stdout,
    stderr,
    resolve: (value) => value,
    mkdtemp: async () => "/tmp",
    fs: { writeFile: async () => {}, rm: async () => {} },
    spawn() {
      return childWith(JSON.stringify({ skill: "pinterest-download", ok: true, exitCode: 0 }), 0);
    },
  });
  assert.equal(ok, 0);
  const missing = await runCli(["--query", "wallpaper", "--out", "/tmp/pins"], {
    stdout,
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
