import assert from "node:assert/strict";
import { access, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import {
  analyzeSnapshot,
  bridgeCommandPayload,
  extractCode,
  normalizeSnapshot,
  pageMatchesExpected,
  renderHtml,
  renderMarkdown,
  scanSensitive,
  selectBrowser,
  validateRequest,
} from "./douyin-competitor-research-free.mjs";

const root = path.resolve(import.meta.dirname, "..");
const run = promisify(execFile);
const load = async (name) => JSON.parse(await readFile(path.join(root, "fixtures", name), "utf8"));
const temp = await mkdtemp(path.join(os.tmpdir(), "douyin-competitor-research-"));
let checks = 0;
const test = async (name, fn) => {
  try { await fn(); checks++; } catch (error) { error.message = `${name}: ${error.message}`; throw error; }
};

try {
  const request = validateRequest(await load("request-valid.json"));
  const invalidRequest = await load("request-invalid.json");
  const fixture = await load("visible-snapshot-success.json");
  const snapshot = normalizeSnapshot(request, fixture.pages, fixture.capturedAt);
  const report = analyzeSnapshot(snapshot);

  await test("request accepts mock and bounds sample inputs", () => {
    assert.equal(request.runtime, "mock");
    assert.equal(request.sampleLimit, 8);
    assert.throws(() => validateRequest(invalidRequest), /accountAlias/);
  });

  await test("snapshot records structure without original copy", () => {
    assert.equal(snapshot.status, "success");
    assert.equal(snapshot.runtime, "mock");
    assert.equal(snapshot.samples.length, 4);
    assert(snapshot.samples.every((sample) => sample.evidence.originalTextStored === false));
    assert.equal(JSON.stringify(snapshot).includes("3步把会议整理成行动清单"), false);
    assert.equal(snapshot.samples[0].contentType, "视频");
    assert.equal(snapshot.samples[1].contentType, "图文");
  });

  await test("analysis contains matrix, hooks, evidence, opportunities and ideas", () => {
    assert.equal(report.kind, "douyin-competitor-research");
    assert.equal(report.sampleCount, 4);
    assert.equal(report.matrix.length, 4);
    assert(report.hookStructures.length >= 2);
    assert(report.differentiationOpportunities.length >= 2);
    assert.equal(report.topicSuggestions.length, 3);
    assert.equal(report.safeguards.backendDataInferred, false);
    assert.equal(JSON.stringify(report).includes("3步把会议整理成行动清单"), false);
    assert(!renderMarkdown(report).includes("不会代码也能做小工具吗"));
    const html = renderHtml(report);
    assert(html.includes('id="filter"'));
    assert(html.includes('id="matrix"'));
  });

  await test("sample limit is global and audience niche are retained", () => {
    const limited = normalizeSnapshot({ ...request, sampleLimit: 2, audience: "独立开发者", niche: "AI 工具" }, fixture.pages, fixture.capturedAt);
    assert.equal(limited.samples.length, 2);
    assert.equal(limited.query.audience, "独立开发者");
    assert.equal(limited.query.niche, "AI 工具");
    assert.equal(pageMatchesExpected("https://www.douyin.com/user/example", "account"), true);
    assert.equal(pageMatchesExpected("https://www.douyin.com/jingxuan/search/AI?type=general", "keyword-search"), true);
    assert.equal(pageMatchesExpected("https://www.douyin.com/", "account"), false);
    const duplicated = normalizeSnapshot({ ...request, sampleLimit: 8 }, [{ ...fixture.pages[0], items: [...fixture.pages[0].items, fixture.pages[0].items[0]] }], fixture.capturedAt);
    assert.equal(duplicated.samples.length, fixture.pages[0].items.length);
  });

  await test("sensitive scan catches secrets but allows public evidence", () => {
    assert.deepEqual(scanSensitive({ sourceUrl: "https://www.douyin.com/video/1", visibleMetricsText: ["1.2万赞"] }), []);
    assert(scanSensitive({ token: "FAKE_SECRET_VALUE" }).length > 0);
    assert.throws(() => analyzeSnapshot({ ...snapshot, secret: "FAKE_SECRET_VALUE" }), /sensitive/);
  });

  await test("browser selection is unambiguous", () => {
    const one = [{ browserId: "browser-a", online: true }];
    const two = [...one, { browserId: "browser-b", online: true }];
    assert.equal(selectBrowser(one).browserId, "browser-a");
    assert.throws(() => selectBrowser(two), /multiple browsers/);
    assert.equal(selectBrowser(two, "browser-b").browserId, "browser-b");
    assert.throws(() => selectBrowser(two, "missing"), /not online/);
  });

  await test("bridge payload carries session only inside command args", () => {
    const payload = bridgeCommandPayload("navigate", { url: "https://www.douyin.com/user/fixture" }, "fixture-session");
    assert.equal(payload.args.session, "fixture-session");
    assert.equal(Object.hasOwn(payload, "session"), false);
  });

  await test("real browser extraction code is self-contained", () => {
    const code = extractCode("account", null);
    assert(code.includes('sourceType: "account"'));
    assert(code.includes("imageAlt"));
    assert(!code.includes("JSON.stringify(expected)"));
  });

  await test("blocked fixture stops without producing a snapshot", async () => {
    const blocked = normalizeSnapshot(request, (await load("visible-snapshot-blocked.json")).pages, "2026-09-08T02:00:00.000Z");
    assert.equal(blocked.status, "needs_user_action");
    assert.equal(blocked.reason, "account_blocked");
  });

  await test("CLI mock collect and analyze create the contract", async () => {
    const output = path.join(temp, "cli");
    await mkdir(output, { recursive: true });
    await run(process.execPath, [path.join(root, "scripts", "douyin-competitor-research-free.mjs"), "collect", "--request", path.join(root, "fixtures", "request-valid.json"), "--input", path.join(root, "fixtures", "visible-snapshot-success.json"), "--output", output]);
    await run(process.execPath, [path.join(root, "scripts", "douyin-competitor-research-free.mjs"), "analyze", "--snapshot", path.join(output, "research-snapshot.json"), "--output", output]);
    const generated = JSON.parse(await readFile(path.join(output, "competitor-research.json"), "utf8"));
    assert.equal(generated.status, "ready_for_human_review");
    assert.equal(generated.runtime, "mock");
    await access(path.join(output, "competitor-research.md"));
    await access(path.join(output, "competitor-research.html"));
  });

  await test("CLI blocked collect writes only a diagnostic", async () => {
    const output = path.join(temp, "blocked");
    await mkdir(output, { recursive: true });
    await writeFile(path.join(output, "research-snapshot.json"), "stale");
    await run(process.execPath, [path.join(root, "scripts", "douyin-competitor-research-free.mjs"), "collect", "--request", path.join(root, "fixtures", "request-valid.json"), "--input", path.join(root, "fixtures", "visible-snapshot-blocked.json"), "--output", output]).catch((error) => assert.equal(error.code, 1));
    const diagnostic = JSON.parse(await readFile(path.join(output, "run-diagnostic.json"), "utf8"));
    assert.equal(diagnostic.status, "needs_user_action");
    await assert.rejects(access(path.join(output, "research-snapshot.json")));
  });

  await test("invalid request also clears stale success output", async () => {
    const output = path.join(temp, "invalid-request");
    await mkdir(output, { recursive: true });
    await writeFile(path.join(output, "competitor-research.json"), "stale");
    await run(process.execPath, [path.join(root, "scripts", "douyin-competitor-research-free.mjs"), "collect", "--request", path.join(root, "fixtures", "request-invalid.json"), "--output", output]).catch((error) => assert.equal(error.code, 2));
    const diagnostic = JSON.parse(await readFile(path.join(output, "run-diagnostic.json"), "utf8"));
    assert.equal(diagnostic.status, "needs_user_action");
    await assert.rejects(access(path.join(output, "competitor-research.json")));
  });

  console.log(JSON.stringify({ status: "passed", assertions: checks, network: "mock-only", originalTextStored: false, tempCleaned: true }));
} finally {
  await rm(temp, { recursive: true, force: true });
}
