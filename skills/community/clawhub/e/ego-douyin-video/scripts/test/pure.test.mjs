import assert from "node:assert/strict";
import test from "node:test";
import {
  HOW_TO_LOGIN,
  LOGIN_TIP,
  MANAGE_URL,
  TITLE_LIMIT,
  UPLOAD_URL,
  classifyLogin,
  clickPoint,
  codePointLength,
  descWriteOk,
  egoMissingSummary,
  flowErrorBody,
  isPublishFormUrl,
  isPublishOwnText,
  isUploadVideoLabel,
  isUserControlInterrupt,
  loginRequiredBody,
  needsRepaint,
  parseCheckArgs,
  parsePublishArgs,
  publishSuccessBody,
  resolveEgoExit,
  resumeAfterInterrupt,
  strip,
  titleWriteOk,
  validatePublishInput,
  verifyPublished,
} from "../lib/pure.mjs";

const chars = (count) => "字".repeat(count);

test("classifyLogin treats the QR wall as logged out and upload chrome as logged in", () => {
  const wall = classifyLogin({
    url: UPLOAD_URL,
    title: "抖音创作者中心",
    text: "扫码登录",
  });
  assert.equal(wall.logged_in, false);
  assert.equal(wall.login_required, true);
  assert.equal(wall.on_login_page, true);
  assert.equal(wall.has_qr_hint, true);

  const ready = classifyLogin({
    url: UPLOAD_URL,
    title: "登录",
    text: "点击上传\n上传视频",
  });
  assert.equal(ready.logged_in, true);
  assert.equal(ready.login_required, false);
  assert.equal(ready.title, "登录");
});

test("a product name in the title is not creator chrome, and 请登录 wins over upload text", () => {
  const titled = classifyLogin({
    url: UPLOAD_URL,
    title: "抖音创作者中心",
    text: "",
  });
  assert.equal(titled.logged_in, false);
  assert.equal(titled.on_login_page, false);

  const both = classifyLogin({
    url: UPLOAD_URL,
    text: "请登录\n上传视频",
  });
  assert.equal(both.logged_in, false);
  assert.equal(both.login_wall, true);
});

test("login URL, passport host, and explicit signals", () => {
  const loginUrl = classifyLogin({ url: "https://creator.douyin.com/login?from=upload", text: "" });
  assert.equal(loginUrl.logged_in, false);
  assert.equal(loginUrl.on_login_page, true);

  const passport = classifyLogin({ url: "https://sso.douyin.com/login", text: "欢迎" });
  assert.equal(passport.on_login_page, true);

  const signaled = classifyLogin({
    url: UPLOAD_URL,
    text: "",
    signals: { uploadChrome: true },
  });
  assert.equal(signaled.logged_in, true);

  const forcedWall = classifyLogin({
    text: "上传视频",
    signals: { onLoginWall: true, platformChrome: true },
  });
  assert.equal(forcedWall.logged_in, false);

  const empty = classifyLogin();
  assert.equal(empty.logged_in, false);
  assert.equal(empty.url, undefined);
});

test("needsRepaint reloads a blank creator page and skips a real wall or session", () => {
  assert.equal(needsRepaint({ url: UPLOAD_URL, text: "", title: "抖音" }), true);
  assert.equal(needsRepaint({ onLoginWall: true, text: "" }), false);
  assert.equal(needsRepaint({ platformChrome: true }), false);
  assert.equal(needsRepaint({ uploadChrome: true, text: "" }), false);
  assert.equal(needsRepaint({ url: "https://creator.douyin.com/login", text: "" }), false);
});

test("parseCheckArgs and publish args", () => {
  assert.equal(parseCheckArgs(["--help"]).help, true);
  assert.equal(parseCheckArgs(["-h"]).help, true);
  const kept = parseCheckArgs(["--keep", "--task-name"]);
  assert.equal(kept.keep, true);
  assert.equal(kept.taskName, "douyin-login-check");
  assert.equal(parseCheckArgs(["--task-name", "douyin-1"]).taskName, "douyin-1");
  assert.throws(() => parseCheckArgs(["--nope"]), /Unknown arg/);

  const parsed = parsePublishArgs(["clip.mp4", "标题", "简介 #话题", "6", "1"]);
  assert.equal(parsed.spaceId, 6);
  assert.equal(parsed.keep, true);
  assert.equal(parsed.title, "标题");
  const defaults = parsePublishArgs(["clip.mp4", "标题", "简介", "", "0"]);
  assert.equal(defaults.spaceId, null);
  assert.equal(defaults.keep, false);
  assert.equal(parsePublishArgs(["clip.mp4", "标题", "简介", "8", "false"]).keep, false);
  assert.equal(parsePublishArgs(["clip.mp4", "标题", "简介", "8", "true"]).keep, true);
  assert.throws(() => parsePublishArgs(["clip.mp4"]), /usage/);
  assert.throws(() => parsePublishArgs([]), /usage/);
  assert.throws(() => parsePublishArgs(["", "标题", "简介"]), /usage/);
  assert.throws(() => parsePublishArgs(["a", "b", "c", "d", "e", "f"]), /too many/);
  assert.throws(() => parsePublishArgs(["a", "b", "c", "nope"]), /spaceId/);
  assert.throws(() => parsePublishArgs(["a", "b", "c", "1", "yes"]), /keep must/);
});

test("publish input enforces the 30-code-point title and a description", () => {
  assert.equal(codePointLength("😀字"), 2);
  assert.equal(TITLE_LIMIT, 30);
  const ok = validatePublishInput({
    video: "/absolute/path/to/video.mp4",
    title: chars(30),
    desc: "简介 #话题",
    exists: true,
    sizeBytes: 2 * 1048576,
  });
  assert.equal(ok.ok, true);
  assert.equal(ok.sizeMB, 2);
  assert.equal(ok.titleLength, 30);
  assert.match(validatePublishInput({ title: "标题", desc: "简介", exists: false }).error, /视频文件不存在/);
  assert.match(validatePublishInput({ exists: false }).error, /视频文件不存在/);
  assert.match(validatePublishInput({
    video: "/v.mp4",
    title: "   ",
    desc: "简介",
    exists: true,
  }).error, /标题不能为空/);
  assert.match(validatePublishInput({
    video: "/v.mp4",
    title: chars(31),
    desc: "简介",
    exists: true,
  }).error, /超过30字\(当前 31 字\)/);
  assert.match(validatePublishInput({
    video: "/v.mp4",
    title: "标题",
    desc: "  ",
    exists: true,
  }).error, /简介不能为空/);
});

test("labels, readback, click point, form URL, and success signals", () => {
  assert.equal(isUploadVideoLabel("上传\n视频"), true);
  assert.equal(isUploadVideoLabel("上传图片"), false);
  assert.equal(isUploadVideoLabel(""), false);
  assert.equal(isPublishOwnText("发布", "button"), true);
  assert.equal(isPublishOwnText("发布", "div"), false);
  assert.equal(isPublishOwnText("立即发布", "BUTTON"), false);
  assert.equal(titleWriteOk({ ok: true, value: "标题" }, "标题"), true);
  assert.equal(titleWriteOk({ ok: false, value: "WRONG" }, "标题"), false);
  assert.equal(titleWriteOk({ ok: false, value: null }, "标题"), false);
  assert.equal(titleWriteOk(null, "标题"), false);
  assert.equal(descWriteOk({ ok: true, text: " 简介 #话题 " }, "简介 #话题"), true);
  assert.equal(descWriteOk({ ok: false, text: "简介" }, "简介"), false);
  assert.equal(descWriteOk(null, "简介"), false);
  assert.deepEqual(clickPoint({ x: 10, y: 20, width: 8, height: 4 }), { x: 14, y: 22 });
  assert.equal(clickPoint(null), null);
  assert.equal(clickPoint({ x: 0, y: 0, width: 0, height: 1 }), null);
  assert.equal(clickPoint({ x: "1", y: 0, width: 1, height: 1 }), null);
  assert.equal(isPublishFormUrl("https://creator.douyin.com/creator-micro/content/post/video"), true);
  assert.equal(isPublishFormUrl("https://creator.douyin.com/creator-micro/content/upload"), false);
  assert.equal(verifyPublished({ url: `${MANAGE_URL}?enter_from=publish`, text: "" }).ok, true);
  assert.equal(verifyPublished({ url: UPLOAD_URL, text: "发布成功" }).successText, true);
  assert.equal(verifyPublished({ url: "", text: "还在编辑" }).ok, false);
  assert.equal(isUserControlInterrupt(new Error("ego user-control: geolocation")), true);
  assert.equal(isUserControlInterrupt("位置权限"), true);
  assert.equal(isUserControlInterrupt("NotAllowedError"), true);
  assert.equal(isUserControlInterrupt(new Error("未找到按钮")), false);
  assert.equal(isUserControlInterrupt(), false);
  assert.match(resumeAfterInterrupt(6), /spaceId 6/);
  assert.match(resumeAfterInterrupt(), /spaceId 重跑/);
  const body = publishSuccessBody({ title: "标题", spaceId: 6 });
  assert.equal(body.ok, true);
  assert.equal(body.manageUrl, MANAGE_URL);
  assert.deepEqual(strip({ a: "", b: null, c: undefined, d: 0, e: "ok" }), { d: 0, e: "ok" });
});

test("login-required and ego-missing summaries stay soft", () => {
  const required = loginRequiredBody({ spaceId: 3 });
  assert.equal(required.exitCode, 2);
  assert.equal(required.login_required, true);
  assert.equal(required.spaceId, 3);
  assert.equal(required.how_to_login.length, HOW_TO_LOGIN.length);
  assert.match(required.login_tip, /works better|Ego Lite/);
  assert.match(loginRequiredBody({ error: "custom" }).error, /custom/);

  const missing = egoMissingSummary();
  assert.equal(missing.exitCode, 2);
  assert.equal(missing.command, "check-login");
  assert.match(missing.error, /ego-browser not found/);
  assert.match(missing.how_to_login_zh[0], /Ego Lite/);
  assert.match(missing.how_to_login.join("\n"), /creator\.douyin\.com/);
  const named = egoMissingSummary("publish");
  assert.equal(named.command, "publish");
  assert.equal(flowErrorBody("boom", { spaceId: 1 }).exitCode, 1);
  assert.match(LOGIN_TIP, /public/);
});

test("resolveEgoExit prefers JSON exitCode, then ego's wrapped code", () => {
  assert.equal(resolveEgoExit({
    stdout: "noise\n{\"exitCode\":2,\"ok\":false}",
    code: 0,
  }), 2);
  assert.equal(resolveEgoExit({
    stderr: "{not json\nnodejs process exited with code 1",
    code: 0,
  }), 1);
  assert.equal(resolveEgoExit({ stdout: "ok", code: 0 }), 0);
  assert.equal(resolveEgoExit({ code: 5 }), 5);
  assert.equal(resolveEgoExit({ code: null }), 1);
  assert.equal(resolveEgoExit({ stderr: "{\"nope\":true}", code: 4 }), 4);
});
