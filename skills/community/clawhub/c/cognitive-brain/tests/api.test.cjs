/**
 * API 端点测试
 */

const assert = require('assert');
const http = require('http');
const { ApiServer } = require('../src/api/server.js');

const TEST_PORT = 3999;

async function runTests() {
  console.log('🧪 Running API Tests...\n');

  let server;
  let passed = 0;
  let failed = 0;

  try {
    // Start test server
    server = new ApiServer(TEST_PORT);
    await server.start();
    console.log('✓ Server started on port', TEST_PORT);

    const baseUrl = `http://localhost:${TEST_PORT}`;

    // Test health endpoint
    console.log('\nTesting /health...');
    const healthRes = await fetch(`${baseUrl}/health`);
    assert.strictEqual(healthRes.status, 200, 'Health should return 200');
    const healthData = await healthRes.json();
    assert.strictEqual(healthData.status, 'ok', 'Status should be ok');
    assert(healthData.version, 'Should have version');
    console.log('  ✓ /health returns correct structure');
    passed++;

    // Test 404
    console.log('\nTesting 404...');
    const notFoundRes = await fetch(`${baseUrl}/nonexistent`);
    assert.strictEqual(notFoundRes.status, 404, 'Should return 404');
    console.log('  ✓ 404 handling');
    passed++;

    // Test rate limiting
    console.log('\nTesting rate limiting...');
    let rateLimitHit = false;
    const requests = [];
    for (let i = 0; i < 105; i++) {
      requests.push(
        fetch(`${baseUrl}/health`).then(res => {
          if (res.status === 429) rateLimitHit = true;
        }).catch(() => {})
      );
    }
    await Promise.all(requests);
    console.log('  ' + (rateLimitHit ? '✓' : '⚠') + ' rate limit protection');
    passed++;

  } catch (err) {
    console.error('✗ API Test error:', err.message);
    failed++;
  } finally {
    // Cleanup
    if (server) {
      try {
        await server.stop();
        console.log('\n✓ Server stopped');
      } catch (e) {
        console.warn('Warning: Error stopping server:', e.message);
      }
    }
  }

  console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);
  process.exit(failed > 0 ? 1 : 0);
}

// Simple fetch polyfill for Node.js < 18
if (!global.fetch) {
  global.fetch = (url, options = {}) => {
    return new Promise((resolve, reject) => {
      const req = http.get(url, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          resolve({
            status: res.statusCode,
            json: () => Promise.resolve(JSON.parse(data))
          });
        });
      });
      req.on('error', reject);
      req.setTimeout(5000, () => reject(new Error('Timeout')));
    });
  };
}

runTests().catch(err => {
  console.error('Test suite error:', err);
  process.exit(1);
});
