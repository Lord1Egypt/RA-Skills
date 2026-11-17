'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');
const {
  API_BASE,
  RECHARGE_URL,
  SERVICE_FAILURE_MESSAGE,
  createIdempotencyKey,
  errorDetails,
  failureOutput,
  formatSeconds
} = require('./transcribe');

test('uses fixed service addresses', () => {
  assert.equal(API_BASE, 'https://calapi.ailuk.cn');
  assert.equal(RECHARGE_URL, 'https://payhtml.ailuk.cn');
});

test('extracts structured insufficient-balance errors', () => {
  assert.deepEqual(
    errorDetails({ detail: { code: 'INSUFFICIENT_BALANCE', message: '余额不足', recharge_url: RECHARGE_URL } }, 402),
    { code: 'INSUFFICIENT_BALANCE', message: '余额不足', rechargeUrl: RECHARGE_URL }
  );
});

test('formats duration without exposing media URL', () => {
  assert.equal(formatSeconds(61_234), '61.2 秒');
});

test('a refreshed media URL creates a new idempotency key', () => {
  const sourceUrl = 'https://www.douyin.com/video/123';
  assert.notEqual(
    createIdempotencyKey(sourceUrl, 'https://v1.douyinvod.com/audio?signature=old'),
    createIdempotencyKey(sourceUrl, 'https://v1.douyinvod.com/audio?signature=new')
  );
});

test('hides support-service errors behind the required user-facing message', () => {
  const error = Object.assign(new Error('internal provider detail'), { status: 500 });
  assert.deepEqual(failureOutput(error), {
    exitCode: 1,
    lines: [SERVICE_FAILURE_MESSAGE]
  });
});

test('keeps the insufficient-balance flow actionable', () => {
  const error = Object.assign(new Error('余额不足'), { code: 'INSUFFICIENT_BALANCE' });
  assert.deepEqual(failureOutput(error), {
    exitCode: 2,
    lines: ['余额不足：余额不足', `充值地址：${RECHARGE_URL}`]
  });
});
