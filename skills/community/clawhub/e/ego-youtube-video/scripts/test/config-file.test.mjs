import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { PUBLISH_CONFIG_PATH } from "../lib/pure.mjs";
import { readConfigSync, writePublishConfigSync } from "../lib/config-file.mjs";

function memoryFs(seed = {}) {
  const files = new Map(Object.entries(seed));
  return {
    files,
    mkdirCalled: [],
    existsSync(file) {
      return files.has(file);
    },
    statSync(file) {
      if (!files.has(file)) throw new Error(`missing ${file}`);
      return { size: files.get(file).size };
    },
    mkdirSync(dir) {
      this.mkdirCalled.push(dir);
    },
    writeFileSync(file, data) {
      const prev = files.get(file);
      files.set(file, { data, size: prev ? prev.size : Buffer.byteLength(data) });
    },
    readFileSync(file) {
      if (!files.has(file)) throw new Error(`missing ${file}`);
      return files.get(file).data;
    },
  };
}

const pathMod = {
  resolve(file) {
    return file.startsWith("/") ? file : `/tmp/${file}`;
  },
};

test("writePublishConfigSync resolves the video and keeps visibility private", () => {
  const io = memoryFs({
    "/absolute/path/to/video.mp4": { size: 2097152, data: "" },
  });
  const written = writePublishConfigSync(
    ["/absolute/path/to/video.mp4", "  Title  ", "Description"],
    { fs: io, path: pathMod },
  );
  assert.equal(written.file, PUBLISH_CONFIG_PATH);
  assert.equal(written.config.video, "/absolute/path/to/video.mp4");
  assert.equal(written.config.title, "Title");
  assert.equal(written.config.description, "Description");
  assert.equal(written.config.visibility, "private");
  assert.equal(written.config.madeForKids, false);
  assert.equal(written.config.keep, false);
  assert.equal(written.config.spaceId, null);
  assert.equal(written.config.thumbnail, "");
  assert.deepEqual(written.config.tags, []);
  assert.equal(written.sizeMB, 2);
  assert.deepEqual(io.mkdirCalled, ["/tmp"]);
  assert.deepEqual(readConfigSync(written.file, io), written.config);
});

test("flags resolve a relative thumbnail and a missing file fails before write", () => {
  const io = memoryFs();
  const written = writePublishConfigSync(
    ["clip.mp4", "Title", "--visibility", "public", "--made-for-kids", "yes", "--tags", "a,b", "--space-id", "8", "--keep"],
    {
      fs: io,
      path: pathMod,
      exists: () => true,
      sizeBytes: 100,
      file: "/tmp/unit-youtube.json",
    },
  );
  assert.equal(written.config.video, "/tmp/clip.mp4");
  assert.equal(written.config.visibility, "public");
  assert.equal(written.config.madeForKids, true);
  assert.equal(written.config.spaceId, 8);
  assert.equal(written.config.keep, true);
  assert.deepEqual(written.config.tags, ["a", "b"]);

  const missing = memoryFs();
  assert.throws(
    () => writePublishConfigSync(
      ["/absolute/path/to/missing.mp4", "Title"],
      { fs: missing, path: pathMod, file: "/tmp/should-not-write.json" },
    ),
    /视频文件不存在/,
  );
  assert.equal(missing.files.size, 0);

  const thumb = memoryFs({
    "/absolute/path/to/video.mp4": { size: 10, data: "" },
  });
  assert.throws(
    () => writePublishConfigSync(
      ["/absolute/path/to/video.mp4", "Title", "--thumbnail", "/absolute/path/to/thumb.jpg"],
      { fs: thumb, path: pathMod, file: "/tmp/thumb.json" },
    ),
    /缩略图不存在/,
  );
  assert.throws(
    () => writePublishConfigSync(["/absolute/path/to/video.mp4", "   "], {
      fs: memoryFs({ "/absolute/path/to/video.mp4": { size: 10, data: "" } }),
      path: pathMod,
    }),
    /usage/,
  );
  assert.throws(() => readConfigSync("/tmp/nope.json", memoryFs()), /missing/);
  assert.throws(() => readConfigSync("/tmp/bad.json", { readFileSync: () => "{" }), SyntaxError);
});

test("the default filesystem writes a real temp config", async () => {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "yt-skill-"));
  const video = path.join(dir, "clip.mp4");
  const thumbnail = path.join(dir, "thumb.jpg");
  const file = path.join(dir, "cfg.json");
  await fs.writeFile(video, Buffer.alloc(8));
  await fs.writeFile(thumbnail, Buffer.alloc(4));
  try {
    const written = writePublishConfigSync(
      [video, "Local title", "Local description", "--thumbnail", thumbnail, "--visibility", "unlisted"],
      { file },
    );
    assert.equal(written.config.visibility, "unlisted");
    assert.equal(written.config.thumbnail, thumbnail);
    assert.equal(readConfigSync(file).title, "Local title");
  } finally {
    await fs.rm(dir, { recursive: true, force: true });
  }
});
