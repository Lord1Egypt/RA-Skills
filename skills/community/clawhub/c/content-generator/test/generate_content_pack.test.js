"use strict";

const assert = require("node:assert/strict");
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const {
  generateContentPack,
  renderMarkdown,
  validateProduct
} = require("../scripts/generate_content_pack");

const fixturePath = path.join(__dirname, "fixtures", "skincare.json");
const fixture = JSON.parse(fs.readFileSync(fixturePath, "utf8"));

test("generates selected platform drafts with quality notes", () => {
  const pack = generateContentPack(fixture);

  assert.equal(pack.brief.name, "HydraGlow Cream");
  assert.ok(pack.platforms.xiaohongshu.titleOptions.length >= 3);
  assert.match(pack.platforms.douyin.spokenScript.join("\n"), /证据/);
  assert.equal(pack.platforms.marketplace.bullets.length, 3);
  assert.equal(pack.qualityNotes.evidenceStatus, "provided");
  assert.deepEqual(pack.qualityNotes.missingFields, []);
});

test("marks missing evidence and missing benefits instead of inventing claims", () => {
  const pack = generateContentPack({
    name: "Mystery Gadget",
    category: "数码",
    audience: "学生"
  });

  assert.equal(pack.qualityNotes.evidenceStatus, "missing");
  assert.ok(pack.qualityNotes.missingFields.includes("benefits"));
  assert.match(pack.platforms.xiaohongshu.body, /待补充证据/);
});

test("flags risky marketing claims", () => {
  const quality = validateProduct({
    name: "Fast Cure",
    category: "美妆",
    audience: "敏感肌",
    scenario: "日常护肤",
    benefits: ["100%治愈泛红"],
    evidence: [],
    limitations: [],
    differentiators: [],
    prohibitedClaims: []
  });

  assert.ok(quality.riskyClaims.includes("medical or body-effect claim"));
  assert.ok(quality.riskyClaims.includes("absolute or guaranteed claim"));
});

test("CLI renders markdown", () => {
  const output = execFileSync(
    process.execPath,
    ["scripts/generate_content_pack.js", "--input", fixturePath, "--format", "markdown"],
    { cwd: path.join(__dirname, ".."), encoding: "utf8" }
  );

  assert.match(output, /# HydraGlow Cream Content Pack/);
  assert.match(output, /### 小红书/);
  assert.match(output, /## Quality Notes/);
});

test("renders markdown from module API", () => {
  const markdown = renderMarkdown(generateContentPack(fixture));
  assert.match(markdown, /Platform Drafts/);
  assert.match(markdown, /HydraGlow Cream/);
});
