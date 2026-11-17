import assert from "node:assert/strict";
import { test } from "node:test";
import { executeCheck } from "../lib/run-check.mjs";

function fakeBrowser({ url, text, openError } = {}) {
  const calls = { finish: 0, handOff: 0 };
  return {
    calls,
    open: openError
      ? async () => {
          throw new Error(openError);
        }
      : async () => ({
          spaceId: 11,
          probe: async () => ({ url, text }),
          finish: async () => {
            calls.finish += 1;
          },
          handOff: async () => {
            calls.handOff += 1;
          },
        }),
  };
}

test("executeCheck: logged in exits 0 and closes space", async () => {
  const b = fakeBrowser({
    url: "https://member.bilibili.com/platform/upload/video/frame",
    text: "创作中心 投稿 内容管理 上传视频",
  });
  const { summary, exitCode } = await executeCheck({ keep: false }, { browser: b });
  assert.equal(exitCode, 0);
  assert.equal(summary.login_required, false);
  assert.equal(b.calls.finish, 1);
  assert.equal(b.calls.handOff, 0);
});

test("executeCheck: login wall exits 2, closes when not keeping", async () => {
  const b = fakeBrowser({ url: "https://passport.bilibili.com/login", text: "扫码登录" });
  const { summary, exitCode } = await executeCheck({ keep: false }, { browser: b });
  assert.equal(exitCode, 2);
  assert.equal(summary.exit_code, 2);
  assert.equal(b.calls.finish, 1);
});

test("executeCheck: login wall with keep hands off instead of closing", async () => {
  const b = fakeBrowser({ url: "https://passport.bilibili.com/login", text: "扫码登录" });
  const { exitCode } = await executeCheck({ keep: true }, { browser: b });
  assert.equal(exitCode, 2);
  assert.equal(b.calls.handOff, 1);
  assert.equal(b.calls.finish, 0);
});

test("executeCheck: open error exits 1 with error body", async () => {
  const b = fakeBrowser({ openError: "boom" });
  const { summary, exitCode } = await executeCheck({}, { browser: b });
  assert.equal(exitCode, 1);
  assert.match(summary.error, /boom/);
  assert.equal(summary.exit_code, 1);
});
