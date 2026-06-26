#!/usr/bin/env node
/**
 * deck_strategy_placeholder_repair.js — Fill planned/analysis_only/recovery
 * placeholders in overlay_strategy and audience_explanation_strategy with
 * conservative defaults.
 *
 * Usage:
 *   node deck_strategy_placeholder_repair.js <slides.json> [--dry-run]
 */

"use strict";

const fs = require("node:fs");
const path = require("node:path");

const UNRESOLVED_PATTERN = /^(planned|analysis_only|recovery|missing|blocked|partial)$/i;

function isPlainObject(v) { return Boolean(v) && typeof v === "object" && !Array.isArray(v); }

function hasUnresolvedStatus(value) {
  if (typeof value === "string") return UNRESOLVED_PATTERN.test(value.trim());
  if (isPlainObject(value)) return UNRESOLVED_PATTERN.test(String(value.status || "").trim());
  return false;
}

function classifySlide(slide, slides) {
  const slideId = String(slide?.slide_id || "");
  const title = String(slide?.title || "").toLowerCase();
  const subtitle = String(slide?.subtitle || "").toLowerCase();
  const desc = String(slide?.description || "").toLowerCase();
  const fullText = [title, subtitle, desc].join(" ");

  const eqBlocks = Array.isArray(slide?.equation_blocks) ? slide.equation_blocks : [];
  const hasDenseFormula = eqBlocks.length >= 2;
  const hasTheorem = /\b(theorem|定理|proposition|命题|lemma|引理|corollary|推论)\b/i.test(fullText);
  const hasNumerical = /(numerical|数值|calibrat|校准|parameter|参数|table|表格|implied|隐含|volatility|波动率)/i.test(fullText);
  const hasFigure = /(figure|fig|图|chart|plot)/i.test(fullText);
  const hasRisk = /(hedge|对冲|risk|风险|sensitiv|敏感度|greeks?)/i.test(fullText);
  const isMotivation = /(motivation|动机|introduct|简介|overview|概览|background|背景|literature|文献|framework|框架|problem|问题)/i.test(fullText);

  // Check if it's an appendix slide
  const isAppendix = /^s\D*[AB]\d*$/i.test(slideId) || /appendix|附录/i.test(fullText);

  // Count bullets
  const bullets = Array.isArray(slide?.bullets) ? slide.bullets : [];
  const bulletCount = bullets.length;

  let pageType = "content";
  if (isMotivation) pageType = "motivation";
  if (hasTheorem) pageType = "theorem";
  if (hasDenseFormula) pageType = "formula_dense";
  if (hasNumerical) pageType = "numerical";
  if (hasFigure && hasNumerical) pageType = "numerical_figure";
  if (isAppendix) pageType = "appendix";

  return {
    slideId,
    pageType,
    hasDenseFormula,
    hasTheorem,
    hasNumerical,
    hasFigure,
    bulletCount,
    equationCount: eqBlocks.length,
    isAppendix,
  };
}

function generateDefaultOverlayStrategy(slide, classification, slides) {
  const { pageType, hasDenseFormula, bulletCount, equationCount } = classification;

  // Conservative per-type defaults
  switch (pageType) {
    case "motivation":
      return {
        status: "covered",
        strategy: "sequential_reveal",
        overlay_count: Math.max(2, bulletCount),
        items: (slide?.bullets || []).slice(0, 5).map((_, i) => ({
          step: i + 1,
          action: "reveal",
          target: `bullet_${i + 1}`,
        })),
        rationale: "动机/背景页，逐条展开以控制观众注意力节奏",
        source: "deck_strategy_placeholder_repair (auto)",
      };

    case "theorem":
      return {
        status: "covered",
        strategy: "static_full",
        overlay_count: 0,
        items: [],
        rationale: "定理页为单次揭示可读性最优，不考虑overlay拆分",
        source: "deck_strategy_placeholder_repair (auto)",
      };

    case "formula_dense":
      return {
        status: "covered",
        strategy: "block_sequential",
        overlay_count: equationCount,
        items: Array.from({ length: equationCount }, (_, i) => ({
          step: i + 1,
          action: "reveal",
          target: `equation_block_${i + 1}`,
        })),
        rationale: "公式密集页逐块展开，每个equation block单独揭示以配合讲解节奏",
        source: "deck_strategy_placeholder_repair (auto)",
      };

    case "numerical":
    case "numerical_figure":
      return {
        status: "covered",
        strategy: "mixed_sequential",
        overlay_count: Math.max(2, bulletCount + equationCount),
        items: [],
        rationale: "数值结果页混合图和/或表格，按结果顺序逐组展示",
        source: "deck_strategy_placeholder_repair (auto)",
      };

    case "appendix":
      return {
        status: "covered",
        strategy: "static_full",
        overlay_count: 0,
        items: [],
        rationale: "附录页一般为一次性引用，无需动态overlay；若正文需要调用，用againframe",
        source: "deck_strategy_placeholder_repair (auto)",
      };

    default:
      if (bulletCount <= 3) {
        return {
          status: "covered",
          strategy: "static_full",
          overlay_count: 0,
          items: [],
          rationale: "要点少（≤3条），单页完整展示即可",
          source: "deck_strategy_placeholder_repair (auto)",
        };
      }
      return {
        status: "covered",
        strategy: "sequential_reveal",
        overlay_count: bulletCount,
        items: (slide?.bullets || []).slice(0, 6).map((_, i) => ({
          step: i + 1,
          action: "reveal",
          target: `bullet_${i + 1}`,
        })),
        rationale: "要点较多，逐条展开以控制信息密度",
        source: "deck_strategy_placeholder_repair (auto)",
      };
  }
}

function generateDefaultAudienceExplanationStrategy(slide, classification, slides) {
  const { pageType, hasDenseFormula, hasTheorem, hasNumerical, hasFigure, isAppendix } = classification;

  switch (pageType) {
    case "motivation":
      return {
        status: "covered",
        style: "question_driven",
        hook: "先抛出研究问题，再展开背景→方法→结论",
        technical_depth: "moderate",
        key_takeaway: "该页说明研究动机和已有文献缺口，听众应形成对研究方向的整体认知",
        source: "deck_strategy_placeholder_repair (auto)",
      };

    case "theorem":
      return {
        status: "covered",
        style: "result_first",
        hook: "先给出定理结论，再简要说明推导思路",
        technical_depth: "deep",
        key_takeaway: "定理本身为核心结果，推导细节可在讲解中跳过后在问答环节展开",
        source: "deck_strategy_placeholder_repair (auto)",
      };

    case "formula_dense":
      return {
        status: "covered",
        style: "step_by_step",
        hook: "逐项解释每个符号和结构的含义，避免听众迷失在符号堆里",
        technical_depth: "deep",
        key_takeaway: "每块公式应有至少一句中文自然语言解释，与symbol对照",
        source: "deck_strategy_placeholder_repair (auto)",
      };

    case "numerical":
    case "numerical_figure":
      return {
        status: "covered",
        style: "data_storytelling",
        hook: "先说明实验设置→展示结果→对比分析→结论",
        technical_depth: "moderate",
        key_takeaway: "数值结果是理论的有力佐证，听众应能自行对照表和图得出结论",
        source: "deck_strategy_placeholder_repair (auto)",
      };

    case "appendix":
      return {
        status: "covered",
        style: "reference_only",
        hook: "附录为补充内容，讲解时提及即可，不展开详细展示",
        technical_depth: "deep",
        key_takeaway: "附录为技术细节补充，不占用主报告时间",
        source: "deck_strategy_placeholder_repair (auto)",
      };

    default:
      return {
        status: "covered",
        style: "progressive_explanation",
        hook: "先概述该页核心信息，再逐条解释",
        technical_depth: "moderate",
        key_takeaway: "听众应能从该页中提取关键结论",
        source: "deck_strategy_placeholder_repair (auto)",
      };
  }
}

function repairStrategyPlaceholders(slidesPath, options = {}) {
  const dryRun = options.dryRun !== false;
  const report = {
    summary: {
      slides_path: slidesPath,
      dry_run: dryRun,
      overlay_fixed: 0,
      audience_fixed: 0,
      total_fixed: 0,
      slides_json_modified: false,
      details: [],
    },
  };

  if (!fs.existsSync(slidesPath)) {
    report.summary.error = "slides.json not found";
    return report;
  }

  let doc;
  try {
    doc = JSON.parse(fs.readFileSync(slidesPath, "utf8"));
  } catch (err) {
    report.summary.error = `parse_error: ${err.message}`;
    return report;
  }

  const slides = Array.isArray(doc.slides) ? doc.slides : [];
  if (slides.length === 0) {
    report.summary.error = "no slides in slides.json";
    return report;
  }

  for (const slide of slides) {
    if (!isPlainObject(slide)) continue;
    const slideId = String(slide.slide_id || "");

    // Fix overlay_strategy
    if (hasUnresolvedStatus(slide.overlay_strategy)) {
      const classification = classifySlide(slide, slides);
      const strategy = generateDefaultOverlayStrategy(slide, classification, slides);
      if (!dryRun) {
        slide.overlay_strategy = strategy;
      }
      report.summary.overlay_fixed++;
      report.summary.details.push({
        slide_id: slideId,
        field: "overlay_strategy",
        old_status: slide.overlay_strategy?.status || slide.overlay_strategy || "planned",
        new_status: strategy.status,
        page_type: classification.pageType,
      });
    }

    // Fix audience_explanation_strategy
    if (hasUnresolvedStatus(slide.audience_explanation_strategy)) {
      const classification = classifySlide(slide, slides);
      const strategy = generateDefaultAudienceExplanationStrategy(slide, classification, slides);
      if (!dryRun) {
        slide.audience_explanation_strategy = strategy;
      }
      report.summary.audience_fixed++;
      report.summary.details.push({
        slide_id: slideId,
        field: "audience_explanation_strategy",
        old_status: slide.audience_explanation_strategy?.status || slide.audience_explanation_strategy || "planned",
        new_status: strategy.status,
        page_type: classification.pageType,
      });
    }
  }

  report.summary.total_fixed = report.summary.overlay_fixed + report.summary.audience_fixed;

  if (!dryRun && report.summary.total_fixed > 0) {
    doc.strategy_placeholder_last_fixed_by = "deck_strategy_placeholder_repair";
    doc.strategy_placeholder_last_fixed_at = new Date().toISOString();
    fs.writeFileSync(slidesPath, JSON.stringify(doc, null, 2), "utf8");
    report.summary.slides_json_modified = true;
  }

  return report;
}

// ─── CLI ────────────────────────────────────────────────────────
function main() {
  const args = process.argv.slice(2);
  let dryRun = false;
  let targetPath = "";

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--dry-run") dryRun = true;
    else if (!args[i].startsWith("--")) targetPath = args[i];
  }

  if (!targetPath) {
    console.error("Usage: node deck_strategy_placeholder_repair.js <slides.json> [--dry-run]");
    process.exit(1);
  }

  if (!fs.existsSync(targetPath)) {
    console.error("File not found:", targetPath);
    process.exit(1);
  }

  const report = repairStrategyPlaceholders(targetPath, { dryRun });
  console.log(JSON.stringify(report, null, 2));
}

if (require.main === module) {
  main();
}

module.exports = { repairStrategyPlaceholders, classifySlide, UNRESOLVED_PATTERN };
