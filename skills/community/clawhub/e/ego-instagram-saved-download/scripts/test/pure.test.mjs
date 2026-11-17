import assert from "node:assert/strict";
import path from "node:path";
import test from "node:test";
import {
  LOGIN_TIP,
  LOGIN_TIP_ZH,
  USAGE,
  acceptPost,
  assertCdn,
  assertSafeOutDir,
  bufferFetchResponse,
  clampCount,
  defaultOut,
  domPosts,
  exitCodeFor,
  filesForPost,
  interpretSession,
  matchesQuery,
  normalizeSavedItem,
  outputName,
  parseArgs,
  parseSavedResponse,
  readSummary,
  savedPath,
  sniffImage,
  sniffVideo,
  toConfig,
} from "../lib/pure.mjs";

const resolve = (value) => path.resolve(value);

function jpeg(size = 120) {
  const buf = Buffer.alloc(size, 4);
  buf[0] = 0xff;
  buf[1] = 0xd8;
  buf[2] = 0xff;
  return buf;
}

const photo = {
  pk: "10",
  code: "ABC123",
  media_type: 1,
  user: { username: "ada" },
  caption: { text: "beach morning" },
  image_versions2: {
    candidates: [
      { url: "https://scontent.cdninstagram.com/small.jpg", width: 320, height: 320 },
      { url: "https://scontent.cdninstagram.com/big.jpg", width: 1080, height: 1080 },
    ],
  },
};

test("parseArgs accepts list, count, query, and out", () => {
  const listed = parseArgs(["list", "--count", "3", "--query", "beach", "--out", "/tmp/ig", "--keep"]);
  assert.equal(listed.command, "saved");
  assert.equal(listed.count, 3);
  assert.equal(listed.query, "beach");
  assert.equal(listed.outDir, "/tmp/ig");
  assert.equal(listed.keepBrowser, true);
  const positional = parseArgs(["saved", "cafe", "4", "/tmp/out"]);
  assert.equal(positional.query, "cafe");
  assert.equal(positional.count, 4);
  assert.equal(positional.outDir, "/tmp/out");
  assert.equal(parseArgs(["--help"]).help, true);
  assert.throws(() => parseArgs(["--count", "0"]), /--count/);
  assert.throws(() => parseArgs(["--nope"]), /Unknown option/);
  assert.equal(clampCount("x"), null);
});

test("toConfig and login copy", () => {
  const config = toConfig(parseArgs(["--count", "2", "--out", "/tmp/ig", "--media", "any"]), { resolve, now: 9 });
  assert.equal(config.limit, 2);
  assert.equal(config.media, "any");
  assert.equal(config.taskName, "instagram-saved-9");
  assert.equal(config.outDir, path.resolve("/tmp/ig"));
  assert.throws(() => toConfig(parseArgs(["--media", "nope"]), { resolve }), /--media/);
  assert.throws(() => assertSafeOutDir("/", resolve), /filesystem root/);
  assert.equal(defaultOut("/Users/nick"), "/Users/nick/Downloads/instagram-saved");
  assert.match(USAGE, /Saved/);
  assert.match(LOGIN_TIP, /Anonymous/);
  assert.match(LOGIN_TIP_ZH, /收藏/);
});

test("session, saved payload, and media selection", () => {
  assert.equal(interpretSession({ url: "https://www.instagram.com/", password: true }).loggedIn, false);
  assert.equal(interpretSession({ url: "https://www.instagram.com/accounts/login/", inbox: true }).loggedIn, false);
  assert.equal(interpretSession({ url: "https://www.instagram.com/", inbox: true }).loggedIn, true);
  assert.equal(interpretSession({ url: "https://www.instagram.com/saved/all-posts/", dsUser: true }).loggedIn, true);
  assert.equal(interpretSession({ url: "https://www.instagram.com/saved/all-posts/", saved: true }).loggedIn, false);
  assert.equal(savedPath(), "/api/v1/feed/saved/posts/");
  assert.match(savedPath("abc 1"), /max_id=abc%201/);

  const wrapped = parseSavedResponse({
    ok: true,
    status: 200,
    body: {
      items: [{ media: photo }, { media: { media_type: 8 } }],
      more_available: true,
      next_max_id: "n1",
    },
  });
  assert.equal(wrapped.error, null);
  assert.equal(wrapped.posts.length, 1);
  assert.equal(wrapped.posts[0].images[0].urls[0], "https://scontent.cdninstagram.com/big.jpg");
  assert.equal(wrapped.posts[0].permalink, "https://www.instagram.com/p/ABC123/");
  assert.equal(wrapped.nextMaxId, "n1");
  assert.equal(matchesQuery(wrapped.posts[0], "Beach"), true);
  assert.equal(matchesQuery(wrapped.posts[0], "nope"), false);
  assert.equal(matchesQuery(wrapped.posts[0], ""), true);

  const direct = normalizeSavedItem({
    id: "9",
    code: "VID",
    media_type: 2,
    image_versions2: { candidates: [{ url: "https://scontent.cdninstagram.com/cover.jpg", width: 640, height: 640 }] },
    video_versions: [{ url: "https://scontent.cdninstagram.com/v.mp4", width: 720 }],
    carousel_media: [
      { image_versions2: { candidates: [{ url: "https://scontent.cdninstagram.com/c1.jpg", width: 800 }] } },
      { video_url: "https://video.cdninstagram.com/c2.mp4" },
    ],
  });
  assert.equal(direct.images.length, 1);
  assert.ok(direct.videos.length >= 1);
  assert.equal(acceptPost(direct, "video"), true);
  assert.equal(filesForPost(direct, "image").every((file) => file.kind === "image"), true);
  assert.equal(filesForPost(direct, "video").every((file) => file.kind === "video"), true);
  assert.ok(filesForPost(direct, "any").some((file) => file.kind === "video"));
  assert.equal(normalizeSavedItem(null), null);
  assert.equal(normalizeSavedItem({ media_type: 1 }), null);

  const ended = parseSavedResponse({
    ok: true,
    status: 200,
    body: JSON.stringify({ items: [photo], more_available: false, next_max_id: "ignored" }),
  });
  assert.equal(ended.nextMaxId, undefined);
  assert.match(parseSavedResponse({ ok: false, status: 500, body: {} }).error, /HTTP 500/);
  assert.equal(parseSavedResponse({ ok: false, status: 401, body: {} }).loginRequired, true);
  assert.match(parseSavedResponse({ ok: true, status: 200, body: "nope" }).error, /non-JSON/);
  assert.equal(parseSavedResponse({ ok: true, status: 200, body: { message: "login_required", status: "fail" } }).loginRequired, true);
  assert.equal(parseSavedResponse({ ok: true, status: 200, body: "<html>login</html>" }).loginRequired, true);

  assert.equal(assertCdn("https://scontent.cdninstagram.com/a.jpg").protocol, "https:");
  assert.throws(() => assertCdn("https://evil.example/a.jpg"), /CDN/);
  assert.throws(() => assertCdn("http://scontent.cdninstagram.com/a.jpg"), /CDN/);
  assert.equal(sniffImage(jpeg()), "image/jpeg");
  const mp4 = Buffer.alloc(16);
  mp4.write("ftyp", 4, "ascii");
  assert.equal(sniffVideo(mp4), true);
  assert.equal(sniffVideo(Buffer.from("no")), false);
  assert.equal(outputName(0, 0, "ABC123", "jpg"), "01_ABC123.jpg");
  assert.equal(outputName(1, 2, "ABC123", "mp4"), "02_ABC123_s03.mp4");
  const dom = domPosts(["https://scontent.cdninstagram.com/a.jpg", "https://evil.example/a.jpg", "https://scontent.cdninstagram.com/a.jpg"]);
  assert.equal(dom.length, 1);
});

test("summary parsing and fetch size cap", async () => {
  const summary = readSummary(`x\n${JSON.stringify({ skill: "instagram-saved-download", ok: true })}\n`);
  assert.equal(summary.ok, true);
  assert.equal(readSummary("nope"), null);
  assert.equal(readSummary('{"skill": "instagram-saved-download"'), null);
  assert.equal(exitCodeFor({ ok: true }, 2), 0);
  assert.equal(exitCodeFor({ ok: false, login_required: true, exitCode: 2 }, 0), 2);
  assert.equal(exitCodeFor(null, null), 1);
  const bytes = jpeg();
  const buffered = await bufferFetchResponse(
    {
      ok: true,
      status: 200,
      headers: { get: () => "" },
      arrayBuffer: async () => bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
    },
    10_000,
  );
  assert.equal(buffered.ok, true);
  const tooBig = await bufferFetchResponse(
    { ok: true, status: 200, headers: { get: (name) => (name === "content-length" ? "999" : "") }, arrayBuffer: async () => bytes.buffer },
    10,
  );
  assert.match(tooBig.error, /larger than/);
});
