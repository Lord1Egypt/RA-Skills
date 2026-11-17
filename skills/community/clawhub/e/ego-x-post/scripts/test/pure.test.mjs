import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
  CAPTURED_CREATE_TWEET_QUERY_ID,
  CAPTURED_FEATURES,
  MAX_TEXT_CHARS,
  PUBLIC_WEB_BEARER,
  SMOKE_TEXT,
  buildCreateNoteTweetBody,
  buildCreateTweetBody,
  buildHeaders,
  charCount,
  classifyLogin,
  confirmationSummary,
  cookieHeaderNames,
  createTweetUrl,
  detectSignals,
  draftOf,
  egoMissingSummary,
  errorText,
  explainGraphqlFailure,
  extractCreateTweetQueryId,
  extractScriptUrls,
  extractTaggedJson,
  extractWebBearer,
  formatDraftText,
  fullTextFromResult,
  formatResult,
  hasHomeTitle,
  interpretCreateTweetResponse,
  isLoginWall,
  isQueryId,
  isScreenName,
  needsNoteTweet,
  needsRepaint,
  normalizeLanguage,
  onHome,
  parseCheckArgs,
  parseCleanupArgs,
  parseLooseJson,
  parsePostArgs,
  rankScriptUrls,
  resolveProcessExit,
  restIdFromResult,
  screenNameFromPath,
  screenNameFromResult,
  statusUrl,
  strip,
  tweetResult,
  weightedLength,
} from "../lib/pure.mjs";

const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const REST_ID = "2117826677376160218";

function created(screen = "Suchuanyi", extra = {}) {
  return {
    data: {
      create_tweet: {
        tweet_results: {
          result: {
            rest_id: REST_ID,
            legacy: { id_str: REST_ID, full_text: "ego-x-post-capture-ping" },
            core: { user_results: { result: { core: { screen_name: screen } } } },
            ...extra,
          },
        },
      },
    },
  };
}

test("strip, charCount, and the smoke text stay inside a standard post", () => {
  assert.deepEqual(strip({ a: 1, b: "", c: null, d: undefined, e: 0, f: false }), { a: 1, e: 0, f: false });
  assert.equal(charCount("a😀"), 2);
  assert.ok(charCount(SMOKE_TEXT) <= 280);
  assert.ok(SMOKE_TEXT.includes("https://github.com/terryso/ego-skills"));
  const skill = fs.readFileSync(path.join(skillRoot, "SKILL.md"), "utf8");
  assert.ok(skill.includes(SMOKE_TEXT));
});

test("argument parsers", () => {
  assert.equal(parseCheckArgs(["--help"]).help, true);
  assert.equal(parseCheckArgs(["-h", "--nope"]).help, true);
  assert.equal(parseCheckArgs(["--keep"]).keep, true);
  assert.equal(parseCheckArgs(["--task-name", "lane"]).taskName, "lane");
  assert.throws(() => parseCheckArgs(["--task-name"]), /Missing value/);
  assert.equal(parseCheckArgs(["--task-name", ""]).taskName, "x-post-login-check");
  assert.throws(() => parseCheckArgs(["--text"]), /Unknown arg/);
  assert.equal(parseCleanupArgs(["--task-name", "space"]).taskName, "space");
  assert.equal(parseCleanupArgs(["--task-name", ""]).taskName, "x-post");
  const post = parsePostArgs(["--text", " hello ", "--reply-to", "99", "--yes", "--json", "--keep", "--query-id", CAPTURED_CREATE_TWEET_QUERY_ID, "--task-name", "box"]);
  assert.equal(post.text, "hello");
  assert.equal(post.replyTo, "99");
  assert.equal(post.yes, true);
  assert.equal(post.json, true);
  assert.equal(post.keep, true);
  assert.equal(post.taskName, "box");
  assert.equal(parsePostArgs(["--help"]).help, true);
  assert.throws(() => parsePostArgs([]), /Missing --text/);
  assert.throws(() => parsePostArgs(["--text"]), /Missing value/);
  assert.throws(() => parsePostArgs(["--text", "--yes"]), /Missing value/);
  assert.throws(() => parsePostArgs(["--text", "x".repeat(MAX_TEXT_CHARS + 1)]), /25000/);
  assert.throws(() => parsePostArgs(["--text", "hi", "--reply-to", "abc"]), /numeric status id/);
  assert.throws(() => parsePostArgs(["--text", "hi", "--query-id", "short"]), /query id/);
  assert.throws(() => parsePostArgs(["--text", "hi", "--nope"]), /Unknown arg/);
  assert.deepEqual(post.images, []);
  const images = parsePostArgs(["--text", "hi", "--image", " a.PNG ", "--image", "b.jpeg", "--image", "c.webp"]);
  assert.deepEqual(images.images, ["a.PNG", "b.jpeg", "c.webp"]);
  assert.throws(() => parsePostArgs(["--text", "hi", "--image", "a.gif"]), /GIF is not supported/);
  assert.throws(() => parsePostArgs(["--text", "hi", "--image", "a.txt"]), /Unsupported image type/);
  assert.throws(() => parsePostArgs(["--text", "hi", "--image"]), /Missing value/);
  assert.throws(() => parsePostArgs(["--text", "hi", "--image", " "]), /Missing value for --image/);
  assert.throws(() => parsePostArgs(["--text", "hi", "--image", "a.png", "--image", "b.png", "--image", "c.png", "--image", "d.png", "--image", "e.png"]), /At most 4/);
});

test("draft formatting refuses to send and warns on replies and long text", () => {
  const summary = confirmationSummary({ text: "hi", replyTo: "" });
  assert.equal(summary.exitCode, 3);
  assert.equal(summary.sent, false);
  assert.match(formatDraftText(summary), /draft \(not sent\)/);
  assert.match(formatResult(summary), /Refusing to post/);
  assert.match(formatResult(summary, { asJson: true }), /"confirmation_required": true/);
  const reply = confirmationSummary({ text: `${"x".repeat(281)}`, replyTo: "5" });
  assert.equal(reply.draft.long_text, true);
  assert.equal(reply.draft.reply_best_effort, true);
  assert.match(formatDraftText(reply), /best-effort/);
  assert.match(formatDraftText(reply), /CreateNoteTweet/);
  assert.match(formatDraftText(summary), /media: \(none\)/);
  const pictured = confirmationSummary({
    text: "hi",
    images: [{ path: "/absolute/path/to/image.png", bytes: 10, md5: "abc123", data: Buffer.from([1]) }],
  });
  assert.match(formatDraftText(pictured), /media \(not uploaded\)/);
  assert.match(formatDraftText(pictured), /10 bytes, md5 abc123/);
  const picturedJson = formatResult(pictured, { asJson: true });
  assert.match(picturedJson, /"md5": "abc123"/);
  assert.equal(picturedJson.includes("media_id"), false);
  assert.equal(picturedJson.includes("\"data\""), false);
  assert.equal(formatDraftText({}).includes("chars: 0"), true);
  assert.match(formatDraftText({ draft: { media: [{ path: "/tmp/plain.png" }] } }), /size unknown/);
  assert.equal(formatResult(null), "");
  assert.equal(formatResult({ exitCode: 0, sent: true, url: "https://x.com/Suchuanyi/status/1" }), "https://x.com/Suchuanyi/status/1\n");
  assert.equal(draftOf({}).reply_to, null);
});

test("login classification uses auth_token, not ct0 alone", () => {
  assert.equal(isLoginWall({ url: "https://x.com/i/flow/login" }), true);
  assert.equal(isLoginWall({ url: "https://x.com/login?lang=en" }), true);
  assert.equal(isLoginWall({ url: "https://x.com/i/flow/signup" }), true);
  assert.equal(isLoginWall({ text: "Sign in to X" }), true);
  assert.equal(isLoginWall({ title: "登录 X" }), true);
  assert.equal(isLoginWall({ url: "https://x.com/home", text: "发帖" }), false);
  assert.equal(hasHomeTitle("主页 / X"), true);
  assert.equal(hasHomeTitle("Home / X"), true);
  assert.equal(hasHomeTitle("X"), false);
  assert.equal(onHome("https://x.com/home"), true);
  assert.equal(onHome("https://twitter.com/home/"), true);
  assert.equal(onHome("https://x.com/explore"), false);
  assert.equal(onHome("not a url"), false);
  assert.equal(isScreenName("Suchuanyi"), true);
  assert.equal(isScreenName("home"), false);
  assert.equal(isScreenName("bad name"), false);
  assert.equal(screenNameFromPath("/Suchuanyi"), "Suchuanyi");
  assert.equal(screenNameFromPath("https://x.com/Suchuanyi/"), "Suchuanyi");
  assert.equal(screenNameFromPath("/home"), "");
  assert.equal(screenNameFromPath("https://x.com/i/status/1"), "");
  assert.equal(screenNameFromPath("http://["), "");
  assert.equal(screenNameFromPath(""), "");
  assert.deepEqual(cookieHeaderNames(" ct0=secret; auth_token=nope "), ["ct0", "auth_token"]);
  assert.deepEqual(cookieHeaderNames(""), []);

  const authed = classifyLogin({
    url: "https://x.com/home",
    title: "主页 / X",
    text: "发帖",
    profileHref: "/Suchuanyi",
    authCookie: true,
    jarRead: true,
  });
  assert.equal(authed.logged_in, true);
  assert.equal(authed.screen_name, "Suchuanyi");

  const guest = classifyLogin({
    url: "https://x.com/home",
    title: "主页 / X",
    authCookie: false,
    csrfCookie: true,
    jarRead: true,
    profileHref: "/Suchuanyi",
  });
  assert.equal(guest.logged_in, false);

  const wall = classifyLogin({ url: "https://x.com/i/flow/login", authCookie: true, jarRead: true, onLoginWall: true });
  assert.equal(wall.logged_in, false);
  assert.equal(wall.on_login_page, true);

  const fallback = classifyLogin({
    url: "https://x.com/home",
    title: "Home / X",
    profileHref: "https://x.com/Suchuanyi",
    jarRead: false,
  });
  assert.equal(fallback.logged_in, true);

  const noJarNoProfile = classifyLogin({ url: "https://x.com/home", title: "主页 / X", jarRead: false });
  assert.equal(noJarNoProfile.logged_in, false);

  assert.equal(needsRepaint({ authCookie: true }), false);
  assert.equal(needsRepaint({ onLoginWall: true }), false);
  assert.equal(needsRepaint({ url: "https://x.com/login" }), false);
  assert.equal(needsRepaint({ title: "主页 / X" }), false);
  assert.equal(needsRepaint({ platformChrome: true }), false);
  assert.equal(needsRepaint({ profileHref: "/Suchuanyi" }), false);
  assert.equal(needsRepaint({ url: "about:blank" }), true);
  assert.equal(detectSignals({ title: "主页 / X", authCookie: 1 }).platformChrome, true);
  assert.equal(detectSignals({ text: "For you" }).platformChrome, true);

  const missing = egoMissingSummary("post");
  assert.equal(missing.exitCode, 2);
  assert.match(missing.how_to_login_zh[0], /Ego Lite/);
  assert.match(JSON.stringify(missing), /x\.com\/home/);
});

test("CreateTweet query id is captured, and other operations are ignored", () => {
  assert.equal(CAPTURED_CREATE_TWEET_QUERY_ID, "l4hk8uVGvR-a8kzQ4nOhPA");
  assert.equal(isQueryId(CAPTURED_CREATE_TWEET_QUERY_ID), true);
  assert.equal(isQueryId("short"), false);
  assert.equal(createTweetUrl(CAPTURED_CREATE_TWEET_QUERY_ID), `https://x.com/i/api/graphql/${CAPTURED_CREATE_TWEET_QUERY_ID}/CreateTweet`);
  assert.equal(createTweetUrl("nope"), "");
  assert.equal(Object.keys(CAPTURED_FEATURES).length, 39);
  assert.equal(CAPTURED_FEATURES.premium_content_api_read_enabled, false);
  assert.equal(CAPTURED_FEATURES.responsive_web_graphql_timeline_navigation_enabled, true);
  assert.match(PUBLIC_WEB_BEARER, /^AAAAAAAAAAAAAAAAAAAAANRILg/);

  const html = `<script src="https://abs.twimg.com/responsive-web/client-web/vendor.abc.js"></script><script src="https://abs.twimg.com/responsive-web/client-web/main.0a76dc3677efe2b2a.js"></script><script src="https://abs.twimg.com/responsive-web/client-web/main.0a76dc3677efe2b2a.js"></script>`;
  const urls = extractScriptUrls(html);
  assert.equal(urls.length, 2);
  const ranked = rankScriptUrls([
    "https://abs.twimg.com/responsive-web/client-web/vendor.1.js",
    "https://abs.twimg.com/responsive-web/client-web/bundle.2.js",
    ...urls,
  ]);
  assert.match(ranked[0], /\/main\./);
  assert.match(ranked[1], /\/bundle\./);
  assert.equal(extractScriptUrls("").length, 0);
  assert.deepEqual(rankScriptUrls(null), []);

  const forward = `queryId:"nxpZCY2K-I6QoFHAHeojFQ",operationName:"DeleteTweet"}{queryId:"${CAPTURED_CREATE_TWEET_QUERY_ID}",operationName:"CreateTweet",operationType:"mutation"`;
  assert.equal(extractCreateTweetQueryId(forward), CAPTURED_CREATE_TWEET_QUERY_ID);
  const reverse = `operationName:"CreateTweet",operationType:"mutation",queryId:"${CAPTURED_CREATE_TWEET_QUERY_ID}"`;
  assert.equal(extractCreateTweetQueryId(reverse), CAPTURED_CREATE_TWEET_QUERY_ID);
  assert.equal(extractCreateTweetQueryId('operationName:"CreateTweet",operationName:"DeleteTweet",queryId:"nxpZCY2K-I6QoFHAHeojFQ"'), "");
  assert.equal(extractCreateTweetQueryId(""), "");
  assert.equal(extractWebBearer(`const t="${PUBLIC_WEB_BEARER}";`), PUBLIC_WEB_BEARER);
  assert.equal(extractWebBearer("no token"), "");

  const bundleDir = path.join(skillRoot, "scripts");
  const files = [];
  const walk = (dir) => {
    for (const name of fs.readdirSync(dir)) {
      const full = path.join(dir, name);
      if (fs.statSync(full).isDirectory()) walk(full);
      else if (name.endsWith(".mjs")) files.push(fs.readFileSync(full, "utf8"));
    }
  };
  walk(path.join(bundleDir, "lib"));
  for (const name of ["check-login.mjs", "post.mjs", "cleanup.mjs"]) {
    files.push(fs.readFileSync(path.join(bundleDir, name), "utf8"));
  }
  const source = files.join("\n");
  assert.equal(source.includes("nxpZCY2K-I6QoFHAHeojFQ"), false);
  assert.equal(source.includes("seOZkIS8AysCGfPo6yYPVA"), true);
  assert.equal(source.includes(".click("), false);
  assert.equal(fs.readFileSync(path.join(skillRoot, "references/create-tweet.md"), "utf8").includes("nxpZCY2K-I6QoFHAHeojFQ"), true);
});

test("request body matches the captured text-only contract", () => {
  const body = buildCreateTweetBody({ text: "ego-x-post-capture-ping", queryId: CAPTURED_CREATE_TWEET_QUERY_ID });
  assert.equal(body.variables.tweet_text, "ego-x-post-capture-ping");
  assert.equal(body.variables.disallowed_reply_options, null);
  assert.deepEqual(body.variables.media, { media_entities: [], possibly_sensitive: false });
  assert.deepEqual(body.variables.semantic_annotation_options, { source: "UniversalLink" });
  assert.equal("reply" in body.variables, false);
  assert.equal("composition_signal_1" in body.variables.semantic_annotation_options, false);
  const note = buildCreateNoteTweetBody({ text: "x".repeat(300), queryId: "seOZkIS8AysCGfPo6yYPVA" });
  assert.equal(note.variables.semantic_annotation_options.composition_signal_1, true);
  assert.equal(note.variables.semantic_annotation_options.source, "UniversalLink");
  assert.equal(note.queryId, "seOZkIS8AysCGfPo6yYPVA");
  assert.equal(needsNoteTweet("x".repeat(280)), false);
  assert.equal(needsNoteTweet("x".repeat(281)), true);
  assert.equal(needsNoteTweet("hi", { long: true }), true);
  assert.equal(needsNoteTweet("中".repeat(140)), false);
  assert.equal(needsNoteTweet("中".repeat(141)), true);
  assert.equal(weightedLength("https://example.com/hello"), 23);
  assert.equal(weightedLength(""), 0);
  assert.equal(body.queryId, CAPTURED_CREATE_TWEET_QUERY_ID);
  body.features.premium_content_api_read_enabled = true;
  assert.equal(CAPTURED_FEATURES.premium_content_api_read_enabled, false);
  const attached = buildCreateTweetBody({
    text: "hi",
    queryId: CAPTURED_CREATE_TWEET_QUERY_ID,
    mediaIds: ["2117874109082427392", "", null],
  });
  assert.deepEqual(attached.variables.media, {
    media_entities: [{ media_id: "2117874109082427392", tagged_users: [] }],
    possibly_sensitive: false,
  });
  const noteMedia = buildCreateNoteTweetBody({
    text: "x".repeat(300),
    queryId: "seOZkIS8AysCGfPo6yYPVA",
    mediaIds: ["1", "2"],
  });
  assert.deepEqual(noteMedia.variables.media.media_entities, [
    { media_id: "1", tagged_users: [] },
    { media_id: "2", tagged_users: [] },
  ]);
  assert.equal(noteMedia.variables.semantic_annotation_options.composition_signal_1, true);
  const reply = buildCreateTweetBody({ text: "r", replyTo: "5", queryId: CAPTURED_CREATE_TWEET_QUERY_ID });
  assert.deepEqual(reply.variables.reply, { in_reply_to_tweet_id: "5", exclude_reply_user_ids: [] });
  assert.equal(normalizeLanguage("zh_CN"), "zh-cn");
  assert.equal(normalizeLanguage("en"), "en");
  assert.equal(normalizeLanguage("nope"), "");
  assert.equal(normalizeLanguage(""), "");
  const headers = buildHeaders({ csrfToken: "secret", language: "zh-cn" });
  assert.equal(headers.authorization, `Bearer ${PUBLIC_WEB_BEARER}`);
  assert.equal(headers["x-csrf-token"], "secret");
  assert.equal(headers["x-twitter-auth-type"], "OAuth2Session");
  assert.equal(headers["x-twitter-client-language"], "zh-cn");
  assert.equal("x-client-transaction-id" in headers, false);
  assert.equal("x-csrf-token" in buildHeaders({ bearer: "AAAA" }), false);
  assert.match(buildHeaders({ bearer: "CUSTOM" }).authorization, /CUSTOM/);
});

test("response parsing returns the status URL and surfaces 226", () => {
  const ok = interpretCreateTweetResponse(200, created());
  assert.equal(ok.ok, true);
  assert.equal(ok.url, `https://x.com/Suchuanyi/status/${REST_ID}`);
  const legacy = created("");
  delete legacy.data.create_tweet.tweet_results.result.core.user_results.result.core;
  legacy.data.create_tweet.tweet_results.result.core.user_results.result.legacy = { screen_name: "Suchuanyi" };
  delete legacy.data.create_tweet.tweet_results.result.rest_id;
  assert.equal(screenNameFromResult(tweetResult(legacy)), "Suchuanyi");
  assert.equal(restIdFromResult(tweetResult(legacy)), REST_ID);
  const wrapped = { data: { create_tweet: { tweet_results: { result: { tweet: created().data.create_tweet.tweet_results.result } } } } };
  assert.equal(interpretCreateTweetResponse(200, wrapped).url, `https://x.com/Suchuanyi/status/${REST_ID}`);
  assert.equal(interpretCreateTweetResponse(200, { data: { create_tweet: { tweet_results: { result: { legacy: {} } } } } }).ok, false);
  assert.match(interpretCreateTweetResponse(200, "not-json").error, /non-JSON/);
  assert.match(interpretCreateTweetResponse(500, { data: {} }).error, /HTTP 500/);
  assert.equal(interpretCreateTweetResponse(200, JSON.stringify(created())).ok, true);
  assert.equal(interpretCreateTweetResponse(0, created()).ok, true);
  assert.deepEqual(parseLooseJson("{\"ok\":true,\"v\":\"a\nb\"}"), { ok: true, v: "a b" });
  assert.equal(parseLooseJson(""), null);
  assert.equal(parseLooseJson("{"), null);
  assert.equal(screenNameFromResult(null), "");
  assert.equal(screenNameFromResult({ core: { user_results: { result: { core: { screen_name: "home" } } } } }), "");
  assert.equal(restIdFromResult(null), "");
  assert.equal(tweetResult(null), null);
  assert.equal(tweetResult({ data: { create_tweet: { tweet_results: { result: "x" } } } }), null);
  assert.equal(statusUrl("nope name", REST_ID), `https://x.com/i/web/status/${REST_ID}`);
  assert.equal(statusUrl("Suchuanyi", "abc"), "");

  const blocked = interpretCreateTweetResponse(200, { errors: [{ code: 226, message: "Authorization: This request looks like it might be automated." }] }, { replyTo: "5" });
  assert.equal(blocked.ok, false);
  assert.equal(blocked.automated, true);
  assert.match(blocked.error, /best-effort/);
  const rootBlock = interpretCreateTweetResponse(200, { errors: [{ message: "automated", extensions: { code: "226" } }] });
  assert.match(rootBlock.error, /x-client-transaction-id/);
  assert.match(interpretCreateTweetResponse(429, { errors: [{ message: "Rate limit exceeded" }] }).error, /Not retried/);
  assert.match(interpretCreateTweetResponse(200, { errors: [{ code: 88, message: "Rate limit" }] }).error, /Not retried/);
  assert.equal(interpretCreateTweetResponse(401, {}).loginRequired, true);
  assert.match(interpretCreateTweetResponse(401, { errors: [{ message: "bad auth" }] }).error, /login required/i);
  const tooLong = interpretCreateTweetResponse(200, { errors: [{ code: 186, message: "Tweet needs to be a bit shorter." }] });
  assert.equal(tooLong.tooLong, true);
  assert.match(tooLong.error, /CreateNoteTweet/);
  const noteBlocked = interpretCreateTweetResponse(200, { errors: [{ code: 226, message: "automated" }] }, { note: true });
  assert.match(noteBlocked.error, /without x-client-transaction-id/);
  const noteBlockedWithId = interpretCreateTweetResponse(200, { errors: [{ code: 226, message: "automated" }] }, { note: true, hadTransactionId: true });
  assert.match(noteBlockedWithId.error, /even with x-client-transaction-id/);
  const full = "N".repeat(332);
  const noteBody = {
    data: {
      notetweet_create: {
        tweet_results: {
          result: {
            rest_id: "2117842578016215436",
            legacy: { id_str: "2117842578016215436", full_text: full.slice(0, 279) },
            note_tweet: { is_expandable: true, note_tweet_results: { result: { text: full } } },
            core: { user_results: { result: { core: { screen_name: "Suchuanyi" } } } },
          },
        },
      },
    },
  };
  const noted = interpretCreateTweetResponse(200, noteBody, { note: true });
  assert.equal(noted.ok, true);
  assert.equal(noted.note, true);
  assert.equal(noted.fullText, full);
  assert.equal(noted.url, "https://x.com/Suchuanyi/status/2117842578016215436");
  assert.equal(fullTextFromResult(noteBody.data.notetweet_create.tweet_results.result), full);
  assert.equal(fullTextFromResult({ legacy: { full_text: "short" } }), "short");
  assert.equal(fullTextFromResult(null), "");
  assert.equal(errorText([{ message: "only" }]), "only");
  assert.equal(errorText([null, { code: "", message: "m" }]), "m");
  assert.match(explainGraphqlFailure({ status: 403, errors: [{ message: "nope" }] }), /nope/);
  assert.match(explainGraphqlFailure({ status: 403, errors: [] }), /HTTP 403/);
});

test("tagged ego output and process exit", () => {
  assert.deepEqual(extractTaggedJson("noise\nXPOST{\"exitCode\":2}\n"), { exitCode: 2 });
  assert.equal(extractTaggedJson("XPOST{"), null);
  assert.equal(extractTaggedJson(""), null);
  assert.equal(resolveProcessExit("nodejs process exited with code 2", 0), 2);
  assert.equal(resolveProcessExit("ok", 0), 0);
  assert.equal(resolveProcessExit("fail", 7), 7);
  assert.equal(resolveProcessExit("fail", null), 1);
});
