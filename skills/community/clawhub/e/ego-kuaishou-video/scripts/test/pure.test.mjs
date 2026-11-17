import test from "node:test";
import assert from "node:assert/strict";
import {
  COMMENT_URL,
  MANAGE_URL,
  PUBLISH_URL,
  classifyLogin,
  commentComposerReady,
  commentTargetOk,
  commentTypedOk,
  descWriteOk,
  egoMissingSummary,
  extractPhotoId,
  extractSelectedVideoTitle,
  flowErrorBody,
  isPublishOwnText,
  loginRequiredBody,
  needsRepaint,
  parseCheckArgs,
  parseCommentArgs,
  parsePublishArgs,
  publishClickPoint,
  publishSuccessBody,
  resolveEgoExit,
  shortVideoUrl,
  uploadSignals,
  validateCommentInput,
  validatePublishInput,
  verifyCommentPosted,
  verifyPublished,
} from "../lib/pure.mjs";

test("classifyLogin treats the QR wall as logged out and creator chrome as logged in", () => {
  const wall = classifyLogin({
    url: PUBLISH_URL,
    title: "登录",
    text: "扫码登录",
  });
  assert.equal(wall.logged_in, false);
  assert.equal(wall.login_required, true);
  assert.equal(wall.on_login_page, true);
  assert.equal(wall.has_qr_hint, true);

  const upload = classifyLogin({ url: PUBLISH_URL, text: "上传视频\n发布作品" });
  assert.equal(upload.logged_in, true);
  assert.equal(upload.login_required, false);
  assert.equal(upload.has_qr_hint, undefined);

  const comment = classifyLogin({ url: COMMENT_URL, text: "评论管理\n发表评论" });
  assert.equal(comment.logged_in, true);
  const works = classifyLogin({ text: "作品管理" });
  assert.equal(works.logged_in, true);
});

test("a product name in the title is not creator chrome, and 请登录 wins over upload text", () => {
  const titled = classifyLogin({
    url: PUBLISH_URL,
    title: "快手创作者服务平台",
    text: "",
  });
  assert.equal(titled.logged_in, false);
  assert.equal(titled.on_login_page, false);

  const mixed = classifyLogin({ text: "请登录\n上传视频" });
  assert.equal(mixed.logged_in, false);
  assert.equal(mixed.login_wall, true);

  const qrCode = classifyLogin({ text: "二维码登录" });
  assert.equal(qrCode.has_qr_hint, true);
  assert.equal(qrCode.logged_in, false);
});

test("login URL, passport host, cookie, and explicit signals", () => {
  assert.equal(classifyLogin({ url: "https://cp.kuaishou.com/login?from=publish" }).logged_in, false);
  assert.equal(classifyLogin({ url: "https://cp.kuaishou.com/login" }).on_login_page, true);
  assert.equal(classifyLogin({ url: "https://passport.kuaishou.com/pc/account/login" }).logged_in, false);

  const cookie = classifyLogin({
    url: PUBLISH_URL,
    signals: { loggedInCookie: true },
  });
  assert.equal(cookie.logged_in, true);

  const cookieOnWall = classifyLogin({
    text: "扫码登录",
    signals: { loggedInCookie: true },
  });
  assert.equal(cookieOnWall.logged_in, false);

  const signaled = classifyLogin({ signals: { platformChrome: true } });
  assert.equal(signaled.logged_in, true);
  const forcedWall = classifyLogin({
    text: "上传视频",
    signals: { onLoginWall: true },
  });
  assert.equal(forcedWall.logged_in, false);

  const empty = classifyLogin({});
  assert.equal(empty.logged_in, false);
  assert.equal(empty.url, undefined);
  assert.equal(empty.title, undefined);
});

test("needsRepaint reloads a blank creator page and skips a real wall or session", () => {
  assert.equal(needsRepaint({ url: PUBLISH_URL, text: "", platformChrome: false }), true);
  assert.equal(needsRepaint({ text: "扫码登录", onLoginWall: true }), false);
  assert.equal(needsRepaint({ platformChrome: true, text: "" }), false);
  assert.equal(needsRepaint({ url: PUBLISH_URL, loggedInCookie: true }), false);
  assert.equal(needsRepaint({ url: "https://passport.kuaishou.com/pc/account/login" }), false);
});

test("parseCheckArgs, publish args, and comment args", () => {
  assert.equal(parseCheckArgs(["--keep"]).keep, true);
  assert.equal(parseCheckArgs(["--help"]).help, true);
  assert.equal(parseCheckArgs(["-h"]).help, true);
  assert.equal(parseCheckArgs(["--task-name", "ks-9"]).taskName, "ks-9");
  assert.equal(parseCheckArgs(["--task-name"]).taskName, "kuaishou-login-check");
  assert.throws(() => parseCheckArgs(["--nope"]), /Unknown arg/);

  const publish = parsePublishArgs(["/absolute/path/to/video.mp4", "描述 #话题", "4", "1"]);
  assert.equal(publish.spaceId, 4);
  assert.equal(publish.keep, true);
  assert.equal(parsePublishArgs(["/absolute/path/to/video.mp4", "描述", "", "0"]).keep, false);
  assert.equal(parsePublishArgs(["/absolute/path/to/video.mp4", "描述", "", "false"]).keep, false);
  assert.equal(parsePublishArgs(["/absolute/path/to/video.mp4", "描述"]).spaceId, null);
  assert.throws(() => parsePublishArgs(["/absolute/path/to/video.mp4"]), /usage/);
  assert.throws(() => parsePublishArgs([]), /usage/);
  assert.throws(() => parsePublishArgs(["", "描述"]), /usage/);
  assert.throws(() => parsePublishArgs(["a.mp4", "描述", "nope"]), /spaceId/);
  assert.throws(() => parsePublishArgs(["a.mp4", "描述", "4", "maybe"]), /keep/);
  assert.throws(() => parsePublishArgs(["a.mp4", "描述", "1", "1", "extra"]), /too many/);

  const comment = parseCommentArgs(["说点儿好听的", "标题", "9", "true"]);
  assert.equal(comment.spaceId, 9);
  assert.equal(comment.keep, true);
  assert.equal(comment.titleHint, "标题");
  assert.equal(parseCommentArgs(["只写评论"]).titleHint, "");
  assert.equal(parseCommentArgs(["   "]).comment, "   ");
  assert.throws(() => parseCommentArgs([]), /usage/);
  assert.throws(() => parseCommentArgs([""]), /usage/);
  assert.throws(() => parseCommentArgs(["hi", "t", "x"]), /spaceId/);
  assert.throws(() => parseCommentArgs(["hi", "t", "1", "2"]), /keep/);
  assert.throws(() => parseCommentArgs(["hi", "t", "1", "1", "z"]), /too many/);
});

test("publish input, description readback, upload signals, and the 发布 click point", () => {
  const missing = validatePublishInput({ video: "/absolute/path/to/video.mp4", desc: "hi", exists: false });
  assert.match(missing.error, /视频文件不存在/);
  assert.match(validatePublishInput({ desc: "hi" }).error, /视频文件不存在/);
  const blank = validatePublishInput({ video: "/absolute/path/to/video.mp4", desc: "  ", exists: true, sizeBytes: 10 });
  assert.match(blank.error, /描述不能为空/);
  const ok = validatePublishInput({
    video: "/absolute/path/to/video.mp4",
    desc: "描述 #话题",
    exists: true,
    sizeBytes: 1.26 * 1048576,
  });
  assert.equal(ok.ok, true);
  assert.equal(ok.sizeMB, 1.3);

  assert.equal(descWriteOk({ ok: true, text: "描述 #话题" }, " 描述 #话题 "), true);
  assert.equal(descWriteOk({ ok: true, text: "别的" }, "描述"), false);
  assert.equal(descWriteOk({ ok: false, error: "未找到描述编辑器" }, "描述"), false);
  assert.equal(descWriteOk(null, "描述"), false);

  assert.deepEqual(uploadSignals("重新上传\n上传中 40%"), { accepted: true, uploading: true });
  assert.equal(uploadSignals("重新上传\n可以发布了").uploading, false);
  assert.equal(uploadSignals("").accepted, false);

  assert.equal(isPublishOwnText("发布"), true);
  assert.equal(isPublishOwnText("立即发布"), false);
  assert.equal(isPublishOwnText("定时发布"), false);
  assert.deepEqual(publishClickPoint({ x: 10, y: 20, width: 40, height: 16 }), { x: 30, y: 28 });
  assert.equal(publishClickPoint(null), null);
  assert.equal(publishClickPoint({ x: 0, y: 0, width: 0, height: 10 }), null);
  assert.equal(publishClickPoint({ x: 0, y: 0, width: 10, height: Number.NaN }), null);
});

test("审核中 is the publish success signal", () => {
  const good = verifyPublished({
    url: "https://cp.kuaishou.com/article/manage/video?status=2&from=publish",
    text: "待发布\n审核中",
  });
  assert.equal(good.ok, true);
  assert.equal(good.status, "审核中");
  const noStatus = verifyPublished({ url: MANAGE_URL, text: "已发布" });
  assert.equal(noStatus.ok, false);
  assert.equal(noStatus.status, undefined);
  const wrongUrl = verifyPublished({ url: PUBLISH_URL, text: "审核中" });
  assert.equal(wrongUrl.ok, false);
  assert.equal(verifyPublished({}).url, undefined);

  const body = publishSuccessBody({ desc: "描述 #话题", spaceId: 4 });
  assert.equal(body.ok, true);
  assert.equal(body.status, "审核中");
  assert.equal(body.manageUrl, MANAGE_URL);
  assert.equal(body.spaceId, 4);
});

test("comment helpers: selected title, composer, send result, photo id", () => {
  const page = "\n这反应也太真实了\n2026-09-01 12:00:00\n有爱评论，说点儿好听的\n";
  assert.equal(extractSelectedVideoTitle(page), "这反应也太真实了");
  assert.equal(extractSelectedVideoTitle("没有时间戳"), "");
  assert.equal(commentComposerReady(page), true);
  assert.equal(commentComposerReady("发表评论"), true);
  assert.equal(commentComposerReady("扫码登录"), false);

  assert.equal(commentTargetOk({ videoTitle: "这反应也太真实了", titleHint: "" }).ok, true);
  assert.equal(commentTargetOk({ videoTitle: "这反应也太真实了", titleHint: "真实" }).ok, true);
  const mismatch = commentTargetOk({ videoTitle: "别的作品", titleHint: "真实" });
  assert.equal(mismatch.ok, false);
  assert.match(mismatch.error, /选择视频/);

  assert.equal(commentTypedOk("你好", "你好"), true);
  assert.equal(commentTypedOk("你好 ", "你好"), false);
  assert.equal(validateCommentInput({ comment: "  " }).ok, false);
  assert.equal(validateCommentInput({ comment: "你好" }).ok, true);

  const posted = verifyCommentPosted("发送成功\n作者\n你好", "你好");
  assert.equal(posted.ok, true);
  assert.equal(verifyCommentPosted("发送成功\n暂无评论\n你好", "你好").ok, false);
  assert.equal(verifyCommentPosted("你好", "你好").toast, false);
  assert.equal(verifyCommentPosted("发送成功", "").ok, false);

  assert.equal(extractPhotoId('<div class="video-item">3xabc1234567890</div>'), "3xabc1234567890");
  assert.equal(extractPhotoId("no id"), null);
  assert.equal(shortVideoUrl("3xabc1234567890"), "https://www.kuaishou.com/short-video/3xabc1234567890");
  assert.equal(shortVideoUrl(""), null);
});

test("login-required and ego-missing summaries stay soft", () => {
  const missing = egoMissingSummary();
  assert.equal(missing.exitCode, 2);
  assert.equal(missing.command, "check-login");
  assert.equal(missing.login_required, true);
  assert.ok(missing.how_to_login.length >= 5);
  assert.match(missing.login_tip_zh, /扫码/);
  assert.match(missing.how_to_login_zh[0], /Ego Lite/);

  const publishMiss = egoMissingSummary("publish");
  assert.equal(publishMiss.command, "publish");

  const required = loginRequiredBody({ spaceId: 3 });
  assert.equal(required.exitCode, 2);
  assert.equal(required.spaceId, 3);
  assert.equal(required.how_to_login.length, 5);
  const custom = loginRequiredBody({ error: "custom" });
  assert.equal(custom.error, "custom");

  assert.equal(flowErrorBody("未找到「发布」按钮", { spaceId: 3 }).exitCode, 1);
});

test("resolveEgoExit prefers JSON exitCode, then ego's wrapped code", () => {
  assert.equal(resolveEgoExit({
    stdout: JSON.stringify({ ok: true, status: "审核中" }),
    code: 0,
  }), 0);
  assert.equal(resolveEgoExit({
    stdout: JSON.stringify({ ok: false, exitCode: 2, login_required: true }),
    code: 0,
  }), 2);
  assert.equal(resolveEgoExit({
    stderr: "not-json {broken\nego's nodejs process exited with code 2\n",
    code: 0,
  }), 2);
  assert.equal(resolveEgoExit({ stderr: "{broken", code: 7 }), 7);
  assert.equal(resolveEgoExit({ code: null }), 1);
  assert.equal(resolveEgoExit({
    stdout: '{"exitCode":1}\n{"ok":true,"exitCode":0}\n',
    code: 1,
  }), 0);
});
