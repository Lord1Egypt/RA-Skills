#!/usr/bin/env node
/**
 * extract-typography.cjs
 *
 * Reads implementation-spec.json and emits typography-map.json:
 * a deduped list of unique text styles with occurrences and sample characters.
 *
 * Purpose: give the agent a single compact reference for every text style
 * used in the design (fontFamily, fontSize, fontWeight, lineHeightPx,
 * letterSpacing, color) — so each CSS rule can be derived from exact Figma
 * values instead of eyeballed from the reference image.
 *
 * Usage:
 *   node scripts/extract-typography.cjs <implementation-spec.json> [output-path]
 */

'use strict';

const fs = require('fs');
const path = require('path');

const STYLE_FIELDS = ['fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'lineHeightPx', 'letterSpacing', 'color'];

function styleKey(style) {
  return STYLE_FIELDS.map((field) => (style?.[field] ?? '')).join('|');
}

function pickStyle(style) {
  const picked = {};
  for (const field of STYLE_FIELDS) if (style?.[field] != null) picked[field] = style[field];
  return picked;
}

function addEntry(stylesByKey, style, sampleText) {
  if (!style || !style.fontFamily) return;
  const key = styleKey(style);
  let entry = stylesByKey.get(key);
  if (!entry) {
    entry = { ...pickStyle(style), key, occurrences: 0, samples: [] };
    stylesByKey.set(key, entry);
  }
  entry.occurrences += 1;
  if (sampleText && entry.samples.length < 3) {
    const trimmed = sampleText.trim().slice(0, 40);
    if (trimmed && !entry.samples.includes(trimmed)) entry.samples.push(trimmed);
  }
}

function buildTypographyMap(spec) {
  const stylesByKey = new Map();
  for (const textNode of (spec.texts || [])) {
    addEntry(stylesByKey, textNode.style, textNode.characters);
    for (const run of (textNode.styledRuns || [])) addEntry(stylesByKey, run.style, run.characters);
  }
  const styles = [...stylesByKey.values()].sort((left, right) => {
    if (right.occurrences !== left.occurrences) return right.occurrences - left.occurrences;
    return (right.fontSize || 0) - (left.fontSize || 0);
  });
  return { ok: true, count: styles.length, styles };
}

function main() {
  const [specPath, outputArg] = process.argv.slice(2);
  if (!specPath) {
    console.error('Usage: node scripts/extract-typography.cjs <implementation-spec.json> [output-path]');
    process.exit(1);
  }

  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  const result = buildTypographyMap(spec);
  result.sourcePath = path.resolve(specPath);

  const outputPath = outputArg
    ? path.resolve(outputArg)
    : path.join(path.dirname(path.resolve(specPath)), 'typography-map.json');

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));

  console.log(JSON.stringify({ ok: true, outputPath, count: result.count }, null, 2));
}

if (require.main === module) main();

module.exports = { buildTypographyMap };
