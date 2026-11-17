---
name: aippt-generator
description: AI 驱动的专业 PPT 生成能力。当用户需要制作工作汇报、客户提案、季度总结、项目汇报、培训分享等商务演示文稿时触发此技能。通过结构化诊断收集用户核心业务内容，运用金字塔逻辑 Prompt 架构生成含原生图表的完整 PPT 成稿，并导出为可编辑的 .pptx 文件。触发词包括：做PPT、生成PPT、写汇报PPT、做演示文稿、生成幻灯片、AI做PPT、制作演示、汇报材料、proposal slides、presentation。
version: 1.0.0
license: MIT-0
---

# AIPPT Generator — AI 专业 PPT 生成

## 概述

此技能将零散的业务内容转化为结构化、可直接汇报的专业 PowerPoint 演示文稿。核心方法论：**结构化诊断收集 → 金字塔逻辑 Prompt → 一步生成完整成稿 → python-pptx 原生图表导出**。

## 核心方法论：咨询公司决策导向

**这不是课件生成器，是决策依据生成器。** 老板看 PPT 是为了做决定，不是来上课的。

核心叙事线（所有场景统一遵循）：

```
为什么做 → 不做的风险 → 方案 → 预期收益
```

绝对禁止的"AI PPT 通病"：
- "什么是 XX" / "XX 的发展历史" / "XX 的定义" 等百科/教科书式页面
- 用概念解释代替数据论证
- 用行业科普代替业务决策建议
- 任何不包含"so what"（那又怎样/所以该怎么做）的页面

## 三步工作流

### Step 1：诊断收集（确定场景 + 收集内容）

根据用户需求匹配 6 大场景之一，收集结构化信息。场景判断规则：

| 用户意图 | 场景代码 | 收集要点 |
|----------|----------|----------|
| 向上级汇报、申请预算/项目 | `boss_report` | 核心结论、为什么做、不做的风险、方案计划、预期收益 |
| 给客户的方案/提案 | `client_proposal` | 客户痛点、方案详情、成功案例、实施计划 |
| 季度/年度总结 | `quarterly_review` | KPI数据、亮点故事、不足分析、下季计划 |
| 项目进展汇报 | `project_report` | 里程碑、风险阻塞、预算、下阶段计划 |
| 培训/分享/演讲 | `training_share` | 大纲、实战案例、互动设计、可带走材料 |
| 已有内容直接转PPT | `custom` | 直接粘贴核心内容 |

**诊断要点**：
- 主动询问用户属于哪种场景；若不确定，先了解用途后推荐
- 参照 `references/scenarios.md` 中对应场景的诊断问题逐项收集
- 核心原则：**数据越具体，AI 生成越有说服力**。鼓励用户带量化数据（金额/百分比/对比基准）
- `custom` 场景无需诊断，用户直接粘贴内容即可

### Step 2：构建 Prompt 并生成 Markdown 成稿

使用三层 Prompt 架构组合完整提示词，一次调用生成完整 PPT Markdown 成稿。

**Prompt 三层架构**（组合顺序不可变）：

1. **场景专属 Prompt 模板** — 从 `references/prompt_templates.md` 取对应场景的 `prompt_template`，用用户输入安全替换 `${占位符}`
2. **共享 Prompt 要求** — 从 `references/prompt_templates.md` 取 `shared_requirements`（standard 或 custom），包含金字塔逻辑、chart 数据块规则
3. **动态注入** — 页数约束（可选）+ 图表配置（可选）

**System Prompt 角色定义**（完整版见 `references/prompt_templates.md`）：

核心信条：你是顶级管理咨询公司顾问（对标麦肯锡/BCG风格）。PPT 是决策依据，不是教学课件。绝对禁止"什么是XX""XX发展历史"等百科式页面。每页先结论后支撑，首句给结论，下接 3-5 个带量化数据的要点。

**Markdown 成稿格式规范**（必须严格遵守）：

- 每页用 `##` 标题分隔（不要用 "Slide N:"、"第N页" 等编号）
- 每页 `##` 标题下**首句先给核心结论**（一句话）
- 再用 3-5 个要点展开，要点用「对比/因果/递进」关系组织
- 每个要点必须带量化数据（金额/百分比/数量），尽量给对比基准（同比/环比/目标 vs 实际）
- 保原意：用用户输入的事实和数据，不臆造
- 图表用 chart 数据块（非 mermaid），格式见下文

**chart 数据块格式**：

```
## 渠道投放占比

抖音和小红书是核心投放渠道，占总预算70%。

- 抖音渠道转化率3.2%，高于均值2.5%
- 小红书ROI达1:4.2，获客成本最低

```chart: pie
抖音 40
小红书 30
其他 30
```
```

图表类型选择规则：
- 占比/构成 → `pie`
- 对比/排名 → `bar`
- 趋势/变化 → `xychart`（注意：数据块写 `chart: xychart`）

**禁止**：mermaid 图表、任何其他图表代码块。流程/结构/时间线一律用要点或表格表达。

### Step 3：导出为 .pptx 文件

将 AI 生成的 Markdown 成稿转换为 PowerPoint 文件。

**使用脚本**：

```bash
python3 scripts/generate_pptx.py \
  --title "PPT标题" \
  --content-file <markdown文件路径> \
  --theme business \
  --font-standard \
  --output <输出.pptx>
```

> **路径说明**：`scripts/generate_pptx.py` 指技能目录下的相对路径。执行时需先 `cd` 到技能目录，或使用完整路径。脚本依赖 `python-pptx`，首次使用时安装：`pip3 install python-pptx`。

**参数说明**：
- `--theme`: 配色主题（business/tech/minimal/vibrant），默认 business
- `--custom-colors`: 自定义配色 JSON（如 `'{"primary":"#0052A4","secondary":"#ED7D31","accent":"#10893E"}'`）
- `--font-standard / --font-compact / --font-loose`: 字号方案（标准/紧凑/宽松）
- `--font-name`: 字体族（思源黑体/微软雅黑/宋体/Helvetica/Arial）

**配色主题**：business（商务经典）/ tech（科技蓝调）/ minimal（简约黑白）/ vibrant（活力创新），默认 business。支持自定义取色。

详细配色色值、字号方案和图表选择指南见 `references/styling_guide.md`。

**依赖安装**（首次使用）：

```bash
pip3 install python-pptx
```

## 关键原则

1. **决策导向，拒绝科普**：每页必须服务于决策。禁止"什么是XX""XX发展历史"等百科式页面。核心叙事线：为什么做 → 不做的风险 → 方案 → 收益
2. **结论先行**：每页首句是核心结论，不是标题的重复展开
3. **数据驱动**：每个要点必须带量化数据，带对比基准（同比/环比/竞对/目标 vs 实际）
4. **不臆造**：只用用户提供的真实数据和事实，可适度润色表达
5. **图表原生**：chart 数据块会被后端转为 PPT 原生可编辑图表（非截图）
6. **金字塔结构**：整份PPT围绕一个核心结论展开，各页之间有逻辑递进关系

## 参考文件

| 文件 | 用途 | 何时加载 |
|------|------|----------|
| `references/scenarios.md` | 6 大场景的诊断问题与业务字段配置 | 收集用户内容时 |
| `references/prompt_templates.md` | 各场景 Prompt 模板 + 共享 Prompt 要求 | 构建 Prompt 时 |
| `references/styling_guide.md` | 配色主题、字号方案、图表选择详细指南 | 选择样式时 |
| `references/example_output.md` | 金标准 PPT 成稿示例（含 chart 数据块） | 生成时作为质量锚点 |
