const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const REPO_ROOT = path.resolve(__dirname, '..', '..');

function loadScriptModule(relativePath) {
  const modulePath = path.join(REPO_ROOT, relativePath);
  let resolvedPath = '';
  try {
    resolvedPath = require.resolve(modulePath);
  } catch (error) {
    throw new Error(
      `Missing ${relativePath}. Expected ngrok bootstrap module at ${modulePath}.`
    );
  }

  delete require.cache[resolvedPath];
  return require(resolvedPath);
}

function pickFunction(moduleValue, candidateNames, description) {
  if (!moduleValue || (typeof moduleValue !== 'object' && typeof moduleValue !== 'function')) {
    throw new Error(`Cannot resolve ${description}: module exports are empty.`);
  }

  for (const name of candidateNames) {
    if (typeof moduleValue?.[name] === 'function') {
      return moduleValue[name];
    }
  }

  if (typeof moduleValue === 'function') {
    return moduleValue;
  }

  const exportNames = Object.keys(moduleValue);
  throw new Error(
    `Cannot resolve ${description}. Tried [${candidateNames.join(', ')}], exports=[${exportNames.join(', ')}].`
  );
}

function invokeFirst(attempts, description) {
  const errors = [];
  for (const attempt of attempts) {
    try {
      const value = attempt();
      if (value !== undefined) {
        return value;
      }
    } catch (error) {
      errors.push(error?.message || String(error));
    }
  }

  throw new Error(
    `Unable to invoke ${description} with supported signatures. Errors: ${errors.join(' | ')}`
  );
}

async function invokeFirstAsync(attempts, description) {
  const errors = [];
  for (const attempt of attempts) {
    try {
      const value = await attempt();
      if (value !== undefined) {
        return value;
      }
    } catch (error) {
      errors.push(error?.message || String(error));
    }
  }

  throw new Error(
    `Unable to invoke ${description} with supported signatures. Errors: ${errors.join(' | ')}`
  );
}

function createFetchStub() {
  const queue = [];
  const calls = [];

  async function fetchStub(input, init = {}) {
    calls.push({ input, init });

    if (queue.length === 0) {
      throw new Error('Unexpected fetch call: no mock response queued');
    }

    const next = queue.shift();
    if (next instanceof Error) {
      throw next;
    }

    const status = next.status ?? 200;
    return {
      ok: next.ok ?? (status >= 200 && status < 300),
      status,
      statusText: next.statusText || '',
      async json() {
        return next.body ?? {};
      },
      async text() {
        if (typeof next.text === 'string') {
          return next.text;
        }
        return JSON.stringify(next.body ?? {});
      },
    };
  }

  fetchStub.calls = calls;
  fetchStub.queueResponse = (response) => {
    queue.push(response);
  };

  return fetchStub;
}

function parseFetchJsonBody(call) {
  if (typeof call?.init?.body !== 'string') {
    return null;
  }

  return JSON.parse(call.init.body);
}

function getRequestUrl(call) {
  const input = call?.input;
  if (typeof input === 'string') {
    return input;
  }
  if (input && typeof input.url === 'string') {
    return input.url;
  }
  return String(input || '');
}

function getRequestMethod(call) {
  if (call?.init?.method) {
    return String(call.init.method).toUpperCase();
  }
  if (call?.input?.method) {
    return String(call.input.method).toUpperCase();
  }
  return 'GET';
}

function getHeaderValue(headers, name) {
  if (!headers) {
    return '';
  }

  if (typeof headers.get === 'function') {
    const value = headers.get(name);
    return value == null ? '' : String(value);
  }

  for (const [key, value] of Object.entries(headers)) {
    if (String(key).toLowerCase() === String(name).toLowerCase()) {
      return value == null ? '' : String(value);
    }
  }

  return '';
}

function loadJsonFixture(fileName) {
  const fixturePath = path.join(REPO_ROOT, 'tests', 'fixtures', fileName);
  return JSON.parse(fs.readFileSync(fixturePath, 'utf8'));
}

function runNodeScript(relativePath, { env = {}, args = [], timeoutMs = 6000, cwd = REPO_ROOT } = {}) {
  const scriptPath = path.join(REPO_ROOT, relativePath);
  const result = spawnSync(process.execPath, [scriptPath, ...args], {
    cwd,
    env: { ...process.env, ...env },
    encoding: 'utf8',
    timeout: timeoutMs,
  });

  return {
    ...result,
    scriptPath,
    output: `${result.stdout || ''}\n${result.stderr || ''}`.trim(),
  };
}

function collectStringLeaves(value, out = []) {
  if (typeof value === 'string') {
    out.push(path.normalize(value));
    return out;
  }

  if (Array.isArray(value)) {
    for (const item of value) {
      collectStringLeaves(item, out);
    }
    return out;
  }

  if (value && typeof value === 'object') {
    for (const item of Object.values(value)) {
      collectStringLeaves(item, out);
    }
  }

  return out;
}

function extractPublicUrl(value) {
  if (typeof value === 'string') {
    return value;
  }

  if (!value || typeof value !== 'object') {
    return '';
  }

  const directKeys = ['publicUrl', 'callbackPublicBaseUrl', 'url', 'public_url'];
  for (const key of directKeys) {
    if (typeof value[key] === 'string') {
      return value[key];
    }
  }

  if (value.tunnel) {
    return extractPublicUrl(value.tunnel);
  }

  return '';
}

function createJsonServer(routeHandlers) {
  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      const url = new URL(req.url || '/', 'http://127.0.0.1');
      const key = `${req.method} ${url.pathname}`;
      const handler = routeHandlers[key];

      if (!handler) {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: { code: 'not_found', message: key } }));
        return;
      }

      let rawBody = '';
      req.on('data', (chunk) => {
        rawBody += chunk.toString();
      });

      req.on('end', async () => {
        let jsonBody = null;
        if (rawBody) {
          try {
            jsonBody = JSON.parse(rawBody);
          } catch (error) {
            jsonBody = null;
          }
        }

        const response = await handler({
          req,
          url,
          rawBody,
          jsonBody,
        });

        const status = response?.status ?? 200;
        const body = response?.body ?? {};
        const headers = {
          'Content-Type': 'application/json',
          ...(response?.headers || {}),
        };

        res.writeHead(status, headers);
        res.end(JSON.stringify(body));
      });
    });

    server.on('error', reject);

    server.listen(0, '127.0.0.1', () => {
      const address = server.address();
      resolve({
        server,
        host: '127.0.0.1',
        port: address.port,
        url: `http://127.0.0.1:${address.port}`,
        close: () =>
          new Promise((resolveClose, rejectClose) => {
            server.close((error) => {
              if (error) {
                rejectClose(error);
                return;
              }
              resolveClose();
            });
          }),
      });
    });
  });
}

module.exports = {
  REPO_ROOT,
  loadScriptModule,
  pickFunction,
  invokeFirst,
  invokeFirstAsync,
  createFetchStub,
  parseFetchJsonBody,
  getRequestUrl,
  getRequestMethod,
  getHeaderValue,
  loadJsonFixture,
  runNodeScript,
  collectStringLeaves,
  extractPublicUrl,
  createJsonServer,
};
