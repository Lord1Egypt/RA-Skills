#!/usr/bin/env node
/**
 * extract-spacing-map.cjs
 *
 * Reads implementation-spec.json and emits spacing-map.json:
 * a flat list of every auto-layout container with its padding + itemSpacing,
 * plus a summary of unique gap and padding values used in the design.
 *
 * Purpose: give the agent a single compact reference for every container's
 * spacing — so each margin / padding / gap in CSS can be cited back to a
 * Figma auto-layout node instead of eyeballed from the reference image.
 *
 * Usage:
 *   node scripts/extract-spacing-map.cjs <implementation-spec.json> [output-path]
 */

'use strict';

const fs = require('fs');
const path = require('path');

function collectContainers(node, pathLabels, collected) {
  const nextPath = [...pathLabels, node.name || node.type || '?'];
  if (node.layout && node.layout.mode) {
    collected.push({
      id: node.id,
      name: node.name,
      path: nextPath.join(' > '),
      mode: node.layout.mode,
      paddingTop: node.layout.paddingTop ?? 0,
      paddingRight: node.layout.paddingRight ?? 0,
      paddingBottom: node.layout.paddingBottom ?? 0,
      paddingLeft: node.layout.paddingLeft ?? 0,
      itemSpacing: node.layout.itemSpacing ?? 0,
      bounds: node.bounds || null,
    });
  }
  for (const child of (node.children || [])) collectContainers(child, nextPath, collected);
}

function summarizeValues(containers) {
  const gapFreq = new Map();
  const paddingFreq = new Map();
  for (const container of containers) {
    const gap = container.itemSpacing;
    gapFreq.set(gap, (gapFreq.get(gap) || 0) + 1);
    for (const side of ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft']) {
      const value = container[side];
      paddingFreq.set(value, (paddingFreq.get(value) || 0) + 1);
    }
  }
  const byCountDesc = ([, left], [, right]) => right - left;
  return {
    uniqueGaps: [...gapFreq.entries()].sort(byCountDesc).map(([value, count]) => ({ value, count })),
    uniquePaddings: [...paddingFreq.entries()].sort(byCountDesc).map(([value, count]) => ({ value, count })),
  };
}

function buildSpacingMap(spec) {
  const containers = [];
  for (const section of (spec.sections || [])) collectContainers(section, [], containers);
  const summary = summarizeValues(containers);
  return { ok: true, count: containers.length, summary, containers };
}

function main() {
  const [specPath, outputArg] = process.argv.slice(2);
  if (!specPath) {
    console.error('Usage: node scripts/extract-spacing-map.cjs <implementation-spec.json> [output-path]');
    process.exit(1);
  }

  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  const result = buildSpacingMap(spec);
  result.sourcePath = path.resolve(specPath);

  const outputPath = outputArg
    ? path.resolve(outputArg)
    : path.join(path.dirname(path.resolve(specPath)), 'spacing-map.json');

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));

  console.log(JSON.stringify({ ok: true, outputPath, count: result.count }, null, 2));
}

if (require.main === module) main();

module.exports = { buildSpacingMap };
