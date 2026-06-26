#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, AlignmentType } = require("docx");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function safe(value, fallback = "") {
  return value == null ? fallback : String(value);
}

function csvEscape(value) {
  const str = safe(value);
  if (str.includes(",") || str.includes("\"") || str.includes("\n")) return `"${str.replace(/"/g, "\"\"")}"`;
  return str;
}

function avg(values) {
  return values.reduce((sum, value) => sum + value, 0) / Math.max(values.length, 1);
}

function getCandidate(payload) {
  return payload.candidate_compensation_context || payload.candidate;
}

function getBand(payload) {
  return payload.internal_company_data?.band || payload.band || null;
}

function getBudget(payload) {
  return payload.internal_company_data?.budget_range || payload.budget_range || null;
}

function getPeers(payload) {
  return payload.internal_company_data?.same_level_employees || payload.internal_reference?.same_level_employees || [];
}

function getMarket(payload) {
  return payload.paid_survey_data || payload.market_benchmark || null;
}

function classifyBandPosition(value, band) {
  if (value < band.monthly_base_min) return "低于 band 下限";
  if (value <= band.monthly_base_mid) return "位于 band 下半段";
  if (value <= band.monthly_base_max) return "位于 band 上半段";
  return "高于 band 上限";
}

function buildDecision(payload) {
  const candidate = getCandidate(payload);
  const band = getBand(payload);
  const market = getMarket(payload);
  const budget = getBudget(payload);
  const peers = getPeers(payload);
  const expected = candidate.expected_monthly_base;
  const internalAvg = peers.length ? avg(peers.map((x) => x.monthly_base)) : 0;

  const evidence = {
    has_band: Boolean(band),
    has_paid_survey_data: Boolean(payload.paid_survey_data || payload.market_benchmark),
    has_internal_reference: peers.length > 0,
    has_budget: Boolean(budget),
    has_current_pay: candidate.current_monthly_base != null,
    has_public_market_signal: Boolean(payload.public_market_signal)
  };

  const missing = [];
  if (!evidence.has_band) missing.push("缺少 band");
  if (!evidence.has_internal_reference) missing.push("缺少内部同岗同级参考");
  if (!evidence.has_budget) missing.push("缺少预算范围");
  if (!evidence.has_current_pay) missing.push("缺少候选人当前薪资或总包口径");
  if (!evidence.has_paid_survey_data) missing.push("缺少正式市场调研分位点");

  const recommendationStrength = evidence.has_band && evidence.has_internal_reference && evidence.has_budget && evidence.has_current_pay && evidence.has_paid_survey_data
    ? "正式建议"
    : evidence.has_band
      ? "弱建议"
      : "仅市场信号判断";

  const bandPosition = band ? classifyBandPosition(expected, band) : "缺少 band，无法判断位置";
  const risks = [];
  if (band && expected > band.monthly_base_max) risks.push("候选人期望高于当前 band 上限");
  if (market && expected > market.p75) risks.push("候选人期望高于市场 P75");
  if (internalAvg && expected > internalAvg * 1.08) risks.push("候选人期望明显高于内部同级平均水平");
  if (budget && expected > budget.max) risks.push("候选人期望高于当前预算上限");
  if (!evidence.has_paid_survey_data) risks.push("当前缺少正式市场调研分位点，仅能参考公开市场信号或内部口径");

  let recommendation = "当前信息不足，建议先补充 band、市场分位和内部参考后再做正式定薪判断";
  let suggestedBase = expected;
  if (band) {
    recommendation = "建议按 band 中高位定薪";
    suggestedBase = Math.min(Math.max(expected, band.monthly_base_mid), band.monthly_base_max);
    if (expected > band.monthly_base_max) {
      recommendation = "建议控制在 band 上限附近，必要时用一次性激励补足";
      suggestedBase = band.monthly_base_max;
    } else if (expected < band.monthly_base_mid) {
      recommendation = "建议按 band 中位附近定薪，保留一定调薪空间";
      suggestedBase = Math.max(expected, band.monthly_base_mid);
    }
  }

  return {
    recommendation,
    suggestedBase,
    bandPosition,
    internalAvg: Math.round(internalAvg),
    risks,
    recommendationStrength,
    missing,
    evidence
  };
}

async function writeDocx(filePath, title, sections) {
  const doc = new Document({
    sections: [{ children: [new Paragraph({ text: title, heading: HeadingLevel.TITLE, alignment: AlignmentType.CENTER }), ...sections] }]
  });
  fs.writeFileSync(filePath, await Packer.toBuffer(doc));
}

function para(text, opts = {}) {
  return new Paragraph({ text, heading: opts.heading, spacing: { after: 160 } });
}

function bullet(text) {
  return new Paragraph({ text, bullet: { level: 0 }, spacing: { after: 120 } });
}

function keyValueTable(rows) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: rows.map(([k, v]) => new TableRow({
      children: [
        new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: k, bold: true })] })] }),
        new TableCell({ children: [new Paragraph(safe(v))] })
      ]
    }))
  });
}

async function main() {
  const inputPath = process.argv[2];
  const outDir = process.argv[3];
  if (!inputPath || !outDir) {
    console.error("Usage: node scripts/generate_band_offer_packet.js <input.json> <output-dir>");
    process.exit(1);
  }

  const payload = readJson(inputPath);
  ensureDir(outDir);
  const result = buildDecision(payload);
  const candidate = getCandidate(payload);
  const band = getBand(payload);
  const market = getMarket(payload);
  const budget = getBudget(payload);

  const reportPath = path.join(outDir, "compensation-band-offer-review.docx");
  const summaryPath = path.join(outDir, "business-summary-message.docx");
  const trackerPath = path.join(outDir, "band-offer-review.csv");
  const jsonPath = path.join(outDir, "band-offer-review-output.json");

  await writeDocx(reportPath, "薪酬 Band 与定薪建议报告", [
    para("一、岗位与候选人概况", { heading: HeadingLevel.HEADING_1 }),
    keyValueTable([
      ["岗位名称", payload.position.job_title],
      ["职级", payload.position.level],
      ["工作城市", payload.position.city],
      ["候选人", candidate.candidate_name],
      ["当前月薪", candidate.current_monthly_base],
      ["期望月薪", candidate.expected_monthly_base],
      ["建议强度", result.recommendationStrength]
    ]),
    para("二、Band 与市场对标", { heading: HeadingLevel.HEADING_1 }),
    bullet(`Band 区间：${band ? `${band.monthly_base_min} - ${band.monthly_base_max}` : "未提供"}`),
    bullet(`Band 中位值：${band ? band.monthly_base_mid : "未提供"}`),
    bullet(`市场 P25/P50/P75：${market ? `${market.p25} / ${market.p50} / ${market.p75}` : "未提供正式市场调研"}`),
    bullet(`内部同级平均月薪：${result.internalAvg || "未提供"}`),
    bullet(`预算范围：${budget ? `${budget.min} - ${budget.max}` : "未提供"}`),
    bullet(`候选人期望位置：${result.bandPosition}`),
    para("三、定薪建议", { heading: HeadingLevel.HEADING_1 }),
    bullet(`建议强度：${result.recommendationStrength}`),
    bullet(`建议：${result.recommendation}`),
    bullet(`建议月薪：${result.suggestedBase}`),
    bullet(`主要风险：${result.risks.join("；") || "暂无明显风险"}`),
    bullet(`岗位判断依据：${candidate.target_role_reason}`),
    bullet(`市场备注：${market?.notes || market?.source_name || "未提供"}`),
    bullet(`仍缺信息：${result.missing.join("；") || "无"}`)
  ]);

  await writeDocx(summaryPath, "给业务或老板的摘要", [
    para("建议发送对象：招聘负责人 / 业务负责人 / 审批人", { heading: HeadingLevel.HEADING_1 }),
    para(`${candidate.candidate_name} 应聘 ${payload.position.job_title}，候选人期望月薪 ${candidate.expected_monthly_base}，当前位于 ${result.bandPosition}。本次判断强度为“${result.recommendationStrength}”。综合 band、市场分位和内部同级参考，${result.recommendation}，建议月薪控制在 ${result.suggestedBase} 左右。${result.risks.length ? `当前需重点关注：${result.risks.join("；")}。` : "当前未发现明显越带宽或市场失衡风险。"}${result.missing.length ? `当前仍缺：${result.missing.join("；")}。` : ""}`)
  ]);

  const header = ["candidate_name", "target_role", "expected_monthly_base", "band_position", "suggested_base", "recommendation_strength", "risk_flags", "recommendation"];
  const row = [
    candidate.candidate_name,
    payload.position.job_title,
    candidate.expected_monthly_base,
    result.bandPosition,
    result.suggestedBase,
    result.recommendationStrength,
    result.risks.join("；"),
    result.recommendation
  ];
  fs.writeFileSync(trackerPath, `${header.join(",")}\n${row.map(csvEscape).join(",")}\n`, "utf8");

  fs.writeFileSync(jsonPath, JSON.stringify({
    normalized_data: payload,
    missing_information: result.missing,
    risk_summary: result.risks.length ? result.risks.join("；") : "暂无明显高风险",
    priority_issues: result.risks,
    next_action: result.recommendationStrength === "正式建议"
      ? `按 ${result.suggestedBase} 左右准备定薪审批材料，并同步说明 band、市场和内部公平依据。`
      : `先补齐 ${result.missing.join("、")}，再决定是否进入正式定薪审批。`,
    message_draft: `${candidate.candidate_name} 的期望薪资与岗位 band、市场分位及内部参考已完成比对，本次属于“${result.recommendationStrength}”，建议 ${result.recommendation}。`,
    record_update: {
      candidate_name: candidate.candidate_name,
      target_role: payload.position.job_title,
      suggested_base: result.suggestedBase,
      recommendation_strength: result.recommendationStrength
    },
    data_sources_used: result.evidence,
    compliance_warning_if_any: []
  }, null, 2), "utf8");

  console.log(JSON.stringify({
    ok: true,
    files: {
      report: reportPath,
      summary: summaryPath,
      tracker: trackerPath,
      json: jsonPath
    }
  }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
