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
  return Array.isArray(list) ? list.join("、") : "";
}

function scoreFromRecommendations(interviews) {
  let score = 70;
  for (const item of interviews) {
    const text = safe(item.hire_recommendation);
    if (text.includes("推进")) score += 6;
    if (text.includes("有条件")) score -= 2;
    if (text.includes("保守")) score -= 3;
    if (text.includes("拒绝")) score -= 18;
  }
  return Math.max(0, Math.min(100, score));
}

function detectConcerns(interviews) {
  const joined = interviews.map((x) => safe(x.feedback)).join(" ");
  const concerns = [];
  if (/owner|负责人意识|长期策略|系统性/.test(joined)) concerns.push("owner意识或系统性策略深度需补充验证");
  if (/薪资|定级|偏高/.test(joined)) concerns.push("薪资或定级存在博弈空间");
  if (/执行/.test(joined)) concerns.push("偏执行型，需继续判断独立规划能力");
  return concerns;
}

function detectStrengths(interviews) {
  const joined = interviews.map((x) => safe(x.feedback)).join(" ");
  const strengths = [];
  if (/数据/.test(joined)) strengths.push("数据分析和增长指标敏感度较好");
  if (/跨团队|推动/.test(joined)) strengths.push("跨团队协作与推动经验较强");
  if (/行业经验|本地生活|电商|会员/.test(joined)) strengths.push("行业和增长场景匹配度较高");
  if (/沟通顺畅|表达/.test(joined)) strengths.push("沟通表达稳定");
  return strengths;
}

function decide(interviews) {
  const joined = interviews.map((x) => safe(x.hire_recommendation) + " " + safe(x.feedback)).join(" ");
  if (/拒绝/.test(joined)) {
    return {
      decision: "暂不推进",
      nextAction: "向候选人发送礼貌拒信，并在 tracker 记录拒绝原因。",
      messageTone: "reject"
    };
  }
  if (/补看|系统性思考|有条件推进/.test(joined)) {
    return {
      decision: "建议推进补充面/终面",
      nextAction: "安排一轮聚焦 owner 意识、长期策略和级别校准的补充面试。",
      messageTone: "advance"
    };
  }
  return {
    decision: "建议推进下一轮",
    nextAction: "进入下一轮面试或内部审批讨论。",
    messageTone: "advance"
  };
}

function buildCandidateMessage(payload, decision) {
  const name = safe(payload.candidate.candidate_name, "候选人");
  const role = safe(payload.candidate.target_role);
  if (decision.messageTone === "reject") {
    return `${name}，你好，感谢你参与我们${role}岗位的面试流程，也感谢你花时间和团队做了深入交流。综合当前岗位需求和面试评估结果，我们这次暂时不会继续推进本岗位流程。你的背景里仍有一些不错的亮点，我们会为你保留简历，后续如果有更匹配的机会会第一时间联系你。祝你接下来的机会顺利。`;
  }
  return `${name}，你好，感谢你参加我们${role}岗位的面试。团队已经完成当前轮次的沟通，整体反馈积极，我们希望继续推进下一步。接下来我们会尽快帮你安排后续面试/沟通，并同步具体时间。也欢迎你提前整理下对岗位、团队和业务的关注点，我们下一轮可以一起详细聊。`;
}

function buildInternalSummary(payload, strengths, concerns, decision, score) {
  const candidate = payload.candidate;
  return [
    `${safe(candidate.candidate_name)} 应聘 ${safe(candidate.target_role)}，综合匹配度 ${score}/100。`,
    strengths.length ? `主要亮点：${strengths.join("；")}。` : "",
    concerns.length ? `主要风险：${concerns.join("；")}。` : "",
    `建议结论：${decision.decision}`,
    `下一步：${decision.nextAction}`
  ].filter(Boolean).join("\n");
}

function buildNormalizedRows(payload) {
  return payload.interviews.map((item) => ({
    interviewer_name: safe(item.interviewer_name),
    interview_round: safe(item.interview_round),
    source: safe(item.source),
    hire_recommendation: safe(item.hire_recommendation),
    confidence_level: safe(item.confidence_level),
    feedback: safe(item.feedback)
  }));
}

function csvEscape(value) {
  const str = safe(value);
  if (str.includes(",") || str.includes("\"") || str.includes("\n")) {
    return `"${str.replace(/"/g, "\"\"")}"`;
  }
  return str;
}

async function writeDocx(filePath, title, sections) {
  const doc = new Document({
    sections: [
      {
        children: [
          new Paragraph({
            text: title,
            heading: HeadingLevel.TITLE,
            alignment: AlignmentType.CENTER
          }),
          ...sections
        ]
      }
    ]
  });
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(filePath, buffer);
}

function para(text, opts = {}) {
  return new Paragraph({
    text,
    heading: opts.heading,
    spacing: { after: 160 }
  });
}

function bullet(text) {
  return new Paragraph({
    text,
    bullet: { level: 0 },
    spacing: { after: 120 }
  });
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
    console.error("Usage: node scripts/generate_interview_packet.js <input.json> <output-dir>");
    process.exit(1);
  }

  const payload = readJson(inputPath);
  ensureDir(outDir);

  const strengths = detectStrengths(payload.interviews);
  const concerns = detectConcerns(payload.interviews);
  const decision = decide(payload.interviews);
  const score = scoreFromRecommendations(payload.interviews);
  const candidateMessage = buildCandidateMessage(payload, decision);
  const internalSummary = buildInternalSummary(payload, strengths, concerns, decision, score);
  const normalizedRows = buildNormalizedRows(payload);

  const memoPath = path.join(outDir, "interview-debrief-memo.docx");
  const messagePath = path.join(outDir, "candidate-follow-up-message.docx");
  const trackerPath = path.join(outDir, "candidate-tracker-update.csv");
  const jsonPath = path.join(outDir, "workflow-output.json");

  await writeDocx(memoPath, "候选人面试评估纪要", [
    para("一、候选人基本信息", { heading: HeadingLevel.HEADING_1 }),
    keyValueTable([
      ["候选人姓名", payload.candidate.candidate_name],
      ["应聘岗位", payload.candidate.target_role],
      ["所在城市", payload.candidate.city],
      ["当前公司", payload.candidate.current_company],
      ["工作年限", payload.candidate.years_of_experience],
      ["期望薪资", payload.candidate.salary_expectation],
      ["到岗周期", payload.candidate.notice_period]
    ]),
    para("二、岗位关键要求", { heading: HeadingLevel.HEADING_1 }),
    bullet(`必备能力：${joinList(payload.job.must_have_skills)}`),
    bullet(`加分项：${joinList(payload.job.preferred_skills)}`),
    bullet(`招聘偏好：${safe(payload.job.hiring_preference)}`),
    para("三、面试反馈汇总", { heading: HeadingLevel.HEADING_1 }),
    ...normalizedRows.flatMap((row) => ([
      para(`${row.interview_round} - ${row.interviewer_name}`, { heading: HeadingLevel.HEADING_2 }),
      bullet(`来源：${row.source}`),
      bullet(`建议：${row.hire_recommendation}`),
      bullet(`置信度：${row.confidence_level}`),
      bullet(`原始反馈：${row.feedback}`)
    ])),
    para("四、综合评估", { heading: HeadingLevel.HEADING_1 }),
    bullet(`综合匹配度：${score}/100`),
    bullet(`主要亮点：${strengths.join("；") || "待补充"}`),
    bullet(`主要风险：${concerns.join("；") || "暂无明显风险"}`),
    bullet(`建议结论：${decision.decision}`),
    bullet(`下一步建议：${decision.nextAction}`),
    para("五、给用人经理的一段话", { heading: HeadingLevel.HEADING_1 }),
    para(internalSummary)
  ]);

  await writeDocx(messagePath, "候选人沟通稿", [
    para("建议发送对象：候选人", { heading: HeadingLevel.HEADING_1 }),
    para(candidateMessage)
  ]);

  const trackerHeader = [
    "candidate_name",
    "target_role",
    "stage",
    "decision",
    "risk_flags",
    "owner",
    "next_action",
    "last_update_summary"
  ];
  const trackerRow = [
    payload.candidate.candidate_name,
    payload.candidate.target_role,
    safe(payload.hr_owner.tracker_stage),
    decision.decision,
    concerns.join("；"),
    safe(payload.hr_owner.owner_name),
    decision.nextAction,
    internalSummary.replace(/\n/g, " ")
  ];
  fs.writeFileSync(
    trackerPath,
    `${trackerHeader.join(",")}\n${trackerRow.map(csvEscape).join(",")}\n`,
    "utf8"
  );

  fs.writeFileSync(
    jsonPath,
    JSON.stringify({
      normalized_data: {
        candidate: payload.candidate,
        job: payload.job,
        interviews: normalizedRows,
        match_score: score
      },
      decision_summary: internalSummary,
      missing_information: [],
      next_action: decision.nextAction,
      message_draft: candidateMessage,
      record_update: {
        stage: safe(payload.hr_owner.tracker_stage),
        decision: decision.decision,
        risk_flags: concerns
      },
      compliance_warning_if_any: []
    }, null, 2),
    "utf8"
  );

  console.log(JSON.stringify({
    ok: true,
    files: {
      memo: memoPath,
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
