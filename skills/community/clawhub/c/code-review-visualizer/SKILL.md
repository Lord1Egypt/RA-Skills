---
name: code-review-visualizer
description: Generate HTML code review pages with risk tags, diff highlights, and file-level annotations. 当用户需要代码审查可视化、PR审查报告、代码diff高亮、风险标签标注、审查页面生成时使用。
---

# Code Review Visualizer

生成带风险标签、diff 高亮、文件级标注的 HTML 代码审查页。将传统的纯文本 diff 和 markdown 审查意见转化为**可视化、可交互的 HTML 审查页面**，让审查者一眼看清代码变更的形状和风险分布。

## 何时使用

- 代码审查（Code Review）时，需要比纯文本 diff 更直观的审查报告
- 需要向团队解释一个 PR 的变更范围和风险等级
- 需要生成带逐文件 diff + 风险标注 + 修改动机的 PR 描述
- 新人 onboarding 时解释某个模块的调用链路和信任边界

## 核心能力

### 1. PR 审查摘要页
- PR 标题 + 动机 + TL;DR
- **风险热力图**：safe / worth a look / needs attention 三级标签
- 逐文件 diff，带语法高亮和风险标签
- Before/After 行为对比

### 2. PR 描述生成
- 动机（Why）— 解决了什么问题
- 逐文件 Walkthrough — 按阅读顺序排列，带 why
- Before/After 行为对比表
- 审查重点提示

### 3. 代码理解页
- 模块调用链路可视化（boxes & arrows）
- 信任边界标注
- 逐步骤代码 Walkthrough，可展开/折叠源码

## 输出格式

**始终输出一个自包含的 HTML 文件**，可通过 `<canvas>` 工具呈现，或直接发送给用户浏览器打开。

HTML 结构：
- 单文件，无外部依赖（所有 CSS/JS 内联）
- 响应式布局，手机可看
- 使用 GitHub 风格 diff 配色（绿=新增，红=删除）
- 风险标签用颜色区分：🟢 safe / 🟡 worth a look / 🔴 needs attention

## HTML 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PR #XXX — Review Summary</title>
<style>
  :root {
    --bg: #0d1117;
    --surface: #161b22;
    --border: #30363d;
    --text: #c9d1d9;
    --text-muted: #8b949e;
    --accent: #58a6ff;
    --green: #2ea043;
    --red: #da3633;
    --yellow: #d29922;
    --diff-add-bg: rgba(46,160,67,0.15);
    --diff-del-bg: rgba(218,54,51,0.15);
    --diff-add-line: #2ea043;
    --diff-del-line: #da3633;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    max-width: 960px;
    margin: 0 auto;
    padding: 24px 16px;
  }
  h1 { font-size: 24px; margin-bottom: 4px; }
  h2 { font-size: 20px; margin: 32px 0 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
  h3 { font-size: 16px; margin: 16px 0 8px; }
  p { margin: 8px 0; }
  a { color: var(--accent); text-decoration: none; }
  
  .meta { color: var(--text-muted); font-size: 14px; margin-bottom: 16px; }
  .meta span { margin-right: 16px; }
  
  /* Risk badges */
  .risk { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 600; }
  .risk-safe { background: rgba(46,160,67,0.2); color: var(--green); }
  .risk-worth { background: rgba(210,153,34,0.2); color: var(--yellow); }
  .risk-attention { background: rgba(218,54,51,0.2); color: var(--red); }
  
  /* Risk map */
  .risk-map { display: flex; gap: 16px; flex-wrap: wrap; margin: 12px 0; }
  .risk-map-item { padding: 8px 16px; border-radius: 8px; background: var(--surface); border: 1px solid var(--border); }
  
  /* Diff block */
  .file-block { margin: 16px 0; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
  .file-header {
    background: var(--surface);
    padding: 8px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
  }
  .file-path { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 13px; }
  .file-stats { color: var(--text-muted); font-size: 12px; }
  .diff-line { font-family: "SFMono-Regular", Consolas, monospace; font-size: 12px; padding: 2px 16px; white-space: pre; }
  .diff-add { background: var(--diff-add-bg); border-left: 3px solid var(--diff-add-line); }
  .diff-del { background: var(--diff-del-bg); border-left: 3px solid var(--diff-del-line); }
  .diff-ctx { border-left: 3px solid transparent; }
  
  /* Before/After */
  .comparison { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }
  .comparison-col { padding: 16px; border-radius: 8px; }
  .comparison-col.before { background: var(--diff-del-bg); border: 1px solid var(--red); }
  .comparison-col.after { background: var(--diff-add-bg); border: 1px solid var(--green); }
  .comparison-col h4 { margin-bottom: 8px; }
  .comparison-col ul { padding-left: 20px; }
  .comparison-col li { margin: 4px 0; }
  
  /* Code walkthrough */
  .step { margin: 16px 0; padding: 16px; background: var(--surface); border-radius: 8px; border-left: 4px solid var(--accent); }
  .step-num { display: inline-block; width: 24px; height: 24px; border-radius: 50%; background: var(--accent); color: var(--bg); text-align: center; line-height: 24px; font-size: 12px; font-weight: 700; margin-right: 8px; }
  .step-title { font-weight: 600; }
  .step-desc { color: var(--text-muted); margin: 8px 0; }
  .step-code { background: var(--bg); padding: 12px; border-radius: 6px; overflow-x: auto; margin: 8px 0; }
  .step-code pre { margin: 0; font-size: 13px; }
  .step-code summary { cursor: pointer; color: var(--accent); font-size: 13px; }
  details { margin: 8px 0; }
  
  /* Trust boundary */
  .trust-boundary { padding: 12px 16px; margin: 12px 0; border: 2px dashed var(--yellow); border-radius: 8px; background: rgba(210,153,34,0.05); }
  .trust-boundary strong { color: var(--yellow); }
  
  @media (max-width: 640px) {
    .comparison { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>
  <!-- Content goes here -->
</body>
</html>
```

## 使用指南

### 场景 1：PR 审查摘要

用户提供 PR diff 或 git 输出，生成包含以下结构的 HTML：

1. **PR 标题 + 描述** — TL;DR 一句话总结
2. **风险地图** — 按文件列出风险等级
3. **逐文件 diff** — 带语法高亮的 diff，标注风险标签
4. **审查建议** — 告诉审查者应该重点关注哪里

### 场景 2：PR 描述生成

用户提供分支名和变更文件列表，生成：

1. **Why** — 变更动机，Before/After 对比
2. **File-by-file** — 按阅读顺序排列的文件说明
3. **Where to focus** — 审查者应关注的文件

### 场景 3：代码 Walkthrough

用户提供代码文件或模块路径，生成：

1. **请求路径** — 从入口到出口的数据流
2. **逐步骤代码** — 可展开的源码块 + 注解
3. **信任边界** — 标注安全边界和外部依赖

## 注意事项

- 所有 CSS 和 JS 必须内联，不引用外部资源
- diff 颜色使用 GitHub 暗色主题配色
- 风险标签只用三种：🟢 safe / 🟡 worth a look / 🔴 needs attention
- 移动端必须可读（响应式网格）
- 如果 diff 太长，只显示关键变更行（上下文行省略）
