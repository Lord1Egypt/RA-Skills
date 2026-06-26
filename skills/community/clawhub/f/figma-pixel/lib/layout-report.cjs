const fs = require('fs');
const path = require('path');

function readJsonSafe(filePath) {
  if (!filePath || !fs.existsSync(filePath)) return null;
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch {
    return null;
  }
}

function parseTopMismatches(top) {
  if (Array.isArray(top)) return top.filter(Boolean);
  return String(top || '').split('|').map((s) => s.trim()).filter(Boolean);
}

function computeMatchStats(pixelmatchReport) {
  const mismatch = pixelmatchReport?.diffPercent ?? null;
  const match = mismatch == null ? null : +(100 - Number(mismatch)).toFixed(2);
  const status = mismatch == null ? 'blocked'
    : mismatch <= 5 ? 'pass'
    : mismatch <= 20 ? 'needs review'
    : 'needs work';
  return { mismatch, match, status };
}

function buildHeaderSection(report) {
  const { figma, page, viewport, matchPercent, mismatchPercent, status, viewportFallbackUsed } = report;
  const lines = ['# Layout report', ''];
  if (figma) lines.push(`- **Figma:** ${figma}`);
  if (page) lines.push(`- **Page:** ${page}`);
  if (viewport) lines.push(`- **Viewport:** ${viewport}`);
  if (viewportFallbackUsed) lines.push('- **Viewport source:** fallback (Figma bounds were unavailable)');
  if (matchPercent != null) lines.push(`- **Match:** ${matchPercent}%`);
  if (mismatchPercent != null) lines.push(`- **Mismatch:** ${mismatchPercent}%`);
  lines.push(`- **Status:** ${status}`, '');
  return lines;
}

function buildArtifactsSection(artifacts, jsonPath) {
  return [
    '## Artifacts',
    `- reference image: ${artifacts.referenceImage || 'n/a'}`,
    `- screenshot: ${artifacts.screenshot || 'n/a'}`,
    `- diff image: ${artifacts.diffImage || 'n/a'}`,
    `- report json: ${jsonPath}`,
    '',
  ];
}

function buildTopMismatchesSection(topMismatches) {
  const lines = ['## Top mismatches'];
  if (topMismatches.length) {
    for (const item of topMismatches) lines.push(`- ${item}`);
  } else {
    lines.push('- n/a');
  }
  lines.push('');
  return lines;
}

function buildOpenCvSection(opencvReport) {
  const lines = ['## OpenCV analysis'];
  if (!opencvReport?.ok) {
    lines.push(`- ${opencvReport?.error || 'not available'}`);
    return lines;
  }
  lines.push(`- difference regions: ${opencvReport.differenceRegionCount ?? 'n/a'}`);
  if (Array.isArray(opencvReport.summary) && opencvReport.summary.length) {
    for (const item of opencvReport.summary.slice(0, 5)) lines.push(`- ${item}`);
  } else {
    lines.push('- n/a');
  }
  if (Array.isArray(opencvReport.largestRegions) && opencvReport.largestRegions.length) {
    lines.push('', '### Largest regions');
    for (const region of opencvReport.largestRegions.slice(0, 5)) {
      lines.push(`- ${region.zone}: ${region.width}x${region.height}px at (${region.x}, ${region.y}), mean diff ${region.meanAbsDiff}`);
    }
  }
  return lines;
}

function buildSummaryMarkdown(report, opencvReport, jsonPath) {
  return [
    ...buildHeaderSection(report),
    ...buildArtifactsSection(report.artifacts, jsonPath),
    ...buildTopMismatchesSection(report.topMismatches),
    ...buildOpenCvSection(opencvReport),
  ].join('\n') + '\n';
}

function generateLayoutReport(options = {}) {
  const outputDir = path.resolve(options.output || 'figma-pixel-runs/project/run-id/final');
  fs.mkdirSync(outputDir, { recursive: true });

  const pixelmatchReport = readJsonSafe(options.pixelmatchReport || '');
  const opencvReport = readJsonSafe(options.opencvReport || '');
  const topMismatches = parseTopMismatches(options.top);
  const { mismatch, match, status } = computeMatchStats(pixelmatchReport);

  const report = {
    figma: options.figma || '',
    page: options.page || '',
    viewport: options.viewport || '',
    matchPercent: match,
    mismatchPercent: mismatch,
    status,
    viewportFallbackUsed: topMismatches.includes('viewport fallback used: no usable Figma node bounds'),
    artifacts: {
      referenceImage: options.reference || null,
      screenshot: options.screenshot || null,
      diffImage: options.diff || null,
      annotatedDiff: opencvReport?.annotatedDiff || null,
      pixelmatchReport: options.pixelmatchReport || null,
      opencvReport: options.opencvReport || null,
    },
    topMismatches,
  };

  const jsonPath = path.join(outputDir, 'report.json');
  const summaryPath = path.join(outputDir, 'summary.md');
  fs.writeFileSync(jsonPath, JSON.stringify(report, null, 2));
  fs.writeFileSync(summaryPath, buildSummaryMarkdown(report, opencvReport, jsonPath));

  return { ok: true, report: jsonPath, summary: summaryPath, status, mismatch };
}

module.exports = { generateLayoutReport };
