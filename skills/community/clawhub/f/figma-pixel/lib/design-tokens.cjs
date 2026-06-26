const fs = require('fs');

function rgbaToHex({ r: red, g: green, b: blue }) {
  return '#' + [red, green, blue]
    .map((channel) => Math.round(channel * 255).toString(16).padStart(2, '0'))
    .join('');
}

function paintToColor(paint) {
  if (!paint || paint.type !== 'SOLID' || !paint.color) return null;
  return {
    hex: rgbaToHex(paint.color),
    opacity: +(paint.opacity ?? paint.color.a ?? 1).toFixed(3),
  };
}

function traverseNodes(node, callback) {
  if (node.visible === false) return;
  callback(node);
  if (Array.isArray(node.children)) {
    for (const child of node.children) traverseNodes(child, callback);
  }
}

function collectFills(node, name, fills, colorIndex) {
  if (!Array.isArray(node.fills)) return;
  for (const paint of node.fills) {
    const color = paintToColor(paint);
    if (!color) continue;
    const key = `${color.hex}|${color.opacity}`;
    let entry = colorIndex.get(key);
    if (!entry) {
      entry = { hex: color.hex, opacity: color.opacity, usedBy: [] };
      colorIndex.set(key, entry);
      fills.push(entry);
    }
    if (!entry.usedBy.includes(name)) entry.usedBy.push(name);
  }
}

function collectTypography(node, name, id, typography) {
  if (node.type !== 'TEXT' || !node.style) return;
  const nodeStyle = node.style;
  const textColor = Array.isArray(node.fills) && node.fills[0]
    ? paintToColor(node.fills[0])
    : null;
  typography.push({
    nodeName: name,
    nodeId: id,
    fontFamily: nodeStyle.fontFamily || null,
    fontSize: nodeStyle.fontSize || null,
    fontWeight: nodeStyle.fontWeight || null,
    lineHeightPx: nodeStyle.lineHeightPx || null,
    lineHeightPercent: nodeStyle.lineHeightPercent || null,
    letterSpacing: nodeStyle.letterSpacing || null,
    textAlignHorizontal: nodeStyle.textAlignHorizontal || null,
    textTransform: nodeStyle.textCase || null,
    color: textColor?.hex || null,
  });
}

function collectSpacing(node, name, id, spacing) {
  if (!node.layoutMode) return;
  if (node.paddingLeft == null && node.paddingTop == null && node.itemSpacing == null) return;
  spacing.push({
    nodeName: name,
    nodeId: id,
    layoutMode: node.layoutMode,
    paddingLeft: node.paddingLeft ?? 0,
    paddingRight: node.paddingRight ?? 0,
    paddingTop: node.paddingTop ?? 0,
    paddingBottom: node.paddingBottom ?? 0,
    itemSpacing: node.itemSpacing ?? 0,
    counterAxisSpacing: node.counterAxisSpacing ?? null,
  });
}

function collectCornerRadius(node, name, id, cornerRadius) {
  if (node.cornerRadius == null && node.rectangleCornerRadii == null) return;
  cornerRadius.push({
    nodeName: name,
    nodeId: id,
    cornerRadius: node.cornerRadius ?? null,
    rectangleCornerRadii: node.rectangleCornerRadii ?? null,
  });
}

function collectStrokes(node, name, id, strokes) {
  if (!Array.isArray(node.strokes) || !node.strokes.length || !node.strokeWeight) return;
  for (const paint of node.strokes) {
    const color = paintToColor(paint);
    if (!color) continue;
    strokes.push({
      nodeName: name,
      nodeId: id,
      strokeWeight: node.strokeWeight,
      hex: color.hex,
      opacity: color.opacity,
      strokeAlign: node.strokeAlign || null,
    });
  }
}

function extractDesignTokens(figmaNodeJson, nodeId) {
  const rootEntry = figmaNodeJson?.nodes?.[nodeId];
  const rootDoc = rootEntry?.document;
  if (!rootDoc) return null;

  const rootBounds = rootDoc.absoluteBoundingBox || rootDoc.absoluteRenderBounds || null;

  const fills = [];
  const typography = [];
  const spacing = [];
  const cornerRadius = [];
  const strokes = [];
  const colorIndex = new Map();

  traverseNodes(rootDoc, (node) => {
    const name = node.name || '';
    const id = node.id || '';
    collectFills(node, name, fills, colorIndex);
    collectTypography(node, name, id, typography);
    collectSpacing(node, name, id, spacing);
    collectCornerRadius(node, name, id, cornerRadius);
    collectStrokes(node, name, id, strokes);
  });

  const frame = rootBounds
      ? { width: Math.round(rootBounds.width), height: Math.round(rootBounds.height) }
      : null

  return {
    frame,
    fills,
    typography,
    spacing,
    cornerRadius,
    strokes,
  };
}

function extractDesignTokensFromFile(figmaNodePath, nodeId) {
  let figmaNodeJson;
  try {
    figmaNodeJson = JSON.parse(fs.readFileSync(figmaNodePath, 'utf8'));
  } catch {
    throw new Error(`figma-node.json not found: ${figmaNodePath}`);
  }
  const resolvedNodeId = nodeId || Object.keys(figmaNodeJson?.nodes || {})[0];
  if (!resolvedNodeId) throw new Error('No node ID found in figma-node.json');
  const tokens = extractDesignTokens(figmaNodeJson, resolvedNodeId);
  if (!tokens) throw new Error(`Node ${resolvedNodeId} not found in figma-node.json`);
  return tokens;
}

module.exports = { extractDesignTokensFromFile };
