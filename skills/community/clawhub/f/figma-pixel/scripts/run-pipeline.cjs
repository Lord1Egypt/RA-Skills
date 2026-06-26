#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { createRunManifest } = require('../lib/run-manifest.cjs');
const { generateLayoutReport } = require('../lib/layout-report.cjs');
const { renderPage: renderPageCapture } = require('../lib/page-render.cjs');
const { runPixelmatch: runPixelmatchDiff } = require('../lib/pixelmatch.cjs');
const { analyzeDiffTiles } = require('../lib/opencv-diff.cjs');
const { compareTiles } = require('../lib/tile-compare.cjs');
const { writeJson } = require('../lib/figma-cache.cjs');
const { prepareFigmaState, prepareCompareOnlyState } = require('../lib/figma-state.cjs');
const { extractDesignTokensFromFile } = require('../lib/design-tokens.cjs');
const { extractFromFile: extractImplementationData } = require('../lib/implementation-extractor.cjs');
const { buildTypographyMap } = require('./extract-typography.cjs');
const { buildSpacingMap } = require('./extract-spacing-map.cjs');
const { buildStrokesMap } = require('./extract-strokes-map.cjs');

function initRun(projectSlug, runId) {
  const manifest = createRunManifest(projectSlug, runId || '', path.resolve(process.cwd(), 'figma-pixel-runs'));
  if (!manifest?.runDir || !manifest?.subdirs) {
    console.error('Failed to initialize run directory');
    process.exit(1);
  }
  return manifest;
}

async function renderPage(pageUrl, screenshotPath, viewport, captureDir) {
  const renderJson = await renderPageCapture(pageUrl, screenshotPath, viewport.width, viewport.height);
  writeJson(path.join(captureDir, 'render-result.json'), renderJson);
  return renderJson;
}

function runPixelmatch(referenceImage, screenshotPath, pixelmatchDir) {
  const diffPath = path.join(pixelmatchDir, 'diff.png');
  const report = runPixelmatchDiff(referenceImage, screenshotPath, diffPath);
  const reportPath = path.join(pixelmatchDir, 'report.json');
  writeJson(reportPath, report);
  return { diffPath, reportPath, report };
}

async function runOpenCvAnalysis(referenceImage, screenshotPath, diffPath, pixelmatchDir, figmaNodePath, tiles) {
  const reportPath = path.join(pixelmatchDir, 'opencv-report.json');

  if (!tiles || !tiles.length) {
    const report = { ok: false, skipped: true, reason: 'no mismatch tiles to analyze', reportPath };
    writeJson(reportPath, report);
    return { reportPath, report };
  }

  try {
    const report = await analyzeDiffTiles(referenceImage, screenshotPath, diffPath, reportPath, figmaNodePath, tiles);
    if (!fs.existsSync(reportPath) && report) writeJson(reportPath, report);
    return { reportPath, report };
  } catch (error) {
    const report = {
      ok: false,
      error: error?.message || 'Tile-based diff region analysis failed',
      reportPath,
    };
    if (!fs.existsSync(reportPath)) writeJson(reportPath, report);
    return { reportPath, report };
  }
}

/**
 * Ensure a JSON artifact exists at outputPath. If a shared cache copy exists,
 * reuse it; otherwise invoke `generate()`, write the result to outputPath, and
 * (when sharedPath is set) persist a copy to the shared cache.
 * Silently swallows generator errors so a single failure does not block the
 * pipeline.
 */
function ensureJsonArtifact({ outputPath, sharedPath, generate }) {
  if (fs.existsSync(outputPath)) return;
  if (sharedPath && fs.existsSync(sharedPath)) {
    fs.copyFileSync(sharedPath, outputPath);
    return;
  }
  try {
    const data = generate();
    if (!data) return;
    writeJson(outputPath, data);
    if (sharedPath) writeJson(sharedPath, data);
  } catch {}
}

/**
 * Generate the Figma-derived analysis artifacts used by the agent:
 * design-tokens, implementation-spec, typography-map, spacing-map.
 * Each artifact reuses its shared cache when available.
 */
function ensureFigmaArtifacts({ figmaNodePath, parsedFigma, paths, sharedPaths }) {
  if (!fs.existsSync(figmaNodePath)) return;

  ensureJsonArtifact({
    outputPath: paths.designTokens,
    sharedPath: null,
    generate: () => extractDesignTokensFromFile(figmaNodePath, parsedFigma.nodeId),
  });

  ensureJsonArtifact({
    outputPath: paths.implSpec,
    sharedPath: sharedPaths.implSpec,
    generate: () => extractImplementationData(figmaNodePath, parsedFigma.nodeId),
  });

  if (!fs.existsSync(paths.implSpec)) return;
  const readSpec = () => JSON.parse(fs.readFileSync(paths.implSpec, 'utf8'));

  ensureJsonArtifact({
    outputPath: paths.typographyMap,
    sharedPath: sharedPaths.typographyMap,
    generate: () => ({ ...buildTypographyMap(readSpec()), sourcePath: paths.implSpec }),
  });

  ensureJsonArtifact({
    outputPath: paths.spacingMap,
    sharedPath: sharedPaths.spacingMap,
    generate: () => ({ ...buildSpacingMap(readSpec()), sourcePath: paths.implSpec }),
  });

  ensureJsonArtifact({
    outputPath: paths.strokesMap,
    sharedPath: sharedPaths.strokesMap,
    generate: () => ({ ...buildStrokesMap(readSpec()), sourcePath: paths.implSpec }),
  });
}

/**
 * Annotate each tile in a tile report with the section it falls in.
 * Reads sections[] from the implementation spec (if available).
 * Adds `sectionName` and `sectionRelativeY` to every tile entry.
 */
function annotateTilesWithSections(tileReport, implSpecPath) {
  if (!tileReport?.tiles?.length) return tileReport;
  let sections = [];
  try {
    if (fs.existsSync(implSpecPath)) {
      const spec = JSON.parse(fs.readFileSync(implSpecPath, 'utf8'));
      sections = (spec.sections || []).map((section) => ({
        name: section.name,
        y: section.bounds?.y ?? 0,
        height: section.bounds?.height ?? 0,
      }));
    }
  } catch {}
  if (!sections.length) return tileReport;

  function sectionForY(tileY) {
    for (const sec of sections) {
      if (tileY >= sec.y && tileY < sec.y + sec.height) {
        return { sectionName: sec.name, sectionRelativeY: tileY - sec.y };
      }
    }
    return {};
  }

  const annotatedTiles = tileReport.tiles.map((tile) => ({ ...tile, ...sectionForY(tile.y) }));
  const annotatedTop = (tileReport.topMismatchTiles || []).map((tile) => ({ ...tile, ...sectionForY(tile.y) }));
  return { ...tileReport, tiles: annotatedTiles, topMismatchTiles: annotatedTop };
}

function buildTopMismatches({ hasReferenceImage, viewport, renderJson, exportJson, pixelmatchReport, opencvReport, tileCompare }) {
  const top = [];
  if (!hasReferenceImage) top.push('reference image missing: figma/reference-image.png');
  if (exportJson && exportJson.ok === false) top.push('figma image export failed');
  if (viewport.fallbackUsed) top.push('viewport fallback used: no usable Figma node bounds');
  if (renderJson.failedRequests?.length) top.push(`failed requests: ${renderJson.failedRequests.length}`);
  if (renderJson.badResponses?.length) top.push(`bad responses: ${renderJson.badResponses.length}`);
  if (tileCompare?.topMismatchTiles?.length) {
    for (const tile of tileCompare.topMismatchTiles.slice(0, 3)) {
      top.push(`tile y=${tile.y}–${tile.y + tile.height}px: ${tile.diffPercent}% mismatch`);
    }
  }
  if (opencvReport?.ok && Array.isArray(opencvReport.summary)) {
    top.push(...opencvReport.summary.slice(0, 5));
  }
  if (opencvReport?.ok && Array.isArray(opencvReport.largestRegions)) {
    for (const region of opencvReport.largestRegions.slice(0, 3)) {
      top.push(`region ${region.zone}: ${region.width}x${region.height}px, mean diff ${region.meanAbsDiff}`);
    }
  }
  if (pixelmatchReport?.diffPercent != null) top.push(`pixel mismatch: ${pixelmatchReport.diffPercent}%`);
  return top;
}

function runFinalReport(options) {
  return generateLayoutReport({
    output: options.outputDir,
    figma: options.figmaUrl,
    page: options.pageUrl,
    viewport: `${options.viewport.width}x${options.viewport.height}`,
    reference: options.referenceImage,
    screenshot: options.screenshotPath,
    diff: options.diffPath,
    pixelmatchReport: options.pixelmatchReportPath,
    opencvReport: options.opencvReportPath,
    top: options.top,
  });
}

/** Read the previous run's mismatch% from the project's run dirs (sorted by name). */
function readPreviousMismatch(projectDir, currentRunId) {
  try {
    const entries = fs.readdirSync(projectDir)
      .filter((entry) => entry !== 'shared' && entry !== currentRunId)
      .sort();
    if (!entries.length) return null;
    const prev = entries[entries.length - 1];
    const reportPath = path.join(projectDir, prev, 'pixelmatch', 'report.json');
    if (!fs.existsSync(reportPath)) return null;
    const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
    return { runId: prev, diffPercent: report.diffPercent ?? null };
  } catch {
    return null;
  }
}

const positional = process.argv.slice(2).filter((arg) => !arg.startsWith('--'));
const flags = new Set(process.argv.slice(2).filter((arg) => arg.startsWith('--')));
const compareOnly = flags.has('--compare-only');

const figmaUrl = positional[0];
const pageUrl = positional[1];
const projectSlug = positional[2] || 'project';
const runId = positional[3];

if (!figmaUrl || !pageUrl) {
  console.error('Usage: node scripts/run-pipeline.cjs <figma-url> <page-url> [project-slug] [run-id] [--compare-only]');
  process.exit(1);
}

async function main() {
  const manifest = initRun(projectSlug, runId);
  const figmaDir = manifest.subdirs.figma;
  const captureDir = manifest.subdirs.capture;
  const pixelmatchDir = manifest.subdirs.pixelmatch;
  const finalDir = manifest.subdirs.final;
  const sharedFigmaRoot = manifest.sharedDirs?.figma || path.join(manifest.projectDir, 'shared', 'figma');

  const figmaState = compareOnly
    ? await prepareCompareOnlyState(figmaUrl, figmaDir, sharedFigmaRoot)
    : await prepareFigmaState(figmaUrl, figmaDir, sharedFigmaRoot);
  const {
    parsedFigma,
    fetchedFigma,
    referenceImagePath,
    exportJson,
    exportAttempts,
    viewport,
    sharedPaths,
  } = figmaState;

  const hasReferenceImage = fs.existsSync(referenceImagePath);
  const screenshotPath = path.join(captureDir, 'captured-page.png');
  const renderJson = await renderPage(pageUrl, screenshotPath, viewport, captureDir);

  const figmaNodePath = path.join(figmaDir, 'figma-node.json');
  const designTokensPath = path.join(figmaDir, 'design-tokens.json');
  const implSpecPath = path.join(figmaDir, 'implementation-spec.json');
  const typographyMapPath = path.join(figmaDir, 'typography-map.json');
  const spacingMapPath = path.join(figmaDir, 'spacing-map.json');
  const strokesMapPath = path.join(figmaDir, 'strokes-map.json');
  const sharedImplSpecPath = path.join(sharedPaths.cacheDir, 'implementation-spec.json');
  const sharedTypographyMapPath = path.join(sharedPaths.cacheDir, 'typography-map.json');
  const sharedSpacingMapPath = path.join(sharedPaths.cacheDir, 'spacing-map.json');
  const sharedStrokesMapPath = path.join(sharedPaths.cacheDir, 'strokes-map.json');

  ensureFigmaArtifacts({
    figmaNodePath,
    parsedFigma,
    paths: {
      designTokens: designTokensPath,
      implSpec: implSpecPath,
      typographyMap: typographyMapPath,
      spacingMap: spacingMapPath,
      strokesMap: strokesMapPath,
    },
    sharedPaths: {
      implSpec: sharedImplSpecPath,
      typographyMap: sharedTypographyMapPath,
      spacingMap: sharedSpacingMapPath,
      strokesMap: sharedStrokesMapPath,
    },
  });

  let pixelmatch = { diffPath: '', reportPath: '', report: null };
  let tileReport = null;

  if (hasReferenceImage) {
    pixelmatch = runPixelmatch(referenceImagePath, screenshotPath, pixelmatchDir);

    // Tile comparison: 300px horizontal bands → ranked mismatch zones
    try {
      tileReport = compareTiles(referenceImagePath, screenshotPath, { tileHeight: 300 });
      // Annotate tiles with section names from the implementation spec
      tileReport = annotateTilesWithSections(tileReport, implSpecPath);
      writeJson(path.join(pixelmatchDir, 'tile-report.json'), tileReport);
    } catch {}
  }

  // ── Write run-result.json early (after pixelmatch, before OpenCV) ──────────
  // This ensures the agent always gets a usable result even if OpenCV crashes.
  const previousRun = readPreviousMismatch(manifest.projectDir, manifest.runId);
  const currentMismatch = pixelmatch.report?.diffPercent ?? null;
  const delta = (previousRun?.diffPercent != null && currentMismatch != null)
    ? +(currentMismatch - previousRun.diffPercent).toFixed(2)
    : null;

  const earlyResult = {
    ok: true,
    runDir: manifest.runDir,
    manifestPath: path.join(manifest.runDir, 'run-manifest.json'),
    viewport,
    fallbackUsed: viewport.fallbackUsed,
    mismatch: currentMismatch,
    delta: delta,
    previousRun: previousRun ?? null,
    artifacts: {
      figmaNode: path.join(figmaDir, 'figma-node.json'),
      implementationSpec: fs.existsSync(implSpecPath) ? implSpecPath : null,
      typographyMap: fs.existsSync(typographyMapPath) ? typographyMapPath : null,
      spacingMap: fs.existsSync(spacingMapPath) ? spacingMapPath : null,
      strokesMap: fs.existsSync(strokesMapPath) ? strokesMapPath : null,
      designTokens: fs.existsSync(designTokensPath) ? designTokensPath : null,
      parsedFigmaUrl: path.join(figmaDir, 'parsed-figma-url.json'),
      viewport: path.join(figmaDir, 'viewport.json'),
      referenceImage: hasReferenceImage ? referenceImagePath : null,
      renderScreenshot: screenshotPath,
      renderReport: path.join(captureDir, 'render-result.json'),
      pixelmatchReport: pixelmatch.reportPath || null,
      pixelmatchDiff: pixelmatch.diffPath || null,
      tileReport: tileReport ? path.join(pixelmatchDir, 'tile-report.json') : null,
      opencvReport: null,
      annotatedDiff: null,
      finalReport: path.join(finalDir, 'report.json'),
      finalSummary: path.join(finalDir, 'summary.md'),
    },
    parsedFigma,
    fetchedFigma,
    exportImage: exportJson,
    exportAttempts,
    sharedFigmaCache: {
      root: sharedFigmaRoot,
      key: sharedPaths.key,
      cacheDir: sharedPaths.cacheDir,
    },
    render: renderJson,
    pixelmatch: pixelmatch.report,
    tileCompare: tileReport,
    opencv: null,
    final: null,
  };
  writeJson(path.join(manifest.runDir, 'run-result.json'), earlyResult);

  // ── OpenCV: per-tile analysis on top mismatch zones ──────────────────────
  let opencv = { reportPath: '', report: null };
  if (hasReferenceImage && tileReport?.topMismatchTiles?.length) {
    const topTiles = tileReport.topMismatchTiles.slice(0, 3);
    opencv = await runOpenCvAnalysis(
      referenceImagePath, screenshotPath, pixelmatch.diffPath,
      pixelmatchDir, figmaNodePath, topTiles
    );
  }

  // ── Final report ──────────────────────────────────────────────────────────
  const top = buildTopMismatches({
    hasReferenceImage,
    viewport,
    renderJson,
    exportJson,
    pixelmatchReport: pixelmatch.report,
    opencvReport: opencv.report,
    tileCompare: tileReport,
  });
  const final = runFinalReport({
    outputDir: finalDir,
    figmaUrl,
    pageUrl,
    viewport,
    referenceImage: hasReferenceImage ? referenceImagePath : '',
    screenshotPath,
    diffPath: pixelmatch.diffPath,
    pixelmatchReportPath: pixelmatch.reportPath,
    opencvReportPath: opencv.reportPath,
    top,
  });

  // ── Overwrite run-result.json with complete data ───────────────────────────
  const runResult = {
    ...earlyResult,
    artifacts: {
      ...earlyResult.artifacts,
      opencvReport: opencv.reportPath || null,
      annotatedDiff: opencv.report?.annotatedDiff || null,
    },
    opencv,
    final,
  };
  writeJson(path.join(manifest.runDir, 'run-result.json'), runResult);
  console.log(JSON.stringify(runResult, null, 2));
}

main().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
