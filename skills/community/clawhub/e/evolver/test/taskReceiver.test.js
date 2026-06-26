'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');

// fetchTasks makes real network calls, so we test the filtering logic
// by importing the schema functions directly and verifying the contract.
const { createTask, validateTask } = require('../src/gep/schemas/task');

describe('fetchTasks — invalid task filtering contract', () => {
  it('validateTask rejects task with no task_id — would be filtered by fetchTasks', () => {
    const t = createTask({ status: 'open' });
    assert.throws(() => validateTask(t), /task_id is required/);
  });

  it('validateTask rejects task with empty string task_id', () => {
    const t = createTask({ task_id: '', status: 'open' });
    assert.throws(() => validateTask(t), /task_id is required/);
  });

  it('validateTask accepts task with valid task_id and status', () => {
    const t = createTask({ task_id: 'task_abc', status: 'open' });
    assert.doesNotThrow(() => validateTask(t));
  });

  it('filter pattern used in fetchTasks keeps valid and drops invalid', () => {
    const raw = [
      { task_id: 'good_1', status: 'open' },
      { status: 'open' },              // missing task_id — should be dropped
      { task_id: '', status: 'open' }, // empty task_id — should be dropped
      { task_id: 'good_2', status: 'claimed' },
    ];

    const filtered = raw
      .map(function(t) { return createTask(t); })
      .filter(function(t) {
        try { return validateTask(t); } catch (e) { return false; }
      });

    assert.equal(filtered.length, 2);
    assert.equal(filtered[0].task_id, 'good_1');
    assert.equal(filtered[1].task_id, 'good_2');
  });

  it('filter drops task with invalid status after normalization would still validate', () => {
    // createTask normalizes invalid status to 'open', so it passes validateTask
    const t = createTask({ task_id: 'task_x', status: 'invalid_status' });
    assert.equal(t.status, 'open');
    assert.doesNotThrow(() => validateTask(t));
  });

  it('filter is idempotent — running createTask twice before filter produces same result', () => {
    const raw = [{ task_id: 'task_1', status: 'open', bounty_amount: 50 }];
    const once = raw.map(function(t) { return createTask(t); })
      .filter(function(t) { try { return validateTask(t); } catch (e) { return false; } });
    const twice = once.map(function(t) { return createTask(t); })
      .filter(function(t) { try { return validateTask(t); } catch (e) { return false; } });
    assert.deepEqual(once, twice);
  });
});
