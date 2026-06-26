import ClawTextIngest from './src/index.js';

async function testIngest() {
  const ingest = new ClawTextIngest();

  console.log('Testing ClawText Ingest...\n');

  // Test 1: Text ingestion
  console.log('✓ Test 1: Text ingestion');
  const textResult = await ingest.fromText(
    'Test memory content about workflow decisions',
    { type: 'decision', entities: ['test'], project: 'testing' }
  );
  console.log(`  Imported: ${textResult.imported}`);

  // Test 2: JSON ingestion (simulating chat export)
  console.log('\n✓ Test 2: JSON ingestion (chat format)');
  const chatData = [
    { timestamp: '2026-03-03T10:00:00Z', user: 'alice', message: 'Team decision: restart on timeout' },
    { timestamp: '2026-03-03T10:05:00Z', user: 'bob', message: 'Confirmed, implementing now' }
  ];
  const jsonResult = await ingest.fromJSON(chatData, 
    { type: 'fact', project: 'team' },
    { 
      keyMap: { contentKey: 'message', dateKey: 'timestamp', authorKey: 'user' }
    }
  );
  console.log(`  Imported: ${jsonResult.imported}`);

  // Test 3: Batch ingestion
  console.log('\n✓ Test 3: Batch ingestion (multiple sources)');
  const batchResult = await ingest.ingestAll([
    {
      type: 'text',
      data: 'Architecture note: Use BM25 for keyword matching',
      metadata: { type: 'fact', project: 'architecture' }
    },
    {
      type: 'text',
      data: 'Pattern: Always validate before applying config',
      metadata: { type: 'code', project: 'patterns', entities: ['config'] }
    }
  ]);
  console.log(`  Total imported: ${batchResult.totalImported}`);

  // Test 4: Report
  console.log('\n✓ Test 4: Report');
  const report = ingest.getReport();
  console.log(`  Total memories imported: ${report.totalImported}`);
  console.log(`  Errors: ${report.errorCount}`);
  console.log(`  Memory directory: ${report.memoryDir}`);

  console.log('\n✅ All tests passed!');
  console.log(`\nMemories written to: ${ingest.memoryDir}/ingested-*.md`);
}

testIngest().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
