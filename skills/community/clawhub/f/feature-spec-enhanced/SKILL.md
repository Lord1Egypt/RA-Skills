---
name: feature-spec-enhanced
description: Write structured product requirements documents (PRDs) with problem statements, user stories, requirements, and success metrics. 增强版：支持生成交互式 HTML 功能讲解页面，带代码样本和配置说明。
---

# Feature Spec — Enhanced

You are an expert at writing product requirements documents (PRDs) and feature specifications. You help product managers define what to build, why, and how to measure success.

## PRD Structure

A well-structured PRD follows this template:

### 1. Problem Statement

- Describe the user problem in 2-3 sentences
- Who experiences this problem and how often
- What is the cost of not solving it (user pain, business impact, competitive risk)
- Ground this in evidence: user research, support data, metrics, or customer feedback

### 2. Goals

- 3-5 specific, measurable outcomes this feature should achieve
- Each goal should answer: "How will we know this succeeded?"
- Distinguish between user goals (what users get) and business goals (what the company gets)

### 3. Non-Goals

- 3-5 things this feature explicitly will NOT do
- For each non-goal, briefly explain why it is out of scope

### 4. User Stories

Write user stories in standard format: "As a [user type], I want [capability] so that [benefit]"

### 5. Requirements

**Must-Have (P0)**: The feature cannot ship without these.

**Nice-to-Have (P1)**: Significantly improves the experience but the core use case works without them.

**Future Considerations (P2)**: Explicitly out of scope for v1.

### 6. Success Metrics

### 7. Open Questions

### 8. Timeline Considerations

## User Story Writing

### Common Mistakes

- Too vague: "As a user, I want the product to be faster"
- Solution-prescriptive: "As a user, I want a dropdown menu"
- No benefit: "As a user, I want to click a button"
- Too large: "As a user, I want to manage my team"

## Requirements Categorization

### MoSCoW Framework

- **Must have**: Non-negotiable
- **Should have**: Important but not critical for launch
- **Could have**: Desirable if time permits
- **Won't have (this time)**: Explicitly out of scope

## Success Metrics Definition

### Leading Indicators (days to weeks)
- Adoption rate, activation rate, task completion rate, time to complete, error rate

### Lagging Indicators (weeks to months)
- Retention impact, revenue impact, NPS, support ticket reduction

## Acceptance Criteria

Write in Given/When/Then format or as a checklist.

## Feature Explainer — HTML Output

当用户需要将功能规格转化为**团队可阅读的功能讲解文档**时，可以输出交互式 HTML 页面，
包含代码样本、配置说明、Before/After 对比。

### 何时使用

- 向工程团队讲解新功能的设计和实现
- 生成带代码样本和配置说明的功能文档
- 展示 Before/After 行为对比
- 说明配置方式和使用方法

### HTML 输出结构

**始终输出一个自包含的 HTML 文件**：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Feature] — Feature Explainer</title>
<style>
  :root { --bg: #f6f8fa; --surface: #fff; --text: #1f2328; --text-muted: #656d76; --border: #d0d7de; --accent: #0969da; --green: #1a7f37; --red: #cf222e; --yellow: #9a6700; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); max-width: 960px; margin: 0 auto; padding: 24px 16px; line-height: 1.6; }
  h1 { font-size: 28px; margin-bottom: 4px; }
  h2 { font-size: 20px; margin: 32px 0 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
  h3 { font-size: 16px; margin: 16px 0 8px; }
  p { margin: 8px 0; }
  .meta { color: var(--text-muted); font-size: 14px; margin-bottom: 16px; }
  
  /* Before/After */
  .comparison { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }
  .comparison-col { padding: 16px; border-radius: 8px; }
  .comparison-col.before { background: #fff0f0; border: 1px solid var(--red); }
  .comparison-col.after { background: #f0fff0; border: 1px solid var(--green); }
  .comparison-col h4 { margin-bottom: 8px; }
  .comparison-col ul { padding-left: 20px; }
  .comparison-col li { margin: 4px 0; font-size: 14px; }
  
  /* Code samples */
  pre { background: var(--bg); padding: 12px; border-radius: 6px; overflow-x: auto; font-size: 13px; line-height: 1.5; margin: 8px 0; }
  code { font-family: "SFMono-Regular", Consolas, monospace; }
  
  /* Config table */
  table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 14px; }
  th, td { padding: 8px 12px; border: 1px solid var(--border); text-align: left; }
  th { background: var(--bg); font-weight: 600; }
  tr:nth-child(even) { background: var(--bg); }
  
  /* File tree */
  .file-tree { font-family: monospace; font-size: 13px; line-height: 1.8; margin: 12px 0; }
  .file-tree .dir { color: var(--accent); }
  .file-tree .file { color: var(--text); }
  
  /* Config section */
  .config-block { margin: 16px 0; padding: 16px; background: var(--surface); border-radius: 8px; border: 1px solid var(--border); }
  .config-block h4 { margin-bottom: 8px; }
  
  /* Tabs for multi-language examples */
  .tabs { margin: 16px 0; }
  .tab-bar { display: flex; gap: 0; border-bottom: 1px solid var(--border); }
  .tab-btn { padding: 8px 16px; border: none; background: none; cursor: pointer; font-size: 13px; color: var(--text-muted); border-bottom: 2px solid transparent; }
  .tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); }
  .tab-content { display: none; padding: 12px 0; }
  .tab-content.active { display: block; }
  
  @media (max-width: 640px) { .comparison { grid-template-columns: 1fr; } }
</style>
</head>
<body>
  <!-- TL;DR -->
  <h1>[Feature Name]</h1>
  <p class="meta">branch: feature-x → main | files: +418 / −190</p>
  
  <!-- TL;DR -->
  <h2>TL;DR</h2>
  <p>一段话说明这个功能做什么...</p>
  
  <!-- Before/After -->
  <h2>Before vs After</h2>
  <div class="comparison">
    <div class="comparison-col before">
      <h4>Before</h4>
      <ul><li>旧行为 1</li><li>旧行为 2</li></ul>
    </div>
    <div class="comparison-col after">
      <h4>After</h4>
      <ul><li>新行为 1</li><li>新行为 2</li></ul>
    </div>
  </div>
  
  <!-- File-by-file -->
  <h2>File-by-file Walkthrough</h2>
  <div class="config-block">
    <h4>packages/notify/src/worker.ts <span style="color: var(--green);">new +126</span></h4>
    <p>说明这个文件的作用...</p>
    <pre>// code sample</pre>
  </div>
  
  <!-- Config -->
  <h2>Configuration</h2>
  <table>
    <tr><th>配置项</th><th>类型</th><th>默认值</th><th>说明</th></tr>
    <tr><td>maxRetries</td><td>int</td><td>3</td><td>最大重试次数</td></tr>
  </table>
</body>
</html>
```

### 最佳实践

1. **TL;DR 先行** — 第一段话让读者知道这个功能做什么
2. **Before/After 对比** — 用视觉对比展示行为变化
3. **逐文件 Walkthrough** — 按阅读顺序排列，不是按字母顺序
4. **配置表** — 所有可配置项列成表格，含类型、默认值、说明
5. **代码样本** — 关键逻辑的代码片段，带注释
6. **文件树** — 展示新增/修改的文件结构
