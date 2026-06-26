const { describe, test } = require('node:test');
const assert = require('node:assert/strict');
const { PassThrough } = require('node:stream');

const { createMcpServer } = require('../src/mcp/server');

function encodeLineJson(value) {
  return `${JSON.stringify(value)}\n`;
}

function tryReadFramedMessage(buffer) {
  const headerEnd = buffer.indexOf('\r\n\r\n');
  if (headerEnd < 0) {
    return null;
  }

  const headerBlock = buffer.slice(0, headerEnd).toString('utf8');
  const contentLengthLine = headerBlock
    .split('\r\n')
    .find((line) => /^content-length:/i.test(line));

  if (!contentLengthLine) {
    return null;
  }

  const contentLength = Number.parseInt(contentLengthLine.split(':')[1].trim(), 10);
  if (!Number.isFinite(contentLength) || contentLength < 0) {
    return null;
  }

  const bodyStart = headerEnd + 4;
  const bodyEnd = bodyStart + contentLength;
  if (buffer.length < bodyEnd) {
    return null;
  }

  const body = buffer.slice(bodyStart, bodyEnd).toString('utf8');
  const rest = buffer.slice(bodyEnd);
  return {
    message: JSON.parse(body),
    rest,
  };
}

function createOutputCollector(output) {
  let buffer = Buffer.alloc(0);
  const queue = [];
  const waiters = [];

  function flush() {
    while (true) {
      const parsed = tryReadFramedMessage(buffer);
      if (!parsed) {
        break;
      }
      buffer = parsed.rest;
      queue.push(parsed.message);
    }

    while (queue.length > 0 && waiters.length > 0) {
      const waiter = waiters.shift();
      waiter(queue.shift());
    }
  }

  output.on('data', (chunk) => {
    const incoming = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    buffer = Buffer.concat([buffer, incoming]);
    flush();
  });

  return {
    nextMessage(timeoutMs = 1500) {
      if (queue.length > 0) {
        return Promise.resolve(queue.shift());
      }

      return new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          reject(new Error(`Timed out waiting for MCP response after ${timeoutMs}ms`));
        }, timeoutMs);

        waiters.push((value) => {
          clearTimeout(timeout);
          resolve(value);
        });
      });
    },
  };
}

describe('mcp server protocol', { concurrency: 1 }, () => {
  test('supports initialize, tools/list and tools/call over stdio', async () => {
    const input = new PassThrough();
    const output = new PassThrough();
    const collector = createOutputCollector(output);
    const executeCalls = [];

    const server = createMcpServer({
      input,
      output,
      logger: { error: () => {} },
      toolHandler: {
        definition: {
          name: 'xiaoice_video_produce',
          description: 'test tool',
          inputSchema: { type: 'object', properties: {}, required: [] },
        },
        async execute(args) {
          executeCalls.push(args);
          return {
            ok: true,
            action: String(args?.action || 'unknown'),
            task: { taskId: 'task-001', status: 'submitted' },
          };
        },
      },
    });

    server.start();

    input.write(
      encodeLineJson({
        jsonrpc: '2.0',
        id: 1,
        method: 'initialize',
        params: {},
      })
    );
    const initializeResp = await collector.nextMessage();
    assert.equal(initializeResp.jsonrpc, '2.0');
    assert.equal(initializeResp.id, 1);
    assert.equal(initializeResp.result.serverInfo.name, 'xiaoice-video-mcp-server');
    assert.ok(initializeResp.result.capabilities.tools);

    input.write(
      encodeLineJson({
        jsonrpc: '2.0',
        id: 2,
        method: 'tools/list',
        params: {},
      })
    );
    const listResp = await collector.nextMessage();
    assert.equal(listResp.id, 2);
    assert.equal(Array.isArray(listResp.result.tools), true);
    assert.equal(listResp.result.tools[0].name, 'xiaoice_video_produce');

    input.write(
      encodeLineJson({
        jsonrpc: '2.0',
        id: 3,
        method: 'tools/call',
        params: {
          name: 'xiaoice_video_produce',
          arguments: {
            action: 'create',
            topic: 'create from protocol test',
            vhBizId: 'biz-protocol-001',
          },
        },
      })
    );
    const callResp = await collector.nextMessage();
    assert.equal(callResp.id, 3);
    assert.equal(callResp.result.isError, false);
    assert.equal(executeCalls.length, 1);
    assert.equal(executeCalls[0].action, 'create');

    server.close();
    input.end();
    output.end();
  });
});
