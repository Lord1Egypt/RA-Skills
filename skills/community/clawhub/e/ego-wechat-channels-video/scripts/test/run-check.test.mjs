import assert from "node:assert/strict";
import test from "node:test";
import { executeCheck } from "../lib/run-check.mjs";

function harness(impl) {
  const calls = { finish: 0, handOff: 0, gotos: [], open: null };
  const browser = {
    async open(opts) {
      calls.open = opts;
      const session = impl(calls);
      return {
        spaceId: session.spaceId ?? 9,
        goto: async (url) => {
          calls.gotos.push(url);
          if (session.onGoto) session.onGoto(url);
        },
        detect: async () => session.detect(),
        finish: async () => {
          calls.finish += 1;
          if (session.finishError) throw new Error(session.finishError);
        },
        handOff: async () => {
          calls.handOff += 1;
          if (session.handOffError) throw new Error(session.handOffError);
        },
      };
    },
  };
  return { browser, calls };
}

const loggedIn = {
  url: "https://channels.weixin.qq.com/platform/post/list",
  title: "视频号助手",
  text: "内容管理",
  platformChrome: true,
  loggedInCookie: true,
};

test("a logged-in Channels page exits 0 and closes the space", async () => {
  const { browser, calls } = harness(() => ({ detect: async () => loggedIn }));
  const summary = await executeCheck({ taskName: "unit" }, { browser });
  assert.equal(summary.ok, true);
  assert.equal(summary.exitCode, 0);
  assert.equal(summary.logged_in, true);
  assert.equal(summary.login_required, false);
  assert.equal(summary.spaceId, 9);
  assert.match(summary.login_tip, /expire/i);
  assert.match(summary.login_tip_zh, /扫码/);
  assert.equal(calls.finish, 1);
  assert.equal(calls.handOff, 0);
  assert.equal(calls.open.keepBrowser, false);
  assert.equal(calls.open.startUrl, "https://channels.weixin.qq.com");
});

test("login.html soft-fails, and --keep hands the page to the user", async () => {
  const { browser, calls } = harness(() => ({
    detect: async () => ({
      url: "https://channels.weixin.qq.com/login.html",
      title: "登录",
      text: "扫码登录",
      platformChrome: false,
      loggedInCookie: false,
    }),
  }));
  const summary = await executeCheck({ keep: true }, { browser });
  assert.equal(summary.exitCode, 2);
  assert.equal(summary.login_required, true);
  assert.equal(summary.on_login_page, true);
  assert.ok(summary.how_to_login.length >= 5);
  assert.ok(summary.how_to_login_zh.length >= 5);
  assert.equal(calls.handOff, 1);
  assert.equal(calls.gotos.length, 0);
  assert.equal(calls.finish, 1);
  assert.equal(calls.open.keepBrowser, true);
});

test("a blank first paint is reloaded once, then a platform page counts as logged in", async () => {
  let reads = 0;
  const { browser, calls } = harness(() => ({
    detect: async () => {
      reads += 1;
      if (reads === 1) {
        return { url: "https://channels.weixin.qq.com/", title: "", text: "", platformChrome: false, loggedInCookie: false };
      }
      return { url: "https://channels.weixin.qq.com/platform", title: "助手", text: "草稿", platformChrome: true, loggedInCookie: false };
    },
  }));
  const summary = await executeCheck({}, { browser });
  assert.equal(summary.logged_in, true);
  assert.equal(summary.exitCode, 0);
  assert.deepEqual(calls.gotos, ["https://channels.weixin.qq.com"]);
});

test("a thrown handoff or finish is recorded and the check still returns", async () => {
  const handed = harness(() => ({
    handOffError: "user declined",
    detect: async () => ({
      url: "https://channels.weixin.qq.com/login.html",
      title: "",
      text: "",
      platformChrome: false,
      loggedInCookie: false,
    }),
  }));
  const soft = await executeCheck({ keep: true }, { browser: handed.browser });
  assert.equal(soft.exitCode, 2);
  assert.equal(handed.calls.finish, 1);

  const closed = harness(() => ({
    finishError: "space already closed",
    detect: async () => loggedIn,
  }));
  const summary = await executeCheck({}, { browser: closed.browser });
  assert.equal(summary.ok, true);
  assert.match(summary.finish_error, /space already closed/);
});

test("browser failures exit 1 and still finish when a session exists", async () => {
  const summary = await executeCheck(
    {},
    {
      browser: {
        async open() {
          throw new Error("ego unavailable");
        },
      },
    },
  );
  assert.equal(summary.exitCode, 1);
  assert.match(summary.error, /ego unavailable/);

  const { browser, calls } = harness(() => ({
    detect: async () => {
      throw new Error("page dead");
    },
  }));
  const detected = await executeCheck({}, { browser });
  assert.equal(detected.exitCode, 1);
  assert.match(detected.error, /page dead/);
  assert.equal(calls.finish, 1);
});
