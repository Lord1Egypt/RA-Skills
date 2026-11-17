"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const { detectBusinessAnalysis, detectIntent, routeSkillIntent } = require("../src");

const intentCases = [
  ["growth", "收入增长放缓，帮我拆一下渠道和新增", "growth_analysis"],
  ["funnel", "注册转化率下降，找一下流失环节", "funnel_analysis"],
  ["retention", "最近续费率下降，帮我定位原因并给动作建议", "retention_analysis"],
  ["revenue", "收入和利润下滑，拆解一下毛利影响", "revenue_analysis"],
  ["efficiency", "仓库库存周转效率下降，帮我分析人效", "efficiency_analysis"],
  ["market research", "请做中国 SaaS 市场规模和竞争格局调研", "market_research"],
];

for (const [name, message, intent] of intentCases) {
  test(`routes ${name} requests to ${intent}`, () => {
    const result = routeSkillIntent(message);

    assert.equal(result.matched, true);
    assert.equal(result.intent, intent);
    assert.ok(result.confidence >= 0 && result.confidence <= 1);
    assert.equal(typeof result.promptHint, "string");
  });
}

test("keeps specific retention intent when diagnosis phrases overlap", () => {
  assert.equal(
    detectIntent("最近续费率下降，帮我定位原因并给动作建议").intent,
    "retention_analysis"
  );
});

test("resolves equal topic scores by declared priority", () => {
  assert.equal(detectIntent("GMV 收入").intent, "growth_analysis");
});

test("does not count a short keyword again when a longer phrase contains it", () => {
  assert.equal(detectIntent("只看转化率").intent, "funnel_analysis");
  assert.equal(detectIntent("只看转化率").confidence, 0.5);
});

test("does not route empty, unrelated, or technical-only requests", () => {
  assert.equal(detectBusinessAnalysis("").matched, false);
  assert.equal(routeSkillIntent("给我一点建议").matched, false);

  const technical = routeSkillIntent("帮我写代码排查接口报错");
  assert.equal(technical.matched, false);
  assert.equal(technical.intent, null);
  assert.equal(technical.promptHint, null);
});

test("accepts the documented object input and normalizes English keywords", () => {
  assert.equal(routeSkillIntent({ message: "Analyze SaaS TAM sizing" }).intent, "market_research");
  assert.equal(routeSkillIntent({ message: "Explain LTV cohort changes" }).intent, "retention_analysis");
});
