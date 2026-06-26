#!/usr/bin/env node
/**
 * Automatic Skill — Stage 3: SEO 优化
 * 在设计完成后、制作前，对 skill 的名称、描述、关键词进行 SEO 优化，
 * 提升可搜索性、传播力和用户点击率。
 *
 * 用法:
 *   node scripts/seo.js --from-pipeline     # 从 data/current-pipeline.json 读取设计结果
 *   node scripts/seo.js "daily-poem"        # 直接传 slug
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

let slug = '';
let designInfo = {};

if (args.includes('--from-pipeline')) {
  const pipelinePath = path.join(__dirname, '..', 'data', 'current-pipeline.json');
  if (!fs.existsSync(pipelinePath)) {
    console.error('ERROR: data/current-pipeline.json not found. Run design.js first.');
    process.exit(1);
  }
  const pipeline = JSON.parse(fs.readFileSync(pipelinePath, 'utf8'));
  const design = pipeline.design;
  const selected = pipeline.selected || (pipeline.research && pipeline.research.selected);
  if (!design && !selected) {
    console.error('ERROR: No design or research data in current-pipeline.json. Complete Stage 2 first.');
    process.exit(1);
  }
  slug = (design && design.slug) || (selected && selected.slug) || '';
  designInfo = design || { slug, idea: selected && selected.description };
} else {
  slug = args.filter(a => !a.startsWith('--') && a !== lang)[0] || '';
  if (!slug) {
    console.error('Usage: node scripts/seo.js --from-pipeline');
    console.error('       node scripts/seo.js <slug>');
    process.exit(1);
  }
}

const now = new Date();
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

const designSummary = JSON.stringify(designInfo, null, 2).slice(0, 1200);

if (lang === 'en') {
  console.log(`
=== AUTOMATIC SKILL — Stage 3: SEO Optimization ===
Skill: ${slug}
Date: ${dateISO}

Design summary:
${designSummary}

You are an SEO and product copywriting specialist. Optimize the skill's discoverability and appeal.

TASK — Produce optimized versions of all the following:

1. DISPLAY NAME (max 30 chars)
   - Must be immediately clear about what the skill DOES
   - Natural language, not technical jargon
   - Example: "Daily Poem ✦ Morning Inspiration" → "Daily Poem"

2. TAGLINE (max 60 chars)
   - One punchy sentence that sells the benefit
   - Example: "A fresh poem delivered every morning, tailored to your mood"
   - No buzzwords like "powerful", "innovative", "seamless"

3. SHORT DESCRIPTION (max 120 chars)
   - For search result snippets and social previews
   - Lead with the #1 user benefit, include 2 primary keywords naturally
   - Must answer: What does it do? Who is it for?

4. FULL DESCRIPTION (200-300 chars)
   - For SKILL.md frontmatter
   - Include use cases, target users, key features
   - Natural keyword density — do not keyword-stuff

5. KEYWORDS (30+ terms)
   Rules:
   - Include the slug itself and natural variations
   - Mix Chinese + English (e.g. "每日诗词", "daily poem", "morning reading")
   - Cover: core function, target users, use scenarios, emotion/benefit words
   - Include long-tail phrases (e.g. "每天早上自动推送诗词")
   - NO commas within a single keyword phrase
   Format: plain list, one per line

6. GITHUB REPO DESCRIPTION (max 150 chars)
   - Technically precise, includes primary keywords
   - Suitable for developers scanning GitHub search results

7. CLAWHUB LISTING TITLE (max 40 chars)
   - Same as display name, or slightly shorter
   - Must contain the primary function keyword

8. SEARCH INTENT COVERAGE
   List 5 search queries a target user might type that this skill should rank for.

OUTPUT FORMAT (JSON, append to data/current-pipeline.json under key "seo"):
{
  "stage": "seo",
  "slug": "${slug}",
  "displayName": "...",
  "tagline": "...",
  "shortDescription": "...",
  "fullDescription": "...",
  "keywords": ["...", "...", "..."],
  "githubDescription": "...",
  "clawhubTitle": "...",
  "searchIntents": ["...", "...", "..."],
  "completedAt": "<ISO timestamp>"
}

Read data/current-pipeline.json, add the "seo" key, save back.
Then proceed to Stage 4: node scripts/create.js --from-pipeline
`);
} else {
  console.log(`
=== AUTOMATIC SKILL — 阶段 3：SEO 优化 ===
Skill：${slug}
日期：${dateISO}

设计摘要：
${designSummary}

你是一名 SEO 与产品文案专家。请对这个 skill 的可发现性和吸引力进行全面优化。

任务 — 产出以下所有内容的优化版本：

1. 展示名称（最多 30 字）
   - 让人一眼明白 skill 能做什么
   - 自然语言，不要技术术语
   - 中文名优先，必要时中英混搭（如「每日诗词」「Career News 职场早报」）

2. 一句话卖点（最多 60 字）
   - 一句能打动用户的话，突出核心价值
   - 禁止：强大、智能、无缝、赋能等空洞词汇
   - 示例：「每天早晨推送一首诗，配合你的心情」

3. 搜索摘要描述（最多 120 字）
   - 用于搜索结果片段和社交预览
   - 开头直接说第一大用户收益，自然嵌入 2 个核心关键词
   - 必须回答：能做什么？适合谁？

4. 完整描述（200-300 字）
   - 用于 SKILL.md frontmatter
   - 涵盖使用场景、目标用户、核心功能
   - 关键词自然分布，不堆砌

5. 关键词列表（30 个以上）
   规则：
   - 包含 slug 本身及变体
   - 中英混合（如「每日诗词」「daily poem」「早间推送」）
   - 覆盖：核心功能、目标用户、使用场景、情绪/收益词
   - 包含长尾词组（如「每天早上自动推送诗词」）
   - 单个关键词/词组内不含逗号
   格式：纯列表，每行一个

6. GitHub 仓库描述（最多 150 字）
   - 技术精准，包含主要关键词
   - 适合在 GitHub 搜索结果中被开发者扫到

7. clawHub 上架标题（最多 40 字）
   - 与展示名称相同或更简洁
   - 必须包含主要功能关键词

8. 搜索意图覆盖
   列出目标用户可能输入的 5 条搜索词，这个 skill 应当能匹配到。

输出格式（JSON，追加到 data/current-pipeline.json 的 "seo" 键下）：
{
  "stage": "seo",
  "slug": "${slug}",
  "displayName": "...",
  "tagline": "...",
  "shortDescription": "...",
  "fullDescription": "...",
  "keywords": ["...", "...", "..."],
  "githubDescription": "...",
  "clawhubTitle": "...",
  "searchIntents": ["...", "...", "..."],
  "completedAt": "<ISO 时间戳>"
}

读取 data/current-pipeline.json，添加 "seo" 键后保存回去。
然后进入阶段 4：node scripts/create.js --from-pipeline
`);
}
