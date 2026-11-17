import assert from "node:assert/strict";
import test from "node:test";
import { STUDIO_URL } from "../lib/pure.mjs";
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
  url: STUDIO_URL,
  title: "YouTube Studio",
  text: "YouTube Studio\nAnalytics",
  cookie: "LOGIN_INFO=yes",
  platformChrome: true,
  loggedInCookie: true,
  onLoginWall: false,
};

test("a logged-in Studio page exits 0 and closes the space", async () => {
  const { browser, calls } = harness(() => ({ detect: async () => loggedIn }));
  const summary = await executeCheck({ taskName: "unit" }, { browser });
  assert.equal(summary.ok, true);
  assert.equal(summary.exitCode, 0);
  assert.equal(summary.logged_in, true);
  assert.equal(summary.login_required, false);
  assert.equal(summary.spaceId, 9);
  assert.match(summary.login_tip, /best results/);
  assert.match(summary.login_tip_zh, /YouTube/);
  assert.equal(calls.finish, 1);
  assert.equal(calls.handOff, 0);
  assert.equal(calls.open.keepBrowser, false);
  assert.equal(calls.open.startUrl, STUDIO_URL);
  assert.equal(calls.open.taskName, "unit");
});

test("a Google sign-in wall soft-fails, and --keep hands the page to the user", async () => {
  const { browser, calls } = harness(() => ({
    detect: async () => ({
      url: "https://accounts.google.com/v3/signin",
      title: "Sign in",
      text: "Choose an account",
      platformChrome: false,
      loggedInCookie: false,
      onLoginWall: true,
    }),
  }));
  const summary = await executeCheck({ keep: true }, { browser });
  assert.equal(summary.exitCode, 2);
  assert.equal(summary.login_required, true);
  assert.equal(summary.on_login_page, true);
  assert.match(summary.error, /YouTube Studio login required/);
  assert.ok(summary.how_to_login.length >= 5);
  assert.ok(summary.how_to_login_zh.length >= 5);
  assert.equal(calls.handOff, 1);
  assert.equal(calls.gotos.length, 0);
  assert.equal(calls.finish, 1);
  assert.equal(calls.open.keepBrowser, true);
  assert.equal(calls.open.taskName, "youtube-login-check");
});

test("a blank first paint is reloaded once, then Studio chrome counts as logged in", async () => {
  let reads = 0;
  const { browser, calls } = harness(() => ({
    detect: async () => {
      reads += 1;
      if (reads === 1) {
        return {
          url: STUDIO_URL,
          title: "YouTube Studio",
          text: "",
          cookie: "",
          platformChrome: false,
          loggedInCookie: false,
          onLoginWall: false,
        };
      }
      return {
        url: STUDIO_URL,
        title: "YouTube Studio",
        text: "Dashboard",
        cookie: "",
        platformChrome: true,
        loggedInCookie: false,
        onLoginWall: false,
      };
    },
  }));
  const summary = await executeCheck({}, { browser });
  assert.equal(summary.logged_in, true);
  assert.equal(summary.exitCode, 0);
  assert.deepEqual(calls.gotos, [STUDIO_URL]);
});

test("a cookie-only session does not reload, and a thrown handoff still returns exit 2", async () => {
  const cookie = harness(() => ({
    detect: async () => ({
      url: STUDIO_URL,
      title: "",
      text: "",
      cookie: "SAPISID=yes",
      platformChrome: false,
      loggedInCookie: true,
      onLoginWall: false,
    }),
  }));
  const viaCookie = await executeCheck({}, { browser: cookie.browser });
  assert.equal(viaCookie.logged_in, true);
  assert.equal(cookie.calls.gotos.length, 0);

  const handed = harness(() => ({
    handOffError: "user declined",
    detect: async () => ({
      url: "https://www.youtube.com/signin",
      title: "",
      text: "Sign in to YouTube",
      platformChrome: false,
      loggedInCookie: false,
      onLoginWall: true,
    }),
  }));
  const soft = await executeCheck({ keep: true }, { browser: handed.browser });
  assert.equal(soft.exitCode, 2);
  assert.equal(handed.calls.handOff, 1);
  assert.equal(handed.calls.finish, 1);
});

test("a thrown finish is recorded and the check still returns", async () => {
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
