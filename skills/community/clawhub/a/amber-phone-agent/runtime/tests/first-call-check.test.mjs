import assert from 'node:assert/strict';
import { randomBytes } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import twilio from 'twilio';
import { firstCallCheck } from '../first-call-check.js';
import { verifyOpenAIWebhook } from '../dist/security.js';

const { version } = JSON.parse(await readFile(new URL('../package.json', import.meta.url)));
const cfg = {
  PUBLIC_BASE_URL: 'https://amber.example',
  TWILIO_AUTH_TOKEN: 'test-twilio-secret',
  OPENAI_WEBHOOK_SECRET: `whsec_${randomBytes(32).toString('base64')}`,
};

function fixture({ localVersion = version, publicInstance = 'bridge-a', acceptUnsignedTwilio = false } = {}) {
  const urls = [];
  return {
    urls,
    async fetchRequest(url, options) {
      urls.push(url);
      assert.equal(options.redirect, 'error');
      const { hostname, pathname } = new URL(url);
      if (pathname === '/healthz') {
        assert.equal(options.method, undefined);
        const local = hostname === '127.0.0.1';
        return Response.json({ ok: true }, { headers: {
          'X-Amber-Version': local ? localVersion : version,
          'X-Amber-Instance': local ? 'bridge-a' : publicInstance,
        } });
      }
      assert.equal(hostname, 'amber.example');
      assert.equal(options.method, 'POST');
      if (pathname === '/twilio/status') {
        assert.equal(options.body, '');
        const signature = options.headers['X-Twilio-Signature'];
        const valid = signature && twilio.validateRequest(cfg.TWILIO_AUTH_TOKEN, signature, url, {});
        return new Response(null, { status: valid || acceptUnsignedTwilio ? 204 : 401 });
      }
      assert.equal(pathname, '/openai/webhook');
      assert.deepEqual(JSON.parse(options.body), { type: 'amber.preflight' });
      const valid = verifyOpenAIWebhook(Buffer.from(options.body), options.headers, cfg.OPENAI_WEBHOOK_SECRET);
      return new Response(null, { status: valid ? 200 : 401 });
    },
  };
}

test('first-call check verifies versions, public bridge identity, and both signatures without a call', async () => {
  const mock = fixture();
  const checks = await firstCallCheck(cfg, { ...mock, skillVersion: async () => version });
  assert.deepEqual(checks.map(({ status }) => status), Array(5).fill('pass'));
  assert.equal(mock.urls.length, 6);
});

test('first-call check flags older skill and bridge versions and avoids public requests', async () => {
  const mock = fixture({ localVersion: '5.5.50' });
  const checks = await firstCallCheck(cfg, { ...mock, skillVersion: async () => '5.5.50' });
  assert.deepEqual(checks.map(({ status }) => status), ['fail', 'fail']);
  assert.match(checks[0].message, /older Amber skill copies/);
  assert.match(checks[1].message, /Rebuild and restart/);
  assert.deepEqual(mock.urls, ['http://127.0.0.1:8000/healthz']);
});

test('first-call check withholds webhook probes when the tunnel reaches another process', async () => {
  const mock = fixture({ publicInstance: 'bridge-b' });
  const checks = await firstCallCheck(cfg, { ...mock, skillVersion: async () => version });
  assert.match(checks.at(-1).message, /different bridge/);
  assert.equal(mock.urls.length, 2);
});

test('first-call check flags a Twilio webhook that accepts unsigned traffic', async () => {
  const mock = fixture({ acceptUnsignedTwilio: true });
  const checks = await firstCallCheck(cfg, { ...mock, skillVersion: async () => version });
  assert.equal(checks[3].status, 'fail');
  assert.match(checks[3].message, /TWILIO_WEBHOOK_STRICT=true/);
  assert.equal(checks[4].status, 'pass');
});
