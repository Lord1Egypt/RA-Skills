import assert from "node:assert/strict";
import test from "node:test";
import {
  DELETE_CONFIRM,
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
  looksLikeObjectId,
  parseStepsJson,
  pickTestcaseFlow,
  scenarioIdFromCases,
  scenarioIdFromPlan,
  stepsForUpdate,
  stepsFromValue,
  taskflowStatusEndpoint,
  taskflowsEndpoint,
  testhubEndpoint,
  testhubIdFrom,
  usercaseFieldEndpoint,
  validateWriteConfig,
} from "../lib/write.mjs";

const PROJECT = "a".repeat(24);
const PLAN = "b".repeat(24);
const GROUP = "c".repeat(24);
const CASE_ID = "d".repeat(24);

test("object ids match _id and display numbers match uniqueId", () => {
  assert.equal(looksLikeObjectId(CASE_ID), true);
  assert.equal(looksLikeObjectId("12"), false);
  assert.equal(looksLikeObjectId(""), false);
  assert.equal(caseMatchesRef(null, "12"), false);
  assert.equal(caseMatchesRef({ uniqueId: 12 }, ""), false);
  assert.equal(caseMatchesRef({ uniqueId: 12, _id: "other" }, "12"), true);
  assert.equal(caseMatchesRef({ uniqueId: 12, _id: CASE_ID }, CASE_ID), true);
  assert.equal(caseMatchesRef({ uniqueId: CASE_ID, _id: "e".repeat(24) }, CASE_ID), false);
});

test("write URLs stay on the captured paths", () => {
  assert.equal(
    createCaseEndpoint(PROJECT, PLAN, "https://example.test"),
    `https://example.test/testcase/api/v1/projects/${PROJECT}/testplans/${PLAN}/testcases`,
  );
  assert.equal(testhubEndpoint(PROJECT), `https://www.teambition.com/testcase/api/v1/projects/${PROJECT}/testhub`);
  assert.equal(
    usercaseFieldEndpoint(PROJECT, "hub", "user", "title"),
    `https://www.teambition.com/testcase/api/v1/projects/${PROJECT}/testhubs/hub/usercases/user/title`,
  );
  assert.throws(() => usercaseFieldEndpoint(PROJECT, "hub", "user", "priority"), /未知用例字段/);
  assert.equal(
    flowStatusEndpoint(PROJECT, PLAN, CASE_ID),
    `https://www.teambition.com/testcase/api/v1/projects/${PROJECT}/testplans/${PLAN}/testcases/${CASE_ID}/flowStatusId`,
  );
  assert.equal(archiveEndpoint(CASE_ID), `https://www.teambition.com/api/testcases/${CASE_ID}/archive`);
  assert.doesNotMatch(archiveEndpoint(CASE_ID), /\/testcase\/api\//);
  assert.match(taskflowsEndpoint(PROJECT, "https://example.test"), /example\.test\/api\/projects\/.+\/taskflows\?type=testcase/);
  assert.match(taskflowStatusEndpoint("flow"), /\/api\/taskflows\/flow\/taskflowstatus$/);
});

test("steps JSON accepts objects and rejects everything else", () => {
  assert.deepEqual(parseStepsJson(null), { steps: undefined });
  assert.deepEqual(parseStepsJson(""), { steps: undefined });
  assert.equal(parseStepsJson("{").error, "--steps-json 不是合法 JSON");
  assert.equal(parseStepsJson("{}").error, "--steps-json 需要数组");
  assert.equal(parseStepsJson("[1]").error, "--steps-json 的每一步需要对象 { desc, expected }");
  assert.equal(stepsFromValue("nope").error, "--steps-json 需要数组");
  const parsed = parseStepsJson('[{"desc":"a","expected":null,"_id":"s","expectPayload":null}]');
  assert.deepEqual(parsed.steps, [{ desc: "a", expected: "", _id: "s", expectPayload: null }]);
  assert.deepEqual(coerceSteps({ stepsJson: "", steps: [{ desc: "b", expected: "c" }] }).steps, [{ desc: "b", expected: "c" }]);
  assert.equal(coerceSteps({ steps: { desc: "a" } }).error, "--steps-json 需要数组");
  assert.deepEqual(coerceSteps({}).steps, undefined);
  assert.deepEqual(stepsForUpdate(null, null), []);
  assert.deepEqual(stepsForUpdate([null, { desc: "a", expected: "b", expectPayload: { urls: ["u"] } }], { nope: true }), [
    { desc: "", expected: "", expectPayload: null },
    { desc: "a", expected: "b", expectPayload: { urls: ["u"] } },
  ]);
  assert.equal(stepsForUpdate([{ desc: "a", expected: "b" }], [{ _id: "keep" }])[0]._id, "keep");
});

test("create body defaults match the captured dialog", () => {
  const body = buildCreateBody({
    title: "标题",
    projectId: PROJECT,
    planId: PLAN,
    groupId: GROUP,
    scenarioFieldConfigId: "sfc",
    priority: 0,
    executorId: "",
    caseType: "",
    steps: [null],
  });
  assert.equal(body.priority, 0);
  assert.equal(body._executorId, null);
  assert.equal(body.caseType, null);
  assert.equal(body._testhubId, null);
  assert.deepEqual(body.steps, [{ desc: "", expected: "" }]);
  assert.deepEqual(body.customfields, []);
  const defaults = buildCreateBody({ title: "标题", projectId: PROJECT, planId: PLAN, groupId: GROUP, scenarioFieldConfigId: "sfc" });
  assert.equal(defaults.priority, -1);
  assert.equal(defaults.precondition, "");
  assert.equal(defaults._executorId, null);
});

test("plan and hub ids are read from the envelopes we saw", () => {
  assert.equal(groupIdFromPlan({ result: { _commongroupId: "g", _rootCommongroupId: "root" } }), "g");
  assert.equal(groupIdFromPlan({ result: { _rootCommongroupId: "root" } }), "root");
  assert.equal(groupIdFromPlan(null), "");
  assert.equal(groupIdFromPlan({ result: { _commongroupId: 1 } }), "");
  assert.equal(scenarioIdFromPlan({ result: { _scenariofieldconfigId: "sfc" } }), "sfc");
  assert.equal(scenarioIdFromPlan({}), "");
  assert.equal(scenarioIdFromCases(null), "");
  assert.equal(scenarioIdFromCases([{ _scenariofieldconfigId: "" }, { _scenariofieldconfigId: "sfc" }]), "sfc");
  assert.equal(testhubIdFrom({ result: { _id: "hub" } }), "hub");
  assert.equal(testhubIdFrom({ result: { _id: 1 } }), "");
  assert.deepEqual(extractNamedList([{ _id: "a" }]), [{ _id: "a" }]);
  assert.deepEqual(extractNamedList(null), []);
  assert.deepEqual(extractNamedList({ result: [{ _id: "b" }] }), [{ _id: "b" }]);
  assert.deepEqual(extractNamedList({ taskflows: [{ _id: "c" }] }, ["taskflows"]), [{ _id: "c" }]);
  assert.deepEqual(extractNamedList({ result: { taskflows: [{ _id: "d" }] } }, ["taskflows"]), [{ _id: "d" }]);
  assert.deepEqual(extractNamedList({ result: { nope: true } }, ["taskflows"]), []);
  assert.equal(pickTestcaseFlow(null), null);
  assert.equal(pickTestcaseFlow([{ name: "无 id" }]), null);
  assert.equal(pickTestcaseFlow([{ _id: "first" }, { _id: "typed", type: "testcase" }])._id, "typed");
  assert.equal(pickTestcaseFlow([{ _id: "only" }])._id, "only");
});

test("write validation is the confirm gate and the field gate", () => {
  assert.equal(validateWriteConfig({ cmd: "plan" }), null);
  assert.equal(validateWriteConfig({ cmd: "create", title: "  " }), "--title 需要标题");
  assert.equal(validateWriteConfig({ cmd: "create", title: "T", priority: "nope" }), "--priority 需要整数");
  assert.match(validateWriteConfig({ cmd: "create", title: "T", steps: ["x"] }), /每一步/);
  assert.equal(validateWriteConfig({ cmd: "create", title: "T", priority: 0 }), null);
  assert.match(validateWriteConfig({ cmd: "update" }), /至少需要/);
  assert.equal(validateWriteConfig({ cmd: "update", title: "  " }), "--title 需要标题");
  assert.equal(validateWriteConfig({ cmd: "update", steps: [] }), null);
  assert.equal(validateWriteConfig({ cmd: "update", stepsJson: "{}" }), "--steps-json 需要数组");
  assert.equal(validateWriteConfig({ cmd: "set-status", flowStatusId: "  " }), "--flow-status-id 需要状态 ID");
  assert.equal(validateWriteConfig({ cmd: "set-status", flowStatusId: "id" }), null);
  assert.equal(validateWriteConfig({ cmd: "delete" }), DELETE_CONFIRM);
  assert.equal(validateWriteConfig({ cmd: "delete", yes: true }), null);
});

test("write formatters print ids the next command needs", () => {
  assert.match(formatCreateResult(null), /已创建 #\?/);
  assert.match(formatCreateResult({ result: { uniqueId: 0, title: "零" } }), /#0 零/);
  assert.match(formatCreateResult({ result: { title: "J" } }, true), /"title": "J"/);
  const updated = formatUpdateResult();
  assert.match(updated, /已更新 #\?/);
  assert.match(formatUpdateResult({
    caseItem: { uniqueId: 3, title: "旧", _id: "i", _fromHubTestcaseId: "u" },
    testhubId: "h",
    fields: { title: { result: {} }, steps: { result: {} } },
  }, true), /"testhubId": "h"/);
  assert.match(formatStatusResult(null, "requested"), /_flowstatusId: requested/);
  assert.match(formatStatusResult({ result: { uniqueId: 4, _id: "i", _flowstatusId: "live" } }, "requested"), /live/);
  assert.match(formatStatusResult({ result: {} }, "requested", true), /"result"/);
  assert.match(formatArchiveResult(null, null), /响应未带 isArchived/);
  assert.match(formatArchiveResult({ isArchived: false, _id: "i" }, { uniqueId: 5, title: "删", _id: "case" }), /isArchived: false/);
  assert.match(formatArchiveResult({ isArchived: true }, { uniqueId: 5 }, true), /"isArchived": true/);
  assert.match(formatFlowStatuses(null, null), /任务流:/);
  assert.match(formatFlowStatuses({ name: "测试工作流", _id: "f" }, [{ _id: "s", kind: "end", name: "已通过" }], true), /已通过/);
});
