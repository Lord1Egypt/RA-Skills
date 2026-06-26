#!/usr/bin/env node
/**
 * Automatic Skill — Stage 10: Final Review (复查)
 * 输出 Agent 执行 prompt，指导其生成完整的流水线报告并写入 pipeline-log.json。
 *
 * 用法:
 *   node scripts/final-review.js <skill-slug>
 *   node scripts/final-review.js --from-pipeline
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

let slug = '';
if (args.includes('--from-pipeline')) {
  const pipelinePath = path.join(__dirname, '..', 'data', 'current-pipeline.json');
  if (fs.existsSync(pipelinePath)) {
    const p = JSON.parse(fs.readFileSync(pipelinePath, 'utf8'));
    slug = (p.design && p.design.slug)
      || (p.research && p.research.selected && p.research.selected.slug)
      || '';
  }
}
if (!slug) {
  slug = args.filter(a => a !== '--lang' && a !== lang && !a.startsWith('--'))[0] || '';
}
if (!slug) {
  console.error('Usage: node scripts/final-review.js <skill-slug>');
  console.error('       node scripts/final-review.js --from-pipeline');
  process.exit(1);
}

const dataDir = path.join(__dirname, '..', 'data');
const pipelinePath = path.join(dataDir, 'current-pipeline.json');
const logPath = path.join(dataDir, 'pipeline-log.json');

if (lang === 'en') {
  console.log(`
=== AUTOMATIC SKILL — Stage 10: Final Review ===
Skill: ${slug}

This is the final stage. Compile a comprehensive report and archive the pipeline run.

STEP 1 — Read the full pipeline state
Read: ${pipelinePath}
Collect all stage results: research, design, create, review, selfRun, selfCheck, upload, verifyUpload.

STEP 2 — Compile pipeline summary
Calculate:
- Total time from research.completedAt to now
- Number of review iterations (how many times review stage was re-run)
- Number of self-check iterations
- Final review score (from selfCheck.score)
- Upload status summary

STEP 3 — Generate the final report

REPORT FORMAT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AUTOMATIC SKILL PIPELINE — FINAL REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Skill:        ${slug}
Date:         <date>
Total Time:   <duration>

PIPELINE STAGES:
  ✅ Stage 1  Research    — Completed at <time>  (<N> ideas evaluated)
  ✅ Stage 2  Design      — Completed at <time>
  ✅ Stage 3  SEO         — displayName: <name>  keywords: <N>
  ✅ Stage 4  Create      — Completed at <time>  (<N> files created)
  ✅ Stage 5  Review      — Score: <N>/100  (<N> iterations)
  ✅ Stage 6  Self-Run    — <N> scripts tested, <N> passed
  ✅ Stage 7  Self-Check  — Score: <N>/100  (<N> checks passed)
  ✅ Stage 8  Upload      — GitHub: <status>  clawHub: <status>
  ✅ Stage 9  Verify      — GitHub: VERIFIED  clawHub: VERIFIED
  ✅ Stage 10 Final Review — COMPLETE

SKILL SUMMARY:
  Name:        <full name>
  Description: <one-line>
  Scripts:     <N> scripts
  Keywords:    <N> keywords
  GitHub:      <repo>/openclaw/agents/skills/${slug}
  clawHub:     <clawhub url>

ISSUES ENCOUNTERED: <list any warnings or fixes applied>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4 — Archive to pipeline-log.json
Read: ${logPath} (if it doesn't exist, start with [])
Append this entry:
{
  "slug": "${slug}",
  "date": "<ISO date>",
  "duration": "<HH:MM:SS>",
  "reviewScore": <N>,
  "selfCheckScore": <N>,
  "githubStatus": "SUCCESS" | "FAILED" | "SKIPPED",
  "clawhubStatus": "SUCCESS" | "FAILED" | "SKIPPED",
  "verdict": "SUCCESS" | "PARTIAL_SUCCESS" | "FAILED",
  "filesCreated": <N>,
  "scriptsTested": <N>,
  "completedAt": "<ISO timestamp>"
}
Save the updated array back to ${logPath}.

STEP 5 — Clean up current pipeline state
Delete: ${pipelinePath}
(The run is complete; next pipeline starts fresh)

STEP 6 — Print completion message
Print a brief summary to the user (or to openclaw push channel) announcing the new skill.
Example:
  🎉 New skill published: ${slug}
  📖 Description: <description>
  🔗 GitHub: <url>
  🏪 clawHub: <url>

DONE. Pipeline complete. ✅
`);
} else {
  console.log(`
=== AUTOMATIC SKILL — 阶段 10：复查 ===
Skill：${slug}

这是最后阶段。编写完整报告并归档本次流水线运行记录。

步骤 1 — 读取完整的流水线状态
读取：${pipelinePath}
收集所有阶段结果：research, design, create, review, selfRun, selfCheck, upload, verifyUpload。

步骤 2 — 编写流水线摘要
计算：
- 从 research.completedAt 到现在的总耗时
- 审核迭代次数（review 阶段重跑了多少次）
- 自检迭代次数
- 最终审核分数（来自 selfCheck.score）
- 上传状态摘要

步骤 3 — 生成最终报告

报告格式：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AUTOMATIC SKILL 流水线 — 最终报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Skill：      ${slug}
日期：       <日期>
总耗时：     <时长>

流水线阶段：
  ✅ 阶段 1 调研   — 完成于 <时间>（评估了 <N> 个创意）
  ✅ 阶段 2 设计   — 完成于 <时间>
  ✅ 阶段 3 制作   — 完成于 <时间>（创建了 <N> 个文件）
  ✅ 阶段 4 审核   — 得分：<N>/100（<N> 次迭代）
  ✅ 阶段 5 自跑   — <N> 个脚本测试，<N> 个通过
  ✅ 阶段 6 自检   — 得分：<N>/100（通过 <N> 项检查）
  ✅ 阶段 7 上传   — GitHub：<状态>  clawHub：<状态>
  ✅ 阶段 8 验收   — GitHub：VERIFIED  clawHub：VERIFIED
  ✅ 阶段 9 复查   — 完成

Skill 摘要：
  名称：     <全名>
  描述：     <一句话>
  脚本数：   <N> 个
  关键词：   <N> 个
  GitHub：   <repo>/openclaw/agents/skills/${slug}
  clawHub：  <clawhub url>

遇到的问题：<列出所有警告或已修复内容>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

步骤 4 — 归档到 pipeline-log.json
读取：${logPath}（如不存在，从 [] 开始）
追加以下条目：
{
  "slug": "${slug}",
  "date": "<ISO 日期>",
  "duration": "<HH:MM:SS>",
  "reviewScore": <N>,
  "selfCheckScore": <N>,
  "githubStatus": "SUCCESS" | "FAILED" | "SKIPPED",
  "clawhubStatus": "SUCCESS" | "FAILED" | "SKIPPED",
  "verdict": "SUCCESS" | "PARTIAL_SUCCESS" | "FAILED",
  "filesCreated": <N>,
  "scriptsTested": <N>,
  "completedAt": "<ISO 时间戳>"
}
将更新后的数组保存回 ${logPath}。

步骤 5 — 清理当前流水线状态
删除：${pipelinePath}
（本次运行完成；下次流水线从头开始）

步骤 6 — 打印完成信息
向用户（或 openclaw 推送渠道）打印简短摘要，宣布新 skill 发布。
示例：
  🎉 新 skill 已发布：${slug}
  📖 描述：<描述>
  🔗 GitHub：<url>
  🏪 clawHub：<url>

完成。流水线结束。✅
`);
}
