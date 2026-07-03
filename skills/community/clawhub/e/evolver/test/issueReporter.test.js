const assert = require('assert');

const MODULE_PATH = require.resolve('../src/gep/issueReporter');

function withFetchMock(mock, fn) {
  const original = global.fetch;
  global.fetch = mock;
  return Promise.resolve(fn()).finally(function () { global.fetch = original; });
}

function jsonResponse(body, status) {
  return {
    ok: status == null || (status >= 200 && status < 300),
    status: status || 200,
    json: async function () { return body; },
    text: async function () { return JSON.stringify(body); },
  };
}

(async function run() {
  delete require.cache[MODULE_PATH];
  const { findExistingIssue } = require('../src/gep/issueReporter');

  // Case 1: search returns matching open issue -> returns object
  await withFetchMock(async function (url, opts) {
    assert.ok(String(url).includes('/search/issues'), 'should hit search API');
    assert.ok(String(url).includes('is%3Aopen'), 'should request open issues');
    return jsonResponse({
      items: [
        { number: 397, html_url: 'https://github.com/x/y/issues/397', title: '[Auto] Recurring failure: Repeated failures with gene: gene_gep_repair_from_errors', state: 'open' }
      ],
    });
  }, async function () {
    const result = await findExistingIssue('x/y', '[Auto] Recurring failure: Repeated failures with gene: gene_gep_repair_from_errors', 'faketoken');
    assert.ok(result && result.number === 397, 'should find existing open issue');
  });

  // Case 2: search returns no items -> returns null
  await withFetchMock(async function () {
    return jsonResponse({ items: [] });
  }, async function () {
    const result = await findExistingIssue('x/y', '[Auto] Recurring failure: Something new', 'faketoken');
    assert.strictEqual(result, null, 'should return null when no matches');
  });

  // Case 3: search returns only closed issues (API scoped to open via query, but guard client-side)
  await withFetchMock(async function () {
    return jsonResponse({
      items: [
        { number: 100, html_url: 'https://github.com/x/y/issues/100', title: '[Auto] Recurring failure: foo', state: 'closed' }
      ],
    });
  }, async function () {
    const result = await findExistingIssue('x/y', '[Auto] Recurring failure: foo', 'faketoken');
    assert.strictEqual(result, null, 'closed issues should not count');
  });

  // Case 4: network failure -> returns null (non-fatal)
  await withFetchMock(async function () { throw new Error('network down'); }, async function () {
    const result = await findExistingIssue('x/y', '[Auto] Recurring failure: foo', 'faketoken');
    assert.strictEqual(result, null, 'network error should return null');
  });

  // Case 5: non-OK response -> returns null
  await withFetchMock(async function () {
    return { ok: false, status: 403, text: async function () { return 'rate limited'; }, json: async function () { return {}; } };
  }, async function () {
    const result = await findExistingIssue('x/y', '[Auto] Recurring failure: foo', 'faketoken');
    assert.strictEqual(result, null, 'non-OK should return null');
  });

  // Case 6: empty title -> returns null without hitting fetch
  let called = false;
  await withFetchMock(async function () { called = true; return jsonResponse({ items: [] }); }, async function () {
    const result = await findExistingIssue('x/y', '', 'faketoken');
    assert.strictEqual(result, null, 'empty title should short-circuit');
    assert.strictEqual(called, false, 'fetch should not be called for empty title');
  });

  // Case 7: default repo matches config.SELF_PR_REPO (no legacy repo drift since v1.69.7)
  const savedIssueRepo = process.env.EVOLVER_ISSUE_REPO;
  delete process.env.EVOLVER_ISSUE_REPO;
  try {
    delete require.cache[MODULE_PATH];
    delete require.cache[require.resolve('../src/config')];
    const { getConfig } = require('../src/gep/issueReporter');
    const { SELF_PR_REPO } = require('../src/config');
    const cfg = getConfig();
    assert.ok(cfg, 'getConfig should return an object when auto-issue is enabled by default');
    assert.strictEqual(cfg.repo, SELF_PR_REPO, 'issueReporter default repo must equal config.SELF_PR_REPO');
    assert.strictEqual(SELF_PR_REPO, 'EvoMap/evolver', 'SELF_PR_REPO default should be EvoMap/evolver');
  } finally {
    if (savedIssueRepo === undefined) {
      delete process.env.EVOLVER_ISSUE_REPO;
    } else {
      process.env.EVOLVER_ISSUE_REPO = savedIssueRepo;
    }
  }

  // Case A: computeErrorKey is stable across (Nx) occurrence counts.
  // Regression: the (Nx) prefix had been hashed verbatim, mutating the key
  // every cycle and defeating recentIssueKeys dedup.
  delete require.cache[MODULE_PATH];
  const { computeErrorKey } = require('../src/gep/issueReporter');
  const k3 = computeErrorKey(['recurring_errsig(3x):timeout on API', 'failure_loop_detected']);
  const k4 = computeErrorKey(['recurring_errsig(4x):timeout on API', 'failure_loop_detected']);
  const k5 = computeErrorKey(['recurring_errsig(5x):timeout on API', 'failure_loop_detected']);
  assert.strictEqual(k3, k4, 'errorKey should be stable across (Nx) counts');
  assert.strictEqual(k4, k5, 'errorKey should be stable across (Nx) counts');

  // Case B: shouldReport enforces minStreak even when streak signal is absent.
  // Regression: prior guard "streakCount > 0 && < minStreak" was a no-op when
  // the consecutive_failure_streak_N signal was missing.
  const { shouldReport } = require('../src/gep/issueReporter');
  const gatedCfg = { repo: 'x/y', cooldownMs: 86400000, minStreak: 5 };
  assert.strictEqual(
    shouldReport(['failure_loop_detected', 'recurring_errsig(2x):foo'], gatedCfg),
    false,
    'minStreak gate must apply when streak signal is absent'
  );
  assert.strictEqual(
    shouldReport(['failure_loop_detected', 'recurring_errsig(2x):foo', 'consecutive_failure_streak_10'], gatedCfg),
    true,
    'should pass when streak meets minStreak'
  );

  // Case C: findExistingIssue no longer matches unrelated titles via loose
  // substring fallback. Prior `it.title.indexOf(titleSig) !== -1` matched
  // issues that merely contained the search signature as a substring.
  await withFetchMock(async function () {
    return jsonResponse({
      items: [
        { number: 12345, state: 'open', html_url: 'https://x/y/12345',
          title: 'META discussion about [Auto] Recurring failure: boom with unrelated context' }
      ],
    });
  }, async function () {
    const target = '[Auto] Recurring failure: boom';
    const result = await findExistingIssue('x/y', target, 'faketoken');
    assert.strictEqual(result, null, 'substring fallback must not match unrelated titles');
  });

  // --- classifyFailure: local triage before opening a public issue --------
  const { classifyFailure } = require('../src/gep/issueReporter');

  // host_no_transcript: nothing for evolver to evolve from
  assert.strictEqual(
    classifyFailure({ signals: ['failure_loop_detected'], recentEvents: [], sessionLog: '' }).bucket,
    'host_no_transcript', 'empty session log -> host_no_transcript');
  assert.strictEqual(
    classifyFailure({ signals: [], recentEvents: [], sessionLog: 'foo [NO SESSION LOGS FOUND] bar' }).bucket,
    'host_no_transcript', 'sentinel -> host_no_transcript');

  // host_provider_error: a provider 400 the host emitted (not evolver core)
  assert.strictEqual(
    classifyFailure({ signals: [], recentEvents: [], sessionLog: '[LLM ERROR] 400 field MaxTokens invalid, should be in [1, 65536]' }).bucket,
    'host_provider_error', 'provider MaxTokens error -> host_provider_error');

  // local_gene_no_blast: locally-generated gene whose cycles change nothing
  assert.strictEqual(
    classifyFailure({
      signals: ['failure_loop_detected', 'ban_gene:sha256:14cc0b42'],
      recentEvents: [
        { outcome: { status: 'failed' }, blast_radius: { files: 0, lines: 0 } },
        { outcome: { status: 'failed' }, blast_radius: { files: 0, lines: 0 } },
      ],
      sessionLog: 'Result: SUCCESS ... Files changed: 0 (metadata-only cycle)',
    }).bucket,
    'local_gene_no_blast', 'local sha256 gene + zero blast -> local_gene_no_blast');

  // unclassified (default-open): published gene, productive blast, real transcript -> still filed
  assert.strictEqual(
    classifyFailure({
      signals: ['failure_loop_detected', 'ban_gene:gene_gep_repair_from_errors'],
      recentEvents: [{ outcome: { status: 'failed' }, blast_radius: { files: 3, lines: 40 } }],
      sessionLog: 'TypeError: cannot read property x of undefined at src/gep/foo.js:10',
    }).bucket,
    'unclassified', 'published gene + productive blast + real log -> filed (unclassified)');

  // a productive failure on a locally-generated gene is NOT suppressed
  assert.strictEqual(
    classifyFailure({
      signals: ['failure_loop_detected', 'ban_gene:gene_auto_2ce76294'],
      recentEvents: [{ outcome: { status: 'failed' }, blast_radius: { files: 2, lines: 9 } }],
      sessionLog: 'some real evolution transcript with an actual error',
    }).bucket,
    'unclassified', 'local gene but productive blast -> not local_gene_no_blast');

  console.log('issueReporter.test.js: OK');
})().catch(function (err) {
  console.error(err);
  process.exit(1);
});
