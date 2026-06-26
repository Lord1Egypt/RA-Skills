'use strict';

const fs = require('fs');

const SCALAR_TEXT_STYLE_FIELDS = ['fontFamily', 'fontWeight', 'fontStyle', 'fontSize', 'lineHeightPx', 'letterSpacing'];

function rgbToHex(r, g, b) {
  return '#' + [r, g, b].map((c) => Math.round(c * 255).toString(16).padStart(2, '0')).join('');
}

function paintToHex(paint) {
  if (!paint || paint.type !== 'SOLID' || !paint.color) return null;
  if (paint.visible === false) return null;
  const { r, g, b } = paint.color;
  const alpha = paint.opacity ?? paint.color.a ?? 1;
  const hex = rgbToHex(r, g, b);
  return alpha < 0.99 ? { hex, opacity: +alpha.toFixed(3) } : hex;
}

function primaryFill(fills) {
  if (!Array.isArray(fills)) return null;
  for (const paint of fills) {
    const hexColor = paintToHex(paint);
    if (hexColor) return hexColor;
  }
  return null;
}

function primaryStroke(node) {
  if (!Array.isArray(node.strokes) || !node.strokes.length) return null;
  const hexColor = paintToHex(node.strokes[0]);
  if (!hexColor) return null;
  const stroke = {
    color: hexColor,
    weight: node.strokeWeight ?? 1,
    align: node.strokeAlign ?? 'INSIDE',
  };
  if (node.individualStrokeWeights) stroke.individualStrokeWeights = node.individualStrokeWeights;
  if (Array.isArray(node.strokeDashes) && node.strokeDashes.length) stroke.dashPattern = node.strokeDashes.slice();
  return stroke;
}

function layoutOf(node) {
  if (!node.layoutMode) return null;
  return {
    mode: node.layoutMode,
    paddingTop: node.paddingTop ?? 0,
    paddingRight: node.paddingRight ?? 0,
    paddingBottom: node.paddingBottom ?? 0,
    paddingLeft: node.paddingLeft ?? 0,
    itemSpacing: node.itemSpacing ?? 0,
    counterAxisSpacing: node.counterAxisSpacing ?? null,
    primaryAxisAlignItems: node.primaryAxisAlignItems ?? null,
    counterAxisAlignItems: node.counterAxisAlignItems ?? null,
  };
}

function textStyleOf(node) {
  const s = node.style;
  if (!s) return null;
  return {
    fontFamily: s.fontFamily ?? null,
    fontSize: s.fontSize ?? null,
    fontWeight: s.fontWeight ?? null,
    fontStyle: s.fontStyle ?? null,
    lineHeightPx: s.lineHeightPx ?? null,
    lineHeightUnit: s.lineHeightUnit ?? null,
    letterSpacing: s.letterSpacing ?? 0,
    textAlignH: s.textAlignHorizontal ?? null,
    textAlignV: s.textAlignVertical ?? null,
    color: primaryFill(node.fills),
  };
}

function mergeTextStyle(base, override) {
  const merged = { ...base };
  if (!override) return merged;
  for (const field of SCALAR_TEXT_STYLE_FIELDS) {
    if (override[field] != null) merged[field] = override[field];
  }
  const color = primaryFill(override.fills);
  if (color) merged.color = color;
  return merged;
}

function getOverrideEntry(overrideTable, id) {
  return id ? (overrideTable[String(id)] || {}) : {};
}

function extractStyledRuns(chars, charOverrides, overrideTable, baseStyle) {
  if (!charOverrides?.length || !overrideTable) return null;
  if (new Set(charOverrides).size <= 1) return null;

  const runs = [];
  let start = 0;
  let currentId = charOverrides[0];

  for (let i = 1; i <= charOverrides.length; i++) {
    const nextId = charOverrides[i] ?? null;
    if (nextId !== currentId) {
      runs.push({
        start,
        end: i,
        characters: chars.slice(start, i),
        style: mergeTextStyle(baseStyle, getOverrideEntry(overrideTable, currentId)),
      });
      start = i;
      currentId = nextId;
    }
  }

  return runs.length > 1 ? runs : null;
}

function boundsOf(node, offsetX, offsetY) {
  const bb = node.absoluteBoundingBox || node.absoluteRenderBounds;
  if (!bb) return null;
  return {
    x: Math.round(bb.x - offsetX),
    y: Math.round(bb.y - offsetY),
    width: Math.round(bb.width),
    height: Math.round(bb.height),
  };
}

function effectsOf(node) {
  if (!Array.isArray(node.effects) || !node.effects.length) return null;
  return node.effects
    .filter((effect) => effect.visible !== false)
    .map((effect) => ({
      type: effect.type,
      radius: effect.radius ?? null,
      color: effect.color ? paintToHex({ type: 'SOLID', color: effect.color, opacity: effect.color.a }) : null,
      offset: effect.offset ?? null,
    }));
}

function buildNode(node, offsetX, offsetY, depth, maxDepth, ctx) {
  const bounds = boundsOf(node, offsetX, offsetY);
  if (!bounds) return null;

  const fill = primaryFill(node.fills);
  const stroke = primaryStroke(node);
  const layout = layoutOf(node);
  const effects = effectsOf(node);

  if (typeof fill === 'string') ctx.colorSet.add(fill);
  else if (fill?.hex) ctx.colorSet.add(fill.hex);

  const out = {
    id: node.id,
    name: node.name,
    type: node.type,
    visible: node.visible !== false,
    bounds,
  };

  if (fill) out.fill = fill;
  if (stroke) out.stroke = stroke;
  if (layout) out.layout = layout;
  if (effects?.length) out.effects = effects;

  if (node.cornerRadius != null) out.cornerRadius = node.cornerRadius;
  if (node.rectangleCornerRadii != null) out.cornerRadii = node.rectangleCornerRadii;
  if (node.opacity != null && node.opacity < 1) out.opacity = +node.opacity.toFixed(3);

  if (node.type === 'TEXT') {
    const style = textStyleOf(node);
    const chars = node.characters ?? '';
    out.characters = chars;
    out.style = style;
    if (style?.fontFamily) ctx.fontSet.add(style.fontFamily);
    if (style?.color && typeof style.color === 'string') ctx.colorSet.add(style.color);

    const styledRuns = extractStyledRuns(chars, node.characterStyleOverrides, node.styleOverrideTable, style);
    if (styledRuns) {
      out.styledRuns = styledRuns;
      ctx.warnList.push(`Node "${node.name}" (${node.id}) has inline style overrides — use styledRuns[] to render mixed bold/italic/colour spans`);
    }

    const textEntry = { id: node.id, name: node.name, characters: chars, bounds, style };
    if (styledRuns) textEntry.styledRuns = styledRuns;
    ctx.textList.push(textEntry);
    return out;
  }

  if (Array.isArray(node.fills)) {
    for (const paint of node.fills) {
      if (paint.visible === false && paint.type === 'SOLID') {
        ctx.warnList.push(`Node "${node.name}" (${node.id}) has an invisible fill — skip rendering it`);
      }
      if (paint.type === 'IMAGE' && paint.visible !== false) {
        out.imageRef = paint.imageRef ?? null;
      }
    }
  }

  if (depth < maxDepth && Array.isArray(node.children)) {
    const children = [];
    for (const child of node.children) {
      if (child.visible === false) {
        ctx.warnList.push(`Node "${child.name}" (${child.id}) has visible=false — do not render`);
        continue;
      }
      const childNode = buildNode(child, offsetX, offsetY, depth + 1, maxDepth, ctx);
      if (childNode) children.push(childNode);
    }
    if (children.length) out.children = children;
  }

  return out;
}

function resolveRootEntry(figmaNodeJson, rootNodeId) {
  const resolvedId = rootNodeId || Object.keys(figmaNodeJson?.nodes || {})[0];
  const rootDoc = figmaNodeJson?.nodes?.[resolvedId]?.document;
  if (!rootDoc) return { error: `Node ${resolvedId} not found` };
  const rootBB = rootDoc.absoluteBoundingBox || rootDoc.absoluteRenderBounds;
  if (!rootBB) return { error: 'Root node has no bounding box' };
  return { resolvedId, rootDoc, rootBB };
}

function collectSections(rootDoc, offsetX, offsetY, maxDepth, ctx) {
  const sections = [];
  for (const child of (rootDoc.children || [])) {
    if (child.visible === false) {
      ctx.warnList.push(`Section "${child.name}" (${child.id}) has visible=false — skip`);
      continue;
    }
    const node = buildNode(child, offsetX, offsetY, 0, maxDepth, ctx);
    if (node) sections.push(node);
  }
  return sections;
}

function sortedColorsByFrequency(colorSet) {
  const freq = new Map();
  for (const hex of colorSet) freq.set(hex, (freq.get(hex) || 0) + 1);
  return [...freq.entries()]
    .sort(([, a], [, b]) => b - a)
    .map(([hex, count]) => ({ hex, count }));
}

function extractImplementationData(figmaNodeJson, rootNodeId, maxDepth = 6) {
  const entry = resolveRootEntry(figmaNodeJson, rootNodeId);
  if (entry.error) return { ok: false, error: entry.error };

  const { resolvedId, rootDoc, rootBB } = entry;
  const viewport = { width: Math.round(rootBB.width), height: Math.round(rootBB.height) };
  const ctx = { fontSet: new Set(), colorSet: new Set(), textList: [], warnList: [] };
  const sections = collectSections(rootDoc, rootBB.x, rootBB.y, maxDepth, ctx);

  return {
    ok: true,
    rootNodeId: resolvedId,
    viewport,
    sections,
    texts: ctx.textList,
    fonts: [...ctx.fontSet].sort(),
    colors: sortedColorsByFrequency(ctx.colorSet),
    warnings: ctx.warnList,
  };
}

function extractFromFile(figmaNodePath, rootNodeId, maxDepth = 6) {
  let json;
  try {
    json = JSON.parse(fs.readFileSync(figmaNodePath, 'utf8'));
  } catch {
    throw new Error(`figma-node.json not found: ${figmaNodePath}`);
  }
  const id = rootNodeId || Object.keys(json?.nodes || {})[0];
  if (!id) throw new Error('No node ID found in figma-node.json');
  return extractImplementationData(json, id, maxDepth);
}

module.exports = { extractFromFile };
