import assert from "node:assert/strict";
import test from "node:test";
import { createMpSession } from "../lib/session.mjs";
import { mpAct } from "../lib/mp-dom.mjs";
import { createDocument, h } from "./dom-fixture.mjs";

function editorDocument() {
  const title = h("textarea", { placeholder: "请在这里输入标题" });
  const body = h("body", { editable: true, text: "选择图片" });
  const frame = h("iframe");
  frame.contentDocument = {
    body,
    querySelectorAll: (selector) => body.querySelectorAll(selector),
    querySelector: (selector) => body.querySelector(selector),
  };
  const imageButton = h("button", { title: "图片" }, ["图片"]);
  const file = h("input", { type: "file", accept: "image/png" });
  const save = h("button", {}, ["保存"]);
  const preview = h("button", {}, ["预览"]);
  const doc = createDocument(h("div", { text: "选择图片 保存成功 新的创作 草稿箱" }, [
    h("div", { className: "weui-desktop-account__nickname", text: "加选" }),
    title, frame, imageButton, file, save, preview,
    h("button", {}, ["新的创作"]),
    h("button", {}, ["文章"]),
    h("button", {}, ["确定"]),
    h("div", { className: "draft-title", attrs: { "data-id": "7" }, text: "题" }),
  ]), { href: "https://mp.weixin.qq.com/cgi-bin/home?t=home/index&token=secret" });
  return { doc, title, body, file };
}

function pageFor(state) {
  const page = {
    async goto() { state.gone = true; },
    async url() { return "https://mp.weixin.qq.com/"; },
    async waitForLoadState() {},
    async waitForTimeout() {},
    async evaluate(fn, arg) { return fn(arg); },
    async fill(_selector, value) { state.filled = value; state.title.value = value; },
    async setInputFiles() { state.files += 1; state.body.childNodes.push(h("img", { attrs: { src: "https://mmbiz.example/a.jpg" } })); },
    async waitForFileChooser() { return null; },
    async waitForEvent() { return state.popup || null; },
    keyboard: { async paste(payload) { state.pasted = payload; } },
    async screenshot({ path: file }) { state.shots.push(file); return file; },
  };
  return page;
}

test("replaceSlot uploads at the placeholder and reports a missing slot", async () => {
  const slot = h("p", { text: "WXIMG0" });
  const body = h("div", { className: "ProseMirror" }, [slot]);
  const rich = h("div", { className: "rich_media_content" }, [body]);
  const file = h("input", { type: "file", accept: "image/jpeg" });
  const title = h("div", { className: "ProseMirror", editable: true, attrs: { "data-placeholder": "请在这里输入标题" } });
  title.getBoundingClientRect = () => ({ width: 200, height: 30 });
  createDocument(h("div", {}, [title, rich, file]));
  let uploaded = false;
  const page = {
    async evaluate(fn, arg) { return fn(arg); },
    async setInputFiles() {
      uploaded = true;
      body.childNodes.push(h("img", { attrs: { src: "https://mmbiz.example/a.jpg" } }));
    },
    async waitForTimeout() {},
    keyboard: { async insertText(value) { title.text = value; } },
  };
  const session = createMpSession({ task: { async finish() {} }, page, timings: { attempts: 1, waitMs: 0 } });
  const titled = await session.fillTitle("正式标题");
  assert.equal(titled.via, "insertText");
  const replaced = await session.replaceSlot(0, "/absolute/path/a.jpg");
  assert.equal(uploaded, true);
  assert.equal(replaced.after, 1);
  createDocument(h("div", { text: "只有正文" }, [
    h("div", { className: "rich_media_content" }, [h("div", { className: "ProseMirror", text: "只有正文" })]),
  ]));
  await assert.rejects(() => session.replaceSlot(1, "/absolute/path/a.jpg"), /WXIMG1/);
});

test("createMpSession requires a task and a page", () => {
  assert.throws(() => createMpSession({}), /task and page/);
});

test("session fills, uploads, saves, and closes the space", async () => {
  const state = { files: 0, shots: [], title: null, body: null, popup: null };
  const built = editorDocument();
  state.title = built.title;
  state.body = built.body;
  const task = {
    spaceId: 3,
    page(label) { state.adopted = label; return pageFor(state); },
    async finish(options) { state.finish = options; },
  };
  const session = createMpSession({ task, page: pageFor(state), timings: { attempts: 2, waitMs: 0 } });
  await session.goto("https://mp.weixin.qq.com/");
  const probe = await session.probe();
  assert.equal(probe.accounts[0], "加选");
  assert.equal(probe.editorReady, true);
  await session.fillTitle("题");
  assert.equal(state.filled, "题");
  assert.equal((await session.fillOptional("set-digest", "")).skipped, true);
  assert.equal((await session.fillOptional("set-source", "https://example.com")).ok, true);
  await session.pasteHtml("<p>正文</p>", "正文");
  assert.match(state.pasted.html, /正文/);
  const uploaded = await session.uploadImage("/absolute/path/cover.jpg");
  assert.equal(uploaded.after, 1);
  assert.equal(state.files, 1);
  const cover = await session.ensureCover();
  assert.equal(cover.ok, false);
  assert.match(cover.error, /cover/);
  await session.clickSave();
  assert.equal(await session.saveConfirmed(), true);
  const drafts = await session.listDrafts();
  assert.equal(drafts[0].id, "7");
  await session.openDraft("题");
  const preview = await session.openPreview();
  assert.equal(preview.ok, true);
  const shots = await session.captureViews("/absolute/path/shots", "draft");
  assert.equal(shots.length, 3);
  await session.finish();
  assert.deepEqual(state.finish, { keep: [] });
  await session.finish();
  assert.equal(built.file.getAttribute("data-wx-article-file"), "1");
});

test("upload can use a file chooser, and a missing editor fails closed", async () => {
  createDocument(h("body", { text: "首页" }, [
    h("button", {}, ["新的创作"]),
    h("button", {}, ["文章"]),
  ]));
  const state = { chooser: 0, popup: { label: "p2", evaluate() {} } };
  const blank = {
    async evaluate(fn, arg) {
      const result = fn(arg);
      if (arg && arg.op === "click" && arg.text === "文章") {
        const title = h("textarea", { placeholder: "请在这里输入标题" });
        const body = h("div", { className: "editor-body", text: "" });
        createDocument(h("div", {}, [title, body, h("button", { title: "图片" }, ["图片"])]));
      }
      return result;
    },
    async waitForTimeout() {},
    async waitForEvent() { return state.popup; },
    keyboard: {},
  };
  const task = {
    page(label) {
      state.label = label;
      return {
        async evaluate(fn, arg) { return mpAct(arg); },
        async waitForTimeout() {},
        async waitForFileChooser() {
          state.chooser += 1;
          return { async setFiles() { state.chooser += 1; } };
        },
        keyboard: { async paste() {} },
      };
    },
    async finish() { state.finished = true; },
  };
  const session = createMpSession({ task, page: blank, timings: { attempts: 3, waitMs: 0 } });
  const opened = await session.openEditor();
  assert.equal(opened.editorReady, true);
  assert.equal(state.label, "p2");
  await assert.rejects(() => session.uploadImage("/absolute/path/a.jpg"), /did not appear|upload control|file upload/);
  await session.finish();
  assert.equal(state.finished, true);
});

test("probe and goto tolerate a dead page", async () => {
  const task = { async finish() {} };
  const page = {
    async goto() { throw new Error("navigation failed"); },
    async evaluate() { throw new Error("evaluate failed"); },
    async waitForLoadState() { throw new Error("idle"); },
  };
  const session = createMpSession({ task, page, timings: { attempts: 1, waitMs: 0 } });
  await assert.rejects(() => session.goto("https://mp.weixin.qq.com/"), /navigation failed/);
  const probe = await session.probe();
  assert.equal(probe.loggedIn, false);
  assert.match(probe.error, /evaluate failed/);
  const quiet = createMpSession({
    task,
    page: {
      async goto() {},
      async evaluate(fn, arg) { return fn(arg); },
    },
    timings: { waitMs: 0, attempts: 1 },
  });
  createDocument(h("div", { className: "editor-body", editable: true, text: "正文" }));
  await quiet.goto("https://mp.weixin.qq.com/");
  assert.equal((await quiet.captureViews("", "draft")).length, 0);
  await assert.rejects(() => quiet.pasteHtml("<p>a</p>", "a"), /paste/);
  await assert.rejects(() => quiet.clickSave(), /保存/);
});
