#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { readStdin, parseArgs, escapeXml } from './utils.mjs';

/**
 * Build SVG for detection bounding boxes and labels (green).
 */
export function buildDetectionSvg(detections, width, height) {
  const rects = [];
  const fontSize = 14;
  const padding = 4;
  const labelHeight = fontSize + padding * 2;

  for (const det of detections) {
    const [x, y, w, h] = det.bbox;
    // Bounding box rectangle
    rects.push(
      `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="none" stroke="rgba(0,255,0,0.8)" stroke-width="2"/>`
    );

    // Label text
    const parts = [];
    if (det.track_id != null) parts.push(`#${det.track_id}`);
    if (det.category && det.category.name) parts.push(det.category.name);
    if (det.confidence != null) parts.push((det.confidence * 100).toFixed(0) + '%');
    const label = parts.join(' ');

    if (label) {
      const labelWidth = label.length * (fontSize * 0.65) + padding * 2;
      const labelY = Math.max(y - labelHeight, 0);
      // Label background
      rects.push(
        `<rect x="${x}" y="${labelY}" width="${labelWidth}" height="${labelHeight}" fill="rgba(0,255,0,0.7)" rx="2"/>`
      );
      // Label text
      rects.push(
        `<text x="${x + padding}" y="${labelY + fontSize + padding - 2}" font-family="sans-serif" font-size="${fontSize}" fill="white">${escapeXml(label)}</text>`
      );
    }
  }

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}">${rects.join('')}</svg>`;
}

/**
 * Helper function to draw an arrow at a specific point.
 * @param {Array} elements - Array to push SVG elements to
 * @param {Object} point - {x, y} coordinates
 * @param {number} dirX - Unit direction vector X component
 * @param {number} dirY - Unit direction vector Y component
 * @param {number} arrowSize - Size of the arrow
 * @param {string} color - Arrow color (rgba string)
 */
function drawArrowAtPoint(elements, point, dirX, dirY, arrowSize, color) {
  const tipX = point.x + dirX * arrowSize;
  const tipY = point.y + dirY * arrowSize;

  // Perpendicular base vectors
  const perpX = -dirY * arrowSize * 0.6;
  const perpY = dirX * arrowSize * 0.6;

  const b1x = point.x - dirX * arrowSize - perpX;
  const b1y = point.y - dirY * arrowSize - perpY;
  const b2x = point.x - dirX * arrowSize + perpX;
  const b2y = point.y - dirY * arrowSize + perpY;

  elements.push(
    `<polygon points="${tipX},${tipY} ${b1x},${b1y} ${b2x},${b2y}" fill="${color}"/>`
  );
}

/**
 * Build SVG for ROI polygons and Tripwire polylines (input overlays).
 *
 * Each overlay item:
 *   { kind: "ROI", points: [x1,y1,x2,y2,...], name?: string }
 *   { kind: "TripWire", points: [x1,y1,x2,y2,...], name?: string, direction?: string }
 *
 * Each crossing item (optional):
 *   { tripwireId?: string, prevPos: [x,y], currPos: [x,y], dotProduct: number }
 */
export function buildOverlaysSvg(overlays, width, height, crossings = []) {
  const elements = [];
  const fontSize = 13;
  const padding = 4;
  const labelHeight = fontSize + padding * 2;

  for (const overlay of overlays) {
    const pts = overlay.points || [];
    // Convert flat [x1,y1,x2,y2,...] to "x1,y1 x2,y2 ..."
    const pointPairs = [];
    for (let i = 0; i < pts.length - 1; i += 2) {
      pointPairs.push(`${pts[i]},${pts[i + 1]}`);
    }
    const pointsStr = pointPairs.join(' ');

    if (overlay.kind === 'ROI') {
      // ROI: blue polygon with semi-transparent fill
      elements.push(
        `<polygon points="${pointsStr}" fill="rgba(0,150,255,0.15)" stroke="rgba(0,150,255,0.6)" stroke-width="2"/>`
      );

      // Label at first vertex
      const name = overlay.name || overlay.displayName || '';
      if (name && pts.length >= 2) {
        const lx = pts[0];
        const ly = Math.max(pts[1] - labelHeight, 0);
        const labelWidth = name.length * (fontSize * 0.65) + padding * 2;
        elements.push(
          `<rect x="${lx}" y="${ly}" width="${labelWidth}" height="${labelHeight}" fill="rgba(0,150,255,0.8)" rx="2"/>`
        );
        elements.push(
          `<text x="${lx + padding}" y="${ly + fontSize + padding - 2}" font-family="sans-serif" font-size="${fontSize}" fill="white">${escapeXml(name)}</text>`
        );
      }
    } else if (overlay.kind === 'TripWire') {
      // TripWire with 4-point structure support
      // points = [x1,y1, x2,y2, x3,y3, x4,y4]
      // p1-p2: main tripwire
      // p3-p4: A-B detection line with directional arrows
      // If only 2-point format provided, auto-generate perpendicular p3-p4

      let p1, p2, p3, p4;

      if (pts.length >= 8) {
        // 4-point structure (explicit format)
        p1 = {x: pts[0], y: pts[1]};
        p2 = {x: pts[2], y: pts[3]};
        p3 = {x: pts[4], y: pts[5]};
        p4 = {x: pts[6], y: pts[7]};
      } else if (pts.length >= 4) {
        // 2-point format: auto-generate perpendicular A-B points
        p1 = {x: pts[0], y: pts[1]};
        p2 = {x: pts[2], y: pts[3]};

        // Calculate perpendicular distance for A-B points
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        const len = Math.sqrt(dx * dx + dy * dy) || 1;
        // Unit perpendicular vector (rotated 90 degrees counter-clockwise)
        const perpX = -dy / len;
        const perpY = dx / len;
        // Distance from the main line to A-B points
        const perpDist = 30;
        // Generate A-B points perpendicular to the main tripwire
        p3 = {
          x: p1.x + perpX * perpDist,
          y: p1.y + perpY * perpDist
        };
        p4 = {
          x: p2.x + perpX * perpDist,
          y: p2.y + perpY * perpDist
        };
      } else {
        // Not enough points, skip rendering
        p1 = p2 = p3 = p4 = null;
      }

      if (p1 && p2 && p3 && p4) {

        // Draw main tripwire line (p1-p2) - dashed, no arrow
        elements.push(
          `<line x1="${p1.x}" y1="${p1.y}" x2="${p2.x}" y2="${p2.y}" stroke="rgba(255,165,0,0.8)" stroke-width="2" stroke-dasharray="8,4"/>`
        );

        // Draw A-B detection line (p3-p4) - dashed with direction arrow
        elements.push(
          `<line x1="${p3.x}" y1="${p3.y}" x2="${p4.x}" y2="${p4.y}" stroke="rgba(255,165,0,0.8)" stroke-width="2" stroke-dasharray="8,4"/>`
        );

        // Calculate direction vector (p3 -> p4)
        const dx = p4.x - p3.x;
        const dy = p4.y - p3.y;
        const len = Math.sqrt(dx * dx + dy * dy) || 1;
        const unitX = dx / len;
        const unitY = dy / len;

        const dir = overlay.direction || 'TwoWay';
        const arrowSize = 12;

        // Draw directional arrows
        if (dir === 'Forward') {
          // Arrow at p4, pointing toward p4 (green)
          drawArrowAtPoint(elements, p4, unitX, unitY, arrowSize, 'rgba(76,175,80,0.8)');
        } else if (dir === 'Backward') {
          // Arrow at p3, pointing toward p3 (red)
          drawArrowAtPoint(elements, p3, -unitX, -unitY, arrowSize, 'rgba(244,67,54,0.8)');
        } else if (dir === 'TwoWay') {
          // Arrows at both p3 and p4 (blue)
          drawArrowAtPoint(elements, p3, -unitX, -unitY, arrowSize, 'rgba(33,150,243,0.8)');
          drawArrowAtPoint(elements, p4, unitX, unitY, arrowSize, 'rgba(33,150,243,0.8)');
        }

        // Add region labels 'A' and 'B'
        const labelFontSize = 12;
        const labelOffset = 8;
        // Label 'A' near p3
        elements.push(
          `<text x="${p3.x - labelOffset}" y="${p3.y - labelOffset}" font-family="sans-serif" font-size="${labelFontSize}" fill="rgba(255,165,0,0.8)" font-weight="bold">A</text>`
        );
        // Label 'B' near p4
        elements.push(
          `<text x="${p4.x + labelOffset}" y="${p4.y - labelOffset}" font-family="sans-serif" font-size="${labelFontSize}" fill="rgba(255,165,0,0.8)" font-weight="bold">B</text>`
        );
      }

      // Label at first vertex (applies to both formats)
      const name = overlay.name || overlay.displayName || '';
      if (name && pts.length >= 2) {
        const lx = pts[0];
        const ly = Math.max(pts[1] - labelHeight, 0);
        const labelWidth = name.length * (fontSize * 0.65) + padding * 2;
        elements.push(
          `<rect x="${lx}" y="${ly}" width="${labelWidth}" height="${labelHeight}" fill="rgba(255,165,0,0.8)" rx="2"/>`
        );
        elements.push(
          `<text x="${lx + padding}" y="${ly + fontSize + padding - 2}" font-family="sans-serif" font-size="${fontSize}" fill="white">${escapeXml(name)}</text>`
        );
      }
    }
  }

  // Draw crossing vectors perpendicular to tripwire
  for (const crossing of crossings) {
    const { tripwireId, prevPos, currPos, dotProduct, direction } = crossing;
    if (!prevPos || !currPos) continue;

    const [prevX, prevY] = prevPos;
    const [currX, currY] = currPos;

    // Crossing point is midpoint between previous and current position
    const crossX = (prevX + currX) / 2;
    const crossY = (prevY + currY) / 2;

    // Determine color based on crossing type
    let arrowColor, dotColor;
    if (direction === 'Forward') {
      // Forward crossing (dot > 0): green
      arrowColor = 'rgba(76,175,80,0.8)';
      dotColor = '#4caf50';
    } else if (direction === 'Backward') {
      // Backward crossing (dot < 0): red
      arrowColor = 'rgba(244,67,54,0.8)';
      dotColor = '#f44336';
    } else {
      // TwoWay crossing: blue
      arrowColor = 'rgba(33,150,243,0.8)';
      dotColor = '#2196f3';
    }

    // Find the associated tripwire to get its direction
    let tripwirePerpX = 1;   // default perpendicular
    let tripwirePerpY = 0;
    for (const overlay of overlays) {
      if (overlay.kind === 'TripWire' && overlay.name === tripwireId) {
        // Get tripwire direction vector
        const pts = Array.isArray(overlay.points[0]) ? overlay.points.flat() : overlay.points;
        if (pts.length >= 4) {
          const midIdx = Math.floor(pts.length / 4);
          const x1 = pts[midIdx * 2];
          const y1 = pts[midIdx * 2 + 1];
          const x2 = pts[(midIdx + 1) * 2];
          const y2 = pts[(midIdx + 1) * 2 + 1];
          const dx = x2 - x1;
          const dy = y2 - y1;
          const len = Math.sqrt(dx * dx + dy * dy) || 1;
          // Perpendicular vector (rotated 90 degrees)
          tripwirePerpX = -dy / len;
          tripwirePerpY = dx / len;
        }
        break;
      }
    }

    const arrowSize = 12;

    if (direction === 'TwoWay') {
      // TwoWay: draw arrows in both directions perpendicular to tripwire

      // Forward arrow
      const fx1 = crossX + tripwirePerpX * arrowSize;
      const fy1 = crossY + tripwirePerpY * arrowSize;
      elements.push(
        `<line x1="${crossX}" y1="${crossY}" x2="${fx1}" y2="${fy1}" stroke="${arrowColor}" stroke-width="2.5" opacity="0.8"/>`
      );
      const perp2X = tripwirePerpY * arrowSize * 0.6;
      const perp2Y = -tripwirePerpX * arrowSize * 0.6;
      elements.push(
        `<polygon points="${fx1},${fy1} ${fx1 - tripwirePerpX * arrowSize - perp2X},${fy1 - tripwirePerpY * arrowSize - perp2Y} ${fx1 - tripwirePerpX * arrowSize + perp2X},${fy1 - tripwirePerpY * arrowSize + perp2Y}" fill="${arrowColor}"/>`
      );

      // Backward arrow
      const bx1 = crossX - tripwirePerpX * arrowSize;
      const by1 = crossY - tripwirePerpY * arrowSize;
      elements.push(
        `<line x1="${crossX}" y1="${crossY}" x2="${bx1}" y2="${by1}" stroke="${arrowColor}" stroke-width="2.5" opacity="0.8"/>`
      );
      elements.push(
        `<polygon points="${bx1},${by1} ${bx1 + tripwirePerpX * arrowSize - perp2X},${by1 + tripwirePerpY * arrowSize - perp2Y} ${bx1 + tripwirePerpX * arrowSize + perp2X},${by1 + tripwirePerpY * arrowSize + perp2Y}" fill="${arrowColor}"/>`
      );

      // Center circle
      elements.push(
        `<circle cx="${crossX}" cy="${crossY}" r="4" fill="${dotColor}" stroke="white" stroke-width="1.5"/>`
      );

      // Label
      elements.push(
        `<text x="${crossX + 10}" y="${crossY - 5}" font-size="11" fill="${dotColor}" font-weight="bold">⟷ TwoWay</text>`
      );
    } else {
      // Forward or Backward: single arrow perpendicular to tripwire
      const sign = direction === 'Forward' ? 1 : -1;
      const arrowX = crossX + tripwirePerpX * arrowSize * sign;
      const arrowY = crossY + tripwirePerpY * arrowSize * sign;

      // Arrow shaft
      elements.push(
        `<line x1="${crossX}" y1="${crossY}" x2="${arrowX}" y2="${arrowY}" stroke="${arrowColor}" stroke-width="2.5" opacity="0.8"/>`
      );

      // Arrow head
      const perpBaseX = tripwirePerpY * arrowSize * 0.6;
      const perpBaseY = -tripwirePerpX * arrowSize * 0.6;
      elements.push(
        `<polygon points="${arrowX},${arrowY} ${arrowX - tripwirePerpX * arrowSize * sign - perpBaseX},${arrowY - tripwirePerpY * arrowSize * sign - perpBaseY} ${arrowX - tripwirePerpX * arrowSize * sign + perpBaseX},${arrowY - tripwirePerpY * arrowSize * sign + perpBaseY}" fill="${arrowColor}"/>`
      );

      // Center circle
      elements.push(
        `<circle cx="${crossX}" cy="${crossY}" r="4" fill="${dotColor}" stroke="white" stroke-width="1.5"/>`
      );

      // Label
      const dirLabel = direction === 'Forward' ? '✓ Forward' : '✗ Backward';
      elements.push(
        `<text x="${crossX + 10}" y="${crossY - 5}" font-size="11" fill="${dotColor}" font-weight="bold">${dirLabel}</text>`
      );
    }
  }

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}">${elements.join('')}</svg>`;
}

/**
 * Build SVG for text lines displayed in a footer area.
 * Returns { svg: string, height: number }.
 *
 * The SVG is positioned to sit at the bottom of the extended canvas,
 * starting at y=imageHeight.
 */
export function buildTextFooterSvg(textLines, width, imageHeight) {
  const fontSize = 16;
  const lineHeight = fontSize + 8;
  const paddingTop = 10;
  const paddingBottom = 10;
  const paddingLeft = 12;
  const totalHeight = paddingTop + textLines.length * lineHeight + paddingBottom;

  const elements = [];
  // Dark background
  elements.push(
    `<rect x="0" y="${imageHeight}" width="${width}" height="${totalHeight}" fill="rgba(0,0,0,0.75)"/>`
  );

  // Text lines
  for (let i = 0; i < textLines.length; i++) {
    const ty = imageHeight + paddingTop + (i + 1) * lineHeight - 4;
    elements.push(
      `<text x="${paddingLeft}" y="${ty}" font-family="sans-serif" font-size="${fontSize}" fill="white">${escapeXml(textLines[i])}</text>`
    );
  }

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${imageHeight + totalHeight}">${elements.join('')}</svg>`;
  return { svg, height: totalHeight };
}

async function main() {
  let sharp;
  try {
    sharp = (await import('sharp')).default;
  } catch {
    console.error('Error: "sharp" package is required for visualization but not installed.');
    console.error('Install it with: npm install sharp');
    process.exit(1);
  }

  const { positional, flags } = parseArgs(process.argv.slice(2));

  const inputImage = positional[0];
  let detectionsArg = positional[1];
  let outputPath = positional[2];

  if (!inputImage || !detectionsArg) {
    console.error('Usage: node visualize.mjs <input-image> <detections-json | -> [output-path] [--overlays \'<json>\'] [--text \'<json>\'] [--crossings \'<json>\']');
    console.error('');
    console.error('  <detections-json>  JSON array of detections (parsedValue format), or "-" to read from stdin');
    console.error('  [output-path]      Optional output path. Default: <input>_detection.<ext>');
    console.error('  --overlays         JSON array of ROI/Tripwire overlay objects');
    console.error('  --text             JSON array of text lines to display as footer');
    console.error('  --crossings        JSON array of tripwire crossing events with motion vectors');
    process.exit(1);
  }

  // Resolve input image
  const resolvedInput = path.resolve(inputImage);
  if (!fs.existsSync(resolvedInput)) {
    console.error(`Input image not found: ${resolvedInput}`);
    process.exit(1);
  }

  // Read detections JSON
  let detectionsJson;
  if (detectionsArg === '-') {
    detectionsJson = await readStdin();
  } else {
    detectionsJson = detectionsArg;
  }

  let detections;
  try {
    detections = JSON.parse(detectionsJson);
  } catch (err) {
    console.error(`Failed to parse detections JSON: ${err.message}`);
    process.exit(1);
  }

  if (!Array.isArray(detections)) {
    console.error('Detections must be a JSON array');
    process.exit(1);
  }

  // Parse --overlays
  let overlays = [];
  if (flags.overlays) {
    try {
      overlays = JSON.parse(flags.overlays);
      if (!Array.isArray(overlays)) {
        console.error('--overlays must be a JSON array');
        process.exit(1);
      }
    } catch (err) {
      console.error(`Failed to parse --overlays JSON: ${err.message}`);
      process.exit(1);
    }
  }

  // Parse --text
  let textLines = [];
  if (flags.text) {
    try {
      textLines = JSON.parse(flags.text);
      if (!Array.isArray(textLines)) {
        console.error('--text must be a JSON array');
        process.exit(1);
      }
    } catch (err) {
      console.error(`Failed to parse --text JSON: ${err.message}`);
      process.exit(1);
    }
  }

  // Parse --crossings
  let crossings = [];
  if (flags.crossings) {
    try {
      crossings = JSON.parse(flags.crossings);
      if (!Array.isArray(crossings)) {
        console.error('--crossings must be a JSON array');
        process.exit(1);
      }
    } catch (err) {
      console.error(`Failed to parse --crossings JSON: ${err.message}`);
      process.exit(1);
    }
  }

  // Validate: must have something to draw
  if (detections.length === 0 && overlays.length === 0 && textLines.length === 0) {
    console.error('Nothing to draw: detections, overlays, and text are all empty');
    process.exit(1);
  }

  // Default output path
  if (!outputPath) {
    const ext = path.extname(inputImage);
    const base = path.basename(inputImage, ext);
    const dir = path.dirname(resolvedInput);
    outputPath = path.join(dir, `${base}_detection${ext}`);
  } else {
    outputPath = path.resolve(outputPath);
  }

  // Read image metadata
  const image = sharp(resolvedInput);
  const metadata = await image.metadata();
  const { width, height } = metadata;

  // Build composite layers
  const composites = [];

  // Layer 1: input overlays (ROI/Tripwire) — drawn first (bottom layer)
  if (overlays.length > 0) {
    const overlaySvg = buildOverlaysSvg(overlays, width, height, crossings);
    composites.push({ input: Buffer.from(overlaySvg), top: 0, left: 0 });
  }

  // Layer 2: detection bboxes — drawn on top of overlays
  if (detections.length > 0) {
    const detSvg = buildDetectionSvg(detections, width, height);
    composites.push({ input: Buffer.from(detSvg), top: 0, left: 0 });
  }

  // Layer 3: text footer — extend canvas and draw at bottom
  let pipeline = image;
  if (textLines.length > 0) {
    const { svg: textSvg, height: textHeight } = buildTextFooterSvg(textLines, width, height);
    pipeline = pipeline.extend({
      bottom: textHeight,
      background: { r: 0, g: 0, b: 0, alpha: 1 },
    });
    composites.push({ input: Buffer.from(textSvg), top: 0, left: 0 });
  }

  // Composite and save
  await pipeline
    .composite(composites)
    .toFile(outputPath);

  console.log(outputPath);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}
