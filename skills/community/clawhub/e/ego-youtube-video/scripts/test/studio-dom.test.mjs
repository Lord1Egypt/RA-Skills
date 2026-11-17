import assert from "node:assert/strict";
import test from "node:test";
import { studioAct } from "../lib/studio-dom.mjs";
import { El, mountDocument, textbox } from "./dom-fixture.mjs";

function withDoc(built, fn) {
  const prevDoc = globalThis.document;
  const prevLoc = globalThis.location;
  globalThis.document = built.doc;
  globalThis.location = built.location;
  try {
    return fn();
  } finally {
    globalThis.document = prevDoc;
    globalThis.location = prevLoc;
  }
}

test("studioAct refuses to run without a document and ignores a missing op", () => {
  const prev = globalThis.document;
  delete globalThis.document;
  try {
    assert.equal(studioAct({ op: "probe" }).ok, false);
  } finally {
    globalThis.document = prev;
  }
  const built = mountDocument({ bodyText: "YouTube Studio\nAnalytics", cookie: "LOGIN_INFO=1", title: "Studio" });
  const probed = withDoc(built, () => studioAct());
  assert.equal(probed.op, "probe");
  assert.match(probed.text, /YouTube Studio/);
  assert.equal(probed.cookie, "LOGIN_INFO=1");
  assert.equal(withDoc(built, () => studioAct({ op: "nope" })).ok, false);
});

test("fill writes shadow textboxes, and a noop execCommand falls back to textContent", () => {
  const built = mountDocument({
    children: [textbox("title-textarea"), textbox("description-textarea")],
    execCommand: "noop",
  });
  const filled = withDoc(built, () => studioAct({
    op: "fill",
    title: "Hello",
    description: "About the video",
  }));
  assert.equal(filled.ok, true);
  assert.equal(filled.title, "Hello");
  assert.equal(filled.description, "About the video");

  const emptyDesc = withDoc(built, () => studioAct({ op: "fill", title: "Only title", description: "  " }));
  assert.equal(emptyDesc.ok, true);
  assert.equal(emptyDesc.description, "");
});

test("fill reports a missing title or description box, and execCommand errors still write", () => {
  const noTitle = mountDocument({ children: [] });
  assert.match(withDoc(noTitle, () => studioAct({ op: "fill", title: "T", description: "" })).error, /标题/);

  const noDesc = mountDocument({ children: [textbox("title-textarea")], execCommand: "throw" });
  const missing = withDoc(noDesc, () => studioAct({ op: "fill", title: "T", description: "Body" }));
  assert.match(missing.error, /简介/);
  assert.equal(missing.title, "T");
});

test("upload entry, Chinese menu text, and a missing menu", () => {
  const closed = mountDocument({
    children: [new El("ytcp-button", { id: "create-icon", text: "创建" })],
  });
  const entry = withDoc(closed, () => studioAct({ op: "upload-entry" }));
  assert.equal(entry.hasCreate, true);
  assert.equal(entry.hasSelectFiles, false);
  assert.equal(entry.hasUploadItem, false);
  assert.match(withDoc(closed, () => studioAct({ op: "click-upload-menu" })).error, /上传视频/);

  let via = "";
  const item = new El("tp-yt-paper-item", {
    text: "上传视频",
    onClick() { via = "text"; },
  });
  const open = mountDocument({
    children: [
      item,
      new El("button", { id: "select-files-button", text: "选择文件" }),
    ],
  });
  const menu = withDoc(open, () => studioAct({ op: "click-upload-menu" }));
  assert.equal(menu.ok, true);
  assert.equal(menu.via, "text");
  assert.equal(via, "text");
  assert.equal(withDoc(open, () => studioAct({ op: "upload-entry" })).hasSelectFiles, true);

  const byId = mountDocument({
    children: [new El("tp-yt-paper-item", { attrs: { "test-id": "upload" }, text: "Upload" })],
  });
  assert.equal(withDoc(byId, () => studioAct({ op: "click-upload-menu" })).via, "test-id");
});

test("tags open Show more, commit chips, and fail when the field never appears", () => {
  const input = new El("input", { id: "text-input" });
  const container = new El("ytcp-form-input-container", { id: "tags-container", children: [input] });
  const toggle = new El("button", {
    text: "显示更多",
    onClick(button) {
      const body = button.owner.body;
      body.children.push(container);
      container.parent = body;
      container.owner = button.owner;
      input.owner = button.owner;
    },
  });
  const built = mountDocument({ children: [toggle] });
  const tagged = withDoc(built, () => studioAct({ op: "tags", tags: ["one", "two", " "] }));
  assert.equal(tagged.ok, true);
  assert.deepEqual(tagged.tags, ["one", "two"]);
  assert.equal(withDoc(built, () => studioAct({ op: "tags", tags: [] })).ok, true);

  const bare = mountDocument({ children: [new El("button", { id: "toggle-button", text: "Show more" })] });
  assert.match(withDoc(bare, () => studioAct({ op: "tags", tags: ["solo"] })).error, /标签/);
  const nowhere = mountDocument({ children: [new El("div", { text: "no tags" })] });
  assert.match(withDoc(nowhere, () => studioAct({ op: "tags", tags: ["solo"] })).error, /标签/);

  const frozen = new El("input", { id: "text-input", lockText: "" });
  const stuck = mountDocument({
    children: [new El("ytcp-form-input-container", { id: "tags-container", children: [frozen] })],
    execCommand: "noop",
  });
  const missed = withDoc(stuck, () => studioAct({ op: "tags", tags: ["solo"] }));
  assert.match(missed.error, /标签未写入/);
});

test("audience, visibility, wizard, click, and thumbnail controls", () => {
  const built = mountDocument({
    children: [
      new El("tp-yt-paper-radio-button", { attrs: { name: "VIDEO_MADE_FOR_KIDS_NOT_MFK" } }),
      new El("tp-yt-paper-radio-button", { attrs: { name: "VIDEO_MADE_FOR_KIDS_MFK" } }),
      new El("tp-yt-paper-radio-button", { attrs: { name: "PRIVATE" } }),
      new El("tp-yt-paper-radio-button", { attrs: { name: "UNLISTED" } }),
      new El("tp-yt-paper-radio-button", { attrs: { name: "PUBLIC" } }),
      new El("ytcp-button", { id: "next-button", text: "Next" }),
      new El("ytcp-button", { id: "done-button", text: "Save", disabled: true }),
      new El("ytcp-button", { id: "aria-off", attrs: { "aria-disabled": "true" } }),
      new El("button", { text: "上传缩略图" }),
    ],
  });
  const kids = withDoc(built, () => studioAct({ op: "audience", madeForKids: false }));
  assert.equal(kids.ok, true);
  assert.equal(kids.checked, true);
  assert.equal(kids.name, "VIDEO_MADE_FOR_KIDS_NOT_MFK");
  const yes = withDoc(built, () => studioAct({ op: "audience", madeForKids: true }));
  assert.equal(yes.name, "VIDEO_MADE_FOR_KIDS_MFK");

  const visibility = withDoc(built, () => studioAct({ op: "visibility", visibility: "unlisted" }));
  assert.equal(visibility.ok, true);
  assert.equal(visibility.name, "UNLISTED");
  assert.equal(withDoc(built, () => studioAct({ op: "visibility" })).name, "PRIVATE");

  const wizard = withDoc(built, () => studioAct({ op: "wizard" }));
  assert.equal(wizard.hasNext, true);
  assert.equal(wizard.nextEnabled, true);
  assert.equal(wizard.hasDone, true);
  assert.equal(wizard.doneEnabled, false);
  assert.equal(wizard.hasVisibility, true);
  assert.equal(wizard.hasKids, true);

  assert.equal(withDoc(built, () => studioAct({ op: "click", selector: "#next-button" })).ok, true);
  assert.equal(withDoc(built, () => studioAct({ op: "click", selector: "#done-button" })).disabled, true);
  assert.equal(withDoc(built, () => studioAct({ op: "click", selector: "#aria-off" })).disabled, true);
  assert.match(withDoc(built, () => studioAct({ op: "click", selector: "#missing" })).error, /未找到/);
  assert.match(withDoc(built, () => studioAct({ op: "click", selector: "" })).error, /未找到/);
  assert.equal(withDoc(built, () => studioAct({ op: "click-thumbnail" })).via, "上传缩略图");

  const file = mountDocument({ children: [new El("input", { id: "file-loader" })] });
  assert.equal(withDoc(file, () => studioAct({ op: "click-thumbnail" })).via, "#file-loader");
  const none = mountDocument({ children: [] });
  assert.match(withDoc(none, () => studioAct({ op: "click-thumbnail" })).error, /缩略图/);
  assert.match(withDoc(none, () => studioAct({ op: "audience", madeForKids: false })).error, /面向儿童/);
  assert.match(withDoc(none, () => studioAct({ op: "visibility", visibility: "public" })).error, /公开范围/);
});

test("pressEnter survives a broken KeyboardEvent and a throwing dispatch", () => {
  const input = new El("input", { id: "text-input" });
  input.dispatchEvent = () => {
    throw new Error("dispatch failed");
  };
  const built = mountDocument({
    children: [new El("ytcp-form-input-container", { id: "tags-container", children: [input] })],
  });
  const prev = globalThis.KeyboardEvent;
  globalThis.KeyboardEvent = function BrokenEvent() {
    throw new Error("no KeyboardEvent");
  };
  try {
    const result = withDoc(built, () => studioAct({ op: "tags", tags: ["solo"] }));
    assert.equal(result.ok, true);
    assert.deepEqual(result.tags, ["solo"]);
  } finally {
    if (prev === undefined) delete globalThis.KeyboardEvent;
    else globalThis.KeyboardEvent = prev;
  }
});

test("surface reads the video link and the error slot", () => {
  const built = mountDocument({
    href: "https://studio.youtube.com/video/AaBbCcDdEe1/edit",
    bodyText: "Upload complete",
    children: [
      new El("a", { href: "https://youtu.be/AaBbCcDdEe1", text: "link" }),
      new El("div", { id: "error-message", text: "daily upload limit reached" }),
    ],
  });
  const surface = withDoc(built, () => studioAct({ op: "surface" }));
  assert.match(surface.href, /youtu\.be\/AaBbCcDdEe1/);
  assert.match(surface.text, /Upload complete/);
  assert.match(surface.error, /daily upload limit/);
  assert.match(surface.url, /studio\.youtube\.com/);

  const styled = mountDocument({
    children: [new El("a", { className: "ytcp-video-info", href: "https://youtu.be/ZzYyXxWwVv1" })],
  });
  assert.match(withDoc(styled, () => studioAct({ op: "surface" })).href, /ZzYyXxWwVv1/);
});
