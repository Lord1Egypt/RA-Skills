const { describe, it, before, after, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const {
  sendHeartbeat,
  getHubEvents,
  consumeHubEvents,
} = require('../src/gep/a2aProtocol');

describe('consumeHubEvents / getHubEvents', () => {
  let originalFetch;
  let originalHubUrl;
  let originalLogsDir;
  let tmpDir;

  let originalInsecure;

  before(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-hub-events-'));
    originalHubUrl = process.env.A2A_HUB_URL;
    originalLogsDir = process.env.EVOLVER_LOGS_DIR;
    originalInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    process.env.A2A_HUB_URL = 'http://localhost:19998';
    process.env.EVOLVER_LOGS_DIR = tmpDir;
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    originalFetch = global.fetch;
  });

  after(() => {
    global.fetch = originalFetch;
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    if (originalLogsDir === undefined) delete process.env.EVOLVER_LOGS_DIR;
    else process.env.EVOLVER_LOGS_DIR = originalLogsDir;
    if (originalInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = originalInsecure;
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('consumeHubEvents returns empty array when no events buffered', () => {
    const events = consumeHubEvents();
    assert.ok(Array.isArray(events));
  });

  it('getHubEvents returns empty array when no events buffered', () => {
    const events = getHubEvents();
    assert.ok(Array.isArray(events));
    assert.equal(events.length, 0);
  });

  it('fetches events when heartbeat returns has_pending_events:true', async () => {
    let pollCalled = false;
    const fakeEvents = [
      { type: 'dialog_message', payload: { text: 'hello' } },
      { type: 'task_available', payload: { task_id: 't1' } },
    ];

    global.fetch = async (url, opts) => {
      if (url.includes('/a2a/events/poll')) {
        pollCalled = true;
        return { ok: true, status: 200, json: async () => ({ events: fakeEvents }) };
      }
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok', has_pending_events: true }),
        text: async () => '',
      };
    };

    const logPath = path.join(tmpDir, 'evolver_loop.log');
    fs.writeFileSync(logPath, '');

    await sendHeartbeat();
    // _fetchHubEvents is async-fire-and-forget from heartbeat;
    // give it a tick to settle
    await new Promise(r => setTimeout(r, 100));

    assert.ok(pollCalled, 'should call /a2a/events/poll when has_pending_events is true');

    const buffered = getHubEvents();
    assert.ok(buffered.length >= 2, 'should buffer the fetched events');
    assert.equal(buffered[buffered.length - 2].type, 'dialog_message');
    assert.equal(buffered[buffered.length - 1].type, 'task_available');

    const consumed = consumeHubEvents();
    assert.ok(consumed.length >= 2, 'consumeHubEvents should return buffered events');

    const afterConsume = getHubEvents();
    assert.equal(afterConsume.length, 0, 'buffer should be empty after consume');
  });

  it('does not call events/poll when has_pending_events is falsy', async () => {
    let pollCalled = false;
    global.fetch = async (url) => {
      if (url.includes('/a2a/events/poll')) {
        pollCalled = true;
        return { ok: true, status: 200, json: async () => ({ events: [] }) };
      }
      return { ok: true, status: 200, json: async () => ({ status: 'ok' }), text: async () => '' };
    };

    const logPath = path.join(tmpDir, 'evolver_loop.log');
    fs.writeFileSync(logPath, '');

    await sendHeartbeat();
    await new Promise(r => setTimeout(r, 100));

    assert.ok(!pollCalled, 'should NOT call /a2a/events/poll when has_pending_events is absent');
  });

  it('handles poll returning events in payload.events format', async () => {
    const fakeEvents = [{ type: 'council_invite', payload: {} }];
    global.fetch = async (url) => {
      if (url.includes('/a2a/events/poll')) {
        return { ok: true, status: 200, json: async () => ({ payload: { events: fakeEvents } }) };
      }
      return { ok: true, status: 200, json: async () => ({ status: 'ok', has_pending_events: true }), text: async () => '' };
    };

    const logPath = path.join(tmpDir, 'evolver_loop.log');
    fs.writeFileSync(logPath, '');

    consumeHubEvents();
    await sendHeartbeat();
    await new Promise(r => setTimeout(r, 100));

    const events = consumeHubEvents();
    assert.ok(events.some(e => e.type === 'council_invite'), 'should parse payload.events format');
  });
});
