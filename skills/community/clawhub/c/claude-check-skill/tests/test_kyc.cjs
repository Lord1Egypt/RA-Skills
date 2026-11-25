const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../scripts/check-kyc.js'), 'utf8');
const uuid = '11111111-1111-1111-1111-111111111111';
async function run(replies, origin = 'https://claude.ai') {
  const calls = [];
  const context = {location: {origin}, AbortController, setTimeout, clearTimeout,
    fetch: async (url, options) => {
      calls.push(url);
      assert.equal(options.method, 'GET');
      assert.equal(options.credentials, 'same-origin');
      assert.equal(options.redirect, 'error');
      assert.ok(url.startsWith('https://claude.ai/api/organizations'));
      const next = replies.shift();
      if (next instanceof Error) throw next;
      assert.ok(next, 'unexpected request');
      return {ok: !next.http, status: next.http || 200, json: async () => {
        if (next.invalid) throw new SyntaxError('SECRET');
        return next.body;
      }};
    }};
  vm.createContext(context);
  return {data: await vm.runInContext(source + ';checkKyc()', context), calls};
}
(async () => {
  assert.equal((await run([], 'https://example.com')).calls.length, 0);
  for (const http of [401, 403, 404, 429, 500]) assert.equal((await run([{http}])).data.error, 'http_' + http);
  assert.equal((await run([{invalid: true}])).data.error, 'invalid_json');
  assert.equal((await run([new Error('SECRET')])).data.error, 'network_or_redirect');
  for (const body of [null, {}, 'bad']) assert.equal((await run([{body}])).data.error, 'invalid_organizations');
  assert.equal((await run([{body: []}])).data.error, 'no_organizations');
  assert.equal((await run([{body: Array(11).fill({uuid})}])).data.error, 'too_many_organizations');
  const bad = await run([{body: [{uuid: '../../secret'}, null]}]);
  assert.equal(bad.calls.length, 1);
  assert.ok(bad.data.rows.every(row => row.error === 'invalid_organization'));
  for (const status of ['not_required', 'pending', 'approved', 'denied', 'SECRET']) {
    const result = await run([{body: [{uuid, name: 'PRIVATE'}]}, {body: {status}}]);
    assert.equal(result.data.rows[0].status, status === 'SECRET' ? 'unknown' : status);
    for (const privateValue of [uuid, 'PRIVATE', 'SECRET']) assert.ok(!JSON.stringify(result.data).includes(privateValue));
  }
  for (const http of [401, 403, 429]) {
    const result = await run([{body: [{uuid}, {uuid}]}, {http}]);
    assert.equal(result.calls.length, 2);
    assert.equal(result.data.incomplete, true);
  }
  const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, '../tools/ai-tools/extension/manifest.json')));
  assert.deepEqual(manifest.permissions, ['activeTab', 'scripting']);
  assert.deepEqual(manifest.host_permissions, ['https://api.ipify.org/*', 'https://api6.ipify.org/*']);
  assert.equal(manifest.background, undefined);
  console.log('KYC tests passed: scope, requests, privacy, status distinctions, partial failure, permissions');
})().catch(error => { console.error(error); process.exitCode = 1; });
