const fs = require('fs');
const path = require('path');

function requireModule(name, installCommand) {
  try {
    return require(name);
  } catch {
    throw new Error([
      `Missing dependency: ${name}`,
      'Install the required runtime in the host environment:',
      installCommand,
    ].join('\n'));
  }
}

function ensureImageData() {
  if (typeof global.ImageData === 'undefined') {
    global.ImageData = class ImageDataPolyfill {
      constructor(data, width, height) {
        this.data = data;
        this.width = width;
        this.height = height;
      }
    };
  }
}

function readPng(PNG, filePath) {
  return PNG.sync.read(fs.readFileSync(filePath));
}

function cropTo(PNG, img, width, height) {
  if (img.width === width && img.height === height) return img;
  const out = new PNG({ width, height });
  PNG.bitblt(img, out, 0, 0, width, height, 0, 0);
  return out;
}

function cropSlice(PNG, img, yStart, yEnd) {
  const sliceHeight = yEnd - yStart;
  if (yStart === 0 && sliceHeight === img.height) return img;
  const out = new PNG({ width: img.width, height: sliceHeight });
  PNG.bitblt(img, out, 0, yStart, img.width, sliceHeight, 0, 0);
  return out;
}

function pngToMat(cv, png) {
  if (typeof cv.matFromImageData === 'function') {
    return cv.matFromImageData(new ImageData(Uint8ClampedArray.from(png.data), png.width, png.height));
  }
  if (typeof cv.matFromArray === 'function') {
    return cv.matFromArray(png.height, png.width, cv.CV_8UC4, Array.from(png.data));
  }
  const mat = new cv.Mat(png.height, png.width, cv.CV_8UC4);
  mat.data.set(Uint8Array.from(png.data));
  return mat;
}

function classifyZone(centerX, centerY, width, height) {
  const vertical = centerY < height * 0.25 ? 'top' : centerY > height * 0.75 ? 'bottom' : 'middle';
  const horizontal = centerX < width * 0.33 ? 'left' : centerX > width * 0.66 ? 'right' : 'center';
  return `${vertical}-${horizontal}`;
}

function buildBinaryMaskMatFromDiff(cv, referencePng, screenshotPng, threshold = 24) {
  const referenceMat = pngToMat(cv, referencePng);
  const screenshotMat = pngToMat(cv, screenshotPng);
  const diffMat = new cv.Mat();
  const gray = new cv.Mat();
  const mask = new cv.Mat();

  cv.absdiff(referenceMat, screenshotMat, diffMat);
  cv.cvtColor(diffMat, gray, cv.COLOR_RGBA2GRAY, 0);
  cv.threshold(gray, mask, threshold, 255, cv.THRESH_BINARY);

  referenceMat.delete();
  screenshotMat.delete();
  diffMat.delete();
  gray.delete();

  return mask;
}

function getMeanAbsDiff(reference, screenshot, rect) {
  let total = 0;
  let count = 0;
  for (let pixelY = rect.y; pixelY < rect.y + rect.height; pixelY += 1) {
    for (let pixelX = rect.x; pixelX < rect.x + rect.width; pixelX += 1) {
      const idx = (pixelY * reference.width + pixelX) << 2;
      total += Math.abs(reference.data[idx] - screenshot.data[idx]);
      total += Math.abs(reference.data[idx + 1] - screenshot.data[idx + 1]);
      total += Math.abs(reference.data[idx + 2] - screenshot.data[idx + 2]);
      count += 3;
    }
  }
  return +(total / Math.max(1, count)).toFixed(2);
}

function setPixel(png, pixelX, pixelY, red, green, blue) {
  if (pixelX < 0 || pixelY < 0 || pixelX >= png.width || pixelY >= png.height) return;
  const idx = (pixelY * png.width + pixelX) << 2;
  png.data[idx] = red;
  png.data[idx + 1] = green;
  png.data[idx + 2] = blue;
  png.data[idx + 3] = 255;
}

function drawRect(png, startX, startY, rectWidth, rectHeight, red, green, blue) {
  const borderWidth = 2;
  for (let offset = 0; offset < borderWidth; offset++) {
    for (let px = startX; px < startX + rectWidth; px++) {
      setPixel(png, px, startY + offset, red, green, blue);
      setPixel(png, px, startY + rectHeight - 1 - offset, red, green, blue);
    }
    for (let py = startY; py < startY + rectHeight; py++) {
      setPixel(png, startX + offset, py, red, green, blue);
      setPixel(png, startX + rectWidth - 1 - offset, py, red, green, blue);
    }
  }
}

function saveAnnotatedDiff(PNG, diffPng, regions, annotatedPath) {
  const out = new PNG({ width: diffPng.width, height: diffPng.height });
  diffPng.data.copy(out.data);
  for (const region of regions) {
    drawRect(out, region.x, region.y, region.width, region.height, 0, 255, 0);
  }
  fs.writeFileSync(annotatedPath, PNG.sync.write(out));
  return annotatedPath;
}

function flattenFigmaNodes(figmaNodeJson, rootNodeId) {
  const nodes = [];
  const rootDoc = figmaNodeJson?.nodes?.[rootNodeId]?.document;
  if (!rootDoc) return nodes;

  const rootBounds = rootDoc.absoluteBoundingBox || rootDoc.absoluteRenderBounds;
  const offsetX = rootBounds?.x || 0;
  const offsetY = rootBounds?.y || 0;

  function traverse(node) {
    if (node.visible === false) return;
    const bounds = node.absoluteBoundingBox || node.absoluteRenderBounds;
    if (bounds) {
      nodes.push({
        id: node.id,
        name: node.name,
        type: node.type,
        x: Math.round(bounds.x - offsetX),
        y: Math.round(bounds.y - offsetY),
        width: Math.round(bounds.width),
        height: Math.round(bounds.height),
      });
    }
    if (Array.isArray(node.children)) {
      for (const child of node.children) traverse(child);
    }
  }
  traverse(rootDoc);
  return nodes;
}

function mapRegionsToFigmaLayers(regions, figmaNodes) {
  if (!figmaNodes || !figmaNodes.length) return regions;
  return regions.map((region) => {
    const overlapping = figmaNodes.filter((node) => (
      region.x < node.x + node.width &&
      region.x + region.width > node.x &&
      region.y < node.y + node.height &&
      region.y + region.height > node.y
    ));
    const best = overlapping.slice(0, 5).map((layer) => ({ id: layer.id, name: layer.name, type: layer.type }));
    return { ...region, figmaLayers: best };
  });
}

function validateInputFiles(paths) {
  for (const filePath of paths) {
    if (!fs.existsSync(filePath)) return { ok: false, error: `Missing input file: ${filePath}` };
  }
  return null;
}

async function loadCvDeps() {
  const { PNG } = requireModule('pngjs', 'npm install pngjs');
  const cvModule = requireModule('@techstark/opencv-js', 'npm install @techstark/opencv-js');
  ensureImageData();
  const cv = await cvModule;
  return { PNG, cv };
}

function loadFigmaNodes(figmaNodePath) {
  if (!figmaNodePath || !fs.existsSync(figmaNodePath)) return [];
  try {
    const json = JSON.parse(fs.readFileSync(figmaNodePath, 'utf8'));
    const rootNodeId = Object.keys(json?.nodes || {})[0];
    return rootNodeId ? flattenFigmaNodes(json, rootNodeId) : [];
  } catch {
    return [];
  }
}

function findContourRects(cv, reference, screenshot, minArea) {
  const thresh = buildBinaryMaskMatFromDiff(cv, reference, screenshot, 24);
  const morph = new cv.Mat();
  const kernel = cv.Mat.ones(3, 3, cv.CV_8U);
  const contours = new cv.MatVector();
  const hierarchy = new cv.Mat();
  const rects = [];

  try {
    cv.morphologyEx(thresh, morph, cv.MORPH_OPEN, kernel);
    cv.morphologyEx(morph, morph, cv.MORPH_CLOSE, kernel);
    cv.findContours(morph, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);
    for (let i = 0; i < contours.size(); i++) {
      const contour = contours.get(i);
      const rect = cv.boundingRect(contour);
      contour.delete();
      if (rect.width * rect.height >= minArea) rects.push(rect);
    }
  } finally {
    thresh.delete();
    morph.delete();
    kernel.delete();
    contours.delete();
    hierarchy.delete();
  }

  return rects;
}

function buildRegionSummary(regions, areaLabel) {
  return regions.slice(0, 5).map((region) => {
    const layers = region.figmaLayers?.length
      ? ` → ${region.figmaLayers.slice(0, 2).map((l) => l.name).join(', ')}`
      : '';
    return `difference block at ${region.zone} (${region.width}x${region.height} px, ${region.coveragePercent}% of ${areaLabel})${layers}`;
  });
}

function writeJsonReport(outputPath, report) {
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));
}

function sortRegions(regions) {
  return regions.sort((a, b) => (b.area - a.area) || (b.meanAbsDiff - a.meanAbsDiff));
}

async function analyzeDiff(referencePath, screenshotPath, diffPath, outputReportPath, figmaNodePath) {
  if (!referencePath || !screenshotPath || !diffPath || !outputReportPath) {
    throw new Error('analyzeDiff: referencePath, screenshotPath, diffPath and outputReportPath are required');
  }

  const fileError = validateInputFiles([referencePath, screenshotPath, diffPath]);
  if (fileError) return { ...fileError, reportPath: outputReportPath };

  const { PNG, cv } = await loadCvDeps();
  const figmaNodes = loadFigmaNodes(figmaNodePath);

  const referenceRaw = readPng(PNG, referencePath);
  const screenshotRaw = readPng(PNG, screenshotPath);
  const diffRaw = readPng(PNG, diffPath);
  const width = Math.min(referenceRaw.width, screenshotRaw.width, diffRaw.width);
  const height = Math.min(referenceRaw.height, screenshotRaw.height, diffRaw.height);
  const reference = cropTo(PNG, referenceRaw, width, height);
  const screenshot = cropTo(PNG, screenshotRaw, width, height);
  const diff = cropTo(PNG, diffRaw, width, height);
  const imageArea = width * height;

  const minArea = Math.max(64, Math.floor(imageArea * 0.0005));
  const rects = findContourRects(cv, reference, screenshot, minArea);
  const rawRegions = rects.map((rect) => ({
    x: rect.x,
    y: rect.y,
    width: rect.width,
    height: rect.height,
    area: rect.width * rect.height,
    coveragePercent: +((rect.width * rect.height / imageArea) * 100).toFixed(2),
    meanAbsDiff: getMeanAbsDiff(reference, screenshot, rect),
    zone: classifyZone(rect.x + rect.width / 2, rect.y + rect.height / 2, width, height),
  }));

  sortRegions(rawRegions);
  const largestRegions = mapRegionsToFigmaLayers(rawRegions.slice(0, 12), figmaNodes);
  const summary = buildRegionSummary(largestRegions, 'page');
  const annotatedDiffPath = outputReportPath.replace(/\.json$/, '-annotated.png');
  saveAnnotatedDiff(PNG, diff, largestRegions, annotatedDiffPath);

  const report = {
    ok: true,
    engine: 'opencv-js',
    referenceImage: referencePath,
    screenshot: screenshotPath,
    diffImage: diffPath,
    annotatedDiff: annotatedDiffPath,
    reportPath: outputReportPath,
    imageSize: { width, height },
    differenceRegionCount: rawRegions.length,
    largestRegions,
    summary,
  };

  writeJsonReport(outputReportPath, report);
  return report;
}

async function analyzeDiffTiles(referencePath, screenshotPath, diffPath, outputReportPath, figmaNodePath, tiles) {
  if (!referencePath || !screenshotPath || !diffPath || !outputReportPath) {
    throw new Error('analyzeDiffTiles: referencePath, screenshotPath, diffPath and outputReportPath are required');
  }
  if (!tiles || !tiles.length) {
    return { ok: false, skipped: true, reason: 'no tiles provided', reportPath: outputReportPath };
  }

  const fileError = validateInputFiles([referencePath, screenshotPath, diffPath]);
  if (fileError) return { ...fileError, reportPath: outputReportPath };

  const { PNG, cv } = await loadCvDeps();
  const figmaNodes = loadFigmaNodes(figmaNodePath);

  const referenceRaw = readPng(PNG, referencePath);
  const screenshotRaw = readPng(PNG, screenshotPath);
  const diffRaw = readPng(PNG, diffPath);
  const width = Math.min(referenceRaw.width, screenshotRaw.width, diffRaw.width);
  const totalHeight = Math.min(referenceRaw.height, screenshotRaw.height, diffRaw.height);

  const allRegions = [];
  const tileResults = [];

  for (const tile of tiles) {
    const yStart = tile.y;
    const yEnd = Math.min(yStart + tile.height, totalHeight);
    if (yEnd <= yStart) continue;

    const sliceArea = width * (yEnd - yStart);
    const refSlice = cropSlice(PNG, referenceRaw, yStart, yEnd);
    const shotSlice = cropSlice(PNG, screenshotRaw, yStart, yEnd);

    const minArea = Math.max(64, Math.floor(sliceArea * 0.002));
    const rects = findContourRects(cv, refSlice, shotSlice, minArea);
    const tileRegions = rects.map((rect) => {
      const absoluteY = yStart + rect.y;
      return {
        x: rect.x,
        y: absoluteY,
        width: rect.width,
        height: rect.height,
        area: rect.width * rect.height,
        tileY: yStart,
        coveragePercent: +((rect.width * rect.height / sliceArea) * 100).toFixed(2),
        meanAbsDiff: getMeanAbsDiff(refSlice, shotSlice, rect),
        zone: classifyZone(rect.x + rect.width / 2, absoluteY + rect.height / 2, width, totalHeight),
      };
    });

    sortRegions(tileRegions);
    allRegions.push(...tileRegions);
    tileResults.push({ tileY: yStart, tileHeight: tile.height, diffPercent: tile.diffPercent, regionCount: tileRegions.length });
  }

  sortRegions(allRegions);
  const largestRegions = mapRegionsToFigmaLayers(allRegions.slice(0, 12), figmaNodes);
  const summary = buildRegionSummary(largestRegions, 'tile');
  const diffFull = cropTo(PNG, diffRaw, width, totalHeight);
  const annotatedDiffPath = outputReportPath.replace(/\.json$/, '-annotated.png');
  saveAnnotatedDiff(PNG, diffFull, largestRegions, annotatedDiffPath);

  const report = {
    ok: true,
    engine: 'opencv-js-tiles',
    referenceImage: referencePath,
    screenshot: screenshotPath,
    diffImage: diffPath,
    annotatedDiff: annotatedDiffPath,
    reportPath: outputReportPath,
    imageSize: { width, height: totalHeight },
    tilesAnalyzed: tileResults,
    differenceRegionCount: allRegions.length,
    largestRegions,
    summary,
  };

  writeJsonReport(outputReportPath, report);
  return report;
}

module.exports = { analyzeDiff, analyzeDiffTiles };
