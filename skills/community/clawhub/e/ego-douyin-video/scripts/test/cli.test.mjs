import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const scripts = fileURLToPath(new URL("../", import.meta.url));
const publishSh = path.join(scripts, "publish.sh");
const checkLogin = path.join(scripts, "check-login.mjs");
const runEgo = path.join(scripts, "run-ego-module.mjs");
const writeCfg = path.join(scripts, "write-publish-config.mjs");
const publishJs = path.join(scripts, "publish.js");

test("publish.sh rejects a missing file before ego", () => {
  const res = spawnSync("bash", [publishSh, "/absolute/path/to/missing.mp4", "标题", "简介"], { encoding: "utf8" });
  assert.equal(res.status, 1);
  assert.match(res.stderr, /视频文件不存在/);
});

test("check-login help and unknown args do not need a browser", () => {
  const help = spawnSync(process.execPath, [checkLogin, "--help"], { encoding: "utf8" });
  assert.equal(help.status, 0);
  assert.match(help.stdout, /douyin-video/);
  assert.match(help.stdout, /works better/);
  assert.match(help.stdout, /yt-dlp/);
  const bad = spawnSync(process.execPath, [checkLogin, "--nope"], { encoding: "utf8" });
  assert.equal(bad.status, 2);
  assert.match(bad.stderr, /Unknown arg/);
});

test("run-ego-module without a script prints usage", () => {
  const res = spawnSync(process.execPath, [runEgo], { encoding: "utf8" });
  assert.equal(res.status, 1);
  assert.match(res.stderr, /usage/);
});

test("write-publish-config writes the temp json and publish.js refuses to run outside ego", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "dy-cli-"));
  const video = path.join(dir, "clip.mp4");
  const config = "/tmp/douyin-video-publish.json";
  fs.writeFileSync(video, Buffer.alloc(4));
  try {
    const wrote = spawnSync(process.execPath, [writeCfg, video, "CLI 标题", "简介 #话题", "", "0"], { encoding: "utf8" });
    assert.equal(wrote.status, 0);
    assert.match(wrote.stdout, /douyin-video-publish\.json/);
    const saved = JSON.parse(fs.readFileSync(config, "utf8"));
    assert.equal(saved.title, "CLI 标题");
    assert.equal(saved.desc, "简介 #话题");
    assert.equal(saved.spaceId, null);
    assert.equal(saved.keep, false);
    assert.equal(saved.video, video);
  } finally {
    fs.rmSync(config, { force: true });
    fs.rmSync(dir, { recursive: true, force: true });
  }

  const direct = spawnSync(process.execPath, [publishJs], { encoding: "utf8" });
  assert.equal(direct.status, 1);
  assert.match(direct.stderr, /配置文件不存在|publish\.sh/);
});
