import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  CAPTURED_CREATE_NOTE_TWEET_QUERY_ID,
  CAPTURED_CREATE_TWEET_QUERY_ID,
  PUBLIC_WEB_BEARER,
} from "../lib/pure.mjs";
import { executeCleanup, executePost, performPost, resolveCreateTweetQuery } from "../lib/post-flow.mjs";

const CSRF = "csrf-secret-value";
const REST_ID = "2117826829981749672";

function successBody(screen = "Suchuanyi") {
  return {
    data: {
      create_tweet: {
        tweet_results: {
          result: {
            rest_id: REST_ID,
            legacy: { id_str: REST_ID },
            core: { user_results: { result: { core: { screen_name: screen } } } },
          },
        },
      },
    },
  };
}

function session(overrides = {}) {
  const calls = { post: null, goto: [], hand: 0, finish: 0, fetched: [] };
  return {
    calls,
    spaceId: 19,
    async ensureSite() {},
    async detect() {
      return overrides.detect ?? {
        url: "https://x.com/home",
        title: "主页 / X",
        text: "发帖",
        lang: "zh-CN",
        authCookie: true,
        csrfCookie: true,
        jarRead: true,
        onLoginWall: false,
        platformChrome: true,
        profileHref: "/Suchuanyi",
      };
    },
    async csrfToken() { return overrides.csrf === undefined ? CSRF : overrides.csrf; },
    async pageSource() {
      if (overrides.pageSourceError) throw new Error("html down");
      return overrides.html ?? "<html></html>";
    },
    async fetchText(url) {
      calls.fetched.push(url);
      if (overrides.fetchError) throw new Error("bundle down");
      return overrides.bundle ?? "";
    },
    async fetchPublicJs(url) {
      calls.fetched.push(url);
      if (overrides.fetchError) throw new Error("bundle down");
      return overrides.bundle ?? "";
    },
    async screenName() {
      if (overrides.screenError) throw new Error("no profile");
      return overrides.href ?? "/Suchuanyi";
    },
    async postJson(request) {
      calls.post = request;
      return overrides.response ?? { status: 200, body: successBody() };
    },
    async goto(url) { calls.goto.push(url); },
    async handOff() {
      calls.hand += 1;
      if (overrides.handError) throw new Error("hand");
    },
    async finish() {
      calls.finish += 1;
      if (overrides.finishError) throw new Error("finish");
    },
    async cleanup() { calls.finish += 1; },
    async clientTransaction() { return "tid-from-session"; },
  };
}

test("a verified CreateTweet response becomes the status URL", async () => {
  const live = session();
  const summary = await performPost({ yes: true, text: "ego-x-post-capture-ping" }, live);
  assert.equal(summary.exitCode, 0);
  assert.equal(summary.sent, true);
  assert.equal(summary.url, `https://x.com/Suchuanyi/status/${REST_ID}`);
  assert.equal(summary.query_id, CAPTURED_CREATE_TWEET_QUERY_ID);
  assert.equal(summary.query_id_source, "captured-2026-11-04");
  assert.equal(live.calls.post.headers["x-csrf-token"], CSRF);
  assert.equal(live.calls.post.headers.authorization, `Bearer ${PUBLIC_WEB_BEARER}`);
  assert.equal(live.calls.post.headers["x-twitter-client-language"], "zh-cn");
  assert.equal(live.calls.post.headers["x-client-transaction-id"], "tid-from-session");
  assert.equal(summary.transaction_id_source, "generated");
  assert.equal(live.calls.post.body.variables.disallowed_reply_options, null);
  assert.equal(JSON.stringify(summary).includes(CSRF), false);
  assert.equal(JSON.stringify(summary).includes(PUBLIC_WEB_BEARER), false);
});

test("bundle query id and bearer win over the captured fallback", async () => {
  const bundleId = "AbcdefghijklmnopQR";
  const bearer = "AAAAAAAAAAAAAAAAAAAAANRILgTESTTOKEN123456";
  const html = `<script src="https://abs.twimg.com/responsive-web/client-web/vendor.1.js"></script><script src="https://abs.twimg.com/responsive-web/client-web/main.deadbeef.js"></script>`;
  const live = session({
    html,
    bundle: `queryId:"${bundleId}",operationName:"CreateTweet" ${bearer}`,
  });
  const summary = await performPost({ yes: true, text: "hi" }, live);
  assert.equal(summary.query_id, bundleId);
  assert.equal(summary.query_id_source, "bundle");
  assert.equal(live.calls.post.url, `https://x.com/i/api/graphql/${bundleId}/CreateTweet`);
  assert.match(live.calls.fetched[0], /\/main\./);
  assert.match(live.calls.post.headers.authorization, /TESTTOKEN123456$/);
});

test("an explicit query id is sent, and a bad one is refused", async () => {
  const live = session({ html: `queryId:"ShouldNotUse0000",operationName:"CreateTweet"` });
  const summary = await performPost({ yes: true, text: "hi", queryId: "OverrideId123456" }, live);
  assert.equal(summary.query_id, "OverrideId123456");
  assert.equal(summary.query_id_source, "flag");
  assert.equal(live.calls.fetched.length, 0);
  const bad = await performPost({ yes: true, text: "hi", queryId: "!!!" }, session());
  assert.equal(bad.exitCode, 1);
  assert.match(bad.error, /not usable/);
  assert.equal(bad.query_id_source, "flag");
});

test("screen name falls back to the profile link, then i/web", async () => {
  const nameless = successBody("");
  delete nameless.data.create_tweet.tweet_results.result.core;
  const fromProfile = await performPost({ yes: true, text: "hi" }, session({
    response: { status: 200, body: nameless },
    href: "https://x.com/Suchuanyi",
  }));
  assert.equal(fromProfile.url, `https://x.com/Suchuanyi/status/${REST_ID}`);
  const web = await performPost({ yes: true, text: "hi" }, session({
    response: { status: 200, body: nameless },
    href: "/home",
    screenError: true,
  }));
  assert.equal(web.url, `https://x.com/i/web/status/${REST_ID}`);
});

test("replies are sent as best-effort and 226 is not retried", async () => {
  const live = session();
  const summary = await performPost({ yes: true, text: "reply", replyTo: "2117826677376160218" }, live);
  assert.equal(summary.reply_best_effort, true);
  assert.match(summary.warning, /226/);
  assert.equal(live.calls.post.body.variables.reply.in_reply_to_tweet_id, "2117826677376160218");
  const blocked = await performPost({ yes: true, text: "reply", replyTo: "5" }, session({
    response: { status: 200, body: { errors: [{ code: 226, message: "This request looks like it might be automated." }] } },
  }));
  assert.equal(blocked.exitCode, 1);
  assert.match(blocked.error, /best-effort/);
  assert.equal(blocked.sent, false);
});

test("login, csrf, rate limit, and repaint", async () => {
  const wall = session({
    detect: { url: "https://x.com/i/flow/login", title: "登录 X", text: "Sign in to X", authCookie: false, jarRead: true, onLoginWall: true },
  });
  const loggedOut = await performPost({ yes: true, text: "hi", keep: true }, wall);
  assert.equal(loggedOut.exitCode, 2);
  assert.equal(wall.calls.hand, 1);
  assert.match(loggedOut.how_to_login[1], /x\.com\/home/);
  const handFails = session({
    detect: { url: "https://x.com/i/flow/login", title: "登录", text: "", authCookie: false, jarRead: true, onLoginWall: true },
    handError: true,
  });
  assert.equal((await performPost({ yes: true, text: "hi", keep: true }, handFails)).exitCode, 2);

  const noCsrf = await performPost({ yes: true, text: "hi", keep: true }, session({ csrf: "", handError: true }));
  assert.equal(noCsrf.exitCode, 2);
  assert.match(noCsrf.error, /ct0 missing/);

  const blank = session({
    detect: { url: "about:blank", title: "", text: "", authCookie: false, jarRead: false },
  });
  let paints = 0;
  blank.detect = async () => {
    paints += 1;
    if (paints === 1) return { url: "about:blank", title: "", text: "", authCookie: false, jarRead: false };
    return { url: "https://x.com/home", title: "主页 / X", text: "发帖", lang: "", authCookie: true, jarRead: true, profileHref: "/Suchuanyi" };
  };
  const painted = await performPost({ yes: true, text: "hi" }, blank);
  assert.equal(painted.exitCode, 0);
  assert.equal(blank.calls.goto[0], "https://x.com/home");
  assert.equal("x-twitter-client-language" in blank.calls.post.headers, false);

  const limited = await performPost({ yes: true, text: "hi" }, session({
    response: { status: 429, body: { errors: [{ code: 88, message: "Rate limit exceeded" }] } },
  }));
  assert.match(limited.error, /Not retried/);
  const unauth = await performPost({ yes: true, text: "hi" }, session({
    response: { status: 401, body: { errors: [{ message: "Could not authenticate" }] } },
  }));
  assert.equal(unauth.exitCode, 2);
});

test("without --yes nothing is fetched, and executePost closes the space", async () => {
  const live = session();
  const draft = await performPost({ text: "hi" }, live);
  assert.equal(draft.exitCode, 3);
  assert.equal(live.calls.post, null);
  const browser = {
    async open() { throw new Error("should not open"); },
  };
  const skipped = await executePost({ text: "hi" }, { browser });
  assert.equal(skipped.exitCode, 3);

  const opened = session();
  const summary = await executePost({ yes: true, text: "hi", keep: true, taskName: "custom" }, {
    browser: {
      async open(opts) {
        assert.equal(opts.taskName, "custom");
        assert.equal(opts.keepBrowser, true);
        assert.equal(opts.startUrl, "https://x.com/home");
        return opened;
      },
    },
  });
  assert.equal(summary.exitCode, 0);
  assert.equal(summary.spaceId, 19);
  assert.equal(opened.calls.finish, 1);

  const boom = await executePost({ yes: true, text: "hi" }, {
    browser: { async open() { throw new Error("space down"); } },
  });
  assert.equal(boom.exitCode, 1);
  assert.match(boom.error, /space down/);

  const finishBoom = session({ finishError: true });
  const finished = await executePost({ yes: true, text: "hi" }, {
    browser: { async open() { return finishBoom; } },
  });
  assert.equal(finished.exitCode, 0);
  assert.match(finished.finish_error, /finish/);
});

test("text over the short limit uses CreateNoteTweet and a transaction id", async () => {
  const live = session();
  live.clientTransaction = async ({ method, path }) => {
    assert.equal(method, "POST");
    assert.match(path, /\/CreateNoteTweet$/);
    return "tid-secret-value";
  };
  const summary = await performPost({ yes: true, text: "x".repeat(332) }, live);
  assert.equal(summary.exitCode, 0);
  assert.equal(summary.operation, "CreateNoteTweet");
  assert.equal(summary.note, true);
  assert.equal(summary.query_id, CAPTURED_CREATE_NOTE_TWEET_QUERY_ID);
  assert.equal(summary.query_id_source, "captured-note-2026-11-04");
  assert.equal(summary.transaction_id_source, "generated");
  assert.equal(live.calls.post.url, `https://x.com/i/api/graphql/${CAPTURED_CREATE_NOTE_TWEET_QUERY_ID}/CreateNoteTweet`);
  assert.equal(live.calls.post.headers["x-client-transaction-id"], "tid-secret-value");
  assert.equal(live.calls.post.body.variables.semantic_annotation_options.composition_signal_1, true);
  assert.equal(JSON.stringify(summary).includes("tid-secret-value"), false);
  assert.equal("x-client-transaction-id" in (await (async () => live.calls.post.headers)()), true);

  const broken = session();
  broken.clientTransaction = async () => { throw new Error("anim down"); };
  const missed = await performPost({ yes: true, text: "x".repeat(281) }, broken);
  assert.equal(missed.sent, false);
  assert.equal(missed.exitCode, 1);
  assert.equal(missed.transaction_id_source, "missing");
  assert.equal(broken.calls.post, null);
  assert.match(missed.error, /Refusing to post without x-client-transaction-id/);
  assert.match(missed.error, /loading-x-anim/);

  const forced = session();
  forced.clientTransaction = async () => { throw new Error("anim down"); };
  const flagged = await performPost({ yes: true, text: "hi", long: true, transactionId: "from-flag" }, forced);
  assert.equal(flagged.operation, "CreateNoteTweet");
  assert.equal(flagged.transaction_id_source, "flag");
  assert.equal(forced.calls.post.headers["x-client-transaction-id"], "from-flag");
  assert.equal(JSON.stringify(flagged).includes("from-flag"), false);

  const bareSession = session();
  delete bareSession.clientTransaction;
  const bare = await performPost({ yes: true, text: "x".repeat(281) }, bareSession);
  assert.equal(bare.sent, false);
  assert.equal(bare.exitCode, 1);
  assert.equal(bare.calls ? bare.calls.post : bareSession.calls.post, null);
  assert.match(bare.error, /Refusing to post without x-client-transaction-id/);
  assert.equal(bare.transaction_id_source, "missing");

  const emptyId = session();
  emptyId.clientTransaction = async () => "";
  const emptyPost = await performPost({ yes: true, text: "hi" }, emptyId);
  assert.equal(emptyPost.sent, false);
  assert.equal(emptyId.calls.post, null);

  const sniffed = session();
  sniffed.clientTransaction = async () => ({ id: "from-another-op", source: "session" });
  const refusedSniff = await performPost({ yes: true, text: "hi" }, sniffed);
  assert.equal(refusedSniff.sent, false);
  assert.equal(refusedSniff.transaction_id_source, "missing");
  assert.equal(sniffed.calls.post, null);

  const rejected = session();
  rejected.clientTransaction = async () => "still-secret";
  const again = await performPost({ yes: true, text: "x".repeat(281) }, {
    ...rejected,
    async postJson(request) {
      rejected.calls.post = request;
      return { status: 200, body: { errors: [{ code: 226, message: "automated" }] } };
    },
  });
  assert.match(again.error, /even with x-client-transaction-id/);
  assert.equal(JSON.stringify(again).includes("still-secret"), false);

  const tooLong = await performPost({ yes: true, text: "hi" }, session({
    response: { status: 200, body: { errors: [{ code: 186, message: "Tweet needs to be a bit shorter." }] } },
  }));
  assert.match(tooLong.error, /GraphQL 186/);
});

test("resolveCreateTweetQuery survives a dead bundle fetch", async () => {
  const dead = session({ pageSourceError: true, fetchError: true });
  const resolved = await resolveCreateTweetQuery(dead, "");
  assert.equal(resolved.queryId, CAPTURED_CREATE_TWEET_QUERY_ID);
  const missed = session({
    html: '<script src="https://abs.twimg.com/responsive-web/client-web/main.err.js"></script>',
  });
  missed.fetchPublicJs = async (url) => {
    missed.calls.fetched.push(url);
    throw new Error("bundle down");
  };
  const fallback = await resolveCreateTweetQuery(missed, "");
  assert.equal(fallback.queryId, CAPTURED_CREATE_TWEET_QUERY_ID);
  assert.equal(missed.calls.fetched.length, 1);
  const shell = session({ html: "<html>no scripts</html>" });
  shell.shellHtml = async () => `<script src="https://abs.twimg.com/responsive-web/client-web/main.live.js"></script>`;
  shell.fetchPublicJs = async (url) => {
    shell.calls.fetched.push(url);
    if (String(url).includes("main.live")) return `queryId:"LiveNoteQueryId123",operationName:"CreateNoteTweet"`;
    return "";
  };
  shell.clientTransaction = async () => "tid-shell";
  const fromShell = await performPost({ yes: true, text: "x".repeat(300) }, shell);
  assert.equal(fromShell.query_id, "LiveNoteQueryId123");
  assert.equal(fromShell.query_id_source, "bundle");
  assert.equal(fromShell.operation, "CreateNoteTweet");
  assert.equal(shell.calls.post.headers["x-client-transaction-id"], "tid-shell");

  const fromDom = session({ html: "<html>no scripts</html>" });
  fromDom.scriptUrls = async () => ["https://abs.twimg.com/responsive-web/client-web/main.fromdom.js"];
  fromDom.fetchPublicJs = async (url) => {
    fromDom.calls.fetched.push(url);
    if (String(url).includes("main.fromdom")) return `queryId:"DomNoteQueryId12345",operationName:"CreateNoteTweet"`;
    return "";
  };
  fromDom.clientTransaction = async () => "tid-dom";
  const domId = await performPost({ yes: true, text: "x".repeat(300) }, fromDom);
  assert.equal(domId.query_id, "DomNoteQueryId12345");
  assert.equal(domId.query_id_source, "bundle");

  const paced = session();
  paced.paceCompose = async () => { paced.calls.goto.push("https://x.com/compose/post"); };
  const pacedPost = await performPost({ yes: true, text: "x".repeat(300) }, paced);
  assert.equal(pacedPost.operation, "CreateNoteTweet");
  assert.deepEqual(paced.calls.goto, ["https://x.com/compose/post"]);
  assert.equal(paced.calls.post.headers.origin, "https://x.com");
  assert.equal(paced.calls.post.headers.referer, "https://x.com/compose/post");
  assert.equal(paced.calls.post.headers["x-twitter-auth-type"], "OAuth2Session");
  assert.equal(paced.calls.post.headers["x-twitter-active-user"], "yes");

  const htmlId = session({ html: `queryId:"FromHtmlBundle1234",operationName:"CreateTweet" ${PUBLIC_WEB_BEARER}` });
  const fromHtml = await resolveCreateTweetQuery(htmlId, "");
  assert.equal(fromHtml.queryId, "FromHtmlBundle1234");
  assert.equal(fromHtml.bearer, PUBLIC_WEB_BEARER);
  assert.equal(htmlId.calls.fetched.length, 0);
});

test("cleanup closes the space and reports an open failure", async () => {
  const live = session();
  const closed = await executeCleanup({ taskName: "x-post" }, {
    browser: { async open(opts) { assert.equal(opts.keepBrowser, false); return live; } },
  });
  assert.equal(closed.ok, true);
  assert.deepEqual(closed.kept, []);
  assert.equal(live.calls.finish, 1);
  const failed = await executeCleanup({}, { browser: { async open() { throw new Error("no space"); } } });
  assert.equal(failed.exitCode, 1);
  const unnamed = await executeCleanup(null, { browser: { async open() { return live; } } });
  assert.equal(unnamed.ok, true);
});

const PNG_BYTES = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 4, 5]);

function pngFile(name, bytes = PNG_BYTES) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "x-post-flow-"));
  const file = path.join(dir, name);
  fs.writeFileSync(file, bytes);
  return file;
}

test("images are attached on CreateTweet and CreateNoteTweet only after login", async () => {
  const file = pngFile("card.png");
  const blocked = session();
  blocked.uploadImages = async () => { throw new Error("should not upload"); };
  const draft = await performPost({ text: "hi", images: [file] }, blocked);
  assert.equal(draft.exitCode, 3);
  assert.equal(blocked.calls.post, null);

  const sent = session();
  let uploaded = null;
  sent.uploadImages = async (request) => {
    uploaded = request;
    return request.images.map((image) => ({ path: image.path, media_id: "11", bytes: image.bytes }));
  };
  const summary = await performPost({ yes: true, text: "hi", images: [file] }, sent);
  assert.equal(summary.exitCode, 0);
  assert.equal(summary.sent, true);
  assert.equal(summary.url, `https://x.com/Suchuanyi/status/${REST_ID}`);
  assert.equal(summary.transaction_id_source, "generated");
  assert.equal(summary.query_id_source, "captured-2026-11-04");
  assert.deepEqual(summary.media, [{ path: file, media_id: "11", bytes: PNG_BYTES.length }]);
  assert.deepEqual(sent.calls.post.body.variables.media, {
    media_entities: [{ media_id: "11", tagged_users: [] }],
    possibly_sensitive: false,
  });
  assert.equal(uploaded.csrfToken, CSRF);
  assert.match(uploaded.bearer, /^AAAA/);
  assert.equal(uploaded.images[0].mediaType, "image/png");
  assert.equal(JSON.stringify(summary).includes(CSRF), false);
  assert.equal(JSON.stringify(summary).includes("\"tweet_id\""), false);

  const other = pngFile("b.png", Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 9]));
  const reply = session();
  reply.uploadImages = async (request) => request.images.map((image, index) => ({
    path: image.path,
    media_id: index === 0 ? "11" : "22",
    bytes: image.bytes,
  }));
  const withReply = await performPost({ yes: true, text: "hi", images: [file, other], replyTo: "5" }, reply);
  assert.deepEqual(withReply.media.map((item) => item.media_id), ["11", "22"]);
  assert.equal(reply.calls.post.body.variables.reply.in_reply_to_tweet_id, "5");
  assert.equal(reply.calls.post.body.variables.media.media_entities[1].tagged_users.length, 0);

  const noted = session();
  noted.clientTransaction = async () => "tid-note";
  noted.uploadImages = async (request) => request.images.map((image) => ({
    path: image.path,
    media_id: "11",
    bytes: image.bytes,
  }));
  const longPost = await performPost({ yes: true, text: "x".repeat(300), images: [file] }, noted);
  assert.equal(longPost.operation, "CreateNoteTweet");
  assert.equal(longPost.note, true);
  assert.equal(noted.calls.post.body.variables.semantic_annotation_options.composition_signal_1, true);
  assert.equal(noted.calls.post.body.variables.media.media_entities[0].media_id, "11");
  assert.deepEqual(longPost.media, [{ path: file, media_id: "11", bytes: PNG_BYTES.length }]);

  const forced = session();
  forced.clientTransaction = async () => "tid-long";
  forced.uploadImages = noted.uploadImages;
  const flagged = await performPost({ yes: true, text: "hi", long: true, images: [file] }, forced);
  assert.equal(flagged.operation, "CreateNoteTweet");
  assert.equal(forced.calls.post.body.variables.media.media_entities[0].media_id, "11");
});

test("a bad image or a failed upload never posts, and the space still closes", async () => {
  let ensured = 0;
  const missing = session();
  missing.ensureSite = async () => { ensured += 1; };
  const notFound = await performPost({ yes: true, text: "hi", images: ["/tmp/no-such-x-post-flow.png"] }, missing);
  assert.equal(notFound.exitCode, 1);
  assert.match(notFound.error, /Image not found/);
  assert.equal(ensured, 0);
  assert.equal(missing.calls.post, null);

  const file = pngFile("card.png");
  const loggedOut = session({
    detect: { url: "https://x.com/i/flow/login", title: "登录 X", text: "", authCookie: false, jarRead: true, onLoginWall: true },
  });
  loggedOut.uploadImages = async () => { throw new Error("uploaded"); };
  assert.equal((await performPost({ yes: true, text: "hi", images: [file] }, loggedOut)).exitCode, 2);

  const noCsrf = session({ csrf: "" });
  noCsrf.uploadImages = async () => { throw new Error("uploaded"); };
  assert.equal((await performPost({ yes: true, text: "hi", images: [file] }, noCsrf)).exitCode, 2);

  const broken = session();
  broken.clientTransaction = async () => { throw new Error("anim down"); };
  broken.uploadImages = async () => { throw new Error("uploaded"); };
  const missed = await performPost({ yes: true, text: "hi", images: [file] }, broken);
  assert.equal(missed.sent, false);
  assert.match(missed.error, /x-client-transaction-id/);

  const bare = session();
  const unavailable = await performPost({ yes: true, text: "hi", images: [file] }, bare);
  assert.match(unavailable.error, /unavailable/);
  assert.equal(bare.calls.post, null);

  const failed = session();
  failed.uploadImages = async () => { throw new Error("append broke"); };
  const uploadFailed = await performPost({ yes: true, text: "hi", images: [file] }, failed);
  assert.equal(uploadFailed.exitCode, 1);
  assert.equal(uploadFailed.sent, false);
  assert.match(uploadFailed.error, /Image upload failed: append broke/);
  assert.equal(failed.calls.post, null);

  const authed = session();
  authed.uploadImages = async () => {
    const error = new Error("card.png: INIT failed (HTTP 401): X login required in Ego Lite");
    error.loginRequired = true;
    throw error;
  };
  const relogin = await performPost({ yes: true, text: "hi", images: [file], keep: true }, authed);
  assert.equal(relogin.exitCode, 2);
  assert.equal(authed.calls.hand, 1);
  const handFails = session({ handError: true });
  handFails.uploadImages = authed.uploadImages;
  assert.equal((await performPost({ yes: true, text: "hi", images: [file], keep: true }, handFails)).exitCode, 2);

  const opened = session();
  opened.uploadImages = async () => { throw new Error("append broke"); };
  const closed = await executePost({ yes: true, text: "hi", images: [file] }, {
    browser: { async open() { return opened; } },
  });
  assert.equal(closed.exitCode, 1);
  assert.equal(opened.calls.finish, 1);
  assert.equal(opened.calls.post, null);
});
