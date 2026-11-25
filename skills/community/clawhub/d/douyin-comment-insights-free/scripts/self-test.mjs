#!/usr/bin/env node

import assert from "node:assert/strict";
import { access, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { execFile } from "node:child_process";
import os from "node:os";
import path from "node:path";
import { promisify } from "node:util";
import {
  extractVisibleComments,
  normalizeSnapshot,
  selectBrowser,
  toMarkdown,
  validateBridgeBase,
  validateUrl,
} from "./douyin-comment-insights-free.mjs";

const root = path.resolve(import.meta.dirname, "..");
const load = async (name) => JSON.parse(await readFile(path.join(root, "fixtures", name), "utf8"));
const run = promisify(execFile);
const temp = await mkdtemp(path.join(os.tmpdir(), "douyin-comment-insights-test-"));
let assertions = 0;
const check = async (name, fn) => {
  try {
    await fn();
    assertions += 1;
  } catch (error) {
    error.message = `${name}: ${error.message}`;
    throw error;
  }
};

try {
  const input = validateUrl("https://www.douyin.com/video/1234567890123456789?from=share");
  const success = await load("success-visible-snapshot.json");
  const syntheticPhone = ["13800", "138000"].join("");
  const syntheticEmail = ["test@", "example.com"].join("");
  const sensitiveSuccess = {
    ...success,
    comments: [...success.comments, { text: `联系我 ${syntheticPhone} 领取资料，别公开发邮箱 ${syntheticEmail}` }],
  };
  const report = normalizeSnapshot(input, sensitiveSuccess, {
    mode: "mock",
    capturedAt: "2026-09-08T00:00:00.000Z",
    limit: 20,
  });

  await check("canonicalizes a single work URL", () => {
    assert.equal(input.input, "https://www.douyin.com/video/1234567890123456789");
    assert.throws(() => validateUrl("https://www.douyin.com/search/评论"), /只接受/);
    assert.throws(() => validateUrl("http://www.douyin.com/video/1234567890123456789"), /HTTPS/);
  });
  await check("Bridge accepts loopback only and page identity fails closed", () => {
    assert.equal(validateBridgeBase("http://127.0.0.1:17777"), "http://127.0.0.1:17777");
    assert.equal(validateBridgeBase("http://[::1]:17777/"), "http://[::1]:17777");
    for (const value of ["https://example.com", "http://user:pass@127.0.0.1:17777", "http://127.0.0.1:17777/api", "http://127.0.0.1:17777/?x=1"]) assert.throws(() => validateBridgeBase(value));
    assert.throws(() => normalizeSnapshot(input, { ...success, url: undefined }, { mode: "real" }), /缺少最终 URL/);
  });
  await check("extracts visible comments without author metadata", () => {
    assert.equal(extractVisibleComments(success).length, 4);
    assert.equal(report.source.mode, "mock");
    assert.equal(report.sample.comments[0].index, 1);
    assert.equal(Object.hasOwn(report.sample.comments[0], "author"), false);
  });
  await check("classifies evidence into needs, questions and objections", () => {
    assert(report.insights.needs.length > 0);
    assert(report.insights.questions.length > 0);
    assert(report.insights.objections.length > 0);
    assert(report.insights.replyDrafts.every((draft) => draft.draft && draft.evidenceIndexes.length > 0));
  });
  await check("redacts sensitive values before JSON or Markdown output", () => {
    assert.equal(report.privacy.redacted, true);
    assert(report.privacy.redactions.some((item) => item.type === "phone"));
    assert(!JSON.stringify(report).includes(syntheticPhone));
    assert(!toMarkdown(report).includes(syntheticPhone));
    assert(toMarkdown(report).includes("mock（本地 fixture）"));
  });
  await check("selects one browser and requires explicit choice for many", () => {
    const one = [{ browserId: "browser-a", displayName: "账号 A", online: true }];
    const two = [...one, { browserId: "browser-b", displayName: "账号 B", online: true }];
    assert.equal(selectBrowser(one).browserId, "browser-a");
    assert.equal(selectBrowser(two, "browser-b").browserId, "browser-b");
    assert.throws(() => selectBrowser(two), /多个在线浏览器/);
    assert.throws(() => selectBrowser([]), /没有在线浏览器/);
  });
  await check("blocks login gates and empty comment pages", async () => {
    const blocked = await load("failure-login-gate.json");
    assert.throws(() => normalizeSnapshot(input, blocked, { mode: "mock" }), /登录|验证/);
    const empty = await load("failure-no-comments.json");
    assert.throws(() => normalizeSnapshot(input, empty, { mode: "mock" }), /没有可见评论/);
  });

  const output = path.join(temp, "success");
  const mockFile = path.join(temp, "success.json");
  await writeFile(mockFile, JSON.stringify(sensitiveSuccess));
  await run(process.execPath, [
    path.join(root, "scripts", "douyin-comment-insights-free.mjs"),
    "inspect",
    "--url",
    input.input,
    "--mock",
    mockFile,
    "--output",
    output,
  ]);
  await check("CLI writes the JSON and Markdown contract", async () => {
    const json = await readFile(path.join(output, "douyin-comment-insights.json"), "utf8");
    const markdown = await readFile(path.join(output, "douyin-comment-insights.md"), "utf8");
    const parsed = JSON.parse(json);
    assert.equal(parsed.status, "success");
    assert.equal(parsed.source.mode, "mock");
    assert(markdown.includes("## 原话证据（已脱敏）"));
    assert(!json.includes(syntheticPhone));
  });

  const failureOutput = path.join(temp, "failure");
  const failureFile = path.join(temp, "failure.json");
  await writeFile(failureFile, JSON.stringify(await load("failure-login-gate.json")));
  await mkdir(failureOutput, { recursive: true });
  await writeFile(path.join(failureOutput, "douyin-comment-insights.json"), "stale");
  await assert.rejects(
    run(process.execPath, [
      path.join(root, "scripts", "douyin-comment-insights-free.mjs"),
      "inspect",
      "--url",
      input.input,
      "--mock",
      failureFile,
      "--output",
      failureOutput,
    ]),
    (error) => error.code === 1 && !/token|cookie|authorization|browserId|session/i.test(error.stderr),
  );
  await check("CLI removes stale success output and writes a bounded diagnostic", async () => {
    await assert.rejects(access(path.join(failureOutput, "douyin-comment-insights.json")));
    const diagnostic = JSON.parse(await readFile(path.join(failureOutput, "run-diagnostic.json"), "utf8"));
    assert.equal(diagnostic.status, "needs_user_action");
    assert.equal(diagnostic.reason, "page_access_requires_user_action");
    assert(!JSON.stringify(diagnostic).includes(os.homedir()));
  });

  console.log(JSON.stringify({ status: "passed", assertions, network: "not_used", mode: "mock-only", tempCleaned: true }));
} finally {
  await rm(temp, { recursive: true, force: true });
}
