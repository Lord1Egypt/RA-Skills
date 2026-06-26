#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

// 上下文组装脚本
// 用于在写章节前，根据当前的记忆库自动拼凑符合要求的 2000-4000 token 内的指令

const args = process.argv.slice(2);
if (args.length < 3) {
  console.log(`
Dream Novel Skill - 章节前处理工具
用法: node prompt-assembler.js <project_dir> <chapter_number> <chapter_outline_file>

功能说明：
读取 characters.json, foreshadowing.json 等库和过去的摘要，基于给定的大纲生成出供 AI 直接进行下一章书写的完整 Prompt。
  `);
  process.exit(1);
}

const projectDir = path.resolve(args[0]);
const chapNum = parseInt(args[1], 10);
const outlineFile = path.resolve(args[2]);

if (!fs.existsSync(outlineFile)) {
  console.error("Outline file not found: " + outlineFile);
  process.exit(1);
}
const outline = fs.readFileSync(outlineFile, 'utf-8');

const loadDb = (name) => {
  const p = path.join(projectDir, name + '.json');
  return fs.existsSync(p) ? JSON.parse(fs.readFileSync(p, 'utf-8')) : {};
};

const charactersDb = loadDb('characters');
const foreshadowingDb = loadDb('foreshadowing');
const summaryDb = loadDb('summary');

// 简单组装上下文
let promptOutput = `# 章节 ${chapNum} 写作任务\n\n## 章节大纲\n${outline}\n\n`;

// 组装历史摘要 (避免超过 token 限制，取最近 5-10 章即可)
const chapterSummaries = summaryDb.chapterSummaries || [];
const recentSummaries = chapterSummaries.slice(-10);
promptOutput += `## 最近剧情摘要\n`;
if (recentSummaries.length > 0) {
  recentSummaries.forEach(s => {
    promptOutput += `- 第 ${s.chapter} 章 ${s.title}: ${s.summary}\n`;
  });
} else {
  promptOutput += "(无历史摘要，这是首章)\n";
}

// 活跃伏笔 (关注近期尚未 resolve 的线索)
const activeForeshadowing = (foreshadowingDb.foreshadowing || []).filter(f => f.status === 'planted' || f.status === 'reinforced');
promptOutput += `\n## 活跃关键伏笔\n`;
if (activeForeshadowing.length > 0) {
  activeForeshadowing.forEach(f => {
    promptOutput += `- ${f.name} (第 ${f.plantedChapter} 章埋设, ${f.expectedResolution})\n`;
  });
} else {
  promptOutput += "(无活跃伏笔)\n";
}

// 可选: 角色信息。如果角色信息太长，应由 Agent 自己裁剪，该工具输出主要存活角色
const activeChars = (charactersDb.characters || []).filter(c => c.status === 'active');
promptOutput += `\n## 活跃角色状态参考\n`;
activeChars.forEach(c => {
  let details = c.profile ? c.profile.background : "无背景描述";
  let curState = c.currentState ? c.currentState.physical : "未知身体状况";
  promptOutput += `- ${c.name} (${c.role}): ${details} [当前状态: ${curState}]\n`;
});

promptOutput += `\n**指令**：\n请根据以上上下文和章节大纲，严谨、优美地续写第 ${chapNum} 章的具体小说内容，字数要求 3000 字以上。\n`;

// 打印给 Agent 读取
console.log(promptOutput);
