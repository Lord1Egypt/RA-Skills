#!/usr/bin/env node
/**
 * diff-wizard.js — CLI entry point for Diff Wizard
 *
 * Smart text comparison tool with format-aware diffing,
 * AI explanation, and 3-way merge.
 *
 * Usage:
 *   diff-wizard <file-a> <file-b>
 *   diff-wizard --paste
 *   diff-wizard --merge <base> <ours> <theirs>
 *   diff-wizard <dir-a> <dir-b>
 *   diff-wizard --help
 */

'use strict';

const fs = require('fs');
const path = require('path');

const diffEngine = require('./lib/diff-engine');
const threeWayMerger = require('./lib/three-way-merger');
const directoryScanner = require('./lib/directory-scanner');
const aiExplainer = require('./lib/ai-explainer');
const outputRenderer = require('./lib/output-renderer');

const VERSION = '1.0.0';

/**
 * Parse command-line arguments.
 * Supports: --option value, --flag, --option=value
 */
function parseArgs(args) {
  const parsed = {
    files: [],
    mode: 'file-diff',
    options: {},
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '--help' || arg === '-h') {
      parsed.mode = 'help';
      return parsed;
    }

    if (arg === '--version' || arg === '-v') {
      parsed.mode = 'version';
      return parsed;
    }

    if (arg === '--paste') {
      parsed.mode = 'paste';
      continue;
    }

    if (arg === '--merge') {
      parsed.mode = 'merge';
      continue;
    }

    if (arg.startsWith('--')) {
      const eqIdx = arg.indexOf('=');
      let key, val;

      if (eqIdx > -1) {
        key = arg.slice(2, eqIdx);
        val = arg.slice(eqIdx + 1);
      } else if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        key = arg.slice(2);
        val = args[++i];
      } else {
        key = arg.slice(2);
        val = true;
      }

      // Normalize key: --no-color → color=false, etc.
      if (key.startsWith('no-')) {
        key = key.slice(3);
        val = false;
      }

      parsed.options[key.replace(/-/g, '_')] = val;
    } else {
      parsed.files.push(arg);
    }
  }

  return parsed;
}

/**
 * Print help/usage.
 */
function printHelp() {
  console.log(`
 ╔══════════════════════════════════════════╗
 ║     Diff Wizard v${VERSION} — 文本对比精灵      ║
 ╚══════════════════════════════════════════╝

 Usage:
   diff-wizard <file-a> <file-b>     Compare two files
   diff-wizard --paste               Paste content to compare
   diff-wizard --merge <base> <ours> <theirs>   3-way merge
   diff-wizard <dir-a> <dir-b>       Compare two directories
   diff-wizard --help                Show this help
   diff-wizard --version             Show version

 Options:
   --format <type>         Force format: json, yaml, csv, toml, code, text
   --output <format>       Output: terminal, unified, side-by-side, markdown, html, json
   --context-lines <n>     Context lines (0-99, default: 3)
   --ignore-whitespace     Ignore whitespace-only changes
   --ignore-case           Ignore case differences
   --sort-keys             Sort JSON keys before comparison
   --ai-explain            Enable AI explanation (default: true)
   --no-ai-explain         Disable AI explanation
   --ai-language <lang>    AI language: zh-CN, en-US, auto
   --detail-level <level>  summary, normal, detailed
   --color / --no-color    Terminal color output
   --exclude <patterns>    Comma-separated exclude patterns (dir mode)
   --auto-resolve          Auto-resolve non-conflicting 3-way merges
   --strategy <strategy>   ours, theirs, manual (3-way merge)
   --output-file <path>    Write output to file

 Examples:
   diff-wizard before.json after.json
   diff-wizard --paste
   diff-wizard --merge base.ts ours.ts theirs.ts
   diff-wizard ./config-v1/ ./config-v2/ --exclude "node_modules,.git"
`);
}

/**
 * Main execution function.
 */
async function main() {
  const parsed = parseArgs(process.argv.slice(2));

  if (parsed.mode === 'help') {
    printHelp();
    return;
  }

  if (parsed.mode === 'version') {
    console.log(`diff-wizard v${VERSION}`);
    return;
  }

  const opts = parsed.options;

  if (parsed.mode === 'paste') {
    await handlePasteMode(opts);
    return;
  }

  if (parsed.mode === 'merge') {
    await handleMergeMode(parsed.files, opts);
    return;
  }

  // Default: file or directory mode
  if (parsed.files.length === 0) {
    console.error('Error: No files specified. Use --help for usage info.');
    process.exit(1);
  }

  if (parsed.files.length === 1) {
    console.error('Error: Only one file specified. Provide two files to compare.');
    process.exit(1);
  }

  // Check if arguments are directories
  const statA = tryStat(parsed.files[0]);
  const statB = tryStat(parsed.files[1]);

  if (statA && statA.isDirectory() && statB && statB.isDirectory()) {
    await handleDirectoryMode(parsed.files[0], parsed.files[1], opts);
  } else {
    await handleFileMode(parsed.files[0], parsed.files[1], opts);
  }
}

/**
 * Handle file comparison mode.
 */
async function handleFileMode(fileA, fileB, opts) {
  const outputFormat = opts.output || 'terminal';

  // Check file existence
  if (!fs.existsSync(fileA)) {
    console.error(`E001: File not found: ${fileA}`);
    // Try to suggest closest match
    const dir = path.dirname(path.resolve(fileA));
    try {
      const candidates = fs.readdirSync(dir);
      const { findClosestPath } = require('./lib/utils');
      const closest = findClosestPath(path.basename(fileA), candidates);
      if (closest) {
        console.error(`Did you mean: ${path.join(dir, closest)}?`);
      }
    } catch { /* ignore */ }
    process.exit(1);
  }

  if (!fs.existsSync(fileB)) {
    console.error(`E001: File not found: ${fileB}`);
    process.exit(1);
  }

  try {
    // Force format detection if not specified
    const effectiveFormat = opts.format || 'auto';

    // Detect binary files
    const { isBinaryFile } = require('./lib/format-detector');
    if (isBinaryFile(fileA) || isBinaryFile(fileB)) {
      console.error('Error: Binary file detected — text comparison not supported.');
      process.exit(1);
    }

    // Perform comparison
    const result = diffEngine.compareFiles(fileA, fileB, {
      format: effectiveFormat,
      contextLines: parseInt(opts.context_lines || '3', 10),
      ignoreWhitespace: opts.ignore_whitespace === true || opts.ignore_whitespace === 'true',
      ignoreCase: opts.ignore_case === true || opts.ignore_case === 'true',
      sortKeys: opts.sort_keys === true || opts.sort_keys === 'true',
      maxFileSizeMB: parseFloat(opts.max_file_size_mb || '100'),
    });

    if (!result.ok) {
      console.error(`Error: ${result.error}`);
      process.exit(1);
    }

    // Generate AI explanation if enabled
    const useAi = opts.ai_explain !== false && opts.ai_explain !== 'false';
    if (useAi && !result.identical) {
      const aiResult = aiExplainer.generateExplanation(result, {
        language: opts.ai_language || 'auto',
      });
      if (aiResult.ok && aiResult.explanation) {
        result.ai_explanation = aiResult.explanation;
        result.ai_summary = aiResult.summary;
      }
    }

    // Render output
    const rendered = outputRenderer.render(result, outputFormat, {
      color: opts.color !== false && opts.color !== 'false',
      detailLevel: opts.detail_level || 'normal',
    });

    console.log(rendered);

    // Write to output file if specified
    if (opts.output_file) {
      fs.writeFileSync(opts.output_file, rendered, 'utf-8');
      console.error(`\n(Output saved to: ${opts.output_file})`);
    }

  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

/**
 * Handle paste mode — read two chunks from stdin.
 */
async function handlePasteMode(opts) {
  const outputFormat = opts.output || 'terminal';
  const readStdin = () => {
    return new Promise((resolve) => {
      const chunks = [];
      process.stdin.setEncoding('utf-8');
      process.stdin.on('data', (chunk) => chunks.push(chunk));
      process.stdin.on('end', () => resolve(chunks.join('')));
    });
  };

  process.stdout.write('📋 Paste left content (Ctrl+D to finish):\n');
  const leftContent = await readStdin();

  if (!leftContent || leftContent.trim().length === 0) {
    console.error('E004: Left content is empty. Please provide content to compare.');
    process.exit(1);
  }

  process.stdout.write('\n📋 Paste right content (Ctrl+D to finish):\n');
  const rightContent = await readStdin();

  if (!rightContent || rightContent.trim().length === 0) {
    console.error('E004: Right content is empty. Please provide content to compare.');
    process.exit(1);
  }

  const effectiveFormat = opts.format || 'auto';
  const result = diffEngine.compareContent(leftContent, rightContent, {
    format: effectiveFormat,
    contextLines: parseInt(opts.context_lines || '3', 10),
    ignoreWhitespace: opts.ignore_whitespace === true || opts.ignore_whitespace === 'true',
    ignoreCase: opts.ignore_case === true || opts.ignore_case === 'true',
    sortKeys: opts.sort_keys === true || opts.sort_keys === 'true',
  });

  if (!result.ok) {
    console.error(`Error: ${result.error}`);
    process.exit(1);
  }

  // Generate AI explanation
  const useAi = opts.ai_explain !== false && opts.ai_explain !== 'false';
  if (useAi && !result.identical) {
    const aiResult = aiExplainer.generateExplanation(result, {
      language: opts.ai_language || 'auto',
    });
    if (aiResult.ok && aiResult.explanation) {
      result.ai_explanation = aiResult.explanation;
      result.ai_summary = aiResult.summary;
    }
  }

  const rendered = outputRenderer.render(result, outputFormat, {
    color: opts.color !== false && opts.color !== 'false',
    detailLevel: opts.detail_level || 'normal',
  });

  console.log(rendered);
}

/**
 * Handle 3-way merge mode.
 */
async function handleMergeMode(files, opts) {
  if (files.length < 3) {
    console.error('Error: --merge requires exactly 3 files: <base> <ours> <theirs>');
    console.error('Usage: diff-wizard --merge base.json ours.json theirs.json');
    process.exit(1);
  }

  const [basePath, oursPath, theirsPath] = files;

  for (const [label, fp] of [['base', basePath], ['ours', oursPath], ['theirs', theirsPath]]) {
    if (!fs.existsSync(fp)) {
      console.error(`E001: ${label} file not found: ${fp}`);
      process.exit(1);
    }
  }

  try {
    // Check binary files
    const { isBinaryFile } = require('./lib/format-detector');
    if (isBinaryFile(basePath) || isBinaryFile(oursPath) || isBinaryFile(theirsPath)) {
      console.error('Error: Binary files not supported for 3-way merge.');
      process.exit(1);
    }

    const baseContent = fs.readFileSync(basePath, 'utf-8');
    const oursContent = fs.readFileSync(oursPath, 'utf-8');
    const theirsContent = fs.readFileSync(theirsPath, 'utf-8');

    const mergeResult = threeWayMerger.threeWayMerge(baseContent, oursContent, theirsContent, {
      autoResolve: opts.auto_resolve === true || opts.auto_resolve === 'true',
      strategy: opts.strategy || 'manual',
      generateAiSuggestions: opts.ai_explain !== false,
    });

    if (!mergeResult.ok) {
      console.error(`Error: ${mergeResult.error}`);
      process.exit(1);
    }

    const rendered = outputRenderer.renderMergeResult(mergeResult, {
      color: opts.color !== false && opts.color !== 'false',
    });

    console.log(rendered);

    // Save merged output if requested
    if (opts.output || opts.output_file) {
      const outputPath = opts.output_file || 'merged-output.txt';
      fs.writeFileSync(outputPath, mergeResult.mergedContent, 'utf-8');
      console.error(`\n(Merged content saved to: ${outputPath})`);
    }

    if (mergeResult.hasConflicts && mergeResult.conflictCount >= 100) {
      console.error('\nE008: Large number of conflicts. Manual review recommended.');
    }

  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

/**
 * Handle directory comparison mode.
 */
async function handleDirectoryMode(dirA, dirB, opts) {
  const outputFormat = opts.output || 'terminal';

  if (!fs.existsSync(dirA)) {
    console.error(`E001: Directory not found: ${dirA}`);
    process.exit(1);
  }
  if (!fs.existsSync(dirB)) {
    console.error(`E001: Directory not found: ${dirB}`);
    process.exit(1);
  }

  try {
    const exclude = opts.exclude
      ? opts.exclude.split(',').map(s => s.trim()).filter(Boolean)
      : [];

    const result = directoryScanner.compareDirectories(dirA, dirB, {
      recursive: true,
      maxDepth: parseInt(opts.max_depth || '99', 10),
      exclude,
      maxFileSizeMB: parseFloat(opts.max_file_size_mb || '100'),
      contextLines: parseInt(opts.context_lines || '3', 10),
      ignoreWhitespace: opts.ignore_whitespace === true || opts.ignore_whitespace === 'true',
    });

    if (!result.ok) {
      console.error(`Error: Could not compare directories`);
      process.exit(1);
    }

    const dd = result.directory_diff;
    const s = result.stats;

    // Render directory summary
    console.log(`\n ═══════════════════════════════════════════`);
    console.log(` 📁 ${dirA}  ↔  ${dirB}`);
    console.log(` ═══════════════════════════════════════════`);
    console.log(` 📊 ${dd.total_files} files total`);
    console.log(` 🟢 Added: ${s.added}  🔴 Deleted: ${s.deleted}  🟡 Modified: ${s.modified}  ⚪ Unchanged: ${s.unchanged}`);

    if (dd.added_files.length > 0) {
      console.log(`\n 🟢 New files:`);
      for (const f of dd.added_files.slice(0, 10)) {
        console.log(`    + ${f}`);
      }
      if (dd.added_files.length > 10) {
        console.log(`    ... and ${dd.added_files.length - 10} more`);
      }
    }

    if (dd.deleted_files.length > 0) {
      console.log(`\n 🔴 Deleted files:`);
      for (const f of dd.deleted_files.slice(0, 10)) {
        console.log(`    - ${f}`);
      }
      if (dd.deleted_files.length > 10) {
        console.log(`    ... and ${dd.deleted_files.length - 10} more`);
      }
    }

    if (dd.modified_files.length > 0) {
      console.log(`\n 🟡 Modified files:`);
      for (const f of dd.modified_files.slice(0, 10)) {
        const diff = dd.per_file_diffs[f];
        if (diff && diff.stats) {
          const stat = diff.stats;
          const added = stat.lines_added || stat.fields_added || 0;
          const deleted = stat.lines_deleted || stat.fields_deleted || 0;
          console.log(`    ~ ${f}  (+${added} -${deleted})`);
        } else {
          console.log(`    ~ ${f}`);
        }
      }
      if (dd.modified_files.length > 10) {
        console.log(`    ... and ${dd.modified_files.length - 10} more`);
      }
    }

    // Generate AI summary for the whole directory diff
    const useAi = opts.ai_explain !== false && opts.ai_explain !== 'false';
    if (useAi && dd.modified_files.length > 0) {
      const isZh = opts.ai_language === 'zh-CN' || (opts.ai_language === 'auto' && detectDirChinese(dirA, dirB));
      const aiSummary = isZh
        ? `${dd.total_files} 个文件中，${s.modified} 个有改动，${s.added} 个新增，${s.deleted} 个删除。`
        : `${dd.total_files} total files: ${s.modified} modified, ${s.added} added, ${s.deleted} deleted.`;
      console.log(`\n 🤖 AI Summary:\n    ${aiSummary}`);
    }

    if (result.scan_errors && result.scan_errors.length > 0) {
      console.log(`\n ⚠ Scan warnings:`);
      for (const err of result.scan_errors.slice(0, 5)) {
        console.log(`    ${err.path}: ${err.error}`);
      }
    }

    console.log();

  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

/**
 * Try to stat a path, returning null on error.
 */
function tryStat(p) {
  try { return fs.statSync(p); } catch { return null; }
}

/**
 * Detect if directory names/paths contain Chinese characters.
 */
function detectDirChinese(dirA, dirB) {
  return /[\u4e00-\u9fff]/.test(dirA) || /[\u4e00-\u9fff]/.test(dirB);
}

// Run main
main().catch(err => {
  console.error(`Fatal: ${err.message}`);
  process.exit(1);
});
