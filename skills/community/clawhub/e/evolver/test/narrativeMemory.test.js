const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const envKeys = ['EVOLUTION_DIR', 'MEMORY_DIR', 'EVOLVER_REPO_ROOT'];

function freshRequire(modulePath) {
  const resolved = require.resolve(modulePath);
  delete require.cache[resolved];
  return require(resolved);
}

function loadMod(tmpDir) {
  process.env.EVOLUTION_DIR = tmpDir;
  delete require.cache[require.resolve('../src/gep/paths')];
  return freshRequire('../src/gep/narrativeMemory');
}

describe('trimNarrative', () => {
  let tmpDir;
  let savedEnv;
  let mod;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'narrative-test-'));
    savedEnv = {};
    for (const k of envKeys) {
      savedEnv[k] = process.env[k];
      delete process.env[k];
    }
    mod = loadMod(tmpDir);
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns content unchanged when under size limit', () => {
    const small = '# header\n\nshort content\n';
    assert.equal(mod.trimNarrative(small), small);
  });

  it('slices trailing bytes when content lacks any entry headers', () => {
    const big = 'a'.repeat(20_000);
    const trimmed = mod.trimNarrative(big);
    assert.ok(trimmed.length <= 12_000);
    assert.equal(trimmed, big.slice(-12_000));
  });

  it('drops oldest entries past the 30-entry cap once size exceeds the limit', () => {
    // Each entry here is ~350 bytes; 40 entries * 350 = ~14k > 12_000 trigger.
    let content = '# Evolution Narrative\n\n';
    for (let i = 1; i <= 40; i++) {
      content += `### [2025-01-01 00:00:${String(i).padStart(2, '0')}] REPAIR - success\n`;
      content += `- ${'x'.repeat(300)}\n\n`;
    }
    assert.ok(content.length > 12_000, 'precondition: content must exceed size limit');
    const trimmed = mod.trimNarrative(content);
    const entryCount = (trimmed.match(/^### \[/gm) || []).length;
    assert.ok(entryCount <= 30, `entryCount should be <= 30, got ${entryCount}`);
    assert.ok(trimmed.includes('# Evolution Narrative'));
    // Oldest entry removed, newest preserved.
    assert.ok(!trimmed.includes('00:00:01]'));
    assert.ok(trimmed.includes('00:00:40]'));
  });

  it('does not cap at 30 entries when total size stays within limit', () => {
    // Small entries keep the file well under 12_000 bytes, so no trimming occurs.
    let content = '# Evolution Narrative\n\n';
    for (let i = 1; i <= 40; i++) {
      content += `### [2025-01-01 00:00:${String(i).padStart(2, '0')}] REPAIR - success\n- ok\n\n`;
    }
    assert.ok(content.length <= 12_000, 'precondition: content stays within size limit');
    const trimmed = mod.trimNarrative(content);
    assert.equal(trimmed, content);
  });

  it('reduces size when 30 entries still exceed the limit (best-effort)', () => {
    // 30 entries of ~650 bytes each = ~19.5k. Trim should at least shrink the content
    // via entries.slice(-keep), though the 30-entry cap does not fire so the algorithm
    // does not guarantee a <=12_000 result here.
    let content = '# Evolution Narrative\n\n';
    for (let i = 1; i <= 30; i++) {
      content += `### [2025-01-01 00:00:${String(i).padStart(2, '0')}] REPAIR - success\n`;
      content += `- ${'x'.repeat(600)}\n\n`;
    }
    assert.ok(content.length > 12_000, 'precondition: content must exceed size limit');
    const trimmed = mod.trimNarrative(content);
    assert.ok(trimmed.length < content.length, 'trim should shrink oversized input');
    assert.ok(trimmed.includes('# Evolution Narrative'));
    const entryCount = (trimmed.match(/^### \[/gm) || []).length;
    assert.ok(entryCount < 30, 'some entries should be dropped by the size-based slice');
  });
});

describe('recordNarrative', () => {
  let tmpDir;
  let savedEnv;
  let mod;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'narrative-record-'));
    savedEnv = {};
    for (const k of envKeys) {
      savedEnv[k] = process.env[k];
      delete process.env[k];
    }
    mod = loadMod(tmpDir);
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('creates the narrative file with header on first record', () => {
    mod.recordNarrative({
      gene: { id: 'g1', category: 'repair', strategy: ['analyze', 'patch', 'verify'] },
      signals: ['log_error'],
      mutation: { category: 'repair', rationale: 'fix timeout' },
      outcome: { status: 'success', score: 0.9 },
      blast: { files: 2, lines: 10 },
      capsule: { summary: 'fixed db timeout' },
    });
    const narrativePath = path.join(tmpDir, 'evolution_narrative.md');
    const content = fs.readFileSync(narrativePath, 'utf8');
    assert.ok(content.startsWith('# Evolution Narrative'));
    assert.ok(content.includes('REPAIR - success'));
    assert.ok(content.includes('Gene: g1 | Score: 0.90 | Scope: 2 files, 10 lines'));
    assert.ok(content.includes('Signals: [log_error]'));
    assert.ok(content.includes('Why: fix timeout'));
    assert.ok(content.includes('1. analyze'));
    assert.ok(content.includes('Result: fixed db timeout'));
  });

  it('appends to an existing file rather than overwriting', () => {
    mod.recordNarrative({
      gene: { id: 'g1', category: 'repair' },
      signals: ['log_error'],
      mutation: {},
      outcome: { status: 'success', score: 0.8 },
      blast: { files: 1, lines: 1 },
      capsule: {},
    });
    mod.recordNarrative({
      gene: { id: 'g2', category: 'innovate' },
      signals: ['capability_gap'],
      mutation: {},
      outcome: { status: 'failed', score: 0.1 },
      blast: { files: 0, lines: 0 },
      capsule: {},
    });
    const content = fs.readFileSync(
      path.join(tmpDir, 'evolution_narrative.md'),
      'utf8'
    );
    const matches = content.match(/^### \[/gm) || [];
    assert.equal(matches.length, 2);
    assert.ok(content.includes('Gene: g1'));
    assert.ok(content.includes('Gene: g2'));
  });

  it('applies sensible defaults for missing fields', () => {
    mod.recordNarrative({
      gene: null,
      signals: null,
      mutation: null,
      outcome: null,
      blast: null,
      capsule: null,
    });
    const content = fs.readFileSync(
      path.join(tmpDir, 'evolution_narrative.md'),
      'utf8'
    );
    assert.ok(content.includes('UNKNOWN - unknown'));
    assert.ok(content.includes('Gene: (auto)'));
    assert.ok(content.includes('Score: ?'));
    assert.ok(content.includes('Scope: 0 files, 0 lines'));
    assert.ok(content.includes('Signals: [(none)]'));
  });

  it('truncates long rationale and capsule summaries to 200 chars', () => {
    const longRationale = 'x'.repeat(500);
    const longSummary = 'y'.repeat(500);
    mod.recordNarrative({
      gene: { id: 'g1', category: 'repair' },
      signals: ['log_error'],
      mutation: { rationale: longRationale },
      outcome: { status: 'success', score: 0.5 },
      blast: { files: 1, lines: 1 },
      capsule: { summary: longSummary },
    });
    const content = fs.readFileSync(
      path.join(tmpDir, 'evolution_narrative.md'),
      'utf8'
    );
    const whyLine = content.split('\n').find((l) => l.startsWith('- Why:')) || '';
    const resultLine = content.split('\n').find((l) => l.startsWith('- Result:')) || '';
    assert.ok(whyLine.length <= '- Why: '.length + 200);
    assert.ok(resultLine.length <= '- Result: '.length + 200);
  });

  it('limits signals summary to first 4', () => {
    mod.recordNarrative({
      gene: { id: 'g1', category: 'repair' },
      signals: ['s1', 's2', 's3', 's4', 's5', 's6'],
      mutation: {},
      outcome: { status: 'success', score: 0.1 },
      blast: { files: 0, lines: 0 },
      capsule: {},
    });
    const content = fs.readFileSync(
      path.join(tmpDir, 'evolution_narrative.md'),
      'utf8'
    );
    assert.ok(content.includes('Signals: [s1, s2, s3, s4]'));
    assert.ok(!content.includes('s5'));
  });

  it('writes atomically via .tmp rename', () => {
    mod.recordNarrative({
      gene: { id: 'g1', category: 'repair' },
      signals: ['log_error'],
      mutation: {},
      outcome: { status: 'success', score: 0.5 },
      blast: { files: 1, lines: 1 },
      capsule: {},
    });
    const narrativePath = path.join(tmpDir, 'evolution_narrative.md');
    const tmpPath = narrativePath + '.tmp';
    assert.ok(fs.existsSync(narrativePath));
    assert.ok(!fs.existsSync(tmpPath));
  });
});

describe('loadNarrativeSummary', () => {
  let tmpDir;
  let savedEnv;
  let mod;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'narrative-load-'));
    savedEnv = {};
    for (const k of envKeys) {
      savedEnv[k] = process.env[k];
      delete process.env[k];
    }
    mod = loadMod(tmpDir);
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns empty string when file is missing', () => {
    assert.equal(mod.loadNarrativeSummary(), '');
  });

  it('returns empty string when file has no entries', () => {
    fs.writeFileSync(
      path.join(tmpDir, 'evolution_narrative.md'),
      '# Evolution Narrative\n\nheader only\n'
    );
    assert.equal(mod.loadNarrativeSummary(), '');
  });

  it('returns up to the last 8 entries by default', () => {
    let content = '# Evolution Narrative\n\n';
    for (let i = 1; i <= 12; i++) {
      content += `### [2025-01-01 00:00:${String(i).padStart(2, '0')}] REPAIR - success\n- body ${i}\n\n`;
    }
    fs.writeFileSync(path.join(tmpDir, 'evolution_narrative.md'), content);
    const summary = mod.loadNarrativeSummary();
    const entryCount = (summary.match(/^### \[/gm) || []).length;
    assert.ok(entryCount <= 8);
    assert.ok(summary.includes('body 12'));
    assert.ok(!summary.includes('body 1\n'));
  });

  it('respects custom maxChars', () => {
    let content = '# Evolution Narrative\n\n';
    for (let i = 1; i <= 8; i++) {
      content += `### [2025-01-01 00:00:${String(i).padStart(2, '0')}] REPAIR - success\n- ${'x'.repeat(500)}\n\n`;
    }
    fs.writeFileSync(path.join(tmpDir, 'evolution_narrative.md'), content);
    const summary = mod.loadNarrativeSummary(600);
    assert.ok(summary.length <= 600);
    assert.ok(summary.startsWith('### ['));
  });

  it('trims whitespace', () => {
    const content =
      '# Evolution Narrative\n\n### [2025-01-01 00:00:01] REPAIR - success\n- ok\n\n\n\n';
    fs.writeFileSync(path.join(tmpDir, 'evolution_narrative.md'), content);
    const summary = mod.loadNarrativeSummary();
    assert.equal(summary, summary.trim());
  });

  it('uses default limit when maxChars is not a finite number', () => {
    let content = '# Evolution Narrative\n\n';
    for (let i = 1; i <= 3; i++) {
      content += `### [2025-01-01 00:00:${String(i).padStart(2, '0')}] REPAIR - success\n- body ${i}\n\n`;
    }
    fs.writeFileSync(path.join(tmpDir, 'evolution_narrative.md'), content);
    const summary = mod.loadNarrativeSummary('not-a-number');
    assert.ok(summary.includes('body 3'));
  });
});
