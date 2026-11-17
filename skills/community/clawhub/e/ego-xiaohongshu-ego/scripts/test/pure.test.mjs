import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  COVER_INPUT_SELECTOR,
  LINKS_EXIT,
  RESULT_TAG,
  VIDEO_INPUT_SELECTOR,
  accountGate,
  assertCoverBeforePublish,
  charCount,
  classifyLogin,
  cleanupTargets,
  composeBody,
  confirmationSummary,
  coverCount,
  coverExtensionOk,
  coverReplacedFirstFrame,
  cropDialogOpen,
  editPageFailed,
  editSettled,
  egoMissingSummary,
  exploreUrl,
  extractTaggedJson,
  findLinks,
  formatRemovedLinks,
  formatResult,
  inputErrorSummary,
  isNoteId,
  mainCoverApplied,
  needsRepaint,
  onCreator,
  parseCheckArgs,
  parseCleanupArgs,
  parseEditArgs,
  parseImpression,
  parsePostArgs,
  pickNote,
  pkToastSeen,
  planOf,
  preparePostCopy,
  publishSucceeded,
  stripLinks,
  titleUnits,
  resolveProcessExit,
  updateUrl,
  uploadReady,
  validateEditInput,
  validatePostInput,
  videoExtensionOk,
} from "../lib/pure.mjs";

const NOTE = "6aeae281000000000e00cb56";

test("selectors and body composition", () => {
  assert.equal(VIDEO_INPUT_SELECTOR, "input.upload-input");
  assert.equal(COVER_INPUT_SELECTOR, "input.pk-cover-list-file-input");
  assert.equal(composeBody("正文", "#a #b"), "正文\n\n#a #b");
  assert.equal(composeBody("", "#a"), "#a");
  assert.equal(composeBody("正文", "  "), "正文");
  assert.equal(charCount("听懂AI"), 4);
  assert.equal(titleUnits("两台Mac跑816B大模型｜听懂AI #053"), 16);
  assert.equal(titleUnits("甲".repeat(21)), 21);
  assert.equal(videoExtensionOk("/tmp/a.MP4"), true);
  assert.equal(videoExtensionOk("/tmp/a.txt"), false);
  assert.equal(coverExtensionOk("/tmp/cover-3x4.PNG"), true);
  assert.equal(coverExtensionOk("/tmp/a.gif"), false);
});

test("argument parsers", () => {
  assert.equal(parseCheckArgs(["--help"]).help, true);
  assert.equal(parseCheckArgs(["-h"]).help, true);
  assert.equal(parseCheckArgs(["--keep", "--expect-account", "听懂AI", "--task-name", "lane"]).expectAccount, "听懂AI");
  assert.equal(parseCheckArgs(["--task-name", ""]).taskName, "xiaohongshu-ego-login");
  assert.throws(() => parseCheckArgs(["--nope"]), /Unknown arg/);
  assert.throws(() => parseCheckArgs(["--expect-account"]), /Missing value/);
  assert.equal(parseCleanupArgs(["--task-name", "xiaohongshu-ego-edit"]).taskName, "xiaohongshu-ego-edit");
  assert.equal(parseCleanupArgs(["--task-name", ""]).taskName, "");
  const post = parsePostArgs([
    "--video", "/tmp/a.mp4", "--title", "标题", "--desc", "正文",
    "--topics", "#a #b", "--cover", "/tmp/cover-3x4.png", "--expect-account", "听懂AI",
    "--yes", "--json", "--keep", "--task-name", "box",
  ]);
  assert.equal(post.yes, true);
  assert.equal(post.topics, "#a #b");
  assert.equal(post.taskName, "box");
  assert.equal(parsePostArgs(["--video", "/tmp/a.mp4", "--title", "标题", "--desc", "正文", "--task-name", ""]).taskName, "xiaohongshu-ego");
  assert.throws(() => parsePostArgs(["--title", "标题", "--desc", "正文"]), /Missing --video/);
  assert.throws(() => parsePostArgs(["--video", "/tmp/a.mp4", "--desc", "正文"]), /Missing --title/);
  assert.throws(() => parsePostArgs(["--video", "/tmp/a.mp4", "--title", "标题"]), /Missing --desc/);
  assert.equal(parsePostArgs(["--help"]).help, true);
  const edit = parseEditArgs(["--note-id", NOTE, "--cover", "/tmp/cover-3x4.png", "--yes"]);
  assert.equal(edit.command, "edit-cover");
  assert.equal(edit.noteId, NOTE);
  assert.throws(() => parseEditArgs(["--cover", "/tmp/a.png"]), /Missing --note-id/);
  assert.throws(() => parseEditArgs(["--note-id", NOTE]), /Missing --cover/);
  assert.equal(parseEditArgs(["--note-id", NOTE, "--cover", "/tmp/a.png", "--task-name", ""]).taskName, "xiaohongshu-ego-edit");
});

test("file validation includes a missing cover and does not invent one", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "xhs-pure-"));
  const video = path.join(dir, "clip.mp4");
  const cover = path.join(dir, "cover-3x4.png");
  const empty = path.join(dir, "empty.png");
  fs.writeFileSync(video, "mp4");
  fs.writeFileSync(cover, "png");
  fs.writeFileSync(empty, "");
  fs.mkdirSync(path.join(dir, "dir.png"));
  const ok = validatePostInput({
    video, title: "标题", desc: "正文", topics: "#a", cover,
  }, { exists: fs.existsSync, stat: fs.statSync });
  assert.equal(ok.ok, true);
  assert.equal(ok.body, "正文\n\n#a");
  assert.match(validatePostInput({
    video, title: "这是一个明显超过二十个字符的标题用来触发提醒", desc: "正文",
  }, { exists: fs.existsSync, stat: fs.statSync }).titleWarning, /20/);
  const missing = validatePostInput({
    video, title: "标题", desc: "正文", cover: path.join(dir, "missing-cover.png"),
  }, { exists: fs.existsSync, stat: fs.statSync });
  assert.equal(missing.ok, false);
  assert.match(missing.error, /--cover not found/);
  assert.match(validatePostInput({ video: "relative.mp4", title: "标题", desc: "正文" }).error, /absolute path/);
  assert.match(validatePostInput({ video: "/tmp/a.gif", title: "标题", desc: "正文" }).error, /extension/);
  assert.match(validatePostInput({ video: "/tmp/missing.mp4", title: "标题", desc: "正文" }, {
    exists: () => false,
  }).error, /--video not found/);
  assert.match(validatePostInput({ video, title: "", desc: "正文" }, { exists: fs.existsSync, stat: fs.statSync }).error, /Missing --title/);
  assert.match(validatePostInput({ video, title: "标题", desc: "" }, { exists: fs.existsSync, stat: fs.statSync }).error, /Missing --desc/);
  assert.match(validatePostInput({ video: "", title: "标题", desc: "正文" }).error, /Missing --video/);
  assert.match(validatePostInput({
    video, title: "标题", desc: "正文", cover: "/tmp/cover.gif",
  }).error, /jpg, .jpeg, or .png/);
  assert.match(validatePostInput({
    video, title: "标题", desc: "正文", cover: "cover-3x4.png",
  }).error, /--cover must be an absolute path/);
  assert.match(validatePostInput({
    video, title: "标题", desc: "正文", cover: empty,
  }, { exists: fs.existsSync, stat: fs.statSync }).error, /empty/);
  assert.match(validatePostInput({
    video, title: "标题", desc: "正文", cover: path.join(dir, "dir.png"),
  }, { exists: fs.existsSync, stat: fs.statSync }).error, /not a file/);
  assert.match(validatePostInput({
    video: path.join(dir, "gone.mp4"), title: "标题", desc: "正文",
  }, { exists: () => true, stat: () => { throw new Error("enoent"); } }).error, /--video not found/);
  const omitted = validatePostInput({ video, title: "标题", desc: "正文" }, { exists: fs.existsSync, stat: fs.statSync });
  assert.equal(omitted.cover, "");
  assert.equal(planOf({ title: "标题", desc: "正文" }, omitted).cover, null);
  assert.equal(planOf({ title: "标题", desc: "正文" }, omitted).cover_mode, "platform-default-first-frame");
  const planned = planOf({ expectAccount: "听懂AI", cover }, ok, { nickname: "听懂AI" });
  assert.equal(planned.cover, cover);
  assert.equal(planned.cover_selector, "编辑封面");
  assert.equal(planned.cover_mode, "main-cover");
  assert.match(planned.cover_note, /编辑封面/);
  assert.match(planned.cover_note, /PK slots/);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("edit input and update url", () => {
  assert.equal(isNoteId(NOTE), true);
  assert.equal(isNoteId("nope"), false);
  assert.equal(updateUrl(NOTE), `https://creator.xiaohongshu.com/publish/update?id=${NOTE}&noteType=video`);
  assert.equal(updateUrl("bad"), "");
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "xhs-edit-"));
  const cover = path.join(dir, "cover-3x4.jpg");
  fs.writeFileSync(cover, "jpg");
  const ok = validateEditInput({ noteId: NOTE, cover }, { exists: fs.existsSync, stat: fs.statSync });
  assert.equal(ok.ok, true);
  const plan = planOf({ noteId: NOTE, command: "edit-cover", cover }, ok);
  assert.equal(plan.note_id, NOTE);
  assert.equal(plan.best_effort, true);
  assert.match(plan.cover_note, /加载失败/);
  assert.match(validateEditInput({ noteId: "bad", cover }).error, /note-id/);
  assert.match(validateEditInput({ noteId: NOTE, cover: "" }).error, /Missing --cover/);
  assert.match(validateEditInput({ noteId: NOTE, cover: "a.png" }).error, /absolute/);
  assert.match(validateEditInput({ noteId: NOTE, cover: "/tmp/a.gif" }).error, /png/);
  assert.match(validateEditInput({ noteId: NOTE, cover: path.join(dir, "missing.png") }, {
    exists: fs.existsSync, stat: fs.statSync,
  }).error, /--cover not found/);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("login, account gate, and upload ready", () => {
  assert.equal(onCreator("https://creator.xiaohongshu.com/publish/publish"), true);
  assert.equal(onCreator("https://www.xiaohongshu.com/explore/abc"), false);
  assert.equal(onCreator("not a url"), false);
  const loggedOut = classifyLogin({
    url: "https://creator.xiaohongshu.com/login",
    text: "扫码登录",
    loginWall: true,
  });
  assert.equal(loggedOut.logged_in, false);
  assert.equal(loggedOut.on_login_page, true);
  const home = classifyLogin({
    url: "https://creator.xiaohongshu.com/",
    text: "发布笔记 笔记管理",
    nickname: "听懂AI",
    creatorChrome: true,
  });
  assert.equal(home.logged_in, true);
  assert.equal(home.nickname, "听懂AI");
  assert.equal(classifyLogin({
    url: "https://www.xiaohongshu.com/",
    text: "发布笔记",
    nickname: "听懂AI",
  }).logged_in, false);
  assert.equal(accountGate({ loggedIn: true, nickname: "听懂AI", expected: "听懂AI" }).ok, true);
  assert.equal(accountGate({ loggedIn: true, nickname: "", expected: "听懂AI", text: "听懂AI" }).nickname_via, "body");
  const wrong = accountGate({ loggedIn: true, nickname: "油管精选", expected: "听懂AI", text: "听懂AI" });
  assert.equal(wrong.account_mismatch, true);
  assert.match(wrong.error, /油管精选/);
  assert.match(accountGate({ loggedIn: true, nickname: "", expected: "听懂AI", text: "首页" }).error, /not found/);
  assert.equal(accountGate({ loggedIn: false, expected: "听懂AI" }).ok, false);
  assert.equal(accountGate({ loggedIn: true, nickname: "听懂AI" }).ok, true);
  assert.equal(needsRepaint({ text: "" }), true);
  assert.equal(needsRepaint({ evaluateError: "boom", text: "" }), true);
  assert.equal(needsRepaint({ loginWall: true, text: "" }), false);
  assert.equal(needsRepaint({ creatorChrome: true }), false);
  assert.equal(needsRepaint({ nickname: "听懂AI" }), false);
  assert.equal(needsRepaint({ text: "x".repeat(41) }), false);
  assert.equal(uploadReady("上传中 12% 重新上传"), false);
  assert.equal(uploadReady("重新上传 设置封面"), true);
  assert.equal(uploadReady("首页"), false);
});

test("cover confirmation requires the toast and a counter advance", () => {
  const before = { text: "封面 0/3", coverCount: 0, pkApplied: false };
  const applied = { text: "已添加 PK 封面\n封面 1/3", pkApplied: true, coverCount: 1, counterText: "1/3" };
  assert.equal(pkToastSeen(applied), true);
  assert.equal(pkToastSeen({ text: "已添加 PK 封面" }), true);
  assert.equal(pkToastSeen(null), false);
  assert.equal(coverCount(applied), 1);
  assert.equal(coverCount({ text: "封面 0/3" }), 0);
  assert.equal(coverCount({ text: "no counter" }), null);
  assert.equal(coverCount(null), null);
  assert.equal(coverCount({ coverCount: Number.NaN, text: "1/3" }), 1);
  assert.equal(mainCoverApplied({ signature: "first-frame.jpg" }, { signature: "custom-cover.jpg", scope: "main" }), true);
  assert.equal(mainCoverApplied({ signature: "first-frame.jpg" }, { signature: "pk-cover-list-blob", scope: "pk" }), false);
  assert.equal(mainCoverApplied({ signature: "first-frame.jpg" }, { signature: "first-frame.jpg" }), false);
  assert.equal(mainCoverApplied({ signature: "" }, { signature: "url(custom-cover.jpg)", scope: "main" }), true);
  assert.equal(mainCoverApplied(null, { signature: "url(custom-cover.jpg)", scope: "main" }), true);
  assert.equal(mainCoverApplied({ signature: "" }, { signature: "", scope: "main" }), false);
  assert.equal(coverReplacedFirstFrame(before, applied), true);
  assert.equal(coverReplacedFirstFrame(before, { pkApplied: true, coverCount: 0, text: "已添加 PK 封面 封面 0/3" }), false);
  assert.equal(coverReplacedFirstFrame(before, { pkApplied: false, coverCount: 1, text: "封面 1/3" }), false);
  assert.equal(coverReplacedFirstFrame({ previewSignature: "first" }, { previewSignature: "other", text: "封面预览" }), false);
  assert.equal(coverReplacedFirstFrame(before, { ...applied, cropDialog: true }), false);
  assert.equal(cropDialogOpen({ text: "裁剪封面" }), true);
  assert.equal(cropDialogOpen({ cropDialog: true }), true);
  assert.equal(cropDialogOpen(null), false);
  assert.equal(coverReplacedFirstFrame(null, null), false);
  assert.equal(coverReplacedFirstFrame({}, { pkApplied: true, text: "已添加 PK 封面 1/3" }), true);
  const guard = assertCoverBeforePublish({ cover: "/tmp/cover-3x4.png", coverConfirmed: false });
  assert.equal(guard.ok, false);
  assert.match(guard.error, /编辑封面/);
  assert.match(guard.error, /first frame/);
  assert.equal(assertCoverBeforePublish({ cover: "", coverConfirmed: false }).ok, true);
  assert.equal(assertCoverBeforePublish({ cover: "/tmp/a.png", coverConfirmed: true }).ok, true);
});

test("notes cannot contain links", () => {
  assert.deepEqual(findLinks("普通正文 封面 cover-3x4.png 第1.2节"), []);
  assert.deepEqual(findLinks("写信 hi@github.com"), []);
  const samples = [
    "看 https://github.com/octo/hello",
    "看 http://example.com/a",
    "看 www.example.com/docs",
    "仓库 github.com/octo/hello",
    "主页 x.com/someone",
    "短链 t.co/abc",
    "短链 t.co",
  ];
  for (const sample of samples) assert.ok(findLinks(sample).length >= 1, sample);
  const stripped = stripLinks("正文\n\n项目地址：https://github.com/octo/hello\n\n链接： x.com/someone\n下一句");
  assert.deepEqual(stripped.removed, ["https://github.com/octo/hello", "x.com/someone"]);
  assert.equal(stripped.text, "正文\n\n下一句");
  assert.equal(stripLinks("看这里 链接：www.example.com/a 完").text, "看这里 完");
  assert.equal(stripLinks("重复 https://t.co/aa 和 https://t.co/aa").removed.length, 2);
  const blocked = preparePostCopy({
    title: "标题 x.com/a",
    desc: "正文 https://github.com/octo/hello",
    topics: "#a t.co/zz",
  });
  assert.equal(blocked.ok, false);
  assert.equal(blocked.exitCode, LINKS_EXIT);
  assert.deepEqual(blocked.links.map((item) => item.field), ["title", "desc", "topics"]);
  const cleaned = preparePostCopy({
    title: "标题",
    desc: "正文\n项目地址：github.com/octo/hello",
    topics: "#话题",
    stripLinks: true,
  });
  assert.equal(cleaned.ok, true);
  assert.equal(cleaned.desc, "正文");
  assert.equal(cleaned.links_removed[0].fragment, "github.com/octo/hello");
  assert.match(preparePostCopy({ title: "https://x.com/a", desc: "正文", stripLinks: true }).error, /title is empty/);
  assert.match(preparePostCopy({ title: "标题", desc: "https://x.com/a", stripLinks: true }).error, /desc is empty/);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "xhs-links-"));
  const video = path.join(dir, "clip.mp4");
  fs.writeFileSync(video, "mp4");
  const rejected = validatePostInput({
    video, title: "标题", desc: "见 github.com/octo/hello", topics: "#a",
  }, { exists: fs.existsSync, stat: fs.statSync });
  assert.equal(rejected.ok, false);
  assert.equal(rejected.exitCode, LINKS_EXIT);
  assert.match(rejected.error, /github.com\/octo\/hello/);
  const summary = inputErrorSummary({ title: "标题", desc: rejected.desc }, rejected);
  assert.equal(summary.exitCode, LINKS_EXIT);
  assert.equal(summary.links[0].fragment, "github.com/octo/hello");
  assert.equal(summary.plan.links[0].field, "desc");
  const allowed = validatePostInput({
    video, title: "标题", desc: "正文\n链接：https://x.com/a", topics: "www.example.com/b", stripLinks: true,
  }, { exists: fs.existsSync, stat: fs.statSync });
  assert.equal(allowed.ok, true);
  assert.equal(allowed.desc, "正文");
  assert.equal(allowed.topics, "");
  assert.equal(allowed.body, "正文");
  assert.equal(allowed.links_removed.length, 2);
  const dry = confirmationSummary({ title: "标题", desc: "正文" }, allowed);
  assert.equal(dry.links_removed.length, 2);
  assert.equal(dry.plan.links_removed.length, 2);
  assert.match(formatRemovedLinks(allowed.links_removed), /removed links:/);
  assert.match(formatResult({
    exitCode: 0, published: true, url: exploreUrl(NOTE), links_removed: allowed.links_removed,
  }), /removed links:/);
  assert.equal(parsePostArgs(["--video", video, "--title", "标题", "--desc", "正文", "--strip-links"]).stripLinks, true);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("note id, edit settlement, and result formatting", () => {
  const impression = JSON.stringify({ noteTarget: { value: { noteId: NOTE } } });
  assert.equal(parseImpression(impression), NOTE);
  assert.equal(parseImpression({ noteTarget: { noteId: NOTE } }), NOTE);
  assert.equal(parseImpression({ noteId: NOTE }), NOTE);
  assert.equal(parseImpression("{"), "");
  assert.equal(parseImpression(null), "");
  assert.equal(parseImpression(7), "");
  assert.equal(parseImpression({ noteId: "short" }), "");
  assert.equal(exploreUrl(NOTE), `https://www.xiaohongshu.com/explore/${NOTE}`);
  assert.equal(exploreUrl("nope"), "");
  const cards = [
    { text: "别的", impression: JSON.stringify({ noteId: "aaaaaaaaaaaaaaaa" }) },
    { text: `看条广告 ${NOTE}`, impression },
  ];
  assert.equal(pickNote(cards, "看条广告").noteId, NOTE);
  assert.equal(pickNote([{ text: "看条广告", "data-impression": impression }], "看条广告").ok, true);
  assert.match(pickNote(cards, "").error, /empty/);
  assert.match(pickNote(cards, "没有").error, /not found/);
  assert.match(pickNote([{ text: "看条广告", impression: "{}" }], "看条广告").error, /noteId/);
  assert.equal(pickNote(null, "看条广告").ok, false);
  assert.equal(publishSucceeded({
    url: "https://creator.xiaohongshu.com/publish/success?ok=1",
    text: "发布成功",
  }), true);
  assert.equal(publishSucceeded({ url: "https://creator.xiaohongshu.com/", text: "发布成功" }), false);
  assert.equal(editPageFailed("加载失败"), true);
  assert.equal(editSettled({ url: "https://creator.xiaohongshu.com/publish/success", text: "发布成功" }), true);
  assert.equal(editSettled({ url: "https://creator.xiaohongshu.com/new/note-manager", text: "笔记" }), true);
  assert.equal(editSettled({ text: "封面PK中" }), true);
  assert.equal(editSettled({ text: "审核中" }), true);
  assert.equal(editSettled({ text: "加载失败 审核中" }), false);
  assert.equal(editSettled({ text: "编辑" }), false);
  const names = cleanupTargets({ listed: ["other", { name: "xiaohongshu-ego-edit" }, { taskName: "xiaohongshu-ego-login" }] });
  assert.deepEqual(names, ["xiaohongshu-ego-edit", "xiaohongshu-ego-login"]);
  assert.deepEqual(cleanupTargets({}), ["xiaohongshu-ego", "xiaohongshu-ego-login", "xiaohongshu-ego-edit"]);
  assert.deepEqual(cleanupTargets({ listed: ["nope"] }), ["xiaohongshu-ego", "xiaohongshu-ego-login", "xiaohongshu-ego-edit"]);
  assert.deepEqual(cleanupTargets({ taskName: "custom-space", listed: [{ name: "custom-space-2" }, "xiaohongshu-ego"] }), ["custom-space"]);
  const dry = confirmationSummary({ cover: "/tmp/cover-3x4.png", title: "标题", desc: "正文" }, {
    cover: "/tmp/cover-3x4.png", title: "标题", desc: "正文", body: "正文", video: "/tmp/a.mp4",
  }, { nickname: "听懂AI" });
  assert.equal(dry.exitCode, 3);
  assert.equal(dry.uploaded, false);
  assert.equal(dry.plan.cover, "/tmp/cover-3x4.png");
  const editDry = confirmationSummary({ command: "edit-cover", noteId: NOTE, cover: "/tmp/a.png" }, { noteId: NOTE, cover: "/tmp/a.png" });
  assert.match(editDry.error, /best-effort/i);
  assert.equal(inputErrorSummary({ cover: "/tmp/missing.png", command: "edit-cover" }, { error: "bad", cover: "/tmp/missing.png" }).command, "edit-cover");
  const missing = egoMissingSummary("post-video");
  assert.equal(missing.exitCode, 2);
  assert.match(missing.how_to_login_zh[0], /Ego Lite/);
  assert.equal(formatResult(null), "");
  assert.equal(formatResult({ exitCode: 0, published: true, url: exploreUrl(NOTE) }), `${exploreUrl(NOTE)}\n`);
  assert.match(formatResult(dry), /confirmation_required/);
  assert.match(formatResult({ exitCode: 0, published: true, url: exploreUrl(NOTE) }, { asJson: true }), /"url"/);
  const tagged = extractTaggedJson(`noise\n${RESULT_TAG}{\n${RESULT_TAG}${JSON.stringify({ exitCode: 3 })}`);
  assert.equal(tagged.exitCode, 3);
  assert.equal(extractTaggedJson(`${RESULT_TAG}{`), null);
  assert.equal(extractTaggedJson("plain"), null);
  assert.equal(resolveProcessExit("nodejs process exited with code 2", 0), 2);
  assert.equal(resolveProcessExit("", 0), 0);
  assert.equal(resolveProcessExit("", null), 1);
});
