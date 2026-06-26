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

function joinList(list) {
  return Array.isArray(list) ? list.join("；") : "";
}

function containsAny(text, keywords) {
  const source = safe(text).toLowerCase();
  return keywords.some((keyword) => source.includes(String(keyword).toLowerCase()));
}

const SKILL_KEYWORD_MAP = {
  "增长策略": ["增长", "增长策略", "拉新", "留存", "转化", "会员增长"],
  "数据分析": ["数据分析", "数据", "分析", "指标", "漏斗", "复盘"],
  "A/B实验": ["a/b", "ab实验", "实验", "测试", "迭代"],
  "跨团队协作": ["跨团队", "跨部门", "协作", "协同", "推动"],
  "电商或本地生活经验": ["电商", "本地生活"],
  "会员体系经验": ["会员", "会员体系", "付费转化"],
  "带项目 owner 经验": ["owner", "主导", "负责人", "独立负责"]
};

function allCandidateText(payload) {
  const candidate = payload.candidate;
  return [
    candidate.current_title,
    candidate.current_company,
    joinList(candidate.industry_experience),
    joinList(candidate.core_skills),
    joinList(candidate.project_highlights),
    candidate.resume_summary
  ].join(" ");
}

function computeMatches(payload) {
  const text = allCandidateText(payload);
  const mustHave = payload.job.must_have_skills.map((skill) => ({
    skill,
    matched: containsAny(text, SKILL_KEYWORD_MAP[skill] || [skill, skill.replace("/", ""), skill.replace("A/B", "ab")])
  }));
  const preferred = payload.job.preferred_skills.map((skill) => ({
    skill,
    matched: containsAny(text, SKILL_KEYWORD_MAP[skill] || [skill])
  }));
  return { mustHave, preferred };
}

function computeScore(matchData) {
  const mustMatched = matchData.mustHave.filter((x) => x.matched).length;
  const preferredMatched = matchData.preferred.filter((x) => x.matched).length;
  const mustBase = (mustMatched / Math.max(1, matchData.mustHave.length)) * 75;
  const preferredBase = (preferredMatched / Math.max(1, matchData.preferred.length)) * 25;
  return Math.round(mustBase + preferredBase);
}

function buildRiskFlags(payload, matchData) {
  const risks = [];
  const text = allCandidateText(payload);
  if (matchData.preferred.filter((x) => x.matched).length === 0) risks.push("加分项命中较少，需要确认行业迁移速度");
  if (!containsAny(text, ["owner", "负责人", "主导"])) risks.push("简历里 owner 角色描述偏少，建议补看独立推动能力");
  if (!containsAny(text, ["电商", "本地生活"])) risks.push("缺少目标行业直接经验，需要评估学习成本");
  return risks;
}

function buildInterviewFocus(payload, risks) {
  const focus = [
    "请候选人展开讲一个自己主导的增长项目，重点看目标拆解、实验设计和结果复盘。",
    "补看跨团队推动时的冲突处理和 owner 意识。",
    "确认对目标行业的理解和迁移路径。"
  ];
  if (safe(payload.candidate.salary_expectation).includes("40k")) {
    focus.push("提前确认级别与薪资预期，避免进入后期博弈。");
  }
  return risks.length ? focus : focus.slice(0, 2);
}

function buildDecision(score) {
  if (score >= 78) return { decision: "建议推进首轮面试", nextAction: "联系候选人安排首轮面试，并提醒用人经理重点补看 owner 意识与行业迁移能力。" };
  if (score >= 60) return { decision: "建议保留并补充信息", nextAction: "先补充关键信息或电话初筛，再决定是否进入正式面试。" };
  return { decision: "暂不推进", nextAction: "记录原因并发送礼貌拒信。" };
}

function buildCandidateMessage(payload, decision) {
  const name = safe(payload.candidate.candidate_name, "候选人");
  const role = safe(payload.job.job_title);
  if (decision.decision === "暂不推进") {
    return `${name}，你好，感谢你投递我们${role}岗位，并花时间和我们沟通。结合当前岗位需求和简历评估结果，这次我们暂时不会继续推进流程。你的经历里仍有不错的亮点，我们会保留资料，后续如果有更适合的岗位会再联系你。祝你接下来的机会顺利。`;
  }
  if (decision.decision === "建议保留并补充信息") {
    return `${name}，你好，我们已经完成了你投递岗位的初步评估，整体背景有一些不错的匹配点。为了更准确判断岗位匹配度，想再和你补充了解几个问题，包括近期主导项目、行业经验和岗位期望。若方便的话，我们可以安排一个简短电话沟通。`;
  }
  return `${name}，你好，我们已经看过你的简历，整体和${role}岗位有较高匹配度，特别是增长项目和跨团队协作相关经历。我们希望继续推进下一步面试，稍后会和你确认可沟通时间，也欢迎你提前整理下近期主导的增长项目和结果复盘。`;
}

function buildRecordSummary(payload, score, decision, risks) {
  return `${safe(payload.candidate.candidate_name)} 应聘 ${safe(payload.job.job_title)}，简历初筛匹配度 ${score}/100；结论：${decision.decision}；主要风险：${risks.join("；") || "暂无明显风险"}；下一步：${decision.nextAction}`;
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

function csvEscape(value) {
  const str = safe(value);
  if (str.includes(",") || str.includes("\"") || str.includes("\n")) return `"${str.replace(/"/g, "\"\"")}"`;
  return str;
}

async function main() {
  const inputPath = process.argv[2];
  const outDir = process.argv[3];
  if (!inputPath || !outDir) {
    console.error("Usage: node scripts/generate_screening_packet.js <input.json> <output-dir>");
    process.exit(1);
  }

  const payload = readJson(inputPath);
  ensureDir(outDir);

  const matchData = computeMatches(payload);
  const score = computeScore(matchData);
  const risks = buildRiskFlags(payload, matchData);
  const interviewFocus = buildInterviewFocus(payload, risks);
  const decision = buildDecision(score);
  const candidateMessage = buildCandidateMessage(payload, decision);
  const recordSummary = buildRecordSummary(payload, score, decision, risks);

  const memoPath = path.join(outDir, "resume-screening-note.docx");
  const messagePath = path.join(outDir, "candidate-screening-message.docx");
  const trackerPath = path.join(outDir, "resume-screening-update.csv");
  const jsonPath = path.join(outDir, "resume-screening-output.json");

  await writeDocx(memoPath, "候选人初筛评估", [
    para("一、岗位与候选人概况", { heading: HeadingLevel.HEADING_1 }),
    keyValueTable([
      ["候选人姓名", payload.candidate.candidate_name],
      ["应聘岗位", payload.job.job_title],
      ["当前职位", payload.candidate.current_title],
      ["当前公司", payload.candidate.current_company],
      ["工作城市", payload.candidate.city],
      ["工作年限", payload.candidate.years_of_experience],
      ["期望薪资", payload.candidate.salary_expectation],
      ["到岗周期", payload.candidate.availability]
    ]),
    para("二、岗位关键要求命中情况", { heading: HeadingLevel.HEADING_1 }),
    bullet(`必备项命中：${matchData.mustHave.map((x) => `${x.skill}${x.matched ? "（命中）" : "（未明确体现）"}`).join("；")}`),
    bullet(`加分项命中：${matchData.preferred.map((x) => `${x.skill}${x.matched ? "（命中）" : "（未明确体现）"}`).join("；")}`),
    bullet(`简历摘要：${payload.candidate.resume_summary}`),
    para("三、初筛结论", { heading: HeadingLevel.HEADING_1 }),
    bullet(`综合匹配度：${score}/100`),
    bullet(`推荐结论：${decision.decision}`),
    bullet(`主要风险：${risks.join("；") || "暂无明显风险"}`),
    bullet(`建议面试重点：${interviewFocus.join("；")}`),
    bullet(`下一步：${decision.nextAction}`)
  ]);

  await writeDocx(messagePath, "候选人初筛沟通稿", [
    para("建议发送对象：候选人", { heading: HeadingLevel.HEADING_1 }),
    para(candidateMessage)
  ]);

  const trackerHeader = ["candidate_name", "target_role", "stage", "decision", "risk_flags", "owner", "next_action", "last_update_summary"];
  const trackerRow = [
    payload.candidate.candidate_name,
    payload.job.job_title,
    payload.hr_owner.tracker_stage,
    decision.decision,
    risks.join("；"),
    payload.hr_owner.owner_name,
    decision.nextAction,
    recordSummary
  ];

  fs.writeFileSync(trackerPath, `${trackerHeader.join(",")}\n${trackerRow.map(csvEscape).join(",")}\n`, "utf8");
  fs.writeFileSync(jsonPath, JSON.stringify({
    normalized_data: {
      candidate: payload.candidate,
      job: payload.job,
      must_have_match: matchData.mustHave,
      preferred_match: matchData.preferred,
      match_score: score
    },
    decision_summary: recordSummary,
    missing_information: [],
    next_action: decision.nextAction,
    message_draft: candidateMessage,
    record_update: {
      stage: payload.hr_owner.tracker_stage,
      decision: decision.decision,
      risk_flags: risks
    },
    compliance_warning_if_any: []
  }, null, 2), "utf8");

  console.log(JSON.stringify({
    ok: true,
    files: {
      note: memoPath,
      message: messagePath,
      tracker: trackerPath,
      json: jsonPath
    }
  }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
