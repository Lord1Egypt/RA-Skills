/**
 * directory-scanner.js — Directory scanning and batch comparison module
 *
 * Recursively scans two directories, aligns files by relative path,
 * and dispatches per-file comparisons.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const diffEngine = require('./diff-engine');
const formatDetector = require('./format-detector');

/**
 * Recursively scan a directory and return a manifest of files.
 * @param {string} dirPath - Directory to scan
 * @param {object} [opts]
 * @param {boolean} [opts.recursive=true]
 * @param {number} [opts.maxDepth=99]
 * @param {number} [opts._depth=0] - Internal
 * @param {string[]} [opts.exclude=[]] - Glob-like patterns to exclude
 * @returns {{ files: string[], errors: Array<{path: string, error: string}>, total: number }}
 */
function scanDirectory(dirPath, opts = {}) {
  const recursive = opts.recursive !== false;
  const maxDepth = opts.maxDepth || 99;
  const exclude = opts.exclude || [];
  const currentDepth = opts._depth || 0;
  const files = [];
  const errors = [];

  if (currentDepth > maxDepth) {
    return { files, errors, total: 0 };
  }

  try {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dirPath, entry.name);
      const relativePath = path.relative(opts._baseDir || dirPath, fullPath);

      // Check exclude patterns
      if (shouldExclude(entry.name, fullPath, exclude)) {
        continue;
      }

      // Skip symlinks by default
      if (entry.isSymbolicLink()) {
        errors.push({ path: relativePath, error: '[symlink: skipped]' });
        continue;
      }

      if (entry.isDirectory()) {
        if (recursive && currentDepth < maxDepth) {
          const subResult = scanDirectory(fullPath, {
            ...opts,
            _baseDir: opts._baseDir || dirPath,
            _depth: currentDepth + 1,
          });
          files.push(...subResult.files);
          errors.push(...subResult.errors);
        }
      } else if (entry.isFile()) {
        try {
          // Test readability
          fs.accessSync(fullPath, fs.constants.R_OK);
          files.push(relativePath);
        } catch {
          errors.push({ path: relativePath, error: '[skipped: permission denied]' });
        }
      }
    }
  } catch (err) {
    errors.push({ path: dirPath, error: `[error: ${err.message}]` });
  }

  return { files, errors, total: files.length };
}

/**
 * Check if a file/dir name matches exclude patterns.
 * Implements simple glob matching (*, ** not supported).
 */
function shouldExclude(name, fullPath, patterns) {
  for (const pattern of patterns) {
    // Simple glob: convert to regex
    const regexStr = pattern
      .replace(/\./g, '\\.')
      .replace(/\*/g, '.*');
    const regex = new RegExp(`^${regexStr}$`, 'i');
    if (regex.test(name) || regex.test(fullPath)) return true;
  }
  return false;
}

/**
 * Build a lookup map of relative path → absolute path.
 * @param {string} baseDir
 * @param {string[]} files
 * @returns {Map<string, string>}
 */
function buildFileMap(baseDir, files) {
  const map = new Map();
  for (const f of files) {
    map.set(f, path.join(baseDir, f));
  }
  return map;
}

/**
 * Compare two directories.
 * @param {string} dirA - Left directory
 * @param {string} dirB - Right directory
 * @param {object} [opts]
 * @param {boolean} [opts.recursive=true]
 * @param {number} [opts.maxDepth=99]
 * @param {string[]} [opts.exclude=[]]
 * @param {number} [opts.maxFileSizeMB=100]
 * @param {number} [opts.contextLines=3]
 * @param {boolean} [opts.ignoreWhitespace=false]
 * @returns {object}
 */
function compareDirectories(dirA, dirB, opts = {}) {
  const scanOpts = {
    recursive: opts.recursive !== false,
    maxDepth: opts.maxDepth || 99,
    exclude: opts.exclude || [],
  };

  // Scan both directories
  const scanA = scanDirectory(dirA, { ...scanOpts, _baseDir: dirA });
  const scanB = scanDirectory(dirB, { ...scanOpts, _baseDir: dirB });

  // Build file maps
  const mapA = buildFileMap(dirA, scanA.files);
  const mapB = buildFileMap(dirB, scanB.files);

  const allFiles = new Set([...mapA.keys(), ...mapB.keys()]);

  const added = [];
  const deleted = [];
  const modified = [];
  const unchanged = [];

  for (const relPath of allFiles) {
    const hasA = mapA.has(relPath);
    const hasB = mapB.has(relPath);

    if (!hasA && hasB) {
      added.push(relPath);
    } else if (hasA && !hasB) {
      deleted.push(relPath);
    } else {
      // Both exist — compare them
      const pathA = mapA.get(relPath);
      const pathB = mapB.get(relPath);

      try {
        const result = diffEngine.compareFiles(pathA, pathB, {
          maxFileSizeMB: opts.maxFileSizeMB || 100,
          contextLines: opts.contextLines || 3,
          ignoreWhitespace: opts.ignoreWhitespace || false,
        });

        if (result.identical) {
          unchanged.push(relPath);
        } else {
          modified.push({ path: relPath, diff: result });
        }
      } catch (err) {
        modified.push({ path: relPath, diff: { error: err.message } });
      }
    }
  }

  // Build per-file diffs
  const perFileDiffs = {};
  for (const m of modified) {
    perFileDiffs[m.path] = m.diff;
  }

  return {
    ok: true,
    dirA,
    dirB,
    directory_diff: {
      total_files: allFiles.size,
      added_files: added,
      deleted_files: deleted,
      modified_files: modified.map(m => m.path),
      unchanged_files: unchanged.length,
      per_file_diffs: perFileDiffs,
    },
    stats: {
      added: added.length,
      deleted: deleted.length,
      modified: modified.length,
      unchanged: unchanged.length,
      total: allFiles.size,
    },
    scan_errors: [...scanA.errors, ...scanB.errors],
  };
}

module.exports = {
  scanDirectory,
  compareDirectories,
  shouldExclude,
};
