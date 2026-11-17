// Phase 2a single-case writes. Paths are the verified browser capture only.
// No network in this file.

import { BASE, planEndpoint } from "./pure.mjs";

export const DELETE_CONFIRM =
  "移到回收站需要 --yes。删除前 Agent 必须先向用户确认 uniqueId 和标题，得到明确同意后再加 --yes。";

const USERCASE_FIELDS = new Set(["title", "precondition", "steps"]);

export function looksLikeObjectId(value) {
  return /^[0-9a-fA-F]{24}$/.test(String(value || ""));
}

export function caseMatchesRef(item, ref) {
  if (!item || ref == null || ref === "") return false;
  const token = String(ref);
  if (looksLikeObjectId(token)) return String(item._id || "") === token;
  return String(item.uniqueId) === token;
}

export function createCaseEndpoint(projectId, planId, base) {
  return `${planEndpoint(projectId, planId, base)}/testcases`;
}

export function testhubEndpoint(projectId, base = BASE) {
  return `${base}/testcase/api/v1/projects/${projectId}/testhub`;
}

export function usercaseFieldEndpoint(projectId, testhubId, usercaseId, field, base = BASE) {
  if (!USERCASE_FIELDS.has(field)) throw new Error(`未知用例字段: ${field}`);
  return `${base}/testcase/api/v1/projects/${projectId}/testhubs/${testhubId}/usercases/${usercaseId}/${field}`;
}

export function flowStatusEndpoint(projectId, planId, testcaseId, base) {
  return `${planEndpoint(projectId, planId, base)}/testcases/${testcaseId}/flowStatusId`;
}

export function archiveEndpoint(testcaseId, base = BASE) {
  return `${base}/api/testcases/${testcaseId}/archive`;
}

export function taskflowsEndpoint(projectId, base = BASE) {
  return `${base}/api/projects/${projectId}/taskflows?type=testcase`;
}

export function taskflowStatusEndpoint(taskflowId, base = BASE) {
  return `${base}/api/taskflows/${taskflowId}/taskflowstatus`;
}

export function stepsFromValue(parsed) {
  if (!Array.isArray(parsed)) return { error: "--steps-json 需要数组" };
  const steps = [];
  for (const step of parsed) {
    if (!step || typeof step !== "object" || Array.isArray(step)) {
      return { error: "--steps-json 的每一步需要对象 { desc, expected }" };
    }
    const item = {
      desc: step.desc == null ? "" : String(step.desc),
      expected: step.expected == null ? "" : String(step.expected),
    };
    if (step._id != null && step._id !== "") item._id = String(step._id);
    if (Object.prototype.hasOwnProperty.call(step, "expectPayload")) item.expectPayload = step.expectPayload;
    steps.push(item);
  }
  return { steps };
}

export function parseStepsJson(text) {
  if (text == null || text === "") return { steps: undefined };
  let parsed;
  try {
    parsed = JSON.parse(String(text));
  } catch {
    return { error: "--steps-json 不是合法 JSON" };
  }
  return stepsFromValue(parsed);
}

export function coerceSteps(config = {}) {
  if (config.stepsJson != null && config.stepsJson !== "") return parseStepsJson(config.stepsJson);
  if (config.steps == null) return { steps: undefined };
  return stepsFromValue(config.steps);
}

export function stepsForUpdate(incoming, existing) {
  const prev = Array.isArray(existing) ? existing : [];
  return (incoming || []).map((step, index) => {
    const next = {
      desc: step && step.desc != null ? String(step.desc) : "",
      expected: step && step.expected != null ? String(step.expected) : "",
      expectPayload: step && step.expectPayload !== undefined ? step.expectPayload : null,
    };
    const id = (step && step._id) || (prev[index] && prev[index]._id);
    if (id) next._id = String(id);
    return next;
  });
}

export function buildCreateBody(fields) {
  const steps = (fields.steps || []).map((step) => ({
    desc: step && step.desc != null ? String(step.desc) : "",
    expected: step && step.expected != null ? String(step.expected) : "",
  }));
  let priority = -1;
  if (fields.priority != null && fields.priority !== "") priority = Number(fields.priority);
  return {
    title: fields.title,
    _executorId: fields.executorId == null || fields.executorId === "" ? null : String(fields.executorId),
    precondition: fields.precondition == null ? "" : String(fields.precondition),
    priority,
    caseType: fields.caseType == null || fields.caseType === "" ? null : String(fields.caseType),
    customfields: [],
    steps,
    _testplanId: fields.planId,
    _projectId: fields.projectId,
    _testhubId: null,
    _commongroupId: fields.groupId,
    _scenariofieldconfigId: fields.scenarioFieldConfigId,
    involvers: [],
    involveMembers: [],
    involveTeams: [],
    involveGroups: [],
  };
}

function textValue(value) {
  return typeof value === "string" ? value : "";
}

export function groupIdFromPlan(body) {
  const data = (body && body.result) || {};
  return textValue(data._commongroupId) || textValue(data._rootCommongroupId);
}

export function scenarioIdFromPlan(body) {
  const data = (body && body.result) || {};
  return textValue(data._scenariofieldconfigId);
}

export function scenarioIdFromCases(cases) {
  const list = Array.isArray(cases) ? cases : [];
  const found = list.find((item) => item && typeof item._scenariofieldconfigId === "string" && item._scenariofieldconfigId);
  return found ? found._scenariofieldconfigId : "";
}

export function testhubIdFrom(body) {
  const data = (body && body.result) || {};
  return textValue(data._id);
}

export function extractNamedList(body, keys) {
  const extra = Array.isArray(keys) ? keys : [];
  if (Array.isArray(body)) return body;
  if (!body || typeof body !== "object") return [];
  for (const key of ["result", ...extra]) {
    if (Array.isArray(body[key])) return body[key];
  }
  const result = body.result;
  if (result && typeof result === "object" && !Array.isArray(result)) {
    for (const key of extra) {
      if (Array.isArray(result[key])) return result[key];
    }
  }
  return [];
}

export function pickTestcaseFlow(list) {
  const flows = Array.isArray(list) ? list : [];
  return flows.find((item) => item && item.type === "testcase" && item._id)
    || flows.find((item) => item && item._id)
    || null;
}

export function validateWriteConfig(config = {}) {
  const cmd = config.cmd;
  if (cmd === "create") {
    if (config.title == null || String(config.title).trim() === "") return "--title 需要标题";
    if (config.priority != null && config.priority !== "") {
      const priority = Number(config.priority);
      if (!Number.isInteger(priority)) return "--priority 需要整数";
    }
    const steps = coerceSteps(config);
    if (steps.error) return steps.error;
  }
  if (cmd === "update") {
    const steps = coerceSteps(config);
    if (steps.error) return steps.error;
    const hasTitle = config.title != null;
    const hasPre = config.precondition != null;
    const hasSteps = steps.steps != null;
    if (!hasTitle && !hasPre && !hasSteps) return "update 至少需要 --title、--precondition 或 --steps-json 之一";
    if (hasTitle && String(config.title).trim() === "") return "--title 需要标题";
  }
  if (cmd === "set-status") {
    if (config.flowStatusId == null || String(config.flowStatusId).trim() === "") return "--flow-status-id 需要状态 ID";
  }
  if (cmd === "delete" && !config.yes) return DELETE_CONFIRM;
  return null;
}

export function formatCreateResult(body, asJson = false) {
  if (asJson) return `${JSON.stringify(body ?? null, null, 2)}\n`;
  const data = (body && body.result) || {};
  const lines = [
    `已创建 #${data.uniqueId ?? "?"} ${data.title || ""}`.trimEnd(),
    `_id: ${data._id || ""}`,
    `_fromHubTestcaseId: ${data._fromHubTestcaseId || ""}`,
  ];
  if (data._flowstatusId) lines.push(`_flowstatusId: ${data._flowstatusId}`);
  return `${lines.join("\n")}\n`;
}

export function formatUpdateResult({ caseItem, testhubId, fields } = {}, asJson = false) {
  const item = caseItem || {};
  const applied = fields || {};
  if (asJson) {
    return `${JSON.stringify({
      uniqueId: item.uniqueId,
      _id: item._id,
      _fromHubTestcaseId: item._fromHubTestcaseId,
      testhubId,
      fields: applied,
    }, null, 2)}\n`;
  }
  const lines = [`已更新 #${item.uniqueId ?? "?"} ${item.title || ""}`.trimEnd()];
  for (const name of ["title", "precondition", "steps"]) {
    if (applied[name]) lines.push(`字段: ${name}`);
  }
  lines.push(`_id: ${item._id || ""}`);
  lines.push(`_fromHubTestcaseId: ${item._fromHubTestcaseId || ""}`);
  lines.push(`testhubId: ${testhubId || ""}`);
  return `${lines.join("\n")}\n`;
}

export function formatStatusResult(body, requestedId, asJson = false) {
  if (asJson) return `${JSON.stringify(body ?? null, null, 2)}\n`;
  const data = (body && body.result) || {};
  return [
    `已更新状态 #${data.uniqueId ?? "?"}`,
    `_id: ${data._id || ""}`,
    `_flowstatusId: ${data._flowstatusId || requestedId || ""}`,
    "",
  ].join("\n");
}

export function formatArchiveResult(body, caseItem, asJson = false) {
  if (asJson) return `${JSON.stringify(body ?? null, null, 2)}\n`;
  const data = body && typeof body === "object" ? body : {};
  const item = caseItem || {};
  const flag = data.isArchived == null ? "（响应未带 isArchived）" : String(data.isArchived);
  return `已移到回收站 #${item.uniqueId ?? "?"} ${item.title || ""}\n_id: ${data._id || item._id || ""}\nisArchived: ${flag}\n`;
}

export function formatFlowStatuses(flow, statuses, asJson = false) {
  const rows = Array.isArray(statuses) ? statuses : [];
  const info = flow || {};
  if (asJson) return `${JSON.stringify({ flow: info, statuses: rows }, null, 2)}\n`;
  const head = `任务流: ${info.name || ""} ${info._id || ""}`.trimEnd();
  const lines = rows.map((item) => `${(item && item._id) || ""}\t${(item && item.kind) || ""}\t${(item && item.name) || ""}`);
  return `${[head, ...lines].join("\n")}\n`;
}
