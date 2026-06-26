const STRUCTURED_FINAL_FIELDS = [
  {
    key: "compile_status",
    description: "structured compile outcome with status, main_pdf_generated, command/logs, and blocker_or_warning_summary",
  },
  {
    key: "readability_status",
    description: "structured readability outcome with overfull_warning_count, severity, and why the deck is or is not reviewable",
  },
  {
    key: "tex_warnings",
    description: "structured raw TeX warning inventory, including tex_warnings.overfull_boxes[] entries from compile logs",
  },
  {
    key: "layout_policy",
    description: "structured layout policy outcome, including layout_policy.overfull_assessment severity and gate decision",
  },
  {
    key: "visible_prose_recovery_hint",
    description: "non-gating recovery hint that may be partial or sampled while the final visible prose audit is still pending",
  },
  {
    key: "visible_prose_fidelity_final",
    description: "structured full-deck audit that checks whether slides.json visible explanatory prose remains visibly present in the rendered deck",
  },
  {
    key: "render_fidelity_safeguards",
    description: "structured list/object describing the concrete safeguards used to prevent scaffold-only or prose-loss regressions",
  },
];

const PPT_STRUCTURED_FINAL_FIELDS = [
  {
    key: "render_status",
    description: "structured PPT renderer outcome with status, main_pptx_generated, command/logs, and blocker_or_warning_summary",
  },
  {
    key: "validation_status",
    description: "structured pptx_validation.json outcome with ok/fatal/warning counts and report path",
  },
  {
    key: "pptx_warnings",
    description: "structured PPT validator warning inventory, including issues[] or warning_count plus summary",
  },
  {
    key: "layout_policy",
    description: "structured layout policy outcome, including layout_policy.overfull_assessment severity and gate decision",
  },
  {
    key: "visible_prose_recovery_hint",
    description: "non-gating recovery hint that may be partial or sampled while the final visible prose audit is still pending",
  },
  {
    key: "visible_prose_fidelity_final",
    description: "structured full-deck audit that checks whether slides.json visible explanatory prose remains visibly present in the rendered PPT deck",
  },
  {
    key: "render_fidelity_safeguards",
    description: "structured list/object describing the concrete safeguards used to prevent scaffold-only, prose-loss, or renderer regressions",
  },
];

function isPlainObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isNonEmptyStructuredValue(value) {
  if (isNonEmptyString(value)) return true;
  if (Array.isArray(value)) return value.length > 0;
  if (isPlainObject(value)) return Object.keys(value).length > 0;
  return false;
}

function firstNonEmptyString(...values) {
  return values.find((value) => isNonEmptyString(value)) || "";
}

function structuredCompileStatusValid(value) {
  if (isNonEmptyString(value)) return true;
  if (!isPlainObject(value)) return false;
  const status = String(value.status || "").trim().toLowerCase();
  const validStatuses = ["compiled", "compiled_with_warnings", "blocked", "failed", "partial", "pass", "success", "succeeded", "ok", "done", "warning"];
  if (!validStatuses.includes(status)) return false;
  if (typeof value.main_pdf_generated !== "boolean") return false;
  const commandOk = isNonEmptyString(value.command) || isNonEmptyString(value.compile_command);
  const explanationOk = isNonEmptyString(value.blocker_or_warning_summary)
    || isNonEmptyString(value.summary)
    || isNonEmptyString(value.warning_summary)
    || isNonEmptyString(value.notes);
  return commandOk && explanationOk;
}

function structuredReadabilityStatusValid(value) {
  if (isNonEmptyString(value)) return true;
  if (!isPlainObject(value)) return false;
  const severity = String(value.severity || value.status || "").trim().toLowerCase();
  const validSeverities = ["none", "ok", "pass", "reviewable", "warning", "minor", "moderate", "severe", "blocked", "fail"];
  if (!validSeverities.includes(severity)) return false;
  const explanationOk = isNonEmptyString(firstNonEmptyString(
    value.summary,
    value.reason,
    value.why,
    value.why_reviewable,
    value.why_not_blocked,
    value.layout_outcome,
    value.assessment,
    value.notes,
    value.justification,
    value.gate_effect
  ));
  return explanationOk;
}

function structuredVisibleProseFidelityValid(value) {
  if (!isPlainObject(value)) return false;
  const status = String(value.status || "").trim().toLowerCase();
  const validStatuses = ["pass", "warning", "fail"];
  if (!validStatuses.includes(status)) return false;
  if (!Array.isArray(value.checked_slide_ids)) return false;
  if (!Number.isFinite(Number(value.checked_slide_count))) return false;
  if (!Number.isFinite(Number(value.total_slide_count))) return false;
  if (!Number.isFinite(Number(value.coverage_ratio))) return false;
  if (!Array.isArray(value.uncovered_source_segments)) return false;
  if (!Array.isArray(value.omitted_by_design)) return false;
  const explanationOk = isNonEmptyString(value.summary)
    || isNonEmptyString(value.justification)
    || isNonEmptyString(value.notes)
    || (value.checked_slide_ids.length === Number(value.checked_slide_count)
      && Array.isArray(value.omitted_by_design));
  const evidenceOk = isNonEmptyStructuredValue(value.evidence)
    || isNonEmptyStructuredValue(value.examples)
    || value.checked_slide_ids.length === Number(value.checked_slide_count);
  return explanationOk && evidenceOk;
}

function structuredVisibleProseRecoveryHintValid(value) {
  if (!isPlainObject(value)) return false;
  const status = String(value.status || "").trim().toLowerCase();
  const validStatuses = ["partial", "blocked", "warning", "advisory", "advice", "hint", "non_gating_hint", "non_gating_recovery_hint", "non_gating_partial_audit", "non_gating_sampled_pass", "recovery_hint", "sampled_recovery_hint"];
  if (!validStatuses.includes(status)) return false;
  const explanationOk = isNonEmptyString(value.summary)
    || isNonEmptyString(value.justification)
    || isNonEmptyString(value.notes)
    || isNonEmptyString(value.hint)
    || isNonEmptyString(value.scope);
  const evidenceOk = Array.isArray(value.checked_slide_ids)
    || Array.isArray(value.sample_slide_ids)
    || Array.isArray(value.sampled_slide_ids)
    || Array.isArray(value.checks_performed)
    || isNonEmptyStructuredValue(value.evidence)
    || isNonEmptyStructuredValue(value.examples)
    || ["advisory", "advice", "hint", "non_gating_hint", "non_gating_recovery_hint", "non_gating_partial_audit", "non_gating_sampled_pass", "recovery_hint", "sampled_recovery_hint"].includes(status);
  const nonGating = value.non_gating === true
    || value.blocking === false
    || ["advisory", "advice", "hint", "non_gating_hint", "non_gating_recovery_hint", "non_gating_partial_audit", "non_gating_sampled_pass", "recovery_hint", "sampled_recovery_hint"].includes(status);
  return explanationOk && evidenceOk && nonGating;
}

function structuredTexWarningsValid(value) {
  if (!isPlainObject(value)) return false;
  const overfullBoxes = value.overfull_boxes;
  if (!Array.isArray(overfullBoxes)) return false;
  const entriesOk = overfullBoxes.every((item) => isPlainObject(item)
    && (isNonEmptyString(item.kind) || isNonEmptyString(item.box_type) || isNonEmptyString(item.type))
    && isNonEmptyString(firstNonEmptyString(item.raw, item.raw_message, item.message)));
  const explanationOk = isNonEmptyString(firstNonEmptyString(
    value.summary,
    value.notes,
    value.warning_summary
  ))
    || typeof value.overfull_warning_count === "number"
    || typeof value.overfull_count === "number";
  return entriesOk && explanationOk;
}

function structuredLayoutPolicyValid(value) {
  if (!isPlainObject(value)) return false;
  const assessment = isPlainObject(value.overfull_assessment)
    ? value.overfull_assessment
    : (isNonEmptyString(value.overfull_assessment)
      ? { severity: value.overfull_assessment, gate_decision: value.gate_decision || value.policy_decision || "pass", summary: value.summary || value.notes || value.policy_notes }
      : null);
  if (!isPlainObject(assessment)) return false;
  const severity = String(assessment.severity || "").trim().toLowerCase();
  const validSeverities = ["none", "minor", "moderate", "severe"];
  if (!validSeverities.includes(severity)) return false;
  const gateDecision = String(assessment.gate_decision || "").trim().toLowerCase();
  const validGateDecisions = ["pass", "repair", "fail"];
  if (!validGateDecisions.includes(gateDecision)) return false;
  return isNonEmptyString(firstNonEmptyString(
    assessment.summary,
    assessment.notes,
    assessment.evidence,
    assessment.threshold_used,
    assessment.rationale,
    assessment.reason,
    assessment.justification,
    value.summary,
    value.notes,
    value.policy_notes
  ));
}

function structuredRenderFidelitySafeguardsValid(value) {
  if (isNonEmptyString(value)) return true;
  if (Array.isArray(value)) return value.length > 0;
  if (!isPlainObject(value)) return false;
  return isNonEmptyStructuredValue(value.checks)
    || isNonEmptyStructuredValue(value.checks_used)
    || isNonEmptyStructuredValue(value.rules)
    || isNonEmptyStructuredValue(value.safeguards)
    || isNonEmptyStructuredValue(value.summary)
    || isNonEmptyStructuredValue(value.notes);
}

function structuredPptRenderStatusValid(value) {
  if (isNonEmptyString(value)) return true;
  if (!isPlainObject(value)) return false;
  const status = String(value.status || "").trim().toLowerCase();
  const validStatuses = ["rendered", "rendered_with_warnings", "blocked", "failed", "partial", "pass", "success", "succeeded", "ok", "done", "warning"];
  if (!validStatuses.includes(status)) return false;
  const generatedFlag = typeof value.main_pptx_generated === "boolean"
    || typeof value.main_pptx_exists === "boolean";
  if (!generatedFlag) return false;
  const commandOk = isNonEmptyString(value.command) || isNonEmptyString(value.render_command) || isNonEmptyString(value.renderer_command);
  const explanationOk = isNonEmptyString(value.blocker_or_warning_summary)
    || isNonEmptyString(value.summary)
    || isNonEmptyString(value.warning_summary)
    || isNonEmptyString(value.notes);
  return commandOk && explanationOk;
}

function structuredPptValidationStatusValid(value) {
  if (isNonEmptyString(value)) return true;
  if (!isPlainObject(value)) return false;
  const hasOkFlag = typeof value.ok === "boolean";
  const status = String(value.status || "").trim().toLowerCase();
  const validStatuses = ["pass", "ok", "success", "succeeded", "warning", "blocked", "failed", "fail"];
  if (!hasOkFlag && !validStatuses.includes(status)) return false;
  const countOk = Number.isFinite(Number(value.fatal_count ?? value.error_count ?? 0))
    && Number.isFinite(Number(value.warning_count ?? 0));
  const reportOk = isNonEmptyString(value.report_path)
    || isNonEmptyString(value.validation_report)
    || isNonEmptyString(value.pptx_validation_json)
    || isNonEmptyString(value.path);
  const explanationOk = isNonEmptyString(value.summary)
    || isNonEmptyString(value.notes)
    || isNonEmptyString(value.blocker_or_warning_summary);
  return countOk && reportOk && explanationOk;
}

function structuredPptWarningsValid(value) {
  if (!isPlainObject(value)) return false;
  const issues = Array.isArray(value.issues) ? value.issues : (Array.isArray(value.warnings) ? value.warnings : []);
  const entriesOk = issues.every((item) => {
    if (isPlainObject(item)) {
      return isNonEmptyString(item.message) || isNonEmptyString(item.code) || isNonEmptyString(item.summary);
    }
    return isNonEmptyString(item);
  });
  const hasCount = Number.isFinite(Number(value.warning_count ?? value.count ?? issues.length));
  const explanationOk = isNonEmptyString(value.summary)
    || isNonEmptyString(value.notes)
    || hasCount;
  return entriesOk && hasCount && explanationOk;
}

function validateFinalBeamerAcceptanceFields(content) {
  const errors = [];
  if (!isPlainObject(content)) return errors;

  const validators = {
    compile_status: structuredCompileStatusValid,
    readability_status: structuredReadabilityStatusValid,
    tex_warnings: structuredTexWarningsValid,
    layout_policy: structuredLayoutPolicyValid,
    visible_prose_recovery_hint: structuredVisibleProseRecoveryHintValid,
    visible_prose_fidelity_final: structuredVisibleProseFidelityValid,
    render_fidelity_safeguards: structuredRenderFidelitySafeguardsValid,
  };

  for (const field of STRUCTURED_FINAL_FIELDS) {
    if (!Object.prototype.hasOwnProperty.call(content, field.key)) {
      errors.push(`programmer structured deliverable field missing: ${field.key}`);
      continue;
    }
    if (!validators[field.key](content[field.key])) {
      errors.push(`programmer structured deliverable field invalid: ${field.key} must be ${field.description}`);
    }
  }
  return errors;
}

function validateFinalPptAcceptanceFields(content) {
  const errors = [];
  if (!isPlainObject(content)) return errors;

  const validators = {
    render_status: structuredPptRenderStatusValid,
    validation_status: structuredPptValidationStatusValid,
    pptx_warnings: structuredPptWarningsValid,
    layout_policy: structuredLayoutPolicyValid,
    visible_prose_recovery_hint: structuredVisibleProseRecoveryHintValid,
    visible_prose_fidelity_final: structuredVisibleProseFidelityValid,
    render_fidelity_safeguards: structuredRenderFidelitySafeguardsValid,
  };

  for (const field of PPT_STRUCTURED_FINAL_FIELDS) {
    if (!Object.prototype.hasOwnProperty.call(content, field.key)) {
      errors.push(`programmer structured deliverable field missing: ${field.key}`);
      continue;
    }
    if (!validators[field.key](content[field.key])) {
      errors.push(`programmer structured deliverable field invalid: ${field.key} must be ${field.description}`);
    }
  }
  return errors;
}

function buildPromptLinesForFinalBeamer() {
  return [
    "For final-phase Beamer tasks, add these additional structured acceptance fields to the same top-level JSON object: compile_status, readability_status, tex_warnings, layout_policy, visible_prose_recovery_hint, visible_prose_fidelity_final, render_fidelity_safeguards.",
    "compile_status must concretely state whether main.pdf was generated, which compile command was used, where logs live, and what blocker/warning summary remains.",
    "readability_status must concretely state the layout/readability outcome and summarize the overfull assessment instead of treating every overfull warning as a hard failure.",
    "tex_warnings.overfull_boxes must preserve the raw TeX warning facts, one entry per parsed overfull warning when available.",
    "layout_policy.overfull_assessment must classify overfull warnings into none/minor/moderate/severe and choose gate_decision=pass/repair/fail accordingly.",
    "visible_prose_recovery_hint is a non-gating recovery/debug hint and may stay partial or sampled.",
    "visible_prose_fidelity_final must be the full-deck gating audit with status pass|warning|fail, full checked slide IDs, checked_slide_count, total_slide_count, coverage_ratio, uncovered_source_segments, and omitted_by_design.",
    "render_fidelity_safeguards must concretely list the safeguards/checks used to prevent scaffold leakage, prose loss, or render-only skeleton output.",
    "Do not rely on free prose alone for those final Beamer checks; fill the structured fields explicitly.",
  ];
}

function buildPromptLinesForFinalPpt() {
  return [
    "For final-phase PPT tasks, add these additional structured acceptance fields to the same top-level JSON object: render_status, validation_status, pptx_warnings, layout_policy, visible_prose_recovery_hint, visible_prose_fidelity_final, render_fidelity_safeguards.",
    "render_status must concretely state whether main.pptx was generated, which renderer command was used, where logs live if any, and what blocker/warning summary remains.",
    "validation_status must summarize pptx_validation.json with ok/fatal_count/warning_count and the concrete report path.",
    "pptx_warnings must preserve validator warning facts from pptx_validation.json issues/warnings; use warning_count=0 plus a summary when there are no warnings.",
    "layout_policy.overfull_assessment must classify PPT layout/render warnings into none/minor/moderate/severe and choose gate_decision=pass/repair/fail accordingly.",
    "visible_prose_recovery_hint is a non-gating recovery/debug hint and may stay partial or sampled.",
    "visible_prose_fidelity_final must be the full-deck gating audit with status pass|warning|fail, full checked slide IDs, checked_slide_count, total_slide_count, coverage_ratio, uncovered_source_segments, and omitted_by_design.",
    "render_fidelity_safeguards must concretely list the validator/renderer/scaffold-leakage/prose-retention checks used to prevent a skeleton or prose-loss PPT output.",
    "Do not rely on free prose alone for those final PPT checks; fill the structured fields explicitly.",
  ];
}

function buildStructuredValidationTokens(content) {
  if (!isPlainObject(content)) return [];
  const tokens = [];

  const compileStatus = content.compile_status;
  if (isNonEmptyStructuredValue(compileStatus)) {
    tokens.push("compile_status", "编译状态", "compile", "latexmk", "xelatex", "main.pdf", "log", JSON.stringify(compileStatus));
  }

  const readabilityStatus = content.readability_status;
  if (isNonEmptyStructuredValue(readabilityStatus)) {
    tokens.push("readability_status", "可读性", "版式", "overfull", "warning", "severity", JSON.stringify(readabilityStatus));
  }

  const texWarnings = content.tex_warnings;
  if (isNonEmptyStructuredValue(texWarnings)) {
    tokens.push("tex_warnings", "overfull", "warning", "tex warning", "原始 TeX 告警", JSON.stringify(texWarnings));
  }

  const layoutPolicy = content.layout_policy;
  if (isNonEmptyStructuredValue(layoutPolicy)) {
    tokens.push("layout_policy", "overfull_assessment", "minor", "moderate", "severe", "gate decision", JSON.stringify(layoutPolicy));
  }

  const visibleProseRecoveryHint = content.visible_prose_recovery_hint;
  if (isNonEmptyStructuredValue(visibleProseRecoveryHint)) {
    tokens.push("visible_prose_recovery_hint", "visible prose", "恢复提示", "non-gating", JSON.stringify(visibleProseRecoveryHint));
  }

  const visibleProseFidelity = content.visible_prose_fidelity_final;
  if (isNonEmptyStructuredValue(visibleProseFidelity)) {
    tokens.push("visible_prose_fidelity_final", "visible prose", "可见正文", "全量核验", "lower-bound visible-content contract", "slides.json", "main.tex", JSON.stringify(visibleProseFidelity));
  }

  const renderFidelitySafeguards = content.render_fidelity_safeguards;
  if (isNonEmptyStructuredValue(renderFidelitySafeguards)) {
    tokens.push("render_fidelity_safeguards", "render fidelity", "safeguards", "safeguard", "防护", "自检", JSON.stringify(renderFidelitySafeguards));
  }

  const renderStatus = content.render_status;
  if (isNonEmptyStructuredValue(renderStatus)) {
    tokens.push("render_status", "PPT 渲染状态", "renderer", "main.pptx", "render command", JSON.stringify(renderStatus));
  }

  const validationStatus = content.validation_status;
  if (isNonEmptyStructuredValue(validationStatus)) {
    tokens.push("validation_status", "pptx_validation.json", "validator", "fatal_count", "warning_count", JSON.stringify(validationStatus));
  }

  const pptxWarnings = content.pptx_warnings;
  if (isNonEmptyStructuredValue(pptxWarnings)) {
    tokens.push("pptx_warnings", "PPT validator warnings", "layout warning", "issues", JSON.stringify(pptxWarnings));
  }

  return tokens;
}

function extractArtifactPaths(content) {
  if (!isPlainObject(content?.artifact_paths)) return {};
  const result = {};
  for (const [key, value] of Object.entries(content.artifact_paths)) {
    if (isNonEmptyString(value)) result[key] = value.trim();
  }
  return result;
}

function collectCheckpointArtifactPaths(checkpoint) {
  if (!isPlainObject(checkpoint)) return {};
  const merged = {};
  const candidates = [];
  if (isPlainObject(checkpoint.final_programmer?.content)) {
    candidates.push(checkpoint.final_programmer.content);
  }
  const rounds = Array.isArray(checkpoint.rounds) ? [...checkpoint.rounds].reverse() : [];
  for (const round of rounds) {
    if (isPlainObject(round?.programmer?.content)) {
      candidates.push(round.programmer.content);
    }
  }
  for (const content of candidates) {
    Object.assign(merged, extractArtifactPaths(content));
  }
  return merged;
}

module.exports = {
  STRUCTURED_FINAL_FIELDS,
  PPT_STRUCTURED_FINAL_FIELDS,
  validateFinalBeamerAcceptanceFields,
  validateFinalPptAcceptanceFields,
  buildPromptLinesForFinalBeamer,
  buildPromptLinesForFinalPpt,
  buildStructuredValidationTokens,
  collectCheckpointArtifactPaths,
};
