import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createHmac, randomUUID } from 'node:crypto';
import { once } from 'node:events';
import { mkdir, mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { createServer } from 'node:net';
import { tmpdir } from 'node:os';
import { basename, join, resolve } from 'node:path';
import { setTimeout as delay } from 'node:timers/promises';
import test from 'node:test';
import twilio from 'twilio';
import { runLocalHelper } from '../dist/local-helper-runner.js';
import { callSkillDirectly, handleSkillCall, registerSkills } from '../dist/skills/router.js';

test('signed inbound calls keep caller context, query calendars on demand, and preserve screening state', async (t) => {
  const dir = await mkdtemp(join(tmpdir(), 'amber-screening-'));
  await mkdir(join(dir, 'data'));
  await writeFile(join(dir, 'data', 'bridge-outbound-map.json'), JSON.stringify({
    approved: { key: 'approved', objective: 'Ask for business hours', createdAtMs: Date.now() },
  }));
  const captures = join(dir, 'accepts.jsonl');
  const calendarTrace = join(dir, 'calendar.jsonl');
  const mockSocket = join(dir, 'mock-websocket.mjs');
  await writeFile(mockSocket, `
import { EventEmitter } from 'node:events';
import { appendFileSync } from 'node:fs';

const trace = (entry) => appendFileSync(${JSON.stringify(calendarTrace)}, JSON.stringify(entry) + '\\n');
export default class extends EventEmitter {
  constructor(url) {
    super();
    if (!String(url).endsWith('call_calendar')) throw new Error('Unexpected call socket');
    setImmediate(() => {
      this.emit('open');
      setImmediate(() => {
        trace({ type: 'requested' });
        this.emit('message', Buffer.from(JSON.stringify({
          type: 'response.function_call_arguments.done',
          item_id: 'availability',
          name: 'ask_openclaw',
          arguments: JSON.stringify({ question: 'Is Friday at 2 PM available for an appointment?' }),
        })));
      });
    });
  }
  send(body) {
    const item = JSON.parse(body).item;
    if (item?.type === 'function_call_output') trace({ type: 'output', result: JSON.parse(item.output) });
  }
}
`);
  const loader = join(dir, 'mock-websocket-loader.mjs');
  await writeFile(loader, `
import { pathToFileURL } from 'node:url';
export function resolve(specifier, context, nextResolve) {
  if (specifier === 'ws' && context.parentURL === pathToFileURL(${JSON.stringify(resolve('dist/index.js'))}).href) {
    return { url: pathToFileURL(${JSON.stringify(mockSocket)}).href, shortCircuit: true };
  }
  return nextResolve(specifier, context);
}
`);
  const preload = join(dir, 'mock-openai.mjs');
  await writeFile(preload, `
import { appendFileSync } from 'node:fs';
import { register } from 'node:module';
import { pathToFileURL } from 'node:url';
register(pathToFileURL(${JSON.stringify(loader)}));
const trace = (entry) => appendFileSync(${JSON.stringify(calendarTrace)}, JSON.stringify(entry) + '\\n');

globalThis.fetch = async (url, init) => {
  const destination = String(url);
  if (destination === 'https://gateway.example.test/v1/chat/completions') {
    const request = JSON.parse(init.body);
    trace({ type: 'gateway', question: JSON.parse(request.messages[1].content).question });
    return Response.json({ choices: [{ message: { content: 'Friday at 2 PM is free.' } }] });
  }
  if (!destination.startsWith('https://api.openai.com/v1/realtime/calls/')) {
    throw new Error('Unexpected network request from bridge test');
  }
  if (destination.endsWith('/call_calendar/accept')) return Response.json({});
  appendFileSync(${JSON.stringify(captures)}, init.body + '\\n');
  return new Response('Test stops before starting a call socket', { status: 500 });
};
`);

  const caller = '+12025550142';
  const account = 'AC' + '0'.repeat(32);
  const providerKey = 'twilio-fixture';
  const webhookKey = 'openai-fixture';
  const bridgeToken = 'bridge-fixture';
  const entry = resolve('dist/index.js');
  let child;
  let base;
  async function stop() {
    if (child?.exitCode === null && child.signalCode === null) {
      const stopped = once(child, 'exit');
      child.kill();
      await stopped;
    }
  }
  t.after(async () => {
    await stop();
    await rm(dir, { recursive: true, force: true });
  });
  async function start() {
    const reserve = createServer().listen(0, '127.0.0.1');
    await once(reserve, 'listening');
    const { port } = reserve.address();
    await new Promise((done) => reserve.close(done));
    base = `http://127.0.0.1:${port}`;
    child = spawn(process.execPath, ['--import', preload, entry], {
      cwd: dir,
      env: {
        PATH: process.env.PATH,
        NODE_ENV: 'test',
        PORT: String(port),
        PUBLIC_BASE_URL: base,
        TWILIO_ACCOUNT_SID: account,
        TWILIO_AUTH_TOKEN: providerKey,
        TWILIO_CALLER_ID: '+12025550123',
        GENZ_CALLER_NUMBERS: caller,
        OPENAI_API_KEY: 'test-only',
        OPENCLAW_GATEWAY_URL: 'https://gateway.example.test',
        OPENCLAW_GATEWAY_TOKEN: 'test-only',
        OPENAI_PROJECT_ID: 'test-only',
        OPENAI_WEBHOOK_SECRET: webhookKey,
        BRIDGE_API_TOKEN: bridgeToken,
      },
      stdio: 'ignore',
    });
    for (let attempt = 0; attempt < 100; attempt += 1) {
      if (child.exitCode !== null) break;
      const health = await fetch(base + '/healthz').catch(() => null);
      if (health?.ok) return;
      await delay(25);
    }
    assert.fail('Bridge never became healthy');
  }

  async function twilioInbound(from, sid) {
    const url = base + '/twilio/inbound';
    const params = { AccountSid: account, From: from, CallSid: sid };
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'x-twilio-signature': twilio.getExpectedTwilioSignature(providerKey, url, params) },
      body: new URLSearchParams(params),
    });
    assert.equal(response.status, 200);
    return response.text();
  }

  async function realtime(callId, headers, expectedStatus = 500) {
    const body = JSON.stringify({
      type: 'realtime.call.incoming',
      data: { call_id: callId, sip_headers: headers },
    });
    const timestamp = String(Math.floor(Date.now() / 1000));
    const id = randomUUID();
    const signature = createHmac('sha256', webhookKey).update(`${id}.${timestamp}.${body}`).digest('base64');
    const response = await fetch(base + '/openai/webhook', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'webhook-id': id,
        'webhook-timestamp': timestamp,
        'webhook-signature': `v1,${signature}`,
      },
      body,
    });
    assert.equal(response.status, expectedStatus);
    if (expectedStatus === 500) {
      const last = (await readFile(captures, 'utf8')).trim().split('\n').at(-1);
      return JSON.parse(last).instructions;
    }
  }

  function setScreening(enabled, authenticated = true) {
    return fetch(base + '/screening', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        ...(authenticated && { authorization: `Bearer ${bridgeToken}` }),
      },
      body: JSON.stringify({ enabled }),
    });
  }

  await start();
  await realtime('call_calendar', [], 200);
  let calendarEvents = [];
  for (let attempt = 0; attempt < 100; attempt += 1) {
    const contents = await readFile(calendarTrace, 'utf8').catch(() => '');
    calendarEvents = contents.trim().split('\n').filter(Boolean).map((line) => JSON.parse(line));
    if (calendarEvents.some(({ type }) => type === 'output')) break;
    await delay(25);
  }
  assert.deepEqual(calendarEvents, [
    { type: 'requested' },
    { type: 'gateway', question: 'Is Friday at 2 PM available for an appointment?' },
    { type: 'output', result: { answer: 'Friday at 2 PM is free.' } },
  ]);

  const firstSid = 'CA' + '1'.repeat(32);
  const first = await twilioInbound(caller, firstSid);
  const second = await twilioInbound('+12025550143', 'CA' + '2'.repeat(32));
  const token = /[?]x-amber-inbound=([a-f0-9]{32})/;
  const firstToken = first.match(token)?.[1];
  const secondToken = second.match(token)?.[1];
  assert.ok(firstToken && secondToken);
  assert.notEqual(firstToken, secondToken);

  const unknown = await realtime('call_unknown', []);
  const header = (value) => [{ name: 'X-Amber-Inbound', value }];
  const firstInstructions = await realtime('call_first', header(firstToken));
  assert.notEqual(firstInstructions, unknown, 'the signed caller keeps its personalized greeting');
  assert.equal(await realtime('call_second', header(secondToken)), unknown);
  assert.equal(await realtime('call_replay', header(firstToken)), unknown);
  assert.equal(await realtime('call_sid_only', [{ name: 'X-Twilio-CallSid', value: firstSid }]), unknown);
  assert.equal(await realtime('call_first', header(firstToken)), firstInstructions, 'a retry can still resolve the same call');

  await realtime('call_log_privacy', [...header(secondToken), { name: 'X-Debug', value: 'private metadata' }]);
  const logsDir = join(dir, 'logs');
  const metadataFile = (await readdir(logsDir)).find(name => name.endsWith('_call_log_privacy.realtime.call.incoming.json'));
  assert.ok(metadataFile);
  const metadata = JSON.parse(await readFile(join(logsDir, metadataFile), 'utf8'));
  assert.deepEqual(metadata.data.callRouting, {
    direction: 'inbound', from: null, to: '+12025550123', twilioCallSid: null, bridgeId: null,
  });
  assert.deepEqual(Object.keys(metadata.data).sort(), ['callRouting', 'call_id']);

  assert.equal((await setScreening(false, false)).status, 401);
  assert.deepEqual(await (await setScreening(false)).json(), { enabled: false });
  const paused = await twilioInbound(caller, firstSid);
  assert.match(paused, /<Reject reason="busy"/);
  assert.doesNotMatch(paused, /<Dial/);
  const beforePausedCall = await readFile(captures, 'utf8');
  await realtime('call_paused', [], 200);
  assert.equal(await readFile(captures, 'utf8'), beforePausedCall);
  const outbound = await realtime('call_outbound', [{ name: 'X-Bridge-Id', value: 'approved' }]);
  assert.match(outbound, /Ask for business hours/);

  await stop();
  await start();
  assert.match(await twilioInbound(caller, firstSid), /<Reject reason="busy"/);
  assert.deepEqual(await (await setScreening(true)).json(), { enabled: true });
  assert.match(await twilioInbound(caller, firstSid), /<Dial/);
});

test('built-in calendar writes and messages require confirmation even with an opt-out manifest', async () => {
  const executions = [];
  const outputs = [];
  registerSkills(['calendar_query', 'send_message', 'crm'].map((name) => ({
    manifest: { name, amber: {
      function_schema: { name },
      capabilities: ['read', 'act'],
      confirmation_required: false,
      permissions: {},
      timeout_ms: 1,
    } },
    handler: async (params) => {
      executions.push([name, params.action]);
      return { success: true };
    },
  })));
  const call = (name, args) => handleSkillCall(name, JSON.stringify(args), null, 'function-call', {
    operatorName: 'Operator',
    callId: 'call',
    callerId: '+12025550142',
    transcript: '',
    clawdClient: null,
    writeJsonl: () => {},
    sendFunctionCallOutput: (_, __, output) => outputs.push(JSON.parse(output)),
  });
  await call('calendar_query', { action: 'create' });
  await call('send_message', { message: 'Call me back' });
  assert.ok(outputs.every((output) => output.requires_confirmation));
  assert.equal(executions.length, 0);

  await call('calendar_query', { action: 'lookup' });
  await call('calendar_query', { action: 'create', confirmed: true });
  await call('crm', { action: 'upsert_contact' });
  assert.deepEqual(executions, [
    ['calendar_query', 'lookup'],
    ['calendar_query', 'create'],
    ['crm', 'upsert_contact'],
  ]);
});

test('local helper permits the approved path and denies same-name executables at another path', async () => {
  const args = ['-p', '1 + 1'];
  const file = process.execPath;
  assert.equal(await runLocalHelper(file, args, { allowedBinaries: [file] }), '2');
  await assert.rejects(runLocalHelper(file, args, { allowedBinaries: [basename(file)] }), /not in allowed list/);
});

test('live-call CRM is bound to the call contact and the internal CRM path remains available', async () => {
  const contactPhone = '+12025550142';
  const otherPhone = '+12025550143';
  const executions = [];
  registerSkills([{
    manifest: { name: 'crm', amber: {
      function_schema: { name: 'crm' },
      capabilities: ['read', 'act'],
      confirmation_required: false,
      permissions: {},
      timeout_ms: 100,
    } },
    handler: async (params) => {
      executions.push(params);
      return { success: true };
    },
  }]);
  const context = {
    operatorName: 'Operator',
    callId: 'call',
    callerId: contactPhone,
    transcript: '',
    clawdClient: null,
    writeJsonl: () => {},
  };
  async function call(params, callerId = contactPhone) {
    let result;
    await handleSkillCall('crm', JSON.stringify(params), null, 'function-call', {
      ...context,
      callerId,
      sendFunctionCallOutput: (_ws, _id, output) => { result = JSON.parse(output); },
    });
    return result;
  }

  for (const action of ['upsert_contact', 'log_interaction', 'tag_contact', 'lookup_contact', 'get_history']) {
    assert.equal((await call({ action, phone: otherPhone })).success, false);
  }
  assert.equal((await call({ action: 'search_contacts', query: 'Alex' })).success, false);
  assert.equal((await call({ action: 'upsert_contact', phone: contactPhone }, '')).success, false);
  assert.equal(executions.length, 0);

  assert.equal((await call({ action: 'upsert_contact', name: 'Alex' })).success, true);
  assert.equal((await call({ action: 'log_interaction', phone: contactPhone })).success, true);
  assert.equal((await callSkillDirectly('crm', { action: 'lookup_contact', phone: otherPhone }, context)).success, true);
  assert.deepEqual(executions.map(({ phone }) => phone), [contactPhone, contactPhone, otherPhone]);
});
