#!/usr/bin/env node
/**
 * Automatic Skill — Pipeline Orchestrator (编排器)
 * 输出 Agent 执行 prompt，引导其完整运行全部 10 个阶段的流水线。
 * Stage 7.5 (Safety Check) runs BEFORE upload as a credential-safety gate.
 *
 * 用法:
 *   node scripts/pipeline.js                     # 自动选题，全流水线
 *   node scripts/pipeline.js --idea "每日诗词"    # 指定主题
 *   node scripts/pipeline.js --dry-run           # 运行到 self-check，不上传
 *   node scripts/pipeline.js --from-stage 4      # 从指定阶段继续（读取现有 pipeline 状态）
 *   node scripts/pipeline.js --lang en
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';
const dryRun = args.includes('--dry-run');

const ideaIdx = args.indexOf('--idea');
const idea = ideaIdx !== -1 ? args[ideaIdx + 1] : null;

const fromStageIdx = args.indexOf('--from-stage');
const fromStage = fromStageIdx !== -1 ? parseInt(args[fromStageIdx + 1], 10) : 1;

const scriptDir = path.join(__dirname);
const dataDir = path.join(__dirname, '..', 'data');
const pipelinePath = path.join(dataDir, 'current-pipeline.json');

const now = new Date();
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

// Check if there's an in-progress pipeline
let existingPipeline = null;
if (fs.existsSync(pipelinePath)) {
  try {
    existingPipeline = JSON.parse(fs.readFileSync(pipelinePath, 'utf8'));
  } catch (e) {
    // ignore parse error
  }
}

if (existingPipeline && fromStage === 1) {
  console.warn(`⚠️  WARNING: A pipeline is already in progress for "${existingPipeline.design && existingPipeline.design.slug || 'unknown'}".`);
  console.warn(`   Use --from-stage <N> to resume, or delete data/current-pipeline.json to start fresh.`);
  console.warn('');
}

const stages = [
  { n: 1,  name: 'Research',     cmd: `node ${scriptDir}/research.js` },
  { n: 2,  name: 'Design',       cmd: `node ${scriptDir}/design.js --from-pipeline` },
  { n: 3,  name: 'SEO',          cmd: `node ${scriptDir}/seo.js --from-pipeline` },
  { n: 4,  name: 'Create',       cmd: `node ${scriptDir}/create.js --from-pipeline` },
  { n: 5,  name: 'Review',       cmd: `node ${scriptDir}/review.js --from-pipeline` },
  { n: 6,  name: 'Self-Run',     cmd: `node ${scriptDir}/self-run.js --from-pipeline` },
  { n: 7,   name: 'Self-Check',    cmd: `node ${scriptDir}/self-check.js --from-pipeline` },
  { n: 7.5, name: 'Safety Check',  cmd: `node ${scriptDir}/scan-check.js --from-pipeline` },
  { n: 8,   name: 'Upload',        cmd: `node ${scriptDir}/upload.js${dryRun ? ' --dry-run' : ''} --from-pipeline` },
  { n: 9,   name: 'Verify',        cmd: `node ${scriptDir}/verify-upload.js --from-pipeline` },
  { n: 10,  name: 'Final Review',  cmd: `node ${scriptDir}/final-review.js --from-pipeline` },
];

const activeStages = dryRun ? stages.slice(0, 7) : stages;
const pendingStages = activeStages.filter(s => s.n >= fromStage);

if (lang === 'en') {
  console.log(`
=== AUTOMATIC SKILL — Full Pipeline Orchestrator ===
Date: ${dateISO}
Mode: ${dryRun ? 'DRY-RUN (stages 1-7 only)' : 'FULL (all 10 stages)'}
${idea ? `Idea: ${idea}` : 'Idea: auto-select from research'}
${fromStage > 1 ? `Resuming from stage: ${fromStage}` : 'Starting from: stage 1'}

You are running the complete Automatic Skill pipeline. Execute each stage IN ORDER.
Do not skip stages. If a stage fails, fix the issue and re-run that stage before proceeding.

LANGUAGE POLICY (follow throughout the entire pipeline):
- SKILL.md content (name, description, sections, commands): write in ENGLISH
- Conversational replies to the user: use the user's language (Chinese if user writes in Chinese)
- All JSON logs, reports, and pipeline state (pipeline-log.json, review scores, etc.): ENGLISH only

EXECUTION PLAN:
${pendingStages.map(s => `  Stage ${s.n}: ${s.name}`).join('\n')}
${dryRun ? '\n⚠️  DRY-RUN: Stages 8-10 (Upload, Verify, Final Review) will be skipped.' : ''}

BEFORE STARTING:
1. Ensure environment variables are set:
   - GITHUB_TOKEN (required for upload)
   - GITHUB_REPO (required for upload, format: owner/repo)
   - CLAWHUB_TOKEN (required for upload)
2. Ensure Node.js >= 18 is installed

EXECUTION INSTRUCTIONS:
For each stage below, run the command to get the stage prompt, then execute that prompt fully before moving to the next stage.

${pendingStages.map(s => `STAGE ${s.n} — ${s.name}
  Run: ${s.n === 2 && idea ? `node ${scriptDir}/design.js "${idea}"` : s.cmd}
  Wait for stage to complete (check data/current-pipeline.json has "${s.name.toLowerCase().replace(/ /g, '-')}" key)
  Then continue to stage ${s.n + 1}.
`).join('\n')}

PROGRESS TRACKING:
After each stage completes, data/current-pipeline.json will contain a new key for that stage.
Check progress at any time: node scripts/status.js

If a stage produces a FAIL verdict, fix the issues described in the stage output and re-run that stage before proceeding.

SAFETY CHECK (Stage 7.5):
Stage 7.5 runs a pre-upload credential-safety check on all generated skill files.
If any credential-exposure issues are found (e.g. hardcoded tokens, echo $TOKEN patterns),
the pipeline BLOCKS and reports the issues. You must fix them manually before proceeding
to Stage 8 (Upload). This is a quality gate, not an auto-fix loop.

After all stages complete, the new skill will be:
- Available locally in SKILL_OUTPUT_DIR
- Committed and pushed to GitHub (unless --dry-run)
- Published on clawHub (unless --dry-run)
- Logged in data/pipeline-log.json

BEGIN with Stage ${fromStage}: run the command listed above for Stage ${fromStage}.
`);
} else {
  console.log(`
=== AUTOMATIC SKILL — 全流水线编排器 ===
日期：${dateISO}
模式：${dryRun ? 'DRY-RUN（仅阶段 1-7）' : '完整（全部 10 个阶段）'}
${idea ? `主题：${idea}` : '主题：由调研阶段自动选定'}
${fromStage > 1 ? `从阶段 ${fromStage} 继续` : '从阶段 1 开始'}

你正在运行完整的 Automatic Skill 流水线。按顺序执行每个阶段。
不要跳过阶段。如果某阶段失败，修复问题并重新运行该阶段，再继续下一阶段。

语言规则（整个流水线全程遵守）：
- SKILL.md 内容（名称、描述、章节、命令）：统一写英文
- 与用户的对话回复：使用用户的语言（用户说中文则全程回中文）
- 所有 JSON 日志、报告、流水线状态（pipeline-log.json、审核评分等）：统一英文

执行计划：
${pendingStages.map(s => `  阶段 ${s.n}：${s.name}`).join('\n')}
${dryRun ? '\n⚠️  DRY-RUN：阶段 8-10（上传、验收、复查）将跳过。' : ''}

开始前：
1. 确保已设置环境变量：
   - GITHUB_TOKEN（上传必需）
   - GITHUB_REPO（上传必需，格式：owner/repo）
   - CLAWHUB_TOKEN（上传必需）
2. 确保已安装 Node.js >= 18

执行说明：
对以下每个阶段，运行命令获取阶段 prompt，然后完整执行该 prompt，再进入下一阶段。

${pendingStages.map(s => `阶段 ${s.n} — ${s.name}
  运行：${s.n === 2 && idea ? `node ${scriptDir}/design.js "${idea}"` : s.cmd}
  等待阶段完成（检查 data/current-pipeline.json 已包含对应键）
  然后继续阶段 ${s.n + 1}。
`).join('\n')}

进度追踪：
每个阶段完成后，data/current-pipeline.json 中将新增该阶段对应的键。
随时查看进度：node scripts/status.js

如果某阶段返回 FAIL，修复阶段输出中描述的问题，重新运行该阶段后再继续。

安全检查（阶段 7.5）：
阶段 7.5 在上传前对所有生成的 skill 文件做凭证安全检查。
如果发现凭证暴露问题（如硬编码 token、echo $TOKEN 模式），
流水线将阻断并报告问题。你必须手动修复后才能进入阶段 8（上传）。
这是一个质检关卡，不是自动修复循环。

最终输出：
所有阶段完成后，新 skill 将：
- 存储在本地 SKILL_OUTPUT_DIR
- 已提交并推送到 GitHub（除非 --dry-run）
- 已发布到 clawHub（除非 --dry-run）
- 已记录在 data/pipeline-log.json

从阶段 ${fromStage} 开始：运行上方阶段 ${fromStage} 对应的命令。
`);
}
