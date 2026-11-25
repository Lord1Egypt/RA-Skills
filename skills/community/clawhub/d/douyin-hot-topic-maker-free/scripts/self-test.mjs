import assert from "node:assert/strict";
import { access, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import os from "node:os";
import path from "node:path";
import { bridgeCommandPayload, HOT_EXTRACT, normalizeSnapshot, renderPlan, SEARCH_EXTRACT, selectBrowser, validateBridgeBase, validateDraft, validateRequest } from "./douyin-hot-topic-maker-free.mjs";

const root = path.resolve(import.meta.dirname, "..");
const run = promisify(execFile);
const load = async (name) => JSON.parse(await readFile(path.join(root, "fixtures", name), "utf8"));
const temp = await mkdtemp(path.join(os.tmpdir(), "douyin-hot-topic-test-"));
let checks = 0;
const test = async (name, fn) => {
  try {
    await fn();
    checks++;
  } catch (error) {
    error.message = `${name}: ${error.message}`;
    throw error;
  }
};

try {
  const request = validateRequest(await load("request-valid.json"));
  const hot = await load("hot-page-success.json");
  const search = await load("search-page-success.json");
  const snapshot = normalizeSnapshot(request, hot, [search], "2026-09-07T00:00:00.000Z");
  const draft = await load("plan-draft-valid.json");

  await test("MIT-0 metadata and first-party editable icon assets agree", async () => {
    const manifest = await readFile(path.join(root, "manifest.yaml"), "utf8");
    const packageJson = JSON.parse(await readFile(path.join(root, "package.json"), "utf8"));
    const svg = await readFile(path.join(root, "assets", "icon-source.svg"), "utf8");
    const rootIcon = await readFile(path.join(root, "icon-512.png"));
    const assetIcon = await readFile(path.join(root, "assets", "icon-512.png"));
    assert.match(manifest, /license: "MIT-0"/);
    assert.equal(packageJson.license, "MIT-0");
    assert.match(manifest, /icon: "icon-512\.png"/);
    assert.match(svg, /<svg[\s>]/);
    assert.deepEqual(rootIcon, assetIcon);
    assert.deepEqual([...rootIcon.subarray(0, 8)], [137, 80, 78, 71, 13, 10, 26, 10]);
  });

  await test("request fixes output at five plans", () => {
    assert.equal(request.planCount, 5);
    assert.equal(request.browserId, null);
    assert.throws(() => validateRequest({ ...request, planCount: 3 }), /fixed at 5/);
  });

  await test("Bridge URL is loopback-only and page extraction excludes hidden cards", () => {
    assert.equal(validateBridgeBase("http://127.0.0.1:17777"), "http://127.0.0.1:17777");
    assert.equal(validateBridgeBase("http://[::1]:17777/"), "http://[::1]:17777");
    for (const value of ["https://example.com", "http://user:pass@127.0.0.1:17777", "http://127.0.0.1:17777/api", "http://127.0.0.1:17777/?x=1"]) assert.throws(() => validateBridgeBase(value));
    const anchor = (title, visible) => ({ innerText: title, href: `https://www.douyin.com/video/${visible ? "1" : "2"}`, getBoundingClientRect: () => ({ width: visible ? 20 : 0, height: 20 }), closest: (selector) => selector === "div" ? { innerText: `热点 ${title}` } : null });
    const nodes = [anchor("显示内容", true), anchor("隐藏推荐", false)];
    const document = { body: { innerText: "热点" }, querySelectorAll: (selector) => selector.includes("/video/") ? nodes : [] };
    const location = { href: "https://www.douyin.com/hot", pathname: "/hot" };
    const extractHot = new Function("document", "location", "getComputedStyle", `return ${HOT_EXTRACT}`)(document, location, () => ({ display: "block", visibility: "visible" }));
    assert.equal(extractHot.items.length, 1);
    assert.equal(extractHot.items[0].title, "显示内容");
    const searchCard = { innerText: "显示搜索结果\n@作者", getBoundingClientRect: () => ({ width: 20, height: 20 }), closest: () => null, querySelector: () => null };
    const searchDoc = { ...document, querySelector: () => null, querySelectorAll: (selector) => selector === ".search-result-card" ? [searchCard] : [] };
    const extractSearch = new Function("document", "location", "getComputedStyle", `return ${SEARCH_EXTRACT}`)(searchDoc, { href: "https://www.douyin.com/jingxuan/search/ai", pathname: "/jingxuan/search/ai" }, () => ({ display: "block", visibility: "visible" }));
    assert.equal(extractSearch.items.length, 1);
  });

  await test("browser selection is automatic only when unambiguous", () => {
    const one = [{ browserId: "browser-a", displayName: "账号 A", online: true }];
    const two = [...one, { browserId: "browser-b", displayName: "账号 B", online: true }];
    assert.equal(selectBrowser(request, one).browserId, "browser-a");
    assert.throws(() => selectBrowser(request, two), /multiple browsers/);
    assert.equal(selectBrowser({ ...request, browserId: "browser-b" }, two).displayName, "账号 B");
    assert.throws(() => selectBrowser({ ...request, browserId: "missing" }, two), /not online/);
  });

  await test("snapshot keeps visible evidence per page", () => {
    const duplicate = snapshot.sources.find((source) => source.evidence.length === 2);
    assert.equal(snapshot.status, "success");
    assert.equal(snapshot.sources.length, 4);
    assert(snapshot.sources.every((source) => source.sourceId.startsWith(snapshot.runId)));
    assert.deepEqual(duplicate.evidence.map((item) => item.sourceType), ["hot-page", "keyword-search"]);
    assert.equal(duplicate.evidence[1].author, "测试作者");
    assert.deepEqual(duplicate.evidence[1].visibleMetricsText, ["1.2万赞"]);
  });

  draft.sourceRunId = snapshot.runId;
  draft.snapshotId = snapshot.accountBinding.snapshotId;
  draft.accountAlias = snapshot.accountAlias;
  const sourceForTitle = (title) => snapshot.sources.find((source) => source.evidence.some((item) => item.title === title)).sourceId;
  draft.plans[0].sourceIds = [sourceForTitle("把会议纪要变成行动清单")];
  draft.plans[1].sourceIds = [sourceForTitle("一人公司的自动化工作流")];
  draft.plans[2].sourceIds = [sourceForTitle("没有代码也能搭小工具")];
  draft.plans[3].sourceIds = [sourceForTitle("AI 工具如何少走弯路")];
  draft.plans[4].sourceIds = [sourceForTitle("一人公司的自动化工作流"), sourceForTitle("把会议纪要变成行动清单")];
  const { finalPlan, markdown } = renderPlan(snapshot, draft);

  await test("final output contains sources and five usable topics", () => {
    assert.equal(finalPlan.plans.length, 5);
    assert.equal(finalPlan.sources.length, 4);
    assert(finalPlan.plans.every((plan) => plan.title && plan.hook3s && plan.angle && plan.accountFit && plan.outline.length === 3 && plan.sourceIds.length));
    assert(!JSON.stringify(finalPlan).match(/browserId|token|cookie|session/i));
    assert(markdown.includes("## 本次可见来源"));
    assert(markdown.includes("- 三段提纲："));
    assert(markdown.includes("- 来源引用："));
  });

  await test("blocked and empty pages stop collection", async () => {
    assert.equal(normalizeSnapshot(request, await load("failure-captcha.json")).status, "needs_user_action");
    assert.equal(normalizeSnapshot(request, { pageText: "热点", items: [] }).reason, "hot_page_evidence_unavailable");
  });

  await test("request boundaries reject malformed inputs", () => {
    const badRequests = [
      { runtime: "other" },
      { runtime: "easy-webbridge", accountAlias: "a", accountProfile: { niche: "", audience: "a", contentPillars: [] } },
      { ...request, planCount: 9 },
      { ...request, searchLimitPerKeyword: 21 }
    ];
    for (const bad of badRequests) assert.throws(() => validateRequest(bad), /must|required|fixed/);
  });

  await test("account and source binding cannot cross environments", () => {
    const crossAccount = structuredClone(draft);
    crossAccount.accountAlias = "other-account";
    assert.throws(() => validateDraft(snapshot, crossAccount), /bound/);
    const foreignSource = structuredClone(draft);
    foreignSource.plans[0].sourceIds = ["another-run-src-001"];
    assert.throws(() => validateDraft(snapshot, foreignSource), /outside/);
  });

  await test("high-risk claims and traffic promises are blocked", () => {
    const highRisk = structuredClone(draft);
    highRisk.plans[0].title = "医疗政策已经确认";
    assert.throws(() => validateDraft(snapshot, highRisk), /high-risk/);
    const promise = structuredClone(draft);
    promise.plans[0].hook3s = "这样做保证流量和转化";
    assert.throws(() => validateDraft(snapshot, promise), /prohibited/);
  });

  await test("Bridge command keeps the session inside args", () => {
    const session = "skill-factory-douyin-hot-topic-maker-free-run-fixture-a";
    const payload = bridgeCommandPayload("navigate", { url: "https://www.douyin.com/hot" }, session);
    assert.equal(payload.action, "navigate");
    assert.equal(payload.args.session, session);
    assert.equal(Object.hasOwn(payload, "session"), false);
    assert.equal(bridgeCommandPayload("close_session", {}, session).action, "close_session");
    assert.equal(Object.hasOwn(bridgeCommandPayload("navigate", { url: "https://www.douyin.com/hot" }, session).args, "active"), false);
  });

  await test("CLI validation failure removes stale success files", async () => {
    const output = path.join(temp, "cli");
    const crossAccount = structuredClone(draft);
    crossAccount.accountAlias = "other-account";
    await mkdir(output, { recursive: true });
    await writeFile(path.join(temp, "cross.json"), JSON.stringify(crossAccount));
    await writeFile(path.join(temp, "snapshot.json"), JSON.stringify(snapshot));
    await writeFile(path.join(output, "publishable-plan.json"), "old");
    await writeFile(path.join(output, "research-snapshot.json"), "old");
    await assert.rejects(
      run(process.execPath, [path.join(root, "scripts", "douyin-hot-topic-maker-free.mjs"), "validate-plan", "--snapshot", path.join(temp, "snapshot.json"), "--draft", path.join(temp, "cross.json"), "--output", output]),
      (error) => error.code === 2 && !/other-account|session|token/i.test(error.stderr)
    );
    const report = JSON.parse(await readFile(path.join(output, "run-diagnostic.json"), "utf8"));
    assert.equal(report.status, "needs_user_action");
    await assert.rejects(access(path.join(output, "publishable-plan.json")));
    await assert.rejects(access(path.join(output, "research-snapshot.json")));
  });

  console.log(JSON.stringify({ status: "passed", assertions: checks, network: "blocked-by-design", tempCleaned: true }));
} finally {
  await rm(temp, { recursive: true, force: true });
}
