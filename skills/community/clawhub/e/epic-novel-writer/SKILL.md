---
name: epic-novel-writer
version: 1.2.1
license: BSD-3-Clause
description: 史诗级长篇网络小说创作skill，包含13阶段写作流程、人物设定、分卷规划、子Agent并行撰写、全文校验、存档管理等完整工作流。覆盖中篇（10-25万字）到超长篇（60-150万字），实测 420,000 字 / 300 章 / 10 卷。支持全局连续编号、只读存档、人物画像 JSON、HTML 导引页生成。
description_zh: "史诗级长篇写作：13 阶段工作流（构思→人物→分卷→章级蓝本→前三章定调→分卷并行撰写→整卷/全文校验→只读存档），全局连续章节编号，人物画像 JSON + HTML 导引页，实测 42 万字 / 300 章 / 10 卷。"
description_en: "Novel writing full workflow — from world-building and character design to chapter planning, manuscript writing, version archiving, and HTML guide generation. Covers medium (100-250k words) to super-long (600k-1.5m words), proven with 420k words / 300 chapters / 10 volumes. Supports global continuous numbering, read-only archives, character JSON, and HTML guides."
homepage: https://clawhub.ai/sunshinejnjn/epic-novel-writer
metadata:
  openclaw:
    emoji: "🖊️"
compatibility: Pure Markdown workflow, no external dependencies. Requires OpenClaw file I/O and shell execution capabilities.
allowed-tools: Read, Write, Edit, Exec
---

# epic-novel-writer — 史诗级长篇写作 Skill

> **语言说明**：本 skill 的流程文档以中文编写（面向中文网文创作场景，目录与术语为中文）；产出内容（正文、大纲、报告）的语言跟随用户项目语言，不限于中文。英文文档见 `README.md`。

## 适用篇幅

| 篇幅 | 章节数 | 字数范围 |
|------|--------|---------|
| 中篇 | 30-80 章 | 10-25 万字 |
| 长篇 | 80-200 章 | 25-60 万字 |
| 超长篇 | 200-500 章 | 60-150 万字 |

> 实测标杆：420,000 字 / 300 章 / 10 卷

## 核心规则

### 所有编辑必须在 `在编辑稿/` 目录上完成
- 修改 → 操作 `在编辑稿/` 的文件
- 不要修改该目录外的文件

### 存档版本（v1/v2/v3...）是只读的
- 用于对比/核对/历史回溯
- 如需对比先读存档参考，然后修改 `在编辑稿/`

### 存档条件
仅在用户**明确发出存档指令**时执行（"存成 v1"、"终稿了"、"存档"等）；不得把一般性讨论当作存档意图，拿不准先向用户确认。按顺序递增。

### 安全规则
- 小说标题**不得直接拼入 shell 命令**（命令注入风险）：先按 `references/archive-template.md` 的白名单净化，路径展开一律加引号
- 存档/反向合并前必须先向用户确认；反向合并会覆盖 `在编辑稿/`，建议先备份

## 写作流程（13 阶段）

1. **构思沟通** → 故事类型、主题、篇幅、视角 → `01-story-premise.md`
2. **人物设定** → 主角团/配角/关系/时间线 → `references/characters/`
3. **核对修订人物** → 2 遍（年龄/关系/出场顺序/时间线）
4. **分卷规划** → 每卷标题/章节范围/核心冲突 → `03-outline/00-master-outline.md`
5. **卷级大纲** → 章节列表/节奏/伏笔/人物变化 → `03-outline/vol-{N}-outline.md`
6. **章级蓝本** → 场景/人物/情节/伏笔 → `03-outline/vol-{N}/chapter-{XX}-blueprint.md`
7. **撰写前三章** → 2 遍校验 + 润色，用户确认定调
8. **分卷并行撰写** → Sub-Agent 并行，卷内串行
9. **整卷校验** → 通读全卷 + 蓝本核对 → `06-validation/vol-{N}-validation-report.md`
10. **重复 4-9** 依次完成各卷
11. **全卷并行修订** → Sub-Agent 并行，2 遍
12. **全文校验** → 3 遍（全局一致性/连贯性/文笔终检）
13. **存档 v0**（须先经用户明确确认，非自动步骤）→ 按 `references/archive-template.md` 执行（含标题净化、路径加引号、风险确认规则）

**命名规则：** 文件名 = 章编号 = 全局连续三位数。`chapter-001.md`（第 1 章），`chapter-031.md`（卷 2 第 1 章）。

## 存档流程

存档时按 `references/archive-template.md` 执行 8 步：
- 生成人物画像 `char_data.json`（主要角色 + 次要角色）
- 生成 HTML 导引页（暗色主题，响应式，章节全局连续编号）
- 每个存档版本独立只读目录

## 子文件

| 文件 | 内容 |
|------|------|
| `references/project-structure.md` | 项目目录结构定义 + 核心规则 |
| `references/lifecycle.md` | 13 阶段完整流程详情（每阶段产出文件） |
| `references/name-rules.md` | 命名规则（全局连续编号、各文件命名表） |
| `references/archive-template.md` | 存档流程模板（8 步 + 命令示例 + 检查清单） |
| `references/world-setting-template.md` | 世界观设定模板 |
| `references/character-card-template.md` | 人物卡模板 |
| `references/chapter-blueprint-template.md` | 章级蓝本模板 |

**许可**：BSD 3-Clause（见 `LICENSE`）。
