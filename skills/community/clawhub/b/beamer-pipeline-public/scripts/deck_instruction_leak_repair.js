#!/usr/bin/env node
/**
 * deck_instruction_leak_repair.js — Deterministic instruction-leak repair
 *
 * Strips LLM thinking/instruction patterns that leak into Beamer frame prose.
 * These are patterns like "完整保留图X图片", "这页共同保证...不被摘要替代",
 * "图示完整保留，讲解时先读坐标轴..." etc.
 *
 * Usage:
 *   node deck_instruction_leak_repair.js <output-directory>          # fix (default)
 *   node deck_instruction_leak_repair.js <output-directory> --check  # check only
 *   node deck_instruction_leak_repair.js <output-directory> --dry-run # report without writing
 */

"use strict";

const fs = require("node:fs");
const path = require("node:path");

// ─── Pattern definitions ────────────────────────────────────────────────────

/**
 * Each rule: { name, regex, action, note }
 * action: "delete-line" | "delete-block" | "unwrap" (keep content after separator)
 * regex is applied per-line against a frame's inner body.
 */
const RULES = [
  // [A] "完整保留 X 图片/表 X" — delete the whole bullet line
  {
    name: "baoliu-bullet",
    regex: /^\s*\\item\s+完整保留\s*(图|表|附录)\s*[0-9A-Za-z一二三四五六七八九十]*(图片|表格)?\s*$/,
    action: "delete-line",
    note: "完整保留图/表/附录的指令行",
  },
  // [A-ext] "完整保留 ... 不以摘要替代"
  {
    name: "baoliu-no-summary",
    regex: /^\s*\\item\s.*完整保留.*不以摘要替代\s*$/,
    action: "delete-line",
    note: "完整保留+不以摘要替代",
  },
  // [A-ext2] "完整保留 ... ODE" / "完整保留 ... PDE"
  {
    name: "baoliu-equation-system",
    regex: /^\s*\\item\s+完整保留.*(ODE|PDE|指数仿射|指数二次)\s*$/,
    action: "delete-line",
    note: "完整保留方程系统/猜测式",
  },
  // [A-ext3] Broad catch: any \item starting with "完整保留"
  {
    name: "baoliu-generic",
    regex: /^\s*\\item\s+完整保留/,
    action: "delete-line",
    note: "通用完整保留行",
  },
  // [B] "这页…共同保证…不被摘要替代"
  {
    name: "gongtong-baozheng",
    regex: /^\s*\\item\s+这页.*共同保证.*不被摘要替代\s*$/,
    action: "delete-line",
    note: "共同保证不被摘要替代",
  },
  // [C] "该页用于…不和…混合"
  {
    name: "gaiye-yongyu",
    regex: /^\s*\\item\s+该页用于.*(不和|不参与|不涉及)/,
    action: "delete-line",
    note: "该页用于公式验证/说明",
  },
  // [D] "\small 图示完整保留，讲解时…"
  {
    name: "tushi-small",
    regex: /^\s*\\small\s+图示完整保留.*讲解时/,
    action: "delete-line",
    note: "图示完整保留讲解提示",
  },
  // [D-ext] Similar small-text instruction notes
  {
    name: "tushi-small-2",
    regex: /^\s*\\small\s+读图重点/,
    action: "delete-line",
    note: "small 读图重点行",
  },
  // [E] "读图/读表重点：" — unwrap (keep content after colon)
  {
    name: "du-tu-zhongdian",
    regex: /^\s*\\item\s+读[图表]重点[：:]\s*(.+)/,
    action: "unwrap",
    replacement: "\\item $1",
    note: "读图/读表重点：保留内容",
  },
  // [E-2] "读图时/读表时/读图要/读表要" — delete presenter cues
  {
    name: "du-tu-biao-cue",
    regex: /^\s*\\item\s*读[图表](?:时|要|的)/u,
    action: "delete-line",
    note: "读图/读表时/要的讲解提示",
  },
  // [F] "这里先定义记号，后续…"
  {
    name: "zheli-xian-dingyi",
    regex: /^\s*\\item\s+这里先定义记号.*后续/,
    action: "delete-line",
    note: "这里先定义记号",
  },
  // [G] "这页/该页/本页 …" — page-level meta-instructions for slide authors
  {
    name: "gaiye-meta",
    regex: /^\s*\\item\s+(?:这页|该页|本页)/u,
    action: "delete-line",
    note: "这页/该页/本页元指令",
  },
  // [H] "后续连续公式页拆分…避免压缩…" — planning notes
  {
    name: "planning-split",
    regex: /^\s*\\item\s+后续.*(?:连续.*(?:公式|页)|拆分.*页|避免.*(?:压缩|省略|删除|隐藏))/u,
    action: "delete-line",
    note: "后续页拆分/压缩规划说明",
  },
];

// ─── Core logic ──────────────────────────────────────────────────────────────

/**
 * Process a list of lines representing the content BETWEEN \begin{frame} and \end{frame}.
 * Returns { lines, removed: [{lineIndex, rule, original}] }
 */
function processFrameBody(lines) {
  const result = { lines: [], removed: [] };

  for (let i = 0; i < lines.length; i++) {
    const original = lines[i];
    let matched = false;

    for (const rule of RULES) {
      const m = original.match(rule.regex);
      if (!m) continue;

      if (rule.action === "delete-line") {
        result.removed.push({ lineIndex: i, rule: rule.name, original: original.trim() });
        matched = true;
        break;
      }

      if (rule.action === "unwrap" && rule.replacement) {
        const replacement = rule.replacement.replace(/\$1/g, (m[1] || "").trim());
        result.lines.push(replacement);
        result.removed.push({
          lineIndex: i,
          rule: rule.name,
          original: original.trim(),
          replaced: replacement.trim(),
        });
        matched = true;
        break;
      }
    }

    if (!matched) {
      result.lines.push(original);
    }
  }

  return result;
}

/**
 * Scan and optionally repair instruction leaks in main.tex.
 */
function repairInstructionLeaks(outputDirectory, options = {}) {
  const dryRun = options.dryRun !== false;
  const mainPath = path.join(outputDirectory, "main.tex");

  const report = {
    summary: {
      output_directory: outputDirectory,
      dry_run: dryRun,
      main_tex_modified: false,
      total_removed: 0,
      rules_hit: {},
    },
    details: [],
  };

  if (!fs.existsSync(mainPath)) {
    report.summary.error = "main.tex not found";
    return report;
  }

  const original = fs.readFileSync(mainPath, "utf8");

  // Process frame by frame
  const framePattern = /\\begin\{frame\}[\s\S]*?\\end\{frame\}/g;
  const processed = original.replace(framePattern, (frameBlock) => {
    const lines = frameBlock.split("\n");
    const bodyLines = [];
    let inFrame = false;
    let frameHeader = "";
    let frameFooter = "";

    // Split into header, body, footer
    const headerIdx = lines.findIndex((l) => /\\begin\{frame\}/.test(l));
    const footerIdx = lines.findIndex((l, i) => i > headerIdx && /\\end\{frame\}/.test(l));

    if (headerIdx < 0) return frameBlock;

    frameHeader = lines.slice(0, headerIdx + 1).join("\n");

    if (footerIdx > headerIdx) {
      frameFooter = "\n" + lines.slice(footerIdx).join("\n");
    }

    bodyLines.length = 0;
    for (let i = headerIdx + 1; i < (footerIdx > headerIdx ? footerIdx : lines.length); i++) {
      bodyLines.push(lines[i]);
    }

    const result = processFrameBody(bodyLines);

    // Record details
    if (result.removed.length > 0) {
      report.details.push({
        frame_header: lines[headerIdx]?.trim().slice(0, 120),
        removed: result.removed,
      });
      for (const r of result.removed) {
        report.summary.rules_hit[r.rule] = (report.summary.rules_hit[r.rule] || 0) + 1;
        report.summary.total_removed++;
      }
    }

    if (result.removed.length === 0) return frameBlock;

    // Reconstruct frame
    const newBody = result.lines.join("\n");
    return frameHeader + "\n" + newBody + frameFooter;
  });

  if (report.summary.total_removed > 0 && !dryRun) {
    fs.writeFileSync(mainPath, processed, "utf8");
    report.summary.main_tex_modified = true;
  }

  return report;
}

/**
 * Generate a patch description for the orchestrator.
 * Returns a flat object the orchestrator can use to write checkpoint notes.
 */
function generateOrchestratorPatch(report) {
  return {
    instruction_leak_repair: {
      applied: report.summary.total_removed > 0 && report.summary.main_tex_modified,
      total_removed: report.summary.total_removed,
      rules_hit: report.summary.rules_hit,
      dry_run: report.summary.dry_run,
    },
  };
}

// ─── CLI ─────────────────────────────────────────────────────────────────────

if (require.main === module) {
  const args = process.argv.slice(2);
  const checkMode = args.includes("--check");
  const dryRun = args.includes("--dry-run") || (process.env.DRY_RUN === "true");
  const outputDir = args.find((a) => !a.startsWith("--"));

  if (!outputDir) {
    console.error("Usage: deck_instruction_leak_repair.js <output-directory> [--check] [--dry-run]");
    process.exit(1);
  }

  const options = {
    dryRun: checkMode || dryRun,
  };

  const report = repairInstructionLeaks(outputDir, options);

  if (checkMode) {
    console.log(JSON.stringify(report, null, 2));
  } else if (dryRun) {
    console.log("[DRY RUN] Would remove", report.summary.total_removed, "instruction-leak lines");
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log("Removed", report.summary.total_removed, "instruction-leak lines");
    if (report.summary.total_removed > 0) {
      console.log("Rules hit:", JSON.stringify(report.summary.rules_hit));
    }
  }

  process.exit(0);
}

module.exports = { repairInstructionLeaks, generateOrchestratorPatch };
