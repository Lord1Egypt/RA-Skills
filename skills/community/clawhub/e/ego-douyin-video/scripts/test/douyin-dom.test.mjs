import assert from "node:assert/strict";
import test from "node:test";
import { douyinAct } from "../lib/douyin-dom.mjs";
import { createDocument, element, textNode, withDocument } from "./dom-fixture.mjs";

function act(built, payload) {
  return withDocument(built, () => douyinAct(payload));
}

test("douyinAct refuses to run without a document and ignores an unknown op", () => {
  const prev = globalThis.document;
  globalThis.document = undefined;
  try {
    assert.equal(douyinAct({ op: "probe" }).ok, false);
  } finally {
    globalThis.document = prev;
  }
  const built = createDocument(element("div", { children: [] }));
  assert.match(act(built, { op: "nope" }).error, /unknown op/);
  assert.equal(act(built, null).ok, true);
  built.doc.body = null;
  assert.equal(act(built, { op: "probe" }).text, "");
});

test("upload label ignores split text and hidden controls, and a zero box is not a point", () => {
  const hidden = element("button", {
    hidden: true,
    children: [textNode("上传视频")],
  });
  const split = element("button", {
    children: [textNode("上传"), textNode("\n"), textNode("视频")],
    rect: { x: 8, y: 12, width: 40, height: 16 },
  });
  const role = element("div", {
    role: "button",
    children: [textNode("上传视频")],
    rect: { x: 4, y: 6, width: 20, height: 10 },
  });
  const body = element("div", {
    innerText: "点击上传 上传视频",
    children: [hidden, split, role],
  });
  const built = createDocument(body, { title: "抖音创作者中心" });
  const probe = act(built, { op: "probe" });
  assert.match(probe.text, /上传视频/);
  assert.equal(probe.title, "抖音创作者中心");
  const point = act(built, { op: "upload-point" });
  assert.equal(point.ok, true);
  assert.equal(point.x, 28);
  assert.equal(point.y, 20);
  assert.equal(act(built, { op: "href" }).href, built.location.href);

  const zero = createDocument(element("div", {
    children: [element("button", {
      children: [textNode("上传视频")],
      rect: { x: 1, y: 1, width: 0, height: 4 },
    })],
  }));
  assert.equal(act(zero, { op: "upload-point" }).ok, false);
  zero.doc.querySelector = undefined;
  zero.doc.querySelectorAll = undefined;
  assert.match(act(zero, { op: "fill-title", title: "标题" }).error, /标题/);
  assert.match(act(zero, { op: "fill-desc", desc: "简介" }).error, /简介/);
});

test("title uses the native setter and description prefers an empty editor", () => {
  const filled = element("div", {
    contentEditable: true,
    children: [textNode("已有")],
    innerText: "已有",
  });
  const empty = element("div", { contentEditable: true, children: [textNode("")] });
  const input = element("input", { placeholder: "填写作品标题，为作品获得更多流量" });
  const body = element("div", {
    innerText: "添加作品简介",
    children: [input, filled, empty],
  });
  const built = createDocument(body);
  const title = act(built, { op: "fill-title", title: "三十字内标题" });
  assert.equal(title.ok, true);
  assert.equal(title.value, "三十字内标题");
  assert.deepEqual(input.events, ["input", "change"]);

  built.doc._activeEditor = null;
  empty.focus = () => {
    empty.focused = true;
    built.doc._activeEditor = empty;
  };
  const desc = act(built, { op: "fill-desc", desc: "简介 #话题" });
  assert.equal(desc.ok, true);
  assert.equal(desc.text, "简介 #话题");
  assert.equal(empty.focused, true);
  assert.equal(filled.innerText, "已有");
  assert.equal(act(built, { op: "form-ready" }).ready, true);
});

test("a broken title setter and a bad description readback are visible", () => {
  const input = element("input", { placeholder: "作品标题" });
  const editor = element("div", { contentEditable: true, children: [textNode("")] });
  const body = element("div", { children: [input, editor] });
  const built = createDocument(body);
  built.doc._badTitle = true;
  built.doc._badDesc = true;
  editor.focus = () => {
    built.doc._activeEditor = editor;
  };
  assert.equal(act(built, { op: "fill-title", title: "标题" }).value, "WRONG");
  assert.equal(act(built, { op: "fill-desc", desc: "简介" }).ok, false);
});

test("without HTMLInputElement or execCommand the fields still write", () => {
  const input = element("input", { placeholder: "作品标题" });
  const editor = element("div", { contentEditable: true, children: [textNode("已有正文")] });
  const body = element("div", { children: [input, editor] });
  const built = createDocument(body);
  built.HTMLInputElement = undefined;
  built.doc.execCommand = undefined;
  const title = withDocument(built, () => douyinAct({ op: "fill-title", title: "直写" }));
  assert.equal(title.value, "直写");
  const desc = withDocument(built, () => douyinAct({ op: "fill-desc", desc: "直写简介" }));
  assert.equal(desc.ok, true);
  assert.equal(desc.text, "直写简介");
});

test("the publish control is the visible BUTTON whose own text is exactly 发布", () => {
  const immediate = element("button", { children: [textNode("立即发布")] });
  const nested = element("button", {
    children: [element("span", { children: [textNode("发布")] })],
  });
  const hidden = element("button", { hidden: true, children: [textNode("发布")] });
  const div = element("div", { children: [textNode("发布")] });
  const badBox = element("button", {
    children: [textNode("发布")],
    rect: { x: 0, y: 0, width: 10, height: 0 },
  });
  const real = element("button", {
    children: [textNode("发布")],
    rect: { x: 40, y: 80, width: 60, height: 20 },
  });
  const body = element("div", {
    innerText: "作品描述",
    children: [immediate, nested, hidden, div, badBox, real],
  });
  const built = createDocument(body);
  const point = act(built, { op: "publish-point" });
  assert.equal(point.ok, true);
  assert.equal(point.x, 70);
  assert.equal(point.y, 90);
  assert.equal(real.scrolled, true);
});

test("publish-point can walk without TreeWalker and reports a missing button", () => {
  const real = element("button", { children: [textNode("发布")] });
  const body = element("div", { children: [real] });
  const built = createDocument(body, { treeWalker: false });
  assert.equal(act(built, { op: "publish-point" }).ok, true);
  const empty = createDocument(element("div", { children: [] }), { treeWalker: false });
  assert.match(act(empty, { op: "publish-point" }).error, /发布/);
  const noButtons = createDocument(element("div", { children: [element("span")] }));
  noButtons.doc.querySelectorAll = undefined;
  assert.match(act(noButtons, { op: "upload-point" }).error, /上传视频/);
});

test("missing title and description editors fail, and success reads the live URL", () => {
  const built = createDocument(element("div", { children: [], innerText: "" }));
  assert.match(act(built, { op: "fill-title", title: "标题" }).error, /标题/);
  assert.match(act(built, { op: "fill-desc", desc: "简介" }).error, /简介/);
  built.location.href = "https://creator.douyin.com/creator-micro/content/manage";
  built.doc.body.innerText = "发布成功";
  const surface = act(built, { op: "success" });
  assert.match(surface.url, /content\/manage/);
  assert.match(surface.text, /发布成功/);
});
