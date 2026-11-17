import test from "node:test";
import assert from "node:assert/strict";
import {
  classifyLogin,
  contentTypeFor,
  parseCheckArgs,
  parseServeArgs,
  publicUrl,
  egoMissingSummary,
} from "../lib/pure.mjs";

test("classifyLogin detects login.html", () => {
  const r = classifyLogin({
    url: "https://channels.weixin.qq.com/login.html",
    title: "登录",
    text: "扫码登录",
  });
  assert.equal(r.logged_in, false);
  assert.equal(r.login_required, true);
  assert.equal(r.on_login_page, true);
});

test("classifyLogin detects platform home", () => {
  const r = classifyLogin({
    url: "https://channels.weixin.qq.com/platform",
    text: "内容管理 发表视频",
    signals: { platformChrome: true },
  });
  assert.equal(r.logged_in, true);
  assert.equal(r.login_required, false);
});

test("parse args", () => {
  assert.equal(parseCheckArgs(["--keep"]).keep, true);
  assert.equal(parseServeArgs(["--file", "/tmp/a.mp4", "--port", "18765"]).port, 18765);
  assert.throws(() => parseServeArgs([]));
});

test("content helpers", () => {
  assert.equal(contentTypeFor("x.mp4"), "video/mp4");
  assert.equal(contentTypeFor("clip.MOV"), "video/quicktime");
  assert.equal(contentTypeFor("a.webm"), "video/webm");
  assert.equal(contentTypeFor("c.png"), "image/png");
  assert.equal(contentTypeFor("c.jpg"), "image/jpeg");
  assert.equal(contentTypeFor("c.jpeg"), "image/jpeg");
  assert.equal(contentTypeFor("c.webp"), "image/webp");
  assert.equal(contentTypeFor("blob.bin"), "application/octet-stream");
  assert.equal(publicUrl(18765, "my video.mp4"), "http://127.0.0.1:18765/my%20video.mp4");
  const missing = egoMissingSummary();
  assert.equal(missing.exitCode, 2);
  assert.equal(missing.login_required, true);
  assert.ok(missing.how_to_login.length >= 5);
  assert.match(missing.login_tip_zh, /扫码/);
});

test("parseCheckArgs and parseServeArgs cover help, names, and bad ports", () => {
  assert.equal(parseCheckArgs(["--help"]).help, true);
  assert.equal(parseCheckArgs(["--task-name", "channels-9"]).taskName, "channels-9");
  assert.equal(parseCheckArgs(["--task-name"]).taskName, "wechat-channels-login-check");
  assert.throws(() => parseCheckArgs(["--nope"]), /Unknown arg/);
  const named = parseServeArgs(["--file", "/tmp/a.mp4", "--name", "clip.mp4", "--port", "9"]);
  assert.equal(named.name, "clip.mp4");
  assert.equal(named.port, 9);
  assert.equal(parseServeArgs(["--help"]).help, true);
  assert.equal(parseServeArgs(["-h"]).file, null);
  assert.throws(() => parseServeArgs(["--file", "/tmp/a.mp4", "--port", "0"]), /--port/);
  assert.throws(() => parseServeArgs(["--file", "/tmp/a.mp4", "--port", "nope"]), /--port/);
  assert.throws(() => parseServeArgs(["--port"]), /--file is required/);
});

test("classifyLogin uses cookies, draft chrome, and ignores QR text off the login page", () => {
  const cookie = classifyLogin({
    url: "https://channels.weixin.qq.com/",
    signals: { loggedInCookie: true },
  });
  assert.equal(cookie.logged_in, true);
  assert.equal(cookie.has_qr_hint, undefined);
  const draft = classifyLogin({ url: "https://channels.weixin.qq.com/platform/post/list", text: "草稿箱" });
  assert.equal(draft.logged_in, true);
  const query = classifyLogin({ url: "https://channels.weixin.qq.com/login?from=home", text: "微信扫一扫" });
  assert.equal(query.on_login_page, true);
  assert.equal(query.has_qr_hint, true);
  assert.equal(query.logged_in, false);
  const empty = classifyLogin({});
  assert.equal(empty.logged_in, false);
  assert.equal(empty.url, undefined);
});
