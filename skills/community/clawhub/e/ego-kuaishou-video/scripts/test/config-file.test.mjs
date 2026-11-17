import test from "node:test";
import assert from "node:assert/strict";
import {
  COMMENT_CONFIG_PATH,
  PUBLISH_CONFIG_PATH,
} from "../lib/pure.mjs";
import {
  readConfigSync,
  writeCommentConfigSync,
  writePublishConfigSync,
} from "../lib/config-file.mjs";

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

test("writePublishConfigSync resolves the video, keeps tags, and round-trips", () => {
  const io = memoryFs({
    "/absolute/path/to/video.mp4": { size: 2097152, data: "" },
  });
  const written = writePublishConfigSync(
    ["/absolute/path/to/video.mp4", "描述 #话题1 #话题2", "4", "1"],
    { fs: io, path: pathMod },
  );
  assert.equal(written.file, PUBLISH_CONFIG_PATH);
  assert.equal(written.config.video, "/absolute/path/to/video.mp4");
  assert.equal(written.config.desc, "描述 #话题1 #话题2");
  assert.equal(written.config.spaceId, 4);
  assert.equal(written.config.keep, true);
  assert.equal(written.sizeMB, 2);
  assert.deepEqual(io.mkdirCalled, ["/tmp"]);
  assert.deepEqual(readConfigSync(written.file, io), written.config);
});

test("a relative video path is resolved and a missing file fails before write", () => {
  const io = memoryFs();
  const written = writePublishConfigSync(
    ["clip.mp4", "描述"],
    {
      fs: io,
      path: pathMod,
      exists: () => true,
      sizeBytes: 100,
      file: "/tmp/unit-publish.json",
    },
  );
  assert.equal(written.config.video, "/tmp/clip.mp4");
  assert.equal(written.config.keep, false);
  assert.equal(written.config.spaceId, null);

  const missing = memoryFs();
  assert.throws(
    () => writePublishConfigSync(
      ["/absolute/path/to/missing.mp4", "描述"],
      { fs: missing, path: pathMod, file: "/tmp/should-not-write.json" },
    ),
    /视频文件不存在/,
  );
  assert.equal(missing.files.size, 0);

  assert.throws(
    () => writePublishConfigSync(
      ["/absolute/path/to/video.mp4", "   "],
      {
        fs: memoryFs({ "/absolute/path/to/video.mp4": { size: 10, data: "" } }),
        path: pathMod,
        file: "/tmp/blank-desc.json",
      },
    ),
    /描述不能为空/,
  );
});

test("writeCommentConfigSync stores the hint and rejects an empty comment", () => {
  const io = memoryFs();
  const written = writeCommentConfigSync(
    ["这反应也太真实了", "真实", "8", "1"],
    { fs: io },
  );
  assert.equal(written.file, COMMENT_CONFIG_PATH);
  assert.equal(written.config.comment, "这反应也太真实了");
  assert.equal(written.config.titleHint, "真实");
  assert.equal(written.config.spaceId, 8);
  assert.equal(written.config.keep, true);
  assert.deepEqual(readConfigSync(COMMENT_CONFIG_PATH, io), written.config);

  assert.throws(() => writeCommentConfigSync(["  "], { fs: memoryFs() }), /评论内容不能为空/);
  assert.throws(() => readConfigSync("/tmp/nope.json", memoryFs()), /missing/);
  assert.throws(() => readConfigSync("/tmp/bad.json", {
    readFileSync: () => "{",
  }), SyntaxError);
});
