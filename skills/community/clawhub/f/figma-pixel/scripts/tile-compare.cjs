#!/usr/bin/env node
/**
 * tile-compare.cjs
 *
 * Splits reference and screenshot into 300px horizontal tiles,
 * runs pixelmatch on each, and reports which zones have the most mismatch.
 *
 * Usage:
 *   node scripts/tile-compare.cjs <reference-png> <screenshot-png> [output-json] [tile-height]
 *
 * Arguments:
 *   reference-png   Path to Figma reference PNG
 *   screenshot-png  Path to captured screenshot PNG
 *   output-json     Where to write tile-report.json (optional)
 *   tile-height     Tile height in px (default: 300)
 *
 * Output (stdout): JSON with per-tile diffPercent and topMismatchTiles
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { compareTiles } = require('../lib/tile-compare.cjs');
const { writeJson } = require('../lib/figma-cache.cjs');

const [refPath, scrPath, outputArg, tileArg] = process.argv.slice(2);

if (!refPath || !scrPath) {
  console.error([
    'Usage: node scripts/tile-compare.cjs <reference-png> <screenshot-png> [output-json] [tile-height]',
    '',
    'Example:',
    '  node scripts/tile-compare.cjs \\',
    '    figma-pixel-runs/my-project/shared/figma/.../reference-image.png \\',
    '    figma-pixel-runs/my-project/run-id/capture/captured-page.png \\',
    '    figma-pixel-runs/my-project/run-id/pixelmatch/tile-report.json',
  ].join('\n'));
  process.exit(1);
}

const tileHeight = tileArg ? parseInt(tileArg, 10) : 300;

const result = compareTiles(refPath, scrPath, { tileHeight });

if (outputArg) {
  const outputPath = path.resolve(outputArg);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  writeJson(outputPath, result);
}

console.log(JSON.stringify(result, null, 2));
