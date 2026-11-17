import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { creatorAct } from "../lib/creator-dom.mjs";
import { createCreatorSession } from "../lib/session.mjs";
import { executePost, performPublish } from "../lib/publish-flow.mjs";
import { runCli } from "../lib/launch.mjs";
import {
  IMAGE_TEXT_COMMAND,
  IMAGE_TEXT_MAX_IMAGES,
  RESULT_TAG,
  imageExtensionOk,
  imageUploadFailed,
  imageUploadPending,
  isImageAccept,
  parseImagePaths,
  parsePostArgs,
  planOf,
  postCommand,
  publishButtonRef,
  validatePostInput,
} from "../lib/pure.mjs";
import { createDocument, h } from "./dom-fixture.mjs";

const IMAGE = "/absolute/path/to/wallpaper-1.jpg";

function imageFiles(count = 2) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "xhs-image-"));
  const images = [];
  for (let i = 1; i <= count; i += 1) {
    const file = path.join(dir, `wallpaper-${i}.jpg`);
    fs.writeFileSync(file, "jpg");
    images.push(file);
  }
  return { dir, images };
}

function capture() {
  let text = "";
  return { text: () => text, write(chunk) { text += chunk; } };
}

function childWith({ stdout = "", stderr = "", code = 0, error } = {}) {
  const child = new EventEmitter();
  child.stdout = new EventEmitter();
  child.stderr = new EventEmitter();
  queueMicrotask(() => {
    if (error) {
      child.emit("error", error);
      return;
    }
    if (stdout) child.stdout.emit("data", stdout);
    if (stderr) child.stderr.emit("data", stderr);
    child.emit("close", code);
  });
  return child;
}

test("parseImagePaths splits, trims, and dedupes the comma list", () => {
  assert.deepEqual(parseImagePaths("/a/1.jpg, /a/2.jpg ,/a/1.jpg,"), ["/a/1.jpg", "/a/2.jpg"]);
  assert.deepEqual(parseImagePaths(""), []);
  assert.deepEqual(parseImagePaths("/a/1.webp"), ["/a/1.webp"]);
});

test("isImageAccept separates the image input from the video input", () => {
  assert.equal(isImageAccept(".jpg,.jpeg,.png,.webp"), true);
  assert.equal(isImageAccept("image/*"), true);
  assert.equal(isImageAccept(".mp4,.mov,.flv,.f4v,.mkv,.rm,.rmvb,.m4v,.mpg,.mpeg,.ts"), false);
  assert.equal(isImageAccept(""), false);
  assert.equal(imageExtensionOk("/a/b.JPG"), true);
  assert.equal(imageExtensionOk("/a/b.gif"), false);
});

test("argument parsers require video or images, never both", () => {
  const images = parsePostArgs(["--images", "/a/1.jpg,/a/2.jpg", "--title", "标题", "--desc", "正文"]);
  assert.deepEqual(images.images, ["/a/1.jpg", "/a/2.jpg"]);
  assert.equal(images.video, "");
  assert.throws(() => parsePostArgs(["--title", "标题", "--desc", "正文"]), /Missing --video or --images/);
  assert.throws(() => parsePostArgs([
    "--video", "/a/v.mp4", "--images", "/a/1.jpg", "--title", "标题", "--desc", "正文",
  ]), /mutually exclusive/);
  assert.throws(() => parsePostArgs(["--images", ",", "--title", "标题", "--desc", "正文"]), /Missing --video or --images/);
  assert.equal(postCommand({ images: [IMAGE] }), IMAGE_TEXT_COMMAND);
  assert.equal(postCommand({ video: "/a/v.mp4" }), "post-video");
});

test("image validation checks every path and rejects cover and overflow", () => {
  const { dir, images } = imageFiles(2);
  const ok = validatePostInput({ images, title: "标题", desc: "正文" }, { exists: fs.existsSync, stat: fs.statSync });
  assert.equal(ok.ok, true);
  assert.deepEqual(ok.images, images);
  assert.equal(ok.body, "正文");
  const relative = validatePostInput({ images: ["wallpaper-1.jpg"], title: "标题", desc: "正文" });
  assert.match(relative.error, /absolute paths/);
  const badExt = validatePostInput({ images: [`${dir}/x.gif`], title: "标题", desc: "正文" });
  assert.match(badExt.error, /jpg, .jpeg, .png, or .webp/);
  const missing = validatePostInput({
    images: [images[0], path.join(dir, "gone.jpg")], title: "标题", desc: "正文",
  }, { exists: fs.existsSync, stat: fs.statSync });
  assert.match(missing.error, /gone.jpg/);
  const empty = validatePostInput({
    images: [path.join(dir, "empty.jpg")], title: "标题", desc: "正文",
  }, {
    exists: fs.existsSync,
    stat: (file) => { fs.writeFileSync(file, ""); return fs.statSync(file); },
  });
  assert.match(empty.error, /empty/);
  const overflow = validatePostInput({
    images: Array.from({ length: IMAGE_TEXT_MAX_IMAGES + 1 }, (_, i) => `${dir}/${i}.jpg`),
    title: "标题", desc: "正文",
  });
  assert.match(overflow.error, /at most 18/);
  const withCover = validatePostInput({ images, title: "标题", desc: "正文", cover: `${dir}/cover.png` });
  assert.match(withCover.error, /--cover applies to video notes only/);
  const both = validatePostInput({
    video: "/absolute/path/to/video.mp4", images, title: "标题", desc: "正文",
  });
  assert.match(both.error, /mutually exclusive/);
  assert.match(validatePostInput({ images, title: "", desc: "正文" }).error, /Missing --title/);
  assert.equal(imageUploadFailed("图片过大 请压缩"), true);
  assert.equal(imageUploadFailed("正常文案"), false);
  assert.equal(imageUploadPending("上传中 32%"), true);
  assert.equal(imageUploadPending("已上传 3 张"), false);
});

test("image plan lists images and keeps the first image as cover", () => {
  const images = [IMAGE, "/absolute/path/to/wallpaper-2.jpg"];
  const plan = planOf({ images, title: "标题", desc: "正文", command: IMAGE_TEXT_COMMAND });
  assert.equal(plan.note_type, "image-text");
  assert.deepEqual(plan.images, images);
  assert.equal(plan.image_count, 2);
  assert.equal(plan.cover, null);
  assert.equal(plan.cover_mode, "first-image");
  assert.equal(plan.cover_selector, null);
  assert.match(plan.cover_note, /first image/);
  const videoPlan = planOf({ video: "/a/v.mp4", title: "标题", desc: "正文" });
  assert.equal(videoPlan.note_type, "video");
  assert.equal(videoPlan.images, undefined);
});

test("creatorAct switches to 上传图文 and finds the image input", () => {
  const video = h("input", { className: "upload-input", type: "file", accept: ".mp4,.mov" });
  const tab = h("span", { className: "title" }, ["上传图文"]);
  createDocument(h("body", {}, [video, h("div", {}, [tab])]), {
    href: "https://creator.xiaohongshu.com/publish/publish",
  });
  const clicked = creatorAct({ op: "image-tab" });
  assert.equal(clicked.ok, true);
  assert.equal(tab.clicked, 1);
  assert.match(clicked.href, /publish\/publish/);
  const imageInput = h("input", { className: "upload-input", type: "file", accept: ".jpg,.jpeg,.png,.webp" });
  imageInput.multiple = true;
  createDocument(h("body", {}, [video, imageInput]));
  const found = creatorAct({ op: "image-input" });
  assert.equal(found.ok, true);
  assert.match(found.accept, /\.webp/);
  assert.equal(found.multiple, true);
  assert.equal(imageInput.getAttribute("data-xhs-image-input"), "1");
  assert.equal(video.getAttribute("data-xhs-image-input"), null);
  createDocument(h("body", {}, [video]));
  assert.match(creatorAct({ op: "image-input" }).error, /image upload input not found/);
  createDocument(h("body"));
  assert.match(creatorAct({ op: "image-tab" }).error, /上传图文/);
});

test("creatorAct image state counts upload thumbnails, pending, and failures", () => {
  const thumbs = [
    h("img", { attrs: { src: "blob:https://creator.xiaohongshu.com/aa-1" } }),
    h("img", { attrs: { src: "https://sns-img-qh.xhscdn.com/1040g008.jpg" } }),
    h("img", { attrs: { src: "https://p.example.com/avatar.jpg" } }),
  ];
  createDocument(h("body", { text: "图片 2/18" }, thumbs));
  const ready = creatorAct({ op: "image-state" });
  assert.equal(ready.uploadThumbs, 2);
  assert.equal(ready.counter, 2);
  assert.equal(ready.pending, false);
  assert.equal(ready.failed, false);
  createDocument(h("body", { text: "上传中 40% 图片 1/18" }, [thumbs[0]]));
  const pending = creatorAct({ op: "image-state" });
  assert.equal(pending.pending, true);
  assert.equal(pending.uploadThumbs, 1);
  createDocument(h("body", { text: "上传失败 请重试" }));
  assert.equal(creatorAct({ op: "image-state" }).failed, true);
});

test("serialized creatorAct keeps the image ops", () => {
  const isolated = new Function(`return (${creatorAct.toString()})`)();
  const imageInput = h("input", { className: "upload-input", type: "file", accept: ".jpg,.jpeg,.png,.webp" });
  imageInput.multiple = true;
  const tab = h("span", { className: "title" }, ["上传图文"]);
  createDocument(h("body", {}, [tab, imageInput]), {
    href: "https://creator.xiaohongshu.com/publish/publish?source=official",
  });
  assert.equal(isolated({ op: "image-tab" }).ok, true);
  const found = isolated({ op: "image-input" });
  assert.equal(found.ok, true);
  assert.equal(found.multiple, true);
  const state = isolated({ op: "image-state" });
  assert.equal(state.uploadThumbs, 0);
  assert.equal(state.pending, false);
});

test("publishButtonRef parses the snapshot button and skips 发布笔记 and 暂存离开", () => {
  const snapshot = [
    "root",
    "  container",
    '    text "发布笔记"',
    "    button [ref=11]",
    '      text "暂存离开"',
    "    button [ref=26]",
    '      text "发布"',
    "  container",
    '    text "笔记预览"',
    "  tooltip [ref=28]",
    '      text "发布笔记"',
  ].join("\n");
  assert.equal(publishButtonRef(snapshot), 26);
  assert.equal(publishButtonRef('button [ref=3]\n  text "发布笔记"'), null);
  assert.equal(publishButtonRef('button [ref=3]\n  text "暂存离开"\ntext "发布"'), null);
  assert.equal(publishButtonRef(""), null);
  assert.equal(publishButtonRef('text "发布"'), null);
});

test("clickPublishImage clicks the snapshot ref and falls back to the role selector", async () => {
  const task = { spaceId: 9, async finish() {}, async handOff() {} };
  const snapshot = [
    "  container",
    '    text "发布笔记"',
    "  button [ref=26]",
    '    text "发布"',
  ].join("\n");
  const clicks = [];
  const tab = {
    async snapshot() { return snapshot; },
    async click(selector) { clicks.push(selector); },
  };
  const session = createCreatorSession({ task, page: tab });
  const result = await session.clickPublish("image");
  assert.equal(result.via, "ref=26");
  assert.deepEqual(clicks, ["ref=26"]);
  const fallbackTab = {
    async snapshot() { return 'button [ref=1]\n  text "发布笔记"'; },
    async click(selector) { clicks.push(selector); },
  };
  const fallback = createCreatorSession({ task, page: fallbackTab });
  const viaLoc = await fallback.clickPublish("image");
  assert.equal(viaLoc.via, "loc=role:button");
  assert.deepEqual(clicks, ["ref=26", "loc=role:button[name='发布']"]);
  const noSnapshot = createCreatorSession({ task, page: {} });
  await assert.rejects(() => noSnapshot.clickPublish("image"), /snapshot is required/);
});

function fakePage(extra = {}) {
  const waits = [];
  return {
    waits,
    async url() { return extra.url || "https://creator.xiaohongshu.com/publish/publish"; },
    async title() { return extra.title || "发布笔记"; },
    async goto() {},
    async waitForLoadState() {},
    async waitForTimeout(ms) { waits.push(ms); },
    async evaluate(fn, payload) {
      if (extra.evaluateError) throw new Error(extra.evaluateError);
      return fn(payload);
    },
    async setInputFiles(selector, file) { extra.files.push({ selector, file }); },
    async fill() {},
    keyboard: { async insertText() {} },
    mouse: null,
  };
}

test("session image methods switch, refuse video accepts, and wait for thumbnails", async () => {
  const task = { spaceId: 9, async finish() {}, async handOff() {} };
  const files = [];
  const tab = h("span", { className: "title" }, ["上传图文"]);
  const imageInput = h("input", { className: "upload-input", type: "file", accept: ".jpg,.jpeg,.png,.webp" });
  imageInput.multiple = true;
  createDocument(h("body", {}, [tab, imageInput]));
  const tab2 = h("span", { className: "title" }, ["上传图文"]);
  const input2 = h("input", { className: "upload-input", type: "file", accept: ".jpg,.jpeg,.png,.webp" });
  input2.multiple = true;
  createDocument(h("body", {}, [tab2, input2]));
  const host = fakePage({ files });
  const session = createCreatorSession({ task, page: host, timings: { uploadAttempts: 3, imageTabAttempts: 2, waitMs: 1 } });
  const switched = await session.switchToImageTab();
  assert.equal(switched.input.ok, true);
  assert.equal(tab2.clicked, 1);
  const uploaded = await session.setImageFiles(["/a/1.jpg", "/a/2.jpg"]);
  assert.equal(uploaded.files, 2);
  assert.deepEqual(files[0].file, ["/a/1.jpg", "/a/2.jpg"]);
  assert.match(files[0].selector, /data-xhs-image-input/);

  const videoOnly = h("input", { className: "upload-input", type: "file", accept: ".mp4,.mov" });
  createDocument(h("body", {}, [videoOnly]));
  const videoSession = createCreatorSession({ task, page: fakePage({}), timings: { imageTabAttempts: 1, waitMs: 1 } });
  await assert.rejects(() => videoSession.switchToImageTab(), /上传图文 tab not found/);
  await assert.rejects(() => videoSession.setImageFiles(["/a/1.jpg"]), /not found/);
  const mixedTab = h("span", { className: "title" }, ["上传图文"]);
  const mixedInput = h("input", { className: "upload-input", type: "file", accept: ".mp4" });
  createDocument(h("body", {}, [mixedTab, mixedInput]));
  const mixedSession = createCreatorSession({ task, page: fakePage({}), timings: { imageTabAttempts: 1, waitMs: 1 } });
  await assert.rejects(() => mixedSession.switchToImageTab(), /did not appear/);

  const thumbs = [
    h("img", { attrs: { src: "blob:x-1" } }),
    h("img", { attrs: { src: "blob:x-2" } }),
  ];
  createDocument(h("body", { text: "图片 2/18" }, thumbs));
  const ready = await session.waitImagesReady(2);
  assert.equal(ready.ok, true);
  createDocument(h("body", { text: "上传失败 请重试" }, thumbs));
  await assert.rejects(() => session.waitImagesReady(2), /upload failed/);
  createDocument(h("body", { text: "上传中 90%" }, [thumbs[0]]));
  const strict = createCreatorSession({ task, page: host, timings: { uploadAttempts: 2, waitMs: 1 } });
  await assert.rejects(() => strict.waitImagesReady(2), /did not settle/);
});

function publishSession(state = {}) {
  const current = {
    detect: {
      url: "https://creator.xiaohongshu.com/publish/publish",
      title: "创作服务平台",
      text: "发布笔记 图片 2/18",
      nickname: "听懂AI",
      creatorChrome: true,
      loginWall: false,
    },
    note: { ok: true, noteId: "6aeae169000000000e00c4ad", url: "https://www.xiaohongshu.com/explore/6aeae169000000000e00c4ad" },
    imageTabThrows: "",
    setImageThrows: "",
    waitImagesThrows: "",
    ...state,
  };
  const calls = [];
  const api = {
    calls,
    spaceId: 80,
    async goto(url) { calls.push(["goto", url]); },
    async detect() { calls.push(["detect"]); return current.detect; },
    async switchToImageTab() {
      calls.push(["switchToImageTab"]);
      if (current.imageTabThrows) throw new Error(current.imageTabThrows);
      return { clicked: { ok: true }, input: { ok: true, accept: ".jpg,.jpeg,.png,.webp", multiple: true } };
    },
    async setImageFiles(files) {
      calls.push(["setImageFiles", files.length]);
      if (current.setImageThrows) throw new Error(current.setImageThrows);
      return { ok: true, files: files.length };
    },
    async waitImagesReady(count) {
      calls.push(["waitImagesReady", count]);
      if (current.waitImagesThrows) throw new Error(current.waitImagesThrows);
      return { ok: true, state: { uploadThumbs: count } };
    },
    async setVideo(file) { calls.push(["setVideo", file]); },
    async waitUpload() { calls.push(["waitUpload"]); },
    async fillTitle(value) { calls.push(["fillTitle", value]); },
    async fillBody() { calls.push(["fillBody"]); },
    async clickPublish(mode) { calls.push(["clickPublish", mode]); },
    async waitSuccess() { calls.push(["waitSuccess"]); return { url: "https://creator.xiaohongshu.com/publish/success" }; },
    async readNote() { calls.push(["readNote"]); return current.note; },
    async probe() { calls.push(["probe"]); return current.detect; },
    async handOff() { calls.push(["handOff"]); },
    async finish() { calls.push(["finish"]); },
  };
  return { api, current, calls };
}

test("image-text publish switches tabs, uploads, and never touches the video path", async () => {
  const { images } = imageFiles(2);
  const live = publishSession();
  const result = await performPublish({ images, title: "标题", desc: "正文", yes: true }, live.api, {
    ok: true, images, title: "标题", desc: "正文", topics: "", body: "正文",
  });
  assert.equal(result.exitCode, 0);
  assert.equal(result.published, true);
  assert.equal(result.image_count, 2);
  assert.equal(result.cover_scope, "first-image");
  assert.equal(live.calls.some((call) => call[0] === "setVideo"), false);
  assert.equal(live.calls.some((call) => call[0] === "waitUpload"), false);
  assert.equal(live.calls.some((call) => call[0] === "setMainCover"), false);
  assert.deepEqual(live.calls.find((call) => call[0] === "setImageFiles"), ["setImageFiles", 2]);
  assert.deepEqual(live.calls.find((call) => call[0] === "clickPublish"), ["clickPublish", "image"]);

  const tabFail = publishSession({ imageTabThrows: "上传图文 tab not found" });
  const stopped = await performPublish({ images, title: "标题", desc: "正文", yes: true }, tabFail.api, {
    ok: true, images, title: "标题", desc: "正文", body: "正文",
  });
  assert.equal(stopped.exitCode, 1);
  assert.equal(stopped.uploaded, false);
  assert.equal(tabFail.calls.some((call) => call[0] === "clickPublish"), false);

  const uploadFail = publishSession({ waitImagesThrows: "image upload failed on the page" });
  const failed = await performPublish({ images, title: "标题", desc: "正文", yes: true }, uploadFail.api, {
    ok: true, images, title: "标题", desc: "正文", body: "正文",
  });
  assert.equal(failed.exitCode, 1);
  assert.equal(failed.clicked_publish, false);
});

test("executePost dry-run and --yes report the image-text command", async () => {
  const { images } = imageFiles(2);
  const dry = publishSession();
  const opens = [];
  const summary = await executePost({
    images, title: "标题", desc: "正文", expectAccount: "听懂AI",
  }, { browser: { async open(opts) { opens.push(opts); return dry.api; } } });
  assert.equal(summary.command, IMAGE_TEXT_COMMAND);
  assert.equal(summary.exitCode, 3);
  assert.equal(summary.plan.note_type, "image-text");
  assert.deepEqual(summary.plan.images, images);
  assert.equal(dry.calls.some((call) => call[0] === "switchToImageTab"), false);

  const live = publishSession();
  const yes = await executePost({ images, title: "标题", desc: "正文", yes: true }, { browser: { async open() { return live.api; } } });
  assert.equal(yes.exitCode, 0);
  assert.equal(yes.published, true);
  assert.match(yes.url, /explore\/6aeae169/);

  const badCover = await executePost({ images, title: "标题", desc: "正文", cover: "/absolute/cover.png" }, { browser: { async open() { return publishSession().api; } } });
  assert.equal(badCover.exitCode, 1);
  assert.match(badCover.error, /--cover applies to video notes only/);
});

test("runCli post-image-text validates before spawning and forwards the plan", async () => {
  const { dir, images } = imageFiles(2);
  const noSpawn = { spawn() { throw new Error("should not spawn"); } };
  const both = { stdout: capture(), stderr: capture(), whichEgo: () => "ego-browser", mkdtemp: async () => "/tmp/t", fs: { writeFile: async () => {}, rm: async () => {} }, existsSync: () => true, statSync: () => ({ size: 8, isFile: () => true }), ...noSpawn };
  assert.equal(await runCli("postImage", [
    "--images", images.join(","), "--video", "/absolute/path/to/video.mp4", "--title", "标题", "--desc", "正文",
  ], both), 1);
  assert.match(both.stderr.text(), /mutually exclusive/);

  const missing = {
    stdout: capture(), stderr: capture(), whichEgo: () => "ego-browser",
    mkdtemp: async () => "/tmp/t", fs: { writeFile: async () => {}, rm: async () => {} },
    existsSync: fs.existsSync, statSync: fs.statSync,
    spawn() { throw new Error("should not spawn"); },
  };
  assert.equal(await runCli("postImage", [
    "--images", `${images[0]},${path.join(dir, "gone.jpg")}`, "--title", "标题", "--desc", "正文",
  ], missing), 1);
  assert.match(missing.stdout.text(), /gone\.jpg/);

  let entry = "";
  const planned = {
    stdout: capture(), stderr: capture(), whichEgo: () => "ego-browser",
    mkdtemp: async () => "/tmp/t",
    fs: { writeFile: async (_file, source) => { entry = source; }, rm: async () => {} },
    existsSync: () => true, statSync: () => ({ size: 8, isFile: () => true }),
    spawn() {
      return childWith({
        stdout: `${RESULT_TAG}${JSON.stringify({ exitCode: 3, confirmation_required: true, plan: { note_type: "image-text", image_count: 2 } })}\n`,
      });
    },
  };
  const code = await runCli("postImage", [
    "--images", images.join(","), "--title", "标题", "--desc", "正文", "--expect-account", "听懂AI",
  ], planned);
  assert.equal(code, 3);
  assert.match(planned.stdout.text(), /image-text/);
  assert.match(entry, /executePost/);
  assert.match(entry, new RegExp(images[0].replace(/\//g, "\\/")));
  assert.match(entry, /"images":\[/);
  fs.rmSync(dir, { recursive: true, force: true });
});
