#!/usr/bin/env node
/**
 * Automatic Skill — Stage 1: Research (调研)
 * 输出一个 Agent 执行 prompt，指导其搜索趋势话题、分析现有 skill 空白，产出 Top-3 创意。
 *
 * 用法:
 *   node scripts/research.js
 *   node scripts/research.js --lang en
 */

const args = process.argv.slice(2);
const lang = args.includes('--lang') ? args[args.indexOf('--lang') + 1] : 'zh';

const now = new Date();
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

if (lang === 'en') {
  console.log(`
=== AUTOMATIC SKILL — Stage 1: Research ===
Date: ${dateISO}

You are the Automatic Skill pipeline. Your task in Stage 1 is to research and identify the best skill idea to build today.

STEP A — Scan existing skills
List all skill folders in the openclaw skills directory (~/.openclaw/workspace/skills or the known skill repository). Record their names and a one-line description of what they do.

STEP B — Search for trending topics (run these searches)
1. Search: "trending app features ${dateISO}"
2. Search: "popular chatbot skills 2026"
3. Search: "most requested AI assistant features"
4. Search: "productivity tools trending ${dateISO}"
5. Search: "daily habit apps 2026"

STEP C — Identify gaps
Compare trending topics with existing skills. List 5 areas that are trending but not yet covered by any existing skill.

STEP D — Generate Top-3 ideas
For each of the top 3 skill ideas, provide:
- Skill name (slug format, e.g. "daily-poem")
- One-line description
- Target audience
- Core features (3-5 bullet points)
- Why it's valuable right now
- Estimated complexity: Low / Medium / High

STEP E — Select the winner
Choose the best idea balancing: user value, originality, feasibility in one day, and fit with the openclaw skill ecosystem.

OUTPUT FORMAT (JSON, to be saved as data/current-pipeline.json stage=research):
{
  "stage": "research",
  "date": "${dateISO}",
  "ideas": [
    { "name": "...", "slug": "...", "description": "...", "features": [], "complexity": "..." },
    { "name": "...", "slug": "...", "description": "...", "features": [], "complexity": "..." },
    { "name": "...", "slug": "...", "description": "...", "features": [], "complexity": "..." }
  ],
  "selected": { "name": "...", "slug": "...", "description": "...", "features": [], "reasoning": "..." },
  "completedAt": "<ISO timestamp>"
}

Save this JSON to: data/current-pipeline.json
Then proceed to Stage 2: node scripts/design.js "<selected slug>"
`);
} else {
  console.log(`
=== AUTOMATIC SKILL — 阶段 1：调研 ===
日期：${dateISO}

你是 Automatic Skill 流水线。第 1 阶段的任务是调研并确定今天要构建的最佳 Skill 创意。

步骤 A — 扫描现有 Skill
列出 openclaw skills 目录（~/.openclaw/workspace/skills 或已知 skill 仓库）中所有 skill 文件夹，记录它们的名称和一句话描述。

步骤 B — 搜索趋势话题（执行以下搜索）
1. 搜索："${dateISO} 热门 App 功能"
2. 搜索："2026 最受欢迎聊天机器人技能"
3. 搜索："AI 助手最常被请求的功能"
4. 搜索："${dateISO} 生产力工具趋势"
5. 搜索："2026 日常习惯打卡类应用趋势"

步骤 C — 识别空白
将趋势话题与现有 skill 对比，列出 5 个有热度但尚无对应 skill 的领域。

步骤 D — 生成 Top-3 创意
对每个候选 skill 创意，给出：
- Skill 名称（slug 格式，如 "daily-poem"）
- 一句话描述
- 目标用户群体
- 核心功能（3-5 条）
- 当下价值亮点
- 预估复杂度：低 / 中 / 高

步骤 E — 选出最优创意
综合评估：用户价值、独创性、单日可交付性、与 openclaw 生态的契合度，选出最终创意。

输出格式（JSON，保存为 data/current-pipeline.json，stage=research）：
{
  "stage": "research",
  "date": "${dateISO}",
  "ideas": [
    { "name": "...", "slug": "...", "description": "...", "features": [], "complexity": "..." },
    { "name": "...", "slug": "...", "description": "...", "features": [], "complexity": "..." },
    { "name": "...", "slug": "...", "description": "...", "features": [], "complexity": "..." }
  ],
  "selected": { "name": "...", "slug": "...", "description": "...", "features": [], "reasoning": "..." },
  "completedAt": "<ISO 时间戳>"
}

将此 JSON 保存到：data/current-pipeline.json
然后进入阶段 2：node scripts/design.js "<selected slug>"
`);
}
