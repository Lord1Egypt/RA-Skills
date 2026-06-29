/**
 * diff-engine.js — Core diff engine for diff-wizard
 *
 * Routes comparison to the appropriate format-specific differ based on
 * detected format. Coordinates between text, JSON, CSV, etc. differ modules.
 * Provides a unified interface for the rest of the application.
 */

'use strict';

const path = require('path');
const fs = require('fs');
const textDiffer = require('./text-differ');
const jsonDiffer = require('./json-differ');
const csvDiffer = require('./csv-differ');
const formatDetector = require('./format-detector');
const security = require('./security');

/**
 * Compare two file contents using the appropriate strategy for the detected format.
 *
 * @param {string} contentA - Left content string
 * @param {string} contentB - Right content string
 * @param {string} labelA - Left label (e.g., filename or "Left")
 * @param {string} labelB - Right label
 * @param {object} [opts]
 * @param {string} [opts.format='auto'] - Forced format or 'auto'
 * @param {number} [opts.contextLines=3]
 * @param {boolean} [opts.ignoreWhitespace=false]
 * @param {boolean} [opts.ignoreCase=false]
 * @param {boolean} [opts.sortKeys=false]
 * @returns {object} Unified diff result object
 */
function compare(contentA, contentB, labelA = 'left', labelB = 'right', opts = {}) {
  const format = opts.format || 'auto';
  const ctxLines = opts.contextLines !== undefined ? opts.contextLines : 3;

  // Determine format
  let detectedFormat = format;
  let detectionSource = 'user-specified';

  if (format === 'auto') {
    // Detect from first non-empty content
    const content = contentA || contentB || '';
    const pathResult = formatDetector.detectFormat(labelA, content);
    const contentResult = content ? formatDetector.detectFromContent(content) : pathResult;

    detectedFormat = contentResult.confidence > pathResult.confidence ? contentResult.format : pathResult.format;
    detectionSource = contentResult.confidence > pathResult.confidence ? contentResult.source : pathResult.source;

    // If label is a file path and we have low confidence, try the other label
    if (detectedFormat === 'text' && pathResult.confidence < 0.5) {
      const pathResultB = formatDetector.detectFormat(labelB, content);
      if (pathResultB.confidence > pathResult.confidence) {
        detectedFormat = pathResultB.format;
        detectionSource = pathResultB.source;
      }
    }
  }

  // Apply content-based overrides if format is still 'auto'
  if (detectedFormat === 'text') {
    const contentDetect = formatDetector.detectFromContent(contentA || contentB || '');
    if (contentDetect.confidence >= 0.8) {
      detectedFormat = contentDetect.format;
      detectionSource = contentDetect.source;
    }
  }

  // Perform comparison based on detected/forced format
  switch (detectedFormat) {
    case 'json': {
      const result = jsonDiffer.compareJSON(contentA, contentB, labelA, labelB, {
        sortKeys: opts.sortKeys,
      });
      return {
        ...result,
        format_detected: 'json',
        format_source: detectionSource,
        labelA,
        labelB,
      };
    }

    case 'csv':
    case 'tsv': {
      const result = csvDiffer.compareCSV(contentA, contentB, { labelA, labelB });
      return {
        ok: true,
        ...result,
        format_detected: detectedFormat,
        format_source: detectionSource,
        labelA,
        labelB,
      };
    }

    case 'text':
    case 'code':
    case 'yaml':
    case 'toml':
    case 'xml':
    case 'html':
    default: {
      if (contentA == null || contentB == null) {
        return { ok: false, error: 'E004: One or both inputs are empty' };
      }
      // For YAML/TOML/XML/HTML/code, use text diff as the base comparison
      // (structured parsing would require heavy dependencies)
      const result = textDiffer.unifiedDiff(contentA, contentB, {
        labelA,
        labelB,
        contextLines: ctxLines,
        ignoreWhitespace: opts.ignoreWhitespace || false,
        ignoreCase: opts.ignoreCase || false,
      });

      return {
        ok: true,
        ...result,
        format_detected: detectedFormat,
        format_source: detectionSource,
        labelA,
        labelB,
        changes: result.hunks
          ? result.hunks.flatMap(h => h.lines
              .filter(l => l.type !== 'equal')
              .map(l => ({
                type: l.type === 'insert' ? 'added' : 'deleted',
                path: l.type === 'insert' ? `Line ${l.newLine}` : `Line ${l.oldLine}`,
                old_value: l.type === 'delete' ? l.text : null,
                new_value: l.type === 'insert' ? l.text : null,
              })))
          : [],
        structured_diff: result.hunks
          ? result.hunks.flatMap(h => h.lines
              .filter(l => l.type !== 'equal')
              .map(l => ({
                type: l.type,
                oldLine: l.oldLine || null,
                newLine: l.newLine || null,
                content: l.text,
              })))
          : [],
      };
    }
  }
}

/**
 * Compare two files by reading them from disk.
 * @param {string} filePathA
 * @param {string} filePathB
 * @param {object} [opts]
 * @returns {object}
 */
function compareFiles(filePathA, filePathB, opts = {}) {
  const maxMB = opts.maxFileSizeMB || 100;

  // Check binary files
  if (formatDetector.isBinaryFile(filePathA) || formatDetector.isBinaryFile(filePathB)) {
    return {
      ok: false,
      error: 'Binary file detected: text comparison not supported for binary files',
    };
  }

  // Read file A
  const resultA = formatDetector.readAndDetect(filePathA, { maxSizeMB: maxMB });
  if (resultA.error) return { ok: false, error: resultA.error };

  // Read file B
  const resultB = formatDetector.readAndDetect(filePathB, { maxSizeMB: maxMB });
  if (resultB.error) return { ok: false, error: resultB.error };

  // Compare
  const labelA = path.basename(filePathA);
  const labelB = path.basename(filePathB);

  // Security: check sensitive files
  const sensA = security.isSensitiveFile(filePathA);
  const sensB = security.isSensitiveFile(filePathB);
  const sensitiveFiles = [];
  if (sensA.sensitive) sensitiveFiles.push(filePathA);
  if (sensB.sensitive) sensitiveFiles.push(filePathB);

  const result = compare(resultA.content, resultB.content, labelA, labelB, opts);

  return {
    ...result,
    fileA: filePathA,
    fileB: filePathB,
    sensitive_files: sensitiveFiles.length > 0 ? sensitiveFiles : undefined,
    format_detected: result.format_detected || resultA.format || 'text',
  };
}

/**
 * Compare two content strings (paste mode).
 * @param {string} contentA
 * @param {string} contentB
 * @param {object} [opts]
 * @returns {object}
 */
function compareContent(contentA, contentB, opts = {}) {
  if (!contentA && !contentB) {
    return { ok: false, error: 'E004: Both inputs are empty' };
  }
  if (contentA === undefined || contentA === null) {
    return { ok: false, error: 'E004: Left content is empty' };
  }
  if (contentB === undefined || contentB === null) {
    return { ok: false, error: 'E004: Right content is empty' };
  }

  return compare(contentA, contentB, 'Left', 'Right', opts);
}

module.exports = {
  compare,
  compareFiles,
  compareContent,
};
