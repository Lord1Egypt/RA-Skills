#!/usr/bin/env node
/**
 * CosDesign — Style Definition Document Generator
 * PROMPT GENERATOR ONLY — outputs a structured agent prompt.
 *
 * Generates a human-readable design style definition document
 * that describes the visual identity in natural language + tokens.
 *
 * Usage:
 *   node scripts/define-style.js <url>
 *   node scripts/define-style.js <url> --name "ProjectName"
 */

const args = process.argv.slice(2);
const nameIdx = args.indexOf('--name');
const projectName = nameIdx !== -1 ? args[nameIdx + 1] : null;
const url = args.filter(a => !a.startsWith('--') && a !== projectName)[0];

if (!url) {
  console.error('Usage: node scripts/define-style.js <url> [--name "ProjectName"]');
  process.exit(1);
}

let hostname;
try { hostname = new URL(url).hostname.replace('www.', ''); } catch { hostname = url; }
const name = projectName || hostname;

console.log(`=== COSDESIGN — 风格定义文档 ===
目标 URL：${url}
项目名称：${name}

你是一个资深设计总监。你的任务是从目标 URL 中提炼出完整的视觉风格定义文档，
这份文档将作为团队设计和开发的"设计宪法"。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第一步 — 获取页面
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

使用 WebFetch 获取 ${url}，提取完整的视觉设计信息。
补充使用 WebSearch 搜索该品牌的设计语言相关信息（如有公开 Brand Guide）。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第二步 — 输出风格定义文档
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ${name} — 设计风格定义

## 1. 视觉性格

用 3-5 个关键词定义这个设计的视觉性格（如：极简 / 圆润 / 高对比 / 科技感 / 温暖），
并用 2-3 句话展开说明为什么选择这些词。

## 2. 色彩哲学

- 主色调的情感含义和使用场景
- 色彩对比度策略（高对比？柔和？）
- 深色/浅色模式策略
- 色彩语义映射（成功/警告/错误/信息）

附：完整色卡表格（名称 | HEX | 用途 | CSS变量）

## 3. 字体性格

- 字体选择的理由（几何无衬线？人文衬线？等宽？）
- 标题与正文的视觉反差策略
- 字号阶梯的数学逻辑（1.25倍？1.333倍？）
- 字重使用规则

附：完整字体规格表

## 4. 空间节奏

- 基础单位（4px grid? 8px grid?）
- 元素之间的呼吸感如何营造
- 信息密度定位（紧凑？宽松？适中？）
- 垂直韵律（section 间距规律）

附：间距 token 表

## 5. 形状语言

- 圆角策略（全圆角？微圆角？直角？混合？）
- 阴影策略（扁平？微阴影？深层次？）
- 边框策略（visible borders? borderless? 分隔线?）

附：圆角 + 阴影 token 表

## 6. 组件设计原则

对以下核心组件，各用 1-2 句话描述设计原则：
- 按钮：...
- 卡片：...
- 导航：...
- 表单：...
- 列表：...

## 7. 动效原则（如有）

- 过渡时长偏好
- 缓动曲线偏好
- 动画风格（克制？活泼？功能性？）

## 8. 一句话设计宣言

用一句话总结这个设计风格的核心理念。
例如："以留白换呼吸，以极简传专业。"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
重要提醒
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- 所有描述必须基于页面实际分析，不是泛泛的设计理论
- 色彩、字体、间距的具体数值必须从页面中提取
- 风格定义要有观点和立场，不要写成中庸的模板
- 这份文档的目标读者是设计师和前端工程师
`);
