const fs = require('fs');
const path = require('path');
const { parseFigmaUrl } = require('./parse-figma-url.cjs');
const { fetchFigmaApi } = require('./figma-api.cjs');
const { exportFigmaImage } = require('./figma-export.cjs');
const {
  writeJson,
  copyFileIfExists,
  readJsonIfExists,
  getSharedFigmaPaths,
  primeRunFigmaDirFromShared,
  persistRunFigmaDirToShared,
} = require('./figma-cache.cjs');

function getNodeDocument(figmaNodeJson, nodeId) {
  if (!figmaNodeJson?.nodes || !nodeId) return null;
  return figmaNodeJson.nodes[nodeId]?.document || null;
}

function deriveViewportFromFigma(figmaNodeJson, nodeId) {
  const node = getNodeDocument(figmaNodeJson, nodeId);
  const directBounds = node?.absoluteBoundingBox || node?.absoluteRenderBounds || null;
  const childBounds = (!directBounds && Array.isArray(node?.children) && node.children.length === 1)
    ? (node.children[0]?.absoluteBoundingBox || node.children[0]?.absoluteRenderBounds || null)
    : null;
  const bounds = directBounds || childBounds || null;
  const width = Math.round(bounds?.width || 0);
  const height = Math.round(bounds?.height || 0);

  if (width > 0 && height > 0) {
    return { width, height, source: childBounds ? 'figma-child-frame' : 'figma-node', fallbackUsed: false };
  }

  if (!figmaNodeJson) throw new Error('Cannot determine viewport from Figma: figma-node.json is missing — make sure the Figma URL includes a node-id');
  if (!node) throw new Error(`Cannot determine viewport from Figma: node "${nodeId}" not found in figma-node.json`);
  throw new Error('Cannot determine viewport from Figma: node has no absoluteBoundingBox / absoluteRenderBounds');
}

function resolveExportNodeId(figmaNodeJson, nodeId) {
  const node = getNodeDocument(figmaNodeJson, nodeId);
  if (!node) return nodeId;
  if (node.type === 'CANVAS' && Array.isArray(node.children) && node.children.length === 1) {
    return node.children[0]?.id || nodeId;
  }
  return nodeId;
}

async function tryExportFigmaImage(fileKey, nodeId, outputPath, nodeJson) {
  if (!fileKey || !nodeId) return null;
  try {
    return await exportFigmaImage(fileKey, nodeId, outputPath, nodeJson);
  } catch (error) {
    return {
      ok: false,
      exitCode: 1,
      stderr: error?.message || 'Figma image export failed',
      imagePath: outputPath,
    };
  }
}

async function exportFigmaImageRobust(fileKey, requestedNodeId, outputPath, figmaNodeJson) {
  const attempts = [];

  const first = await tryExportFigmaImage(fileKey, requestedNodeId, outputPath, figmaNodeJson);
  if (first) attempts.push(first);
  if (first?.ok) return { result: first, attempts };

  const resolvedNodeId = resolveExportNodeId(figmaNodeJson, requestedNodeId);
  if (resolvedNodeId && resolvedNodeId !== requestedNodeId) {
    const second = await tryExportFigmaImage(fileKey, resolvedNodeId, outputPath, figmaNodeJson);
    if (second) attempts.push(second);
    if (second?.ok) return { result: second, attempts };
  }

  return { result: attempts[attempts.length - 1] || null, attempts };
}

async function prepareFigmaState(figmaUrl, figmaDir, sharedFigmaRoot) {
  const parsedFigma = parseFigmaUrl(figmaUrl);
  writeJson(path.join(figmaDir, 'parsed-figma-url.json'), parsedFigma);

  const sharedPaths = getSharedFigmaPaths(sharedFigmaRoot, parsedFigma);
  primeRunFigmaDirFromShared(sharedPaths, figmaDir);

  let fetchedFigma = readJsonIfExists(path.join(figmaDir, 'fetch-result.json'));
  if (!fetchedFigma?.ok) {
    fetchedFigma = await fetchFigmaApi(figmaUrl, figmaDir);
    writeJson(path.join(figmaDir, 'fetch-result.json'), fetchedFigma);
  }

  const figmaNodeJson = readJsonIfExists(path.join(figmaDir, 'figma-node.json'));
  const referenceImagePath = path.join(figmaDir, 'reference-image.png');
  let exportJson = readJsonIfExists(path.join(figmaDir, 'export-image-result.json'));
  let exportAttempts = readJsonIfExists(path.join(figmaDir, 'export-image-attempts.json')) || [];

  if (!fs.existsSync(referenceImagePath) || !exportJson?.ok) {
    const exportState = await exportFigmaImageRobust(fetchedFigma.fileKey, fetchedFigma.nodeId, referenceImagePath, figmaNodeJson);
    exportJson = exportState.result;
    exportAttempts = exportState.attempts || [];
    writeJson(path.join(figmaDir, 'export-image-result.json'), exportJson || {});
    writeJson(path.join(figmaDir, 'export-image-attempts.json'), exportAttempts);
  }

  let viewport = readJsonIfExists(path.join(figmaDir, 'viewport.json'));
  if (!viewport?.width || !viewport?.height) {
    viewport = deriveViewportFromFigma(figmaNodeJson, parsedFigma.nodeId);
    writeJson(path.join(figmaDir, 'viewport.json'), viewport);
  }

  persistRunFigmaDirToShared(figmaDir, sharedPaths);

  return { parsedFigma, fetchedFigma, referenceImagePath, exportJson, exportAttempts, viewport, sharedPaths };
}

async function prepareCompareOnlyState(figmaUrl, figmaDir, sharedFigmaRoot) {
  const parsedFigma = parseFigmaUrl(figmaUrl);
  const sharedPaths = getSharedFigmaPaths(sharedFigmaRoot, parsedFigma);

  const referenceImagePath = path.join(figmaDir, 'reference-image.png');
  const hasCachedRef = copyFileIfExists(sharedPaths.referenceImage, referenceImagePath);
  if (!hasCachedRef) {
    throw new Error(
      `--compare-only: no cached reference image found at ${sharedPaths.referenceImage}\n` +
      'Run the full pipeline first to populate the shared cache.'
    );
  }

  copyFileIfExists(sharedPaths.figmaNode, path.join(figmaDir, 'figma-node.json'));
  copyFileIfExists(sharedPaths.viewport, path.join(figmaDir, 'viewport.json'));
  writeJson(path.join(figmaDir, 'parsed-figma-url.json'), parsedFigma);

  const figmaNodeJson = readJsonIfExists(path.join(figmaDir, 'figma-node.json'));
  let viewport = readJsonIfExists(path.join(figmaDir, 'viewport.json'));
  if (!viewport?.width || !viewport?.height) {
    viewport = deriveViewportFromFigma(figmaNodeJson, parsedFigma.nodeId);
    writeJson(path.join(figmaDir, 'viewport.json'), viewport);
  }

  const fetchedFigma =  { ok: true, fileKey: parsedFigma.fileKey, nodeId: parsedFigma.nodeId };
  const exportJson = { ok: true, compareOnly: true };

  return {
    parsedFigma,
    fetchedFigma,
    referenceImagePath,
    exportJson,
    exportAttempts: [],
    viewport,
    sharedPaths,
  };
}

module.exports = {
  prepareFigmaState,
  prepareCompareOnlyState,
};
