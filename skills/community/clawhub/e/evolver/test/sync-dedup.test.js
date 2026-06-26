// End-to-end test for `node index.js sync` dedup logic.
//
// We spin up an in-process HTTP mock for /a2a/assets/published-by-me (and
// purchased) so we can verify what the CLI does given a controlled set of
// Hub responses. The two failure modes we want to lock down:
//
// 1. A bundled default-seed gene (id e.g. `gene_gep_repair_from_errors`,
//    no hub_asset_id) must NOT cause Hub copies of the same id to silently
//    skip on first sync. We allow the default to win unless the user
//    passes --force, but the run must clearly report "id_collision" so
//    the user understands why nothing changed.
// 2. With --force, the local entry is overwritten with the Hub copy and a
//    hub_asset_id is recorded; subsequent runs without --force become
//    no-ops via the hub_asset_id dedup check.

const { describe, it, before, after } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const http = require('http');

const { spawn } = require('child_process');

function startMock(handlers) {
  const server = http.createServer((req, res) => {
    const url = new URL(req.url, 'http://x');
    const route = handlers[url.pathname];
    if (!route) {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'not_found' }));
      return;
    }
    let body = '';
    req.on('data', (c) => { body += c; });
    req.on('end', () => {
      try {
        const result = route({ url, body, headers: req.headers });
        res.writeHead(result.status || 200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result.body || {}));
      } catch (e) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
  });
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => {
      const addr = server.address();
      resolve({ server, url: 'http://127.0.0.1:' + addr.port });
    });
  });
}

// Async version of spawn so the in-process mock HTTP server keeps servicing
// requests while the child runs. spawnSync would block this event loop and
// deadlock against our own mock.
function runSync(env, extraArgs) {
  const cwd = path.resolve(__dirname, '..');
  const argv = ['index.js', 'sync', '--scope=published'].concat(extraArgs || []);
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, argv, {
      cwd,
      env: { ...process.env, EVOMAP_HUB_ALLOW_INSECURE: '1', ...env },
    });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (d) => { stdout += d.toString('utf8'); });
    child.stderr.on('data', (d) => { stderr += d.toString('utf8'); });
    const t = setTimeout(() => {
      child.kill('SIGTERM');
      reject(new Error('runSync timed out\nstdout=' + stdout + '\nstderr=' + stderr));
    }, 15000);
    child.on('exit', (status, signal) => {
      clearTimeout(t);
      resolve({ stdout, stderr, status, signal });
    });
    child.on('error', (e) => { clearTimeout(t); reject(e); });
  });
}

function mkSandbox() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-sync-'));
  const assetsDir = path.join(root, 'assets', 'gep');
  fs.mkdirSync(assetsDir, { recursive: true });
  return { root, assetsDir };
}

describe('sync dedup (id collision vs hub_asset_id)', () => {
  let mock;
  before(async () => {
    const hubAsset = {
      asset_id: 'hub-asset-aaaa1111',
      asset_type: 'Gene',
      local_id: 'gene_gep_repair_from_errors',
      payload: {
        id: 'gene_gep_repair_from_errors',
        category: 'repair',
        signals: ['error'],
        strategy: ['hub-strategy-step'],
        avoid: [],
        validation: {},
        summary: 'hub copy',
      },
    };
    mock = await startMock({
      '/a2a/assets/published-by-me': () => ({
        body: { assets: [hubAsset], count: 1, has_more: false, next_cursor: null, node_ids: ['node-test'] },
      }),
      '/a2a/assets/purchased': () => ({
        body: { assets: [], count: 0, has_more: false, next_cursor: null, node_ids: ['node-test'] },
      }),
      // Detail endpoint not needed because we ship payload inline.
    });
  });
  after(() => {
    if (mock) mock.server.close();
  });

  it('skips a hub asset whose local_id matches a default-seed gene (no --force)', async () => {
    const { assetsDir } = mkSandbox();
    fs.writeFileSync(
      path.join(assetsDir, 'genes.json'),
      JSON.stringify({ version: 1, genes: [{ id: 'gene_gep_repair_from_errors', strategy: ['local-default'] }] }, null, 2)
    );

    const r = await runSync({
      A2A_HUB_URL: mock.url,
      A2A_NODE_ID: 'node_aaaaaaaaaaaa',
      A2A_NODE_SECRET: 'a'.repeat(64),
      GEP_ASSETS_DIR: assetsDir,
    });

    assert.equal(r.status, 0, 'sync should exit 0; stdout=' + r.stdout + ' stderr=' + r.stderr);
    assert.match(r.stdout, /id_collision=1/);
    assert.match(r.stdout, /--force/);
    const genes = JSON.parse(fs.readFileSync(path.join(assetsDir, 'genes.json'), 'utf8')).genes;
    assert.equal(genes.length, 1);
    assert.equal(genes[0].strategy[0], 'local-default', 'local default must be preserved');
    assert.equal(genes[0].hub_asset_id, undefined, 'no hub_asset_id should be written without --force');
  });

  it('overwrites the default-seed gene with the Hub copy when --force is set', async () => {
    const { assetsDir } = mkSandbox();
    fs.writeFileSync(
      path.join(assetsDir, 'genes.json'),
      JSON.stringify({ version: 1, genes: [{ id: 'gene_gep_repair_from_errors', strategy: ['local-default'] }] }, null, 2)
    );

    const r = await runSync({
      A2A_HUB_URL: mock.url,
      A2A_NODE_ID: 'node_aaaaaaaaaaaa',
      A2A_NODE_SECRET: 'a'.repeat(64),
      GEP_ASSETS_DIR: assetsDir,
    }, ['--force']);

    assert.equal(r.status, 0, 'sync should exit 0; stdout=' + r.stdout + ' stderr=' + r.stderr);
    assert.match(r.stdout, /synced=1/);
    const genes = JSON.parse(fs.readFileSync(path.join(assetsDir, 'genes.json'), 'utf8')).genes;
    assert.equal(genes.length, 1);
    assert.equal(genes[0].strategy[0], 'hub-strategy-step', 'Hub strategy must overwrite local default');
    assert.equal(genes[0].hub_asset_id, 'hub-asset-aaaa1111');
  });

  it('is idempotent on a second run: hub_asset_id match -> already_synced (not re-fetched)', async () => {
    const { assetsDir } = mkSandbox();
    fs.writeFileSync(
      path.join(assetsDir, 'genes.json'),
      JSON.stringify({
        version: 1,
        genes: [{
          id: 'gene_gep_repair_from_errors',
          strategy: ['hub-strategy-step'],
          hub_asset_id: 'hub-asset-aaaa1111',
          synced_at: '2026-05-04T00:00:00.000Z',
        }],
      }, null, 2)
    );

    const r = await runSync({
      A2A_HUB_URL: mock.url,
      A2A_NODE_ID: 'node_aaaaaaaaaaaa',
      A2A_NODE_SECRET: 'a'.repeat(64),
      GEP_ASSETS_DIR: assetsDir,
    });

    assert.equal(r.status, 0);
    assert.match(r.stdout, /already_synced=1/);
    assert.match(r.stdout, /id_collision=0/);
    assert.doesNotMatch(r.stdout, /--force/, 'no --force suggestion when there is no real id collision');
  });
});
