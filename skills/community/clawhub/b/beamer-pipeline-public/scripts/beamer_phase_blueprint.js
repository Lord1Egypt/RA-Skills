"use strict";

const DECK_PIPELINE_PHASE_BLUEPRINTS = Object.freeze([
  {
    name: "analysis",
    title: "分析",
    goal: "建立 analysis.json，并补齐 paragraph_ledger / figure / table / equation / notation / formal statement 等源侧盘点基线。",
    requiredArtifacts: ["analysis.json"],
    reviewerPhase: false,
    finalPhase: false,
  },
  {
    name: "slides_outline_skeleton",
    title: "slides 大纲 / skeleton",
    goal: "生成 slides.json，明确路线图、结论预告、正文/附录拆分与逐页 skeleton；equation_coverage / notation_coverage 在本阶段可先保留 planned 占位。",
    requiredArtifacts: ["analysis.json", "slides.json"],
    reviewerPhase: true,
    finalPhase: false,
  },
  {
    name: "equation_coverage",
    title: "公式覆盖",
    goal: "把 equation_coverage 真正落到 slide/frame 映射与解释上，不再保留 planned/blocked/missing/partial 占位。",
    requiredArtifacts: ["analysis.json", "slides.json"],
    reviewerPhase: true,
    finalPhase: false,
  },
  {
    name: "notation_consistency",
    title: "记号 / 一致性",
    goal: "补齐 notation_coverage，并修正符号首现定义、先定义后使用与跨页一致性问题。",
    requiredArtifacts: ["analysis.json", "slides.json"],
    reviewerPhase: true,
    finalPhase: false,
  },
  {
    name: "compile_and_structural_repair",
    title: "编译与结构修复",
    goal: "生成主工件并完成编译、结构、版式与渲染保真修补。",
    requiredArtifacts: ["analysis.json", "slides.json", "main.tex", "main.pdf"],
    reviewerPhase: true,
    finalPhase: false,
  },
  {
    name: "review_and_auto_rework",
    title: "reviewer 审核与自动返工",
    goal: "把 reviewer 打回转成 repair tickets，自动返工直到 reviewer 放行。",
    requiredArtifacts: ["analysis.json", "slides.json", "main.tex", "main.pdf"],
    reviewerPhase: true,
    finalPhase: false,
  },
  {
    name: "final_acceptance_delivery",
    title: "终验与交付",
    goal: "补齐最终结构化验收字段，跑 tester / 终验，并交付 ready_for_review=true 的最终结果。",
    requiredArtifacts: ["analysis.json", "slides.json", "main.tex", "main.pdf", "README.md", "asset_manifest.json", "figures"],
    reviewerPhase: false,
    finalPhase: true,
  },
]);

const DECK_PIPELINE_TOTAL_PHASES = DECK_PIPELINE_PHASE_BLUEPRINTS.length;
const DECK_PIPELINE_PHASE_INDEX = Object.freeze(DECK_PIPELINE_PHASE_BLUEPRINTS.reduce((acc, spec, index) => {
  acc[spec.name] = index + 1;
  return acc;
}, {}));

function getBeamerPipelinePhase(round) {
  const normalizedRound = Math.min(Math.max(Number(round || 1), 1), DECK_PIPELINE_TOTAL_PHASES);
  const spec = DECK_PIPELINE_PHASE_BLUEPRINTS[normalizedRound - 1];
  return {
    ...spec,
    index: normalizedRound,
    total: DECK_PIPELINE_TOTAL_PHASES,
    mode: "beamer",
    finalArtifact: "main.tex",
  };
}

function summarizePhase(phase) {
  if (!phase) return "";
  return `第 ${phase.index}/${phase.total} 阶段：${phase.title}`;
}

function phaseAllowsPlannedCoverageField(phase, fieldName) {
  const phaseIndex = Number(phase?.index || 0) || 0;
  if (!phase || phase.finalPhase === true || phaseIndex <= 0) return false;
  const lastPlanningPhaseIndex = fieldName === "equation_coverage"
    ? DECK_PIPELINE_PHASE_INDEX.slides_outline_skeleton
    : (fieldName === "notation_coverage"
      ? DECK_PIPELINE_PHASE_INDEX.equation_coverage
      : DECK_PIPELINE_PHASE_INDEX.analysis);
  return phaseIndex <= lastPlanningPhaseIndex;
}

function requiredArtifactNamesForPhase(phase) {
  return Array.isArray(phase?.requiredArtifacts) ? [...phase.requiredArtifacts] : [];
}

module.exports = {
  DECK_PIPELINE_PHASE_BLUEPRINTS,
  DECK_PIPELINE_TOTAL_PHASES,
  DECK_PIPELINE_PHASE_INDEX,
  getBeamerPipelinePhase,
  phaseAllowsPlannedCoverageField,
  requiredArtifactNamesForPhase,
  summarizePhase,
};
