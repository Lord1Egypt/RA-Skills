// Pure helpers for teambition-ego. No browser, no process.exit.

export const SKILL = "teambition-ego";
export const BASE = "https://www.teambition.com";
export const HOME_URL = `${BASE}/`;
export const SPACE_NAME = "tb-testcase api";
export const LOGIN_TASK = "teambition-login-check";
export const MAX_PAGES = 30;
export const RESULT_TAG = "TBEGO";

// Body text, not the document title. A signed-out tab can still be titled Teambition.
export const PLATFORM_CHROME_RE = /我的项目|工作台|新建项目|项目列表|测试计划|测试用例|My Projects|Workbench|Test Plan|Test Cases/;
export const LOGIN_WALL_RE = /扫码登录|二维码登录|密码登录|账号登录|手机号登录|请登录|登录 Teambition|Sign in to Teambition/;
export const LOGIN_COOKIE_RE = /(?:^|;\s*)(?:TEAMBITION_SESSIONID|TB_ACCESS_TOKEN)=/;
export const COOKIE_NAMES = ["TEAMBITION_SESSIONID", "TB_ACCESS_TOKEN"];

const PRIORITY = { 0: "紧急", 1: "高", 2: "中", 3: "低" };
const PLAN_URL_RE = /\/project\/([0-9a-f]{24})\/testplan\/([0-9a-f]{24})(?:\/group\/([0-9a-f]{24}))?/;

export const HOW_TO_LOGIN = [
  "Install Ego Lite and put ego-browser on PATH (often ~/.local/bin). Open the Ego Lite app.",
  "Visit https://www.teambition.com/ and sign in to the Teambition account that can open the test plan.",
  "Leave that teambition.com session signed in inside Ego. Do not paste cookies or an Open API token.",
  "Re-run this skill’s login-check. Read or change test cases only after exit 0.",
  "Sessions expire. Login-check before reading. Never type a password.",
];

export const HOW_TO_LOGIN_ZH = [
  "先安装 Ego Lite，并把 ego-browser 放进 PATH（常见 ~/.local/bin）。打开 Ego Lite。",
  "访问 https://www.teambition.com/ ，登录能打开该测试计划的 Teambition 账号。",
  "保持 Ego 里的 teambition.com 为登录状态。不要粘贴 Cookie，也不要填 Open API token。",
  "重新跑 login-check。只有退出码 0 之后才读取或修改用例。",
  "登录态会过期。每次读取前都要先检查。不要代填密码。",
];

export const LOGIN_TIP =
  "Tell the user: sign in to teambition.com inside Ego Lite before reading or changing test plans. Testcase reads and Phase 2a writes use the browser session at www.teambition.com, not a teambition_cli or MCP token. If login-check exits 2, ask them to open Ego Lite, sign in, then re-run. Never type a password or paste cookies.";

export const LOGIN_TIP_ZH =
  "请告诉用户：在 Ego Lite 里登录 teambition.com 之后才能读或改测试计划。用例的读和 Phase 2a 写都走浏览器会话 www.teambition.com，不要用 teambition_cli 或 MCP token。若 login-check 退出码是 2，请人在 Ego Lite 打开 teambition.com 登录后再跑。不要代填密码，不要粘贴 Cookie。";

export const USAGE = `teambition-ego — Teambition test plans and test cases via Ego Lite

Install Ego Lite and put ego-browser on PATH first. Missing ego-browser soft-fails (exit 2).
Test plans use the browser session at https://www.teambition.com/testcase/api/ .
Archive uses https://www.teambition.com/api/testcases/{id}/archive (not under /testcase/api/).
Do not use teambition_cli or an Open API / MCP token for this module.

  node scripts/check-login.mjs
  node scripts/check-login.mjs --keep
  node scripts/tb.mjs testcase parse-url <testplan-url>
  node scripts/tb.mjs testcase plan <projectId> <planId> [--json]
  node scripts/tb.mjs testcase groups <projectId> <planId> [--json]
  node scripts/tb.mjs testcase cases <projectId> <planId> [--group <groupId>] [--json]
  node scripts/tb.mjs testcase get <projectId> <planId> <uniqueId> [--json]
  node scripts/tb.mjs testcase flow-statuses <projectId> [--json]
  node scripts/tb.mjs testcase create <projectId> <planId> --title <title> [--group <groupId>] [--precondition <text>] [--steps-json <json>] [--priority <n>] [--executor-id <id>] [--case-type <type>] [--scenario-field-config-id <id>] [--json]
  node scripts/tb.mjs testcase update <projectId> <planId> <caseId|uniqueId> [--title <title>] [--precondition <text>] [--steps-json <json>] [--json]
  node scripts/tb.mjs testcase set-status <projectId> <planId> <caseId|uniqueId> --flow-status-id <id> [--json]
  node scripts/tb.mjs testcase delete <projectId> <planId> <caseId|uniqueId> --yes [--json]
  node scripts/tb.mjs testcase cleanup

Phase 1 domain: testcase.
Phase 2a writes on that domain: create, update, set-status, delete (archive).
Not in this phase: task, project. Not in this build: group-create, move, bulk.

check-login exits 0 when teambition.com is signed in, 2 when login is required or ego-browser is missing.
Default finish({ keep: [] }). --keep leaves the page and calls handOff().
Reads and Phase 2a writes keep the named browser space open for reuse. cleanup closes it.
delete moves one execution case to the recycle bin and requires --yes. The agent confirms uniqueId and title with the user first.
`;

export const FUTURE_DOMAINS = ["task", "project"];

export function strip(obj) {
  for (const key of Object.keys(obj)) {
    if (obj[key] === undefined || obj[key] === null || obj[key] === "") delete obj[key];
  }
  return obj;
}

export function parseCheckArgs(argv) {
  const out = { keep: false, help: false, taskName: LOGIN_TASK };
  const args = argv || [];
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--help" || arg === "-h") out.help = true;
    else if (arg === "--keep") out.keep = true;
    else if (arg === "--task-name") out.taskName = String(args[++i] || out.taskName);
    else throw new Error(`Unknown arg: ${arg}`);
  }
  return out;
}

export function isLoginWall({ url = "", title = "", text = "" } = {}) {
  const pageUrl = String(url || "");
  const blob = `${pageUrl}\n${title}\n${text}`;
  if (/account\.teambition\.com|login\.teambition\.com/i.test(pageUrl)) return true;
  if (/\/login(\b|[/?#]|$)/i.test(pageUrl)) return true;
  return LOGIN_WALL_RE.test(blob);
}

export function detectSignals({ url = "", title = "", text = "", cookie = "" } = {}) {
  const body = String(text || "");
  return {
    platformChrome: PLATFORM_CHROME_RE.test(body),
    onLoginWall: isLoginWall({ url, title, text }),
    loggedInCookie: LOGIN_COOKIE_RE.test(String(cookie || "")),
  };
}

export function classifyLogin({ url = "", title = "", text = "", cookie = "", signals = {} } = {}) {
  const pageUrl = String(url || "");
  const body = String(text || "");
  const loginWall = Boolean(signals.onLoginWall) || isLoginWall({ url: pageUrl, title, text: body });
  const platformHint = PLATFORM_CHROME_RE.test(body) || Boolean(signals.platformChrome);
  const cookieIn = LOGIN_COOKIE_RE.test(String(cookie || "")) || Boolean(signals.loggedInCookie);
  const loggedIn = !loginWall && (platformHint || cookieIn);
  const qrText = /扫码登录|二维码登录/.test(`${pageUrl}\n${title}\n${body}`);
  return strip({
    logged_in: loggedIn,
    login_required: !loggedIn,
    on_login_page: Boolean(loginWall || qrText),
    login_wall: loginWall || undefined,
    has_qr_hint: qrText || undefined,
    url: pageUrl || undefined,
    title: title || undefined,
  });
}

export function needsRepaint(detected = {}) {
  if (detected.platformChrome) return false;
  if (detected.onLoginWall) return false;
  const classified = classifyLogin({
    url: detected.url,
    title: detected.title,
    text: detected.text,
    signals: {
      platformChrome: detected.platformChrome,
      loggedInCookie: detected.loggedInCookie,
      onLoginWall: detected.onLoginWall,
    },
  });
  return !classified.logged_in && !classified.on_login_page;
}

export function egoMissingSummary(command = "check-login") {
  return strip({
    skill: SKILL,
    command,
    ok: false,
    logged_in: false,
    login_required: true,
    exitCode: 2,
    error: "ego-browser not found on PATH",
    login_tip: LOGIN_TIP,
    login_tip_zh: LOGIN_TIP_ZH,
    how_to_login: [
      "Install Ego Lite, then ensure `ego-browser` is on PATH (often ~/.local/bin).",
      ...HOW_TO_LOGIN,
    ],
    how_to_login_zh: [
      "先安装 Ego Lite，并把 ego-browser 放进 PATH（常见 ~/.local/bin）。",
      ...HOW_TO_LOGIN_ZH,
    ],
  });
}

export function loggedInCookieHeader(cookies) {
  if (!Array.isArray(cookies)) return "";
  const names = new Set(COOKIE_NAMES);
  const parts = [];
  for (const cookie of cookies) {
    if (!cookie || !names.has(cookie.name)) continue;
    parts.push(`${cookie.name}=1`);
  }
  return parts.join("; ");
}

export function parseLooseJson(text) {
  if (text == null || text === "") return null;
  const source = String(text);
  try {
    return JSON.parse(source);
  } catch {
    // Teambition occasionally returns unescaped control characters.
  }
  try {
    return JSON.parse(source.replace(/[\u0000-\u001F]+/g, " "));
  } catch {
    return null;
  }
}

export function parsePlanUrl(url) {
  const match = PLAN_URL_RE.exec(String(url || ""));
  if (!match) return null;
  return { projectId: match[1], planId: match[2], groupId: match[3] || "" };
}

const VALUE_FLAGS = {
  "--group": ["groupId", "--group 需要分组 ID"],
  "--title": ["title", "--title 需要标题"],
  "--precondition": ["precondition", "--precondition 需要文本"],
  "--steps-json": ["stepsJson", "--steps-json 需要 JSON 文本"],
  "--priority": ["priority", "--priority 需要整数"],
  "--executor-id": ["executorId", "--executor-id 需要成员 ID"],
  "--case-type": ["caseType", "--case-type 需要类型"],
  "--scenario-field-config-id": ["scenarioFieldConfigId", "--scenario-field-config-id 需要 ID"],
  "--flow-status-id": ["flowStatusId", "--flow-status-id 需要状态 ID"],
};

export function parseTestcaseArgs(argv) {
  const args = argv || [];
  const positional = [];
  const out = { positional, asJson: false, help: false, yes: false };
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--json") {
      out.asJson = true;
      continue;
    }
    if (arg === "--help" || arg === "-h") {
      out.help = true;
      continue;
    }
    if (arg === "--yes") {
      out.yes = true;
      continue;
    }
    const spec = VALUE_FLAGS[arg];
    if (spec) {
      const value = args[i + 1];
      const allowEmpty = arg === "--precondition";
      if (value == null || (!allowEmpty && value === "") || String(value).startsWith("--")) {
        return { error: spec[1] };
      }
      out[spec[0]] = String(value);
      i += 1;
      continue;
    }
    positional.push(arg);
  }
  return { cmd: positional[0], ...out };
}

export function buildTql(planId, groupId) {
  let tql = `_testplanId = ${planId}`;
  if (groupId) tql += ` AND groupId = ${groupId}`;
  return tql;
}

export function planEndpoint(projectId, planId, base = BASE) {
  return `${base}/testcase/api/v1/projects/${projectId}/testplans/${planId}`;
}

export function groupsEndpoint(projectId, planId, base = BASE) {
  return `${planEndpoint(projectId, planId, base)}/groups`;
}

export function buildCaseQueryUrl({
  base = BASE,
  projectId,
  tql,
  pageToken = "",
  pageSize = 100,
  needResult = true,
} = {}) {
  const params = new URLSearchParams({
    tql: String(tql ?? ""),
    pageSize: String(pageSize),
    needTestCaseResult: String(needResult !== false),
  });
  if (pageToken) params.set("pageToken", String(pageToken));
  return `${base}/testcase/api/v3/project/${projectId}/testcase/query?${params.toString()}`;
}

export function extractGroups(body) {
  if (Array.isArray(body)) return body;
  const obj = body && typeof body === "object" ? body : {};
  const result = obj.result;
  const groups = obj.groups;
  if (Array.isArray(result) && result.length > 0) return result;
  if (Array.isArray(groups) && (result == null || (Array.isArray(result) && result.length === 0))) return groups;
  if (Array.isArray(result)) return result;
  return [];
}

export function formatPlan(body, asJson = false) {
  if (asJson) return `${JSON.stringify(body ?? null, null, 2)}\n`;
  const data = (body && body.result) || {};
  const creator = (data.creator && data.creator.name) || "";
  let count = data.testcaseCount;
  if (count && typeof count === "object") count = count.total;
  const lines = [`名称: ${data.name || ""}`];
  const info = [];
  if (data.statusName || data.status) info.push(`状态: ${data.statusName || data.status}`);
  if (count) info.push(`用例数: ${count}`);
  if (creator) info.push(`创建人: ${creator}`);
  if (info.length) lines.push(info.join(" | "));
  return `${lines.join("\n")}\n`;
}

export function formatGroups(body, asJson = false) {
  const groups = extractGroups(body);
  if (asJson) return `${JSON.stringify(groups, null, 2)}\n`;
  if (!groups.length) return "";
  return `${groups.map((group) => `${group._id || ""}\t${group.resourceCount ?? 0}\t${group.name || ""}`).join("\n")}\n`;
}

export function formatCases(cases, asJson = false) {
  const list = Array.isArray(cases) ? cases : [];
  if (asJson) return { stdout: `${JSON.stringify(list, null, 2)}\n`, stderr: "" };
  const lines = list.map((item) => {
    const done = item.isDone ? "✓" : "✗";
    const group = (item.commongroup && item.commongroup.name) || "";
    const id = item.uniqueId ?? "?";
    return `#${id}\t${done}\t${group}\t${item.title || ""}`;
  });
  return {
    stdout: lines.length ? `${lines.join("\n")}\n` : "",
    stderr: `共 ${list.length} 条\n`,
  };
}

function stepUrls(step) {
  const actual = step && step.actualPayload && step.actualPayload.urls;
  if (Array.isArray(actual) && actual.length) return actual;
  const expected = step && step.expectPayload && step.expectPayload.urls;
  return Array.isArray(expected) ? expected : [];
}

export function formatCase(item, asJson = false) {
  if (asJson) return `${JSON.stringify(item, null, 2)}\n`;
  const executor = (item.executor && item.executor.name) || "-";
  const group = (item.commongroup && item.commongroup.name) || "-";
  const status = item.isDone ? "已完成" : "未完成";
  const raw = item.priority;
  const priority = raw == null ? "" : (PRIORITY[raw] ?? raw);
  const lines = [
    `#${item.uniqueId ?? "?"} ${item.title || ""}`.trimEnd(),
    `状态: ${status} | 优先级: ${priority} | 执行人: ${executor} | 分组: ${group}`,
  ];
  if (item.precondition) lines.push(`前置条件: ${item.precondition}`);
  const steps = Array.isArray(item.steps) ? item.steps : [];
  if (!steps.length) {
    lines.push("(无步骤)");
  } else {
    lines.push(`步骤 (${steps.length}):`);
    steps.forEach((step, index) => {
      lines.push(`  ${index + 1}. 操作: ${step.desc || ""}`);
      lines.push(`     预期: ${step.expected || ""}`);
      if (step.actual) lines.push(`     实际: ${step.actual}`);
      if (step.resultStatus) lines.push(`     结果: ${step.resultStatus}`);
      for (const url of stepUrls(step)) lines.push(`     截图: ${url}`);
    });
  }
  return `${lines.join("\n")}\n`;
}

export function mapBrowserError(message) {
  const text = String(message ?? "");
  if (text.includes("401")) return "未登录：请在 Ego 浏览器打开 teambition.com 登录后重试";
  return text;
}

function httpErrorDetail(body) {
  if (!body || typeof body !== "object") return "";
  const msg = body.message || body.error || body.msg;
  if (typeof msg !== "string") return "";
  const text = msg.trim();
  return text ? text.slice(0, 200) : "";
}

export function interpretFetch(payload) {
  if (!payload || typeof payload !== "object") return { error: "浏览器返回了意外结构" };
  if (payload.error) return { error: mapBrowserError(payload.error) };
  if (payload.status === 401) return { error: mapBrowserError("401 未登录") };
  if (typeof payload.status === "number" && (payload.status < 200 || payload.status >= 300)) {
    const detail = httpErrorDetail(payload.body);
    return { error: detail ? `HTTP ${payload.status}: ${detail}` : `HTTP ${payload.status}` };
  }
  return { body: payload.body };
}

export function extractTaggedJson(combined, tag = RESULT_TAG) {
  const lines = String(combined || "").split(/\n/).map((line) => line.trim()).filter(Boolean);
  for (let i = lines.length - 1; i >= 0; i--) {
    const line = lines[i];
    const at = line.indexOf(tag);
    if (at === -1) continue;
    try {
      return JSON.parse(line.slice(at + tag.length));
    } catch {
      // keep scanning
    }
  }
  return null;
}

export function resolveProcessExit(combined, code) {
  const matched = String(combined || "").match(/nodejs process exited with code (\d+)/);
  if (matched) return Number(matched[1]);
  if (code === 0) return 0;
  return code ?? 1;
}

export function missingIds(cmd, positional) {
  const ids = (positional || []).slice(1);
  if (cmd === "parse-url") return ids[0] ? null : "缺少 URL";
  if (cmd === "flow-statuses") return ids[0] ? null : "缺少 projectId";
  if (cmd === "plan" || cmd === "groups" || cmd === "cases" || cmd === "create") {
    if (!ids[0] || !ids[1]) return "缺少 projectId 或 planId";
  }
  if (cmd === "get" && (!ids[0] || !ids[1] || ids[2] == null || ids[2] === "")) return "缺少 projectId、planId 或 uniqueId";
  if ((cmd === "update" || cmd === "set-status" || cmd === "delete") && (!ids[0] || !ids[1] || ids[2] == null || ids[2] === "")) {
    return "缺少 projectId、planId 或用例 id";
  }
  return null;
}
