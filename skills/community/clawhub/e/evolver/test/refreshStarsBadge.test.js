'use strict';

const test = require('node:test');
const assert = require('node:assert');

const { metric, rewriteStarsValue } = require('../scripts/refresh_stars_badge');

test('metric formats counts the way shields.io does', () => {
  assert.equal(metric(999), '999');
  assert.equal(metric(1000), '1k');
  assert.equal(metric(1100), '1.1k');
  assert.equal(metric(8336), '8.3k'); // current EvoMap/evolver count
  assert.equal(metric(9999), '10k'); // 9.999 -> "10.0" -> trim ".0"
  assert.equal(metric(12345), '12k');
  assert.equal(metric(23456), '23k');
  assert.equal(metric(150000), '150k');
  assert.equal(metric(1500000), '1.5M');
});

test('metric is defensive about junk input', () => {
  assert.equal(metric(NaN), 'NaN');
  assert.equal(metric(-5), '-5');
  assert.equal(metric(0), '0');
});

const BADGE = (v) =>
  `[![GitHub stars](https://img.shields.io/badge/Stars-${v}-2b3137?logo=github&logoColor=white)](https://github.com/EvoMap/evolver/stargazers)`;

test('rewriteStarsValue swaps the value in the real badge URL', () => {
  assert.equal(rewriteStarsValue(BADGE('8.3k'), '12k'), BADGE('12k'));
});

test('rewriteStarsValue is idempotent when already current', () => {
  const before = BADGE('8.3k');
  assert.equal(rewriteStarsValue(before, '8.3k'), before);
});

test('rewriteStarsValue leaves content without a Stars badge untouched', () => {
  const other = '[![License](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](x)';
  assert.equal(rewriteStarsValue(other, '12k'), other);
});

test('rewriteStarsValue does not touch a dynamic github/stars badge', () => {
  // A dynamic badge must not be matched -- only static `badge/Stars-` URLs.
  const dynamic = 'https://img.shields.io/github/stars/EvoMap/evolver?style=social';
  assert.equal(rewriteStarsValue(dynamic, '12k'), dynamic);
});

test('rewriteStarsValue updates every occurrence', () => {
  const doc = `${BADGE('8.3k')}\n\n...later...\n\n${BADGE('8.3k')}`;
  assert.equal(rewriteStarsValue(doc, '9k'), `${BADGE('9k')}\n\n...later...\n\n${BADGE('9k')}`);
});
