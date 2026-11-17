import assert from "node:assert/strict";
import test from "node:test";
import { CREATOR_HOME } from "../lib/pure.mjs";
import { executeCheck } from "../lib/run-check.mjs";

function harness(impl) {
  const calls = { finish: 0, handOff: 0, gotos: [], open: null, finishError: "" };
  const browser = {
    async open(opts) {
      calls.open = opts;
      const session = impl(calls);
      return {
        spaceId: session.spaceId ?? 9,
        goto: async (url) => { calls.gotos.push(url); if (session.goto) await session.goto(url); },
        detect: async () => session.detect(),
        finish: async () => {
          calls.finish += 1;
          if (session.finishError) throw new Error(session.finishError);
        },
        handOff: async () => {
          calls.handOff += 1;
          if (session.handOffError) throw new Error("handoff");
        },
      };
    },
  };
  return { browser, calls };
}

const signedIn = {
  url: CREATOR_HOME,
  title: "创作服务平台",
  text: "发布笔记 笔记管理",
  nickname: "听懂AI",
  creatorChrome: true,
  loginWall: false,
};

test("a logged-in creator exits 0 and closes the space", async () => {
  const { browser, calls } = harness(() => ({ detect: async () => signedIn }));
  const summary = await executeCheck({ taskName: "unit", expectAccount: "听懂AI" }, { browser });
  assert.equal(summary.exitCode, 0);
  assert.equal(summary.logged_in, true);
  assert.equal(summary.nickname, "听懂AI");
  assert.equal(summary.account_mismatch, false);
  assert.equal(calls.finish, 1);
  assert.equal(calls.handOff, 0);
  assert.equal(calls.open.startUrl, CREATOR_HOME);
  assert.equal(calls.open.keepBrowser, false);
});

test("login wall and account mismatch soft-fail", async () => {
  const wall = harness(() => ({
    detect: async () => ({
      url: "https://creator.xiaohongshu.com/login",
      title: "登录",
      text: "扫码登录",
      loginWall: true,
    }),
    handOffError: true,
  }));
  const loggedOut = await executeCheck({ keep: true }, { browser: wall.browser });
  assert.equal(loggedOut.exitCode, 2);
  assert.equal(loggedOut.login_required, true);
  assert.ok(loggedOut.how_to_login_zh.length >= 4);
  assert.equal(wall.calls.handOff, 1);
  assert.equal(wall.calls.finish, 1);
  const mismatch = harness(() => ({
    detect: async () => ({ ...signedIn, nickname: "油管精选" }),
  }));
  const wrong = await executeCheck({ expectAccount: "听懂AI" }, { browser: mismatch.browser });
  assert.equal(wrong.exitCode, 2);
  assert.equal(wrong.account_mismatch, true);
  assert.match(wrong.error, /油管精选/);
  assert.equal(mismatch.calls.handOff, 0);
});

test("blank pages repaint, evaluate errors exit 1, and finish errors are kept", async () => {
  let n = 0;
  const { browser, calls } = harness(() => ({
    detect: async () => {
      n += 1;
      if (n === 1) return { url: "", text: "", title: "" };
      return signedIn;
    },
  }));
  const summary = await executeCheck({}, { browser });
  assert.equal(summary.exitCode, 0);
  assert.equal(calls.gotos[0], CREATOR_HOME);
  const broken = harness(() => ({
    detect: async () => ({ url: CREATOR_HOME, text: "", evaluateError: "evaluate down" }),
  }));
  const failed = await executeCheck({}, { browser: broken.browser });
  assert.equal(failed.exitCode, 1);
  assert.match(failed.error, /evaluate down/);
  const noisy = harness(() => ({
    detect: async () => ({
      url: "https://creator.xiaohongshu.com/login",
      text: "扫码登录",
      loginWall: true,
      evaluateError: "partial",
    }),
  }));
  const partial = await executeCheck({ expectAccount: "听懂AI" }, { browser: noisy.browser });
  assert.equal(partial.exitCode, 1);
  assert.match(partial.error, /partial/);
  assert.equal(partial.account_mismatch, undefined);
  const closing = harness(() => ({ detect: async () => signedIn, finishError: "finish broke" }));
  const closed = await executeCheck({}, { browser: closing.browser });
  assert.equal(closed.exitCode, 0);
  assert.match(closed.finish_error, /finish broke/);
  const required = await executeCheck({}, {});
  assert.equal(required.exitCode, 1);
  assert.match(required.error, /browser is required/);
  const thrown = await executeCheck({}, { browser: { async open() { throw new Error("no space"); } } });
  assert.equal(thrown.exitCode, 1);
  assert.match(thrown.error, /no space/);
});
