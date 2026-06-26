const fs = require('fs');
const path = require('path');
const { getFigmaToken } = require('./config.cjs');
const { fetchJson } = require('./figma-api.cjs');

function assertHttpsDownloadUrl(url) {
  const parsed = new URL(url);
  if (parsed.protocol !== 'https:') {
    throw new Error(`Blocked non-HTTPS reference image download: ${parsed.protocol}`);
  }
}

async function downloadFile(url, outputPath) {
  assertHttpsDownloadUrl(url);
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Reference image download failed: ${response.status}`);
  const arrayBuffer = await response.arrayBuffer();
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, Buffer.from(arrayBuffer));
}

function isSingleChildCanvas(document) {
  return document.type === 'CANVAS' && Array.isArray(document.children) && document.children.length === 1;
}

function pickExportTarget(nodeJson, requestedNodeId) {
  const document = nodeJson?.nodes?.[requestedNodeId]?.document || null;
  if (!document) {
    return { exportNodeId: requestedNodeId, reason: 'requested-node-missing' };
  }

  if (isSingleChildCanvas(document)) {
    const child = document.children[0];
    return {
      exportNodeId: child.id || requestedNodeId,
      reason: 'single-child-frame',
      requestedNodeType: document.type,
      exportNodeType: child.type,
    };
  }

  return {
    exportNodeId: requestedNodeId,
    reason: 'direct-node',
    requestedNodeType: document.type,
    exportNodeType: document.type,
  };
}

async function exportFigmaImage(fileKey, nodeId, outputPath = 'reference-image.png', nodeJson = null, options = {}) {
  if (!fileKey || !nodeId) throw new Error('exportFigmaImage: fileKey and nodeId are required');

  const token = getFigmaToken(options);
  const resolvedOutputPath = path.resolve(outputPath);
  const target = pickExportTarget(nodeJson, nodeId);
  const headers = { 'X-Figma-Token': token };
  const imageJson = await fetchJson(
    `https://api.figma.com/v1/images/${fileKey}?ids=${encodeURIComponent(target.exportNodeId)}&format=png&scale=1`,
    headers,
    'Figma image'
  );

  const imageUrl = imageJson?.images?.[target.exportNodeId];
  if (!imageUrl) throw new Error('Figma image export URL not found');

  await downloadFile(imageUrl, resolvedOutputPath);

  return {
    ok: true,
    fileKey,
    requestedNodeId: nodeId,
    exportNodeId: target.exportNodeId,
    reason: target.reason,
    requestedNodeType: target.requestedNodeType ?? null,
    exportNodeType: target.exportNodeType ?? null,
    imagePath: resolvedOutputPath,
  };
}

module.exports = { exportFigmaImage };
