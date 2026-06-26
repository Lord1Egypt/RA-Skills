const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const savedEnv = {};
const envKeys = ['EVOLVER_ATP_PICKUP', 'MEMORY_DIR'];

let tmpMemoryDir;
let pickup;
let hubClient;
let origListMyTasks;

function makeTmpMemoryDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'atp-pickup-'));
}

beforeEach(() => {
  for (const k of envKeys) {
    savedEnv[k] = process.env[k];
    delete process.env[k];
  }
  tmpMemoryDir = makeTmpMemoryDir();
  process.env.MEMORY_DIR = tmpMemoryDir;

  for (const key of Object.keys(require.cache)) {
    if (key.includes('/src/atp/') || key.includes('/src/gep/paths')) {
      delete require.cache[key];
    }
  }
  pickup = require('../src/atp/atpTaskPickup');
  hubClient = require('../src/atp/hubClient');
  origListMyTasks = hubClient.listMyTasks;
});

afterEach(() => {
  if (origListMyTasks) hubClient.listMyTasks = origListMyTasks;
  for (const k of envKeys) {
    if (savedEnv[k] === undefined) delete process.env[k];
    else process.env[k] = savedEnv[k];
  }
  try { fs.rmSync(tmpMemoryDir, { recursive: true, force: true }); } catch (_) {}
});

describe('atpTaskPickup._isEnabled', () => {
  it('is on by default', () => {
    assert.equal(pickup._isEnabled(), true);
  });
  it('respects EVOLVER_ATP_PICKUP=off', () => {
    process.env.EVOLVER_ATP_PICKUP = 'off';
    assert.equal(pickup._isEnabled(), false);
  });
  it('respects EVOLVER_ATP_PICKUP=0', () => {
    process.env.EVOLVER_ATP_PICKUP = '0';
    assert.equal(pickup._isEnabled(), false);
  });
});

describe('atpTaskPickup._isEligible', () => {
  it('accepts ATP tasks without a result_asset_id', () => {
    const ok = pickup._isEligible({ id: 't1', atp_order_id: 'p1', status: 'claimed' });
    assert.equal(ok, true);
  });
  it('rejects tasks with no atp_order_id', () => {
    assert.equal(pickup._isEligible({ id: 't1', status: 'claimed' }), false);
  });
  it('rejects tasks that already have a result_asset_id', () => {
    assert.equal(pickup._isEligible({
      id: 't1', atp_order_id: 'p1', status: 'claimed', result_asset_id: 'sha256:abc',
    }), false);
  });
  it('rejects completed tasks', () => {
    assert.equal(pickup._isEligible({ id: 't1', atp_order_id: 'p1', status: 'completed' }), false);
  });
  it('rejects tasks without id', () => {
    assert.equal(pickup._isEligible({ atp_order_id: 'p1', status: 'claimed' }), false);
  });
});

describe('atpTaskPickup._buildSpawnTask', () => {
  it('embeds key task fields in the spawn prompt', () => {
    const task = {
      id: 'task_abc',
      atp_order_id: 'proof_xyz',
      title: 'Help me debug a bug',
      user_question_body: 'I have a null-pointer in foo.js line 42',
      capabilities: ['debugging'],
      signals: 'log_error',
    };
    const prompt = pickup._buildSpawnTask(task);
    assert.ok(prompt.includes('task_abc'));
    assert.ok(prompt.includes('proof_xyz'));
    assert.ok(prompt.includes('debugging'));
    assert.ok(prompt.includes('null-pointer'));
    assert.ok(prompt.includes('atp-complete'));
    assert.ok(prompt.includes('--task-id=task_abc'));
    assert.ok(prompt.includes('--order-id=proof_xyz'));
  });

  it('works when buyer question is missing', () => {
    const prompt = pickup._buildSpawnTask({
      id: 't1', atp_order_id: 'p1', capabilities: [], signals: '',
    });
    assert.ok(prompt.includes('buyer did not provide a question body'));
  });

  it('clips extremely long buyer questions', () => {
    const longQ = 'x'.repeat(50000);
    const prompt = pickup._buildSpawnTask({
      id: 't1', atp_order_id: 'p1', user_question_body: longQ,
    });
    assert.ok(prompt.length < 20000, 'spawn prompt should be clipped well under 20k chars, got ' + prompt.length);
  });
});

describe('atpTaskPickup.pickOne', () => {
  it('returns null when Hub has no tasks', async () => {
    hubClient.listMyTasks = async () => ({ ok: true, data: { tasks: [] } });
    const r = await pickup.pickOne({ limit: 5 });
    assert.equal(r, null);
  });

  it('returns null when Hub call fails', async () => {
    hubClient.listMyTasks = async () => ({ ok: false, error: 'network' });
    const r = await pickup.pickOne({ limit: 5 });
    assert.equal(r, null);
  });

  it('returns null when disabled via env', async () => {
    process.env.EVOLVER_ATP_PICKUP = 'off';
    const r = await pickup.pickOne({ limit: 5 });
    assert.equal(r, null);
  });

  it('returns a spawn call when an eligible ATP task is available', async () => {
    hubClient.listMyTasks = async () => ({
      ok: true,
      data: {
        tasks: [
          { id: 't_done', atp_order_id: 'p1', status: 'claimed', result_asset_id: 'sha256:x' },
          { id: 't_no_atp', status: 'claimed' },
          { id: 't_target', atp_order_id: 'p2', status: 'claimed', title: 'pick me', user_question_body: 'q' },
        ],
      },
    });
    const r = await pickup.pickOne({ limit: 5 });
    assert.ok(r, 'expected a pick');
    assert.equal(r.task.id, 't_target');
    assert.ok(r.spawnCall.startsWith('sessions_spawn('));
    assert.ok(r.spawnCall.includes('atp_pickup'));
  });

  it('does not respawn the same task within the cooldown window', async () => {
    let listCalls = 0;
    hubClient.listMyTasks = async () => {
      listCalls++;
      return {
        ok: true,
        data: {
          tasks: [
            { id: 't_sticky', atp_order_id: 'p_sticky', status: 'claimed', title: 't', user_question_body: 'q' },
          ],
        },
      };
    };
    const first = await pickup.pickOne({ limit: 5 });
    assert.ok(first);
    const second = await pickup.pickOne({ limit: 5 });
    assert.equal(second, null, 'cooldown should block the second pick for the same task');
    assert.equal(listCalls, 2);
  });

  it('forget() allows the same task to be picked again', async () => {
    hubClient.listMyTasks = async () => ({
      ok: true,
      data: {
        tasks: [
          { id: 't_retry', atp_order_id: 'p_retry', status: 'claimed', title: 't', user_question_body: 'q' },
        ],
      },
    });
    const first = await pickup.pickOne({ limit: 5 });
    assert.ok(first);
    pickup.forget('t_retry');
    const second = await pickup.pickOne({ limit: 5 });
    assert.ok(second, 'expected second pick after forget()');
  });
});
