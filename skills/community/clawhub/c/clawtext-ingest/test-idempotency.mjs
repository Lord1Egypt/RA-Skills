import ClawTextIngest from './src/index.js';
import fs from 'fs';
import path from 'path';
import os from 'os';

const testDir = path.join(os.tmpdir(), 'clawtext-ingest-test');

async function testIdempotency() {
  // Setup
  if (fs.existsSync(testDir)) {
    fs.rmSync(testDir, { recursive: true });
  }
  fs.mkdirSync(testDir, { recursive: true });

  console.log('🧪 Testing Idempotency & Deduplication\n');

  // Test 1: Same content ingested twice should skip second
  console.log('Test 1: Duplicate detection');
  const ingest1 = new ClawTextIngest(testDir);
  const r1 = await ingest1.ingestAll([
    { type: 'text', data: 'Test content A', metadata: { project: 'test' } },
    { type: 'text', data: 'Test content B', metadata: { project: 'test' } }
  ]);
  console.log(`  First run: imported=${r1.totalImported}, skipped=${r1.totalSkipped}`);
  if (r1.totalImported !== 2) throw new Error('Expected 2 imports on first run');

  // Second ingest with same content
  const ingest2 = new ClawTextIngest(testDir);
  const r2 = await ingest2.ingestAll([
    { type: 'text', data: 'Test content A', metadata: { project: 'test' } },
    { type: 'text', data: 'Test content B', metadata: { project: 'test' } }
  ]);
  console.log(`  Second run: imported=${r2.totalImported}, skipped=${r2.totalSkipped}`);
  if (r2.totalSkipped !== 2) throw new Error(`Expected 2 skipped on second run, got ${r2.totalSkipped}`);
  console.log('  ✅ Duplicates detected & skipped\n');

  // Test 2: New content mixed with duplicates
  console.log('Test 2: Mixed new & duplicate');
  const ingest3 = new ClawTextIngest(testDir);
  const r3 = await ingest3.ingestAll([
    { type: 'text', data: 'Test content A', metadata: { project: 'test' } }, // dup
    { type: 'text', data: 'Test content C', metadata: { project: 'test' } }  // new
  ]);
  console.log(`  Mixed run: imported=${r3.totalImported}, skipped=${r3.totalSkipped}`);
  if (r3.totalImported !== 1 || r3.totalSkipped !== 1) {
    throw new Error(`Expected 1 import + 1 skip, got ${r3.totalImported} + ${r3.totalSkipped}`);
  }
  console.log('  ✅ Mixed batch processed correctly\n');

  // Test 3: Hash file persistence
  console.log('Test 3: Hash persistence');
  const ingest4 = new ClawTextIngest(testDir);
  const hashes = ingest4.hashes;
  console.log(`  Loaded ${Object.keys(hashes).length} hashes from disk`);
  if (Object.keys(hashes).length !== 3) throw new Error('Expected 3 hashes persisted');
  console.log('  ✅ Hashes persisted across instances\n');

  console.log('✅ All idempotency tests passed!\n');

  // Cleanup
  fs.rmSync(testDir, { recursive: true });
}

testIdempotency().catch(err => {
  console.error('❌ Test failed:', err.message);
  process.exit(1);
});
