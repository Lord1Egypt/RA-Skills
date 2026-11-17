import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  CHUNK_BYTES,
  MAX_CHUNK_BYTES,
  MAX_IMAGE_BYTES,
  MAX_IMAGES,
  appendUrl,
  clampChunkBytes,
  describeImages,
  finalizeUrl,
  initUrl,
  magicMatches,
  mediaIdFrom,
  mediaTypeForName,
  parseMediaJson,
  processingErrorText,
  segmentSlices,
  statusUrl,
} from "../lib/media.mjs";

const PNG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x01, 0x02]);
const JPEG = Buffer.from([0xff, 0xd8, 0xff, 0xe0, 0x00, 0x10]);
const WEBP = Buffer.concat([Buffer.from("RIFF"), Buffer.from([0, 0, 0, 0]), Buffer.from("WEBP"), Buffer.from([9])]);

test("image names accept png jpeg webp and reject gif", () => {
  assert.equal(mediaTypeForName("/tmp/Card.PNG"), "image/png");
  assert.equal(mediaTypeForName("photo.jpg"), "image/jpeg");
  assert.equal(mediaTypeForName("photo.jpeg"), "image/jpeg");
  assert.equal(mediaTypeForName("photo.WEBP"), "image/webp");
  assert.throws(() => mediaTypeForName("anim.gif"), /GIF is not supported/);
  assert.throws(() => mediaTypeForName("notes.txt"), /Unsupported image type/);
  assert.throws(() => mediaTypeForName(""), /Unsupported image type/);
  assert.equal(MAX_IMAGES, 4);
  assert.equal(MAX_IMAGE_BYTES, 5 * 1024 * 1024);
});

test("magic bytes match the three image types only", () => {
  assert.equal(magicMatches(null, "image/png"), false);
  assert.equal(magicMatches(PNG.subarray(0, 4), "image/png"), false);
  assert.equal(magicMatches(PNG, "image/png"), true);
  assert.equal(magicMatches(JPEG.subarray(0, 2), "image/jpeg"), false);
  assert.equal(magicMatches(JPEG, "image/jpeg"), true);
  assert.equal(magicMatches(WEBP.subarray(0, 8), "image/webp"), false);
  assert.equal(magicMatches(WEBP, "image/webp"), true);
  assert.equal(magicMatches(PNG, "image/gif"), false);
  assert.equal(magicMatches(JPEG, "image/png"), false);
});

test("chunk size is capped at 5 MiB and slices stay in order", () => {
  assert.equal(clampChunkBytes(0), CHUNK_BYTES);
  assert.equal(clampChunkBytes(-5), CHUNK_BYTES);
  assert.equal(clampChunkBytes(Number.NaN), CHUNK_BYTES);
  assert.equal(clampChunkBytes(32.9), 32);
  assert.equal(clampChunkBytes(9 * 1024 * 1024), MAX_CHUNK_BYTES);
  assert.equal(segmentSlices(Buffer.alloc(0)).length, 0);
  const slices = segmentSlices(Buffer.from([1, 2, 3, 4, 5, 6, 7]), 4);
  assert.deepEqual(slices.map((slice) => slice.index), [0, 1]);
  const joined = Buffer.concat(slices.map((slice) => Buffer.from(slice.b64, "base64")));
  assert.deepEqual([...joined], [1, 2, 3, 4, 5, 6, 7]);
  assert.equal(segmentSlices(Buffer.from([1, 2, 3]), 9 * 1024 * 1024).length, 1);
});

test("upload urls match the captured query shape", () => {
  assert.equal(
    initUrl({ totalBytes: 81425, mediaType: "image/png" }),
    "https://upload.x.com/i/media/upload.json?command=INIT&total_bytes=81425&media_type=image%2Fpng&media_category=tweet_image",
  );
  assert.equal(
    appendUrl({ mediaId: "2117874109082427392", segmentIndex: 0 }),
    "https://upload.x.com/i/media/upload.json?command=APPEND&media_id=2117874109082427392&segment_index=0",
  );
  assert.equal(
    finalizeUrl({ mediaId: "2117874109082427392", md5: "150443FD2CEADA6212A7A9A03103E66A" }),
    "https://upload.x.com/i/media/upload.json?command=FINALIZE&media_id=2117874109082427392&original_md5=150443fd2ceada6212a7a9a03103e66a",
  );
  assert.equal(
    statusUrl("2117874109082427392"),
    "https://upload.x.com/i/media/upload.json?command=STATUS&media_id=2117874109082427392",
  );
});

test("upload JSON helpers keep media_id_string and processing errors", () => {
  assert.equal(parseMediaJson(""), null);
  assert.equal(parseMediaJson(null), null);
  assert.equal(parseMediaJson("[]"), null);
  assert.equal(parseMediaJson("null"), null);
  assert.equal(parseMediaJson("{"), null);
  assert.deepEqual(parseMediaJson('{"media_id_string":"12"}'), { media_id_string: "12" });
  assert.deepEqual(parseMediaJson({ ok: true }), { ok: true });
  assert.equal(mediaIdFrom({ media_id_string: "2117874109082427392" }), "2117874109082427392");
  assert.equal(mediaIdFrom({ media_id_string: 2117874109082427392 }), "");
  assert.equal(mediaIdFrom({ media_id: "12" }), "");
  assert.equal(mediaIdFrom(null), "");
  assert.match(processingErrorText({ error: { code: 0 } }), /INTERNAL_ERROR/);
  assert.match(processingErrorText({ error: { code: 1 } }), /INVALID_MEDIA/);
  assert.match(processingErrorText({ error: { code: 2 } }), /FILE_TOO_LARGE/);
  assert.match(processingErrorText({ error: { code: 3 } }), /UNSUPPORTED_MEDIA/);
  assert.match(processingErrorText({ error: { code: 4 } }), /TIMEOUT/);
  assert.match(processingErrorText({ error: { code: 9 } }), /FAILED \(code 9\)/);
  assert.match(processingErrorText({}), /code \?/);
  assert.match(processingErrorText({ error: { code: "" } }), /code \?/);
  assert.match(processingErrorText({ error: { code: null } }), /code \?/);
});

test("describeImages reads png jpeg and webp and hashes the bytes", async () => {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "x-post-media-"));
  const png = path.join(dir, "card.png");
  const jpeg = path.join(dir, "card.jpg");
  const webp = path.join(dir, "card.webp");
  await fs.writeFile(png, PNG);
  await fs.writeFile(jpeg, JPEG);
  await fs.writeFile(webp, WEBP);
  const relative = path.relative(process.cwd(), png);
  const described = await describeImages([relative, jpeg, ` ${webp} `]);
  assert.equal(described[0].path, path.resolve(relative));
  assert.equal(described[0].bytes, PNG.length);
  assert.equal(described[0].mediaType, "image/png");
  assert.equal(described[0].md5, crypto.createHash("md5").update(PNG).digest("hex"));
  assert.equal(described[1].mediaType, "image/jpeg");
  assert.equal(described[2].mediaType, "image/webp");
  assert.equal(described[2].path, webp);
});

test("describeImages rejects bad files before a caller could upload them", async () => {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "x-post-media-bad-"));
  const folder = path.join(dir, "folder.png");
  await fs.mkdir(folder);
  await assert.rejects(describeImages([folder]), /not a file/);
  const empty = path.join(dir, "empty.png");
  await fs.writeFile(empty, Buffer.alloc(0));
  await assert.rejects(describeImages([empty]), /Image is empty/);
  await assert.rejects(describeImages(["/tmp/does-not-exist-x-post-card.png"]), /Image not found/);
  await assert.rejects(describeImages(["anim.gif"]), /GIF is not supported/);
  await assert.rejects(describeImages(null), /file paths/);
  await assert.rejects(describeImages(["a.png", "b.png", "c.png", "d.png", "e.png"]), /At most 4/);
  await assert.rejects(describeImages(["  "]), /Missing value/);

  let reads = 0;
  const stat = async () => ({ size: MAX_IMAGE_BYTES + 1, isFile: () => true });
  const readFile = async () => { reads += 1; return PNG; };
  await assert.rejects(describeImages(["/tmp/big.png"], { stat, readFile }), /exceeds 5 MiB/);
  assert.equal(reads, 0);

  await assert.rejects(describeImages(["/tmp/card.png"], {
    stat: async () => { const error = new Error("denied"); error.code = "EACCES"; throw error; },
    readFile,
  }), /not readable: \/tmp\/card.png \(EACCES\)/);
  await assert.rejects(describeImages(["/tmp/card.png"], {
    stat: async () => { throw new Error("boom"); },
    readFile,
  }), /not readable: \/tmp\/card.png$/);
  await assert.rejects(describeImages(["/tmp/card.png"], {
    stat: async () => ({ size: 4 }),
    readFile,
  }), /not a file/);
  await assert.rejects(describeImages(["/tmp/card.png"], {
    stat: async () => ({ size: "nope", isFile: () => true }),
    readFile,
  }), /size is unusable/);
  await assert.rejects(describeImages(["/tmp/card.png"], {
    stat: async () => ({ size: PNG.length, isFile: () => true }),
    readFile: async () => Buffer.concat([PNG, Buffer.from([0])]),
  }), /size changed/);
  await assert.rejects(describeImages(["/tmp/card.png"], {
    stat: async () => ({ size: JPEG.length, isFile: () => true }),
    readFile: async () => JPEG,
  }), /do not look like image\/png/);
});
