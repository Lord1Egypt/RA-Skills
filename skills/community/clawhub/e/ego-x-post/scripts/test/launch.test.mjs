import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { CAPTURED_CREATE_TWEET_QUERY_ID, RESULT_TAG, SMOKE_TEXT } from "../lib/pure.mjs";
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
  mkdtemp: async () => "/tmp/ego-x-post-test",
  fs: { writeFile: async () => {}, rm: async () => {} },
  ...extra,
});

test("whichEgo maps the probe", () => {
  assert.equal(whichEgo(() => ({ error: new Error("missing") })), null);
  assert.equal(whichEgo(() => ({ status: 0 })), "ego-browser");
  assert.equal(whichEgo(() => null), "ego-browser");
  const live = whichEgo();
  assert.ok(live === null || live === "ego-browser");
});

test("renderEntry inlines the post config", () => {
  const source = renderEntry({
    config: { yes: true, text: 'say "hi"', keep: false },
    runHref: "file:///opt/post-flow.mjs",
    depsHref: "file:///opt/ego-deps.mjs",
    exportName: "executePost",
  });
  assert.match(source, /executePost/);
  assert.match(source, /ego-deps\.mjs/);
  assert.match(source, /say \\"hi\\"/);
  assert.doesNotMatch(source, /ct0/);
});

test("help and unknown args do not spawn", async () => {
  let spawned = 0;
  const help = io({ spawn() { spawned += 1; } });
  assert.equal(await runCli("post", ["--help"], help), 0);
  assert.match(help.stdout.text(), /--yes/);
  assert.equal(await runCli("check", ["-h"], io({ spawn() { spawned += 1; } })), 0);
  assert.equal(await runCli("cleanup", ["--help"], io({ spawn() { spawned += 1; } })), 0);
  const bad = io({ spawn() { spawned += 1; } });
  assert.equal(await runCli("post", ["--text", "hi", "--nope"], bad), 1);
  assert.match(bad.stderr.text(), /Unknown arg/);
  assert.equal(await runCli("check", ["--nope"], io()), 1);
  assert.equal(await runCli("nope", [], io()), 1);
  assert.equal(spawned, 0);
});

test("a missing ego-browser soft-fails before a draft can send", async () => {
  const deps = io({ whichEgo: () => null, spawn() { throw new Error("should not spawn"); } });
  const code = await runCli("post", ["--text", "hello"], deps);
  assert.equal(code, 2);
  assert.match(deps.stdout.text(), /ego-browser not found/);
  assert.match(deps.stdout.text(), /how_to_login_zh/);
  assert.match(deps.stdout.text(), /hello/);
  const check = io({ whichEgo: () => null });
  assert.equal(await runCli("check", [], check), 2);
  assert.equal(check.stdout.text().includes('"draft"'), false);
});

test("without --yes the draft is printed and ego is not spawned", async () => {
  let spawned = 0;
  const plain = io({ spawn() { spawned += 1; } });
  assert.equal(await runCli("post", ["--text", SMOKE_TEXT], plain), 3);
  assert.match(plain.stdout.text(), /draft \(not sent\)/);
  assert.match(plain.stdout.text(), /Nothing sends without --yes/);
  const reply = io({ spawn() { spawned += 1; } });
  assert.equal(await runCli("post", ["--text", "hi", "--reply-to", "5", "--json"], reply), 3);
  assert.match(reply.stdout.text(), /reply_best_effort/);
  assert.equal(spawned, 0);
});

test("the built-in probe is used when whichEgo is not injected", async () => {
  const missing = io({
    whichEgo: undefined,
    spawnSync: () => ({ error: new Error("no bin") }),
    spawn() { throw new Error("nope"); },
  });
  assert.equal(await runCli("check", [], missing), 2);
  const present = io({
    whichEgo: undefined,
    spawnSync: () => ({ status: 0 }),
    spawn() {
      return childWith({ stdout: `${RESULT_TAG}${JSON.stringify({ exitCode: 0, ok: true, logged_in: true })}\n` });
    },
  });
  assert.equal(await runCli("check", [], present), 0);
});

test("--yes prints the status URL and --json keeps the summary", async () => {
  const url = "https://x.com/Suchuanyi/status/2117826677376160218";
  let entry = "";
  const deps = io({
    fs: {
      writeFile: async (_file, source) => { entry = source; },
      rm: () => Promise.reject(new Error("rm failed")),
    },
    spawn() {
      return childWith({
        stdout: `${RESULT_TAG}${JSON.stringify({ ok: true, sent: true, exitCode: 0, url })}\n`,
        stderr: "browser warning",
      });
    },
  });
  const code = await runCli("post", ["--text", "hi", "--yes", "--keep", "--query-id", CAPTURED_CREATE_TWEET_QUERY_ID], deps);
  assert.equal(code, 0);
  assert.equal(deps.stdout.text(), `${url}\n`);
  assert.match(entry, /executePost/);
  assert.equal(entry.includes(CAPTURED_CREATE_TWEET_QUERY_ID), true);
  assert.match(deps.stderr.text(), /browser warning/);
  const asJson = io({
    spawn() {
      return childWith({ stderr: `noise\n${RESULT_TAG}${JSON.stringify({ ok: true, sent: true, exitCode: 0, url })}\n` });
    },
  });
  assert.equal(await runCli("post", ["--text", "hi", "--yes", "--json"], asJson), 0);
  assert.match(asJson.stdout.text(), /"url":/);
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
  assert.equal(await runCli("post", ["--text", "hi", "--yes"], wrote), 1);
  assert.match(wrote.stderr.text(), /disk full/);
  const noRm = io({
    fs: { writeFile: async () => {} },
    spawn() { return childWith({ stdout: `${RESULT_TAG}${JSON.stringify({ exitCode: 0 })}\n` }); },
  });
  assert.equal(await runCli("cleanup", ["--task-name", "x-post"], noRm), 0);
});

function writePng(name = "card.png", bytes = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 1])) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "x-post-cli-"));
  const file = path.join(dir, name);
  fs.writeFileSync(file, bytes);
  return file;
}

test("image files are checked before ego, and a dry-run prints size and md5", async () => {
  let probes = 0;
  const missing = io({
    whichEgo() { probes += 1; return "ego-browser"; },
    spawn() { throw new Error("should not spawn"); },
  });
  assert.equal(await runCli("post", ["--text", "hi", "--image", "/tmp/no-such-x-post.png"], missing), 1);
  assert.match(missing.stderr.text(), /Image not found/);
  assert.equal(probes, 0);

  const gif = io({
    whichEgo() { probes += 1; return "ego-browser"; },
    spawn() { throw new Error("should not spawn"); },
  });
  assert.equal(await runCli("post", ["--text", "hi", "--image", "anim.gif"], gif), 1);
  assert.match(gif.stderr.text(), /GIF is not supported/);
  assert.equal(probes, 0);

  const big = writePng("big.png");
  fs.truncateSync(big, 5 * 1024 * 1024 + 1);
  const oversized = io({ spawn() { throw new Error("should not spawn"); } });
  assert.equal(await runCli("post", ["--text", "hi", "--image", big], oversized), 1);
  assert.match(oversized.stderr.text(), /exceeds 5 MiB/);

  const file = writePng();
  let spawned = 0;
  const draft = io({ spawn() { spawned += 1; } });
  assert.equal(await runCli("post", ["--text", "hi", "--image", file], draft), 3);
  assert.match(draft.stdout.text(), /media \(not uploaded\)/);
  assert.match(draft.stdout.text(), /md5 [0-9a-f]{32}/);
  assert.match(draft.stdout.text(), new RegExp(`${file.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}`));
  assert.equal(draft.stdout.text().includes("media_id"), false);
  assert.equal(spawned, 0);

  const asJson = io({ spawn() { spawned += 1; } });
  assert.equal(await runCli("post", ["--text", "hi", "--image", file, "--json"], asJson), 3);
  assert.match(asJson.stdout.text(), /"md5":/);
  assert.equal(asJson.stdout.text().includes("media_id"), false);

  const absent = io({
    whichEgo: () => null,
    spawn() { throw new Error("should not spawn"); },
  });
  assert.equal(await runCli("post", ["--text", "hello", "--image", file], absent), 2);
  assert.match(absent.stdout.text(), /md5/);
  assert.match(absent.stdout.text(), /ego-browser not found/);
});

test("--yes passes image paths into the entry and does not inline the bytes", async () => {
  const bytes = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 7, 7, 7]);
  const first = writePng("one.png", bytes);
  const second = writePng("two.webp", Buffer.concat([
    Buffer.from("RIFF"),
    Buffer.from([0, 0, 0, 0]),
    Buffer.from("WEBP"),
  ]));
  let entry = "";
  const deps = io({
    fs: {
      writeFile: async (_file, source) => { entry = source; },
      rm: async () => {},
    },
    spawn() {
      return childWith({
        stdout: `${RESULT_TAG}${JSON.stringify({
          ok: true,
          sent: true,
          exitCode: 0,
          url: "https://x.com/Suchuanyi/status/1",
          media: [{ path: first, media_id: "2117874109082427392", bytes: bytes.length }],
          transaction_id_source: "generated",
          query_id_source: "bundle",
        })}\n`,
      });
    },
  });
  const code = await runCli("post", ["--text", "hi", "--image", first, "--image", second, "--yes", "--json"], deps);
  assert.equal(code, 0);
  assert.match(deps.stdout.text(), /"media_id": "2117874109082427392"/);
  assert.match(deps.stdout.text(), /"transaction_id_source": "generated"/);
  assert.match(deps.stdout.text(), /"query_id_source": "bundle"/);
  assert.match(entry, /"images":\[/);
  assert.match(entry, new RegExp(first.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
  assert.match(entry, new RegExp(second.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
  assert.equal(entry.includes(bytes.toString("base64")), false);
});
