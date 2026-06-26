'use strict';

const test = require('node:test');
const assert = require('node:assert');
const { geneToSkillMd } = require('../src/gep/skillPublisher');

test('geneToSkillMd: top-level avoid field renders in dedicated ## Avoid section', () => {
  const gene = {
    id: 'gene_distilled_retry_with_backoff',
    summary: 'Retry with exponential backoff on transient errors',
    category: 'repair',
    signals_match: ['timeout', 'econnreset'],
    strategy: [
      'Detect transient error class (timeout, ECONNRESET, 5xx)',
      'Sleep with exponential backoff and jitter',
      'Cap total attempts and surface a clear error',
    ],
    avoid: [
      'retrying on 4xx client errors',
      'unbounded retry loops without a deadline',
    ],
    validation: ['node --check src/retry.js'],
  };
  const md = geneToSkillMd(gene);
  assert.match(md, /^## Strategy$/m, 'strategy section present');
  assert.match(md, /^## Avoid$/m, 'dedicated avoid section present');
  assert.match(md, /^- retrying on 4xx client errors$/m);
  assert.match(md, /^- unbounded retry loops without a deadline$/m);
  // AVOID items should NOT appear as strategy list items
  assert.doesNotMatch(md, /^\d+\. \*\*Avoid\*\*/m, 'avoid must not be bolded as strategy step');
  assert.doesNotMatch(md, /\*\*AVOID\*\*/i);
});

test('geneToSkillMd: legacy "AVOID: ..." strategy steps are moved to ## Avoid section', () => {
  const gene = {
    id: 'gene_distilled_legacy',
    summary: 'Legacy gene with AVOID prefix inside strategy (pre-2026-04-21)',
    category: 'repair',
    signals_match: ['legacy'],
    strategy: [
      'Write the right thing carefully',
      'AVOID: hardcoding secrets',
      'AVOID: swallowing exceptions silently',
      'Document the rationale',
    ],
    validation: ['node --check ok.js'],
  };
  const md = geneToSkillMd(gene);
  assert.match(md, /^## Avoid$/m);
  assert.match(md, /^- hardcoding secrets$/m);
  assert.match(md, /^- swallowing exceptions silently$/m);
  // Strategy section should skip AVOID lines entirely, so we expect 2 numbered items,
  // not 4. Also no "**AVOID**" bolding.
  const strategyBlock = md.split(/^## Avoid$/m)[0].split(/^## Strategy$/m)[1] || '';
  assert.doesNotMatch(strategyBlock, /AVOID/i, 'AVOID lines must be stripped from strategy block');
  assert.match(strategyBlock, /^1\. \*\*Write\*\* -- /m);
  assert.match(strategyBlock, /^2\. \*\*Document\*\* -- /m);
});

test('geneToSkillMd: no avoid section when gene has neither avoid field nor AVOID: steps', () => {
  const gene = {
    id: 'gene_distilled_clean',
    summary: 'Clean gene without any anti-patterns',
    category: 'innovate',
    signals_match: ['clean'],
    strategy: [
      'Plan the change',
      'Implement it',
      'Verify',
    ],
    validation: ['node --check ok.js'],
  };
  const md = geneToSkillMd(gene);
  assert.doesNotMatch(md, /^## Avoid$/m);
});

test('geneToSkillMd: determiners ("The", "This") are not extracted as verbs', () => {
  const gene = {
    id: 'gene_distilled_determiner_guard',
    summary: 'Guard against determiner being mistaken as verb',
    category: 'optimize',
    signals_match: ['guard'],
    strategy: [
      'The build output must be checked before upload',
      'Run the unit tests',
      'Verify integrity',
    ],
    validation: ['node --check ok.js'],
  };
  const md = geneToSkillMd(gene);
  assert.doesNotMatch(md, /\*\*The\*\*/);
  assert.match(md, /^1\. The build output must be checked before upload$/m);
  assert.match(md, /^2\. \*\*Run\*\* -- the unit tests$/m);
});

test('geneToSkillMd: anti-pattern markers (NEVER, DON\'T) are not bolded as verbs', () => {
  const gene = {
    id: 'gene_distilled_antipattern_markers',
    summary: 'Anti-pattern marker guard',
    category: 'repair',
    signals_match: ['guard'],
    strategy: [
      'NEVER log raw secrets',
      "DON'T catch Error without rethrow",
      'Do the right thing',
    ],
    validation: ['node --check ok.js'],
  };
  const md = geneToSkillMd(gene);
  assert.doesNotMatch(md, /\*\*NEVER\*\*/i);
  assert.doesNotMatch(md, /\*\*DON\*\*/i);
  // "NEVER log raw secrets" starts with "NEVER" (uppercase, no lowercase),
  // which already would not match /^[A-Z][a-z]+/, but we keep the explicit
  // assertion in case anyone relaxes the regex later.
});
