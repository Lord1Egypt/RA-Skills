import assert from "node:assert/strict";
import test from "node:test";
import { CREATOR_HOME } from "../lib/pure.mjs";
import { createEgoBrowser } from "../lib/ego-deps.mjs";

function fakeTask() {
  const calls = { goto: [], finish: [] };
  const page = {
    async url() { return CREATOR_HOME; },
    async title() { return "创作服务平台"; },
    async goto(url) { calls.goto.push(url); },
    async waitForLoadState() {},
    async waitForTimeout() {},
    async evaluate() { return { ok: true, text: "", url: CREATOR_HOME, title: "" }; },
    async setInputFiles() {},
  };
  return {
    calls,
    spaceId: 4,
    page() { return page; },
    async finish(arg) { calls.finish.push(arg); },
    async handOff() {},
  };
}

test("createEgoBrowser opens the creator site and finishes keep empty", async () => {
  const task = fakeTask();
  const listed = [];
  const browser = createEgoBrowser({
    taskSpace: async (name) => {
      assert.equal(name, "xiaohongshu-ego");
      return task;
    },
    listSpaces: async () => listed,
  });
  assert.equal(browser.listSpaces, browser.listSpaces);
  const session = await browser.open({ taskName: "xiaohongshu-ego", startUrl: CREATOR_HOME, keepBrowser: false });
  assert.equal(session.spaceId, 4);
  assert.equal(task.calls.goto[0], CREATOR_HOME);
  await session.finish();
  assert.deepEqual(task.calls.finish, [{ keep: [] }]);
  const keptTask = fakeTask();
  keptTask.page().waitForLoadState = async () => { throw new Error("sockets"); };
  const keptBrowser = createEgoBrowser({ taskSpace: async () => keptTask });
  const kept = await keptBrowser.open({ taskName: "xiaohongshu-ego", startUrl: CREATOR_HOME, keepBrowser: true });
  await kept.finish();
  assert.deepEqual(keptTask.calls.finish, [{ keep: ["p1"] }]);
  const bare = fakeTask();
  await createEgoBrowser({ taskSpace: async () => bare }).open({ taskName: "xiaohongshu-ego" });
  assert.equal(bare.calls.goto.length, 0);
});

test("taskSpace and listSpaces fall back to ego globals", async () => {
  const previousSpace = globalThis.taskSpace;
  const previousList = globalThis.listTaskSpaces;
  const previousSpaces = globalThis.taskSpaces;
  delete globalThis.taskSpace;
  delete globalThis.listTaskSpaces;
  delete globalThis.taskSpaces;
  await assert.rejects(() => createEgoBrowser().open({ taskName: "xiaohongshu-ego" }), /taskSpace/);
  const browser = createEgoBrowser();
  assert.equal(await browser.listSpaces(), null);
  globalThis.listTaskSpaces = () => ["xiaohongshu-ego"];
  assert.deepEqual(await createEgoBrowser().listSpaces(), ["xiaohongshu-ego"]);
  globalThis.taskSpace = previousSpace;
  globalThis.listTaskSpaces = previousList;
  globalThis.taskSpaces = previousSpaces;
});
