// 脱敏模块的回归测试。
//
// 这里的断言都从 os.homedir() 现算，不写死某个平台的路径，
// 否则 Windows 和 CI 上的 Linux 会各挂一半。

import test from 'node:test';
import assert from 'node:assert/strict';
import os from 'node:os';
import path from 'node:path';
import { createRedactor, redact, LEVELS } from '../scripts/lib/redact.mjs';

const home = os.homedir();

test('off 档原样返回', () => {
  const s = `失败路径 ${path.join(home, 'proj', 'a.log')}`;
  assert.equal(redact(s, 'off'), s);
});

test('home 档把家目录换成 ~，目录结构保留', () => {
  const p = path.join(home, 'proj', 'sub', 'a.log');
  const out = redact(`打开 ${p} 失败`, 'home');
  assert.ok(out.startsWith('打开 ~'), out);
  assert.ok(out.includes('/proj/sub/a.log') || out.includes('\\proj\\sub\\a.log'), out);
  assert.ok(!out.includes(home), '原始家目录不应残留');
});

test('home 档同时认正斜杠和反斜杠两种写法', () => {
  const win = home.replace(/\//g, '\\');
  const posix = home.replace(/\\/g, '/');
  for (const v of [win, posix]) {
    const out = redact(`x ${v}/a/b.txt y`, 'home');
    assert.ok(!out.includes(home), `未替换：${v} -> ${out}`);
    assert.ok(out.includes('~/a/b.txt') || out.includes('~\\a\\b.txt'), out);
  }
});

test('home 档换掉同机其它用户', () => {
  const out = redact('log at /home/bob/.ssh/id_rsa', 'home');
  assert.equal(out, 'log at ~bob/.ssh/id_rsa');
});

test('幂等：处理两次结果不变', () => {
  const src = `A ${path.join(home, 'x', 'y.log')} B /home/bob/z C alice@example.com REDACTED-SECRET`;
  const once = redact(src, 'strict');
  assert.equal(redact(once, 'strict'), once);
});

test('strict 档遮邮箱、令牌、内网 IP', () => {
  const r = createRedactor('strict');
  assert.equal(r.apply('mail alice@example.com'), 'mail a***@example.com');
  assert.equal(r.apply('key REDACTED-SECRET'), 'key [redacted]');
  assert.equal(r.apply('gh ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123'), 'gh [redacted]');
  assert.equal(r.apply('jwt eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcdefghij'),
    'jwt [redacted]');
  assert.equal(r.apply('ip 192.168.1.44'), 'ip 192.168.x.x');
});

test('strict 档不动公网 IP 与 commit hash', () => {
  const s = 'dns 8.8.8.8 commit 9f2c1ab7a3d5';
  assert.equal(redact(s, 'strict'), s);
});

test('home 档遮令牌但不碰邮箱', () => {
  const s = 'alice@example.com REDACTED-SECRET';
  const out = redact(s, 'home');
  assert.ok(out.includes('alice@example.com'), '邮箱留给 strict');
  assert.ok(out.includes('[redacted]'), '令牌在 home 档就该遮');
  assert.equal(out, 'alice@example.com [redacted]');
});

test('令牌遮蔽不受档位影响，只有 off 放行', () => {
  const s = 'ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123 REDACTED-SECRET';
  assert.equal(redact(s, 'off'), s);
  assert.equal(redact(s, 'home'), '[redacted] [redacted]');
  assert.equal(redact(s, 'strict'), '[redacted] [redacted]');
});

test('未知档位回落 home', () => {
  const r = createRedactor('nonsense');
  assert.equal(r.level, 'home');
  assert.deepEqual(LEVELS, ['off', 'home', 'strict']);
});

test('hits 只统计实际替换处数', () => {
  const r = createRedactor('home');
  assert.equal(r.hits(), 0);
  r.apply('a alice@example.com b');
  assert.equal(r.hits(), 0, 'home 档不该把邮箱算成替换');
  r.apply(`p ${path.join(home, 'k')} q`);
  assert.ok(r.hits() >= 1);
});

test('空值与非字符串不炸', () => {
  const r = createRedactor('strict');
  assert.equal(r.apply(''), '');
  assert.equal(r.apply(null), '');
  assert.equal(r.apply(undefined), '');
});
