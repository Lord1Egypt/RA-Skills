import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { applyCover, executeCleanup, executeEdit, executePost, performEdit, performPublish } from "../lib/publish-flow.mjs";
import { CREATOR_HOME, PUBLISH_URL } from "../lib/pure.mjs";

const NOTE = "6aeae281000000000e00cb56";
const VIDEO = "/absolute/path/to/video.mp4";
const COVER = "/absolute/path/to/cover-3x4.png";

function files() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "xhs-flow-"));
  const video = path.join(dir, "clip.mp4");
  const cover = path.join(dir, "cover-3x4.png");
  fs.writeFileSync(video, "mp4");
  fs.writeFileSync(cover, "png");
  return { dir, video, cover };
}

function loggedIn(nickname = "听懂AI") {
  return {
    url: CREATOR_HOME,
    title: "创作服务平台",
    text: "发布笔记 重新上传 设置封面",
    nickname,
    creatorChrome: true,
    loginWall: false,
  };
}

function session(state = {}) {
  const calls = [];
  const current = {
    detect: loggedIn(),
    coverOk: { signature: "custom-cover", scope: "main" },
    cover: { signature: "first-frame", scope: "main" },
    coverFails: 0,
    note: { ok: true, noteId: NOTE, url: `https://www.xiaohongshu.com/explore/${NOTE}` },
    probe: { text: "编辑 封面 0/3", url: `https://creator.xiaohongshu.com/publish/update?id=${NOTE}&noteType=video` },
    ...state,
  };
  const api = {
    calls,
    spaceId: 80,
    async goto(url) { calls.push(["goto", url]); if (current.gotoError) throw new Error(current.gotoError); },
    async detect() { calls.push(["detect"]); return current.detect; },
    async mainCoverState() {
      calls.push(["mainCoverState"]);
      return current.cover;
    },
    async setMainCover(file) { calls.push(["setMainCover", file]); if (current.coverThrow) throw new Error(current.coverThrow); },
    async waitMainCover(before) {
      calls.push(["waitMainCover", before && before.signature]);
      if (current.coverFails > 0) {
        current.coverFails -= 1;
        throw new Error("not yet");
      }
      if (current.badCover) return { state: current.cover };
      if (current.directState) return current.directState;
      return { state: current.coverOk };
    },
    async setVideo(file) { calls.push(["setVideo", file]); },
    async waitUpload() { calls.push(["waitUpload"]); if (current.uploadError) throw new Error(current.uploadError); },
    async fillTitle(value) { calls.push(["fillTitle", value]); if (current.fillError) throw new Error(current.fillError); },
    async fillBody() { calls.push(["fillBody"]); },
    async clickPublish() { calls.push(["clickPublish"]); if (current.clickError) throw new Error(current.clickError); },
    async waitSuccess() { calls.push(["waitSuccess"]); if (current.successError) throw new Error(current.successError); return { url: "https://creator.xiaohongshu.com/publish/success" }; },
    async readNote() { calls.push(["readNote"]); return current.note; },
    async probe() { calls.push(["probe"]); if (current.probeError) throw new Error(current.probeError); return current.probe; },
    async waitEditSettled() { calls.push(["waitEdit"]); if (current.editError) throw new Error(current.editError); return { ok: true }; },
    async handOff() { calls.push(["handOff"]); },
    async finish() { calls.push(["finish"]); if (current.finishError) throw new Error(current.finishError); },
  };
  return { api, current, calls };
}

function browserFor(api, opens = []) {
  return {
    async open(opts) {
      opens.push(opts);
      return api;
    },
  };
}

const checked = { ok: true, video: VIDEO, title: "标题", desc: "正文", topics: "#a", body: "正文\n\n#a", cover: COVER };

test("applyCover retries once and then refuses", async () => {
  const first = session({ coverFails: 1 });
  const ok = await applyCover(first.api, COVER);
  assert.equal(ok.ok, true);
  assert.equal(ok.attempts, 2);
  assert.equal(ok.replaced_first_frame, true);
  const stuck = session({ coverFails: 2 });
  const failed = await applyCover(stuck.api, COVER);
  assert.equal(failed.ok, false);
  assert.match(failed.error, /first frame/);
  assert.match(failed.error, /编辑封面/);
  const soft = session({ badCover: true, cover: { signature: "first-frame", scope: "main" } });
  const unchanged = await applyCover(soft.api, COVER);
  assert.equal(unchanged.ok, false);
  const direct = session({ directState: { signature: "custom-cover", scope: "main" } });
  const plain = await applyCover(direct.api, COVER);
  assert.equal(plain.ok, true);
  assert.equal(plain.cover_scope, "main");
});

test("dry-run lists the cover and does not upload", async () => {
  const { dir, video, cover } = files();
  const live = session();
  const opens = [];
  const summary = await executePost({
    video, title: "标题", desc: "正文", topics: "#a #b", cover, expectAccount: "听懂AI",
  }, { browser: browserFor(live.api, opens) });
  assert.equal(summary.exitCode, 3);
  assert.equal(summary.uploaded, false);
  assert.equal(summary.plan.cover, cover);
  assert.equal(summary.plan.cover_mode, "main-cover");
  assert.equal(summary.plan.cover_selector, "编辑封面");
  assert.equal(opens[0].startUrl, CREATOR_HOME);
  assert.equal(live.calls.some((call) => call[0] === "setVideo"), false);
  assert.equal(live.calls.some((call) => call[0] === "setMainCover"), false);
  assert.equal(live.calls.at(-1)[0], "finish");
  const omitted = await executePost({
    video, title: "标题", desc: "正文",
  }, { browser: browserFor(session().api) });
  assert.equal(omitted.plan.cover, null);
  assert.match(omitted.plan.cover_note, /first frame/);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("links fail before upload, and --strip-links rewrites the copy", async () => {
  const { dir, video, cover } = files();
  let opened = 0;
  const blocked = await executePost({
    yes: true, video, title: "标题", desc: "项目地址：https://github.com/octo/hello", cover,
  }, { browser: { async open() { opened += 1; } } });
  assert.equal(blocked.exitCode, 4);
  assert.equal(opened, 0);
  assert.match(blocked.error, /github.com\/octo\/hello/);
  assert.equal(blocked.uploaded, false);
  const live = session();
  const summary = await executePost({
    video, title: "标题", desc: "正文\n链接：x.com/someone", topics: "#话题", cover, stripLinks: true,
  }, { browser: browserFor(live.api) });
  assert.equal(summary.exitCode, 3);
  assert.equal(summary.plan.desc, "正文");
  assert.equal(summary.links_removed[0].fragment, "x.com/someone");
  assert.equal(live.calls.some((call) => call[0] === "setVideo"), false);
  const published = session();
  const sent = await executePost({
    yes: true, video, title: "标题", desc: "正文 github.com/octo/hello", cover, stripLinks: true,
  }, { browser: browserFor(published.api) });
  assert.equal(sent.exitCode, 0);
  assert.equal(sent.clicked_publish, true);
  assert.deepEqual(published.calls.find((call) => call[0] === "fillTitle"), ["fillTitle", "标题"]);
  assert.equal(published.calls.some((call) => call[0] === "setMainCover"), true);
  const dry = await executePost({
    video, title: "标题", desc: "见 www.example.com/docs", stripLinks: false,
  }, { browser: { async open() { opened += 1; } } });
  assert.equal(dry.exitCode, 4);
  assert.equal(opened, 0);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("missing cover fails before a browser opens", async () => {
  const { dir, video } = files();
  let opened = 0;
  const summary = await executePost({
    video, title: "标题", desc: "正文", cover: path.join(dir, "missing-cover.png"),
  }, { browser: { async open() { opened += 1; } } });
  assert.equal(summary.exitCode, 1);
  assert.match(summary.error, /--cover not found/);
  assert.match(summary.plan.cover, /missing-cover/);
  assert.equal(opened, 0);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("--yes replaces the first frame before 发布", async () => {
  const live = session();
  const summary = await performPublish({ yes: true, expectAccount: "听懂AI", keep: false }, live.api, checked);
  assert.equal(summary.exitCode, 0);
  assert.equal(summary.published, true);
  assert.equal(summary.cover_confirmed, true);
  assert.equal(summary.replaced_first_frame, true);
  assert.equal(summary.clicked_publish, true);
  assert.equal(summary.url, `https://www.xiaohongshu.com/explore/${NOTE}`);
  const names = live.calls.map((call) => call[0]);
  const videoAt = names.indexOf("setVideo");
  const coverAt = names.indexOf("setMainCover");
  const clickAt = names.indexOf("clickPublish");
  assert.ok(videoAt < coverAt && coverAt < clickAt);
  assert.equal(live.calls.find((call) => call[0] === "setMainCover")[1], COVER);
  assert.equal(live.calls.find((call) => call[0] === "goto")[1], PUBLISH_URL);
});

test("missing 编辑封面 fails before 发布 and does not use PK", async () => {
  const missing = session({ coverThrow: "封面编辑器（编辑封面）没有打开" });
  const summary = await performPublish({ yes: true }, missing.api, checked);
  assert.equal(summary.exitCode, 1);
  assert.match(summary.error, /编辑封面/);
  assert.equal(summary.clicked_publish, false);
  assert.equal(missing.calls.some((call) => call[0] === "clickPublish"), false);
  const live = session();
  const ok = await performPublish({ yes: true }, live.api, checked);
  assert.equal(ok.cover_scope, "main");
  assert.equal(ok.cover_via, "编辑封面");
  assert.equal(live.calls.some((call) => call[0] === "clearAutoCovers"), false);
});

test("unconfirmed cover never clicks 发布", async () => {
  const live = session({ coverFails: 2 });
  const summary = await performPublish({ yes: true }, live.api, checked);
  assert.equal(summary.exitCode, 1);
  assert.equal(summary.published, false);
  assert.equal(summary.clicked_publish, false);
  assert.equal(summary.cover_confirmed, false);
  assert.match(summary.error, /first frame/);
  assert.equal(live.calls.filter((call) => call[0] === "setMainCover").length, 2);
  assert.equal(live.calls.some((call) => call[0] === "clickPublish"), false);
  const noCover = session();
  const plain = await performPublish({ yes: true }, noCover.api, { ...checked, cover: "" });
  assert.equal(plain.exitCode, 0);
  assert.equal(noCover.calls.some((call) => call[0] === "setMainCover"), false);
  assert.equal(noCover.calls.some((call) => call[0] === "clickPublish"), true);
});

test("publish stops for login, account, and later step errors", async () => {
  const wall = session({ detect: { url: "https://creator.xiaohongshu.com/login", text: "扫码登录", loginWall: true } });
  const loggedOut = await performPublish({ yes: true, keep: true }, wall.api, checked);
  assert.equal(loggedOut.exitCode, 2);
  assert.equal(wall.calls.some((call) => call[0] === "handOff"), true);
  assert.equal(wall.calls.some((call) => call[0] === "setVideo"), false);
  const quiet = session({ detect: { url: "https://creator.xiaohongshu.com/login", text: "扫码登录", loginWall: true } });
  await performPublish({ yes: true }, quiet.api, checked);
  assert.equal(quiet.calls.some((call) => call[0] === "handOff"), false);
  const brokenHand = session({ detect: { url: "https://creator.xiaohongshu.com/login", text: "扫码登录", loginWall: true } });
  brokenHand.api.handOff = async () => { throw new Error("no handoff"); };
  assert.equal((await performPublish({ yes: true, keep: true }, brokenHand.api, checked)).exitCode, 2);
  const wrong = session({ detect: loggedIn("油管精选") });
  const mismatch = await performPublish({ yes: true, expectAccount: "听懂AI" }, wrong.api, checked);
  assert.equal(mismatch.account_mismatch, true);
  assert.equal(wrong.calls.some((call) => call[0] === "setVideo"), false);
  const late = session();
  let detects = 0;
  late.api.detect = async () => {
    detects += 1;
    late.calls.push(["detect"]);
    return detects < 2 ? loggedIn() : loggedIn("油管精选");
  };
  const second = await performPublish({ yes: true, expectAccount: "听懂AI" }, late.api, checked);
  assert.equal(second.exitCode, 2);
  assert.equal(late.calls.some((call) => call[0] === "clickPublish"), false);
  assert.equal(late.calls.some((call) => call[0] === "setMainCover"), true);
  const upload = session({ uploadError: "stalled" });
  assert.match((await performPublish({ yes: true }, upload.api, checked)).error, /stalled/);
  const fill = session({ fillError: "title" });
  assert.match((await performPublish({ yes: true }, fill.api, checked)).error, /title/);
  assert.equal(fill.calls.some((call) => call[0] === "clickPublish"), false);
  const click = session({ clickError: "blocked" });
  assert.match((await performPublish({ yes: true }, click.api, checked)).error, /blocked/);
  const success = session({ successError: "no success" });
  assert.match((await performPublish({ yes: true }, success.api, checked)).error, /no success/);
  const lost = session({ note: { ok: false, error: "note card matching title not found" } });
  const missing = await performPublish({ yes: true }, lost.api, checked);
  assert.equal(missing.published, true);
  assert.equal(missing.exitCode, 1);
  assert.match(missing.error, /do not retry/);
  const boom = session();
  boom.api.readNote = async () => { throw new Error("cards down"); };
  assert.match((await performPublish({ yes: true }, boom.api, checked)).error, /cards down/);
  const nav = session({ gotoError: "navigate" });
  assert.match((await performPublish({ yes: true }, nav.api, checked)).error, /navigate/);
  const blank = session({ detect: { url: CREATOR_HOME, text: "", evaluateError: "blank" } });
  assert.equal((await performPublish({ yes: true }, blank.api, checked)).exitCode, 1);
  const lateBlank = session();
  let seen = 0;
  lateBlank.api.detect = async () => {
    seen += 1;
    lateBlank.calls.push(["detect"]);
    return seen < 2 ? loggedIn() : { url: CREATOR_HOME, text: "", evaluateError: "blank later" };
  };
  assert.match((await performPublish({ yes: true }, lateBlank.api, checked)).error, /blank later/);
  assert.equal(lateBlank.calls.some((call) => call[0] === "clickPublish"), false);
});

test("executePost closes the space and records finish errors", async () => {
  const { dir, video, cover } = files();
  const live = session({ finishError: "finish broke" });
  const summary = await executePost({
    yes: true, video, title: "标题", desc: "正文", cover, taskName: "xiaohongshu-ego-box", keep: true,
  }, { browser: browserFor(live.api) });
  assert.equal(summary.exitCode, 0);
  assert.match(summary.finish_error, /finish broke/);
  assert.equal(live.calls.at(-1)[0], "finish");
  const thrown = await executePost({ yes: true, video, title: "标题", desc: "正文" }, {
    browser: { async open() { throw new Error("no browser"); } },
  });
  assert.match(thrown.error, /no browser/);
  const required = await executePost({ video, title: "标题", desc: "正文" }, {});
  assert.match(required.error, /browser is required/);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("dry-run login failure still lists the cover", async () => {
  const { dir, video, cover } = files();
  const wall = session({ detect: { url: "https://creator.xiaohongshu.com/login", text: "扫码登录", loginWall: true } });
  const summary = await executePost({
    video, title: "标题", desc: "正文", cover, keep: true,
  }, { browser: browserFor(wall.api) });
  assert.equal(summary.exitCode, 2);
  assert.equal(summary.plan.cover, cover);
  assert.equal(wall.calls.some((call) => call[0] === "setMainCover"), false);
  assert.equal(wall.calls.some((call) => call[0] === "handOff"), true);
  const wrong = session({ detect: loggedIn("油管精选") });
  const mismatch = await executePost({
    video, title: "标题", desc: "正文", cover, expectAccount: "听懂AI",
  }, { browser: browserFor(wrong.api) });
  assert.equal(mismatch.exitCode, 2);
  assert.equal(mismatch.plan.cover, cover);
  const blank = session({ detect: { url: CREATOR_HOME, text: "", evaluateError: "blank" } });
  const errored = await executePost({
    video, title: "标题", desc: "正文", cover,
  }, { browser: browserFor(blank.api) });
  assert.equal(errored.exitCode, 1);
  assert.equal(errored.plan.cover, cover);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("edit-cover confirms the same PK input and will not publish a failed cover", async () => {
  const { dir, cover } = files();
  const live = session();
  const opens = [];
  const summary = await executeEdit({
    yes: true, noteId: NOTE, cover, expectAccount: "听懂AI",
  }, { browser: browserFor(live.api, opens) });
  assert.equal(summary.exitCode, 0);
  assert.equal(summary.best_effort, true);
  assert.equal(summary.cover_confirmed, true);
  assert.equal(summary.url, `https://www.xiaohongshu.com/explore/${NOTE}`);
  assert.match(summary.warning, /审核中/);
  assert.equal(live.calls.some((call) => call[0] === "setVideo"), false);
  assert.equal(live.calls.filter((call) => call[0] === "setMainCover").length, 1);
  const names = live.calls.map((call) => call[0]);
  assert.ok(names.indexOf("setMainCover") < names.indexOf("clickPublish"));
  assert.match(opens[0].startUrl, /publish\/update/);
  const failed = session({ coverFails: 2 });
  const blocked = await performEdit({ yes: true, expectAccount: "听懂AI", noteId: NOTE }, failed.api, {
    noteId: NOTE, cover,
  });
  assert.equal(blocked.clicked_publish, false);
  assert.match(blocked.error, /first frame/);
  const dry = session();
  const plan = await executeEdit({ noteId: NOTE, cover }, { browser: browserFor(dry.api) });
  assert.equal(plan.exitCode, 3);
  assert.equal(plan.plan.cover, cover);
  assert.equal(plan.plan.note_id, NOTE);
  assert.equal(dry.calls.some((call) => call[0] === "setMainCover"), false);
  const missing = await executeEdit({ noteId: NOTE, cover: path.join(dir, "nope.png") }, {
    browser: { async open() { throw new Error("should not open"); } },
  });
  assert.match(missing.error, /--cover not found/);
  const finishing = session({ finishError: "edit finish" });
  const finished = await executeEdit({
    yes: true, noteId: NOTE, cover,
  }, { browser: browserFor(finishing.api) });
  assert.equal(finished.exitCode, 0);
  assert.match(finished.finish_error, /edit finish/);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("edit-cover treats 加载失败 and login problems as best-effort stops", async () => {
  const loaded = session({ probe: { text: "加载失败", url: "https://creator.xiaohongshu.com/publish/update" } });
  const failed = await performEdit({ yes: true, noteId: NOTE }, loaded.api, { noteId: NOTE, cover: COVER });
  assert.match(failed.error, /加载失败/);
  assert.equal(failed.clicked_publish, false);
  assert.equal(loaded.calls.some((call) => call[0] === "setMainCover"), false);
  const wall = session({ detect: { url: "https://creator.xiaohongshu.com/login", text: "扫码登录", loginWall: true } });
  const loggedOut = await performEdit({ yes: true, noteId: NOTE, keep: true }, wall.api, { noteId: NOTE, cover: COVER });
  assert.equal(loggedOut.exitCode, 2);
  assert.equal(wall.calls.some((call) => call[0] === "setMainCover"), false);
  const wrong = session({ detect: loggedIn("油管精选") });
  const mismatch = await performEdit({ yes: true, noteId: NOTE, expectAccount: "听懂AI" }, wrong.api, { noteId: NOTE, cover: COVER });
  assert.equal(mismatch.account_mismatch, true);
  let detects = 0;
  const late = session();
  late.api.detect = async () => {
    detects += 1;
    late.calls.push(["detect"]);
    return detects < 2 ? loggedIn() : loggedIn("油管精选");
  };
  const second = await performEdit({ yes: true, noteId: NOTE, expectAccount: "听懂AI" }, late.api, { noteId: NOTE, cover: COVER });
  assert.equal(second.exitCode, 2);
  assert.equal(late.calls.some((call) => call[0] === "clickPublish"), false);
  const click = session({ clickError: "no" });
  assert.match((await performEdit({ yes: true, noteId: NOTE }, click.api, { noteId: NOTE, cover: COVER })).error, /no/);
  const settle = session({ editError: "still editing" });
  assert.match((await performEdit({ yes: true, noteId: NOTE }, settle.api, { noteId: NOTE, cover: COVER })).error, /still editing/);
  const nav = session({ gotoError: "down" });
  assert.match((await performEdit({ yes: true, noteId: NOTE }, nav.api, { noteId: NOTE, cover: COVER })).error, /down/);
  const probe = session({ probeError: "probe" });
  assert.match((await performEdit({ yes: true, noteId: NOTE }, probe.api, { noteId: NOTE, cover: COVER })).error, /probe/);
  const blank = session({ detect: { url: CREATOR_HOME, text: "", evaluateError: "blank" } });
  assert.equal((await performEdit({ yes: true, noteId: NOTE }, blank.api, { noteId: NOTE, cover: COVER })).exitCode, 1);
  const required = await executeEdit({ noteId: "bad", cover: COVER }, {});
  assert.match(required.error, /note-id/);
  const thrown = await executeEdit({ noteId: NOTE, cover: COVER, yes: true }, {
    existsSync: () => true,
    statSync: () => ({ size: 4, isFile: () => true }),
    browser: { async open() { throw new Error("closed"); } },
  });
  assert.match(thrown.error, /closed/);
});

test("cleanup closes prefix spaces and records partial failure", async () => {
  const opened = [];
  const summary = await executeCleanup({}, {
    browser: {
      async listSpaces() { return ["xiaohongshu-ego", { name: "other" }, { taskName: "xiaohongshu-ego-edit" }]; },
      async open(opts) {
        opened.push(opts.taskName);
        return { spaceId: opened.length, async cleanup() {} };
      },
    },
  });
  assert.equal(summary.ok, true);
  assert.deepEqual(summary.kept, []);
  assert.deepEqual(opened, ["xiaohongshu-ego", "xiaohongshu-ego-edit"]);
  const fallback = await executeCleanup({}, {
    browser: {
      async listSpaces() { throw new Error("no list"); },
      async open() { return { spaceId: 1, async finish() {} }; },
    },
  });
  assert.equal(fallback.closed.length, 3);
  const partial = await executeCleanup({ taskName: "xiaohongshu-ego-box" }, {
    browser: {
      async open() { throw new Error("missing space"); },
    },
  });
  assert.equal(partial.exitCode, 1);
  assert.match(partial.error, /missing space/);
  const none = await executeCleanup({}, {});
  assert.match(none.error, /browser is required/);
});
