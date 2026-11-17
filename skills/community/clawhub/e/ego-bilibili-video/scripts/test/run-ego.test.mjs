import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import { test } from "node:test";
import { runEgoFile } from "../lib/run-ego.mjs";

function makeStream(data) {
  const s = new EventEmitter();
  setTimeout(() => s.emit("data", Buffer.from(data)), 0);
  return s;
}

function fakeIO({ ego = true, exitCode = 0, stdout = "", stderr = "" } = {}) {
  const out = [];
  const err = [];
  return {
    deps: {
      spawn: () => ({
        stdout: stdout ? makeStream(stdout) : null,
        stderr: stderr ? makeStream(stderr) : null,
        on: (evt, cb) => {
          if (evt === "close") setTimeout(() => cb(exitCode), 0);
        },
      }),
      stdout: { write: (s) => out.push(s) },
      stderr: { write: (s) => err.push(s) },
      whichEgo: () => (ego ? "ego-browser" : null),
      command: "publish",
    },
    out,
    err,
  };
}

test("runEgoFile: missing ego-browser exits 2 with summary", async () => {
  const { deps, out } = fakeIO({ ego: false });
  const code = await runEgoFile("/tmp/x.mjs", deps);
  assert.equal(code, 2);
  assert.match(out.join(""), /login_required/);
});

test("runEgoFile: usage error without file", async () => {
  const { deps, err } = fakeIO();
  const code = await runEgoFile("", deps);
  assert.equal(code, 1);
  assert.match(err.join(""), /usage/);
});

test("runEgoFile: propagates child exit code and output", async () => {
  const { deps, out } = fakeIO({ exitCode: 0, stdout: '{"ok":true}\n' });
  const code = await runEgoFile("/tmp/x.mjs", deps);
  assert.equal(code, 0);
  assert.match(out.join(""), /"ok":true/);
});

test("runEgoFile: login_required stdout maps to exit 2", async () => {
  const body = JSON.stringify({ login_required: true, exit_code: 2 });
  const { deps } = fakeIO({ exitCode: 0, stdout: `${body}\n` });
  const code = await runEgoFile("/tmp/x.mjs", deps);
  assert.equal(code, 2);
});

test("runEgoFile: spawn error resolves 1", async () => {
  const out = [];
  const err = [];
  const code = await runEgoFile("/tmp/x.mjs", {
    spawn: () => ({
      stdout: null,
      stderr: null,
      on: (evt, cb) => {
        if (evt === "error") setTimeout(() => cb(new Error("spawn fail")), 0);
      },
    }),
    stdout: { write: (s) => out.push(s) },
    stderr: { write: (s) => err.push(s) },
    whichEgo: () => "ego-browser",
    command: "publish",
  });
  assert.equal(code, 1);
  assert.match(err.join(""), /spawn fail/);
});
