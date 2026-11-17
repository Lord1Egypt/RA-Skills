import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { RESULT_TAG } from "../lib/pure.mjs";
import { renderEntry, runCli, whichEgo } from "../lib/launch.mjs";

function capture() {
  let text = "";
  return { text: () => text, write(chunk) { text += chunk; } };
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
  mkdtemp: async () => path.join(os.tmpdir(), "ego-wechat-article-test"),
  fs: {
    promises: {
      writeFile: async () => {},
      rm: async () => {},
    },
  },
  prepare: async () => ({ ok: true, article: { title: "题", hash: "abc", imageCount: 0, images: [], fidelity: [] } }),
  ...extra,
});

test("whichEgo maps PATH, a missing binary, and the home fallback", () => {
  assert.equal(whichEgo(() => ({ error: new Error("missing") }), {}), null);
  assert.equal(whichEgo(() => ({ status: 0 })), "ego-browser");
  assert.equal(whichEgo(() => null), "ego-browser");
  const fallback = whichEgo((cmd) => (
    cmd === "ego-browser" ? { error: new Error("no path") } : { status: 0 }
  ), { HOME: path.join(os.tmpdir(), "fixture-home") });
  assert.match(fallback, /ego-browser$/);
  const live = whichEgo();
  const homeBin = path.join(process.env.HOME || process.env.USERPROFILE || "", ".local", "bin", "ego-browser");
  assert.ok(live === null || live === "ego-browser" || live === homeBin);
});

test("renderEntry inlines the save config", () => {
  const source = renderEntry({
    config: { yes: false, article: { title: "题" } },
    runHref: "file:///opt/editor-flow.mjs",
    depsHref: "file:///opt/ego-deps.mjs",
    exportName: "executeSave",
  });
  assert.match(source, /executeSave/);
  assert.match(source, /WXARTICLE/);
  assert.match(source, /"yes":false/);
});

test("help and bad arguments do not spawn", async () => {
  let spawned = 0;
  const help = io({ spawn() { spawned += 1; } });
  assert.equal(await runCli("save", ["--help"], help), 0);
  assert.match(help.stdout.text(), /--markdown/);
  assert.equal(await runCli("check", ["-h"], io()), 0);
  assert.equal(await runCli("cleanup", ["--help"], io()), 0);
  const bad = io();
  assert.equal(await runCli("save", ["--markdown", "/absolute/path/a.md", "--nope"], bad), 1);
  assert.match(bad.stderr.text(), /Unknown/);
  assert.equal(await runCli("nope", [], io()), 1);
  assert.equal(spawned, 0);
  const missing = io({ prepare: async () => ({ ok: false, error: "cannot read markdown: missing" }) });
  assert.equal(await runCli("save", ["--markdown", "/absolute/path/missing.md"], missing), 1);
  assert.match(missing.stdout.text(), /cannot read/);
});

test("a missing ego-browser soft-fails after the plan is built", async () => {
  const deps = io({ whichEgo: () => null, spawn() { throw new Error("should not spawn"); } });
  assert.equal(await runCli("save", ["--markdown", "/absolute/path/a.md"], deps), 2);
  assert.match(deps.stdout.text(), /ego-browser not found/);
  assert.match(deps.stdout.text(), /题/);
  const check = io({ whichEgo: () => null });
  assert.equal(await runCli("check", [], check), 2);
});

test("without --yes the plan is fetched and nothing is marked saved", async () => {
  let entry = "";
  const deps = io({
    fs: { promises: { writeFile: async (_file, source) => { entry = source; }, rm: async () => {} } },
    spawn() {
      return childWith({
        stdout: `${RESULT_TAG}${JSON.stringify({ exitCode: 3, confirmation_required: true, saved: false, title: "题" })}\n`,
      });
    },
  });
  const code = await runCli("save", ["--markdown", "/absolute/path/a.md", "--expect-account", "加选"], deps);
  assert.equal(code, 3);
  assert.match(entry, /"yes":false/);
  assert.match(deps.stdout.text(), /confirmation_required/);
});

test("--yes prints the saved line and --json keeps the summary", async () => {
  let entry = "";
  const deps = io({
    fs: {
      promises: {
        writeFile: async (_file, source) => { entry = source; },
        rm: async () => { throw new Error("rm failed"); },
      },
    },
    spawn() {
      return childWith({
        stdout: `${RESULT_TAG}${JSON.stringify({ exitCode: 0, saved: true, title: "题", account: "加选", draftId: "9" })}\n`,
        stderr: "noise\n",
      });
    },
  });
  const code = await runCli("save", ["--markdown", "/absolute/path/a.md", "--yes", "--json"], deps);
  assert.equal(code, 0);
  assert.match(entry, /"yes":true/);
  assert.match(deps.stdout.text(), /"draftId": "9"/);
  assert.match(deps.stderr.text(), /noise/);
  const plain = io({
    spawn() {
      return childWith({
        stdout: `${RESULT_TAG}${JSON.stringify({ exitCode: 0, saved: true, title: "题", account: "加选" })}\n`,
      });
    },
  });
  assert.equal(await runCli("save", ["--markdown", "/absolute/path/a.md", "--yes"], plain), 0);
  assert.match(plain.stdout.text(), /^saved 题/);
});

test("spawn failures and untagged output stay visible", async () => {
  const broken = io({
    spawn() { return childWith({ error: new Error("spawn failed") }); },
  });
  assert.equal(await runCli("check", [], broken), 1);
  assert.match(broken.stderr.text(), /spawn failed/);
  const plain = io({
    spawn() { return childWith({ stdout: "hello", code: 0 }); },
  });
  assert.equal(await runCli("cleanup", [], plain), 0);
  assert.match(plain.stdout.text(), /hello/);
  const threw = io({
    spawn() { throw new Error("boom"); },
  });
  assert.equal(await runCli("check", [], threw), 1);
  assert.match(threw.stderr.text(), /boom/);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "wx-launch-"));
  const markdown = path.join(dir, "post.md");
  fs.writeFileSync(markdown, "---\ntitle: 题\n---\n\n正文\n");
  const real = io({
    prepare: undefined,
    fs,
    whichEgo: () => null,
  });
  assert.equal(await runCli("save", ["--markdown", markdown, "--title", "改过的题"], real), 2);
  assert.match(real.stdout.text(), /改过的题/);
  fs.rmSync(dir, { recursive: true, force: true });
});
