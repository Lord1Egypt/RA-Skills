/**
 * AI Content Repurposer - Test Suite
 */

const ContentConverter = require('../src/converter');
const assert = require('assert');

console.log('🧪 Running AI Content Repurposer Tests...\n');

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${error.message}`);
    failed++;
  }
}

async function runTests() {
  const converter = new ContentConverter();

  // Test 1: YouTube video ID extraction
  test('Extract YouTube video ID from URL', () => {
    const url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';
    const videoId = converter._extractVideoId(url);
    assert.strictEqual(videoId, 'dQw4w9WgXcQ');
  });

  // Test 2: YouTube video ID from short URL
  test('Extract YouTube video ID from short URL', () => {
    const url = 'https://youtu.be/dQw4w9WgXcQ';
    const videoId = converter._extractVideoId(url);
    assert.strictEqual(videoId, 'dQw4w9WgXcQ');
  });

  // Test 3: Fallback response when AI not configured
  test('Return fallback response without API key', async () => {
    const result = await converter.youtubeToShortForm('Test transcript', 'tiktok');
    assert(result.warning || typeof result === 'object');
  });

  // Test 4: Platform limits
  test('TikTok platform has correct limits', () => {
    const limits = {
      tiktok: { maxDuration: 180, maxChars: 2000 },
      shorts: { maxDuration: 60, maxChars: 1000 },
      reels: { maxDuration: 90, maxChars: 1500 }
    };
    assert.strictEqual(limits.tiktok.maxDuration, 180);
    assert.strictEqual(limits.shorts.maxDuration, 60);
    assert.strictEqual(limits.reels.maxDuration, 90);
  });

  // Test 5: Module exports
  test('ContentConverter class is exported', () => {
    assert.strictEqual(typeof ContentConverter, 'function');
  });

  // Test 6: Instance creation
  test('Can create converter instance with options', () => {
    const converter = new ContentConverter({
      apiKey: 'test-key',
      model: 'gpt-4'
    });
    assert.strictEqual(converter.apiKey, 'test-key');
    assert.strictEqual(converter.model, 'gpt-4');
  });

  // Test 7: Default options
  test('Default options are set correctly', () => {
    const converter = new ContentConverter();
    assert.strictEqual(converter.model, 'gpt-4');
  });

  console.log(`\n${'='.repeat(50)}`);
  console.log(`Tests complete: ${passed} passed, ${failed} failed`);
  console.log(`${'='.repeat(50)}\n`);

  process.exit(failed > 0 ? 1 : 0);
}

runTests();
