const { test } = require('node:test');
const assert = require('node:assert/strict');
const { parseDue, dueBucket, parseArgs } = require('../lib/cli');

const now = new Date(2026, 10, 6, 12, 0);

test('a due date is a day, a day and time, or today / tomorrow', () => {
  assert.deepEqual(parseDue('2026-11-10', now), { date: '2026-11-10', time: null });
  assert.deepEqual(parseDue('2026-11-10 9:05', now), { date: '2026-11-10', time: '09:05' });
  assert.deepEqual(parseDue('tomorrow 18:30', now), { date: '2026-11-07', time: '18:30' });
  assert.throws(() => parseDue('2026-02-30', now));
  assert.throws(() => parseDue('next week', now));
});

test('a timed reminder is overdue once its minute passes, a dated one the day after', () => {
  assert.equal(dueBucket('2026-11-06T11:59', now), 'overdue');
  assert.equal(dueBucket('2026-11-06T12:30', now), 'today');
  assert.equal(dueBucket('2026-11-06', now), 'today');
  assert.equal(dueBucket('2026-11-05', now), 'overdue');
  assert.equal(dueBucket('2026-11-07', now), 'upcoming');
  assert.equal(dueBucket(null, now), null);
  assert.equal(parseArgs(['delete', 'x', '-y']).result.flags.yes, true);
});
