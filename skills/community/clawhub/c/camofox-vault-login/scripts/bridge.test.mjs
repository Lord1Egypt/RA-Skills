import test from 'node:test';
import assert from 'node:assert/strict';
import { bridge, origin } from './bridge.mjs';
import { createVault, childEnv, captured, inspectionExpression } from './runtime.mjs';
const id = '11111111-1111-1111-1111-111111111111';
const secret = 'SYNTHETIC_PASSWORD_MARKER';
const profile = { expectedVaultServerUrl: 'https://vault.example.invalid', expectedVaultEmail: 'fixture@example.invalid', keychainAccount: 'fixture', keychainService: 'fixture-vault' };
const site = 'https://login.example.invalid';
const item = () => ({ id, type: 1, name: secret, login: { username: 'SYNTHETIC_USER_MARKER', password: secret, totp: 'JBSWY3DPEHPK3PXP', uris: [{ uri: site, match: null }] } });
function fixture() {
  const state = { items: [item()], typed: [], inspections: 0, unlocks: 0, codes: 0 };
  const vault = { status: async () => ({ serverUrl: 'https://vault.example.invalid', userEmail: 'fixture@example.invalid', status: 'unlocked' }), unlock: async () => state.unlocks++, items: async () => state.items, totp: async () => { state.codes++; return { code: '123456', expiresAt: Date.now() + 30000 }; } };
  const browser = { inspect: async (_, selector) => { state.inspections++; return { url: site, top: true, count: 1, tag: 'INPUT', type: selector === '#p' ? 'password' : 'text', visible: true, disabled: false, readOnly: false, actions: [site + '/login'] }; }, type: async (_, selector, text) => state.typed.push({ selector, text }) };
  return { profile, state, vault, browser, request: { origin: site, tabId: 'tab', fields: { username: '#u', password: '#p' } } };
}
const execute = f => bridge(f.request, f);
const redacted = r => { assert.ok(!JSON.stringify(r).includes('MARKER')); assert.ok(!JSON.stringify(r).includes('123456')); };
test('username/password happy path, no submit and no secrets returned', async () => { const f = fixture(), r = await execute(f); assert.equal(r.ok, true); assert.deepEqual(r.filled, ['username','password']); assert.equal(f.state.typed[1].text, secret); assert.equal(r.submitted, false); redacted(r); });
test('TOTP happy path', async () => { const f = fixture(); f.request.fields = { totp: '#otp' }; assert.equal((await execute(f)).ok, true); assert.equal(f.state.typed[0].text, '123456'); });
test('locked unlocks once', async () => { const f = fixture(); const original = f.vault.status; f.vault.status = async () => ({ ...await original(), status: 'locked' }); assert.equal((await execute(f)).ok, true); assert.equal(f.state.unlocks, 1); });
test('unlocked never unlocks', async () => { const f = fixture(); await execute(f); assert.equal(f.state.unlocks, 0); });
for (const url of ['http://login.example.invalid','https://a:b@login.example.invalid','https://login.example.invalid.evil.example.invalid','https://sub.login.example.invalid','https://example.invalid','https://login.example.invalid:444','https://xn--exampl-gva.example.invalid','https://login.example.invalid.']) test('reject origin collision ' + url, async () => { const f = fixture(); f.request.origin = url; assert.equal((await execute(f)).ok, false); assert.equal(f.state.typed.length, 0); });
for (const match of [3,4,8,5]) test('unsupported/never URI rule ' + match, async () => { const f = fixture(); f.state.items[0].login.uris[0].match = match; assert.equal((await execute(f)).ok, false); });
test('SSO mapping must be stored exact URI and cannot broaden origins', async () => { const f = fixture(); f.state.items[0].login.uris.push({ uri: 'https://sso.example.invalid', match: 1 }); f.request.trustedOrigins = ['https://sso.example.invalid']; assert.equal((await execute(f)).ok, true); f.request.trustedOrigins = ['https://evil.example.invalid']; assert.equal((await execute(f)).code, 'MAPPING_NOT_IN_VAULT'); });
test('ambiguous requires ID; no item fails', async () => { const f = fixture(); f.state.items.push({ ...item(), id: '22222222-2222-2222-2222-222222222222' }); assert.equal((await execute(f)).code, 'AMBIGUOUS_ITEMS'); f.request.itemId = id; assert.equal((await execute(f)).ok, true); f.state.items = []; assert.equal((await execute(f)).code, 'NO_MATCHING_ITEM'); });
test('metadata only, no vault strings', async () => { const f = fixture(); f.request.action = 'list'; const r = await execute(f); assert.equal(r.items[0].id, id); redacted(r); assert.equal(f.state.inspections, 0); });
test('stale origin between fields leaves partial fill recorded', async () => { const f = fixture(), inspect = f.browser.inspect; f.browser.inspect = async (...args) => ({ ...await inspect(...args), url: f.state.typed.length ? 'https://evil.example.invalid' : site }); const r = await execute(f); assert.equal(r.code, 'ORIGIN_CHANGED'); assert.deepEqual(r.filled, ['username']); });
test('second guard detects changed target', async () => { const f = fixture(), inspect = f.browser.inspect; f.browser.inspect = async (...args) => ({ ...await inspect(...args), count: f.state.inspections > 1 ? 2 : 1 }); assert.equal((await execute(f)).code, 'TARGET_CHANGED'); assert.equal(f.state.typed.length, 0); });
for (const patch of [{ top: false },{ count: 2 },{ count: 0 },{ visible: false },{ disabled: true },{ readOnly: true },{ tag: 'DIV' },{ type: 'hidden' },{ actions: ['https://evil.example.invalid'] },{ actions: ['javascript:alert(1)'] }]) test('hostile field ' + JSON.stringify(patch), async () => { const f = fixture(), inspect = f.browser.inspect; f.browser.inspect = async (...a) => ({ ...await inspect(...a), ...patch }); assert.equal((await execute(f)).ok, false); assert.equal(f.state.typed.length, 0); });
test('dry-run has no browser mutation or TOTP generation', async () => { const f = fixture(); f.request.action = 'dry-run'; f.request.fields.totp = '#otp'; assert.equal((await execute(f)).stage, 'validated'); assert.equal(f.state.typed.length, 0); assert.equal(f.state.codes, 0); });
for (const component of ['status','items','totp','inspect','type']) test('exception redaction ' + component, async () => { const f = fixture(); if (component === 'totp') f.request.fields = { totp: '#otp' }; (component === 'inspect' || component === 'type' ? f.browser : f.vault)[component] = async () => { throw new Error(secret + '123456'); }; const r = await execute(f); assert.equal(r.ok, false); redacted(r); });
test('selector syntax failure is redacted', async () => { const f = fixture(); f.browser.inspect = async () => { throw new SyntaxError(secret); }; redacted(await execute(f)); });
test('vault identity mismatch blocks before lookup', async () => { const f = fixture(); f.vault.status = async () => ({ status: 'unlocked', serverUrl: 'https://evil.example.invalid' }); assert.equal((await execute(f)).code, 'VAULT_IDENTITY_MISMATCH'); });
test('captured process timeout and stderr never expose payload', async () => { await assert.rejects(captured(process.execPath, ['-e', 'process.stderr.write("SYNTHETIC_PASSWORD_MARKER");setTimeout(()=>{},1000)'], childEnv(), 25), e => e.code === 'SUBPROCESS_TIMEOUT' && !String(e).includes('MARKER')); });
test('child env allowlist and reuse session; no secret args', async () => { const calls = []; const v = createVault({ profile, env: { PATH: '/bin', BW_SESSION: 'SESSION_MARKER', OTHER_SECRET: secret }, run: async (file, args, env) => { calls.push({ file, args, env }); return args[0] === 'status' ? '{}' : '[]'; } }); await v.status(); await v.items(); assert.equal(calls[0].env.BW_SESSION, 'SESSION_MARKER'); assert.equal(calls[0].env.OTHER_SECRET, undefined); assert.ok(!JSON.stringify(calls.map(c => c.args)).includes('MARKER')); });
test('keychain password only in unlock env; session only bw env', async () => { const calls = []; const v = createVault({ profile, env: { BW_SESSION: 'OLD_MARKER' }, run: async (file,args,env) => { calls.push({file,args,env}); return file.includes('security') ? 'MASTER_MARKER\n' : args[0] === 'unlock' ? 'SESSION_MARKER' : '[]'; } }); await v.unlock(); await v.items(); assert.equal(calls[0].env.BW_SESSION, undefined); assert.equal(calls[1].env.BW_PASSWORD, 'MASTER_MARKER'); assert.equal(calls[1].env.BW_SESSION, undefined); assert.equal(calls[2].env.BW_PASSWORD, undefined); assert.equal(calls[2].env.BW_SESSION, 'SESSION_MARKER'); assert.ok(!JSON.stringify(calls.map(c => c.args)).includes('MARKER')); });
test('fresh TOTP waits out short window', async () => { let time = 25000, slept = 0; const v = createVault({ profile, now: () => time, sleep: async ms => { slept += ms; time += ms; }, run: async () => '123456' }); assert.equal((await v.totp(item())).code, '123456'); assert.equal(slept, 5100); });
test('slow TOTP fails closed; unsupported seeds fail', async () => { let time = 0; const v = createVault({ profile, now: () => time, run: async () => { time = 25000; return '123456'; } }); await assert.rejects(v.totp(item()), { code: 'TOTP_TOO_OLD' }); const i = item(); i.login.totp = 'steam://seed'; await assert.rejects(v.totp(i), { code: 'UNSUPPORTED_TOTP' }); });
test('fixed inspector source has no secret values and escapes selector', () => { const s = inspectionExpression('input[title="\" ) evil()"]'); assert.ok(!s.includes('.value')); assert.ok(!s.includes('innerText')); assert.ok(s.includes('querySelectorAll')); assert.equal(origin(site + '/path'), site); });


test('contract payload echo discarded and arguments fixed', async () => {
  const { browserFromContract } = await import('./runtime.mjs');
  const f = fixture(), original = f.browser.inspect, calls = [];
  f.browser = browserFromContract({ runTool: async (name,args) => { calls.push({ name,args }); return { payload: name === 'camofox_evaluate' ? { ok: true, result: await original(args.tabId, args.expression.includes('#p') ? '#p' : '#u') } : { ok: true, echoed: secret } }; } });
  const r = await execute(f); assert.equal(r.ok, true); redacted(r);
  for (const c of calls) if (c.name === 'camofox_evaluate') assert.ok(!c.args.expression.includes(secret)); else { assert.equal(c.args.pressEnter, false); assert.deepEqual(Object.keys(c.args).sort(), ['pressEnter','selector','tabId','text']); }
});
test('contract timeout stops with unknown outcome and no retry', async () => {
  const { browserFromContract } = await import('./runtime.mjs'); const f = fixture(); let calls = 0;
  const transport = browserFromContract({ timeoutMs: 2, runTool: async () => { calls++; return new Promise(() => {}); } });
  f.browser.type = transport.type;
  const r = await execute(f); assert.equal(r.code, 'BROWSER_TIMEOUT'); assert.equal(r.outcome, 'unknown-partial-fill-possible'); assert.equal(calls, 1);
});
test('TOTP expires during second inspection: never typed', async () => { const f = fixture(); f.request.fields = { totp: '#otp' }; f.now = () => Date.now() + 25000; assert.equal((await execute(f)).code, 'TOTP_TOO_OLD'); assert.equal(f.state.typed.length, 0); });
test('unsupported unrelated item does not prevent exact match', async () => { const f = fixture(); const other = item(); other.id = '22222222-2222-2222-2222-222222222222'; other.login.uris = [{ uri: 'evil.*', match: 4 }]; f.state.items.push(other); assert.equal((await execute(f)).ok, true); });
test('inspector executes against synthetic DOM, ignores value', async () => {
  const { runInNewContext } = await import('node:vm');
  const e = { value: secret, tagName: 'INPUT', type: 'password', hidden: false, readOnly: false, form: { action: site + '/login', target: '', elements: [] }, matches: () => false, closest: () => null, getBoundingClientRect: () => ({ width: 20, height: 10 }), getClientRects: () => [1] };
  const window = {}; window.top = window;
  const ctx = { document: { querySelectorAll: () => [e] }, location: { origin: site, href: site + '/login' }, window, URL, getComputedStyle: () => ({ display: 'block', visibility: 'visible', opacity: '1' }) };
  const r = runInNewContext(inspectionExpression('#p'),ctx); assert.equal(r.visible,true); assert.equal(r.type,'password'); redacted(r);
  e.form.elements.push({ hasAttribute: x => x === 'formaction', formAction: 'https://evil.example.invalid' }); assert.equal(runInNewContext(inspectionExpression('#p'),ctx).actions[1], 'https://evil.example.invalid');
});

// Review regressions: use real child-process stdout bytes, not a mock backslash-n.
test('actual subprocess newline trimmed from Keychain output', async () => {
  for (const ending of ['LF','CRLF']) {
    const v = createVault({ profile, env: {}, run: async (file,args,env) => {
      if (file.includes('security')) return captured(process.execPath, ['-e', 'process.stdout.write("MASTER_MARKER" + String.fromCharCode(' + (ending === 'LF' ? '10' : '13,10') + '))'], childEnv());
      assert.equal(env.BW_PASSWORD, 'MASTER_MARKER'); return 'SESSION_MARKER';
    } }); await v.unlock();
  }
});
test('CLI writes actual JSON newline, not literal escape', () => {
  const { spawnSync } = process.getBuiltinModule('node:child_process');
  const r = spawnSync(process.execPath, ['cli.mjs'], { input: '{"unexpected":true}', encoding: 'utf8', env: childEnv() });
  assert.equal(r.stdout.charCodeAt(r.stdout.length - 1), 10);
  assert.equal(JSON.parse(r.stdout).code, 'UNKNOWN_REQUEST_KEY'); assert.ok(!r.stdout.includes(String.fromCharCode(92) + 'n'));
});
test('bare DNS and origin-only URI shape works without weakening host matching', async () => {
  const { authorized } = await import('./bridge.mjs'); const i = item();
  i.login.uris = [{uri:'https://app.example.invalid'}, {uri:'sso.example.invalid'}, {uri:'https://sso.example.invalid',match:2}];
  assert.equal(authorized(i,'https://sso.example.invalid'),true); assert.equal(authorized(i,'https://app.example.invalid'),true);
  for (const bad of ['https://sso.example.invalid.evil.example.invalid','https://sub.sso.example.invalid','https://example.invalid','https://sso.example.invalid:444']) assert.equal(authorized(i,bad),false);
});
test('starts-with origin-only narrows exactly; path/query rules excluded per entry', async () => {
  const { authorized } = await import('./bridge.mjs'); const i = item();
  i.login.uris = [{uri:site,match:2}]; assert.equal(authorized(i,site),true); assert.equal(authorized(i,site+'.evil.example.invalid'),false);
  for (const uri of [site+'/login',site+'/?x=1',site+'/#fragment']) {i.login.uris = [{uri,match:2}]; assert.equal(authorized(i,site),false);}
  i.login.uris.push({uri:site,match:1}); assert.equal(authorized(i,site),true);
});
test('invalid/unsupported entries do not mask separate safe URI', async () => {
  const { authorized } = await import('./bridge.mjs'); const i = item();
  i.login.uris.push({uri:'evil.*',match:4},{uri:'bad/path'},{uri:site,match:5}); assert.equal(authorized(i,site),true);
  for (const uri of ['login.example.invalid/path','login.example.invalid:443','a@login.example.invalid','login.example.invalid.evil.example.invalid']) {i.login.uris = [{uri}];assert.equal(authorized(i,site),false);}
});
