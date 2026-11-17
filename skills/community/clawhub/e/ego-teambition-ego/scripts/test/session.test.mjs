import assert from "node:assert/strict";
import test from "node:test";
import { createPageSession, createTransport } from "../lib/session.mjs";

function fakePage(overrides = {}) {
  const calls = { goto: [], fetch: [], load: 0, finish: [], hand: 0 };
  const page = {
    async url() {
      return overrides.url ?? "https://www.teambition.com/home";
    },
    async goto(url) {
      calls.goto.push(url);
    },
    async waitForLoadState() {
      calls.load += 1;
    },
    async fetch(url, opts) {
      calls.fetch.push({ url, opts });
      return overrides.response ?? { status: 200, body: '{"ok":true}' };
    },
    ...overrides.page,
  };
  const task = {
    spaceId: 4,
    async finish(arg) {
      calls.finish.push(arg);
    },
    async handOff() {
      calls.hand += 1;
    },
  };
  return { page, task, calls };
}

test("createPageSession requires a task and a page", () => {
  assert.throws(() => createPageSession(), /requires task and page/);
  assert.throws(() => createPageSession({ task: {} }), /requires task and page/);
});

test("ensureSite opens teambition only when the tab is elsewhere", async () => {
  const home = fakePage();
  const session = createPageSession(home);
  await session.ensureSite();
  assert.deepEqual(home.calls.goto, []);

  const blank = fakePage({ url: "" });
  const opened = createPageSession(blank);
  await opened.ensureSite();
  assert.deepEqual(blank.calls.goto, ["https://www.teambition.com"]);
  assert.equal(blank.calls.load, 1);

  const other = fakePage({
    url: "https://example.test/",
    page: { async waitForLoadState() { throw new Error("unused"); } },
  });
  delete other.page.waitForLoadState;
  other.page.url = async () => "https://example.test/";
  other.page.goto = async (url) => { other.calls.goto.push(url); };
  other.page.fetch = home.page.fetch;
  const moved = createPageSession({ task: other.task, page: other.page });
  await moved.ensureSite();
  assert.deepEqual(other.calls.goto, ["https://www.teambition.com"]);

  const broken = fakePage({
    page: {
      async url() { throw new Error("no url"); },
      async goto(url) { broken.calls.goto.push(url); },
      async waitForLoadState() { broken.calls.load += 1; },
    },
  });
  const recovered = createPageSession(broken);
  await recovered.ensureSite();
  assert.equal(broken.calls.goto.length, 1);
});

test("fetch parses strings, objects, and empty responses", async () => {
  const ok = fakePage();
  const session = createPageSession(ok);
  const parsed = await session.fetch("https://www.teambition.com/testcase/api/x", { timeout: 5 });
  assert.deepEqual(parsed, { status: 200, body: { ok: true } });
  assert.deepEqual(ok.calls.fetch[0].opts, { timeout: 5 });

  const loose = fakePage({ response: { status: 200, body: '{"a":"x\u0001y"}' } });
  const looseSession = createPageSession(loose);
  assert.deepEqual((await looseSession.fetch("u")).body, { a: "x y" });

  const bad = fakePage({ response: { status: 200, body: "nope" } });
  assert.equal((await createPageSession(bad).fetch("u")).body, null);

  const objectBody = fakePage({ response: { status: 201, body: { already: true } } });
  assert.deepEqual(await createPageSession(objectBody).fetch("u"), { status: 201, body: { already: true } });

  const empty = fakePage({
    page: {
      async fetch() { return null; },
    },
  });
  assert.deepEqual(await createPageSession(empty).fetch("u"), { status: 0, body: null });
});

test("non-GET fetch sends JSON bodies and leaves archive empty", async () => {
  const posted = fakePage();
  await createPageSession(posted).fetch("https://www.teambition.com/testcase/api/v1/testcases", {
    method: "post",
    body: { title: "新建" },
    timeout: 9,
  });
  assert.equal(posted.calls.fetch[0].opts.method, "POST");
  assert.equal(posted.calls.fetch[0].opts.credentials, "include");
  assert.equal(posted.calls.fetch[0].opts.headers["content-type"], "application/json");
  assert.equal(posted.calls.fetch[0].opts.body, "{\"title\":\"新建\"}");
  assert.equal(posted.calls.fetch[0].opts.timeout, 9);

  const archived = fakePage();
  await createPageSession(archived).fetch("https://www.teambition.com/api/testcases/abc/archive", {
    method: "POST",
    body: null,
  });
  assert.equal(archived.calls.fetch[0].opts.method, "POST");
  assert.equal(archived.calls.fetch[0].opts.credentials, "include");
  assert.equal(archived.calls.fetch[0].opts.body, undefined);
  assert.equal(archived.calls.fetch[0].opts.headers, undefined);

  const put = fakePage();
  await createPageSession(put).fetch("https://www.teambition.com/testcase/api/v1/title", {
    method: "PUT",
    body: "{\"title\":\"已改\"}",
    headers: { "x-trace": "1" },
  });
  assert.equal(put.calls.fetch[0].opts.body, "{\"title\":\"已改\"}");
  assert.equal(put.calls.fetch[0].opts.headers["x-trace"], "1");
  assert.equal(put.calls.fetch[0].opts.headers["content-type"], "application/json");
});

test("finish, cleanup, and handOff", async () => {
  const bag = fakePage();
  const session = createPageSession(bag);
  await session.finish();
  await session.finish({ keep: true });
  assert.deepEqual(bag.calls.finish, [{ keep: [] }]);
  await session.cleanup();
  assert.deepEqual(bag.calls.finish[1], { keep: [] });
  await session.handOff();
  assert.equal(bag.calls.hand, 1);

  const kept = fakePage();
  await createPageSession(kept).finish({ keep: true });
  assert.deepEqual(kept.calls.finish, [{ keep: ["p1"] }]);

  const quiet = fakePage();
  delete quiet.task.handOff;
  await createPageSession(quiet).handOff();
  assert.equal(quiet.calls.hand, 0);
});

test("browser transport delegates and open transport stays a stub", async () => {
  const session = { async fetch(url) { return { status: 200, url }; } };
  const browser = createTransport("browser", session);
  assert.equal(browser.implemented, true);
  assert.deepEqual(await browser.request("https://example"), { status: 200, url: "https://example" });
  assert.throws(() => createTransport("browser", {}), /requires a page session/);
  assert.throws(() => createTransport("browser", null), /requires a page session/);

  for (const kind of ["open", "open-api"]) {
    const open = createTransport(kind, null);
    assert.equal(open.implemented, false);
    await assert.rejects(open.request(), (error) => {
      assert.equal(error.code, "TRANSPORT_NOT_IMPLEMENTED");
      assert.match(error.message, /Phase 1/);
      assert.match(error.message, /testcase\/api/);
      return true;
    });
  }
  assert.throws(() => createTransport("socket"), /Unknown transport: socket/);
  const implicit = createTransport(undefined, session);
  assert.equal(implicit.kind, "browser");
});
