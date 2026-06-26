#!/usr/bin/env node
/**
 * extract-strokes-map.cjs
 *
 * Reads implementation-spec.json and emits strokes-map.json:
 * a flat list of every node with a visible stroke, plus a summary of unique
 * stroke colors, weights, and which sides strokes appear on.
 *
 * Purpose: give the agent a single compact reference for every border /
 * outline / divider in the design — so each CSS `border*`, `outline*`, or
 * `box-shadow` rule can be cited back to a Figma node instead of eyeballed
 * (or missed entirely) from the reference image.
 *
 * Usage:
 *   node scripts/extract-strokes-map.cjs <implementation-spec.json> [output-path]
 */

'use strict';

const fs = require('fs');
const path = require('path');

const SIDES = ['top', 'right', 'bottom', 'left'];

function activeSides(stroke) {
  const individual = stroke.individualStrokeWeights;
  if (!individual) return SIDES.slice();
  return SIDES.filter((side) => (individual[side] ?? 0) > 0);
}

function strokeColorHex(stroke) {
  if (!stroke?.color) return null;
  return typeof stroke.color === 'string' ? stroke.color : (stroke.color.hex || null);
}

function collectStrokes(node, pathLabels, collected) {
  const nextPath = [...pathLabels, node.name || node.type || '?'];
  if (node.visible !== false && node.stroke) {
    const sides = activeSides(node.stroke);
    const individual = node.stroke.individualStrokeWeights || null;
    const perSideWeight = individual
      ? SIDES.reduce((acc, side) => { acc[side] = individual[side] ?? 0; return acc; }, {})
      : SIDES.reduce((acc, side) => { acc[side] = node.stroke.weight ?? 1; return acc; }, {});
    collected.push({
      id: node.id,
      name: node.name,
      type: node.type,
      path: nextPath.join(' > '),
      bounds: node.bounds || null,
      color: strokeColorHex(node.stroke),
      colorWithOpacity: typeof node.stroke.color === 'object' ? node.stroke.color : null,
      weight: node.stroke.weight ?? 1,
      align: node.stroke.align ?? 'INSIDE',
      sides,
      perSideWeight,
      dashPattern: node.stroke.dashPattern || null,
      cornerRadius: node.cornerRadius ?? null,
      cornerRadii: node.cornerRadii || null,
    });
  }
  for (const child of (node.children || [])) collectStrokes(child, nextPath, collected);
}

function summarize(strokes) {
  const colorFreq = new Map();
  const weightFreq = new Map();
  const sideFreq = { top: 0, right: 0, bottom: 0, left: 0 };
  let allSidesCount = 0;
  let partialSidesCount = 0;

  for (const entry of strokes) {
    if (entry.color) colorFreq.set(entry.color, (colorFreq.get(entry.color) || 0) + 1);
    for (const side of entry.sides) {
      const w = entry.perSideWeight[side];
      if (w > 0) {
        weightFreq.set(w, (weightFreq.get(w) || 0) + 1);
        sideFreq[side] += 1;
      }
    }
    if (entry.sides.length === 4) allSidesCount += 1;
    else partialSidesCount += 1;
  }

  const byCountDesc = ([, left], [, right]) => right - left;
  return {
    uniqueColors: [...colorFreq.entries()].sort(byCountDesc).map(([value, count]) => ({ value, count })),
    uniqueWeights: [...weightFreq.entries()].sort(byCountDesc).map(([value, count]) => ({ value, count })),
    sideDistribution: sideFreq,
    allSidesCount,
    partialSidesCount,
  };
}

function buildStrokesMap(spec) {
  const strokes = [];
  for (const section of (spec.sections || [])) collectStrokes(section, [], strokes);
  const summary = summarize(strokes);
  return { ok: true, count: strokes.length, summary, strokes };
}

function main() {
  const [specPath, outputArg] = process.argv.slice(2);
  if (!specPath) {
    console.error('Usage: node scripts/extract-strokes-map.cjs <implementation-spec.json> [output-path]');
    process.exit(1);
  }

  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  const result = buildStrokesMap(spec);
  result.sourcePath = path.resolve(specPath);

  const outputPath = outputArg
    ? path.resolve(outputArg)
    : path.join(path.dirname(path.resolve(specPath)), 'strokes-map.json');

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));

  console.log(JSON.stringify({ ok: true, outputPath, count: result.count }, null, 2));
}

if (require.main === module) main();

module.exports = { buildStrokesMap };
