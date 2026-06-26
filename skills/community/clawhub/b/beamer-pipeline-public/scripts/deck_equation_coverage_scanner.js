#!/usr/bin/env node
/**
 * deck_equation_coverage_scanner.js
 *
 * Cross-file diagnostic for equation coverage in Beamer deck pipelines.
 * Maps equation_coverage entries from slides.json / analysis.json against
 * actual visible content in main.tex Beamer frames.
 *
 * Usage:
 *   node scripts/deck_equation_coverage_scanner.js <task-dir>
 *
 * Output: JSON matrix of equation → slide → frame diagnostics.
 */

"use strict";

const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Helpers (replicated from dev_pipeline_orchestrator.js to keep scanner standalone)
// ---------------------------------------------------------------------------

function isPlainObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function uniqueStrings(values) {
  return Array.from(new Set((Array.isArray(values) ? values : []).map(String).filter(Boolean)));
}

function readJsonFile(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// LaTeX token helpers
// ---------------------------------------------------------------------------

function readBalancedTexGroup(source, startIndex, open, close) {
  let depth = 0;
  let i = startIndex;
  while (i < source.length) {
    const ch = source[i];
    if (ch === open) { depth++; }
    else if (ch === close) {
      depth--;
      if (depth === 0) {
        return { value: source.slice(startIndex + 1, i), endIndex: i + 1 };
      }
    }
    i++;
  }
  return null;
}

// ---------------------------------------------------------------------------
// Equation number helpers
// ---------------------------------------------------------------------------

function extractEquationNumbersFromText(text) {
  const numbers = [];
  const source = String(text || "");
  // Match patterns: 2.1, A.1, B.2, (2.1), Eq. (2.1), etc.
  for (const match of source.matchAll(/(?:Eqs?\.?\s*)?\(?(\d+)\.(\d+)\)?/g)) {
    numbers.push(`${match[1]}.${match[2]}`);
  }
  // Also match appendix: A.1, B.2
  for (const match of source.matchAll(/\b([A-Z])\.(\d+)\b/g)) {
    // Skip if already captured as num.num
    numbers.push(`${match[1]}.${match[2]}`);
  }
  // Single numbers: 15, 16, etc.
  for (const match of source.matchAll(/(?:^|[^\d.])(\d{1,3})(?:[^\d.]|$)/g)) {
    const num = match[1];
    if (!numbers.includes(num) && !source.includes(`Eq. (${num})`) && !source.includes(`(${num}.`)) {
      // Only add standalone numbers if they appear as tagged equations
    }
  }
  return Array.from(new Set(numbers));
}

function equationKeysFromValues(numbers) {
  return (Array.isArray(numbers) ? numbers : []).map(String).filter(Boolean);
}

// ---------------------------------------------------------------------------
// Frame parsing (replicating parseMainTexFrames from orchestrator)
// ---------------------------------------------------------------------------

const DISPLAY_EQ_RE = /\\eqs?\{|\\begin\{equation\*?\}|\\begin\{align(?:ed)?\*?\}|\\begin\{gather\*?\}|\\begin\{multline\*?\}|\\begin\{flalign\*?\}|\\\[/g;
const TAG_RE = /\\tag\{([^}]+)\}/g;
const BEGIN_FRAME_RE = /\\begin\{frame\}/;
const END_FRAME_RE = /\\end\{frame\}/;

function normalizeFrameLabel(value) {
  return String(value || "").trim().toLowerCase();
}

function extractFrameLabelFromOptions(optionText) {
  const raw = String(optionText || "").trim();
  if (!raw) return "";
  const match = raw.match(/(?:^|,)\s*label\s*=\s*([^,\]]+)/i);
  return match ? match[1].trim() : "";
}

function frameTaggedEquationKeys(body) {
  const keys = [];
  const source = String(body || "");
  TAG_RE.lastIndex = 0;
  for (const match of source.matchAll(TAG_RE)) {
    const tagContent = String(match[1] || "").trim();
    const extracted = extractEquationNumbersFromText(tagContent);
    if (extracted.length > 0) {
      keys.push(...extracted);
    }
    if (/^\d+$/.test(tagContent)) {
      keys.push(tagContent);
    }
    const appendixMatch = tagContent.match(/^A0*([1-9]\d*)$/i);
    if (appendixMatch) {
      keys.push(`A${Number(appendixMatch[1])}`);
    }
  }
  return Array.from(new Set(keys));
}

function parseMainTexFrames(tex) {
  const frames = [];
  const source = String(tex || "");
  const beginMarker = "\\begin{frame}";
  const endMarker = "\\end{frame}";
  let cursor = 0;

  while (cursor < source.length) {
    const beginIndex = source.indexOf(beginMarker, cursor);
    if (beginIndex === -1) break;
    let headerIndex = beginIndex + beginMarker.length;
    while (/\s/.test(source[headerIndex] || "")) headerIndex++;

    if (source[headerIndex] === "<") {
      const grp = readBalancedTexGroup(source, headerIndex, "<", ">");
      if (grp) headerIndex = grp.endIndex;
      while (/\s/.test(source[headerIndex] || "")) headerIndex++;
    }
    let optionText = "";
    if (source[headerIndex] === "[") {
      const grp = readBalancedTexGroup(source, headerIndex, "[", "]");
      if (grp) {
        optionText = grp.value;
        headerIndex = grp.endIndex;
        while (/\s/.test(source[headerIndex] || "")) headerIndex++;
      }
    }
    let title = "";
    if (source[headerIndex] === "{") {
      const grp = readBalancedTexGroup(source, headerIndex, "{", "}");
      if (grp) {
        title = grp.value;
        headerIndex = grp.endIndex;
      }
    }

    const endIndex = source.indexOf(endMarker, headerIndex);
    if (endIndex === -1) break;
    const body = source.slice(headerIndex, endIndex);

    DISPLAY_EQ_RE.lastIndex = 0;
    const displayEquationCount = (body.match(DISPLAY_EQ_RE) || []).length;
    const taggedEquationKeys = frameTaggedEquationKeys(body);
    const taggedEquationCount = taggedEquationKeys.length;
    const visibleEquationSignalCount = Math.max(displayEquationCount, taggedEquationCount);

    const frameFull = source.slice(beginIndex, endIndex + endMarker.length);
    const label = extractFrameLabelFromOptions(optionText);

    // Find \begin{aligned} specifically (not counted by displayEq regex)
    const alignedCount = (body.match(/\\begin\{aligned\*?\}/g) || []).length;
    // Find inline display-style math: $\displaystyle ... \tag{X}$
    const inlineDisplayMathWithTag = (body.match(/\$\\displaystyle.+?\\tag\{[^}]+\}.+?\$/gs) || []).length;
    // Detect equations using \begin{aligned} inside $...$ pattern
    const inlineAlignedEq = /(?<!\\)\$(?:\\displaystyle\s*)?\\begin\{aligned\*?\}/.test(body);

    frames.push({
      index: frames.length,
      label,
      title: title.slice(0, 80),
      displayEquationCount,
      taggedEquationCount,
      taggedEquationKeys,
      visibleEquationSignalCount,
      alignedCount,
      inlineDisplayMathWithTag,
      inlineAlignedEq,
      bodyLength: body.length,
      bodyPreview: body.slice(0, 200).replace(/\s+/g, " "),
    });

    cursor = endIndex + endMarker.length;
  }
  return frames;
}

// ---------------------------------------------------------------------------
// Slide helpers
// ---------------------------------------------------------------------------

function slideIdFromPlan(slide) {
  return String(slide?.slide_id ?? slide?.id ?? "").trim();
}

function equationBlocksFromSlide(slide) {
  if (!isPlainObject(slide)) return [];
  // Check slide.equation_blocks
  const direct = Array.isArray(slide.equation_blocks) ? slide.equation_blocks : [];
  if (direct.length > 0) return direct;
  // Check blocks[].equation_blocks or blocks with type=equation
  const blocks = Array.isArray(slide.blocks) ? slide.blocks : [];
  return blocks.filter((b) => {
    if (!isPlainObject(b)) return false;
    const type = String(b.type || "").toLowerCase();
    return type === "equation" || type === "equation_block" || type === "math";
  });
}

// ---------------------------------------------------------------------------
// Equation coverage normalization
// ---------------------------------------------------------------------------

function canonicalizeEquationCoverageEntries(rawCoverage) {
  if (!Array.isArray(rawCoverage)) return [];
  return rawCoverage.map((entry) => {
    if (!isPlainObject(entry)) return entry;
    const sourceLabel = entry.source_label || entry.label || "";
    const numbers = entry.equation_numbers || entry.numbers || entry.equations || [];
    const slideIds = entry.slide_ids || [entry.slide_id].filter(Boolean);
    const status = entry.status || "covered";
    const sourceParagraphIds = entry.source_paragraph_ids || [];
    return {
      source_label: String(sourceLabel).trim(),
      equation_numbers: Array.isArray(numbers) ? numbers.map(String) : [String(numbers)],
      slide_ids: Array.isArray(slideIds) ? slideIds.map(String).filter(Boolean) : [],
      status: String(status).trim().toLowerCase(),
      source_paragraph_ids: Array.isArray(sourceParagraphIds) ? sourceParagraphIds.map(String) : [],
      coverage_stage: entry.coverage_stage || "",
      notes: entry.notes || "",
    };
  });
}

// ---------------------------------------------------------------------------
// Frame lookup (matching frame label → slide_id)
// ---------------------------------------------------------------------------

function buildFrameLookup(frames) {
  const byLabel = new Map();
  for (const frame of frames) {
    if (!isPlainObject(frame)) continue;
    const labels = [frame.label].filter(Boolean);
    for (const label of labels) {
      const key = normalizeFrameLabel(label);
      if (key && !byLabel.has(key)) {
        byLabel.set(key, frame);
      }
    }
  }
  return { frames, byLabel };
}

// ---------------------------------------------------------------------------
// Main scanner logic
// ---------------------------------------------------------------------------

function scanEquationCoverage(taskDir) {
  const analysisPath = path.join(taskDir, "analysis.json");
  const slidesPath = path.join(taskDir, "slides.json");
  const mainTexPath = path.join(taskDir, "main.tex");

  const analysis = readJsonFile(analysisPath);
  const slidesDoc = readJsonFile(slidesPath);
  const tex = fs.existsSync(mainTexPath) ? fs.readFileSync(mainTexPath, "utf8") : null;

  const report = {
    task_dir: taskDir,
    files: {
      "analysis.json": !!analysis,
      "slides.json": !!slidesDoc,
      "main.tex": !!tex,
    },
    summary: {},
    frames: [],
    coverage_entries: [],
    diagnostics: [],
  };

  // Parse main.tex frames
  if (tex) {
    report.frames = parseMainTexFrames(tex);
  }

  const frameLookup = buildFrameLookup(report.frames);

  // Collect equation_coverage from both sources
  const slidesEqCov = Array.isArray(slidesDoc?.equation_coverage) ? slidesDoc.equation_coverage : [];
  const analysisEqCov = Array.isArray(analysis?.equation_coverage) ? analysis.equation_coverage : [];
  const rawCoverage = slidesEqCov.length > 0 ? slidesEqCov : analysisEqCov;
  const coverage = canonicalizeEquationCoverageEntries(rawCoverage);

  // Build slide index
  const slides = Array.isArray(slidesDoc?.slides) ? slidesDoc.slides :
    (Array.isArray(slidesDoc?.slide_plan) ? slidesDoc.slide_plan : []);
  const slideIndex = new Map();
  for (const slide of slides) {
    const sid = slideIdFromPlan(slide);
    if (sid) slideIndex.set(normalizeFrameLabel(sid), slide);
  }

  // Analyze each coverage entry
  const totalEntries = coverage.length;
  let missingFrames = 0;
  let missingTags = 0;
  let missingBlocks = 0;
  let displayEqZero = 0;
  let inlineAlignedCount = 0;
  const equationIssues = [];

  for (const entry of coverage) {
    const status = entry.status;
    if (!["covered", "covered_with_ocr_gap_note", "inline_integrated", "standalone_supplement", "partial"].includes(status)) continue;

    const label = entry.source_label;
    const numbers = entry.equation_numbers;
    const slideIds = entry.slide_ids;

    if (slideIds.length === 0) {
      equationIssues.push({
        label,
        issue: "no_slide_ids",
        detail: `equation_coverage marks ${label} as ${status} but has no slide_ids`,
      });
      continue;
    }

    for (const slideId of slideIds) {
      const normalized = normalizeFrameLabel(slideId);
      const frame = frameLookup.byLabel.get(normalized);
      const slide = slideIndex.get(normalized);

      const diag = {
        label,
        slide_id: slideId,
        status,
        equation_numbers: numbers,
        frame_found: !!frame,
        frame_index: frame ? frame.index : -1,
        frame_label: frame ? frame.label : null,
        frame_display_eq_count: frame ? frame.displayEquationCount : 0,
        frame_tagged_eq_count: frame ? frame.taggedEquationCount : 0,
        frame_tagged_keys: frame ? frame.taggedEquationKeys : [],
        frame_visible_eq_signal: frame ? frame.visibleEquationSignalCount : 0,
        frame_inline_aligned_eq: frame ? frame.inlineAlignedEq : false,
        frame_aligned_count: frame ? frame.alignedCount : 0,
        slide_has_equation_blocks: slide ? equationBlocksFromSlide(slide).length > 0 : false,
        slide_equation_block_count: slide ? equationBlocksFromSlide(slide).length : 0,
      };

      // Check for issues
      const issues = [];
      if (!frame) {
        issues.push("frame_not_found");
        missingFrames++;
      }
      if (frame && frame.visibleEquationSignalCount === 0) {
        issues.push("no_visible_equation_block");
        displayEqZero++;
      }
      if (frame && frame.displayEquationCount === 0 && frame.alignedCount > 0) {
        issues.push("uses_aligned_not_align");
        inlineAlignedCount++;
      }

      // Check tagged equation number matching. Normalize coverage labels such as
      // "Eq. (2.1)" into the same canonical keys used by \tag{2.1} parsing.
      if (frame && numbers.length > 0) {
        const frameKeys = new Set(frame.taggedEquationKeys.map(String));
        const missing = [];
        for (const rawNumber of numbers) {
          const canonical = extractEquationNumbersFromText(rawNumber);
          const candidates = canonical.length > 0 ? canonical : [String(rawNumber)];
          if (!candidates.some((candidate) => frameKeys.has(String(candidate)))) {
            missing.push(String(rawNumber));
          }
        }
        if (missing.length > 0) {
          issues.push(`missing_tags:${missing.join(",")}`);
          missingTags += missing.length;
        }
      }

      // Check slides.json equation_blocks
      if (slide && equationBlocksFromSlide(slide).length === 0 && numbers.length > 0 && frame && frame.alignedCount > 0) {
        issues.push("no_equation_blocks_in_slides_json");
        missingBlocks++;
      }

      diag.issues = issues;
      diag.recommended_action = recommendAction(diag);

      equationIssues.push(diag);
    }
  }

  // Summary
  report.summary = {
    total_coverage_entries: totalEntries,
    covered_entries_analyzed: equationIssues.length,
    frames_total: report.frames.length,
    frames_with_labels: report.frames.filter((f) => f.label).length,
    frames_with_visible_eq: report.frames.filter((f) => f.visibleEquationSignalCount > 0).length,
    frames_with_aligned: report.frames.filter((f) => f.alignedCount > 0).length,
    frames_with_inline_display_math_tag: report.frames.filter((f) => f.inlineDisplayMathWithTag > 0).length,
    issues: {
      missing_frames: missingFrames,
      display_eq_zero: displayEqZero,
      missing_tags: missingTags,
      missing_blocks_in_slides: missingBlocks,
      uses_aligned_not_align: inlineAlignedCount,
    },
  };

  report.diagnostics = equationIssues;

  return report;
}

function recommendAction(diag) {
  const issues = diag.issues || [];
  if (issues.includes("frame_not_found")) return "create_frame_for_slide";
  if (issues.includes("no_visible_equation_block") && diag.frame_inline_aligned_eq) {
    return "convert_inline_aligned_to_display_math";
  }
  if (issues.includes("no_visible_equation_block") && !diag.frame_found) {
    return "insert_equation_into_frame";
  }
  if (issues.some((i) => i.startsWith("missing_tags"))) {
    return diag.frame_aligned_count > 0
      ? "add_tag_to_existing_aligned_equation"
      : "insert_equation_with_tag_into_frame";
  }
  if (issues.includes("uses_aligned_not_align")) {
    return "change_aligned_to_align_or_add_to_validator_regex";
  }
  return "none";
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

if (require.main === module) {
  const taskDir = process.argv[2];
  if (!taskDir) {
    console.error("Usage: node deck_equation_coverage_scanner.js <task-dir>");
    process.exit(1);
  }
  const report = scanEquationCoverage(taskDir);
  console.log(JSON.stringify(report, null, 2));
}

module.exports = { scanEquationCoverage, parseMainTexFrames, canonicalizeEquationCoverageEntries };
