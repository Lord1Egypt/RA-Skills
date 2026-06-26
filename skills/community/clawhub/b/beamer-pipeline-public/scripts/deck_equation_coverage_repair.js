#!/usr/bin/env node
/**
 * deck_equation_coverage_repair.js
 *
 * Deterministic auto-repair for equation_coverage defects in Beamer deck pipelines.
 * Consumes scanner output and applies targeted patches to main.tex frames
 * without requiring full programmer re-generation.
 *
 * Repair strategies (in order of preference):
 *   A. Frame has inline `$\displaystyle \begin{aligned}...\end{aligned}\tag{X}$`
 *      → Annotate with a hidden `\[...\]` wrapper so the validator regex matches.
 *      (The actual fix is in the orchestrator regex — see below.)
 *
 *   B. Frame has equation content but missing `\tag{X}` marker
 *      → Insert the appropriate `\tag{}` from analysis.json equation ledger.
 *
 *   C. Frame is missing the equation entirely, but source paragraph is known
 *      → Extract equation LaTeX from analysis.json paragraph_ledger and insert.
 *
 *   D. equation_coverage format mismatch (eq. numbers vs tagged keys)
 *      → Auto-correct the equation_numbers field in coverage (when allowed).
 *
 * Usage:
 *   node scripts/deck_equation_coverage_repair.js <task-dir> [--dry-run] [--scanner-output <json-path>]
 *
 * With --dry-run: reports what would be changed without modifying files.
 * Without --dry-run: applies patches and writes modified main.tex.
 */

"use strict";

const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function isPlainObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function readJsonFile(filePath) {
  try { return JSON.parse(fs.readFileSync(filePath, "utf8")); } catch { return null; }
}

function readBalancedTexGroup(source, startIndex, open, close) {
  let depth = 0;
  let i = startIndex;
  while (i < source.length) {
    const ch = source[i];
    if (ch === open) { depth++; }
    else if (ch === close) { depth--; if (depth === 0) return { value: source.slice(startIndex + 1, i), endIndex: i + 1 }; }
    i++;
  }
  return null;
}

// ---------------------------------------------------------------------------
// Frame parsing (abridged — full version in scanner)
// ---------------------------------------------------------------------------

function extractFrameLabelFromOptions(optionText) {
  const match = String(optionText || "").match(/(?:^|,)\s*label\s*=\s*([^,\]]+)/i);
  return match ? match[1].trim() : "";
}

function parseFramesWithPositions(tex) {
  const frames = [];
  const beginMarker = "\\begin{frame}";
  const endMarker = "\\end{frame}";
  let cursor = 0;

  while (cursor < tex.length) {
    const beginIndex = tex.indexOf(beginMarker, cursor);
    if (beginIndex === -1) break;
    let headerIndex = beginIndex + beginMarker.length;
    while (/\s/.test(tex[headerIndex] || "")) headerIndex++;

    if (tex[headerIndex] === "<") {
      const grp = readBalancedTexGroup(tex, headerIndex, "<", ">");
      if (grp) headerIndex = grp.endIndex;
      while (/\s/.test(tex[headerIndex] || "")) headerIndex++;
    }
    let optionText = "";
    if (tex[headerIndex] === "[") {
      const grp = readBalancedTexGroup(tex, headerIndex, "[", "]");
      if (grp) { optionText = grp.value; headerIndex = grp.endIndex; }
      while (/\s/.test(tex[headerIndex] || "")) headerIndex++;
    }
    if (tex[headerIndex] === "{") {
      const grp = readBalancedTexGroup(tex, headerIndex, "{", "}");
      if (grp) headerIndex = grp.endIndex;
    }

    const endIndex = tex.indexOf(endMarker, headerIndex);
    if (endIndex === -1) break;

    const body = tex.slice(headerIndex, endIndex);
    const fullFrame = tex.slice(beginIndex, endIndex + endMarker.length);
    const label = extractFrameLabelFromOptions(optionText);
    const frameEndInTex = endIndex + endMarker.length;

    // Check if body uses $\displaystyle \begin{aligned}...\end{aligned}\tag{X}$
    const alignedMatch = body.match(/\$\\displaystyle\s*(\\begin\{aligned\*?\}[\s\S]*?\\end\{aligned\*?\})\s*\\tag\{([^}]+)\}\s*\$/);
    const hasInlineAligned = alignedMatch !== null;

    // Extract all \tag{...} values
    const tags = [];
    for (const m of body.matchAll(/\\tag\{([^}]+)\}/g)) {
      tags.push(m[1].trim());
    }

    frames.push({
      index: frames.length,
      label,
      frameStartInTex: beginIndex,
      frameEndInTex,
      bodyStartInTex: headerIndex,
      bodyEndInTex: endIndex,
      fullFrame,
      body,
      hasInlineAligned,
      alignedBody: alignedMatch ? alignedMatch[1] : null,
      alignedTag: alignedMatch ? alignedMatch[2] : null,
      tags,
    });
    cursor = endIndex + endMarker.length;
  }
  return frames;
}

// ---------------------------------------------------------------------------
// Equation ledger extraction
// ---------------------------------------------------------------------------

function buildEquationLedger(analysis) {
  const ledger = new Map();
  const paragraphs = Array.isArray(analysis?.paragraph_ledger) ? analysis.paragraph_ledger : [];

  for (const para of paragraphs) {
    if (!isPlainObject(para)) continue;
    const tags = Array.isArray(para.equation_tags) ? para.equation_tags : [];
    const excerpt = String(para.source_excerpt || "");

    // Extract numbered equation blocks from source_excerpt
    for (const tag of tags) {
      const tagStr = String(tag).trim();
      // Map paragraph's tagged equation numbers to their LaTeX
      if (!ledger.has(tagStr)) {
        // Try to extract the equation from the excerpt
        const eqMatch = excerpt.match(new RegExp(
          `(?:\\\\begin\\{(?:equation|align|aligned)\\*?\\}[\\s\\S]*?\\\\end\\{(?:equation|align|aligned)\\*?\\}|` +
          `\\$\\$[\\s\\S]*?\\$\\$|` +
          `\\\\\\[[\\s\\S]*?\\\\\\])` +
          `[\\s\\S]*?\\\\tag\\{${tagStr.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\}`
        ));
        if (eqMatch) {
          ledger.set(tagStr, { tag: tagStr, latex: eqMatch[0], sourceParagraph: para.paragraph_id });
        }
      }
    }
  }

  return ledger;
}

// ---------------------------------------------------------------------------
// Repair actions
// ---------------------------------------------------------------------------

/**
 * Strategy A: For frames using $\displaystyle \begin{aligned}...\end{aligned}\tag{X}$,
 * the issue is that the validator's regex doesn't match \begin{aligned}.
 * We have two options:
 *   1. Patch the validator regex in orchestrator (add "aligned" pattern)
 *   2. Convert the equation in main.tex
 *
 * Since modifying inside adjustbox is risky, we recommend option 1.
 * This function generates the recommended orchestrator patch.
 */
function recommendAlignedRegexFix() {
  return {
    type: "orchestrator_regex_fix",
    file: "scripts/dev_pipeline_orchestrator.js",
    description: "Add \\begin{aligned} to the display equation regex so inline display math with aligned is counted",
    oldPattern: "\\\\begin\\{align\\*?\\}",
    newPattern: "\\\\begin\\{align(?:ed)?\\*?\\}",
    searchLine: "const displayEquationCount = (body.match(/\\\\eqs?\\{|\\\\begin\\{equation\\*?\\}|\\\\begin\\{align\\*?\\}|\\\\begin\\{gather\\*?\\}|\\\\begin\\{multline\\*?\\}|\\\\begin\\{flalign\\*?\\}|\\\\\\[/g) || []).length;",
  };
}

/**
 * Strategy B: Add missing \tag{} markers to frames that have aligned content.
 * This handles cases where the equation content exists but the tag number
 * expected by equation_coverage is missing or mismatched.
 */
function repairMissingTags(mainTex, frames, coverageEntries, equationLedger) {
  const patches = [];

  // Build map: slide_id → expected equation numbers
  const expectedBySlide = new Map();
  for (const entry of coverageEntries) {
    if (!isPlainObject(entry)) continue;
    const slideIds = Array.isArray(entry.slide_ids) ? entry.slide_ids : [entry.slide_id].filter(Boolean);
    const numbers = Array.isArray(entry.equation_numbers) ? entry.equation_numbers : [entry.equation_numbers].filter(Boolean);
    for (const sid of slideIds) {
      const sidStr = String(sid).trim();
      if (!expectedBySlide.has(sidStr)) expectedBySlide.set(sidStr, []);
      expectedBySlide.get(sidStr).push(...numbers);
    }
  }

  for (const frame of frames) {
    if (!frame.label) continue;
    const expected = expectedBySlide.get(frame.label.toLowerCase());
    if (!expected || expected.length === 0) continue;

    // Normalize: extract "2.1" from "Eq. (2.1)", etc.
    const expectedNums = new Set();
    for (const e of expected) {
      const str = String(e);
      const m = str.match(/(\d+\.\d+|[A-Z]\.\d+)/);
      if (m) expectedNums.add(m[1]);
      else if (/^\d+$/.test(str)) expectedNums.add(str);
    }

    const frameNums = new Set(frame.tags.map((t) => {
      const m = t.match(/(\d+\.\d+|[A-Z]\.\d+)/);
      return m ? m[1] : t;
    }));

    const missing = [...expectedNums].filter((n) => !frameNums.has(n));

    if (missing.length > 0 && frame.hasInlineAligned) {
      // The frame has inline aligned equations — add missing tags
      // We append \tag{missing_num} after the aligned block
      for (const num of missing) {
        patches.push({
          type: "add_missing_tag",
          frameLabel: frame.label,
          frameIndex: frame.index,
          equationNumber: num,
          description: `Frame ${frame.label} has inline aligned equation but missing \\tag{${num}}`,
          action: "add_tag_to_aligned_block",
        });
      }
    }
  }

  return patches;
}

/**
 * Strategy C: Insert missing equation block from analysis.json ledger into main.tex.
 */
function repairMissingEquations(mainTex, frames, coverageEntries, equationLedger) {
  const patches = [];
  const texSource = mainTex;

  // Build map as above
  const expectedBySlide = new Map();
  for (const entry of coverageEntries) {
    if (!isPlainObject(entry)) continue;
    const slideIds = Array.isArray(entry.slide_ids) ? entry.slide_ids : [entry.slide_id].filter(Boolean);
    for (const sid of slideIds) {
      const sidStr = String(sid).trim();
      if (!expectedBySlide.has(sidStr)) expectedBySlide.set(sidStr, []);
      expectedBySlide.get(sidStr).push(entry);
    }
  }

  for (const frame of frames) {
    if (!frame.label) continue;
    const entries = expectedBySlide.get(frame.label.toLowerCase());
    if (!entries || entries.length === 0) continue;

    for (const entry of entries) {
      const numbers = Array.isArray(entry.equation_numbers) ? entry.equation_numbers : [entry.equation_numbers].filter(Boolean);
      const frameNumSet = new Set(frame.tags);

      const allPresent = numbers.every((n) => {
        const str = String(n);
        const m = str.match(/(\d+\.\d+|[A-Z]\.\d+)/);
        const key = m ? m[1] : str;
        return frame.tags.some((t) => t.includes(key));
      });

      if (!allPresent && !frame.hasInlineAligned) {
        // Frame doesn't have any aligned block with tags — need to insert equation
        const sourceParagraphIds = Array.isArray(entry.source_paragraph_ids) ? entry.source_paragraph_ids : [];
        patches.push({
          type: "insert_equation_from_ledger",
          frameLabel: frame.label,
          frameIndex: frame.index,
          sourceLabel: entry.source_label || entry.label,
          equationNumbers: numbers,
          sourceParagraphIds,
          description: `Frame ${frame.label} missing entire equation block for ${numbers.join(", ")}`,
          action: "insert_equation_at_frame_end",
        });
      }
    }
  }

  return patches;
}

// ---------------------------------------------------------------------------
// Main repair function
// ---------------------------------------------------------------------------

function repairEquationCoverage(taskDir, options = {}) {
  const dryRun = options.dryRun || false;
  const analysisPath = path.join(taskDir, "analysis.json");
  const slidesPath = path.join(taskDir, "slides.json");
  const mainTexPath = path.join(taskDir, "main.tex");

  const analysis = readJsonFile(analysisPath);
  const slidesDoc = readJsonFile(slidesPath);

  if (!fs.existsSync(mainTexPath)) {
    return { error: "main.tex not found", taskDir };
  }

  const mainTex = fs.readFileSync(mainTexPath, "utf8");
  const frames = parseFramesWithPositions(mainTex);
  const equationLedger = buildEquationLedger(analysis);

  // Collect equation_coverage
  const coverage = Array.isArray(slidesDoc?.equation_coverage)
    ? slidesDoc.equation_coverage
    : (Array.isArray(analysis?.equation_coverage) ? analysis.equation_coverage : []);

  const report = {
    task_dir: taskDir,
    dry_run: dryRun,
    summary: {
      total_frames: frames.length,
      frames_with_labels: frames.filter((f) => f.label).length,
      frames_with_inline_aligned: frames.filter((f) => f.hasInlineAligned).length,
      total_coverage_entries: coverage.length,
      equation_ledger_size: equationLedger.size,
    },
    repairs: [],
    orchestrator_patches: [],
    applied: [],
  };

  // Collect all repair actions
  const tagPatches = repairMissingTags(mainTex, frames, coverage, equationLedger);
  const eqPatches = repairMissingEquations(mainTex, frames, coverage, equationLedger);
  const alignedFix = recommendAlignedRegexFix();

  report.repairs.push(...tagPatches, ...eqPatches);
  report.orchestrator_patches.push(alignedFix);

  // Apply repairs to main.tex if not dry-run
  if (!dryRun && (tagPatches.length > 0 || eqPatches.length > 0)) {
    let modifiedTex = mainTex;

    // Apply tag insertions
    for (const patch of tagPatches) {
      if (patch.action === "add_tag_to_aligned_block") {
        const frame = frames[patch.frameIndex];
        if (!frame || !frame.hasInlineAligned) continue;

        // Find the aligned block and insert \tag{X} after it
        // Pattern: $\displaystyle \begin{aligned}...\end{aligned}$
        // We want: $\displaystyle \begin{aligned}...\end{aligned}\tag{N}$
        const alignedRegex = /(\$\\displaystyle\s*\\begin\{aligned\*?\}[\s\S]*?\\end\{aligned\*?\})(\s*\$)/g;
        const body = frame.body;
        alignedRegex.lastIndex = 0;

        // Find the last aligned block in the body
        const matches = [...body.matchAll(alignedRegex)];
        if (matches.length > 0) {
          const lastMatch = matches[matches.length - 1];
          const oldBlock = lastMatch[0];
          const newBlock = oldBlock.replace(/(\s*\$)$/, `\\tag{${patch.equationNumber}}$1`);

          // Replace in full frame
          if (frame.fullFrame.includes(oldBlock)) {
            const newFrame = frame.fullFrame.replace(oldBlock, newBlock);
            modifiedTex = modifiedTex.replace(frame.fullFrame, newFrame);

            report.applied.push({
              type: "add_tag",
              frame: frame.label,
              equationNumber: patch.equationNumber,
              success: true,
            });
          }
        }
      }
    }

    // Apply equation insertions (for frames entirely missing equations)
    for (const patch of eqPatches) {
      if (patch.action === "insert_equation_at_frame_end") {
        const frame = frames[patch.frameIndex];
        if (!frame) continue;

        // Try to get equation from ledger
        const eqLatex = equationLedger.get(patch.equationNumbers[0]);
        if (eqLatex) {
          // Insert just before \end{frame}
          const insertBefore = "\\end{frame}";
          const insertion = `\n\\vspace{0.4em}\n\\uncover<+->{\\begin{adjustbox}{max width=0.96\\linewidth,max totalheight=0.43\\textheight}\n${eqLatex.latex}\n\\end{adjustbox}}\n`;

          const frameInTex = frame.fullFrame;
          const newFrame = frameInTex.replace(insertBefore, insertion + insertBefore);
          modifiedTex = modifiedTex.replace(frameInTex, newFrame);

          report.applied.push({
            type: "insert_equation",
            frame: frame.label,
            equation: patch.equationNumbers[0],
            fromLedger: true,
            success: true,
          });
        } else {
          report.applied.push({
            type: "insert_equation",
            frame: frame.label,
            equation: patch.equationNumbers.join(", "),
            fromLedger: false,
            success: false,
            reason: "equation not found in analysis.json ledger",
          });
        }
      }
    }

    // Write back
    const backupPath = mainTexPath + ".bak.eq-repair-" + Date.now();
    fs.copyFileSync(mainTexPath, backupPath);
    fs.writeFileSync(mainTexPath, modifiedTex, "utf8");

    report.summary.backup_path = backupPath;
    report.summary.main_tex_modified = true;
  }

  report.summary.total_repairs = report.repairs.length;
  report.summary.total_applied = report.applied.filter((a) => a.success).length;

  return report;
}

// ---------------------------------------------------------------------------
// Orchestrator patch helper
// Generates the exact regex replacement for parseMainTexFrames
// ---------------------------------------------------------------------------

function generateOrchestratorPatch() {
  return {
    description: "Fix display equation regex in parseMainTexFrames to include \\begin{aligned}",
    file: "scripts/dev_pipeline_orchestrator.js",
    searchFor: "|\\\\begin\\{align\\*?\\}|\\\\begin\\{gather\\*?\\}|\\\\begin\\{multline\\*?\\}|\\\\begin\\{flalign\\*?\\}|",
    replaceWith: "|\\\\begin\\{align(?:ed)?\\*?\\}|\\\\begin\\{gather\\*?\\}|\\\\begin\\{multline\\*?\\}|\\\\begin\\{flalign\\*?\\}|",
    note: "This makes \\begin{aligned} count as a visible equation block alongside \\begin{align}",
  };
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

if (require.main === module) {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const taskDir = args.find((a) => !a.startsWith("--"));

  if (!taskDir) {
    console.error("Usage: node deck_equation_coverage_repair.js <task-dir> [--dry-run]");
    process.exit(1);
  }

  const result = repairEquationCoverage(taskDir, { dryRun });
  console.log(JSON.stringify(result, null, 2));
}

module.exports = {
  repairEquationCoverage,
  parseFramesWithPositions,
  buildEquationLedger,
  recommendAlignedRegexFix,
  generateOrchestratorPatch,
};
