export const TOKEN_KEYS = [
  "total_tokens",
  "input_tokens",
  "cached_input_tokens",
  "output_tokens",
  "reasoning_output_tokens",
];

export function emptyToken() {
  return Object.fromEntries(TOKEN_KEYS.map((key) => [key, 0]));
}

export function addToken(target, usage) {
  for (const key of TOKEN_KEYS) target[key] += Number(usage?.[key] || 0);
  return target;
}

export function maxToken(target, usage) {
  for (const key of TOKEN_KEYS) {
    target[key] = Math.max(Number(target[key] || 0), Number(usage?.[key] || 0));
  }
  return target;
}

export function validateReport(report) {
  const errors = [];
  if (!report || typeof report !== "object" || Array.isArray(report)) {
    return ["报告数据不是有效对象"];
  }
  if (report.schemaVersion !== 2) errors.push("schemaVersion 必须是 2");
  if (report.platform !== "codex") errors.push("platform 必须是 codex");
  if (!report.summary || typeof report.summary !== "object") errors.push("缺少 summary");
  if (!Array.isArray(report.projects)) errors.push("projects 必须是数组");
  if (!Array.isArray(report.diagnostics)) errors.push("diagnostics 必须是数组");
  return errors;
}

export function normalizeReport(report) {
  if (report?.schemaVersion === 2) return report;
  const projects = Array.isArray(report?.projects) ? report.projects : [];
  return {
    schemaVersion: 2,
    platform: "codex",
    generatedAt: report?.generatedAt || new Date().toISOString(),
    range: report?.range || { days: 7 },
    workspace: report?.workspaceLabel || "本地工作区",
    summary: report?.summary || {},
    projects: projects.map((project) => ({
      ...project,
      category: project.category || "其他任务",
      confidence: project.confidence || "medium",
      evidence: Array.isArray(project.evidence) ? project.evidence : [],
      actions: Array.isArray(project.actions) ? project.actions : [],
      promptAssessment: project.promptAssessment || {
        summary: project.promptIssue || project.issue || "缺少可用的 Prompt 诊断信息。",
        missing: [],
        signals: {},
      },
      nextPrompt: project.nextPrompt || "请明确最终交付物、范围、输入材料、约束和验收标准。",
      level: project.level || "yellow",
    })),
    diagnostics: Array.isArray(report?.diagnostics) ? report.diagnostics : [],
    environment: report?.environment || {},
  };
}
