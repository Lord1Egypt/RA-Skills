import assert from "node:assert/strict";
import path from "node:path";
import test from "node:test";
import {
  LOGIN_TIP,
  LOGIN_TIP_ZH,
  MAX_PREVIEW_BYTES,
  USAGE,
  acceptMedia,
  assertPinimg,
  assertSafeOutDir,
  bufferFetchResponse,
  clampCount,
  clampPreviews,
  defaultOut,
  exitCodeFor,
  foldDomUrls,
  hlsDerivedMp4,
  ihtVideoId,
  interpretSession,
  isVideoUrl,
  mediaDimensions,
  meetsMinResolution,
  normalizePin,
  outputName,
  parseArgs,
  parseBoard,
  parseResourceResponse,
  pickVideo,
  pinIdFromInput,
  previewCandidates,
  previewPayload,
  readFetchResponse,
  readSummary,
  relatedRequest,
  resizeUrl,
  resourcePath,
  searchRequest,
  sizeCandidates,
  sniffImage,
  sniffVideo,
  toConfig,
  toOriginals,
  videoTryUrls,
} from "../lib/pure.mjs";

function jpeg(size = 120) {
  const buf = Buffer.alloc(size, 7);
  buf[0] = 0xff;
  buf[1] = 0xd8;
  buf[2] = 0xff;
  return buf;
}

const resolve = (value) => path.resolve(value);

test("parseArgs keeps the legacy search positionals and the new commands", () => {
  const legacy = parseArgs(["wallpaper", "2", "/tmp/pins"]);
  assert.equal(legacy.command, "search");
  assert.equal(legacy.query, "wallpaper");
  assert.equal(legacy.count, 2);
  assert.equal(legacy.outDir, "/tmp/pins");
  const related = parseArgs(["related", "--pin", "99", "--count", "4", "--allow-anonymous", "--keep"]);
  assert.equal(related.command, "related");
  assert.equal(related.pin, "99");
  assert.equal(related.count, 4);
  assert.equal(related.allowAnonymous, true);
  assert.equal(related.keepBrowser, true);
  const urls = parseArgs(["download", "--url", "https://i.pinimg.com/a.jpg", "--url", "https://v.pinimg.com/a.mp4"]);
  assert.deepEqual(urls.urls, ["https://i.pinimg.com/a.jpg", "https://v.pinimg.com/a.mp4"]);
  assert.equal(parseArgs(["--help"]).help, true);
  const sized = parseArgs(["--query", "wallpaper", "--min-width", "720", "--min-height", "480"]);
  assert.equal(sized.minWidth, 720);
  assert.equal(sized.minHeight, 480);
  assert.throws(() => parseArgs(["--min-width", "-1", "--query", "a"]), /min-width/);
  assert.throws(() => parseArgs(["--min-height", "tall", "--query", "a"]), /min-height/);
  assert.equal(parseArgs(["board", "pinterest.com/a/b"]).board, "pinterest.com/a/b");
  assert.equal(parseArgs(["preview", "https://i.pinimg.com/a.jpg"]).urls[0], "https://i.pinimg.com/a.jpg");
});

test("parseArgs rejects unknown flags and missing values", () => {
  assert.throws(() => parseArgs(["--nope"]), /Unknown option/);
  assert.throws(() => parseArgs(["--query"]), /Missing value/);
  assert.equal(clampCount(0), null);
  assert.equal(clampCount(101), null);
  assert.equal(clampCount("x"), null);
  assert.equal(clampCount(3), 3);
  assert.equal(clampPreviews(""), 0);
  assert.equal(clampPreviews(8), 8);
  assert.equal(clampPreviews(9), null);
  assert.equal(clampPreviews("no"), null);
});

test("toConfig resolves a safe directory and validates commands", () => {
  const config = toConfig(parseArgs(["--query", "wallpaper", "--out", "/tmp/pins", "--previews", "1", "--min-width", "640"]), {
    resolve,
    now: 5,
  });
  assert.equal(config.command, "search");
  assert.equal(config.taskName, "pinterest-download-5");
  assert.equal(config.previews, 1);
  assert.equal(config.minWidth, 640);
  assert.equal(config.minHeight, 0);
  assert.equal(config.outDir, path.resolve("/tmp/pins"));
  assert.throws(() => toConfig(parseArgs(["--size", "huge", "--query", "a"]), { resolve }), /--size/);
  assert.throws(() => toConfig(parseArgs(["--media", "nope", "--query", "a"]), { resolve }), /--media/);
  assert.throws(() => toConfig(parseArgs(["--count", "0", "--query", "a"]), { resolve }), /--count/);
  assert.throws(() => toConfig(parseArgs(["search"]), { resolve }), /query is required/);
  assert.throws(() => toConfig(parseArgs(["related"]), { resolve }), /--pin/);
  assert.throws(() => toConfig(parseArgs(["board"]), { resolve }), /--board/);
  assert.throws(() => toConfig(parseArgs(["download"]), { resolve }), /--url/);
  assert.throws(() => assertSafeOutDir("/", resolve), /filesystem root/);
  assert.equal(defaultOut("/Users/nick"), "/Users/nick/Downloads/pinterest-ego");
  assert.match(USAGE, /related/);
  assert.match(LOGIN_TIP, /anonymous/i);
  assert.match(LOGIN_TIP_ZH, /匿名/);
});

test("normalizePin, video picking, and media filters", () => {
  assert.equal(normalizePin({ type: "story" }), null);
  assert.equal(normalizePin({ type: "pin", is_promoted: true, images: { orig: { url: "https://i.pinimg.com/a.jpg" } } }), null);
  const image = normalizePin({
    type: "pin",
    id: "42",
    title: "Desk",
    images: { orig: { url: "https://i.pinimg.com/originals/aa/bb/cc.jpg", width: 400, height: 400 } },
  });
  assert.equal(image.id, "42");
  assert.equal(image.low_res, true);
  assert.equal(image.pin_url, "https://www.pinterest.com/pin/42/");
  const anon = normalizePin({
    type: "pin",
    id: "e1_abc",
    images: { "736x": { url: "https://i.pinimg.com/736x/aa/bb/cc.jpg", width: 736, height: 1000 } },
  });
  assert.equal(anon.id, undefined);
  const video = normalizePin({
    type: "pin",
    id: "7",
    images: { orig: { url: "https://i.pinimg.com/originals/aa/bb/v.jpg", width: 800, height: 600 } },
    videos: { video_list: { V_HLSV3: { url: "https://v.pinimg.com/videos/mc/hls/abc.m3u8" }, V_720P: { url: "https://v.pinimg.com/videos/mc/720p/abc.mp4", width: 720, height: 720, duration: 4000 } } },
  });
  assert.equal(video.video_url, "https://v.pinimg.com/videos/mc/720p/abc.mp4");
  assert.equal(video.video_seconds, 4);
  assert.equal(acceptMedia(video, "image"), false);
  assert.equal(acceptMedia(video, "video"), true);
  assert.equal(acceptMedia(image, "any"), true);
  const hlsOnly = pickVideo({
    story_pin_data: { pages: [{ blocks: [{ video: { video_list: { V_HLSV4: { url: "https://v.pinimg.com/videos/iht/hls/zz.m3u8", duration: 1500 } } } }] }] },
  });
  assert.equal(hlsOnly.video_url, "https://v.pinimg.com/videos/iht/expMp4/zz_720w.mp4");
  assert.equal(hlsOnly.video_hls, "https://v.pinimg.com/videos/iht/hls/zz.m3u8");
  assert.equal(hlsDerivedMp4("https://v.pinimg.com/videos/mc/hls/abc.m3u8"), "https://v.pinimg.com/videos/mc/720p/abc.mp4");
  assert.equal(
    hlsDerivedMp4("https://v1.pinimg.com/videos/iht/hls/f9/91/17/f99117a3c598ab87cd1233848fe90011.m3u8"),
    "https://v1.pinimg.com/videos/iht/expMp4/f9/91/17/f99117a3c598ab87cd1233848fe90011_720w.mp4",
  );
  assert.equal(hlsDerivedMp4("https://cdn.example/plain.mp4"), undefined);
  assert.equal(pickVideo({}), undefined);
});

test("urls, sniffing, names, and fetch limits", () => {
  assert.equal(
    resizeUrl("https://i.pinimg.com/originals/aa/bb/cc.png", "736x"),
    "https://i.pinimg.com/736x/aa/bb/cc.jpg",
  );
  assert.equal(resizeUrl("https://i.pinimg.com/236x/aa/bb/cc.jpg", "originals"), "https://i.pinimg.com/originals/aa/bb/cc.jpg");
  assert.equal(toOriginals(null), null);
  assert.equal(toOriginals("https://example.com/a.jpg"), "https://example.com/a.jpg");
  assert.equal(assertPinimg("https://i.pinimg.com/a.jpg").hostname, "i.pinimg.com");
  assert.equal(assertPinimg("https://v1.pinimg.com/videos/iht/hls/a_720w.cmfv").hostname, "v1.pinimg.com");
  assert.throws(() => assertPinimg("http://i.pinimg.com/a.jpg"), /https/);
  assert.throws(() => assertPinimg("https://evil.com/a.jpg"), /pinimg/);
  assert.throws(() => assertPinimg("not a url"), /Invalid/);
  assert.equal(sniffImage(jpeg()), "image/jpeg");
  const png = Buffer.alloc(16);
  png.writeUInt32BE(0x89504e47, 0);
  assert.equal(sniffImage(png), "image/png");
  assert.equal(sniffImage(Buffer.from("GIF89a-extra-bytes!!")), "image/gif");
  const webp = Buffer.alloc(12);
  webp.write("RIFF", 0, "ascii");
  webp.write("WEBP", 8, "ascii");
  assert.equal(sniffImage(webp), "image/webp");
  assert.equal(sniffImage(Buffer.from("hello")), null);
  const mp4 = Buffer.alloc(16);
  mp4.write("ftyp", 4, "ascii");
  assert.equal(sniffVideo(mp4), true);
  assert.equal(sniffVideo(Buffer.from("nope")), false);
  assert.equal(isVideoUrl("https://v.pinimg.com/a.mp4?x=1"), true);
  assert.equal(videoTryUrls("https://v.pinimg.com/videos/iht/hls/a.m3u8")[0], "https://v.pinimg.com/videos/iht/expMp4/a_720w.mp4");
  assert.equal(videoTryUrls("https://v.pinimg.com/nope.m3u8").length, 0);
  assert.equal(videoTryUrls("https://v.pinimg.com/v_720w.cmfv").length, 3);
  assert.deepEqual(videoTryUrls("https://v.pinimg.com/videos/mc/720p/abc.mp4"), ["https://v.pinimg.com/videos/mc/720p/abc.mp4"]);
  const sample = "https://v1.pinimg.com/videos/iht/hls/f9/91/17/f99117a3c598ab87cd1233848fe90011_720w.cmfv";
  const tries = videoTryUrls(sample);
  assert.equal(tries[0], "https://v1.pinimg.com/videos/iht/expMp4/f9/91/17/f99117a3c598ab87cd1233848fe90011_720w.mp4");
  assert.ok(tries.includes(sample));
  assert.equal(
    videoTryUrls("https://v1.pinimg.com/videos/iht/720p/f9/91/17/f99117a3c598ab87cd1233848fe90011.mp4")[0],
    tries[0],
  );
  assert.equal(ihtVideoId("https://cdn.example/plain.mp4"), null);
  assert.equal(meetsMinResolution({ width: 800, height: 600 }, 0, 0).ok, true);
  assert.equal(meetsMinResolution({ width: 800, height: 400 }, 720, 0).ok, true);
  assert.equal(meetsMinResolution({ width: 800, height: 400 }, 900, 0).ok, false);
  assert.equal(meetsMinResolution({ width: 800, height: 400 }, 0, 500).reason, "height 400 < 500");
  assert.equal(meetsMinResolution({ width: 800, height: 400 }, 700, 500).ok, false);
  assert.equal(meetsMinResolution({ height: 900 }, 100, 0).reason, "width unknown");
  assert.equal(meetsMinResolution({ video_width: 320, video_height: 320, width: 1080, height: 1920 }, 500, 0, "video").ok, false);
  assert.deepEqual(mediaDimensions({ video_width: 1280, width: 100 }, "video"), { width: 1280, height: 0 });
  assert.match(USAGE, /min-width/);
  assert.deepEqual(sizeCandidates("https://i.pinimg.com/originals/a.jpg", "originals")[0].includes("originals"), true);
  assert.ok(previewCandidates("https://i.pinimg.com/originals/a.jpg")[0].includes("/236x/"));
  assert.match(outputName(0, "https://i.pinimg.com/originals/aa/bb/file.jpg", "jpg"), /^01_file\.jpg$/);
  assert.equal(outputName(1, "not a url", "jpg"), "02_file.jpg");
  const preview = previewPayload(jpeg());
  assert.equal(preview.mimeType, "image/jpeg");
  assert.equal(Buffer.from(preview.data, "base64").length, 120);
  assert.throws(() => previewPayload(jpeg(50)), /too small/);
  assert.throws(() => previewPayload(Buffer.alloc(MAX_PREVIEW_BYTES + 5, 1)), /not an image/);
  const huge = jpeg(MAX_PREVIEW_BYTES + 5);
  assert.throws(() => previewPayload(huge), /too large/);
});

test("resource parsing, boards, and pin ids", async () => {
  const ok = parseResourceResponse({
    ok: true,
    status: 200,
    body: JSON.stringify({ resource_response: { message: "确定", http_status: 200, data: { results: [{ type: "pin" }] }, bookmark: "next" } }),
  });
  assert.equal(ok.error, null);
  assert.equal(ok.items.length, 1);
  assert.equal(ok.bookmark, "next");
  const ended = parseResourceResponse({
    ok: true,
    status: 200,
    body: { resource_response: { data: [{ type: "pin" }], bookmark: "-end-" } },
  });
  assert.equal(ended.bookmark, undefined);
  assert.equal(ended.items.length, 1);
  assert.match(parseResourceResponse({ ok: false, status: 403, body: {} }).error, /HTTP 403/);
  assert.match(parseResourceResponse({ ok: true, status: 200, body: "nope" }).error, /non-JSON/);
  assert.match(parseResourceResponse({ ok: true, status: 200, body: { resource_response: { status: "failure", http_status: 500 } } }).error, /500/);
  const request = searchRequest("壁纸", "bm");
  assert.equal(request.options.bookmarks[0], "bm");
  const path = resourcePath(request, 9);
  assert.match(path, /BaseSearchResource/);
  assert.match(path, /_=9/);
  assert.equal(relatedRequest("55").options.pin_id, "55");
  assert.equal(relatedRequest("55", "b").options.bookmarks[0], "b");
  const board = parseBoard("https://www.pinterest.com/ada/my%20board/");
  assert.equal(board.username, "ada");
  assert.equal(board.slug, "my board");
  assert.throws(() => parseBoard(""), /required/);
  assert.throws(() => parseBoard("/only"), /board URL/);
  assert.equal(parseBoard("pinterest.com/a/b").path, "/a/b/");
  assert.equal(pinIdFromInput("55").id, "55");
  assert.equal(pinIdFromInput("https://www.pinterest.com/pin/nice--77/").id, "77");
  assert.equal(pinIdFromInput("https://pin.it/abc").redirect, "https://pin.it/abc");
  assert.match(pinIdFromInput("e1_zz").error, /e1_/);
  assert.match(pinIdFromInput("").error, /required/);
  assert.match(pinIdFromInput("https://example.com/nope").error, /Could not find/);
  assert.match(pinIdFromInput("%%%%").error, /Not a pin/);
});

test("session interpretation and CLI result parsing", async () => {
  assert.equal(interpretSession({ url: "https://www.pinterest.com/search/pins/", unauth: true }).loggedIn, false);
  assert.equal(
    interpretSession({ url: "https://www.pinterest.com/", profile: true, authCookie: false, unauth: false }).loggedIn,
    true,
  );
  assert.equal(interpretSession({ url: "https://www.pinterest.com/login/", authCookie: true }).loggedIn, false);
  const dom = foldDomUrls(
    ["https://i.pinimg.com/236x/aa/bb/cc.jpg", "https://i.pinimg.com/236x/aa/bb/cc.jpg", "https://example.com/x.jpg"],
    5,
  );
  assert.equal(dom[0].image_url, "https://i.pinimg.com/originals/aa/bb/cc.jpg");
  assert.equal(dom.length, 2);
  const summary = readSummary(`noise\n${JSON.stringify({ skill: "pinterest-download", ok: true })}\nego's nodejs process exited with code 0\n`);
  assert.equal(summary.ok, true);
  assert.equal(readSummary("no json"), null);
  assert.equal(readSummary('{"skill": "pinterest-download"'), null);
  assert.equal(exitCodeFor({ ok: true, login_required: false }, 2), 0);
  assert.equal(exitCodeFor({ ok: false, login_required: true, exitCode: 2 }, 0), 2);
  assert.equal(exitCodeFor({ ok: false, exitCode: 2 }, 0), 2);
  assert.equal(exitCodeFor(null, 2), 2);
  assert.equal(exitCodeFor(null, null), 1);
  const head = readFetchResponse({ status: 200, headers: { get: (name) => (name === "content-length" ? "999999" : "video/mp4") } }, 10);
  assert.match(head.error, /larger than/);
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
  assert.equal(buffered.buf.length, 120);
  const small = jpeg(50);
  const tooBig = await bufferFetchResponse(
    {
      ok: true,
      status: 200,
      headers: { get: () => "" },
      arrayBuffer: async () => small.buffer.slice(small.byteOffset, small.byteOffset + small.byteLength),
    },
    10,
  );
  assert.match(tooBig.error, /larger than/);
});
