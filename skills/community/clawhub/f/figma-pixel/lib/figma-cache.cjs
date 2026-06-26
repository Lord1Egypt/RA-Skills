const fs = require('fs');
const path = require('path');

const CACHE_FILES = [
  ['parsed-figma-url.json', 'parsedFigmaUrl'],
  ['fetch-result.json', 'fetchResult'],
  ['figma-node.json', 'figmaNode'],
  ['export-image-result.json', 'exportImageResult'],
  ['export-image-attempts.json', 'exportImageAttempts'],
  ['reference-image.png', 'referenceImage'],
  ['viewport.json', 'viewport'],
  ['implementation-spec.json', 'implementationSpec'],
];

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(value, null, 2));
}

function copyFileIfExists(fromPath, toPath) {
  if (!fromPath || !toPath || !fs.existsSync(fromPath)) return false;
  fs.mkdirSync(path.dirname(toPath), { recursive: true });
  fs.copyFileSync(fromPath, toPath);
  return true;
}

function readJsonIfExists(filePath) {
  if (!fs.existsSync(filePath)) return null;
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function buildSharedFigmaKey(parsedFigma) {
  const sanitize = (s) => String(s).replace(/[^a-zA-Z0-9_-]/g, (c) => c === ':' ? '__' : '-');
  return `${sanitize(parsedFigma?.fileKey || 'file')}--${sanitize(parsedFigma?.nodeId || 'root')}`;
}

function getSharedFigmaPaths(sharedFigmaRoot, parsedFigma) {
  const key = buildSharedFigmaKey(parsedFigma);
  const cacheDir = path.join(sharedFigmaRoot, key);
  const paths = { key, cacheDir };
  for (const [filename, prop] of CACHE_FILES) {
    paths[prop] = path.join(cacheDir, filename);
  }
  return paths;
}

function primeRunFigmaDirFromShared(sharedPaths, figmaDir) {
  for (const [filename, prop] of CACHE_FILES) {
    copyFileIfExists(sharedPaths[prop], path.join(figmaDir, filename));
  }
}

function persistRunFigmaDirToShared(figmaDir, sharedPaths) {
  fs.mkdirSync(sharedPaths.cacheDir, { recursive: true });
  for (const [filename, prop] of CACHE_FILES) {
    copyFileIfExists(path.join(figmaDir, filename), sharedPaths[prop]);
  }
}

module.exports = {
  CACHE_FILES,
  writeJson,
  copyFileIfExists,
  readJsonIfExists,
  getSharedFigmaPaths,
  primeRunFigmaDirFromShared,
  persistRunFigmaDirToShared,
};
