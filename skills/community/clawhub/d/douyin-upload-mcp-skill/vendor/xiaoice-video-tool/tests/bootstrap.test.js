const test = require('node:test');
const assert = require('node:assert/strict');

const { createServiceSkeleton } = require('../src/service');
const { createMcpSkeleton } = require('../src/mcp');
const { createHealthSnapshot } = require('../src/shared');
const { bootstrap } = require('../src');

test('shared module returns a health snapshot', () => {
  const health = createHealthSnapshot();

  assert.equal(health.status, 'ok');
  assert.equal(health.version, 1);
});

test('service module exposes expected metadata', () => {
  const service = createServiceSkeleton();

  assert.equal(service.name, 'video-task-service');
  assert.equal(service.health.status, 'ok');
});

test('mcp module exposes expected metadata', () => {
  const mcp = createMcpSkeleton();

  assert.equal(mcp.name, 'mcp-server');
  assert.deepEqual(mcp.tools, ['xiaoice_video_produce']);
});

test('root bootstrap wires modules together', () => {
  const app = bootstrap();

  assert.equal(app.service.name, 'video-task-service');
  assert.equal(app.mcp.name, 'mcp-server');
  assert.equal(app.health.status, 'ok');
});
