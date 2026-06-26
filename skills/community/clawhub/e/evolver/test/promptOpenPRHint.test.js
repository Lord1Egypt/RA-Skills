'use strict';

// Tests for buildOpenPRHintBlock — the prompt-side rendering of open-PR
// hints surfaced by select.js. Pure string formatter, easy to test.

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { buildOpenPRHintBlock } = require('../src/gep/prompt');

describe('buildOpenPRHintBlock', () => {
  it('returns empty string for null/undefined/empty array', () => {
    assert.equal(buildOpenPRHintBlock(null), '');
    assert.equal(buildOpenPRHintBlock(undefined), '');
    assert.equal(buildOpenPRHintBlock([]), '');
  });

  it('renders one PR hint with token overlap and file sample', () => {
    const block = buildOpenPRHintBlock([
      {
        number: 38,
        title: 'fix(gep): inbound asset_id integrity check',
        headRefName: 'fix/phase4-integrity-tests',
        files: ['src/gep/a2aProtocol.js', 'test/solidifyIntegration.test.js'],
        tokenOverlap: 0.83,
      },
    ]);
    assert.ok(block.includes('Open PR Hint'));
    assert.ok(block.includes('PR #38'));
    assert.ok(block.includes('inbound asset_id integrity check'));
    assert.ok(block.includes('fix/phase4-integrity-tests'));
    assert.ok(block.includes('0.83'));
    assert.ok(block.includes('src/gep/a2aProtocol.js'));
    assert.ok(block.includes('ROLLED BACK at solidify time'));
  });

  it('caps the rendered list at 3 PRs', () => {
    const hints = [];
    for (let i = 1; i <= 5; i++) {
      hints.push({
        number: i,
        title: 'pr ' + i,
        headRefName: 'branch-' + i,
        files: ['src/file' + i + '.js'],
        tokenOverlap: 0.8,
      });
    }
    const block = buildOpenPRHintBlock(hints);
    assert.ok(block.includes('PR #1'));
    assert.ok(block.includes('PR #2'));
    assert.ok(block.includes('PR #3'));
    assert.ok(!block.includes('PR #4'), '4th and beyond should be dropped');
    assert.ok(!block.includes('PR #5'));
  });

  it('truncates long titles to 80 chars', () => {
    const longTitle = 'x'.repeat(200);
    const block = buildOpenPRHintBlock([{
      number: 1,
      title: longTitle,
      headRefName: 'b',
      files: ['a.js'],
      tokenOverlap: 0.7,
    }]);
    // The truncated title appears in the block but not the full 200-char one
    assert.ok(block.includes('x'.repeat(80)));
    assert.ok(!block.includes('x'.repeat(81)));
  });

  it('handles missing files array gracefully', () => {
    const block = buildOpenPRHintBlock([{
      number: 1,
      title: 'no files pr',
      headRefName: 'b',
      // intentionally no files field
      tokenOverlap: 0.9,
    }]);
    assert.ok(block.includes('PR #1'));
    assert.ok(block.includes('(no files listed)'));
  });
});
