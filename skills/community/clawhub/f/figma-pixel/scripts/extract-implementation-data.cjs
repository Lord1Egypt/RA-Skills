#!/usr/bin/env node
/**
 * extract-implementation-data.cjs
 *
 * Extracts a structured implementation spec from figma-node.json in a single pass.
 * Use this before writing any HTML/CSS to avoid repeated ad-hoc JSON queries.
 *
 * Usage:
 *   node scripts/extract-implementation-data.cjs <figma-node-json> [output-path] [max-depth]
 *
 * Arguments:
 *   figma-node-json   Path to figma-node.json produced by fetch-figma-api.cjs
 *   output-path       Where to write implementation-spec.json (optional;
 *                     defaults to same dir as figma-node.json)
 *   max-depth         How deep to walk the node tree (default: 6)
 *
 * Output (implementation-spec.json):
 *   {
 *     ok: true,
 *     rootNodeId,
 *     viewport: { width, height },
 *     sections: [ ... ],       // top-level frames with full annotated tree
 *     texts: [ ... ],          // flat list of all text nodes with style + styledRuns
 *     fonts: [ ... ],          // unique font families
 *     colors: [ ... ],         // unique fill colors sorted by frequency
 *     warnings: [ ... ]        // hidden nodes, invisible fills, inline style overrides
 *   }
 *
 * Each node in sections/tree includes:
 *   id, name, type, visible, bounds (x/y relative to root frame),
 *   fill, stroke, cornerRadius, cornerRadii, opacity,
 *   layout (auto-layout: mode/padding/gap),
 *   effects (shadows/blurs),
 *   characters + style (TEXT nodes only),
 *   styledRuns[] (TEXT nodes with inline bold/italic/colour — each run: { start, end, characters, style })
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { extractFromFile } = require('../lib/implementation-extractor.cjs');

function main() {
  const [figmaNodePath, outputArg, depthArg] = process.argv.slice(2);

  if (!figmaNodePath) {
    console.error([
      'Usage: node scripts/extract-implementation-data.cjs <figma-node-json> [output-path] [max-depth]',
      '',
      'Example:',
      '  node scripts/extract-implementation-data.cjs \\',
      '    figma-pixel-runs/my-project/shared/figma/figma-node.json',
    ].join('\n'));
    process.exit(1);
  }

  const maxDepth = depthArg ? parseInt(depthArg, 10) : 6;

  const result = extractFromFile(figmaNodePath, null, maxDepth);

  const outputPath = outputArg
    ? path.resolve(outputArg)
    : path.join(path.dirname(path.resolve(figmaNodePath)), 'implementation-spec.json');

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));

  if (result.ok) {
    const sections = result.sections?.length ?? 0;
    const texts = result.texts?.length ?? 0;
    const richTextNodes = result.texts?.filter((t) => t.styledRuns?.length).length ?? 0;
    const fonts = result.fonts?.join(', ') || '(none)';
    const warnings = result.warnings?.length ?? 0;
    console.log(JSON.stringify({
      ok: true,
      outputPath,
      viewport: result.viewport,
      sections,
      texts,
      richTextNodes,
      fonts,
      warnings,
      topColors: result.colors?.slice(0, 6).map((c) => c.hex),
    }, null, 2));
  } else {
    console.error(JSON.stringify(result, null, 2));
    process.exit(1);
  }
}

main();
