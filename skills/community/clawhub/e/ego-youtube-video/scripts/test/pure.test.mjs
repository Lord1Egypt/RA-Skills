import test from "node:test";
import assert from "node:assert/strict";
import {
  STUDIO_URL,
  audienceSelector,
  classifyLogin,
  classifyProcessingStatus,
  detectSignals,
  egoMissingSummary,
  extractVideoId,
  flowErrorBody,
  isLoginWall,
  loginRequiredBody,
  metadataWriteOk,
  needsRepaint,
  parseCheckArgs,
  parseMadeForKids,
  parsePublishArgs,
  parseTags,
  parseVisibility,
  publishSuccessBody,
  resolveEgoExit,
  studioUrlFor,
  uploadLimitHit,
  uploadSignals,
  validatePublishInput,
  verifyPublished,
  videoUrlFor,
  visibilitySelector,
} from "../lib/pure.mjs";

test("classifyLogin treats the Google wall as logged out and Studio chrome as logged in", () => {
  const wall = classifyLogin({
    url: "https://accounts.google.com/v3/signin",
    title: "Sign in",
    text: "Choose an account",
  });
  assert.equal(wall.logged_in, false);
  assert.equal(wall.login_required, true);
  assert.equal(wall.on_login_page, true);
  assert.equal(wall.login_wall, true);

  const studio = classifyLogin({
    url: STUDIO_URL,
    text: "YouTube Studio\nUpload videos\nAnalytics",
  });
  assert.equal(studio.logged_in, true);
  assert.equal(studio.login_required, false);
  assert.equal(studio.on_login_page, false);
  assert.equal(studio.login_wall, false);

  const chinese = classifyLogin({ url: STUDIO_URL, text: "YouTube 工作室\n上传视频\n数据分析" });
  assert.equal(chinese.logged_in, true);
  const dashboard = classifyLogin({ text: "Dashboard\nChannel content" });
  assert.equal(dashboard.logged_in, true);
});

test("a product name in the title is not Studio chrome, and the login wall wins over cookies", () => {
  const titled = classifyLogin({
    url: STUDIO_URL,
    title: "YouTube Studio",
    text: "",
  });
  assert.equal(titled.logged_in, false);
  assert.equal(titled.on_login_page, false);

  const cookieOnWall = classifyLogin({
    url: "https://accounts.google.com/ServiceLogin",
    cookie: "LOGIN_INFO=abc",
    text: "Sign in to YouTube",
  });
  assert.equal(cookieOnWall.logged_in, false);

  const zh = classifyLogin({ text: "使用 Google 账号登录" });
  assert.equal(zh.logged_in, false);
  assert.equal(classifyLogin({ text: "选择账号" }).on_login_page, true);
  assert.equal(classifyLogin({ text: "使用您的 Google 账号" }).login_wall, true);
  assert.equal(classifyLogin({ text: "登录以继续" }).on_login_page, true);
  assert.equal(classifyLogin({ text: "扫码登录" }).on_login_page, true);
});

test("login URL, cookie, and explicit signals", () => {
  assert.equal(isLoginWall({ url: "https://www.youtube.com/signin?next=%2F" }), true);
  assert.equal(isLoginWall({ url: "https://studio.youtube.com/" }), false);
  assert.equal(classifyLogin({ url: "https://accounts.google.com/ServiceLogin" }).logged_in, false);

  const cookie = classifyLogin({
    url: STUDIO_URL,
    cookie: "SAPISID=abc",
  });
  assert.equal(cookie.logged_in, true);
  assert.equal(classifyLogin({ url: STUDIO_URL, cookie: "__Secure-3PSID=abc" }).logged_in, true);
  assert.equal(classifyLogin({ url: STUDIO_URL, cookie: "__Secure-1PSID=abc" }).logged_in, true);
  assert.equal(classifyLogin({ url: STUDIO_URL, cookie: "VISITOR_INFO1_LIVE=abc" }).logged_in, false);

  const signaled = classifyLogin({ signals: { platformChrome: true } });
  assert.equal(signaled.logged_in, true);
  const forcedWall = classifyLogin({
    text: "YouTube Studio",
    signals: { onLoginWall: true },
  });
  assert.equal(forcedWall.logged_in, false);
  const cookieSignal = classifyLogin({ signals: { loggedInCookie: true } });
  assert.equal(cookieSignal.logged_in, true);

  const empty = classifyLogin({});
  assert.equal(empty.logged_in, false);
  assert.equal(empty.url, undefined);
  assert.equal(empty.title, undefined);

  const signals = detectSignals({
    url: STUDIO_URL,
    text: "Analytics",
    cookie: "LOGIN_INFO=1",
  });
  assert.equal(signals.platformChrome, true);
  assert.equal(signals.onLoginWall, false);
  assert.equal(signals.loggedInCookie, true);
  assert.equal(detectSignals({ url: "https://www.youtube.com/signin", title: "Sign in" }).onLoginWall, true);
});

test("needsRepaint reloads a blank Studio page and skips a real wall or session", () => {
  assert.equal(needsRepaint({ url: STUDIO_URL, text: "", platformChrome: false }), true);
  assert.equal(needsRepaint({ text: "Choose an account", onLoginWall: true }), false);
  assert.equal(needsRepaint({ platformChrome: true, text: "" }), false);
  assert.equal(needsRepaint({ url: STUDIO_URL, loggedInCookie: true }), false);
  assert.equal(needsRepaint({ url: "https://accounts.google.com/v3/signin" }), false);
  assert.equal(needsRepaint({ url: STUDIO_URL, cookie: "LOGIN_INFO=1" }), false);
});

test("parseCheckArgs and publish args, including defaults", () => {
  assert.equal(parseCheckArgs(["--keep"]).keep, true);
  assert.equal(parseCheckArgs(["--help"]).help, true);
  assert.equal(parseCheckArgs(["-h"]).help, true);
  assert.equal(parseCheckArgs(["--task-name", "yt-9"]).taskName, "yt-9");
  assert.equal(parseCheckArgs(["--task-name"]).taskName, "youtube-login-check");
  assert.throws(() => parseCheckArgs(["--nope"]), /Unknown arg/);

  const positional = parsePublishArgs(["/absolute/path/to/video.mp4", "Title", "Description"]);
  assert.equal(positional.video, "/absolute/path/to/video.mp4");
  assert.equal(positional.title, "Title");
  assert.equal(positional.description, "Description");
  assert.equal(positional.visibility, "private");
  assert.equal(positional.madeForKids, false);
  assert.equal(positional.keep, false);
  assert.equal(positional.spaceId, null);
  assert.deepEqual(positional.tags, []);

  const flags = parsePublishArgs([
    "--video=/absolute/path/to/video.mp4",
    "--title", "Title",
    "--desc", "About",
    "--tags", "one, two, one",
    "--visibility", "Unlisted",
    "--thumbnail", "/absolute/path/to/thumbnail.jpg",
    "--made-for-kids=yes",
    "--space-id", "4",
    "--keep",
  ]);
  assert.equal(flags.visibility, "unlisted");
  assert.equal(flags.madeForKids, true);
  assert.equal(flags.spaceId, 4);
  assert.equal(flags.keep, true);
  assert.deepEqual(flags.tags, ["one", "two"]);
  assert.equal(flags.description, "About");
  assert.equal(flags.thumbnail, "/absolute/path/to/thumbnail.jpg");

  const mixed = parsePublishArgs([
    "--title", "From flag",
    "/absolute/path/to/video.mp4",
    "ignored because title is set",
    "--no-keep",
  ]);
  assert.equal(mixed.video, "/absolute/path/to/video.mp4");
  assert.equal(mixed.title, "From flag");
  assert.equal(mixed.description, "ignored because title is set");
  assert.equal(mixed.keep, false);

  assert.equal(parseVisibility("PUBLIC"), "public");
  assert.equal(parseMadeForKids("false"), false);
  assert.equal(parseMadeForKids("1"), true);
  assert.equal(parseMadeForKids("n"), false);
  assert.equal(parseMadeForKids(undefined), false);
  assert.deepEqual(parseTags([" a ", "a", ""]), ["a"]);
  assert.deepEqual(parseTags(null), []);

  assert.throws(() => parsePublishArgs([]), /usage/);
  assert.throws(() => parsePublishArgs(["/absolute/path/to/video.mp4"]), /usage/);
  assert.throws(() => parsePublishArgs(["/absolute/path/to/video.mp4", "   "]), /usage/);
  assert.throws(() => parsePublishArgs(["a.mp4", "Title", "Desc", "extra"]), /too many/);
  assert.throws(() => parsePublishArgs(["--video"]), /requires a value/);
  assert.throws(() => parsePublishArgs(["--title", "--video", "a.mp4"]), /requires a value/);
  assert.throws(() => parsePublishArgs(["a.mp4", "Title", "--visibility", "friends"]), /visibility/);
  assert.throws(() => parsePublishArgs(["a.mp4", "Title", "--made-for-kids", "maybe"]), /made-for-kids/);
  assert.throws(() => parsePublishArgs(["a.mp4", "Title", "--space-id", "nope"]), /spaceId/);
  assert.throws(() => parsePublishArgs(["a.mp4", "Title", "--plugin"]), /Unknown arg/);
  assert.throws(() => parseVisibility("draft"), /visibility/);
  assert.throws(() => parseMadeForKids("maybe"), /made-for-kids/);
});

test("publish input rejects empty, huge, and non-video files", () => {
  const missing = validatePublishInput({ video: "/absolute/path/to/video.mp4", title: "Title", exists: false });
  assert.match(missing.error, /视频文件不存在/);
  assert.match(validatePublishInput({ title: "Title" }).error, /视频文件不存在/);
  const ext = validatePublishInput({
    video: "/absolute/path/to/notes.txt",
    title: "Title",
    exists: true,
    sizeBytes: 10,
  });
  assert.match(ext.error, /不是支持的视频文件/);
  const empty = validatePublishInput({
    video: "/absolute/path/to/video.mp4",
    title: "Title",
    exists: true,
    sizeBytes: 0,
  });
  assert.match(empty.error, /视频文件是空的/);
  const blank = validatePublishInput({
    video: "/absolute/path/to/video.mp4",
    title: "  ",
    exists: true,
    sizeBytes: 10,
  });
  assert.match(blank.error, /标题不能为空/);
  const longTitle = validatePublishInput({
    video: "/absolute/path/to/video.mp4",
    title: "a".repeat(101),
    exists: true,
    sizeBytes: 10,
  });
  assert.match(longTitle.error, /100/);
  const longDesc = validatePublishInput({
    video: "/absolute/path/to/video.mp4",
    title: "Title",
    description: "b".repeat(5001),
    exists: true,
    sizeBytes: 10,
  });
  assert.match(longDesc.error, /5000/);
  const badVis = validatePublishInput({
    video: "/absolute/path/to/video.mp4",
    title: "Title",
    visibility: "draft",
    exists: true,
    sizeBytes: 10,
  });
  assert.match(badVis.error, /公开范围/);
  const longTags = validatePublishInput({
    video: "/absolute/path/to/video.mp4",
    title: "Title",
    tags: ["x".repeat(501)],
    exists: true,
    sizeBytes: 10,
  });
  assert.match(longTags.error, /500/);
  const thumbMissing = validatePublishInput({
    video: "/absolute/path/to/video.mp4",
    title: "Title",
    thumbnail: "/absolute/path/to/thumbnail.jpg",
    exists: true,
    thumbExists: false,
    sizeBytes: 10,
  });
  assert.match(thumbMissing.error, /缩略图不存在/);
  const thumbExt = validatePublishInput({
    video: "/absolute/path/to/video.mp4",
    title: "Title",
    thumbnail: "/absolute/path/to/thumbnail.bmp",
    exists: true,
    thumbExists: true,
    sizeBytes: 10,
  });
  assert.match(thumbExt.error, /不是支持的缩略图/);

  const ok = validatePublishInput({
    video: "/absolute/path/to/video.webm",
    title: "  Title  ",
    description: "",
    tags: ["one", " one "],
    visibility: "PUBLIC",
    thumbnail: "/absolute/path/to/thumbnail.png",
    madeForKids: true,
    exists: true,
    thumbExists: true,
    sizeBytes: 1.26 * 1048576,
  });
  assert.equal(ok.ok, true);
  assert.equal(ok.sizeMB, 1.3);
  assert.equal(ok.visibility, "public");
  assert.equal(ok.madeForKids, true);
  assert.deepEqual(ok.tags, ["one"]);
});

test("metadata readback, upload signals, and processing status priority", () => {
  assert.equal(metadataWriteOk({ ok: true, title: "Title\u00a0", description: "" }, { title: " Title ", description: "" }), true);
  assert.equal(metadataWriteOk({ ok: true, title: "Title", description: "About" }, { title: "Title", description: " About " }), true);
  assert.equal(metadataWriteOk({ ok: true, title: "Other" }, { title: "Title" }), false);
  assert.equal(metadataWriteOk({ ok: true, title: "Title", description: "nope" }, { title: "Title", description: "About" }), false);
  assert.equal(metadataWriteOk({ ok: false, error: "未找到标题输入框" }, { title: "Title" }), false);
  assert.equal(metadataWriteOk(null, { title: "Title" }), false);

  assert.equal(uploadSignals("Uploading 40%").started, true);
  assert.equal(uploadSignals("Uploading 40%").uploading, true);
  assert.equal(uploadSignals("Upload complete").uploading, false);
  assert.equal(uploadSignals("Upload complete").status, "Upload complete");
  assert.equal(uploadSignals("正在上传").uploading, true);
  assert.equal(uploadSignals("上传完成").status, "Upload complete");
  assert.equal(uploadSignals("").started, false);

  assert.equal(classifyProcessingStatus("Checks complete\nUploading 10%"), "Checks complete");
  assert.equal(classifyProcessingStatus("No issues found"), "Checks complete");
  assert.equal(classifyProcessingStatus("检查完毕"), "Checks complete");
  assert.equal(classifyProcessingStatus("Processing will begin shortly"), "Processing");
  assert.equal(classifyProcessingStatus("处理即将开始"), "Processing");
  assert.equal(classifyProcessingStatus("正在处理 HD"), "Processing");
  assert.equal(classifyProcessingStatus("Video processing"), "Processing");
  assert.equal(classifyProcessingStatus("上传完毕"), "Upload complete");
  assert.equal(classifyProcessingStatus("上传中 20%"), "Uploading");
  assert.equal(classifyProcessingStatus("Video published"), "Published");
  assert.equal(classifyProcessingStatus("视频已发布"), "Published");
  assert.equal(classifyProcessingStatus("Your video is public"), "Published");
  assert.equal(classifyProcessingStatus("saved as private"), "Saved");
  assert.equal(classifyProcessingStatus("已保存"), "Saved");
  assert.equal(classifyProcessingStatus("Share your video"), "Saved");
  assert.equal(classifyProcessingStatus("分享你的视频"), "Saved");
  assert.equal(classifyProcessingStatus("Video link"), "Saved");
  assert.equal(classifyProcessingStatus("still choosing a file"), null);

  assert.equal(uploadLimitHit("You hit the daily upload limit"), true);
  assert.equal(uploadLimitHit("upload limit reached"), true);
  assert.equal(uploadLimitHit("上传次数已达上限"), true);
  assert.equal(uploadLimitHit("已达到上传上限"), true);
  assert.equal(uploadLimitHit("Upload complete"), false);
});

test("video id extraction is the publish success signal", () => {
  assert.equal(extractVideoId("https://youtu.be/AaBbCcDdEe1"), "AaBbCcDdEe1");
  assert.equal(extractVideoId("https://www.youtube.com/watch?v=AaBbCcDdEe1&t=3"), "AaBbCcDdEe1");
  assert.equal(extractVideoId("https://studio.youtube.com/video/AaBbCcDdEe1/edit"), "AaBbCcDdEe1");
  assert.equal(extractVideoId("https://www.youtube.com/shorts/AaBbCcDdEe1"), "AaBbCcDdEe1");
  assert.equal(extractVideoId("https://www.youtube.com/embed/AaBbCcDdEe1"), "AaBbCcDdEe1");
  assert.equal(extractVideoId("https://www.youtube.com/live/AaBbCcDdEe1"), "AaBbCcDdEe1");
  assert.equal(extractVideoId("https://youtu.be/AaBbCcDdEe"), null);
  assert.equal(extractVideoId("https://youtu.be/AaBbCcDdEe12"), null);
  assert.equal(extractVideoId("no id"), null);
  assert.equal(videoUrlFor("AaBbCcDdEe1"), "https://youtu.be/AaBbCcDdEe1");
  assert.equal(videoUrlFor(""), null);
  assert.equal(studioUrlFor("AaBbCcDdEe1"), "https://studio.youtube.com/video/AaBbCcDdEe1/edit");
  assert.equal(studioUrlFor(""), null);

  const good = verifyPublished({
    href: "https://youtu.be/AaBbCcDdEe1",
    pageUrl: "https://studio.youtube.com/video/AaBbCcDdEe1/edit",
    text: "Checks complete",
  });
  assert.equal(good.ok, true);
  assert.equal(good.status, "Checks complete");
  assert.equal(good.videoId, "AaBbCcDdEe1");
  assert.equal(good.videoUrl, "https://youtu.be/AaBbCcDdEe1");
  const noStatus = verifyPublished({ href: "https://youtu.be/AaBbCcDdEe1", text: "hello" });
  assert.equal(noStatus.ok, false);
  assert.equal(noStatus.status, undefined);
  const noId = verifyPublished({ text: "Upload complete" });
  assert.equal(noId.ok, false);
  assert.equal(verifyPublished({}).videoUrl, undefined);

  const body = publishSuccessBody({
    ...good,
    title: "Title",
    visibility: "private",
    madeForKids: false,
    tags: ["one"],
    spaceId: 4,
  });
  assert.equal(body.ok, true);
  assert.equal(body.status, "Checks complete");
  assert.equal(body.visibility, "private");
  assert.equal(body.description, "");
  assert.equal(body.madeForKids, false);
  assert.equal(body.spaceId, 4);
  assert.equal(audienceSelector(false), 'tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]');
  assert.equal(audienceSelector(true), 'tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_MFK"]');
  assert.equal(visibilitySelector("public"), 'tp-yt-paper-radio-button[name="PUBLIC"]');
  assert.equal(visibilitySelector("nope"), 'tp-yt-paper-radio-button[name="PRIVATE"]');
});

test("login-required and ego-missing summaries stay soft", () => {
  const missing = egoMissingSummary();
  assert.equal(missing.exitCode, 2);
  assert.equal(missing.command, "check-login");
  assert.equal(missing.login_required, true);
  assert.ok(missing.how_to_login.length >= 5);
  assert.match(missing.login_tip, /best results/);
  assert.match(missing.login_tip_zh, /YouTube/);
  assert.match(missing.how_to_login_zh[0], /Ego Lite/);
  assert.match(missing.how_to_login.join("\n"), /studio\.youtube\.com/);

  const publishMiss = egoMissingSummary("publish");
  assert.equal(publishMiss.command, "publish");

  const required = loginRequiredBody({ spaceId: 3 });
  assert.equal(required.exitCode, 2);
  assert.equal(required.spaceId, 3);
  assert.equal(required.how_to_login.length, 5);
  assert.match(required.error, /YouTube Studio login required/);
  const custom = loginRequiredBody({ error: "custom" });
  assert.equal(custom.error, "custom");

  assert.equal(flowErrorBody("未找到选择文件按钮", { spaceId: 3 }).exitCode, 1);
});

test("resolveEgoExit prefers JSON exitCode, then ego's wrapped code", () => {
  assert.equal(resolveEgoExit({
    stdout: JSON.stringify({ ok: true, status: "Processing" }),
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
