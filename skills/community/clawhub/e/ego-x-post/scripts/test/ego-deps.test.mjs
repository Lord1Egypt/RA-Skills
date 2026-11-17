import assert from "node:assert/strict";
import test from "node:test";
import { HOME_URL } from "../lib/pure.mjs";
import { createEgoBrowser } from "../lib/ego-deps.mjs";

function fakeTask() {
  const calls = { goto: [], idle: 0, timeout: 0, finish: [] };
  const page = {
    async url() { return HOME_URL; },
    async title() { return "主页 / X"; },
    async goto(url) { calls.goto.push(url); },
    async waitForLoadState() { calls.idle += 1; },
    async waitForTimeout(ms) { calls.timeout = ms; },
    async evaluate() { return { text: "", href: "", cookie: "", lang: "" }; },
    async fetch() { return { status: 200, body: "" }; },
    async cdp() { return { cookies: [] }; },
  };
  return {
    calls,
    spaceId: 3,
    page() { return page; },
    async finish(arg) { calls.finish.push(arg); },
    async handOff() {},
  };
}

test("createEgoBrowser opens x.com and finishes keep empty", async () => {
  const task = fakeTask();
  const browser = createEgoBrowser({
    taskSpace: async (name) => {
      assert.equal(name, "x-post");
      return task;
    },
  });
  const session = await browser.open({ taskName: "x-post", startUrl: HOME_URL, keepBrowser: false });
  assert.equal(session.spaceId, 3);
  assert.equal(task.calls.goto[0], HOME_URL);
  assert.equal(task.calls.timeout, 800);
  await session.finish();
  assert.deepEqual(task.calls.finish, [{ keep: [] }]);
});

test("networkidle failure, keep, and a skipped start URL", async () => {
  const task = fakeTask();
  const page = task.page();
  page.waitForLoadState = async () => { throw new Error("sockets"); };
  delete page.waitForTimeout;
  task.page = () => page;
  const browser = createEgoBrowser({ taskSpace: async () => task });
  const kept = await browser.open({ taskName: "x-post", startUrl: HOME_URL, keepBrowser: true });
  await kept.finish();
  assert.deepEqual(task.calls.finish, [{ keep: ["p1"] }]);
  const idle = fakeTask();
  const bare = createEgoBrowser({ taskSpace: async () => idle });
  await bare.open({ taskName: "x-post" });
  assert.equal(idle.calls.goto.length, 0);
});

test("taskSpace is only available inside ego-browser", async () => {
  const previous = globalThis.taskSpace;
  delete globalThis.taskSpace;
  await assert.rejects(() => createEgoBrowser().open({ taskName: "x-post" }), /taskSpace/);
  globalThis.taskSpace = previous;
});
