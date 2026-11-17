// 入口冒烟测试。
//
// 单元测试只覆盖被 import 的模块，两个 CLI 入口没有测试会一直裸奔：
// 改坏一次 import 路径，测试全绿，命令一跑就 ExitCode 1。
// 这里只验「能起来、参数不合理时退出码对」，不联网、不读用户会话。

import test from 'node:test';
import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const run = promisify(execFile);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const env = { ...process.env, NO_PROXY: '127.0.0.1,localhost', CSR_LANG: 'zh' };

async function cli(script, args) {
  try {
    const { stdout, stderr } = await run(process.execPath, [path.join(root, 'scripts', script), ...args], {
      cwd: root,
      env,
      timeout: 60000,
    });
    return { code: 0, stdout, stderr };
  } catch (e) {
    return { code: e.code, stdout: e.stdout || '', stderr: e.stderr || '' };
  }
}

test('sessions.mjs sources 能列出全部来源', async () => {
  const r = await cli('sessions.mjs', ['sources']);
  assert.equal(r.code, 0, r.stderr);
  for (const name of ['claude', 'codex', 'workbuddy']) {
    assert.ok(r.stdout.includes(name), `缺少来源 ${name}`);
  }
});

test('sessions.mjs 无参数时打用法并退出 2', async () => {
  const r = await cli('sessions.mjs', []);
  assert.equal(r.code, 2);
  assert.ok(r.stderr.includes('sessions.mjs export'), r.stderr);
});

test('read.mjs 无参数时打用法并退出 2', async () => {
  const r = await cli('read.mjs', []);
  assert.equal(r.code, 2);
  assert.ok(r.stderr.includes('read.mjs'), r.stderr);
});

test('read.mjs 遇到未知参数直接拒', async () => {
  const r = await cli('read.mjs', ['--nope']);
  assert.notEqual(r.code, 0);
});
