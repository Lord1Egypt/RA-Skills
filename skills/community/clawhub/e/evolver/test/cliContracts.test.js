const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const {
  parseReuseArgs,
  parsePublishArgs,
  buildPublishBundle,
  runReuseCommand,
  runPublishCommand,
} = require('../src/gep/cliContracts');
const { computeAssetId } = require('../src/gep/contentHash');

function capture() {
  let text = '';
  return {
    out: { write: s => { text += s; } },
    text: () => text,
    json: () => JSON.parse(text),
  };
}

async function captureProcessOutput(fn) {
  let stdout = '';
  let stderr = '';
  const originalStdoutWrite = process.stdout.write;
  const originalStderrWrite = process.stderr.write;
  process.stdout.write = function (chunk, ...args) {
    stdout += String(chunk);
    if (typeof args[args.length - 1] === 'function') args[args.length - 1]();
    return true;
  };
  process.stderr.write = function (chunk, ...args) {
    stderr += String(chunk);
    if (typeof args[args.length - 1] === 'function') args[args.length - 1]();
    return true;
  };
  try {
    const result = await fn();
    return { result, stdout, stderr };
  } finally {
    process.stdout.write = originalStdoutWrite;
    process.stderr.write = originalStderrWrite;
  }
}

function singleJsonLine(stdout) {
  const lines = stdout.trimEnd().split('\n');
  assert.equal(lines.length, 1);
  return JSON.parse(lines[0]);
}

function gene(extra) {
  return Object.assign({
    type: 'Gene',
    schema_version: '1',
    asset_id: 'sha256:gene-original',
    id: 'gene-1',
    category: 'repair',
    signals_match: ['log_error'],
    strategy: ['inspect logs'],
    constraints: { max_files: 2, forbidden_paths: [] },
    validation: ['node --test'],
  }, extra || {});
}

function capsule(extra) {
  return Object.assign({
    type: 'Capsule',
    schema_version: '1',
    asset_id: 'sha256:cap-original',
    id: 'cap-1',
    trigger: ['log_error'],
    gene: 'sha256:gene-original',
    summary: 'fixed retry path',
    confidence: 0.9,
    blast_radius: { files: 1, lines: 3 },
    outcome: { status: 'success', score: 0.8 },
  }, extra || {});
}

function event(extra) {
  return Object.assign({
    type: 'EvolutionEvent',
    schema_version: '1',
    asset_id: 'sha256:event-original',
    id: 'event-1',
    gene: 'sha256:gene-original',
    capsule: 'sha256:cap-original',
    signals: ['log_error'],
    outcome: { status: 'success' },
  }, extra || {});
}

function withComputedAssetId(asset) {
  const copy = Object.assign({}, asset);
  copy.asset_id = computeAssetId(copy);
  return copy;
}

function fakeStore(records) {
  const writes = [];
  return {
    writes,
    loadGenes: () => records.filter(r => r.type === 'Gene'),
    loadCapsules: () => records.filter(r => r.type === 'Capsule'),
    readAllEvents: () => records.filter(r => r.type === 'EvolutionEvent'),
    upsertGene: asset => {
      writes.push(asset);
      if (!asset.asset_id) asset.asset_id = 'sha256:stored-gene';
    },
    upsertCapsule: asset => {
      writes.push(asset);
      if (!asset.asset_id) asset.asset_id = 'sha256:stored-cap';
    },
    appendEventJsonl: asset => {
      writes.push(asset);
    },
  };
}

function fakeA2a() {
  return {
    buildPublishBundle: ({ gene, capsule, event }) => ({
      protocol: 'gep-a2a',
      protocol_version: '1.0.0',
      message_type: 'publish',
      payload: { assets: [gene, capsule].concat(event ? [event] : []) },
    }),
    buildFetch: ({ assetIds }) => ({
      protocol: 'gep-a2a',
      protocol_version: '1.0.0',
      message_type: 'fetch',
      payload: { asset_ids: assetIds },
    }),
    buildHubHeaders: () => ({ authorization: 'Bearer test' }),
  };
}

function authorizationHeader(headers) {
  return headers && (headers.Authorization || headers.authorization);
}

function mutatingA2a() {
  return {
    buildPublishBundle: ({ gene, capsule, event }) => {
      if (!Array.isArray(capsule.execution_trace)) {
        capsule.execution_trace = [{ step: 1, stage: 'build', cmd: 'node --test', exit: 0 }];
      }
      gene.asset_id = computeAssetId(gene);
      capsule.asset_id = computeAssetId(capsule);
      return {
        protocol: 'gep-a2a',
        protocol_version: '1.0.0',
        message_type: 'publish',
        payload: { assets: [gene, capsule].concat(event ? [event] : []) },
      };
    },
    buildFetch: fakeA2a().buildFetch,
    buildHubHeaders: fakeA2a().buildHubHeaders,
  };
}

function signingMutatingA2a(secret, leaked) {
  return {
    buildPublishBundle: ({ gene, capsule, event }) => {
      if (!Array.isArray(capsule.execution_trace)) {
        capsule.execution_trace = [{ step: 1, stage: 'build', cmd: 'node --test ' + leaked, exit: 0 }];
      }
      gene.asset_id = computeAssetId(gene);
      capsule.asset_id = computeAssetId(capsule);
      if (event) event.asset_id = computeAssetId(event);
      const ids = [gene.asset_id, capsule.asset_id].sort();
      const signature = crypto.createHmac('sha256', secret).update(ids.join('|')).digest('hex');
      return {
        protocol: 'gep-a2a',
        protocol_version: '1.0.0',
        message_type: 'publish',
        payload: {
          assets: [gene, capsule].concat(event ? [event] : []),
          signature,
        },
      };
    },
    buildFetch: fakeA2a().buildFetch,
    buildHubHeaders: fakeA2a().buildHubHeaders,
  };
}

function expectedSignature(assets, secret) {
  const ids = assets
    .filter(asset => asset.type === 'Gene' || asset.type === 'Capsule')
    .map(asset => asset.asset_id)
    .sort();
  return crypto.createHmac('sha256', secret).update(ids.join('|')).digest('hex');
}

test('reuse.v1 parser accepts --id and rejects missing id', () => {
  assert.deepEqual(parseReuseArgs(['--id', 'sha256:x', '--json']), { ok: true, assetId: 'sha256:x', jsonOut: true });
  assert.equal(parseReuseArgs(['--json']).ok, false);
  assert.equal(parseReuseArgs(['--id', 'sha256:x', '--unknown', '--json']).reason, 'unsupported');
  assert.equal(parseReuseArgs(['sha256:x', '--json']).reason, 'unsupported');
  assert.equal(parseReuseArgs(['--id', 'sha256:x']).reason, 'unsupported');
});

test('publish.v1 parser accepts repeated assets and dry-run', () => {
  assert.deepEqual(parsePublishArgs(['--asset', 'g', '--capsule=c', '--dry-run', '--json']), {
    ok: true,
    assetRefs: ['g', 'c'],
    dryRun: true,
    jsonOut: true,
  });
  assert.equal(parsePublishArgs(['--unknown']).reason, 'unsupported');
  assert.equal(parsePublishArgs(['--asset', 'g']).reason, 'unsupported');
  assert.equal(parsePublishArgs(['g', '--json']).reason, 'unsupported');
});

test('reuse.v1 stores fetched Hub assets without transport metadata', async () => {
  const store = fakeStore([]);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-'));
  const io = capture();
  const fetched = Object.assign(withComputedAssetId(gene()), { credit_cost: { total: 3 } });
  const code = await runReuseCommand(['--id', fetched.asset_id, '--json'], {
    out: io.out,
    assetsDir: dir,
    assetStore: store,
    fetchAssetById: async () => fetched,
  });

  assert.equal(code, 0);
  assert.equal(io.json().contract, 'reuse.v1');
  assert.equal(io.json().status, 'ok');
  assert.equal(store.writes.length, 1);
  assert.equal(store.writes[0].credit_cost, undefined);
  assert.ok(fs.readFileSync(path.join(dir, 'provenance.jsonl'), 'utf8').includes('"source":"hub"'));
});

test('reuse.v1 fails closed when provenance append fails', async () => {
  const store = fakeStore([]);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-provenance-fail-'));
  fs.mkdirSync(path.join(dir, 'provenance.jsonl'));
  const io = capture();
  const fetched = withComputedAssetId(gene());
  const code = await runReuseCommand(['--id', fetched.asset_id, '--json'], {
    out: io.out,
    assetsDir: dir,
    assetStore: store,
    fetchAssetById: async () => fetched,
  });
  const json = io.json();
  const stdout = io.text();

  assert.equal(code, 1);
  assert.equal(json.ok, false);
  assert.equal(json.reason, 'internal_error');
  assert.notEqual(json.status, 'ok');
  assert.equal(store.writes.length, 0);
  assert.equal(stdout.includes(dir), false);
  assert.equal(stdout.includes('provenance.jsonl'), false);
  assert.equal(stdout.includes('EISDIR'), false);
  assert.equal(stdout.includes('.env'), false);
  assert.equal(stdout.includes('token='), false);
});

test('reuse.v1 does not leave provenance when local store fails', async () => {
  const store = fakeStore([]);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-store-fail-'));
  const provenancePath = path.join(dir, 'provenance.jsonl');
  const existingProvenance = JSON.stringify({ assetId: 'sha256:existing', source: 'hub' }) + '\n';
  fs.writeFileSync(provenancePath, existingProvenance, 'utf8');
  const io = capture();
  const fetched = withComputedAssetId(gene());
  let attemptedStore = false;
  store.upsertGene = () => {
    attemptedStore = true;
    throw new Error('store failed token=abcdefghijklmnop path=/tmp/.env');
  };
  const code = await runReuseCommand(['--id', fetched.asset_id, '--json'], {
    out: io.out,
    assetsDir: dir,
    assetStore: store,
    fetchAssetById: async () => fetched,
  });
  const stdout = io.text();

  assert.equal(code, 1);
  assert.equal(attemptedStore, true);
  assert.equal(io.json().reason, 'internal_error');
  assert.equal(fs.readFileSync(provenancePath, 'utf8'), existingProvenance);
  assert.equal(stdout.includes('store failed'), false);
  assert.equal(stdout.includes('token=abcdefghijklmnop'), false);
  assert.equal(stdout.includes('/tmp/.env'), false);
});

test('reuse.v1 removes newly staged provenance when local store fails', async () => {
  const store = fakeStore([]);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-store-fail-new-'));
  const io = capture();
  const fetched = withComputedAssetId(gene());
  store.upsertGene = () => {
    throw new Error('store failed');
  };
  const code = await runReuseCommand(['--id', fetched.asset_id, '--json'], {
    out: io.out,
    assetsDir: dir,
    assetStore: store,
    fetchAssetById: async () => fetched,
  });

  assert.equal(code, 1);
  assert.equal(io.json().reason, 'internal_error');
  assert.equal(fs.existsSync(path.join(dir, 'provenance.jsonl')), false);
});

test('reuse.v1 rejects same local id with different asset_id before writing', async () => {
  const cases = [
    {
      local: withComputedAssetId(gene({ id: 'shared-id', strategy: ['local strategy'] })),
      fetched: withComputedAssetId(gene({ id: 'shared-id', strategy: ['hub strategy'] })),
    },
    {
      local: withComputedAssetId(capsule({ id: 'shared-id', summary: 'local capsule' })),
      fetched: withComputedAssetId(capsule({ id: 'shared-id', summary: 'hub capsule' })),
    },
  ];

  for (const row of cases) {
    const store = fakeStore([row.local]);
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-conflict-'));
    const io = capture();
    const code = await runReuseCommand(['--id', row.fetched.asset_id, '--json'], {
      out: io.out,
      assetsDir: dir,
      assetStore: store,
      fetchAssetById: async () => row.fetched,
    });

    assert.equal(code, 1);
    assert.equal(io.json().reason, 'internal_error');
    assert.equal(io.json().message, 'local asset id conflict');
    assert.equal(store.writes.length, 0);
    assert.equal(fs.existsSync(path.join(dir, 'provenance.jsonl')), false);
    assert.equal(row.local.asset_id === row.fetched.asset_id, false);
  }
});

test('reuse.v1 allows idempotent same local id and asset_id', async () => {
  const cases = [
    withComputedAssetId(gene({ id: 'same-gene-id' })),
    withComputedAssetId(capsule({ id: 'same-capsule-id' })),
  ];

  for (const fetched of cases) {
    const store = fakeStore([fetched]);
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-idempotent-'));
    const io = capture();
    const code = await runReuseCommand(['--id', fetched.asset_id, '--json'], {
      out: io.out,
      assetsDir: dir,
      assetStore: store,
      fetchAssetById: async () => Object.assign({}, fetched),
    });

    assert.equal(code, 0);
    assert.equal(io.json().asset_id, fetched.asset_id);
    assert.equal(store.writes.length, 1);
  }
});

test('reuse.v1 rejects Hub assets whose asset_id does not match content hash', async () => {
  const store = fakeStore([]);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-mismatch-'));
  const io = capture();
  const code = await runReuseCommand(['--id', 'sha256:bad', '--json'], {
    out: io.out,
    assetsDir: dir,
    assetStore: store,
    fetchAssetById: async () => gene({ asset_id: 'sha256:bad' }),
  });

  assert.equal(code, 1);
  assert.equal(io.json().reason, 'internal_error');
  assert.equal(store.writes.length, 0);
  assert.equal(fs.existsSync(path.join(dir, 'provenance.jsonl')), false);
});

test('reuse.v1 maps missing assets to not_found', async () => {
  const io = capture();
  const code = await runReuseCommand(['--id=missing', '--json'], {
    out: io.out,
    assetStore: fakeStore([]),
    fetchAssetById: async () => null,
  });

  assert.equal(code, 1);
  assert.deepEqual({ ok: io.json().ok, contract: io.json().contract, reason: io.json().reason }, {
    ok: false,
    contract: 'reuse.v1',
    reason: 'not_found',
  });
});

test('reuse.v1 rejects positional ids before fetch or store', async () => {
  const store = fakeStore([]);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-positional-'));
  const io = capture();
  const fetchedAsset = withComputedAssetId(gene());
  let fetched = false;
  const code = await runReuseCommand([fetchedAsset.asset_id, '--json'], {
    out: io.out,
    assetsDir: dir,
    assetStore: store,
    fetchAssetById: async () => {
      fetched = true;
      return fetchedAsset;
    },
  });

  assert.equal(code, 1);
  assert.equal(io.json().reason, 'unsupported');
  assert.equal(fetched, false);
  assert.equal(store.writes.length, 0);
  assert.equal(fs.existsSync(path.join(dir, 'provenance.jsonl')), false);
});

test('reuse.v1 rejects unsupported flags before fetch or store', async () => {
  const io = capture();
  let fetched = false;
  const store = fakeStore([]);
  const code = await runReuseCommand(['--id', 'sha256:gene', '--future', '--json'], {
    out: io.out,
    assetStore: store,
    fetchAssetById: async () => {
      fetched = true;
      return gene({ asset_id: 'sha256:gene' });
    },
  });

  assert.equal(code, 1);
  assert.equal(io.json().reason, 'unsupported');
  assert.equal(fetched, false);
  assert.equal(store.writes.length, 0);
});

test('reuse.v1 rejects missing --json before fetch or store', async () => {
  const store = fakeStore([]);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-no-json-'));
  const io = capture();
  const fetchedAsset = withComputedAssetId(gene());
  let fetched = false;
  const code = await runReuseCommand(['--id', fetchedAsset.asset_id], {
    out: io.out,
    assetsDir: dir,
    assetStore: store,
    fetchAssetById: async () => {
      fetched = true;
      return fetchedAsset;
    },
  });

  assert.equal(code, 1);
  assert.equal(io.json().reason, 'unsupported');
  assert.equal(fetched, false);
  assert.equal(store.writes.length, 0);
  assert.equal(fs.existsSync(path.join(dir, 'provenance.jsonl')), false);
});

test('reuse.v1 rejects assets that would be re-identified by local storage', async () => {
  const store = fakeStore([]);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-unstable-'));
  const io = capture();
  const fetched = gene();
  delete fetched.schema_version;
  fetched.asset_id = computeAssetId(fetched);
  const code = await runReuseCommand(['--id', fetched.asset_id, '--json'], {
    out: io.out,
    assetsDir: dir,
    assetStore: store,
    fetchAssetById: async () => fetched,
  });

  assert.equal(code, 1);
  assert.equal(io.json().reason, 'internal_error');
  assert.equal(store.writes.length, 0);
  assert.equal(fs.existsSync(path.join(dir, 'provenance.jsonl')), false);
});

test('publish.v1 bundle preparation rejects a bare Gene', () => {
  const result = buildPublishBundle(['g'], { assetStore: fakeStore([gene({ asset_id: 'g' })]) });
  assert.equal(result.ok, false);
  assert.equal(result.reason, 'bundle_required');
});

test('publish.v1 bundle preparation rejects a bare Capsule', () => {
  const result = buildPublishBundle(['c'], { assetStore: fakeStore([capsule({ asset_id: 'c' })]) });
  assert.equal(result.ok, false);
  assert.equal(result.reason, 'bundle_required');
});

test('publish.v1 rejects multiple bundle assets before silent drop', async () => {
  const cases = [
    {
      name: 'genes',
      args: ['--asset=g1', '--asset=g2', '--asset=c'],
      records: [
        gene({ asset_id: 'g1', id: 'gene-1' }),
        gene({ asset_id: 'g2', id: 'gene-2' }),
        capsule({ asset_id: 'c', gene: 'g1' }),
      ],
    },
    {
      name: 'capsules',
      args: ['--asset=g', '--asset=c1', '--asset=c2'],
      records: [
        gene({ asset_id: 'g' }),
        capsule({ asset_id: 'c1', id: 'cap-1', gene: 'g' }),
        capsule({ asset_id: 'c2', id: 'cap-2', gene: 'g' }),
      ],
    },
    {
      name: 'events',
      args: ['--asset=g', '--asset=c', '--asset=e1', '--asset=e2'],
      records: [
        gene({ asset_id: 'g' }),
        capsule({ asset_id: 'c', gene: 'g' }),
        event({ asset_id: 'e1', id: 'event-1' }),
        event({ asset_id: 'e2', id: 'event-2' }),
      ],
    },
  ];

  for (const row of cases) {
    const io = capture();
    let validated = false;
    let published = false;
    const code = await runPublishCommand(row.args.concat(['--json']), {
      out: io.out,
      hubUrl: 'https://hub.test',
      nodeSecret: 's'.repeat(64),
      a2a: fakeA2a(),
      assetStore: fakeStore(row.records),
      validate: async () => {
        validated = true;
        throw new Error(row.name + ' should not validate');
      },
      publish: async () => {
        published = true;
        throw new Error(row.name + ' should not publish');
      },
    });

    assert.equal(code, 1);
    assert.equal(io.json().reason, 'bundle_required');
    assert.equal(validated, false);
    assert.equal(published, false);
  }
});

test('publish.v1 loads local asset store once for multiple refs', () => {
  const loads = { genes: 0, capsules: 0, events: 0 };
  const bundle = buildPublishBundle(['g', 'c', 'e'], {
    assetStore: {
      loadGenes: () => {
        loads.genes++;
        return [gene({ asset_id: 'g' })];
      },
      loadCapsules: () => {
        loads.capsules++;
        return [capsule({ asset_id: 'c', gene: 'g' })];
      },
      readAllEvents: () => {
        loads.events++;
        return [event({ asset_id: 'e', gene: 'g', capsule: 'c' })];
      },
    },
  });

  assert.equal(bundle.ok, true);
  assert.deepEqual(loads, { genes: 1, capsules: 1, events: 1 });
  assert.deepEqual(bundle.original.map(asset => asset.asset_id), ['g', 'c', 'e']);
});

test('publish.v1 rejects missing --json before validate or publish', async () => {
  const io = capture();
  let validated = false;
  let published = false;
  const code = await runPublishCommand(['--asset=g', '--asset=c'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => {
      validated = true;
      throw new Error('publish without --json should not validate');
    },
    publish: async () => {
      published = true;
      throw new Error('publish without --json should not publish');
    },
  });

  assert.equal(code, 1);
  assert.equal(io.json().reason, 'unsupported');
  assert.equal(validated, false);
  assert.equal(published, false);
});

test('publish.v1 rejects positional args before validate or publish', async () => {
  const io = capture();
  let validated = false;
  let published = false;
  const code = await runPublishCommand(['g', 'c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => {
      validated = true;
      throw new Error('positional publish args should not validate');
    },
    publish: async () => {
      published = true;
      throw new Error('positional publish args should not publish');
    },
  });

  assert.equal(code, 1);
  assert.equal(io.json().reason, 'unsupported');
  assert.equal(validated, false);
  assert.equal(published, false);
});

test('publish.v1 dry-run calls validate and includes estimated credits', async () => {
  const io = capture();
  let validated = false;
  let fetched = false;
  let published = false;
  const code = await runPublishCommand(['--asset', 'g', '--asset', 'c', '--dry-run', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async message => {
      validated = true;
      assert.equal(message.message_type, 'publish');
      return {
        ok: true,
        status: 200,
        body: { payload: { valid: true, credits: { required: 2, available: 5, estimated: 2, balance_kind: 'node_balance' } } },
      };
    },
    publish: async () => {
      published = true;
      throw new Error('dry-run should not publish');
    },
    hubFetch: async () => {
      fetched = true;
      throw new Error('dry-run should not call hubFetch');
    },
  });
  const json = io.json();

  assert.equal(code, 0);
  assert.equal(json.contract, 'publish.v1');
  assert.equal(json.mode, 'dry_run');
  assert.equal(json.blocked, false);
  assert.equal(json.gates.quality, 'pass');
  assert.deepEqual(json.credits, {
    required: 2,
    available: 5,
    estimated: 2,
    balance_kind: 'node_balance',
  });
  assert.ok(Array.isArray(json.payload.assets));
  assert.equal(validated, true);
  assert.equal(published, false);
  assert.equal(fetched, false);
});

test('publish.v1 dry-run does not create a persistent node id', async () => {
  const io = capture();
  const a2a = require('../src/gep/a2aProtocol');
  const home = fs.mkdtempSync(path.join(os.tmpdir(), 'publish-v1-dry-run-home-'));
  const repoNodeFile = path.join(__dirname, '..', '.evomap_node_id');
  const hadRepoNodeFile = fs.existsSync(repoNodeFile);
  const oldHome = process.env.EVOLVER_HOME;
  const oldNodeId = process.env.A2A_NODE_ID;
  const oldSecret = process.env.A2A_NODE_SECRET;
  let repoNodeCreated = false;
  try {
    process.env.EVOLVER_HOME = home;
    delete process.env.A2A_NODE_ID;
    process.env.A2A_NODE_SECRET = 's'.repeat(64);
    if (a2a._resetCachedNodeIdForTesting) a2a._resetCachedNodeIdForTesting();

    const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
      out: io.out,
      hubUrl: 'https://hub.test',
      assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
      validate: async message => {
        assert.equal(message.sender_id, 'node_000000000000');
        assert.equal(message.payload.signature.length, 64);
        return { ok: true, status: 200, body: { payload: { valid: true } } };
      },
    });

    repoNodeCreated = !hadRepoNodeFile && fs.existsSync(repoNodeFile);
    assert.equal(code, 0);
    assert.equal(io.json().mode, 'dry_run');
    assert.equal(fs.existsSync(path.join(home, 'node_id')), false);
    assert.equal(repoNodeCreated, false);
  } finally {
    if (repoNodeCreated) {
      try { fs.unlinkSync(repoNodeFile); } catch (_) {}
    }
    if (oldHome === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = oldHome;
    if (oldNodeId === undefined) delete process.env.A2A_NODE_ID;
    else process.env.A2A_NODE_ID = oldNodeId;
    if (oldSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = oldSecret;
    if (a2a._resetCachedNodeIdForTesting) a2a._resetCachedNodeIdForTesting();
  }
});

test('publish.v1 dry-run quality failure returns blocked quality gate', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({
      ok: false,
      status: 400,
      body: { payload: { valid: false, credits: { required: 4, available: 8, estimated: 4, balance_kind: 'node_balance' } } },
    }),
    publish: async () => {
      throw new Error('dry-run should not publish after quality failure');
    },
  });
  const json = io.json();

  assert.equal(code, 0);
  assert.equal(json.ok, true);
  assert.equal(json.blocked, true);
  assert.equal(json.gates.quality, 'fail');
  assert.deepEqual(json.block_reasons, ['quality_gate_failed']);
  assert.equal(json.credits.required, 4);
  assert.equal(json.credits.available, 8);
  assert.equal(json.credits.estimated, 4);
  assert.equal(json.credits.balance_kind, 'node_balance');
  assert.ok(Array.isArray(json.payload.assets));
});

test('publish.v1 actual fail-closes empty validate responses before publish', async () => {
  const cases = [
    {
      name: 'empty body',
      response: () => ({ ok: true, status: 200, json: async () => ({}) }),
    },
    {
      name: 'empty payload',
      response: () => ({ ok: true, status: 200, json: async () => ({ payload: {} }) }),
    },
    {
      name: 'no response body',
      response: () => ({
        ok: true,
        status: 200,
        json: async () => { throw new Error('empty body'); },
        text: async () => '',
      }),
    },
  ];

  for (const row of cases) {
    const io = capture();
    let published = false;
    const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
      out: io.out,
      hubUrl: 'https://hub.test',
      nodeSecret: 's'.repeat(64),
      a2a: fakeA2a(),
      assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
      hubFetch: async url => {
        if (url.endsWith('/a2a/validate')) return row.response();
        if (url.endsWith('/a2a/publish')) {
          published = true;
          return { ok: true, status: 200, json: async () => ({ payload: { status: 'accepted' } }) };
        }
        throw new Error('unexpected endpoint');
      },
    });
    const json = io.json();

    assert.equal(code, 1, row.name);
    assert.equal(json.ok, false, row.name);
    assert.equal(json.contract, 'publish.v1', row.name);
    assert.equal(json.reason, 'quality_gate_failed', row.name);
    assert.equal(json.retryable, false, row.name);
    assert.equal(published, false, row.name);
  }
});

test('publish.v1 dry-run does not success-preview empty validate responses', async () => {
  const cases = [
    {
      name: 'empty body',
      response: () => ({ ok: true, status: 200, json: async () => ({}) }),
    },
    {
      name: 'empty payload',
      response: () => ({ ok: true, status: 200, json: async () => ({ payload: {} }) }),
    },
    {
      name: 'no response body',
      response: () => ({
        ok: true,
        status: 200,
        json: async () => { throw new Error('empty body'); },
        text: async () => '',
      }),
    },
  ];

  for (const row of cases) {
    const io = capture();
    const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
      out: io.out,
      hubUrl: 'https://hub.test',
      nodeSecret: 's'.repeat(64),
      a2a: fakeA2a(),
      assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
      hubFetch: async url => {
        assert.ok(url.endsWith('/a2a/validate'), row.name);
        return row.response();
      },
    });
    const json = io.json();

    assert.equal(code, 0, row.name);
    assert.equal(json.contract, 'publish.v1', row.name);
    assert.equal(json.mode, 'dry_run', row.name);
    assert.notDeepEqual({ ok: json.ok, blocked: json.blocked }, { ok: true, blocked: false }, row.name);
    assert.equal(json.blocked, true, row.name);
    assert.equal(json.gates.quality, 'fail', row.name);
    assert.deepEqual(json.block_reasons, ['quality_gate_failed'], row.name);
  }
});

test('publish.v1 reads invalid JSON Response text for stable Hub reasons', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    hubFetch: async () => new Response('auth_required', { status: 400 }),
  });
  const json = io.json();

  assert.equal(code, 1);
  assert.equal(json.ok, false);
  assert.equal(json.reason, 'auth_required');
  assert.equal(json.message, 'Hub authentication required');
});

test('publish.v1 parses valid JSON Response bodies without regression', async () => {
  const io = capture();
  const seen = [];
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    hubFetch: async url => {
      seen.push(url);
      if (url.endsWith('/a2a/validate')) {
        return new Response(JSON.stringify({ payload: { valid: true } }), { status: 200 });
      }
      return new Response(JSON.stringify({ payload: { status: 'accepted' } }), { status: 200 });
    },
  });
  const json = io.json();

  assert.equal(code, 0);
  assert.equal(json.status, 'accepted');
  assert.equal(seen.length, 2);
});

test('publish.v1 dry-run without Hub auth fails auth_required instead of fake pass', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: null,
    a2a: {
      buildPublishBundle: () => {
        throw new Error('publishBundle: node_secret is required for signing');
      },
    },
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    hubFetch: async () => {
      throw new Error('dry-run should not reach hubFetch without auth');
    },
  });
  const json = io.json();

  assert.equal(code, 1);
  assert.equal(json.ok, false);
  assert.equal(json.mode, 'dry_run');
  assert.equal(json.reason, 'auth_required');
});

test('publish.v1 validate failures map status to contract reasons', async () => {
  const cases = [
    [401, 'auth_required', false],
    [403, 'auth_required', false],
    [402, 'insufficient_credits', false],
    [429, 'network_error', true],
    [500, 'network_error', true],
    [0, 'network_error', true],
  ];

  for (const [status, reason, retryable] of cases) {
    const actual = capture();
    const actualCode = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
      out: actual.out,
      hubUrl: 'https://hub.test',
      nodeSecret: 's'.repeat(64),
      a2a: fakeA2a(),
      assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
      validate: async () => ({ ok: false, status, body: { payload: { error: 'raw upstream failure' } } }),
      publish: async () => { throw new Error('publish should not run after validate failure'); },
    });
    assert.equal(actualCode, 1);
    assert.equal(actual.json().reason, reason);
    assert.equal(actual.json().retryable, retryable);

  }
});

test('publish.v1 preserves stable Hub capability reasons instead of quality gate fallback', async () => {
  for (const reason of ['unsupported', 'cli_unavailable']) {
    const dryRun = capture();
    const dryRunCode = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
      out: dryRun.out,
      hubUrl: 'https://hub.test',
      nodeSecret: 's'.repeat(64),
      a2a: fakeA2a(),
      assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
      validate: async () => ({ ok: false, status: 400, reason, body: { payload: { reason } } }),
      publish: async () => {
        throw new Error('publish should not run after capability failure');
      },
    });
    assert.equal(dryRunCode, 1);
    assert.equal(dryRun.json().ok, false);
    assert.equal(dryRun.json().reason, reason);
    assert.equal(dryRun.json().block_reasons, undefined);

    const actual = capture();
    const actualCode = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
      out: actual.out,
      hubUrl: 'https://hub.test',
      nodeSecret: 's'.repeat(64),
      a2a: fakeA2a(),
      assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
      validate: async () => ({ ok: false, status: 404, body: { payload: { reason } } }),
      publish: async () => {
        throw new Error('publish should not run after capability failure');
      },
    });
    assert.equal(actualCode, 1);
    assert.equal(actual.json().reason, reason);
  }
});

test('reuse.v1 preserves stable Hub capability reasons instead of not_found fallback', async () => {
  for (const reason of ['unsupported', 'cli_unavailable']) {
    const io = capture();
    const code = await runReuseCommand(['--id=sha256:missing', '--json'], {
      out: io.out,
      hubUrl: 'https://hub.test',
      nodeSecret: 's'.repeat(64),
      a2a: fakeA2a(),
      hubFetch: async () => ({ ok: false, status: 404, json: async () => ({ payload: { reason } }) }),
    });

    assert.equal(code, 1);
    assert.equal(io.json().ok, false);
    assert.equal(io.json().reason, reason);
    assert.notEqual(io.json().reason, 'not_found');
  }
});

test('reuse.v1 uses node secret for node-scoped fetch when OAuth is also available', async () => {
  const nodeSecret = 'n'.repeat(64);
  const oauthToken = 'oauth-access-token';
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-node-auth-'));
  const fetched = withComputedAssetId(gene());
  const io = capture();
  let buildHubHeadersCalls = 0;
  let fetchCalls = 0;
  const a2a = Object.assign({}, fakeA2a(), {
    buildHubHeaders: () => {
      buildHubHeadersCalls++;
      return { Authorization: 'Bearer ' + oauthToken };
    },
  });

  const code = await runReuseCommand(['--id', fetched.asset_id, '--json'], {
    out: io.out,
    assetsDir: dir,
    assetStore: fakeStore([]),
    hubUrl: 'https://hub.test',
    nodeSecret,
    a2a,
    hubFetch: async (url, opts) => {
      fetchCalls++;
      assert.ok(url.endsWith('/a2a/fetch'));
      assert.equal(authorizationHeader(opts.headers), 'Bearer ' + nodeSecret);
      assert.notEqual(authorizationHeader(opts.headers), 'Bearer ' + oauthToken);
      return { ok: true, status: 200, json: async () => ({ payload: { assets: [fetched] } }) };
    },
  });

  assert.equal(code, 0);
  assert.equal(fetchCalls, 1);
  assert.equal(buildHubHeadersCalls, 0);
  assert.equal(io.json().status, 'ok');
});

test('publish.v1 redacts literal local node secrets from stdout JSON and dependency stderr', async () => {
  const io = capture();
  let stderr = '';
  const originalStderrWrite = process.stderr.write;
  const secret = 'a'.repeat(64);
  process.stderr.write = function (chunk, ...args) {
    stderr += String(chunk);
    if (typeof args[args.length - 1] === 'function') args[args.length - 1]();
    return true;
  };
  try {
    const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
      out: io.out,
      hubUrl: 'https://hub.test',
      a2a: Object.assign({}, fakeA2a(), { getHubNodeSecret: () => secret }),
      assetStore: {
        loadGenes: () => {
          console.warn('raw node_secret=' + secret + ' token=abcdefghijklmnop path=/tmp/.env');
          process.stderr.write('direct node_secret=' + secret + ' token=mnopqrstuvwxyz12 path=/tmp/.env\n');
          return [gene({ asset_id: 'g', strategy: ['avoid ' + secret] })];
        },
        loadCapsules: () => [capsule({ asset_id: 'c', gene: 'g', summary: 'contains ' + secret })],
        readAllEvents: () => [],
      },
      validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
    });
    const jsonText = JSON.stringify(io.json());

    assert.equal(code, 0);
    assert.equal(jsonText.includes(secret), false);
    assert.equal(stderr.includes(secret), false);
    assert.equal(stderr.includes('token=abcdefghijklmnop'), false);
    assert.equal(stderr.includes('token=mnopqrstuvwxyz12'), false);
    assert.equal(stderr.includes('/tmp/.env'), false);
  } finally {
    process.stderr.write = originalStderrWrite;
  }
});

test('publish.v1 redacts secret-shaped object keys before dry-run preview', async () => {
  const io = capture();
  const marker = 'token=abcdefghijklmnop';
  const marker2 = 'secret=mnopqrstuvwxyz12';
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([
      gene({ asset_id: 'g', metadata: { [marker]: 'safe-value', [marker2]: 'second-value' } }),
      capsule({ asset_id: 'c', gene: 'g' }),
    ]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
  });
  const json = io.json();
  const text = JSON.stringify(json);

  assert.equal(code, 0);
  assert.equal(text.includes(marker), false);
  assert.equal(text.includes(marker2), false);
  assert.equal(json.blocked, false);
  assert.equal(json.gates.leak, 'pass');
  assert.equal(json.payload.assets[0].metadata[marker], undefined);
  assert.equal(json.payload.assets[0].metadata[marker2], undefined);
  assert.equal(json.payload.assets[0].metadata['[REDACTED]'], 'safe-value');
  assert.equal(json.payload.assets[0].metadata['[REDACTED]_2'], 'second-value');
});

test('publish.v1 redacts nested secret keys and values before dry-run preview', async () => {
  const io = capture();
  const secret = 'q'.repeat(64);
  const marker = 'token=abcdefghijklmnop';
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: secret,
    a2a: fakeA2a(),
    assetStore: fakeStore([
      gene({ asset_id: 'g', metadata: { nested: { [marker]: 'value ' + secret, safe: ['again ' + secret] } } }),
      capsule({ asset_id: 'c', gene: 'g' }),
    ]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
  });
  const json = io.json();
  const nested = json.payload.assets[0].metadata.nested;
  const text = JSON.stringify(json);

  assert.equal(code, 0);
  assert.equal(text.includes(secret), false);
  assert.equal(text.includes(marker), false);
  assert.equal(nested[marker], undefined);
  assert.equal(nested['[REDACTED]'], 'value [REDACTED]');
  assert.deepEqual(nested.safe, ['again [REDACTED]']);
});

test('publish.v1 dry-run does not block when redaction leaves final payload clean', async () => {
  const io = capture();
  let validated = false;
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([
      gene({ asset_id: 'g' }),
      capsule({ asset_id: 'c', gene: 'g', summary: 'secret=abcdefghijklmnop' }),
    ]),
    validate: async () => {
      validated = true;
      return { ok: true, status: 200, body: { payload: { valid: true } } };
    },
  });
  const json = io.json();

  assert.equal(code, 0);
  assert.equal(json.ok, true);
  assert.equal(json.blocked, false);
  assert.equal(json.gates.leak, 'pass');
  assert.equal(json.payload.assets[1].summary, '[REDACTED]');
  assert.equal(validated, true);
});

test('publish.v1 actual hard-rejects a final payload with residual leak', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([
      gene({ asset_id: 'g' }),
      capsule({ asset_id: 'c', gene: 'g', summary: 'internal endpoint 10.1.2.3:8080' }),
    ]),
    validate: async () => { throw new Error('validate should not run when locally blocked'); },
    publish: async () => { throw new Error('publish should not run when locally blocked'); },
  });

  assert.equal(code, 1);
  assert.equal(io.json().reason, 'leak_detected');
});

test('publish.v1 dry-run hard leak blocks without exposing payload assets', async () => {
  const io = capture();
  const oldLeakMode = process.env.EVOLVER_LEAK_CHECK;
  let validated = false;
  let published = false;
  delete process.env.EVOLVER_LEAK_CHECK;
  try {
    const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
      out: io.out,
      hubUrl: 'https://hub.test',
      nodeSecret: 's'.repeat(64),
      a2a: fakeA2a(),
      assetStore: fakeStore([
        gene({ asset_id: 'g' }),
        capsule({ asset_id: 'c', gene: 'g', summary: 'internal endpoint 10.1.2.3:8080' }),
      ]),
      validate: async () => {
        validated = true;
        throw new Error('dry-run should not validate when locally blocked');
      },
      publish: async () => {
        published = true;
        throw new Error('dry-run should not publish when locally blocked');
      },
    });
    const json = io.json();

    assert.equal(code, 0);
    assert.equal(io.text().includes('10.1.2.3:8080'), false);
    assert.equal(json.ok, true);
    assert.equal(json.blocked, true);
    assert.equal(json.gates.leak, 'fail');
    assert.deepEqual(json.block_reasons, ['leak_detected']);
    assert.ok(Array.isArray(json.assets));
    assert.equal(json.payload, undefined);
    assert.equal(validated, false);
    assert.equal(published, false);
  } finally {
    if (oldLeakMode === undefined) delete process.env.EVOLVER_LEAK_CHECK;
    else process.env.EVOLVER_LEAK_CHECK = oldLeakMode;
  }
});

test('publish.v1 leak gate ignores legacy warn and off modes', async () => {
  const oldLeakMode = process.env.EVOLVER_LEAK_CHECK;
  try {
    for (const mode of ['warn', 'off']) {
      process.env.EVOLVER_LEAK_CHECK = mode;

      const actual = capture();
      let actualValidated = false;
      let actualPublished = false;
      const actualCode = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
        out: actual.out,
        hubUrl: 'https://hub.test',
        nodeSecret: 's'.repeat(64),
        a2a: fakeA2a(),
        assetStore: fakeStore([
          gene({ asset_id: 'g' }),
          capsule({ asset_id: 'c', gene: 'g', summary: 'internal endpoint 10.1.2.3:8080' }),
        ]),
        validate: async () => {
          actualValidated = true;
          throw new Error('actual should not validate when locally blocked');
        },
        publish: async () => {
          actualPublished = true;
          throw new Error('actual should not publish when locally blocked');
        },
      });

      assert.equal(actualCode, 1, mode);
      assert.equal(actual.json().reason, 'leak_detected', mode);
      assert.equal(actualValidated, false, mode);
      assert.equal(actualPublished, false, mode);

      const dryRun = capture();
      let dryRunValidated = false;
      let dryRunPublished = false;
      const dryRunCode = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
        out: dryRun.out,
        hubUrl: 'https://hub.test',
        nodeSecret: 's'.repeat(64),
        a2a: fakeA2a(),
        assetStore: fakeStore([
          gene({ asset_id: 'g' }),
          capsule({ asset_id: 'c', gene: 'g', summary: 'internal endpoint 10.1.2.3:8080' }),
        ]),
        validate: async () => {
          dryRunValidated = true;
          throw new Error('dry-run should not validate when locally blocked');
        },
        publish: async () => {
          dryRunPublished = true;
          throw new Error('dry-run should not publish when locally blocked');
        },
      });
      const dryRunJson = dryRun.json();

      assert.equal(dryRunCode, 0, mode);
      assert.equal(dryRunJson.blocked, true, mode);
      assert.deepEqual(dryRunJson.block_reasons, ['leak_detected'], mode);
      assert.equal(dryRunJson.gates.leak, 'fail', mode);
      assert.equal(dryRunValidated, false, mode);
      assert.equal(dryRunPublished, false, mode);
    }
  } finally {
    if (oldLeakMode === undefined) delete process.env.EVOLVER_LEAK_CHECK;
    else process.env.EVOLVER_LEAK_CHECK = oldLeakMode;
  }
});

test('publish.v1 dry-run missing refs read local files without initializing assetStore', async () => {
  const io = capture();
  const dir = path.join(os.tmpdir(), 'publish-v1-no-init-' + Date.now() + '-' + Math.random().toString(16).slice(2));
  const code = await runPublishCommand(['--asset=missing-gene', '--asset=missing-capsule', '--dry-run', '--json'], {
    out: io.out,
    assetsDir: dir,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
  });

  assert.equal(code, 1);
  assert.equal(io.json().reason, 'schema_invalid');
  assert.equal(fs.existsSync(dir), false);
});

test('publish.v1 maps thrown hub fetch during validate to retryable network_error', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    hubFetch: async () => { throw new Error('ECONNRESET raw socket failure'); },
    publish: async () => { throw new Error('publish should not run after validate failure'); },
  });
  const json = io.json();

  assert.equal(code, 1);
  assert.equal(json.reason, 'network_error');
  assert.equal(json.retryable, true);
  assert.equal(JSON.stringify(json).includes('ECONNRESET'), false);
});

test('publish.v1 actual publish maps thrown hub fetch to retryable network_error', async () => {
  const io = capture();
  let calls = 0;
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    hubFetch: async () => {
      calls++;
      if (calls === 1) return { ok: true, status: 200, json: async () => ({ payload: { valid: true } }) };
      throw new Error('DNS failure for hub.test');
    },
  });
  const json = io.json();

  assert.equal(code, 1);
  assert.equal(json.reason, 'network_error');
  assert.equal(json.retryable, true);
  assert.equal(JSON.stringify(json).includes('DNS failure'), false);
});

test('publish.v1 actual publish requires Hub auth before validate or publish', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: null,
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => {
      throw new Error('actual publish should not validate without auth');
    },
    publish: async () => {
      throw new Error('actual publish should not publish without auth');
    },
  });
  const json = io.json();

  assert.equal(code, 1);
  assert.equal(json.reason, 'auth_required');
});

test('publish.v1 uses node secret for node-scoped validate and publish when OAuth is also available', async () => {
  const nodeSecret = 'n'.repeat(64);
  const oauthToken = 'oauth-access-token';
  const io = capture();
  const seen = {};
  let buildHubHeadersCalls = 0;
  const a2a = Object.assign({}, fakeA2a(), {
    buildHubHeaders: () => {
      buildHubHeadersCalls++;
      return { Authorization: 'Bearer ' + oauthToken };
    },
  });

  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret,
    a2a,
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    hubFetch: async (url, opts) => {
      const auth = authorizationHeader(opts.headers);
      assert.equal(auth, 'Bearer ' + nodeSecret);
      assert.notEqual(auth, 'Bearer ' + oauthToken);
      if (url.endsWith('/a2a/validate')) {
        seen.validate = auth;
        return { ok: true, status: 200, json: async () => ({ payload: { valid: true } }) };
      }
      if (url.endsWith('/a2a/publish')) {
        seen.publish = auth;
        return { ok: true, status: 200, json: async () => ({ payload: { status: 'accepted' } }) };
      }
      throw new Error('unexpected endpoint');
    },
  });

  assert.equal(code, 0);
  assert.deepEqual(seen, {
    validate: 'Bearer ' + nodeSecret,
    publish: 'Bearer ' + nodeSecret,
  });
  assert.equal(buildHubHeadersCalls, 0);
  assert.equal(io.json().status, 'accepted');
});

test('publish.v1 rejects OAuth-only authorization for node-scoped dry-run and actual publish', async () => {
  const oauthA2a = {
    buildPublishBundle: () => {
      throw new Error('publishBundle: node_secret is required for signing');
    },
    buildHubHeaders: () => ({ Authorization: 'Bearer oauth-access-token' }),
  };

  for (const row of [
    { name: 'dry-run', args: ['--asset=g', '--asset=c', '--dry-run', '--json'], mode: 'dry_run' },
    { name: 'actual', args: ['--asset=g', '--asset=c', '--json'], mode: 'publish' },
  ]) {
    const io = capture();
    let hubCalls = 0;
    const code = await runPublishCommand(row.args, {
      out: io.out,
      hubUrl: 'https://hub.test',
      nodeSecret: null,
      a2a: oauthA2a,
      assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
      hubFetch: async () => {
        hubCalls++;
        throw new Error(row.name + ' should not send OAuth to node-scoped endpoint');
      },
    });

    assert.equal(code, 1, row.name);
    assert.equal(hubCalls, 0, row.name);
    assert.equal(io.json().mode, row.mode, row.name);
    assert.equal(io.json().reason, 'auth_required', row.name);
  }
});

test('publish.v1 assets summary is generated from final publish payload', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: mutatingA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
  });
  const json = io.json();

  assert.equal(code, 0);
  assert.deepEqual(json.assets, json.payload.assets.map(asset => ({ asset_id: asset.asset_id, type: asset.type })));
  assert.equal(json.payload.assets[0].asset_id, computeAssetId(json.payload.assets[0]));
  assert.equal(json.payload.assets[1].asset_id, computeAssetId(json.payload.assets[1]));
  assert.equal(json.payload.assets[1].execution_trace.length, 1);
});

test('publish.v1 actual publishes final sanitized rehashed and resigned payload', async () => {
  const io = capture();
  const secret = 'h'.repeat(64);
  const leaked = 'token=abcdefghijklmnop';
  let validatedMessage = null;
  let publishedMessage = null;
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: secret,
    a2a: signingMutatingA2a(secret, leaked),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async message => {
      validatedMessage = JSON.parse(JSON.stringify(message));
      return { ok: true, status: 200, body: { payload: { valid: true } } };
    },
    publish: async message => {
      publishedMessage = JSON.parse(JSON.stringify(message));
      return { ok: true, status: 200, body: { payload: { status: 'accepted' } } };
    },
  });
  const json = io.json();
  const assets = publishedMessage.payload.assets;

  assert.equal(code, 0);
  assert.equal(JSON.stringify(validatedMessage).includes(leaked), false);
  assert.equal(JSON.stringify(publishedMessage).includes(leaked), false);
  assert.equal(assets[0].asset_id, computeAssetId(assets[0]));
  assert.equal(assets[1].asset_id, computeAssetId(assets[1]));
  assert.equal(publishedMessage.payload.signature, expectedSignature(assets, secret));
  assert.equal(validatedMessage.payload.signature, publishedMessage.payload.signature);
  assert.deepEqual(json.assets, assets.map(asset => ({ asset_id: asset.asset_id, type: asset.type })));
});

test('publish.v1 dry-run validates final sanitized rehashed and resigned payload', async () => {
  const io = capture();
  const secret = 'h'.repeat(64);
  const leaked = 'token=abcdefghijklmnop';
  let validatedMessage = null;
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: secret,
    a2a: signingMutatingA2a(secret, leaked),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async message => {
      validatedMessage = JSON.parse(JSON.stringify(message));
      return { ok: true, status: 200, body: { payload: { valid: true } } };
    },
  });
  const json = io.json();
  const assets = validatedMessage.payload.assets;

  assert.equal(code, 0);
  assert.equal(JSON.stringify(validatedMessage).includes(leaked), false);
  assert.equal(assets[0].asset_id, computeAssetId(assets[0]));
  assert.equal(assets[1].asset_id, computeAssetId(assets[1]));
  assert.equal(validatedMessage.payload.signature, expectedSignature(assets, secret));
  assert.deepEqual(json.assets, assets.map(asset => ({ asset_id: asset.asset_id, type: asset.type })));
});

test('publish.v1 omits unsafe original_asset_id values from stdout JSON', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=token=abcdefghijklmnop', '--asset=c', '--dry-run', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([
      gene({ asset_id: 'token=abcdefghijklmnop' }),
      capsule({ asset_id: 'c', gene: 'token=abcdefghijklmnop' }),
    ]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
  });
  const json = io.json();

  assert.equal(code, 0);
  assert.equal(JSON.stringify(json).includes('token=abcdefghijklmnop'), false);
});

test('publish.v1 actual returns accepted status and charged credits', async () => {
  const io = capture();
  let validated = false;
  let published = false;
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => {
      validated = true;
      return { ok: true, status: 200, body: { payload: { valid: true } } };
    },
    publish: async () => {
      published = true;
      return {
        ok: true,
        status: 200,
        body: { payload: { status: 'accepted', receipt_id: 'rcpt_1', bundle_id: 'bdl_1', credits: { required: 3, available: 6, charged: 3, balance_kind: 'node_balance' } } },
      };
    },
  });
  const json = io.json();

  assert.equal(code, 0);
  assert.equal(validated, true);
  assert.equal(published, true);
  assert.equal(json.status, 'accepted');
  assert.equal(json.receipt_id, 'rcpt_1');
  assert.equal(json.bundle_id, 'bdl_1');
  assert.equal(json.credits.charged, 3);
});

test('publish.v1 treats already_published 200 responses as idempotent success', async () => {
  for (const decision of ['reject', 'rejected']) {
    const io = capture();
    const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
      out: io.out,
      hubUrl: 'https://hub.test',
      nodeSecret: 's'.repeat(64),
      a2a: fakeA2a(),
      assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
      validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
      publish: async () => ({
        ok: true,
        status: 200,
        body: {
          payload: {
            decision,
            reason: 'already_published',
            target_asset_id: 'sha256:existing-published-asset',
            credits: { required: 0, available: 6, charged: 0, balance_kind: 'node_balance' },
          },
        },
      }),
    });
    const json = io.json();
    const stdout = io.text();

    assert.equal(code, 0);
    assert.equal(json.ok, true);
    assert.equal(json.contract, 'publish.v1');
    assert.equal(json.mode, 'publish');
    assert.equal(json.status, 'published');
    assert.equal(json.reason, undefined);
    assert.notEqual(json.reason, 'internal_error');
    assert.equal(json.receipt_id, undefined);
    assert.equal(json.credits.required, 0);
    assert.equal(json.credits.available, 6);
    assert.equal(json.credits.charged, 0);
    assert.equal(stdout.includes('already_published'), false);
    assert.equal(stdout.includes('sha256:existing-published-asset'), false);
  }
});

test('publish.v1 does not treat other reject reasons as success', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
    publish: async () => ({
      ok: true,
      status: 200,
      body: { payload: { decision: 'reject', reason: 'internal_error', bundle_id: 'bdl_1' } },
    }),
  });
  const json = io.json();

  assert.equal(code, 1);
  assert.equal(json.ok, false);
  assert.equal(json.reason, 'internal_error');
  assert.equal(json.status, undefined);
});

test('publish.v1 credits do not fabricate estimated or charged from required', async () => {
  const dryRun = capture();
  const dryRunCode = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
    out: dryRun.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true, credits: { required: 2, available: 5 } } } }),
  });
  assert.equal(dryRunCode, 0);
  assert.equal(dryRun.json().credits.required, 2);
  assert.equal(dryRun.json().credits.estimated, undefined);

  const actual = capture();
  const actualCode = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: actual.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
    publish: async () => ({ ok: true, status: 200, body: { payload: { status: 'accepted', credits: { required: 3, available: 7 } } } }),
  });
  assert.equal(actualCode, 0);
  assert.equal(actual.json().credits.required, 3);
  assert.equal(actual.json().credits.charged, undefined);
});

test('publish.v1 credits keep zero and integer strings but omit fractional numeric fields', async () => {
  const dryRun = capture();
  const dryRunCode = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
    out: dryRun.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({
      ok: true,
      status: 200,
      body: { payload: { valid: true, credits: { required: 0, available: '5', estimated: '0', balance_kind: 'node_balance' } } },
    }),
  });
  assert.equal(dryRunCode, 0);
  assert.deepEqual(dryRun.json().credits, {
    required: 0,
    available: 5,
    estimated: 0,
    balance_kind: 'node_balance',
  });

  const actual = capture();
  const actualCode = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: actual.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
    publish: async () => ({
      ok: true,
      status: 200,
      body: { payload: { status: 'accepted', credits: { required: 1.25, available: '2.5', estimated: 3.1, charged: '4.2', balance_kind: 'node_balance' } } },
    }),
  });
  const fractionalCredits = actual.json().credits;

  assert.equal(actualCode, 0);
  assert.equal(fractionalCredits.required, undefined);
  assert.equal(fractionalCredits.available, undefined);
  assert.equal(fractionalCredits.estimated, undefined);
  assert.equal(fractionalCredits.charged, undefined);
  assert.equal(fractionalCredits.balance_kind, 'node_balance');
});

test('publish.v1 failure messages do not echo raw Hub errors', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
    publish: async () => ({
      ok: false,
      status: 500,
      reason: 'upstream token=abcdefghijklmnop',
      body: { payload: { error: 'upstream token=abcdefghijklmnop' } },
    }),
  });
  const json = io.json();

  assert.equal(code, 1);
  assert.equal(json.reason, 'network_error');
  assert.equal(json.message, 'Hub unreachable');
  assert.equal(JSON.stringify(json).includes('token=abcdefghijklmnop'), false);
});

test('publish.v1 failed publish omits lifecycle status from failure envelope', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
    publish: async () => ({
      ok: false,
      status: 500,
      body: { payload: { status: 'accepted', credits: { required: 1, available: 2 } } },
    }),
  });
  const json = io.json();

  assert.equal(code, 1);
  assert.equal(json.ok, false);
  assert.equal(json.reason, 'network_error');
  assert.equal(json.retryable, true);
  assert.equal(json.status, undefined);
  assert.equal(json.credits.required, 1);
});

test('publish.v1 credits omit unsafe balance_kind strings', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
    publish: async () => ({
      ok: true,
      status: 200,
      body: { payload: { status: 'accepted', credits: { required: 1, available: 2, balance_kind: 'token=abcdefghijklmnop' } } },
    }),
  });
  const json = io.json();

  assert.equal(code, 0);
  assert.equal(json.credits.required, 1);
  assert.equal(json.credits.balance_kind, undefined);
  assert.equal(JSON.stringify(json).includes('token=abcdefghijklmnop'), false);
});

test('publish.v1 success does not fabricate lifecycle status or receipt', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
    publish: async () => ({ ok: true, status: 200, body: { payload: { ok: true } } }),
  });
  const json = io.json();

  assert.equal(code, 1);
  assert.equal(json.ok, false);
  assert.equal(json.reason, 'internal_error');
  assert.equal(json.status, undefined);
  assert.equal(json.receipt_id, undefined);
});

test('publish.v1 rejects non-lifecycle Hub status ok', async () => {
  const io = capture();
  const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: io.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
    publish: async () => ({ ok: true, status: 200, body: { payload: { status: 'ok', bundle_id: 'bdl_1' } } }),
  });
  const json = io.json();

  assert.equal(code, 1);
  assert.equal(json.ok, false);
  assert.equal(json.reason, 'internal_error');
  assert.equal(json.status, undefined);
  assert.notEqual(json.status, 'accepted');
});

test('publish.v1 maps Hub accept and quarantine decisions', async () => {
  const accepted = capture();
  const acceptedCode = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: accepted.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
    publish: async () => ({ ok: true, status: 200, body: { payload: { decision: 'accept', bundle_id: 'bdl_1' } } }),
  });
  assert.equal(acceptedCode, 0);
  assert.equal(accepted.json().status, 'accepted');

  const quarantined = capture();
  const quarantinedCode = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
    out: quarantined.out,
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
    publish: async () => ({ ok: true, status: 200, body: { payload: { decision: 'quarantine', bundle_id: 'bdl_2' } } }),
  });
  const quarantinedJson = quarantined.json();

  assert.equal(quarantinedCode, 1);
  assert.equal(quarantinedJson.ok, false);
  assert.equal(quarantinedJson.reason, 'quality_gate_failed');
  assert.equal(quarantinedJson.status, undefined);
  assert.equal(quarantinedJson.bundle_id, undefined);
  assert.equal(quarantinedJson.gates.quality, 'fail');
});

test('publish.v1 rejects non-A2A ok and approved decisions', async () => {
  for (const decision of ['ok', 'approved']) {
    const io = capture();
    const code = await runPublishCommand(['--asset=g', '--asset=c', '--json'], {
      out: io.out,
      hubUrl: 'https://hub.test',
      nodeSecret: 's'.repeat(64),
      a2a: fakeA2a(),
      assetStore: fakeStore([gene({ asset_id: 'g' }), capsule({ asset_id: 'c', gene: 'g' })]),
      validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
      publish: async () => ({ ok: true, status: 200, body: { payload: { decision, bundle_id: 'bdl_1' } } }),
    });
    const json = io.json();

    assert.equal(code, 1);
    assert.equal(json.reason, 'internal_error');
    assert.equal(json.status, undefined);
  }
});

test('reuse.v1 default output rejects missing --json before dependency stdout', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-stdout-default-'));
  const fetched = withComputedAssetId(gene());
  const captured = await captureProcessOutput(() => runReuseCommand(['--id', fetched.asset_id], {
    assetsDir: dir,
    assetStore: fakeStore([]),
    fetchAssetById: async () => {
      process.stdout.write('[fetch] direct stdout\n');
      return fetched;
    },
  }));
  const json = singleJsonLine(captured.stdout);

  assert.equal(captured.result, 1);
  assert.equal(json.contract, 'reuse.v1');
  assert.equal(json.reason, 'unsupported');
  assert.equal(captured.stdout.includes('[fetch]'), false);
  assert.equal(captured.stderr.includes('[fetch]'), false);
});

test('publish.v1 default output rejects missing --json before dependency stdout', async () => {
  const captured = await captureProcessOutput(() => runPublishCommand(['--asset=g', '--asset=c', '--dry-run'], {
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: {
      loadGenes: () => {
        process.stdout.write('[store] direct stdout\n');
        return [gene({ asset_id: 'g' })];
      },
      loadCapsules: () => [capsule({ asset_id: 'c', gene: 'g' })],
      readAllEvents: () => [],
    },
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
  }));
  const json = singleJsonLine(captured.stdout);

  assert.equal(captured.result, 1);
  assert.equal(json.contract, 'publish.v1');
  assert.equal(json.reason, 'unsupported');
  assert.equal(captured.stdout.includes('[store]'), false);
  assert.equal(captured.stderr.includes('[store]'), false);
});

test('publish.v1 --json redirects dependency console output away from stdout', async () => {
  const io = capture();
  let stdout = '';
  let stderr = '';
  const originalStdoutWrite = process.stdout.write;
  const originalStderrWrite = process.stderr.write;
  process.stdout.write = function (chunk, ...args) {
    stdout += String(chunk);
    if (typeof args[args.length - 1] === 'function') args[args.length - 1]();
    return true;
  };
  process.stderr.write = function (chunk, ...args) {
    stderr += String(chunk);
    if (typeof args[args.length - 1] === 'function') args[args.length - 1]();
    return true;
  };
  try {
    const code = await runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
      out: io.out,
      hubUrl: 'https://hub.test',
      nodeSecret: 's'.repeat(64),
      a2a: fakeA2a(),
      assetStore: {
        loadGenes: () => {
          console.log('[AssetStore] migrated');
          return [gene({ asset_id: 'g' })];
        },
        loadCapsules: () => [capsule({ asset_id: 'c', gene: 'g' })],
        readAllEvents: () => [],
      },
      validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
    });

    assert.equal(code, 0);
    assert.equal(stdout, '');
    assert.match(stderr, /AssetStore/);
    assert.equal(io.json().contract, 'publish.v1');
  } finally {
    process.stdout.write = originalStdoutWrite;
    process.stderr.write = originalStderrWrite;
  }
});

test('reuse.v1 --json keeps default stdout JSON-only when dependencies write stdout', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reuse-v1-stdout-'));
  const fetched = withComputedAssetId(gene());
  const store = fakeStore([]);
  const captured = await captureProcessOutput(() => runReuseCommand(['--id', fetched.asset_id, '--json'], {
    assetsDir: dir,
    assetStore: store,
    fetchAssetById: async () => {
      process.stdout.write('[fetch] direct stdout\n');
      return fetched;
    },
  }));
  const json = singleJsonLine(captured.stdout);

  assert.equal(captured.result, 0);
  assert.equal(json.contract, 'reuse.v1');
  assert.equal(json.status, 'ok');
  assert.equal(captured.stdout.includes('[fetch]'), false);
  assert.match(captured.stderr, /\[fetch\] direct stdout/);
});

test('publish.v1 --json keeps default stdout JSON-only when dependencies write stdout', async () => {
  const captured = await captureProcessOutput(() => runPublishCommand(['--asset=g', '--asset=c', '--dry-run', '--json'], {
    hubUrl: 'https://hub.test',
    nodeSecret: 's'.repeat(64),
    a2a: fakeA2a(),
    assetStore: {
      loadGenes: () => {
        process.stdout.write('[store] direct stdout\n');
        return [gene({ asset_id: 'g' })];
      },
      loadCapsules: () => [capsule({ asset_id: 'c', gene: 'g' })],
      readAllEvents: () => [],
    },
    validate: async () => ({ ok: true, status: 200, body: { payload: { valid: true } } }),
  }));
  const json = singleJsonLine(captured.stdout);

  assert.equal(captured.result, 0);
  assert.equal(json.contract, 'publish.v1');
  assert.equal(json.mode, 'dry_run');
  assert.equal(captured.stdout.includes('[store]'), false);
  assert.match(captured.stderr, /\[store\] direct stdout/);
});
