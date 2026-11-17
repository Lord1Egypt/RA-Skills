import assert from "node:assert/strict";
import test from "node:test";
import { executeCheck, executeCleanup, executeSave } from "../lib/editor-flow.mjs";

function article(extra = {}) {
  return {
    title: "题",
    hash: "abc",
    digest: "摘要",
    sourceUrl: "https://example.com/p",
    segments: [{ kind: "html", html: "<p>正文</p>", text: "正文" }],
    snippets: ["正文"],
    links: [{ href: "https://example.com/a", text: "链接" }],
    imageCount: 0,
    images: [],
    fidelity: ["images are uploaded"],
    ...extra,
  };
}

function memoryReceipts(initial = null) {
  const saved = [];
  return {
    saved,
    read() { return initial && initial.current ? initial.current : null; },
    write(_dir, receipt) {
      saved.push(receipt);
      if (initial) initial.current = receipt;
    },
  };
}

function browserWith(session, spaces) {
  return {
    async open() {
      if (session.openError) throw new Error(session.openError);
      return session;
    },
    async listSpaces() {
      if (spaces && spaces.error) throw new Error(spaces.error);
      return spaces || [];
    },
    async finishSpace(space) {
      (spaces.closed || (spaces.closed = [])).push(space.id);
    },
  };
}

function session(overrides = {}) {
  const calls = [];
  const api = {
    calls,
    openError: overrides.openError || "",
    async probe() {
      if (overrides.probeError) throw new Error(overrides.probeError);
      return overrides.probe || { loggedIn: true, loginWall: false, accounts: ["加选"], ambiguous: false };
    },
    async listDrafts() {
      calls.push("drafts");
      const queue = overrides.draftQueue;
      if (queue && queue.length) return queue.shift();
      return overrides.drafts || [];
    },
    async openEditor() { calls.push("editor"); },
    async fillTitle() { calls.push("title"); },
    async fillOptional() { calls.push("optional"); },
    async pasteHtml() { calls.push("paste"); },
    async uploadImage() { calls.push("upload"); if (overrides.uploadError) throw new Error(overrides.uploadError); },
    async replaceSlot() { return this.uploadImage(); },
    async ensureCover() { calls.push("cover"); return overrides.cover || { ok: true, skipped: true }; },
    async readEditor() {
      calls.push("read");
      return overrides.read || { title: "题", text: "正文", imageCount: 0, hrefs: ["https://example.com/a"] };
    },
    async clickSave() { calls.push("save"); if (overrides.saveError) throw new Error(overrides.saveError); },
    async saveConfirmed() { return overrides.confirmed === true; },
    async openDraft() { calls.push("reopen"); if (overrides.reopenError) throw new Error(overrides.reopenError); },
    async openPreview() { return { ok: true, kind: "pane" }; },
    async captureViews(_dir, prefix) { return [`/absolute/path/${prefix}-top.png`]; },
    async finish() { calls.push("finish"); if (overrides.finishError) throw new Error("finish failed"); },
  };
  return api;
}

const config = (extra = {}) => ({
  yes: true,
  expectAccount: "",
  receiptDir: "/absolute/path/receipts",
  screenshotDir: "",
  article: article(),
  ...extra,
});

test("check reports the account and stops when it is not unique", async () => {
  const loggedIn = session();
  const ok = await executeCheck({}, { browser: browserWith(loggedIn), receipts: memoryReceipts() });
  assert.equal(ok.exitCode, 0);
  assert.equal(ok.account, "加选");
  assert.equal(loggedIn.calls.at(-1), "finish");

  const out = await executeCheck({}, {
    browser: browserWith(session({ probe: { loggedIn: false, loginWall: true, accounts: [] } })),
    receipts: memoryReceipts(),
  });
  assert.equal(out.exitCode, 2);
  assert.equal(out.login_required, true);

  const many = await executeCheck({ expectAccount: "加选" }, {
    browser: browserWith(session({ probe: { loggedIn: true, accounts: ["甲", "乙"], ambiguous: true } })),
    receipts: memoryReceipts(),
  });
  assert.equal(many.exitCode, 4);
  assert.deepEqual(many.accounts, ["甲", "乙"]);

  const unnamed = await executeSave(config(), {
    browser: browserWith(session({ probe: { loggedIn: true, accounts: [] } })),
    receipts: memoryReceipts(),
  });
  assert.equal(unnamed.reason, "unidentified-account");
  assert.equal(unnamed.plan.title, "题");
  const mismatch = await executeCheck({ expectAccount: "别的号" }, {
    browser: browserWith(loggedIn),
    receipts: memoryReceipts(),
  });
  assert.equal(mismatch.reason, "account-mismatch");
});

test("save is dry-run unless --yes, and a saved receipt is not written again", async () => {
  const dry = session();
  const preview = await executeSave(config({ yes: false }), {
    browser: browserWith(dry),
    receipts: memoryReceipts(),
  });
  assert.equal(preview.exitCode, 3);
  assert.equal(preview.confirmation_required, true);
  assert.equal(dry.calls.includes("save"), false);
  assert.equal(dry.calls.includes("editor"), false);

  const dup = session();
  const again = await executeSave(config(), {
    browser: browserWith(dup),
    receipts: memoryReceipts({ current: { hash: "abc", status: "saved", draftId: "4", draftTime: "今天" } }),
  });
  assert.equal(again.duplicate, true);
  assert.equal(again.saved, false);
  assert.equal(again.draftId, "4");
  assert.equal(dup.calls.includes("editor"), false);
});

test("an uncertain receipt is reconciled from the draft list before another save", async () => {
  const found = session({ drafts: [{ title: "题", id: "8", time: "今天 01:00" }] });
  const kept = await executeSave(config(), {
    browser: browserWith(found),
    receipts: memoryReceipts({ current: { hash: "abc", status: "uncertain" } }),
  });
  assert.equal(kept.action, "reconciled");
  assert.equal(kept.draftId, "8");
  assert.equal(found.calls.includes("save"), false);

  const missing = session({
    draftQueue: [[], [{ title: "题", id: "9", time: "今天" }]],
  });
  const store = memoryReceipts({ current: { hash: "abc", status: "pending" } });
  const retried = await executeSave(config({ screenshotDir: "/absolute/path/shots" }), {
    browser: browserWith(missing),
    receipts: store,
    now: () => "2026-11-08T00:00:00.000Z",
  });
  assert.equal(retried.saved, true);
  assert.equal(retried.draftId, "9");
  assert.equal(retried.preview, true);
  assert.equal(store.saved.at(-1).status, "saved");
  assert.equal(missing.calls.includes("upload"), false);
});

test("a new draft is saved once, then not when readback, cover, or the list is unsafe", async () => {
  const happy = session({ drafts: [{ title: "题", id: "3", time: "今天" }] });
  const saved = await executeSave(config({
    article: article({
      segments: [
        { kind: "html", html: "<p>正文</p>", text: "正文" },
        { kind: "image", path: "/absolute/path/a.jpg" },
      ],
      imageCount: 1,
    }),
    read: undefined,
  }), {
    browser: browserWith(session({
      drafts: [{ title: "题", id: "3", time: "今天" }],
      read: { title: "题", text: "正文", imageCount: 1, hrefs: [] },
    })),
    receipts: memoryReceipts(),
    now: () => "2026-11-08T00:00:00.000Z",
  });
  assert.equal(saved.saved, true);
  assert.equal(saved.screenshots.length, 0);
  assert.equal(happy.calls.length, 0);

  const badRead = session();
  const rejected = await executeSave(config(), {
    browser: browserWith(session({ read: { title: "题", text: "缺了", imageCount: 0, hrefs: [] } })),
    receipts: memoryReceipts(),
  });
  assert.match(rejected.error, /readback/);
  assert.equal(badRead.calls.includes("save"), false);

  const covered = session({ cover: { ok: false, error: "cover is empty" } });
  const noCover = await executeSave(config(), { browser: browserWith(covered), receipts: memoryReceipts() });
  assert.match(noCover.error, /cover/);
  assert.equal(covered.calls.includes("save"), false);

  const broken = session({ saveError: "保存 control not found" });
  const noButton = await executeSave(config(), { browser: browserWith(broken), receipts: memoryReceipts() });
  assert.match(noButton.error, /保存/);

  const unsure = session({ drafts: [] });
  const uncertain = await executeSave(config(), { browser: browserWith(unsure), receipts: memoryReceipts() });
  assert.equal(uncertain.exitCode, 4);
  assert.equal(uncertain.action, "uncertain");

  const doubled = session({ drafts: [{ title: "题" }, { title: "题" }] });
  const ambiguous = await executeSave(config(), {
    browser: browserWith(doubled),
    receipts: memoryReceipts({ current: { hash: "abc", status: "pending" } }),
  });
  assert.equal(ambiguous.action, "ambiguous-draft");

  const store = memoryReceipts();
  store.write = () => { throw new Error("disk full"); };
  const unwritten = await executeSave(config(), { browser: browserWith(session()), receipts: store });
  assert.match(unwritten.error, /receipt/);

  const missingArticle = await executeSave(config({ article: null }), {
    browser: browserWith(session()),
    receipts: memoryReceipts(),
  });
  assert.match(missingArticle.error, /not prepared/);

  const crashed = await executeSave(config(), {
    browser: browserWith(session({ openError: "space failed" })),
    receipts: memoryReceipts(),
  });
  assert.match(crashed.error, /space failed/);

  const reopened = session({
    drafts: [{ title: "题", id: "3", time: "今天" }],
    reopenError: "draft editor did not open",
  });
  const partial = await executeSave(config(), { browser: browserWith(reopened), receipts: memoryReceipts() });
  assert.equal(partial.saved, true);
  assert.match(partial.warning, /did not open/);

  const noisy = session({ finishError: true });
  const still = await executeCheck({}, { browser: browserWith(noisy), receipts: memoryReceipts() });
  assert.equal(still.exitCode, 0);
  assert.equal(noisy.calls.includes("finish"), true);
});

test("cleanup closes only this skill's spaces", async () => {
  const spaces = [{ id: 7, name: "wechat-article-ego" }, { id: 8, name: "other" }];
  const closed = await executeCleanup({}, { browser: browserWith(null, spaces) });
  assert.deepEqual(spaces.closed, [7]);
  assert.equal(closed.exitCode, 0);
  const failed = await executeCleanup({}, { browser: browserWith(null, { error: "no list" }) });
  assert.equal(failed.exitCode, 1);
});
