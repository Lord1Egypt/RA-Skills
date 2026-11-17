// 端口复用的判据。
//
// 背景：以前只要端口上应答的是 Chrome 就直接复用，省一次启动。问题是「端口上有
// Chrome」不代表那是我们起的。别人开着 --remote-debugging-port 的浏览器（调试工具、
// 另一个自动化脚本、安全审计员的窗口），连上去就等于借用人家的会话和 cookie。
// 现在只认自己写下的标记：端口 + profile 都对得上才算。
import test from 'node:test';
import assert from 'node:assert/strict';
import { isOurChrome } from '../scripts/lib/backend/cdp.mjs';

const profile = '/home/alice/.chat-share-reader/chrome-profile';

test('端口空着，不复用', () => {
  assert.equal(isOurChrome({ state: 'free', port: 9333, profile, mark: null }), false);
});

test('端口被别的程序占着，不复用', () => {
  assert.equal(isOurChrome({ state: 'busy', port: 9333, profile, mark: null }), false);
});

test('端口是 Chrome 但没有标记，不复用', () => {
  assert.equal(isOurChrome({ state: 'chrome', port: 9333, profile, mark: null }), false);
});

test('标记的端口对不上，不复用', () => {
  assert.equal(
    isOurChrome({ state: 'chrome', port: 9333, profile, mark: { port: 9444, profile } }),
    false
  );
});

test('标记的 profile 对不上，不复用', () => {
  assert.equal(
    isOurChrome({
      state: 'chrome',
      port: 9333,
      profile,
      mark: { port: 9333, profile: '/home/alice/.chat-share-reader/other' },
    }),
    false
  );
});

test('端口和 profile 都对得上才复用', () => {
  assert.equal(isOurChrome({ state: 'chrome', port: 9333, profile, mark: { port: 9333, profile } }), true);
});
