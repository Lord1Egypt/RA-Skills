import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { OUTBOUND_INTENT_RETENTION_MS, updateOutboundMetadata } from '../dist/outbound-metadata.js';

test('outbound plans expire from disk while routing history survives', (t) => {
  const folder = mkdtempSync(join(tmpdir(), 'amber-outbound-metadata-'));
  t.after(() => rmSync(folder, { recursive: true, force: true }));
  const file = join(folder, 'calls.json');
  const createdAtMs = Date.now();
  const metadata = {
    bridgeId: 'pending',
    to: '+12025550142',
    objective: 'Book a table',
    callPlan: { customer: { name: 'Synthetic Customer' } },
    model: 'gpt-realtime-2.1',
    createdAtMs,
  };
  writeFileSync(file, JSON.stringify({ schema: 1, calls: { sid: metadata } }), { mode: 0o644 });
  const atExpiry = createdAtMs + OUTBOUND_INTENT_RETENTION_MS;
  const restored = updateOutboundMetadata(file, atExpiry - 1);
  assert.deepEqual(restored.sid, metadata);
  assert.equal(statSync(file).mode & 0o777, 0o600);

  updateOutboundMetadata(file, atExpiry);
  const { callPlan, ...history } = metadata;
  const contents = readFileSync(file, 'utf8');
  assert.deepEqual(JSON.parse(contents).calls, { sid: history });
  assert(!contents.includes(callPlan.customer.name));

  const stored = updateOutboundMetadata(file, atExpiry, {
    sid: 'next',
    metadata: { ...metadata, bridgeId: 'next', createdAtMs: atExpiry },
  });
  assert.deepEqual(stored.sid, history);
  assert.deepEqual(stored.next.callPlan, callPlan);
  assert.equal(statSync(file).mode & 0o777, 0o600);
});
