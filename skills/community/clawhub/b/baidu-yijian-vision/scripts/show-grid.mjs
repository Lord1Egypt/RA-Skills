#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { parseArgs, escapeXml } from './utils.mjs';

/**
 * Compute adaptive grid dimensions so that cells are approximately square.
 *
 * @param {number} imageWidth
 * @param {number} imageHeight
 * @returns {{ cols: number, rows: number }}
 */
export function computeGridSize(imageWidth, imageHeight) {
  // Target ~30-42 intersection points with roughly square cells.
  // We pick the short side = 4 segments and scale the long side proportionally.
  const minSegments = 4;
  const ratio = imageWidth / imageHeight;

  let cols, rows;
  if (ratio >= 1) {
    // Landscape or square
    rows = minSegments;
    cols = Math.round(rows * ratio);
    // Clamp cols to a reasonable range
    cols = Math.max(minSegments, Math.min(cols, 12));
  } else {
    // Portrait
    cols = minSegments;
    rows = Math.round(cols / ratio);
    rows = Math.max(minSegments, Math.min(rows, 12));
  }

  return { cols, rows };
}

/**
 * Generate column labels: A, B, C, ..., Z, AA, AB, ...
 */
export function generateColLabels(count) {
  const labels = [];
  for (let i = 0; i < count; i++) {
    let label = '';
    let n = i;
    do {
      label = String.fromCharCode(65 + (n % 26)) + label;
      n = Math.floor(n / 26) - 1;
    } while (n >= 0);
    labels.push(label);
  }
  return labels;
}

/**
 * Generate row labels: 0, 1, 2, ...
 */
export function generateRowLabels(count) {
  return Array.from({ length: count }, (_, i) => String(i));
}

/**
 * Build an SVG overlay with grid lines, intersection dots, and labels.
 *
 * The SVG covers the full extended canvas (margin + image).
 *
 * @param {object} params
 * @param {number} params.imageWidth
 * @param {number} params.imageHeight
 * @param {number} params.cols - number of column segments (cols+1 vertical lines)
 * @param {number} params.rows - number of row segments (rows+1 horizontal lines)
 * @param {number} params.marginTop
 * @param {number} params.marginLeft
 * @param {number} params.marginBottom
 * @param {number} params.marginRight
 * @returns {string} SVG string
 */
export function buildGridSvg({ imageWidth, imageHeight, cols, rows, marginTop, marginLeft, marginBottom, marginRight }) {
  const totalWidth = marginLeft + imageWidth + marginRight;
  const totalHeight = marginTop + imageHeight + marginBottom;
  const gridWidth = imageWidth / cols;
  const gridHeight = imageHeight / rows;

  const colLabels = generateColLabels(cols + 1);
  const rowLabels = generateRowLabels(rows + 1);

  const elements = [];
  const fontSize = 16;
  const dotR = 5;

  // Grid lines — vertical
  for (let c = 0; c <= cols; c++) {
    const x = marginLeft + c * gridWidth;
    elements.push(
      `<line x1="${x}" y1="${marginTop}" x2="${x}" y2="${totalHeight}" stroke="rgba(255,255,255,0.55)" stroke-width="2"/>`
    );
  }

  // Grid lines — horizontal
  for (let r = 0; r <= rows; r++) {
    const y = marginTop + r * gridHeight;
    elements.push(
      `<line x1="${marginLeft}" y1="${y}" x2="${totalWidth}" y2="${y}" stroke="rgba(255,255,255,0.55)" stroke-width="2"/>`
    );
  }

  // Intersection dots
  for (let c = 0; c <= cols; c++) {
    for (let r = 0; r <= rows; r++) {
      const cx = marginLeft + c * gridWidth;
      const cy = marginTop + r * gridHeight;
      elements.push(
        `<circle cx="${cx}" cy="${cy}" r="${dotR}" fill="white" stroke="rgba(0,0,0,0.7)" stroke-width="1.5"/>`
      );
    }
  }

  // Column labels — along the top margin
  for (let c = 0; c <= cols; c++) {
    const x = marginLeft + c * gridWidth;
    const textWidth = colLabels[c].length * fontSize * 0.65;
    const bgWidth = textWidth + 10;
    const bgX = x - bgWidth / 2;
    const bgY = 2;
    const bgH = fontSize + 10;
    elements.push(
      `<rect x="${bgX}" y="${bgY}" width="${bgWidth}" height="${bgH}" fill="rgba(0,0,0,0.75)" rx="3"/>`
    );
    elements.push(
      `<text x="${x}" y="${bgY + fontSize + 3}" font-family="sans-serif" font-size="${fontSize}" font-weight="bold" fill="white" text-anchor="middle">${escapeXml(colLabels[c])}</text>`
    );
  }

  // Row labels — along the left margin
  for (let r = 0; r <= rows; r++) {
    const y = marginTop + r * gridHeight;
    const label = rowLabels[r];
    const textWidth = label.length * fontSize * 0.65;
    const bgWidth = textWidth + 10;
    const bgH = fontSize + 10;
    const bgX = 2;
    const bgY = y - bgH / 2;
    elements.push(
      `<rect x="${bgX}" y="${bgY}" width="${bgWidth}" height="${bgH}" fill="rgba(0,0,0,0.75)" rx="3"/>`
    );
    elements.push(
      `<text x="${bgX + bgWidth / 2}" y="${bgY + fontSize + 3}" font-family="sans-serif" font-size="${fontSize}" font-weight="bold" fill="white" text-anchor="middle">${escapeXml(label)}</text>`
    );
  }

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${totalWidth}" height="${totalHeight}">${elements.join('')}</svg>`;
}

async function main() {
  let sharp;
  try {
    sharp = (await import('sharp')).default;
  } catch {
    console.error('Error: "sharp" package is required for grid generation but not installed.');
    console.error('Install it with: npm install sharp');
    process.exit(1);
  }

  const { positional, flags } = parseArgs(process.argv.slice(2));
  const inputImage = positional[0];
  let outputPath = positional[1];

  if (!inputImage) {
    console.error('Usage: node show-grid.mjs <input-image> [output-path] [--cols N] [--rows N]');
    console.error('');
    console.error('  Generates a grid reference image for specifying ROI/Tripwire coordinates.');
    console.error('  --cols   Number of column segments (default: auto based on aspect ratio)');
    console.error('  --rows   Number of row segments (default: auto based on aspect ratio)');
    process.exit(1);
  }

  const resolvedInput = path.resolve(inputImage);
  if (!fs.existsSync(resolvedInput)) {
    console.error(`Input image not found: ${resolvedInput}`);
    process.exit(1);
  }

  // Read image metadata
  const image = sharp(resolvedInput);
  const metadata = await image.metadata();
  const { width: imageWidth, height: imageHeight } = metadata;

  // Compute grid size
  let { cols, rows } = computeGridSize(imageWidth, imageHeight);
  if (flags.cols) cols = parseInt(flags.cols, 10);
  if (flags.rows) rows = parseInt(flags.rows, 10);

  if (cols < 1 || rows < 1 || isNaN(cols) || isNaN(rows)) {
    console.error('--cols and --rows must be positive integers');
    process.exit(1);
  }

  const marginTop = 32;
  const marginLeft = 32;
  const marginBottom = 18;
  const marginRight = 18;

  // Build SVG
  const svg = buildGridSvg({ imageWidth, imageHeight, cols, rows, marginTop, marginLeft, marginBottom, marginRight });

  // Default output path
  if (!outputPath) {
    const ext = path.extname(inputImage);
    const base = path.basename(inputImage, ext);
    const dir = path.dirname(resolvedInput);
    outputPath = path.join(dir, `${base}_grid${ext}`);
  } else {
    outputPath = path.resolve(outputPath);
  }

  // Extend canvas for margins, composite grid SVG
  await image
    .extend({
      top: marginTop,
      left: marginLeft,
      bottom: marginBottom,
      right: marginRight,
      background: { r: 30, g: 30, b: 30, alpha: 1 },
    })
    .composite([{ input: Buffer.from(svg), top: 0, left: 0 }])
    .toFile(outputPath);

  // Output metadata JSON for Agent consumption
  const gridWidth = imageWidth / cols;
  const gridHeight = imageHeight / rows;
  const colLabels = generateColLabels(cols + 1);
  const rowLabels = generateRowLabels(rows + 1);

  const result = {
    path: outputPath,
    cols,
    rows,
    colLabels,
    rowLabels,
    gridWidth: Math.round(gridWidth * 100) / 100,
    gridHeight: Math.round(gridHeight * 100) / 100,
    marginLeft,
    marginTop,
    imageWidth,
    imageHeight,
  };

  console.log(JSON.stringify(result));
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}
