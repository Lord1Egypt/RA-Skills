import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import test from "node:test";
import { executeTestcase, renderTestcaseEntry, runTestcaseCli } from "../lib/domains/testcase.mjs";

const PROJECT = "a".repeat(24);
const PLAN = "b".repeat(24);
const GROUP = "c".repeat(24);

function sessionFrom(pages) {
  const urls = [];
  let index = 0;
  return {
    urls,
    ensured: 0,
    cleaned: 0,
    async ensureSite() { this.ensured += 1; },
    async fetch(url) {
      urls.push(url);
      const page = pages[Math.min(index, pages.length - 1)];
      index += 1;
      if (page && page.throw) throw new Error(page.throw);
      return page;
    },
    async cleanup() { this.cleaned += 1; },
  };
}

function childWith({ stdout = "", stderr = "", code = 0, error } = {}) {
  const child = new EventEmitter();
  child.stdout = new EventEmitter();
  child.stderr = new EventEmitter();
  queueMicrotask(() => {
    if (error) {
      child.emit("error", error);
      return;
    }
    if (stdout) child.stdout.emit("data", stdout);
    if (stderr) child.stderr.emit("data", stderr);
    child.emit("close", code);
  });
  return child;
}

const host = (extra = {}) => ({
  whichEgo: () => "ego-browser",
  mkdtemp: async () => "/tmp/ego-teambition-tb-test",
  fs: { writeFile: async () => {}, rm: async () => {} },
  ...extra,
});

test("cleanup and rejected commands", async () => {
  const session = sessionFrom([]);
  const closed = await executeTestcase({ cmd: "cleanup" }, { session });
  assert.equal(closed.exitCode, 0);
  assert.match(closed.stdout, /已关闭常驻浏览器空间/);
  assert.equal(session.cleaned, 1);

  const unknown = await executeTestcase({ cmd: "group-create" }, { session });
  assert.equal(unknown.exitCode, 1);
  assert.match(unknown.stderr, /未知命令/);

  const missing = await executeTestcase({ cmd: "plan" }, { session: sessionFrom([]) });
  assert.match(missing.stderr, /缺少 projectId/);

  const boom = sessionFrom([]);
  boom.cleanup = async () => { throw new Error("finish failed"); };
  const failed = await executeTestcase({ cmd: "cleanup" }, { session: boom });
  assert.match(failed.stderr, /finish failed/);
});

test("plan and groups format the browser payload", async () => {
  const plan = sessionFrom([{ status: 200, body: { result: { name: "回归", statusName: "进行中", testcaseCount: { total: 2 }, creator: { name: "Ada" } } } }]);
  const text = await executeTestcase({ cmd: "plan", projectId: PROJECT, planId: PLAN }, { session: plan });
  assert.equal(text.exitCode, 0);
  assert.match(text.stdout, /名称: 回归/);
  assert.equal(plan.ensured, 1);
  assert.match(plan.urls[0], /\/testplans\//);

  const json = await executeTestcase({ cmd: "plan", projectId: PROJECT, planId: PLAN, asJson: true }, { session: sessionFrom([{ status: 200, body: { result: { name: "J" } } }]) });
  assert.match(json.stdout, /"name": "J"/);

  const denied = await executeTestcase({ cmd: "plan", projectId: PROJECT, planId: PLAN }, { session: sessionFrom([{ status: 401, body: {} }]) });
  assert.match(denied.stderr, /未登录：请在 Ego 浏览器打开 teambition.com/);

  const http = await executeTestcase({ cmd: "groups", projectId: PROJECT, planId: PLAN }, { session: sessionFrom([{ status: 500, body: {} }]) });
  assert.match(http.stderr, /HTTP 500/);

  const groups = await executeTestcase({ cmd: "groups", projectId: PROJECT, planId: PLAN }, {
    session: sessionFrom([{ status: 200, body: { result: [], groups: [{ _id: GROUP, resourceCount: 1, name: "登录" }] } }]),
  });
  assert.equal(groups.stdout, `${GROUP}\t1\t登录\n`);
  assert.match(groups.stdout ? "" : "", /^$/);
  const groupJson = await executeTestcase({
    cmd: "groups",
    projectId: PROJECT,
    planId: PLAN,
    asJson: true,
  }, { session: sessionFrom([{ status: 200, body: [{ _id: "x", name: "A" }] }]) });
  assert.match(groupJson.stdout, /"name": "A"/);
});

test("cases paginate, and get stops when the id appears", async () => {
  const pages = [
    { status: 200, body: { result: [{ uniqueId: 1, title: "一", isDone: true, commongroup: { name: "G" } }], nextPageToken: "100" } },
    { status: 200, body: { result: [{ uniqueId: 2, title: "二", isDone: false }], nextPageToken: "" } },
  ];
  const session = sessionFrom(pages);
  const listed = await executeTestcase({ cmd: "cases", projectId: PROJECT, planId: PLAN, groupId: GROUP }, { session });
  assert.match(listed.stdout, /#1\t✓\tG\t一/);
  assert.match(listed.stdout, /#2\t✗/);
  assert.equal(listed.stderr, "共 2 条\n");
  assert.match(session.urls[0], new RegExp(`groupId`));
  assert.doesNotMatch(session.urls[0], /pageToken/);
  assert.match(session.urls[1], /pageToken=100/);

  const capped = sessionFrom([{ status: 200, body: { result: [{ uniqueId: 1, title: "x" }], nextPageToken: "next" } }]);
  const limited = await executeTestcase({ cmd: "cases", projectId: PROJECT, planId: PLAN, maxPages: 2 }, { session: capped });
  assert.equal(capped.urls.length, 2);
  assert.match(limited.stderr, /共 2 条/);

  const empty = await executeTestcase({ cmd: "cases", projectId: PROJECT, planId: PLAN }, {
    session: sessionFrom([{ status: 200, body: { result: [], nextPageToken: "100" } }]),
  });
  assert.equal(empty.stderr, "共 0 条\n");

  const json = await executeTestcase({ cmd: "cases", projectId: PROJECT, planId: PLAN, asJson: true }, {
    session: sessionFrom([{ status: 200, body: { result: [{ uniqueId: 4, title: "J" }] } }]),
  });
  assert.equal(json.stderr, "");
  assert.match(json.stdout, /"uniqueId": 4/);

  const denied = await executeTestcase({ cmd: "cases", projectId: PROJECT, planId: PLAN }, {
    session: sessionFrom([
      { status: 200, body: { result: [{ uniqueId: 1 }], nextPageToken: "100" } },
      { status: 401, body: {} },
    ]),
  });
  assert.equal(denied.stdout, "");
  assert.match(denied.stderr, /未登录/);

  const bad = await executeTestcase({ cmd: "get", projectId: PROJECT, planId: PLAN, uniqueId: "9" }, {
    session: sessionFrom([{ status: 200, body: null }]),
  });
  assert.match(bad.stderr, /响应 JSON 解析失败/);

  const missing = await executeTestcase({ cmd: "get", projectId: PROJECT, planId: PLAN, uniqueId: "9" }, {
    session: sessionFrom([{ status: 200, body: { result: [{ uniqueId: 1, title: "no" }] } }]),
  });
  assert.match(missing.stderr, /计划内未找到用例 #9/);

  const found = await executeTestcase({ cmd: "get", projectId: PROJECT, planId: PLAN, uniqueId: "2" }, {
    session: sessionFrom([
      { status: 200, body: { result: [{ uniqueId: 1, title: "skip" }], nextPageToken: "100" } },
      { status: 200, body: { result: [{ uniqueId: "2", title: "命中", isDone: true, priority: 1, precondition: "就绪", steps: [{ desc: "点", expected: "开" }] }], nextPageToken: "200" } },
    ]),
  });
  assert.match(found.stdout, /#2 命中/);
  assert.match(found.stdout, /优先级: 高/);
  assert.match(found.stdout, /前置条件: 就绪/);
  const foundSessionUrls = 2;
  assert.equal(foundSessionUrls, 2);

  const asJson = await executeTestcase({ cmd: "get", projectId: PROJECT, planId: PLAN, uniqueId: 3, asJson: true }, {
    session: sessionFrom([{ status: 200, body: { result: [{ uniqueId: 3, title: "JSON" }] } }]),
  });
  assert.match(asJson.stdout, /"title": "JSON"/);

  const http = await executeTestcase({ cmd: "cases", projectId: PROJECT, planId: PLAN }, {
    session: sessionFrom([{ status: 502, body: { result: [] } }]),
  });
  assert.match(http.stderr, /HTTP 502/);
});

test("open transport does not call page.fetch", async () => {
  const session = sessionFrom([]);
  const result = await executeTestcase({ cmd: "cases", projectId: PROJECT, planId: PLAN, transport: "open" }, { session });
  assert.equal(result.exitCode, 1);
  assert.match(result.stderr, /Phase 1/);
  assert.equal(session.urls.length, 0);
  const weird = await executeTestcase({ cmd: "plan", projectId: PROJECT, planId: PLAN, transport: "socket" }, { session });
  assert.match(weird.stderr, /Unknown transport/);
  const thrown = sessionFrom([{ throw: "page down" }]);
  const crashed = await executeTestcase({ cmd: "plan", projectId: PROJECT, planId: PLAN }, { session: thrown });
  assert.match(crashed.stderr, /page down/);
});

test("parse-url stays local and the launcher soft-fails without ego", async () => {
  const url = `https://www.teambition.com/project/${PROJECT}/testplan/${PLAN}/group/${GROUP}`;
  const parsed = await runTestcaseCli(["parse-url", url], host());
  assert.equal(parsed.stdout, `${PROJECT}\t${PLAN}\t${GROUP}\n`);
  const bare = await runTestcaseCli(["parse-url", `https://www.teambition.com/project/${PROJECT}/testplan/${PLAN}`]);
  assert.equal(bare.stdout, `${PROJECT}\t${PLAN}\t\n`);
  const bad = await runTestcaseCli(["parse-url", "https://example.test/nope"]);
  assert.match(bad.stderr, /无法解析 URL/);
  assert.equal((await runTestcaseCli(["parse-url"])).exitCode, 1);
  assert.equal((await runTestcaseCli(["--help"])).exitCode, 0);
  assert.equal((await runTestcaseCli([])).exitCode, 1);
  assert.match((await runTestcaseCli(["nope"])).stdout, /Phase 1/);
  assert.match((await runTestcaseCli(["plan", "--group"])).stderr, /--group 需要分组 ID/);
  assert.match((await runTestcaseCli(["plan", PROJECT])).stderr, /缺少 projectId/);

  let spawned = 0;
  const missing = await runTestcaseCli(["plan", PROJECT, PLAN], host({
    whichEgo: () => null,
    spawn() { spawned += 1; },
  }));
  assert.equal(missing.exitCode, 2);
  assert.match(missing.stdout, /ego-browser not found/);
  assert.equal(spawned, 0);

  const probed = await runTestcaseCli(["cleanup"], host({
    whichEgo: undefined,
    spawnSync: () => ({ error: new Error("missing") }),
    spawn() { spawned += 1; },
  }));
  assert.equal(probed.exitCode, 2);
});

test("the launcher reads a TBEGO result and reports browser failures", async () => {
  let entry = "";
  const payload = JSON.stringify({ exitCode: 0, stdout: "名称: 计划\n", stderr: "" });
  const ok = await runTestcaseCli(["plan", PROJECT, PLAN, "--json"], host({
    fs: {
      writeFile: async (_file, source) => { entry = source; },
      rm: async () => { throw new Error("rm"); },
    },
    spawn() { return childWith({ stdout: `noise\nTBEGO{bad\nTBEGO${payload}\n` }); },
  }));
  assert.equal(ok.exitCode, 0);
  assert.equal(ok.stdout, "名称: 计划\n");
  assert.match(entry, /tb-testcase api/);
  assert.match(entry, /"asJson":true/);
  assert.match(entry, new RegExp(PROJECT));
  assert.match(renderTestcaseEntry({ config: { cmd: "plan" }, runHref: "file:///run.mjs", sessionHref: "file:///ego.mjs" }), /createEgoSession/);

  const quiet = await runTestcaseCli(["cleanup"], host({
    spawn() { return childWith({ stdout: "TBEGO" + JSON.stringify({ stdout: "已关闭常驻浏览器空间\n" }), code: 0 }); },
  }));
  assert.equal(quiet.exitCode, 0);

  const lost = await runTestcaseCli(["cleanup"], host({
    spawn() { return childWith({ stdout: "no marker", code: 0 }); },
  }));
  assert.equal(lost.exitCode, 1);
  assert.match(lost.stderr, /浏览器执行失败/);

  const coded = await runTestcaseCli(["cleanup"], host({
    spawn() { return childWith({ stderr: "nodejs process exited with code 2", code: 0 }); },
  }));
  assert.equal(coded.exitCode, 2);

  const raw = await runTestcaseCli(["cleanup"], host({
    spawn() { return childWith({ code: 7 }); },
  }));
  assert.equal(raw.exitCode, 7);

  const crashed = await runTestcaseCli(["cleanup"], host({
    spawn() { return childWith({ error: new Error("ENOENT") }); },
  }));
  assert.equal(crashed.exitCode, 1);
  assert.match(crashed.stderr, /ENOENT/);

  const thrown = await runTestcaseCli(["cleanup"], host({
    spawn() { throw new Error("spawn broke"); },
  }));
  assert.match(thrown.stderr, /spawn broke/);

  const closed = await runTestcaseCli(["cleanup"], host({
    spawn() { return childWith({ code: null }); },
  }));
  assert.equal(closed.exitCode, 1);
});

const HUB = "e".repeat(24);
const USERCASE = "f".repeat(24);
const CASE_ID = "d".repeat(24);
const SFC = "1".repeat(24);
const FLOW = "2".repeat(24);

function queuedSession(pages) {
  const calls = [];
  let index = 0;
  return {
    calls,
    ensured: 0,
    async ensureSite() { this.ensured += 1; },
    async fetch(url, opts = {}) {
      calls.push({ url, method: opts.method || "GET", body: opts.body });
      const page = pages[Math.min(index, pages.length - 1)];
      index += 1;
      if (page && page.throw) throw new Error(page.throw);
      return page;
    },
  };
}

function queryPage(rows, nextPageToken = "") {
  return { status: 200, body: { result: rows, nextPageToken } };
}

test("create posts the captured testcases path and resolves missing defaults", async () => {
  const created = {
    status: 201,
    body: {
      result: {
        _id: CASE_ID,
        uniqueId: 36158,
        title: "新建",
        _fromHubTestcaseId: USERCASE,
        _flowstatusId: FLOW,
      },
    },
  };
  const direct = queuedSession([created]);
  const done = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "新建",
    groupId: GROUP,
    scenarioFieldConfigId: SFC,
    precondition: "前置",
    priority: 0,
    executorId: "member-1",
    caseType: "function",
    steps: [{ desc: "打开", expected: "看见", _id: "drop-me" }],
  }, { session: direct });
  assert.equal(done.exitCode, 0);
  assert.equal(direct.ensured, 1);
  assert.equal(direct.calls.length, 1);
  assert.equal(direct.calls[0].method, "POST");
  assert.equal(
    direct.calls[0].url,
    `https://www.teambition.com/testcase/api/v1/projects/${PROJECT}/testplans/${PLAN}/testcases`,
  );
  assert.equal(direct.calls[0].body.priority, 0);
  assert.equal(direct.calls[0].body._executorId, "member-1");
  assert.equal(direct.calls[0].body.caseType, "function");
  assert.equal(direct.calls[0].body._commongroupId, GROUP);
  assert.equal(direct.calls[0].body._scenariofieldconfigId, SFC);
  assert.equal(direct.calls[0].body._testhubId, null);
  assert.deepEqual(direct.calls[0].body.steps, [{ desc: "打开", expected: "看见" }]);
  assert.match(done.stdout, /已创建 #36158 新建/);
  assert.match(done.stdout, new RegExp(USERCASE));
  assert.match(done.stdout, new RegExp(FLOW));

  const defaults = queuedSession([created]);
  const plain = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "缺省",
    groupId: GROUP,
    scenarioFieldConfigId: SFC,
    asJson: true,
  }, { session: defaults });
  assert.equal(plain.exitCode, 0);
  assert.equal(defaults.calls[0].body.priority, -1);
  assert.equal(defaults.calls[0].body._executorId, null);
  assert.equal(defaults.calls[0].body.caseType, null);
  assert.equal(defaults.calls[0].body.precondition, "");
  assert.deepEqual(defaults.calls[0].body.steps, []);
  assert.match(plain.stdout, /"_fromHubTestcaseId"/);

  const fromPlan = queuedSession([
    { status: 200, body: { result: { _scenariofieldconfigId: SFC } } },
    created,
  ]);
  const planned = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "从计划补场景",
    groupId: GROUP,
  }, { session: fromPlan });
  assert.equal(planned.exitCode, 0);
  assert.match(fromPlan.calls[0].url, /\/testplans\/[^/]+$/);
  assert.equal(fromPlan.calls[1].method, "POST");
  assert.equal(fromPlan.calls[1].body._scenariofieldconfigId, SFC);

  const fromCase = queuedSession([
    { status: 200, body: { result: { name: "计划" } } },
    queryPage([{ _scenariofieldconfigId: SFC, title: "样例" }], "100"),
    created,
  ]);
  const sampled = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "从用例补场景",
    groupId: GROUP,
  }, { session: fromCase });
  assert.equal(sampled.exitCode, 0);
  assert.match(fromCase.calls[1].url, /needTestCaseResult=false/);
  assert.equal(fromCase.calls.length, 3);

  const rooted = queuedSession([
    { status: 200, body: { result: { _rootCommongroupId: GROUP, _scenariofieldconfigId: SFC } } },
    created,
  ]);
  const rootedResult = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "根分组",
  }, { session: rooted });
  assert.equal(rootedResult.exitCode, 0);
  assert.equal(rooted.calls[1].body._commongroupId, GROUP);

  const denied = queuedSession([{ status: 401, body: {} }]);
  const login = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "未登录",
  }, { session: denied });
  assert.match(login.stderr, /未登录：请在 Ego 浏览器打开 teambition.com/);
  assert.equal(denied.calls.some((call) => call.method === "POST"), false);

  const noGroup = queuedSession([{ status: 200, body: { result: {} } }]);
  const missingGroup = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "无分组",
  }, { session: noGroup });
  assert.match(missingGroup.stderr, /--group/);
  assert.equal(noGroup.calls.length, 1);

  const noSfc = queuedSession([
    { status: 200, body: { result: { name: "计划" } } },
    queryPage([{ title: "没有场景字段" }]),
  ]);
  const missingSfc = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "无场景",
    groupId: GROUP,
  }, { session: noSfc });
  assert.match(missingSfc.stderr, /--scenario-field-config-id/);
  assert.equal(noSfc.calls.some((call) => call.method === "POST"), false);

  const queryDenied = queuedSession([
    { status: 200, body: { result: { name: "计划" } } },
    { status: 401, body: {} },
  ]);
  const queryLogin = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "查询未登录",
    groupId: GROUP,
  }, { session: queryDenied });
  assert.match(queryLogin.stderr, /未登录/);

  const rejected = queuedSession([{ status: 400, body: { message: "标题重复" } }]);
  const http = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "坏请求",
    groupId: GROUP,
    scenarioFieldConfigId: SFC,
  }, { session: rejected });
  assert.match(http.stderr, /HTTP 400: 标题重复/);

  const empty = queuedSession([{ status: 200, body: null }]);
  const badJson = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "空响应",
    groupId: GROUP,
    scenarioFieldConfigId: SFC,
  }, { session: empty });
  assert.match(badJson.stderr, /响应 JSON 解析失败/);

  const offline = queuedSession([{ throw: "page down" }]);
  const crashed = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "崩了",
    groupId: GROUP,
    scenarioFieldConfigId: SFC,
  }, { session: offline });
  assert.match(crashed.stderr, /page down/);

  const noTitle = queuedSession([]);
  const invalid = await executeTestcase({ cmd: "create", projectId: PROJECT, planId: PLAN }, { session: noTitle });
  assert.match(invalid.stderr, /--title/);
  assert.equal(noTitle.ensured, 0);
  assert.equal(noTitle.calls.length, 0);

  const badPriority = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "优先级",
    priority: 1.5,
  }, { session: queuedSession([]) });
  assert.match(badPriority.stderr, /--priority/);

  const badSteps = await executeTestcase({
    cmd: "create",
    projectId: PROJECT,
    planId: PLAN,
    title: "步骤",
    stepsJson: "{",
  }, { session: queuedSession([]) });
  assert.match(badSteps.stderr, /不是合法 JSON/);
});

test("update uses hub usercase puts and keeps step ids", async () => {
  const row = {
    _id: CASE_ID,
    uniqueId: 42,
    title: "旧标题",
    _fromHubTestcaseId: USERCASE,
    steps: [{ _id: "step-1", desc: "旧", expected: "旧预期" }],
  };
  const hub = { status: 200, body: { result: { _id: HUB, name: "项目用例库" } } };
  const saved = { status: 200, body: { result: { _id: USERCASE } } };
  const session = queuedSession([queryPage([row]), hub, saved, saved, { status: 500, body: { message: "步骤坏了" } }]);
  const failed = await executeTestcase({
    cmd: "update",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    title: "新标题",
    precondition: "",
    steps: [
      { desc: "新操作", expected: "新预期" },
      { desc: "追加", expected: "追加预期", _id: "step-2", expectPayload: { urls: [] } },
    ],
  }, { session });
  assert.match(failed.stderr, /更新 steps 失败: HTTP 500: 步骤坏了/);
  assert.equal(session.calls[1].url, `https://www.teambition.com/testcase/api/v1/projects/${PROJECT}/testhub`);
  assert.doesNotMatch(session.calls[1].url, /\/testhubs(\/|$)/);
  assert.equal(session.calls[2].method, "PUT");
  assert.equal(session.calls[2].body.title, "新标题");
  assert.match(session.calls[2].url, new RegExp(`/testhubs/${HUB}/usercases/${USERCASE}/title$`));
  assert.equal(session.calls[3].body.precondition, "");
  assert.match(session.calls[3].url, /\/precondition$/);
  assert.equal(session.calls.length, 5);
  assert.equal(session.calls[4].body.steps[0]._id, "step-1");
  assert.equal(session.calls[4].body.steps[0].expectPayload, null);
  assert.equal(session.calls[4].body.steps[1]._id, "step-2");
  assert.deepEqual(session.calls[4].body.steps[1].expectPayload, { urls: [] });

  const okSession = queuedSession([queryPage([row]), hub, saved]);
  const titled = await executeTestcase({
    cmd: "update",
    projectId: PROJECT,
    planId: PLAN,
    uniqueId: "42",
    title: "只改标题",
    asJson: true,
  }, { session: okSession });
  assert.equal(titled.exitCode, 0);
  assert.equal(okSession.calls.length, 3);
  assert.match(titled.stdout, /"testhubId"/);
  assert.match(titled.stdout, new RegExp(HUB));

  const textSession = queuedSession([
    queryPage([{ uniqueId: 7, title: "跳过" }], "100"),
    queryPage([row]),
    hub,
    saved,
    saved,
  ]);
  const text = await executeTestcase({
    cmd: "update",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: CASE_ID,
    title: "按 _id",
    steps: [{ desc: "只一步", expected: "过" }],
  }, { session: textSession });
  assert.equal(text.exitCode, 0);
  assert.match(text.stdout, /字段: title/);
  assert.match(text.stdout, /字段: steps/);
  assert.equal(textSession.calls[3].body.title, "按 _id");
  assert.equal(textSession.calls[4].body.steps[0]._id, "step-1");

  const missing = await executeTestcase({
    cmd: "update",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "404",
    title: "没有",
  }, { session: queuedSession([queryPage([{ uniqueId: 1, _id: CASE_ID, title: "别的" }])]) });
  assert.match(missing.stderr, /计划内未找到用例 404/);

  const noHubId = await executeTestcase({
    cmd: "update",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    title: "无库",
  }, { session: queuedSession([queryPage([{ ...row, _fromHubTestcaseId: "" }])]) });
  assert.match(noHubId.stderr, /_fromHubTestcaseId/);
  assert.equal(noHubId.stderr.includes("testhub"), false);

  const noCaseId = await executeTestcase({
    cmd: "update",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    title: "无 id",
  }, { session: queuedSession([queryPage([{ uniqueId: 42, title: "无", _fromHubTestcaseId: USERCASE }])]) });
  assert.match(noCaseId.stderr, /用例缺少 _id/);

  const hubHttp = await executeTestcase({
    cmd: "update",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    precondition: "前置",
  }, { session: queuedSession([queryPage([row]), { status: 404, body: {} }]) });
  assert.match(hubHttp.stderr, /HTTP 404/);

  const hubEmpty = await executeTestcase({
    cmd: "update",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    title: "库没有 id",
  }, { session: queuedSession([queryPage([row]), { status: 200, body: { result: { name: "空" } } }]) });
  assert.match(hubEmpty.stderr, /没有返回 testhubId/);

  const queryHttp = await executeTestcase({
    cmd: "update",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    title: "查询失败",
  }, { session: queuedSession([{ status: 401, body: {} }]) });
  assert.match(queryHttp.stderr, /未登录/);

  const needsField = queuedSession([]);
  const none = await executeTestcase({
    cmd: "update",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
  }, { session: needsField });
  assert.match(none.stderr, /至少需要/);
  assert.equal(needsField.calls.length, 0);

  const blankTitle = await executeTestcase({
    cmd: "update",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    title: "  ",
  }, { session: queuedSession([]) });
  assert.match(blankTitle.stderr, /--title/);
});

test("set-status puts _flowStatusId and delete archives only with --yes", async () => {
  const row = { _id: CASE_ID, uniqueId: 42, title: "要改状态" };
  const statusSession = queuedSession([
    queryPage([{ uniqueId: 1, _id: "c".repeat(24), title: "别的" }], "100"),
    queryPage([row]),
    { status: 200, body: { result: { _id: CASE_ID, uniqueId: 42, _flowstatusId: FLOW } } },
  ]);
  const status = await executeTestcase({
    cmd: "set-status",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    flowStatusId: FLOW,
  }, { session: statusSession });
  assert.equal(status.exitCode, 0);
  assert.equal(statusSession.calls[2].method, "PUT");
  assert.deepEqual(statusSession.calls[2].body, { _flowStatusId: FLOW });
  assert.equal(
    statusSession.calls[2].url,
    `https://www.teambition.com/testcase/api/v1/projects/${PROJECT}/testplans/${PLAN}/testcases/${CASE_ID}/flowStatusId`,
  );
  assert.match(status.stdout, new RegExp(`_flowstatusId: ${FLOW}`));

  const fallback = await executeTestcase({
    cmd: "set-status",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: CASE_ID,
    flowStatusId: "fallback-status",
  }, { session: queuedSession([queryPage([row]), { status: 200, body: { result: { _id: CASE_ID } } }]) });
  assert.equal(fallback.exitCode, 0);
  assert.match(fallback.stdout, /fallback-status/);

  const json = await executeTestcase({
    cmd: "set-status",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: CASE_ID,
    flowStatusId: FLOW,
    asJson: true,
  }, { session: queuedSession([queryPage([row]), { status: 200, body: { result: { _id: CASE_ID, uniqueId: 42 } } }]) });
  assert.match(json.stdout, new RegExp(CASE_ID));

  const denied = await executeTestcase({
    cmd: "set-status",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    flowStatusId: FLOW,
  }, { session: queuedSession([queryPage([row]), { status: 401, body: {} }]) });
  assert.match(denied.stderr, /未登录/);

  const empty = await executeTestcase({
    cmd: "set-status",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    flowStatusId: FLOW,
  }, { session: queuedSession([queryPage([row]), { status: 200, body: null }]) });
  assert.match(empty.stderr, /响应 JSON 解析失败/);

  const missingFlag = queuedSession([]);
  const noFlag = await executeTestcase({
    cmd: "set-status",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    flowStatusId: "  ",
  }, { session: missingFlag });
  assert.match(noFlag.stderr, /--flow-status-id/);
  assert.equal(missingFlag.ensured, 0);

  const blocked = queuedSession([]);
  const noYes = await executeTestcase({
    cmd: "delete",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
  }, { session: blocked });
  assert.match(noYes.stderr, /--yes/);
  assert.match(noYes.stderr, /uniqueId/);
  assert.equal(blocked.calls.length, 0);
  assert.equal(blocked.ensured, 0);

  const archived = queuedSession([
    queryPage([row]),
    { status: 200, body: { _id: CASE_ID, _projectId: PROJECT, isArchived: true, updated: "2026-11-04T03:27:23.912Z" } },
  ]);
  const removed = await executeTestcase({
    cmd: "delete",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    yes: true,
  }, { session: archived });
  assert.equal(removed.exitCode, 0);
  assert.equal(archived.calls[1].method, "POST");
  assert.equal(archived.calls[1].body, undefined);
  assert.equal(archived.calls[1].url, `https://www.teambition.com/api/testcases/${CASE_ID}/archive`);
  assert.doesNotMatch(archived.calls[1].url, /\/testcase\/api\//);
  assert.match(removed.stdout, /已移到回收站 #42 要改状态/);
  assert.match(removed.stdout, /isArchived: true/);

  const quiet = await executeTestcase({
    cmd: "delete",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    yes: true,
  }, { session: queuedSession([queryPage([row]), { status: 200, body: { _id: CASE_ID } }]) });
  assert.match(quiet.stdout, /响应未带 isArchived/);

  const negative = await executeTestcase({
    cmd: "delete",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    yes: true,
    asJson: true,
  }, { session: queuedSession([queryPage([row]), { status: 200, body: { _id: CASE_ID, isArchived: false } }]) });
  assert.match(negative.stdout, /"isArchived": false/);

  const http = await executeTestcase({
    cmd: "delete",
    projectId: PROJECT,
    planId: PLAN,
    caseRef: "42",
    yes: true,
  }, { session: queuedSession([queryPage([row]), { status: 404, body: {} }]) });
  assert.match(http.stderr, /HTTP 404/);

  const missingIds = await executeTestcase({ cmd: "delete", yes: true }, { session: queuedSession([]) });
  assert.match(missingIds.stderr, /缺少 projectId、planId 或用例 id/);
});

test("flow-statuses lists the testcase taskflow", async () => {
  const session = queuedSession([
    { status: 200, body: { result: { taskflows: [
      { _id: "9".repeat(24), name: "其它", type: "task" },
      { _id: FLOW, name: "测试工作流", type: "testcase" },
    ] } } },
    { status: 200, body: { result: [
      { _id: "874", name: "待评审", kind: "start" },
      { _id: "871", name: "已通过", kind: "end" },
    ] } },
  ]);
  const listed = await executeTestcase({ cmd: "flow-statuses", projectId: PROJECT }, { session });
  assert.equal(listed.exitCode, 0);
  assert.match(session.calls[0].url, new RegExp(`/api/projects/${PROJECT}/taskflows\\?type=testcase`));
  assert.equal(session.calls[1].url, `https://www.teambition.com/api/taskflows/${FLOW}/taskflowstatus`);
  assert.match(listed.stdout, /测试工作流/);
  assert.match(listed.stdout, /874\tstart\t待评审/);

  const asJson = await executeTestcase({
    cmd: "flow-statuses",
    projectId: PROJECT,
    asJson: true,
  }, { session: queuedSession([
    { status: 200, body: [{ _id: FLOW, name: "只有 id" }] },
    { status: 200, body: { statuses: [{ _id: "s", name: "阻塞" }] } },
  ]) });
  assert.match(asJson.stdout, /"阻塞"/);

  const denied = await executeTestcase({
    cmd: "flow-statuses",
    projectId: PROJECT,
  }, { session: queuedSession([{ status: 401, body: {} }]) });
  assert.match(denied.stderr, /未登录/);

  const empty = await executeTestcase({
    cmd: "flow-statuses",
    projectId: PROJECT,
  }, { session: queuedSession([{ status: 200, body: { result: [] } }]) });
  assert.match(empty.stderr, /未找到 type=testcase 的任务流/);

  const statusHttp = await executeTestcase({
    cmd: "flow-statuses",
    projectId: PROJECT,
  }, { session: queuedSession([
    { status: 200, body: { result: [{ _id: FLOW, type: "testcase" }] } },
    { status: 500, body: { msg: "流状态失败" } },
  ]) });
  assert.match(statusHttp.stderr, /HTTP 500: 流状态失败/);

  const missing = await executeTestcase({ cmd: "flow-statuses" }, { session: queuedSession([]) });
  assert.match(missing.stderr, /缺少 projectId/);
});

test("write flags fail before ego-browser starts", async () => {
  const removed = await runTestcaseCli(["delete", PROJECT, PLAN, "12"]);
  assert.match(removed.stderr, /--yes/);
  assert.equal(removed.exitCode, 1);

  assert.match((await runTestcaseCli(["create", PROJECT, PLAN])).stderr, /--title 需要标题/);
  assert.match((await runTestcaseCli(["create", PROJECT, PLAN, "--title"])).stderr, /--title 需要标题/);
  assert.match((await runTestcaseCli(["create", PROJECT, PLAN, "--title", "T", "--steps-json", "{"])).stderr, /不是合法 JSON/);
  assert.match((await runTestcaseCli(["create", PROJECT, PLAN, "--title", "T", "--priority", "1.5"])).stderr, /--priority/);
  assert.match((await runTestcaseCli(["update", PROJECT, PLAN, "3"])).stderr, /至少需要/);
  assert.match((await runTestcaseCli(["update", PROJECT, PLAN, "3", "--title", "  "])).stderr, /--title/);
  assert.match((await runTestcaseCli(["set-status", PROJECT, PLAN, "3"])).stderr, /--flow-status-id/);
  assert.match((await runTestcaseCli(["flow-statuses"])).stderr, /缺少 projectId/);
  assert.match((await runTestcaseCli(["delete", PROJECT, PLAN])).stderr, /缺少 projectId、planId 或用例 id/);
  assert.match((await runTestcaseCli(["group-create", PROJECT, PLAN])).stdout, /Phase 2a/);

  let entry = "";
  let spawned = 0;
  const launched = await runTestcaseCli([
    "delete", PROJECT, PLAN, "12", "--yes", "--json",
  ], host({
    fs: {
      writeFile: async (_file, source) => { entry = source; },
      rm: async () => {},
    },
    spawn() {
      spawned += 1;
      return childWith({ stdout: `TBEGO${JSON.stringify({ exitCode: 0, stdout: "已移到回收站\n", stderr: "" })}` });
    },
  }));
  assert.equal(launched.exitCode, 0);
  assert.equal(spawned, 1);
  assert.match(entry, /"yes":true/);
  assert.match(entry, /"cmd":"delete"/);
  assert.match(entry, /"caseRef":"12"/);
});
