import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { RESULT_TAG, exploreUrl } from "../lib/pure.mjs";
import { renderEntry, runCli, whichEgo } from "../lib/launch.mjs";

const NOTE = "6aeae281000000000e00cb56";

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
  mkdtemp: async () => "/tmp/ego-xiaohongshu-test",
  fs: { writeFile: async () => {}, rm: async () => {} },
  existsSync: () => true,
  statSync: () => ({ size: 8, isFile: () => true }),
  ...extra,
});

const postArgs = ["--video", "/absolute/path/to/video.mp4", "--title", "标题", "--desc", "正文"];

test("whichEgo maps the probe and the home-bin fallback", () => {
  assert.equal(whichEgo(() => ({ error: new Error("missing") }), {}), null);
  assert.equal(whichEgo(() => ({ status: 0 })), "ego-browser");
  assert.equal(whichEgo(() => null), "ego-browser");
  const home = "/tmp/fixture-home";
  const fallback = whichEgo((cmd) => (
    cmd === "ego-browser" ? { error: new Error("no path") } : { status: 0 }
  ), { HOME: home });
  assert.equal(fallback, path.join(home, ".local", "bin", "ego-browser"));
  const live = whichEgo();
  // The live probe depends on the host: null when ego is not installed,
  // "ego-browser" when it is on PATH, and the absolute ~/.local/bin path when
  // it is installed but that directory is missing from PATH (non-interactive
  // shells). All three are valid results.
  const homeBin = path.join(process.env.HOME || process.env.USERPROFILE || "", ".local", "bin", "ego-browser");
  assert.ok(live === null || live === "ego-browser" || live === homeBin);
});

test("renderEntry inlines the publish config", () => {
  const source = renderEntry({
    config: { yes: true, title: '标题 "甲"', cover: "/absolute/path/to/cover-3x4.png" },
    runHref: "file:///opt/publish-flow.mjs",
    depsHref: "file:///opt/ego-deps.mjs",
    exportName: "executePost",
  });
  assert.match(source, /executePost/);
  assert.match(source, /cover-3x4\.png/);
  assert.match(source, /XHSEGO/);
});

test("help, unknown args, and a missing cover do not spawn", async () => {
  let spawned = 0;
  const help = io({ spawn() { spawned += 1; } });
  assert.equal(await runCli("post", ["--help"], help), 0);
  assert.match(help.stdout.text(), /--yes/);
  assert.equal(await runCli("check", ["-h"], io()), 0);
  assert.equal(await runCli("cleanup", ["--help"], io()), 0);
  assert.equal(await runCli("edit", ["--help"], io()), 0);
  const bad = io();
  assert.equal(await runCli("post", [...postArgs, "--nope"], bad), 1);
  assert.match(bad.stderr.text(), /Unknown arg/);
  assert.equal(await runCli("nope", [], io()), 1);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "xhs-launch-"));
  const video = path.join(dir, "clip.mp4");
  fs.writeFileSync(video, "mp4");
  const missing = io({
    existsSync: fs.existsSync,
    statSync: fs.statSync,
    spawn() { spawned += 1; },
  });
  const code = await runCli("post", [
    "--video", video, "--title", "标题", "--desc", "正文", "--cover", path.join(dir, "cover-3x4.png"),
  ], missing);
  assert.equal(code, 1);
  assert.match(missing.stdout.text(), /--cover not found/);
  assert.equal(spawned, 0);
  const linked = io({ spawn() { spawned += 1; } });
  const linkedCode = await runCli("post", [...postArgs, "--desc", "见 github.com/octo/hello"], linked);
  assert.equal(linkedCode, 4);
  assert.match(linked.stdout.text(), /github.com\/octo\/hello/);
  assert.match(linked.stdout.text(), /strip-links/);
  assert.equal(spawned, 0);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("a missing ego-browser soft-fails before upload", async () => {
  const deps = io({ whichEgo: () => null, spawn() { throw new Error("should not spawn"); } });
  assert.equal(await runCli("post", [...postArgs, "--cover", "/absolute/path/to/cover-3x4.png"], deps), 2);
  assert.match(deps.stdout.text(), /ego-browser not found/);
  assert.match(deps.stdout.text(), /cover-3x4/);
  const edit = io({ whichEgo: () => null });
  assert.equal(await runCli("edit", ["--note-id", NOTE, "--cover", "/absolute/path/to/cover-3x4.png"], edit), 2);
  assert.match(edit.stdout.text(), /best-effort|cover-3x4|update/);
  const check = io({ whichEgo: () => null });
  assert.equal(await runCli("check", [], check), 2);
});

test("without --yes the plan is fetched and the cover path is kept", async () => {
  let entry = "";
  const deps = io({
    fs: { writeFile: async (_file, source) => { entry = source; }, rm: async () => {} },
    spawn() {
      return childWith({
        stdout: `${RESULT_TAG}${JSON.stringify({
          exitCode: 3, confirmation_required: true, uploaded: false, plan: { cover: "/absolute/path/to/cover-3x4.png" },
        })}\n`,
      });
    },
  });
  const code = await runCli("post", [...postArgs, "--cover", "/absolute/path/to/cover-3x4.png", "--expect-account", "听懂AI"], deps);
  assert.equal(code, 3);
  assert.match(deps.stdout.text(), /cover-3x4/);
  assert.match(entry, /"yes":false/);
  assert.match(entry, /executePost/);
  assert.doesNotMatch(entry, /clicked_publish":true/);
});

test("--yes prints the explore URL and --json keeps the summary", async () => {
  const url = exploreUrl(NOTE);
  let entry = "";
  const deps = io({
    fs: {
      writeFile: async (_file, source) => { entry = source; },
      rm: () => Promise.reject(new Error("rm failed")),
    },
    spawn() {
      return childWith({
        stdout: `${RESULT_TAG}${JSON.stringify({ ok: true, published: true, exitCode: 0, url, cover_confirmed: true })}\n`,
        stderr: "browser warning",
      });
    },
  });
  const code = await runCli("post", [...postArgs, "--cover", "/absolute/path/to/cover-3x4.png", "--yes", "--keep"], deps);
  assert.equal(code, 0);
  assert.equal(deps.stdout.text(), `${url}\n`);
  assert.match(entry, /executePost/);
  assert.match(deps.stderr.text(), /browser warning/);
  const asJson = io({
    spawn() {
      return childWith({ stderr: `noise\n${RESULT_TAG}${JSON.stringify({ ok: true, published: true, exitCode: 0, url })}\n` });
    },
  });
  assert.equal(await runCli("post", [...postArgs, "--yes", "--json"], asJson), 0);
  assert.match(asJson.stdout.text(), /"url"/);
  assert.match(asJson.stderr.text(), /noise/);
});

test("spawn failures and untagged output", async () => {
  const plain = io({ spawn() { return childWith({ stdout: "hello from ego", code: 0 }); } });
  assert.equal(await runCli("cleanup", [], plain), 0);
  assert.match(plain.stdout.text(), /hello from ego/);
  const noNl = io({ spawn() { return childWith({ stdout: "hello", code: 0 }); } });
  assert.match((await runCli("cleanup", [], noNl), noNl.stdout.text()), /hello\n/);
  const reported = io({ spawn() { return childWith({ stderr: "nodejs process exited with code 2", code: 0 }); } });
  assert.equal(await runCli("check", [], reported), 2);
  const raw = io({ spawn() { return childWith({ code: 7 }); } });
  assert.equal(await runCli("check", [], raw), 7);
  const closed = io({ spawn() { return childWith({ code: null }); } });
  assert.equal(await runCli("check", [], closed), 1);
  const crashed = io({ spawn() { return childWith({ error: new Error("spawn ego-browser ENOENT") }); } });
  assert.equal(await runCli("check", [], crashed), 1);
  assert.match(crashed.stderr.text(), /ENOENT/);
  const badTag = io({ spawn() { return childWith({ stdout: `${RESULT_TAG}{`, code: 4 }); } });
  assert.equal(await runCli("check", [], badTag), 4);
  const wrote = io({
    fs: { writeFile: async () => { throw new Error("disk full"); } },
    spawn() { throw new Error("should not spawn"); },
  });
  assert.equal(await runCli("post", [...postArgs, "--yes"], wrote), 1);
  assert.match(wrote.stderr.text(), /disk full/);
  const noRm = io({
    fs: { writeFile: async () => {} },
    spawn() { return childWith({ stdout: `${RESULT_TAG}${JSON.stringify({ exitCode: 0 })}\n` }); },
  });
  assert.equal(await runCli("cleanup", ["--task-name", "xiaohongshu-ego"], noRm), 0);
  const present = io({
    whichEgo: undefined,
    spawnSync: () => ({ status: 0 }),
    spawn() { return childWith({ stdout: `${RESULT_TAG}${JSON.stringify({ exitCode: 0, ok: true, logged_in: true })}\n` }); },
  });
  assert.equal(await runCli("check", ["--expect-account", "听懂AI"], present), 0);
  const absent = io({
    whichEgo: undefined,
    spawnSync: () => ({ error: new Error("no bin") }),
    spawn() { throw new Error("nope"); },
  });
  assert.equal(await runCli("check", [], absent), 2);
});
