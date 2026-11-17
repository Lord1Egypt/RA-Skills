import assert from "node:assert/strict";
import test from "node:test";
import {
  FUTURE_DOMAINS,
  USAGE,
  buildCaseQueryUrl,
  buildTql,
  classifyLogin,
  detectSignals,
  egoMissingSummary,
  extractGroups,
  extractTaggedJson,
  formatCase,
  formatCases,
  formatGroups,
  formatPlan,
  groupsEndpoint,
  interpretFetch,
  isLoginWall,
  loggedInCookieHeader,
  mapBrowserError,
  missingIds,
  needsRepaint,
  parseCheckArgs,
  parseLooseJson,
  parsePlanUrl,
  parseTestcaseArgs,
  planEndpoint,
  resolveProcessExit,
  strip,
} from "../lib/pure.mjs";

const PROJECT = "a".repeat(24);
const PLAN = "b".repeat(24);
const GROUP = "c".repeat(24);

test("strip drops empty values and keeps zero", () => {
  assert.deepEqual(strip({ a: 0, b: false, c: "", d: null, e: undefined, f: "x" }), { a: 0, b: false, f: "x" });
});

test("parseCheckArgs accepts help, keep, and task name", () => {
  assert.equal(parseCheckArgs([]).keep, false);
  assert.equal(parseCheckArgs(["--help"]).help, true);
  assert.equal(parseCheckArgs(["-h"]).help, true);
  const named = parseCheckArgs(["--keep", "--task-name", "teambition-1"]);
  assert.equal(named.keep, true);
  assert.equal(named.taskName, "teambition-1");
  assert.equal(parseCheckArgs(["--task-name"]).taskName, "teambition-login-check");
  assert.throws(() => parseCheckArgs(["--nope"]), /Unknown arg/);
});

test("login wall, chrome, and cookie signals", () => {
  assert.equal(isLoginWall({ url: "https://account.teambition.com/login" }), true);
  assert.equal(isLoginWall({ url: "https://login.teambition.com/signin" }), true);
  assert.equal(isLoginWall({ url: "https://www.teambition.com/login?next=/" }), true);
  assert.equal(isLoginWall({ text: "请登录" }), true);
  assert.equal(isLoginWall({ url: "https://www.teambition.com/project/1", text: "我的项目" }), false);

  const signals = detectSignals({
    url: "https://www.teambition.com/",
    text: "工作台",
    cookie: "TEAMBITION_SESSIONID=secret",
  });
  assert.equal(signals.platformChrome, true);
  assert.equal(signals.onLoginWall, false);
  assert.equal(signals.loggedInCookie, true);
  assert.equal(detectSignals({ cookie: "TB_ACCESS_TOKEN=secret" }).loggedInCookie, true);
  assert.equal(detectSignals({ text: "Sign in to Teambition" }).onLoginWall, true);
});

test("classifyLogin ignores the document title and lets the wall win", () => {
  const titled = classifyLogin({ url: "https://www.teambition.com/", title: "Teambition", text: "" });
  assert.equal(titled.logged_in, false);
  assert.equal(titled.on_login_page, false);

  const wall = classifyLogin({
    url: "https://www.teambition.com/",
    text: "扫码登录",
    cookie: "TEAMBITION_SESSIONID=secret",
  });
  assert.equal(wall.logged_in, false);
  assert.equal(wall.has_qr_hint, true);
  assert.equal(wall.login_wall, true);

  const chrome = classifyLogin({ text: "测试计划\n测试用例" });
  assert.equal(chrome.logged_in, true);
  assert.equal(chrome.login_required, false);

  const cookie = classifyLogin({ signals: { loggedInCookie: true } });
  assert.equal(cookie.logged_in, true);
  const forced = classifyLogin({ signals: { onLoginWall: true, platformChrome: true } });
  assert.equal(forced.logged_in, false);
  const qr = classifyLogin({ text: "二维码登录" });
  assert.equal(qr.has_qr_hint, true);
  assert.equal(qr.logged_in, false);
});

test("needsRepaint reloads a blank page and skips a known wall or cookie", () => {
  assert.equal(needsRepaint({ platformChrome: true, text: "" }), false);
  assert.equal(needsRepaint({ onLoginWall: true, text: "扫码登录" }), false);
  assert.equal(needsRepaint({ url: "https://www.teambition.com/", title: "Teambition", text: "" }), true);
  assert.equal(needsRepaint({ loggedInCookie: true, url: "https://www.teambition.com/" }), false);
});

test("ego missing summary is a bilingual soft-fail", () => {
  const summary = egoMissingSummary("plan");
  assert.equal(summary.exitCode, 2);
  assert.equal(summary.command, "plan");
  assert.equal(summary.login_required, true);
  assert.ok(summary.how_to_login.length >= 5);
  assert.ok(summary.how_to_login_zh.length >= 5);
  assert.match(summary.login_tip, /teambition.com/);
  assert.match(summary.error, /ego-browser not found/);
});

test("cookie header keeps names and drops values", () => {
  assert.equal(loggedInCookieHeader(null), "");
  assert.equal(loggedInCookieHeader([{ name: "other", value: "nope" }, null]), "");
  const header = loggedInCookieHeader([
    { name: "TEAMBITION_SESSIONID", value: "super-secret" },
    { name: "TB_ACCESS_TOKEN", value: "also-secret" },
  ]);
  assert.equal(header, "TEAMBITION_SESSIONID=1; TB_ACCESS_TOKEN=1");
  assert.doesNotMatch(header, /secret/);
});

test("loose JSON accepts control characters and rejects garbage", () => {
  assert.equal(parseLooseJson(null), null);
  assert.equal(parseLooseJson(""), null);
  assert.deepEqual(parseLooseJson('{"a":1}'), { a: 1 });
  assert.deepEqual(parseLooseJson('{"a":"x\u0001y"}'), { a: "x y" });
  assert.equal(parseLooseJson("not-json"), null);
});

test("parsePlanUrl reads the testplan path", () => {
  const url = `https://www.teambition.com/project/${PROJECT}/testplan/${PLAN}/group/${GROUP}?x=1`;
  assert.deepEqual(parsePlanUrl(url), { projectId: PROJECT, planId: PLAN, groupId: GROUP });
  assert.equal(parsePlanUrl(`https://www.teambition.com/project/${PROJECT}/testplan/${PLAN}`).groupId, "");
  assert.equal(parsePlanUrl(`https://www.teambition.com/project/${"G".repeat(24)}/testplan/${PLAN}`), null);
  assert.equal(parsePlanUrl(""), null);
});

test("parseTestcaseArgs pulls flags out of the positional list", () => {
  const parsed = parseTestcaseArgs(["cases", PROJECT, PLAN, "--group", GROUP, "--json"]);
  assert.equal(parsed.cmd, "cases");
  assert.equal(parsed.groupId, GROUP);
  assert.equal(parsed.asJson, true);
  assert.deepEqual(parsed.positional, ["cases", PROJECT, PLAN]);
  assert.equal(parseTestcaseArgs(["--help"]).help, true);
  assert.equal(parseTestcaseArgs(["-h", "plan"]).help, true);
  assert.equal(parseTestcaseArgs(["plan", "--group"]).error, "--group 需要分组 ID");
  assert.equal(parseTestcaseArgs(["plan", "--group", "--json"]).error, "--group 需要分组 ID");
  assert.equal(parseTestcaseArgs([]).cmd, undefined);
  const write = parseTestcaseArgs([
    "create", PROJECT, PLAN,
    "--title", "标题",
    "--precondition", "",
    "--steps-json", "[]",
    "--priority", "-1",
    "--executor-id", "member",
    "--case-type", "function",
    "--scenario-field-config-id", GROUP,
    "--yes",
  ]);
  assert.equal(write.title, "标题");
  assert.equal(write.precondition, "");
  assert.equal(write.stepsJson, "[]");
  assert.equal(write.priority, "-1");
  assert.equal(write.executorId, "member");
  assert.equal(write.caseType, "function");
  assert.equal(write.scenarioFieldConfigId, GROUP);
  assert.equal(write.yes, true);
  assert.equal(parseTestcaseArgs(["update", "--title"]).error, "--title 需要标题");
  assert.equal(parseTestcaseArgs(["update", "--precondition"]).error, "--precondition 需要文本");
  assert.equal(parseTestcaseArgs(["set-status", "--flow-status-id"]).error, "--flow-status-id 需要状态 ID");
  assert.equal(parseTestcaseArgs(["create", "--steps-json", "--json"]).error, "--steps-json 需要 JSON 文本");
});

test("query URLs encode TQL and page tokens", () => {
  assert.equal(buildTql(PLAN, ""), `_testplanId = ${PLAN}`);
  assert.equal(buildTql(PLAN, GROUP), `_testplanId = ${PLAN} AND groupId = ${GROUP}`);
  assert.equal(planEndpoint(PROJECT, PLAN), `https://www.teambition.com/testcase/api/v1/projects/${PROJECT}/testplans/${PLAN}`);
  assert.equal(groupsEndpoint(PROJECT, PLAN, "https://example.test"), `https://example.test/testcase/api/v1/projects/${PROJECT}/testplans/${PLAN}/groups`);
  const first = buildCaseQueryUrl({ projectId: PROJECT, tql: buildTql(PLAN), needResult: true });
  assert.match(first, /needTestCaseResult=true/);
  assert.doesNotMatch(first, /pageToken/);
  const second = buildCaseQueryUrl({
    projectId: PROJECT,
    tql: buildTql(PLAN, GROUP),
    pageToken: "100",
    needResult: false,
  });
  assert.match(second, /pageToken=100/);
  assert.match(second, /needTestCaseResult=false/);
  assert.match(second, /groupId/);
});

test("extractGroups matches the Python falsy fallback", () => {
  assert.deepEqual(extractGroups([{ _id: "1" }]), [{ _id: "1" }]);
  assert.deepEqual(extractGroups({ result: [{ _id: "a" }] }).length, 1);
  assert.deepEqual(extractGroups({ result: [], groups: [{ _id: "b" }] }), [{ _id: "b" }]);
  assert.deepEqual(extractGroups({ result: [], groups: [] }), []);
  assert.deepEqual(extractGroups(null), []);
  assert.deepEqual(extractGroups({ result: { nope: true }, groups: [{ _id: "c" }] }), []);
});

test("formatPlan prints the fields the Python skill prints", () => {
  const text = formatPlan({
    result: {
      name: "计划",
      statusName: "进行中",
      testcaseCount: { total: 4 },
      creator: { name: "Ada" },
    },
  });
  assert.match(text, /名称: 计划/);
  assert.match(text, /状态: 进行中/);
  assert.match(text, /用例数: 4/);
  assert.match(text, /创建人: Ada/);
  const numeric = formatPlan({ result: { name: "N", status: "open", testcaseCount: 2 } });
  assert.match(numeric, /状态: open/);
  assert.match(numeric, /用例数: 2/);
  const empty = formatPlan({ result: { testcaseCount: 0 } });
  assert.equal(empty, "名称: \n");
  assert.match(formatPlan({ result: { name: "Z" } }, true), /"result"/);
  assert.match(formatPlan(null, true), /null/);
});

test("formatGroups and formatCases", () => {
  const lines = formatGroups({ result: [{ _id: "g1", resourceCount: 0, name: "登录" }] });
  assert.equal(lines, "g1\t0\t登录\n");
  assert.equal(formatGroups({ groups: [{ name: "空" }] }), "\t0\t空\n");
  assert.equal(formatGroups({}), "");
  assert.match(formatGroups([{ _id: "x" }], true), /"x"/);

  const table = formatCases([{ uniqueId: 3, isDone: true, commongroup: { name: "G" }, title: "标题" }, { title: "缺号" }]);
  assert.match(table.stdout, /#3\t✓\tG\t标题/);
  assert.match(table.stdout, /#\?\t✗\t\t缺号/);
  assert.equal(table.stderr, "共 2 条\n");
  const json = formatCases([{ uniqueId: 1 }], true);
  assert.equal(json.stderr, "");
  assert.match(json.stdout, /"uniqueId": 1/);
  assert.equal(formatCases(null).stderr, "共 0 条\n");
});

test("formatCase includes steps, priority zero, and screenshot fallback", () => {
  const text = formatCase({
    uniqueId: 8,
    title: "登录",
    isDone: false,
    priority: 0,
    executor: { name: "Ada" },
    commongroup: { name: "账号" },
    precondition: "已打开",
    steps: [
      {
        desc: "输入",
        expected: "进入",
        actual: "进入了",
        resultStatus: "passed",
        actualPayload: { urls: [] },
        expectPayload: { urls: ["https://example.test/a.png"] },
      },
      { desc: "退出", expected: "关闭", actualPayload: { urls: ["https://example.test/b.png"] } },
    ],
  });
  assert.match(text, /#8 登录/);
  assert.match(text, /未完成/);
  assert.match(text, /优先级: 紧急/);
  assert.match(text, /前置条件: 已打开/);
  assert.match(text, /步骤 \(2\)/);
  assert.match(text, /实际: 进入了/);
  assert.match(text, /结果: passed/);
  assert.match(text, /https:\/\/example.test\/a.png/);
  assert.match(text, /https:\/\/example.test\/b.png/);
  const bare = formatCase({ uniqueId: 1, priority: 9, title: "无步骤" });
  assert.match(bare, /优先级: 9/);
  assert.match(bare, /执行人: -/);
  assert.match(bare, /\(无步骤\)/);
  assert.match(formatCase({ priority: null }), /优先级:  \|/);
  assert.match(formatCase({ uniqueId: 1, title: "J" }, true), /"title": "J"/);
});

test("errors, tagged JSON, and process exit", () => {
  assert.match(mapBrowserError("401 未登录"), /未登录：请在 Ego 浏览器打开 teambition.com/);
  assert.match(mapBrowserError("HTTP 401"), /未登录/);
  assert.equal(mapBrowserError("HTTP 500"), "HTTP 500");
  assert.equal(mapBrowserError(null), "");
  assert.equal(interpretFetch(null).error, "浏览器返回了意外结构");
  assert.match(interpretFetch({ error: "401 未登录" }).error, /未登录：/);
  assert.match(interpretFetch({ status: 401, body: {} }).error, /未登录：/);
  assert.equal(interpretFetch({ status: 500 }).error, "HTTP 500");
  assert.equal(interpretFetch({ status: 400, body: { message: "标题重复" } }).error, "HTTP 400: 标题重复");
  assert.equal(interpretFetch({ status: 400, body: { message: "   " } }).error, "HTTP 400");
  assert.equal(interpretFetch({ status: 400, body: { error: { code: 1 } } }).error, "HTTP 400");
  assert.equal(interpretFetch({ status: 400, body: "nope" }).error, "HTTP 400");
  assert.equal(interpretFetch({ status: 400, body: { msg: "x".repeat(250) } }).error.length, "HTTP 400: ".length + 200);
  assert.deepEqual(interpretFetch({ status: 201, body: { ok: 1 } }), { body: { ok: 1 } });
  assert.deepEqual(interpretFetch({ status: 200, body: { ok: 1 } }), { body: { ok: 1 } });
  assert.deepEqual(interpretFetch({ body: { ok: 1 } }), { body: { ok: 1 } });

  const combined = 'TBEGO{"stdout":"ok"}\nTBEGO{"exitCode":\n';
  assert.equal(extractTaggedJson(combined).stdout, "ok");
  assert.equal(extractTaggedJson("nope"), null);
  assert.equal(extractTaggedJson(""), null);
  assert.deepEqual(extractTaggedJson("ZZ{\"a\":1}", "ZZ"), { a: 1 });

  assert.equal(resolveProcessExit("nodejs process exited with code 2", 0), 2);
  assert.equal(resolveProcessExit("ok", 0), 0);
  assert.equal(resolveProcessExit("", 7), 7);
  assert.equal(resolveProcessExit("", null), 1);
});

test("missingIds and the phase-1 usage text", () => {
  assert.equal(missingIds("parse-url", ["parse-url"]), "缺少 URL");
  assert.equal(missingIds("parse-url", ["parse-url", "https://example"]), null);
  assert.equal(missingIds("plan", ["plan", PROJECT]), "缺少 projectId 或 planId");
  assert.equal(missingIds("cases", ["cases", PROJECT, PLAN]), null);
  assert.equal(missingIds("get", ["get", PROJECT, PLAN, ""]), "缺少 projectId、planId 或 uniqueId");
  assert.equal(missingIds("get", ["get", PROJECT, PLAN, "12"]), null);
  assert.equal(missingIds("cleanup", ["cleanup"]), null);
  assert.equal(missingIds("flow-statuses", ["flow-statuses"]), "缺少 projectId");
  assert.equal(missingIds("flow-statuses", ["flow-statuses", PROJECT]), null);
  assert.equal(missingIds("create", ["create", PROJECT]), "缺少 projectId 或 planId");
  assert.equal(missingIds("create", ["create", PROJECT, PLAN]), null);
  assert.equal(missingIds("update", ["update", PROJECT, PLAN, ""]), "缺少 projectId、planId 或用例 id");
  assert.equal(missingIds("delete", ["delete", PROJECT, PLAN, "12"]), null);
  assert.equal(missingIds("set-status", ["set-status", PROJECT, PLAN, "12"]), null);
  assert.deepEqual(FUTURE_DOMAINS, ["task", "project"]);
  assert.match(USAGE, /testcase/);
  assert.match(USAGE, /teambition_cli/);
  assert.match(USAGE, /task, project/);
});
