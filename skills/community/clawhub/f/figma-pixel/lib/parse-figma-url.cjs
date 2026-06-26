function parseFigmaUrl(input) {
  if (!input) throw new Error('Usage: node scripts/parse-figma-url.cjs <figma-url>');

  let url;
  try {
    url = new URL(input);
  } catch {
    throw new Error('Invalid URL');
  }

  const pathParts = url.pathname.split('/').filter(Boolean);
  const fileIndex = pathParts.findIndex((part) => part === 'file' || part === 'design');
  const fileKey = fileIndex >= 0 ? pathParts[fileIndex + 1] : null;
  const rawNodeId = url.searchParams.get('node-id') || url.searchParams.get('nodeId') || null;
  const decodedNodeId = rawNodeId ? decodeURIComponent(rawNodeId) : null;
  const nodeId = decodedNodeId ? decodedNodeId.replace(/-/g, ':') : null;

  return {
    url: input,
    fileKey,
    nodeId,
    pathname: url.pathname,
  };
}

module.exports = { parseFigmaUrl };
