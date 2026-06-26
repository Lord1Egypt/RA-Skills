const { createToolHandler, TOOL_NAME } = require('./tool');

const JSON_RPC_VERSION = '2.0';
const MCP_PROTOCOL_VERSION = '2024-11-05';
const MCP_SERVER_NAME = 'xiaoice-video-mcp-server';
const MCP_SERVER_VERSION = '0.1.0';

function isObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function truncateText(value, maxLength = 200) {
  const text = String(value == null ? '' : value).trim();
  if (!text) {
    return '';
  }
  if (text.length <= maxLength) {
    return text;
  }
  return `${text.slice(0, maxLength)}...`;
}

function parseHeaders(headerBlock) {
  const headers = {};
  const lines = headerBlock.split('\r\n');

  for (const line of lines) {
    const separator = line.indexOf(':');
    if (separator <= 0) {
      continue;
    }
    const key = line.slice(0, separator).trim().toLowerCase();
    const value = line.slice(separator + 1).trim();
    headers[key] = value;
  }

  return headers;
}

function startsWithContentLength(buffer) {
  if (!buffer || buffer.length === 0) {
    return false;
  }
  const preview = buffer.slice(0, 32).toString('utf8');
  return /^\s*content-length:/i.test(preview);
}

function makeToolResultPayload(payload) {
  const normalized = isObject(payload)
    ? payload
    : {
        ok: false,
        action: 'unknown',
        error: {
          code: 'internal_error',
          message: 'Tool returned an invalid payload',
        },
      };

  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(normalized, null, 2),
      },
    ],
    isError: normalized.ok === false,
    structuredContent: normalized,
  };
}

function createUnknownToolPayload(toolName) {
  return {
    ok: false,
    action: 'unknown',
    error: {
      code: 'tool_not_found',
      message: `Unknown tool: ${toolName || '(empty)'}`,
    },
  };
}

function createMcpServer(userConfig = {}) {
  const input = userConfig.input || process.stdin;
  const output = userConfig.output || process.stdout;
  const logger = userConfig.logger || console;
  const toolHandler = userConfig.toolHandler || createToolHandler(userConfig);

  let buffer = Buffer.alloc(0);
  let started = false;
  let closed = false;
  let requestQueue = Promise.resolve();

  function sendMessage(payload) {
    if (closed) {
      return;
    }
    const raw = JSON.stringify(payload);
    const byteLength = Buffer.byteLength(raw, 'utf8');
    output.write(`Content-Length: ${byteLength}\r\n\r\n${raw}`);
  }

  function sendResult(id, result) {
    if (id === undefined) {
      return;
    }
    sendMessage({
      jsonrpc: JSON_RPC_VERSION,
      id,
      result,
    });
  }

  function sendError(id, code, message, data) {
    if (id === undefined) {
      return;
    }
    const payload = {
      jsonrpc: JSON_RPC_VERSION,
      id,
      error: {
        code,
        message,
      },
    };
    if (data !== undefined) {
      payload.error.data = data;
    }
    sendMessage(payload);
  }

  function queueRequest(request) {
    requestQueue = requestQueue
      .then(async () => {
        await handleRequest(request);
      })
      .catch((error) => {
        logger.error?.('[mcp-server] request handling failed', error);

        if (isObject(request) && Object.prototype.hasOwnProperty.call(request, 'id')) {
          sendError(
            request.id,
            -32603,
            'Internal error',
            { reason: truncateText(error?.message || 'Unhandled server error') }
          );
        }
      });
  }

  async function handleRequest(request) {
    if (!isObject(request)) {
      sendError(null, -32600, 'Invalid Request');
      return;
    }

    const hasId = Object.prototype.hasOwnProperty.call(request, 'id');
    const id = hasId ? request.id : undefined;

    if (request.jsonrpc !== JSON_RPC_VERSION) {
      sendError(id, -32600, 'Invalid Request', { reason: 'jsonrpc must be "2.0"' });
      return;
    }

    const method = typeof request.method === 'string' ? request.method.trim() : '';
    if (!method) {
      sendError(id, -32600, 'Invalid Request', { reason: 'method is required' });
      return;
    }

    if (method === 'notifications/initialized') {
      return;
    }

    if (method === 'initialize') {
      sendResult(id, {
        protocolVersion: MCP_PROTOCOL_VERSION,
        capabilities: {
          tools: {},
        },
        serverInfo: {
          name: MCP_SERVER_NAME,
          version: MCP_SERVER_VERSION,
        },
      });
      return;
    }

    if (method === 'tools/list') {
      sendResult(id, {
        tools: [toolHandler.definition],
      });
      return;
    }

    if (method === 'tools/call') {
      if (!isObject(request.params)) {
        sendError(id, -32602, 'Invalid params', { reason: 'params must be an object' });
        return;
      }

      const toolName = typeof request.params.name === 'string'
        ? request.params.name.trim()
        : '';
      if (!toolName) {
        sendError(id, -32602, 'Invalid params', { reason: 'params.name is required' });
        return;
      }

      if (toolName !== TOOL_NAME) {
        sendResult(id, makeToolResultPayload(createUnknownToolPayload(toolName)));
        return;
      }

      const toolArgs = Object.prototype.hasOwnProperty.call(request.params, 'arguments')
        ? request.params.arguments
        : {};
      const toolPayload = await toolHandler.execute(toolArgs);
      sendResult(id, makeToolResultPayload(toolPayload));
      return;
    }

    if (id === undefined) {
      return;
    }

    sendError(id, -32601, `Method not found: ${method}`);
  }

  function handleRawMessage(rawText) {
    let message;
    try {
      message = JSON.parse(rawText);
    } catch (error) {
      sendError(null, -32700, 'Parse error', { raw: truncateText(rawText) });
      return;
    }

    if (Array.isArray(message)) {
      sendError(null, -32600, 'Invalid Request', { reason: 'Batch requests are not supported' });
      return;
    }

    queueRequest(message);
  }

  function consumeContentLengthMessages() {
    while (true) {
      const headerEnd = buffer.indexOf('\r\n\r\n');
      if (headerEnd < 0) {
        return;
      }

      const headerBlock = buffer.slice(0, headerEnd).toString('utf8');
      const headers = parseHeaders(headerBlock);
      const contentLength = Number.parseInt(headers['content-length'], 10);

      if (!Number.isFinite(contentLength) || contentLength < 0) {
        buffer = buffer.slice(headerEnd + 4);
        sendError(null, -32700, 'Parse error', { reason: 'Invalid Content-Length header' });
        continue;
      }

      const bodyStart = headerEnd + 4;
      const bodyEnd = bodyStart + contentLength;
      if (buffer.length < bodyEnd) {
        return;
      }

      const body = buffer.slice(bodyStart, bodyEnd).toString('utf8');
      buffer = buffer.slice(bodyEnd);
      handleRawMessage(body);
    }
  }

  function consumeLineDelimitedMessages() {
    while (true) {
      const lineEnd = buffer.indexOf('\n');
      if (lineEnd < 0) {
        return;
      }

      const line = buffer.slice(0, lineEnd).toString('utf8').trim();
      buffer = buffer.slice(lineEnd + 1);
      if (!line) {
        continue;
      }

      handleRawMessage(line);
    }
  }

  function onData(chunk) {
    if (closed) {
      return;
    }

    const incoming = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    buffer = Buffer.concat([buffer, incoming]);

    if (startsWithContentLength(buffer)) {
      consumeContentLengthMessages();
      return;
    }
    consumeLineDelimitedMessages();
  }

  function onError(error) {
    logger.error?.('[mcp-server] stdio stream error', error);
  }

  function start() {
    if (started) {
      return;
    }
    started = true;

    input.on('data', onData);
    input.on('error', onError);

    if (typeof input.resume === 'function') {
      input.resume();
    }
  }

  function close() {
    if (closed) {
      return;
    }
    closed = true;

    input.off('data', onData);
    input.off('error', onError);

    if (typeof input.pause === 'function') {
      input.pause();
    }
  }

  return {
    start,
    close,
  };
}

module.exports = {
  createMcpServer,
};
