/**
 * CLI tests — run with `npm test` (node:test, no third-party dependencies).
 *
 * 每个用例起一个本地 HTTP 桩服务当平台 API，用真实子进程跑 CLI，
 * 断言的是使用者实际看到的 stdout JSON / 退出码 / 发出的请求。
 */

import { test, describe, before, after, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const CLI = join(dirname(fileURLToPath(import.meta.url)), 'cli.mjs');
const TOKEN = 'tmu_test_token_do_not_leak';

/** 当前用例的响应桩：(req, body) => { status, json, headers } */
let handler;
/** 当前用例收到的请求记录 */
let received;
let server;
let baseUrl;

before(async () => {
  server = createServer((req, res) => {
    let raw = '';
    req.on('data', (chunk) => { raw += chunk; });
    req.on('end', () => {
      const body = raw ? JSON.parse(raw) : null;
      received.push({ method: req.method, url: req.url, headers: req.headers, body });
      const result = handler(req, body) ?? { status: 200, json: { success: true } };
      res.writeHead(result.status ?? 200, {
        'content-type': 'application/json',
        ...(result.headers ?? {}),
      });
      res.end(JSON.stringify(result.json ?? {}));
    });
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

after(() => new Promise((resolve) => server.close(resolve)));

beforeEach(() => {
  received = [];
  handler = () => ({ status: 200, json: { success: true } });
});

/** 跑一次 CLI，返回退出码与解析后的 stdout。 */
function runCli(args, envOverrides = {}) {
  return new Promise((resolve) => {
    const child = spawn(process.execPath, [CLI, ...args], {
      env: {
        PATH: process.env.PATH,
        CHINA_TM_PLATFORM_BASE_URL: baseUrl,
        CHINA_TM_USER_TOKEN: TOKEN,
        ALLOW_HTTP: 'true',
        ...envOverrides,
      },
    });

    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (c) => { stdout += c; });
    child.stderr.on('data', (c) => { stderr += c; });
    child.on('close', (code) => {
      let json = null;
      try { json = JSON.parse(stdout); } catch { /* 让断言去报原文 */ }
      resolve({ code, stdout, stderr, json });
    });
  });
}

describe('argument handling', () => {
  test('help works without any environment variables', async () => {
    const r = await runCli(['help'], {
      CHINA_TM_PLATFORM_BASE_URL: undefined,
      CHINA_TM_USER_TOKEN: undefined,
    });
    assert.equal(r.code, 0);
    assert.equal(r.json.success, true);
    assert.equal(r.json.command, 'help');
  });

  test('--help and -h are aliases of help', async () => {
    for (const flag of ['--help', '-h']) {
      const r = await runCli([flag]);
      assert.equal(r.json.command, 'help', `${flag} should print help`);
    }
  });

  test('an unknown command reports UNKNOWN_COMMAND, not a missing env var', async () => {
    const r = await runCli(['serch'], {
      CHINA_TM_PLATFORM_BASE_URL: undefined,
      CHINA_TM_USER_TOKEN: undefined,
    });
    assert.equal(r.code, 1);
    assert.equal(r.json.error.code, 'UNKNOWN_COMMAND');
  });

  test('missing environment variables are reported per variable', async () => {
    const r = await runCli(['capabilities'], { CHINA_TM_USER_TOKEN: undefined });
    assert.equal(r.json.error.code, 'ENV_MISSING');
    assert.match(r.json.error.message, /CHINA_TM_USER_TOKEN/);
  });

  test('a plain-HTTP base URL is refused unless ALLOW_HTTP is set', async () => {
    const r = await runCli(['capabilities'], { ALLOW_HTTP: undefined });
    assert.equal(r.json.error.code, 'HTTPS_REQUIRED');
    assert.equal(received.length, 0);
  });

  test('ALLOW_HTTP warns on stderr that the token goes out in cleartext', async () => {
    const r = await runCli(['capabilities']);
    assert.match(r.stderr, /ALLOW_HTTP/);
    assert.ok(!r.stderr.includes(TOKEN));
  });

  test('a flag-looking value is not swallowed as the option value', async () => {
    // 旧行为：--query 吞掉 "--page"，真的去查询 "--page" 并扣 1 点
    const r = await runCli(['search', '--query', '--page', '1']);
    assert.equal(r.json.error.code, 'ARGUMENT_INVALID');
    assert.equal(received.length, 0, 'must not spend a point on a malformed query');
  });

  test('--key=value form is supported', async () => {
    handler = () => ({ status: 200, json: { success: true, total: 0, results: [] } });
    const r = await runCli(['search', '--query=华源科技']);
    assert.equal(r.code, 0);
    assert.equal(received[0].body.query, '华源科技');
  });

  test('--lang en switches error messages to English', async () => {
    const r = await runCli(['search', '--lang', 'en']);
    assert.equal(r.json.error.code, 'ARGUMENT_INVALID');
    assert.match(r.json.error.message, /requires --query/);
  });
});

describe('search', () => {
  test('sends the auth header, the idempotency key and a fixed page size', async () => {
    handler = () => ({ status: 200, json: { success: true, queryId: 'qry_1', total: 0, results: [] } });
    const r = await runCli(['search', '--query', '  华源科技  ']);

    assert.equal(r.code, 0);
    const req = received[0];
    assert.equal(req.method, 'POST');
    assert.equal(req.url, '/v1/openclaw/trademarks/search');
    assert.equal(req.headers.authorization, `Bearer ${TOKEN}`);
    assert.match(req.headers['x-oc-request-id'], /^[A-Za-z0-9_-]{8,64}$/);
    assert.deepEqual(req.body, {
      query: '华源科技',
      page: 1,
      pageSize: 50,
      channel: 'clawhub',
    });
    assert.ok(!r.stdout.includes(TOKEN), 'the token must never reach stdout');
  });

  test('--page > 1 is rejected locally without calling the platform', async () => {
    const r = await runCli(['search', '--query', '华源科技', '--page', '2']);
    assert.equal(r.code, 1);
    assert.equal(r.json.error.code, 'PAGINATION_NOT_SUPPORTED');
    assert.equal(received.length, 0, 'must not spend a round-trip on an unsupported page');
  });

  test('--pageSize is ignored with a note, the platform value stays 50', async () => {
    handler = () => ({ status: 200, json: { success: true } });
    const r = await runCli(['search', '--query', '华源科技', '--pageSize', '100']);
    assert.equal(received[0].body.pageSize, 50);
    assert.match(r.stderr, /pageSize/);
  });

  test('a query longer than 200 characters is rejected', async () => {
    const r = await runCli(['search', '--query', 'x'.repeat(201)]);
    assert.equal(r.json.error.code, 'ARGUMENT_INVALID');
    assert.equal(received.length, 0);
  });
});

describe('error passthrough', () => {
  test('402 keeps rechargeUrl so the agent can hand it to the user', async () => {
    handler = () => ({
      status: 402,
      json: {
        success: false,
        error: {
          code: 'POINTS_NOT_ENOUGH',
          message: '点数不足，请先充值',
          rechargeUrl: 'https://tm.zhengquai.com/billing',
        },
      },
    });

    const r = await runCli(['search', '--query', '华源科技']);
    assert.equal(r.code, 1);
    assert.equal(r.json.error.code, 'POINTS_NOT_ENOUGH');
    assert.equal(r.json.error.rechargeUrl, 'https://tm.zhengquai.com/billing');
    assert.equal(r.json.error.httpStatus, 402);
    assert.equal(received.length, 1, '402 must not be retried');
  });

  test('500 keeps refundedPoints and retries with the same idempotency key', async () => {
    handler = () => ({
      status: 500,
      json: {
        success: false,
        error: { code: 'SERVER_ERROR', message: '查询失败，请稍后重试' },
        refundedPoints: 1,
      },
    });

    const r = await runCli(['search', '--query', '华源科技']);
    assert.equal(r.json.error.code, 'SERVER_ERROR');
    assert.equal(r.json.error.refundedPoints, 1);
    assert.equal(received.length, 3, 'initial attempt + 2 retries');
    const ids = new Set(received.map((x) => x.headers['x-oc-request-id']));
    assert.equal(ids.size, 1, 'retries must reuse one idempotency key');
  });

  test('502 UPSTREAM_ERROR is not retried (the platform already refunded)', async () => {
    handler = () => ({
      status: 502,
      json: {
        success: false,
        error: { code: 'UPSTREAM_ERROR', message: '商标详情获取失败' },
        refundedPoints: 2,
      },
    });

    const r = await runCli(['detail', '--tmid', 'tm_1']);
    assert.equal(r.json.error.code, 'UPSTREAM_ERROR');
    assert.equal(received.length, 1);
  });

  test('429 surfaces retryAfterSeconds instead of hammering the platform', async () => {
    handler = () => ({
      status: 429,
      headers: { 'retry-after': '60' },
      json: { success: false, error: { code: 'RATE_LIMITED', message: '请求过于频繁' } },
    });

    const r = await runCli(['modules']);
    assert.equal(r.json.error.code, 'RATE_LIMITED');
    assert.equal(r.json.error.retryAfterSeconds, 60);
    assert.equal(received.length, 1);
  });

  test('a request timeout is reported as UPSTREAM_TIMEOUT', async () => {
    handler = () => null; // 不回包，让 CLI 侧超时
    const slow = createServer((req, res) => { void req; void res; });
    await new Promise((resolve) => slow.listen(0, '127.0.0.1', resolve));

    const r = await runCli(['modules'], {
      CHINA_TM_PLATFORM_BASE_URL: `http://127.0.0.1:${slow.address().port}`,
      CHINA_TM_TIMEOUT_MS: '300',
    });

    await new Promise((resolve) => slow.close(resolve));
    assert.equal(r.json.error.code, 'UPSTREAM_TIMEOUT');
  });
});

describe('export', () => {
  test('duplicate tmids are de-duplicated before the tiered charge', async () => {
    handler = () => ({ status: 200, json: { success: true, exportJobId: 'exp_1', status: 'queued' } });
    await runCli(['export', '--queryId', 'qry_1', '--tmids', 'tm_1, tm_2 ,tm_1,,tm_2']);
    assert.deepEqual(received[0].body.selectedTmids, ['tm_1', 'tm_2']);
  });

  test('export-status queries once and flags a still-running job', async () => {
    handler = () => ({ status: 200, json: { success: true, exportJobId: 'exp_1', status: 'processing' } });
    const r = await runCli(['export-status', '--jobId', 'exp_1']);

    assert.equal(r.code, 0);
    assert.equal(received.length, 1, 'must not poll inside a single CLI invocation');
    assert.equal(r.json.pending, true);
    assert.ok(r.json.hint);
  });

  test('export-status returns a completed job without the pending flag', async () => {
    handler = () => ({
      status: 200,
      json: { success: true, exportJobId: 'exp_1', status: 'completed', downloadUrl: 'https://example.com/a.xlsx' },
    });
    const r = await runCli(['export-status', '--jobId', 'exp_1']);
    assert.equal(r.json.pending, undefined);
    assert.equal(r.json.data.downloadUrl, 'https://example.com/a.xlsx');
  });
});
