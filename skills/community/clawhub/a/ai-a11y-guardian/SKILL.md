---
name: ai-a11y-guardian
description: AI辅助无障碍合规守护者 — 自动化检测网页/移动端H5的无障碍问题，生成修复建议并出具合规报告
category: AI|开发|自动化
triggers: 无障碍检测, accessibility, a11y, WCAG合规, 网页无障碍, 移动端无障碍, 读屏兼容, 色盲友好, 合规报告
version: 1.0.0
author: OpenClaw Agent
tags:
  - accessibility
  - wcag
  - web
  - compliance
  - automation
  - mobile
  - inclusive-design
  - audit
dependencies:
  - agent-browser
  - summarize
  - card-renderer
---

# AI 无障碍合规守护者 (AI A11y Guardian)

一键检测网页 / H5 页面的无障碍（Accessibility）问题，对照 WCAG 2.1 / 2.2 标准出具修复建议，并生成可视化合规报告。

## 业务场景

政务平台、教育类应用、电商购物车、银行保险等涉及公共服务的 Web / H5 产品，必须满足国家《信息技术 无障碍设计规范》与 WCAG 国际标准。传统人工审查效率低、覆盖窄，且难以覆盖动态渲染的 SPA 页面。

本 Combo 编排 agent-browser、summarize、card-renderer 三个专业 Skill，一次完成页面扫描 → AI 分析 → 报告生成的全链路。

## 痛点

- 开发者不了解 WCAG 细节，代码埋下无障碍隐患
- 人工审查无法覆盖动态渲染的 JavaScript SPA 页面
- 测试报告缺乏可操作的修复指导
- 合规认证需要第三方报告，手动整理费时费力

## 工作流程

```
[输入 URL / HTML 源码 / 截图]
      ↓
agent-browser    → 深度渲染页面（含 JS 执行），截图 + 提取 DOM 结构
      ↓
summarize         → AI 对照 WCAG 2.1 AA 标准逐一分析，输出结构化问题清单
      ↓
card-renderer     → 将严重问题渲染为可视化违规卡片，生成合规摘要图
      ↓
[交付物] 问题清单 + 修复建议 + 合规报告卡片
```

## 核心功能

- **全自动页面渲染**：使用真实 Chromium 浏览器完整执行 JS，捕获 Shadow DOM、懒加载内容
- **多层级问题识别**：色彩对比度不足（AA/AAA）、键盘陷阱、缺少 ARIA 标签、图片缺少 alt、表单标签缺失、焦点顺序混乱等
- **可操作的修复建议**：每个问题附修复代码片段（HTML/CSS/ARIA），无需猜测
- **可视化合规报告**：生成违规卡片图，适合提交给合规团队或客户
- **批量 URL 扫描**：支持多个页面一次性检测，汇总成综合报告

## 使用方法

### 触发词
- `无障碍检测 <URL>`
- `a11y 检查 <URL>`
- `WCAG 合规报告 <URL>`
- `网页无障碍问题`
- `生成无障碍报告`

### 输入
提供以下任一：
- **URL**：完整网页地址（自动渲染）
- **HTML 源码**：粘贴 HTML 内容（静态分析）
- **截图文件路径**：已有页面截图（辅助分析）

### 可选参数
- `--level AA|AAA` 指定合规等级（默认 AA）
- `--format card|list` 报告格式（默认 card）

### 示例对话

**用户**：`检测 https://example.com 的无障碍问题`

**AI**：
> 🧩 Step 1: 渲染页面中...
> 🔍 Step 2: WCAG 分析中...
> 📊 Step 3: 生成合规报告中...

**检测结果示例**：

| 问题 | 严重性 | WCAG条款 | 修复难度 |
|------|--------|----------|----------|
| 图片缺少 alt 属性 | 🔴 高 | 1.1.1 Non-text Content | 🟢 易 |
| 按钮缺少可访问名称 | 🔴 高 | 4.1.2 Name, Role, Value | 🟢 易 |
| 色彩对比度不足 (5.2:1) | 🟡 中 | 1.4.3 Contrast | 🟡 中 |
| 键盘无法聚焦模态框 | 🔴 高 | 2.1.2 No Keyboard Trap | 🟡 中 |
| 表单缺少 label 标签 | 🟡 中 | 3.3.2 Labels or Instructions | 🟢 易 |

**合规摘要**：
- 总体评分：68/100
- 致命问题：2 项 | 中等问题：3 项 | 提示：7 项
- 预估修复时间：2 小时

## 输出示例

```
📋 无障碍合规报告 - example.com
生成时间：2026-04-24 19:40 UTC

🚨 致命问题 (2)
  ❌ 图片 logo.png 缺少 alt 属性 → WCAG 1.1.1
     修复：<img src="logo.png" alt="公司Logo">

  ❌ 登录按钮无名称 → WCAG 4.1.2
     修复：<button aria-label="登录">

⚠️ 中等问题 (3)
  ⚡ 搜索框对比度 3.2:1（需≥4.5:1）→ WCAG 1.4.3
  ⚡ 弹出框无法键盘关闭 → WCAG 2.1.2
  ⚡ 表单缺少必填项标记 → WCAG 3.3.2

💡 优化提示 (7)
  建议为所有图标按钮添加 aria-label...
  建议为日期选择器添加 aria-describedby...

🖼️ [合规报告卡片图片]
```

## 依赖说明

### agent-browser
用于完整渲染页面（含 JavaScript 执行）。支持等待动态内容加载，捕获 Shadow DOM、iframe 内内容，提取完整 DOM 树用于分析。

### summarize
调用 AI（MiniMax）对照 WCAG 2.1 / 2.2 标准条款，对提取的 DOM 结构进行逐条分析，输出带严重性评级的结构化问题清单，并附修复建议。

### card-renderer
将严重问题列表和高评分问题渲染为知识卡片风格的违规汇总图，图片可分享给团队或用于合规存档。

## 注意事项

- 页面需要公开可访问（内网页面请提供 HTML 源码）
- 检测基于截图 + DOM 结构，无法替代真实读屏软件测试
- 涉及登录态页面的检测请提前告知 AI 以获取测试账号
- 合规报告图片默认使用 Mac Pro 风格，可通过参数切换赛博朋克风格