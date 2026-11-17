import assert from "node:assert/strict";
import test from "node:test";
import { HOME_URL } from "../lib/pure.mjs";
import { createEgoBrowser, createEgoSession, readCookieJar } from "../lib/ego-deps.mjs";

function fakeTask(name) {
  const calls = { finish: [], hand: 0, goto: [], idle: 0, timeout: 0 };
  const page = {
    async url() { return "https://www.teambition.com/home"; },
    async title() { return "Teambition"; },
    async goto(url) { calls.goto.push(url); },
    async waitForLoadState() { calls.idle += 1; },
    async waitForTimeout(ms) { calls.timeout = ms; },
    async evaluate() {
      return { text: "我的项目", cookie: "TEAMBITION_SESSIONID=super-secret" };
    },
    async fetch() {
      return { status: 200, body: '{"ok":true}' };
    },
    async cdp() {
      return { cookies: [{ name: "TB_ACCESS_TOKEN", value: "also-secret" }] };
    },
  };
  return {
    name,
    spaceId: 8,
    calls,
    page() { return page; },
    async finish(arg) { calls.finish.push(arg); },
    async handOff() { calls.hand += 1; },
  };
}

test("readCookieJar falls back when the scoped call fails", async () => {
  assert.deepEqual(await readCookieJar(null), []);
  assert.deepEqual(await readCookieJar({}), []);
  const direct = await readCookieJar({
    async cdp(method) {
      assert.equal(method, "Network.getCookies");
      return { cookies: [{ name: "TEAMBITION_SESSIONID", value: "s" }] };
    },
  });
  assert.equal(direct.length, 1);

  let calls = 0;
  const fallback = await readCookieJar({
    async cdp() {
      calls += 1;
      if (calls === 1) return { cookies: null };
      return { cookies: [{ name: "TB_ACCESS_TOKEN" }] };
    },
  });
  assert.equal(fallback[0].name, "TB_ACCESS_TOKEN");

  const thrown = await readCookieJar({
    async cdp() {
      throw new Error("cdp down");
    },
  });
  assert.deepEqual(thrown, []);

  let n = 0;
  const second = await readCookieJar({
    async cdp() {
      n += 1;
      if (n === 1) throw new Error("scoped");
      return { nope: true };
    },
  });
  assert.deepEqual(second, []);
});

test("createEgoBrowser detects a session without returning cookie values", async () => {
  const task = fakeTask("teambition-login-check");
  task.page = (() => {
    const page = task.page();
    page.waitForLoadState = async () => { throw new Error("sockets"); };
    return () => page;
  })();
  const browser = createEgoBrowser({ taskSpace: async (name) => { assert.equal(name, "teambition-login-check"); return task; } });
  const session = await browser.open({ taskName: "teambition-login-check", startUrl: HOME_URL, keepBrowser: false });
  assert.equal(session.spaceId, 8);
  assert.equal(task.calls.goto[0], HOME_URL);
  assert.equal(task.calls.timeout, 800);
  const detected = await session.detect();
  assert.equal(detected.platformChrome, true);
  assert.equal(detected.loggedInCookie, true);
  assert.equal(JSON.stringify(detected).includes("secret"), false);
  assert.equal(await session.url(), "https://www.teambition.com/home");
  await session.finish();
  await session.finish();
  assert.deepEqual(task.calls.finish, [{ keep: [] }]);
  await session.handOff();
  assert.equal(task.calls.hand, 1);
});

test("networkidle success, keep, and a skipped start URL", async () => {
  const idle = fakeTask("idle");
  delete idle.page().waitForTimeout;
  const browser = createEgoBrowser({ taskSpace: async () => idle });
  const session = await browser.open({ taskName: "idle", startUrl: HOME_URL, keepBrowser: true });
  assert.equal(idle.calls.idle, 1);
  await session.finish();
  assert.deepEqual(idle.calls.finish, [{ keep: ["p1"] }]);

  const quiet = fakeTask("quiet");
  let gotos = 0;
  const page = quiet.page();
  page.goto = async () => { gotos += 1; };
  quiet.page = () => page;
  const noStart = createEgoBrowser({ taskSpace: async () => quiet });
  await noStart.open({ taskName: "quiet" });
  assert.equal(gotos, 0);
});

test("createEgoSession uses an injected space and the ego global", async () => {
  const task = fakeTask("tb-testcase api");
  const session = await createEgoSession({ taskName: "tb-testcase api" }, { taskSpace: async () => task });
  assert.equal(session.spaceId, 8);
  const body = await session.fetch("https://www.teambition.com/testcase/api/x");
  assert.equal(body.status, 200);
  assert.deepEqual(body.body, { ok: true });

  await assert.rejects(createEgoSession({}), /only available inside ego-browser/);
  globalThis.taskSpace = async () => fakeTask("global");
  try {
    const browser = createEgoBrowser();
    const opened = await browser.open({ taskName: "from-global", startUrl: HOME_URL });
    assert.equal(opened.spaceId, 8);
  } finally {
    delete globalThis.taskSpace;
  }
});
