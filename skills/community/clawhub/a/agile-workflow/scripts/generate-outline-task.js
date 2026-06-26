#!/usr/bin/env node
/**
 * 细纲任务描述生成器 v2.0
 * 
 * 功能：为章节细纲任务生成详细的描述文本
 * 包含：13 个模块的完整要求
 */

const fs = require('fs');
const path = require('path');

// 细纲模板路径
const TEMPLATE_PATH = '/home/ubutu/.openclaw/workspace/skills/novel-writer-assistant/templates/CHAPTER_OUTLINE_TEMPLATE_V2.md';

/**
 * 生成细纲任务描述
 * @param {string} chapterNum - 章节号
 * @param {string} chapterTitle - 章节标题
 * @param {string} projectDir - 项目目录
 * @param {object} options - 可选配置
 */
function generateOutlineTaskDescription(chapterNum, chapterTitle, projectDir, options = {}) {
  const {
    unitName = '',           // 所属单元名
    prevChapterTitle = '',   // 前章标题
    nextChapterTitle = '',   // 下章标题
    wordCount = 6500,        // 目标字数
    keyEvents = [],          // 关键事件
    characters = [],         // 出场人物
    foreshadowing = {        // 伏笔
      recover: [],           // 需要回收的伏笔
      plant: []              // 需要埋设的伏笔
    }
  } = options;

  const description = `# 细纲创作任务：第 ${chapterNum} 章「${chapterTitle}」

## 📋 任务概述
- **章节号**: 第 ${chapterNum} 章
- **章节标题**: ${chapterTitle}
- **所属单元**: ${unitName || '（请参考项目设定）'}
- **目标字数**: ${wordCount} 字（细纲字数：3000-5000 字）
- **输出路径**: ${projectDir}/04_章节细纲/第${chapterNum}章_${chapterTitle}.md

## 📚 参考资源
- **细纲模板**: ${TEMPLATE_PATH}
- **项目设定**: ${projectDir}/00_小说核心设定.md
- **世界观**: ${projectDir}/01_世界观架构/
- **人物体系**: ${projectDir}/02_人物体系/
- **情节大纲**: ${projectDir}/03_情节大纲/
${prevChapterTitle ? `- **前章细纲**: ${projectDir}/04_章节细纲/第${chapterNum - 1}章_${prevChapterTitle}.md` : ''}

## ✅ 必填模块（13 个）

### 一、基础信息
- 章节号、章节标题、所属单元、核心目标、字数要求、创作优先级

### 二、时间线定位 ⭐
- 绝对时间（开始/结束时间，持续时间）
- 相对时间（距上章/距下章）
- 时间线检查清单

### 三、空间定位 ⭐
- 主场景表（场景/地点/时间段/持续时间）
- 场景转换路径

### 四、人物出场 ⭐
- 出场人物清单（人物/出场时间/离场时间/状态变化）
- 人物状态检查清单

### 五、剧情概括
- 五幕结构（开篇/发展/高潮/转折/收尾）
- 每幕包含：场景、事件、情绪、钩子

### 六、分镜设计 ⭐ 核心
- 场景拆分表（场景/类型/字数/时间/地点/人物/核心事件）
- 场景类型标注（对话/动作/描写/心理/过渡/高潮）

### 七、详细分镜脚本 ⭐ 核心
- 每场景 3-5 个镜头
- 每镜头包含：内容、字数、情绪、文笔要点
- 关键对话（必须包含 3-5 句）

### 八、文笔要求 ⭐
- 整体风格（基调/节奏/视角）
- 各场景文笔要求（文风/节奏/情感基调/特殊要求）
- 文笔技巧要求（五感描写/对话占比/心理描写/环境描写）

### 九、情绪曲线 ⭐
- 情绪曲线图（ASCII 图示）
- 各阶段情绪表（阶段/情绪/触发点/读者感受）

### 十、伏笔管理 ⭐
- 本章回收的伏笔
- 本章埋设的伏笔
- 伏笔检查清单

### 十一、情节检查清单 ⭐
- 逻辑正确性（时间线/空间/人物状态/动机/信息合理）
- 情节推进检查

### 十二、创作参考素材（可选）
- 场景氛围参考、人物行为参考、关键词库

### 十三、输出要求
- 文件命名正确
- 保存路径正确
- 质量标准达标

## 🎯 质量标准

| 指标 | 要求 |
|------|------|
| 结构完整 | 13 个模块全部填写 |
| 分镜详细 | 每场景至少 3 个镜头 |
| 时间线正确 | 与前后章节衔接 |
| 情绪曲线清晰 | 有起伏变化 |
| 伏笔管理完整 | 埋设/回收有记录 |
| 细纲字数 | 3000-5000 字 |

## ⚠️ 重要提示

1. **时间线必须正确**: 确保与前章时间衔接，不影响后续章节
2. **分镜必须详细**: 写手应该能直接按分镜创作，无需额外思考
3. **伏笔必须追踪**: 明确标注回收哪些伏笔，埋设哪些新伏笔
4. **情绪曲线必须有**: 确保章节有节奏感，读者有情绪起伏

---

**核心原则**: 让写手拿到细纲就能直接创作，无需额外思考！

请严格按照模板创作，确保所有 13 个模块都填写完整。`;

  return description;
}

/**
 * 从任务 ID 解析章节号
 */
function parseTaskId(taskId) {
  // 支持格式: chapter-1-outline, chapter-01-outline, chapter_1_outline
  const match = taskId.match(/chapter[-_]?(\d+)/i);
  if (match) {
    return parseInt(match[1], 10);
  }
  return null;
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 3) {
    console.log('用法: node generate-outline-task.js <章节号> <章节标题> <项目目录> [选项JSON]');
    console.log('');
    console.log('示例:');
    console.log('  node generate-outline-task.js 1 "午夜当铺" /path/to/project');
    console.log('  node generate-outline-task.js 2 "归来的妹妹" /path/to/project \'{"unitName":"卷1入行"}\'');
    process.exit(1);
  }

  const chapterNum = parseInt(args[0], 10);
  const chapterTitle = args[1];
  const projectDir = args[2];
  const optionsJson = args[3] || '{}';

  let options;
  try {
    options = JSON.parse(optionsJson);
  } catch (e) {
    console.error('❌ 选项 JSON 解析失败:', e.message);
    process.exit(1);
  }

  const description = generateOutlineTaskDescription(chapterNum, chapterTitle, projectDir, options);
  console.log(description);
}

main();