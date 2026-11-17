import assert from "node:assert/strict";
import test from "node:test";
import { HOME_URL } from "../lib/pure.mjs";
import { executeCheck } from "../lib/run-check.mjs";

function harness(impl) {
  const calls = { finish: 0, handOff: 0, gotos: [], open: null };
  const browser = {
    async open(opts) {
      calls.open = opts;
      const session = impl(calls);
      return {
        spaceId: session.spaceId ?? 4,
        goto: async (url) => { calls.gotos.push(url); },
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

test("a logged-in home timeline exits 0 and closes the space", async () => {
  const { browser, calls } = harness(() => ({
    detect: async () => ({
      url: HOME_URL,
      title: "主页 / X",
      text: "发帖",
      authCookie: true,
      csrfCookie: true,
      jarRead: true,
      platformChrome: true,
      profileHref: "/Suchuanyi",
    }),
  }));
  const summary = await executeCheck({ taskName: "unit" }, { browser });
  assert.equal(summary.ok, true);
  assert.equal(summary.exitCode, 0);
  assert.equal(summary.logged_in, true);
  assert.equal(summary.login_required, false);
  assert.equal(summary.screen_name, "Suchuanyi");
  assert.equal(summary.spaceId, 4);
  assert.match(summary.login_tip, /x\.com/);
  assert.equal(calls.finish, 1);
  assert.equal(calls.handOff, 0);
  assert.equal(calls.open.keepBrowser, false);
  assert.equal(calls.open.startUrl, HOME_URL);
  assert.equal(JSON.stringify(summary).includes("secret"), false);
});

test("a login wall soft-fails, and --keep hands the page over", async () => {
  const { browser, calls } = harness(() => ({
    detect: async () => ({
      url: "https://x.com/i/flow/login",
      title: "登录 X",
      text: "Sign in to X",
      authCookie: false,
      jarRead: true,
      onLoginWall: true,
    }),
  }));
  const summary = await executeCheck({ keep: true }, { browser });
  assert.equal(summary.exitCode, 2);
  assert.equal(summary.login_required, true);
  assert.equal(summary.on_login_page, true);
  assert.match(summary.error, /login required/i);
  assert.ok(summary.how_to_login.length >= 4);
  assert.ok(summary.how_to_login_zh.length >= 4);
  assert.equal(calls.handOff, 1);
  assert.equal(calls.finish, 1);
  assert.equal(calls.open.keepBrowser, true);
});

test("handOff and finish errors do not hide the login result", async () => {
  const { browser, calls } = harness(() => ({
    detect: async () => ({ url: "https://x.com/login", title: "", text: "", authCookie: false, jarRead: true, onLoginWall: true }),
    handOffError: "no hand",
    finishError: "no finish",
  }));
  const summary = await executeCheck({ keep: true }, { browser });
  assert.equal(summary.exitCode, 2);
  assert.match(summary.finish_error, /no finish/);
  assert.equal(calls.handOff, 1);
});

test("a blank tab is repainted once", async () => {
  let paints = 0;
  const { browser, calls } = harness(() => ({
    detect: async () => {
      paints += 1;
      if (paints === 1) return { url: "about:blank", title: "", text: "", authCookie: false, jarRead: false };
      return { url: HOME_URL, title: "主页 / X", text: "发帖", authCookie: true, jarRead: true, platformChrome: true, profileHref: "/Suchuanyi" };
    },
  }));
  const summary = await executeCheck({}, { browser });
  assert.equal(summary.exitCode, 0);
  assert.deepEqual(calls.gotos, [HOME_URL]);
});

test("an open failure exits 1", async () => {
  const summary = await executeCheck({}, { browser: { async open() { throw new Error("space down"); } } });
  assert.equal(summary.exitCode, 1);
  assert.match(summary.error, /space down/);
});
