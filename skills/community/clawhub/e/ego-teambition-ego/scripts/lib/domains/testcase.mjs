import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { whichEgo } from "../launch-check.mjs";
import {
  MAX_PAGES,
  RESULT_TAG,
  SPACE_NAME,
  USAGE,
  buildCaseQueryUrl,
  buildTql,
  egoMissingSummary,
  extractTaggedJson,
  formatCase,
  formatCases,
  formatGroups,
  formatPlan,
  groupsEndpoint,
  interpretFetch,
  mapBrowserError,
  missingIds,
  parsePlanUrl,
  parseTestcaseArgs,
  planEndpoint,
  resolveProcessExit,
} from "../pure.mjs";
import { createTransport } from "../session.mjs";
import {
  archiveEndpoint,
  buildCreateBody,
  caseMatchesRef,
  coerceSteps,
  createCaseEndpoint,
  extractNamedList,
  flowStatusEndpoint,
  formatArchiveResult,
  formatCreateResult,
  formatFlowStatuses,
  formatStatusResult,
  formatUpdateResult,
  groupIdFromPlan,
  pickTestcaseFlow,
  scenarioIdFromCases,
  scenarioIdFromPlan,
  stepsForUpdate,
  taskflowStatusEndpoint,
  taskflowsEndpoint,
  testhubEndpoint,
  testhubIdFrom,
  usercaseFieldEndpoint,
  validateWriteConfig,
} from "../write.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

function fail(message, code = 1) {
  return { exitCode: code, stdout: "", stderr: `错误: ${message}\n` };
}

function ok(stdout, stderr = "") {
  return { exitCode: 0, stdout, stderr };
}

export async function collectCases(session, config) {
  const tql = buildTql(config.planId, config.mode === "cases" ? config.groupId : "");
  const maxPages = config.maxPages || MAX_PAGES;
  const out = [];
  let token = "";
  let pages = 0;
  let found = null;
  while (pages < maxPages) {
    const url = buildCaseQueryUrl({
      projectId: config.projectId,
      tql,
      pageToken: token,
      needResult: config.needResult !== false,
    });
    const fetchPage = config.fetch || ((nextUrl, opts) => session.fetch(nextUrl, opts));
    const response = await fetchPage(url, { timeout: 30_000 });
    const status = response && response.status != null ? response.status : 200;
    if (status === 401) return { error: "401 未登录" };
    if (status !== 200) return { error: `HTTP ${status}` };
    const body = response ? response.body : null;
    if (!body || typeof body !== "object") return { error: "响应 JSON 解析失败" };
    const rows = Array.isArray(body.result) ? body.result : [];
    if (config.mode === "get") {
      const ref = config.caseRef != null && config.caseRef !== "" ? config.caseRef : config.uniqueId;
      found = rows.find((item) => caseMatchesRef(item, ref)) || null;
      if (found) break;
    } else {
      out.push(...rows);
    }
    pages += 1;
    token = body.nextPageToken || "";
    if (!token || rows.length === 0) break;
  }
  if (config.mode === "get") return { found };
  return { cases: out };
}

const READ_OR_WRITE = new Set([
  "plan",
  "groups",
  "cases",
  "get",
  "flow-statuses",
  "create",
  "update",
  "set-status",
  "delete",
]);

function fetchWith(link) {
  return (url, opts) => link.request(url, opts);
}

async function requestChecked(link, url, opts) {
  const payload = await link.request(url, opts);
  const checked = interpretFetch(payload);
  if (!checked.error && (checked.body == null || typeof checked.body !== "object")) {
    return { error: "响应 JSON 解析失败" };
  }
  return checked;
}

async function findCase(session, link, config) {
  const collected = await collectCases(session, {
    mode: "get",
    projectId: config.projectId,
    planId: config.planId,
    caseRef: config.caseRef != null && config.caseRef !== "" ? config.caseRef : config.uniqueId,
    needResult: true,
    maxPages: config.maxPages,
    fetch: fetchWith(link),
  });
  if (collected.error) return { error: mapBrowserError(collected.error) };
  if (collected.found == null) {
    const label = config.caseRef != null && config.caseRef !== "" ? config.caseRef : config.uniqueId;
    return { error: `计划内未找到用例 ${label}` };
  }
  if (!collected.found._id) return { error: "用例缺少 _id" };
  return { item: collected.found };
}

async function resolveCreateContext(link, session, config) {
  let groupId = config.groupId || "";
  let sfcId = config.scenarioFieldConfigId || "";
  if (!groupId || !sfcId) {
    const plan = await requestChecked(link, planEndpoint(config.projectId, config.planId));
    if (plan.error) return plan;
    if (!groupId) groupId = groupIdFromPlan(plan.body);
    if (!sfcId) sfcId = scenarioIdFromPlan(plan.body);
  }
  if (!groupId) return { error: "缺少分组：传入 --group <groupId>" };
  if (!sfcId) {
    const collected = await collectCases(session, {
      mode: "cases",
      projectId: config.projectId,
      planId: config.planId,
      needResult: false,
      maxPages: 1,
      fetch: fetchWith(link),
    });
    if (collected.error) return { error: mapBrowserError(collected.error) };
    sfcId = scenarioIdFromCases(collected.cases);
  }
  if (!sfcId) return { error: "缺少场景字段配置：传入 --scenario-field-config-id" };
  return { groupId, sfcId };
}

async function createCase(link, session, config) {
  const steps = coerceSteps(config);
  if (steps.error) return fail(steps.error);
  const context = await resolveCreateContext(link, session, config);
  if (context.error) return fail(context.error);
  const checked = await requestChecked(link, createCaseEndpoint(config.projectId, config.planId), {
    method: "POST",
    body: buildCreateBody({
      title: config.title,
      precondition: config.precondition,
      steps: steps.steps || [],
      priority: config.priority,
      executorId: config.executorId,
      caseType: config.caseType,
      projectId: config.projectId,
      planId: config.planId,
      groupId: context.groupId,
      scenarioFieldConfigId: context.sfcId,
    }),
    timeout: 30_000,
  });
  if (checked.error) return fail(checked.error);
  return ok(formatCreateResult(checked.body, config.asJson));
}

async function putUsercaseField(link, config, testhubId, usercaseId, field, body) {
  return requestChecked(
    link,
    usercaseFieldEndpoint(config.projectId, testhubId, usercaseId, field),
    { method: "PUT", body, timeout: 30_000 },
  );
}

async function updateCase(link, session, config) {
  const steps = coerceSteps(config);
  if (steps.error) return fail(steps.error);
  const found = await findCase(session, link, config);
  if (found.error) return fail(found.error);
  if (!found.item._fromHubTestcaseId) {
    return fail("用例缺少 _fromHubTestcaseId，无法更新标题、前置条件或步骤");
  }
  const hub = await requestChecked(link, testhubEndpoint(config.projectId));
  if (hub.error) return fail(hub.error);
  const testhubId = testhubIdFrom(hub.body);
  if (!testhubId) return fail("GET /testhub 没有返回 testhubId");
  const applied = {};
  if (config.title != null) {
    const title = await putUsercaseField(link, config, testhubId, found.item._fromHubTestcaseId, "title", {
      title: String(config.title),
    });
    if (title.error) return fail(`更新 title 失败: ${title.error}`);
    applied.title = title.body;
  }
  if (config.precondition != null) {
    const precondition = await putUsercaseField(link, config, testhubId, found.item._fromHubTestcaseId, "precondition", {
      precondition: String(config.precondition),
    });
    if (precondition.error) return fail(`更新 precondition 失败: ${precondition.error}`);
    applied.precondition = precondition.body;
  }
  if (steps.steps != null) {
    const saved = await putUsercaseField(link, config, testhubId, found.item._fromHubTestcaseId, "steps", {
      steps: stepsForUpdate(steps.steps, found.item.steps),
    });
    if (saved.error) return fail(`更新 steps 失败: ${saved.error}`);
    applied.steps = saved.body;
  }
  return ok(formatUpdateResult({ caseItem: found.item, testhubId, fields: applied }, config.asJson));
}

async function setStatus(link, session, config) {
  const found = await findCase(session, link, config);
  if (found.error) return fail(found.error);
  const checked = await requestChecked(link, flowStatusEndpoint(config.projectId, config.planId, found.item._id), {
    method: "PUT",
    body: { _flowStatusId: String(config.flowStatusId) },
    timeout: 30_000,
  });
  if (checked.error) return fail(checked.error);
  return ok(formatStatusResult(checked.body, config.flowStatusId, config.asJson));
}

async function archiveCase(link, session, config) {
  const found = await findCase(session, link, config);
  if (found.error) return fail(found.error);
  const checked = await requestChecked(link, archiveEndpoint(found.item._id), {
    method: "POST",
    timeout: 30_000,
  });
  if (checked.error) return fail(checked.error);
  return ok(formatArchiveResult(checked.body, found.item, config.asJson));
}

async function listFlowStatuses(link, config) {
  const flows = await requestChecked(link, taskflowsEndpoint(config.projectId));
  if (flows.error) return fail(flows.error);
  const flow = pickTestcaseFlow(extractNamedList(flows.body, ["taskflows"]));
  if (!flow) return fail("未找到 type=testcase 的任务流");
  const statuses = await requestChecked(link, taskflowStatusEndpoint(flow._id));
  if (statuses.error) return fail(statuses.error);
  const rows = extractNamedList(statuses.body, ["taskflowstatuses", "statuses"]);
  return ok(formatFlowStatuses(flow, rows, config.asJson));
}

export async function executeTestcase(config, { session, transport } = {}) {
  const cmd = config.cmd;
  try {
    if (cmd === "cleanup") {
      await session.cleanup();
      return ok("已关闭常驻浏览器空间\n");
    }
    if (!READ_OR_WRITE.has(cmd)) return fail(`未知命令: ${cmd || ""}`);
    const idError = missingIds(cmd, [cmd, config.projectId, config.planId, config.caseRef || config.uniqueId]);
    if (idError) return fail(idError);
    const writeError = validateWriteConfig(config);
    if (writeError) return fail(writeError);
    if (typeof session.ensureSite === "function") await session.ensureSite();
    const link = transport || createTransport(config.transport || "browser", session);
    if (cmd === "plan") {
      const checked = await requestChecked(link, planEndpoint(config.projectId, config.planId));
      if (checked.error) return fail(checked.error);
      return ok(formatPlan(checked.body, config.asJson));
    }
    if (cmd === "groups") {
      const checked = await requestChecked(link, groupsEndpoint(config.projectId, config.planId));
      if (checked.error) return fail(checked.error);
      return ok(formatGroups(checked.body, config.asJson));
    }
    if (cmd === "flow-statuses") return await listFlowStatuses(link, config);
    if (cmd === "create") return await createCase(link, session, config);
    if (cmd === "update") return await updateCase(link, session, config);
    if (cmd === "set-status") return await setStatus(link, session, config);
    if (cmd === "delete") return await archiveCase(link, session, config);
    const collected = await collectCases(session, {
      mode: cmd,
      projectId: config.projectId,
      planId: config.planId,
      groupId: config.groupId,
      uniqueId: config.uniqueId,
      caseRef: config.caseRef,
      needResult: true,
      maxPages: config.maxPages,
      fetch: fetchWith(link),
    });
    if (collected.error) return fail(mapBrowserError(collected.error));
    if (cmd === "get") {
      if (collected.found == null) return fail(`计划内未找到用例 #${config.uniqueId}`);
      return ok(formatCase(collected.found, config.asJson));
    }
    const formatted = formatCases(collected.cases, config.asJson);
    return ok(formatted.stdout, formatted.stderr);
  } catch (error) {
    return fail(error && error.message ? error.message : String(error));
  }
}

export function renderTestcaseEntry({ config, runHref, sessionHref }) {
  return [
    `import { executeTestcase } from ${JSON.stringify(runHref)};`,
    `import { createEgoSession } from ${JSON.stringify(sessionHref)};`,
    `const config = ${JSON.stringify(config)};`,
    `const session = await createEgoSession(config);`,
    `const result = await executeTestcase(config, { session });`,
    `console.log(${JSON.stringify(RESULT_TAG)} + JSON.stringify(result));`,
    `if (result.exitCode) process.exitCode = result.exitCode;`,
    "",
  ].join("\n");
}

async function launchTestcase(config, deps) {
  const io = {
    fs: deps.fs || fs,
    spawn: deps.spawn || spawn,
    spawnSync: deps.spawnSync,
    whichEgo: deps.whichEgo,
    mkdtemp: deps.mkdtemp || ((prefix) => fs.mkdtemp(prefix)),
    tmp: deps.tmp || os.tmpdir(),
    runModule: deps.runModule || path.join(here, "testcase.mjs"),
    egoModule: deps.egoModule || path.join(here, "..", "ego-deps.mjs"),
  };
  const detect = io.whichEgo || ((impl) => whichEgo(impl || io.spawnSync));
  if (!detect(io.spawnSync)) {
    const summary = egoMissingSummary(config.cmd || "testcase");
    return {
      exitCode: 2,
      stdout: `${JSON.stringify(summary, null, 2)}\n`,
      stderr: "",
    };
  }

  const dir = await io.mkdtemp(path.join(io.tmp, "ego-teambition-tb-"));
  const entry = path.join(dir, "entry.mjs");
  let stdoutBuf = "";
  let stderrBuf = "";
  let code = 1;
  try {
    await io.fs.writeFile(
      entry,
      renderTestcaseEntry({
        config,
        runHref: pathToFileURL(io.runModule).href,
        sessionHref: pathToFileURL(io.egoModule).href,
      }),
    );
    const href = pathToFileURL(entry).href;
    const child = io.spawn("ego-browser", ["nodejs", "-e", `await import(${JSON.stringify(href)})`], {
      stdio: ["ignore", "pipe", "pipe"],
    });
    child.stdout.on("data", (chunk) => {
      stdoutBuf += chunk;
    });
    child.stderr.on("data", (chunk) => {
      stderrBuf += chunk;
    });
    code = await new Promise((resolve) => {
      child.on("error", (error) => {
        stderrBuf += String(error.message || error);
        resolve(1);
      });
      child.on("close", (status) => resolve(status ?? 1));
    });
  } catch (error) {
    stderrBuf += String(error && error.message ? error.message : error);
    code = 1;
  } finally {
    if (io.fs.rm) await io.fs.rm(dir, { recursive: true, force: true }).catch(() => {});
  }

  const combined = `${stdoutBuf}\n${stderrBuf}`;
  const result = extractTaggedJson(combined, RESULT_TAG);
  if (result && typeof result === "object") {
    return {
      exitCode: typeof result.exitCode === "number" ? result.exitCode : resolveProcessExit(combined, code),
      stdout: result.stdout || "",
      stderr: result.stderr || "",
    };
  }
  const tail = combined.trim().slice(-300);
  const resolved = resolveProcessExit(combined, code);
  return {
    exitCode: code === 0 && resolved === 0 ? 1 : resolved,
    stdout: "",
    stderr: `错误: 浏览器执行失败（exit=${code}）: ${tail}\n`,
  };
}

export async function runTestcaseCli(argv, deps = {}) {
  const parsed = parseTestcaseArgs(argv);
  if (parsed.error) return fail(parsed.error);
  if (parsed.help || !parsed.cmd) {
    return { exitCode: parsed.help ? 0 : 1, stdout: USAGE, stderr: "" };
  }
  if (parsed.cmd === "parse-url") {
    const idError = missingIds("parse-url", parsed.positional);
    if (idError) return fail(idError);
    const ids = parsePlanUrl(parsed.positional[1]);
    if (!ids) {
      return fail("无法解析 URL，期望格式 .../project/{projectId}/testplan/{planId}/group/{groupId}");
    }
    return ok(`${ids.projectId}\t${ids.planId}\t${ids.groupId}\n`);
  }
  if (!READ_OR_WRITE.has(parsed.cmd) && parsed.cmd !== "cleanup") {
    return { exitCode: 1, stdout: USAGE, stderr: "" };
  }
  const idError = missingIds(parsed.cmd, parsed.positional);
  if (idError) return fail(idError);
  const built = buildTestcaseConfig(parsed);
  if (built.error) return fail(built.error);
  const writeError = validateWriteConfig(built.config);
  if (writeError) return fail(writeError);
  return launchTestcase(built.config, deps);
}

export function buildTestcaseConfig(parsed) {
  const ids = parsed.positional.slice(1);
  const steps = parsed.stepsJson != null ? coerceSteps({ stepsJson: parsed.stepsJson }) : { steps: undefined };
  if (steps.error) return { error: steps.error };
  const config = {
    cmd: parsed.cmd,
    asJson: Boolean(parsed.asJson),
    projectId: ids[0],
    planId: ids[1],
    uniqueId: ids[2],
    caseRef: ids[2],
    groupId: parsed.groupId || "",
    title: parsed.title,
    precondition: parsed.precondition,
    steps: steps.steps,
    executorId: parsed.executorId,
    caseType: parsed.caseType,
    scenarioFieldConfigId: parsed.scenarioFieldConfigId || "",
    flowStatusId: parsed.flowStatusId,
    yes: Boolean(parsed.yes),
    taskName: SPACE_NAME,
    transport: "browser",
  };
  if (parsed.priority != null) config.priority = Number(parsed.priority);
  return { config };
}
