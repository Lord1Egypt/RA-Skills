import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { classifyImageRef, createReceiptStore, prepareArticle, withinRoot } from "../lib/prepare.mjs";

const jpeg = Buffer.from([0xff, 0xd8, 0xff, 0x00, 0x11, 0x22]);

function tempDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), "wx-article-"));
}

test("local, remote, and escaping image refs", () => {
  const dir = tempDir();
  assert.equal(withinRoot(path.join(dir, "a.jpg"), dir), true);
  assert.equal(withinRoot(path.join(dir, "..", "nope.jpg"), dir), false);
  const remote = classifyImageRef(path.join(dir, "post.md"), "https://cdn.example/a.jpg");
  assert.equal(remote.remote, "https://cdn.example/a.jpg");
  const local = path.join(dir, "cover.jpg");
  fs.writeFileSync(local, jpeg);
  assert.equal(classifyImageRef(path.join(dir, "post.md"), "cover.jpg").local, local);
  assert.equal(classifyImageRef(path.join(dir, "post.md"), local).local, local);
  assert.throws(() => classifyImageRef(path.join(dir, "post.md"), "../secret.jpg"), /escapes/);
  assert.throws(() => classifyImageRef(path.join(dir, "post.md"), "file:///tmp/a.jpg"), /unsupported/);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("prepareArticle resolves local and remote images and stores a receipt", async () => {
  const dir = tempDir();
  const image = path.join(dir, "cover.jpg");
  fs.writeFileSync(image, jpeg);
  const markdown = path.join(dir, "post.md");
  fs.writeFileSync(markdown, `---\ntitle: "题"\ndescription: "摘要"\n---\n\n![封面](cover.jpg)\n\n正文\n\n![远程](https://cdn.example/inline.jpg)\n`);
  const assets = path.join(dir, "assets");
  const fetched = [];
  const prepared = await prepareArticle({
    markdownPath: markdown,
    assetDir: assets,
    fetchImpl: async (url) => {
      fetched.push(url);
      return {
        ok: true,
        status: 200,
        headers: { get: () => String(jpeg.length) },
        arrayBuffer: async () => jpeg,
      };
    },
  });
  assert.equal(prepared.ok, true);
  assert.equal(prepared.article.imageCount, 2);
  assert.equal(fetched.length, 1);
  assert.equal(fs.existsSync(prepared.article.segments.find((segment) => segment.kind === "image" && segment.index === 1).path), true);
  const store = createReceiptStore();
  const receiptDir = path.join(dir, "receipts");
  store.write(receiptDir, { hash: prepared.article.hash, status: "saved", title: "题" });
  assert.equal(store.read(receiptDir, prepared.article.hash).status, "saved");
  assert.equal(store.read(receiptDir, "missing"), null);
  assert.equal(store.read("", "x"), null);
  fs.writeFileSync(path.join(receiptDir, "broken.json"), "{");
  const broken = createReceiptStore();
  assert.equal(broken.read(receiptDir, "broken").status, "uncertain");
  const missing = await prepareArticle({ markdownPath: path.join(dir, "nope.md") });
  assert.match(missing.error, /cannot read/);
  const noMarkdown = await prepareArticle({});
  assert.match(noMarkdown.error, /required/);
  fs.rmSync(dir, { recursive: true, force: true });
});

test("prepareArticle rejects a bad download, a huge image, and a non-image", async () => {
  const dir = tempDir();
  const markdown = path.join(dir, "post.md");
  fs.writeFileSync(markdown, `---\ntitle: "题"\n---\n\n![图](https://cdn.example/a.jpg)\n`);
  const failed = await prepareArticle({
    markdownPath: markdown,
    assetDir: path.join(dir, "assets"),
    fetchImpl: async () => ({ ok: false, status: 404, headers: { get: () => "0" } }),
  });
  assert.match(failed.error, /404/);
  const huge = await prepareArticle({
    markdownPath: markdown,
    assetDir: path.join(dir, "assets"),
    fetchImpl: async () => ({ ok: true, status: 200, headers: { get: () => String(9 * 1024 * 1024) } }),
  });
  assert.match(huge.error, /exceeds/);
  const fake = await prepareArticle({
    markdownPath: markdown,
    assetDir: path.join(dir, "assets"),
    fetchImpl: async () => ({
      ok: true,
      status: 200,
      headers: { get: () => "4" },
      arrayBuffer: async () => Buffer.from("nope"),
    }),
  });
  assert.match(fake.error, /not an image/);
  const noFetch = await prepareArticle({
    markdownPath: markdown,
    assetDir: path.join(dir, "assets"),
    fetchImpl: null,
  });
  assert.match(noFetch.error, /fetch/);
  fs.writeFileSync(markdown, `---\ntitle: "题"\n---\n\n![图](note.txt)\n`);
  fs.writeFileSync(path.join(dir, "note.txt"), "hello");
  const localBad = await prepareArticle({ markdownPath: markdown, assetDir: dir });
  assert.match(localBad.error, /not an image/);
  fs.writeFileSync(markdown, `---\ntitle: "题"\n---\n\n![图](../outside.jpg)\n`);
  const escaped = await prepareArticle({ markdownPath: markdown, assetDir: dir });
  assert.match(escaped.error, /escapes/);
  fs.rmSync(dir, { recursive: true, force: true });
});
