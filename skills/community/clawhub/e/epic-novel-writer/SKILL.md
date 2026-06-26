---
name: epic-novel-writer
description: Novel writing full workflow — from world-building and character design to chapter planning, manuscript writing, version archiving, and HTML guide generation. Covers medium (100-250k words) to super-long (600k-1.5m words), proven with 420k words / 300 chapters / 10 volumes. Supports global continuous numbering, read-only archives, character JSON, and HTML guides.
metadata:
  openclaw:
    emoji: "🖊️"
    version: "1.1.1"
compatibility: Pure Markdown workflow, no external dependencies. Requires OpenClaw file I/O and shell execution capabilities.
allowed-tools: Read, Write, Edit, Exec
---

# epic-novel-writer — 史诗级长篇写作 Skill

---

BSD 3-Clause License

Copyright (c) 2026, sunshinejnjn@github

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## 项目结构

```
[小说标题]/
├── 在编辑稿/          ← 所有编辑工作在此目录
│   ├── 01-story-premise.md      # 故事设定
│   ├── 02-world-setting.md      # 世界观设定
│   ├── 03-chapters-written.md   # 章节完成状态
│   ├── 03-outline/              # 大纲（卷级 + 章级蓝图）
│   ├── 04-chapters/             # 章节正文（按卷分目录）
│   ├── 05-reports/              # 过程报告
│   ├── 06-validation/           # 验证报告
│   ├── references/              # 参考（人物卡、关系、线索台账）
│   └── media/                   # 图片/media
├── [小说标题]_v1/             ← 存档版本（只读）
├── [小说标题]_v2/             ← 存档版本（只读）
├── [小说标题]_v3/             ← 存档版本（只读）
└── ……
```

## ⚠️ 核心规则

### 所有编辑必须在 在编辑稿 目录上完成

- **任何时候**修改章节、大纲、参考文档，操作对象都是 `在编辑稿/` 下的文件
- 不要修改 `在编辑稿/` 之外的任何文件

### 存档版本（v1/v2/v3...）是只读的

- **禁止**在 v1/v2/v3 等存档目录上做任何编辑
- 存档版本只用于**对比、核对、历史回溯**
- 如果需要对比编辑稿和存档，先用存档作为参考，然后修改 在编辑稿 中的内容
- 违反此规则会导致内容冲突，务必遵守

### 阶段性存档规则

仅在用户**明确要求**某个版本作为阶段性成果时，才创建存档版本：
- 用户说"存成 v1"、"这是终稿了"、"存档"等类似表述
- 存档命名：`[小说标题]_v1/`、`[小说标题]_v2/` 等，按创建顺序递增

---

## 📦 版本存档

### 存档流程模板

存档的完整流程定义在以下模板文件中，存档时严格参照执行：

> **模板路径**：`references/archive-template.md`（本 SKILL 内）

该模板包含：
- 存档目录结构（每个文件的用途）
- 8 个执行步骤（从创建目录到完成检查）
- 命名规则（文件编号 = 章编号）
- 人物画像 JSON 生成指南
- HTML 导引文件生成要点
- 反向合并规则

### 存档时的工作方式

1. 先读 `references/archive-template.md` 获取完整流程
2. 按模板中的步骤逐项执行
3. 模板中每个步骤都有对应的命令示例，可直接参考执行
4. 完成后用模板中的「完成检查」清单逐项验证

### 命名规则（文件编号 = 章编号）

> **这是存档流程中的核心规则，已同步到模板中：**

- ❌ **禁止每卷内从第 1 章重新开始编号**（不要出现卷 1 有 1-30 章、卷 2 也有 1-30 章的情况）
- ✅ **文件名 = 章编号 = 全局连续三位数**：`chapter-001.md`（第 1 章）、`chapter-300.md`（第 300 章）
- ✅ 卷 1 第 1 章 = `chapter-001.md`，卷 2 第 1 章 = `chapter-031.md`（假设卷 1 有 30 章）

### 人物画像生成

存档时应生成 `char_data.json`，包含主要角色画像：

**主要角色定义**：在正文中出现频率高、推动主线或关键剧情的角色。至少包含：
- 主角
- 女主/重要配角
- 核心死党/对照
- 关键灵体
- 关键引导者

**每个角色的画像字段**：
| 字段 | 说明 |
|------|------|
| `name` | 角色名 |
| `role` | 角色定位（主角/灵体/引导者等） |
| `portrait` | 角色图片路径（media 目录） |
| `description` | 简要描述（1-3 句话） |
| `key_arc` | 角色关键成长线（→ 分隔） |
| `first_appearance` | 首次出场章节号（如"第 1 章"） |
| `affinity` | 简称/昵称（用于图片文件匹配） |

次要角色（每卷单元灵）可在 `minor_characters` 数组中补充。

### HTML 导引文件

存档时生成 `[小说标题]_导引.html`，这是存档的**核心导航页**：

**页面必须包含四个区域：**

1. **页面头部** — 标题 + 版本 + 统计数据（如"[小说标题] v3 · N 角色 · M 章"）

2. **全文简要介绍** — 从 `01-story-premise.md` 和 `02-world-setting.md` 提取，写一段 200-300 字的小说概述，包含核心主题、故事走向、整体氛围

3. **人物卡区域** — 响应式网格，每人一张卡片（图片 + 名字 + 角色定位 + 简述），暗色主题，hover 高亮

4. **章节目录区域** — 按卷分组，**章节号全局连续编号**（不是每卷从 1 开始！），每章超链接指向对应 txt 文件

**样式要求**：
- 暗色主题（背景 `#0a0a0f`，卡片 `#12121a`）
- 响应式布局（CSS Grid，移动端适配）
- 字体：`PingFang SC, Microsoft YaHei, sans-serif`
- 章节链接 hover 效果

**关键检查**：章节号是否全局连续？每个链接是否能正确导航？

---

## 📐 写作流程（完整生命周期）

> 以下为标准写作流程，按阶段顺序执行。每个阶段输出明确文件，下游阶段依赖上游产出。

### 阶段 1：构思沟通

与用户深入沟通，确定以下核心要素：
- 故事类型（奇幻/科幻/悬疑/现实/……）
- 核心主题与想要表达的情感
- 目标读者群体与文风偏好
- 预期篇幅（总章数、总字数）
- 叙事视角（第一人称/第三人称/多视角轮换）
- 基调（轻松/沉重/悬疑/热血/……）

> **篇幅估算参考**：每章约 4,000 字，每卷约 10 章（~40,000 字）。用户给定总字数后，按此标准反推总章数和卷数。例如：12 万字 → 约 30 章 → 3 卷。

**产出**：`01-story-premise.md`

### 阶段 2：人物设定（含时间线）

根据构思创建角色设定，包含：
- **主角团**：姓名、年龄、身份、外貌、性格核心、成长弧线、首次出场章
- **配角群**：核心配角、反派、辅助角色
- **人物关系**：谁和谁是朋友/敌人/恋人/师徒/对立
- **时间线**：故事起止时间、关键事件时间锚点、角色年龄变化追踪

**产出**：`references/characters/角色名.md`（每个角色一张卡片）+ `references/character-relationships.md`

### 阶段 3：核对修订人物与时间线（2 遍）

**第 1 遍核对**：
- 年龄一致性：角色年龄是否随时间线合理变化
- 关系一致性：A 是 B 的哥哥，B 是 A 的弟弟（双向验证）
- 首次出场顺序：角色不可能在出场前出现在场景中
- 时间线逻辑：事件先后顺序是否自洽

**第 2 遍修订**：
- 根据第 1 遍发现的问题修正
- 用户确认修改（或自行修正）
- 最终锁定人物设定与时间线

**产出**：修订后的人物卡片 + 关系表（时间线锁定，后续不再变动基础设定）

### 阶段 4：分卷规划

- 将故事按剧情阶段划分为若干卷
- 每卷确定：卷编号、卷标题、章节范围、核心冲突、卷内主角弧光
- 全局章号规划：确定每卷首尾章号（例如卷 1: 001-030，卷 2: 031-060）

**产出**：`03-outline/00-master-outline.md`（总纲）

### 阶段 5：卷级大纲

为每一卷撰写大纲，包含：
- 卷内章节列表（章号 + 标题 + 简要剧情说明）
- 卷内节奏规划（开篇/发展/高潮/收尾）
- 卷内伏笔清单（埋设章节 + 回收章节）
- 卷内人物变化节点

**产出**：`03-outline/vol-{N}-outline.md`（每卷一个）

### 阶段 6：章级蓝本

为每卷的每一个章节撰写蓝本（blueprint），包含：
- 场景设定（时间、地点、环境）
- 出场人物（状态 + 在本章作用）
- 情节大纲（开场→发展→高潮→收尾，按百分比分配）
- 关键事件清单
- 伏笔/线索记录（本章节埋设 + 回收）
- 技能/设定调用

**产出**：`03-outline/vol-{N}/chapter-{XX}-blueprint.md`（每章一个）

### 阶段 7：撰写前三章（开篇定调）

**先写而非先写全卷**，确保文风和叙事基调正确：
1. 按章级蓝本撰写第 1-3 章正文
2. 每章完成后进行 **2 遍校验与润色**：
   - 第 1 遍：逻辑校验（与蓝本是否一致、时间线是否正确）
   - 第 2 遍：文笔润色（节奏、对话、描写质量）
3. 用户确认前三章定调无误

**产出**：`04-chapters/vol-1/chapter-001.md` ~ `chapter-003.md`（校验润色后的定稿）

### 阶段 8：分卷并行撰写（Sub-Agent 并行）

- 使用 Sub-Agent **并行**撰写同一卷内的各章（而非全卷全章同时，避免上下文过长）
- 每卷内部章节**按顺序串行**撰写（前一章完成后再写下一章，保证连贯性）
- 每个 Sub-Agent 负责一个卷内章节，拿到蓝本 + 前文上下文
- 写完即校验

**产出**：`04-chapters/vol-{N}/chapter-{XX}.md`

### 阶段 9：整卷校验与蓝本核对

卷内所有章节完成后，执行：
1. **整卷校验**：通读全卷，检查剧情连贯性、角色一致性、伏笔回收情况
2. **蓝本核对**：对比蓝本与正文，检查是否偏离预设、是否有遗漏的伏笔/设定
3. 修正发现的问题
4. 用户确认本卷定稿

**产出**：修订后的正文 + `06-validation/vol-{N}-validation-report.md`（校验报告）

### 阶段 10：重复阶段 4-9，依次完成各卷

- 按卷编号顺序，重复分卷规划 → 章级蓝本 → 前三章式开篇校验 → 分章撰写 → 整卷校验
- 每卷完成后锁定，不再修改（除非重大设定变更）

### 阶段 11：全卷并行修订（Sub-Agent 并行，2 遍）

所有卷完成后，使用 Sub-Agent **并行**执行修订：
- 每个卷由一个 Sub-Agent 独立修订
- **第 1 遍修订**：逻辑/设定一致性校验 + 剧情润色
- **第 2 遍修订**：文笔打磨 + 细节完善

**产出**：修订后的各卷正文

### 阶段 12：全文校验（3 遍）

全书完成后，执行全文级别校验：
- **第 1 遍**：全局一致性校验（人物年龄、关系、能力随章节变化是否合理）
- **第 2 遍**：剧情连贯性校验（跨卷伏笔、悬念回收、节奏分布）
- **第 3 遍**：文笔终检（风格统一性、对话差异化、描写质量）

**产出**：全文定稿 + `06-validation/full-book-validation-report.md`

### 阶段 13：存档 v0

全书定稿后，执行第一次完整存档：
- 按 `references/archive-template.md` 执行 8 步存档流程
- 存档命名：`[小说标题]_v0/`（v0 表示全书完成的首个存档）
- 生成人物画像 JSON + HTML 导引页 + 全文合并版

**产出**：`[小说标题]_v0/` 完整存档目录

---

## 📏 适用篇幅

| 篇幅 | 章节数 | 字数范围 | 推荐程度 |
|------|--------|---------|---------|
| 中篇 | 30-80 章 | 10-25 万字 | ✅ 完全覆盖 |
| 长篇 | 80-200 章 | 25-60 万字 | ✅ 完美匹配 |
| 超长篇 | 200-500 章 | 60-150 万字 | ✅ 完全胜任 |

> 💡 **实测标杆**：本项目已用于生成 **420,000 字**（300 章，10 卷），验证了全局连续编号、防崩设定体系、HTML 导引页生成等核心功能在超长篇场景下的可靠性。

## 📏 适用篇幅

| 篇幅 | 章节数 | 字数范围 | 推荐程度 |
|------|--------|---------|---------|
| 中篇 | 30-80 章 | 10-25 万字 | ✅ 完全覆盖 |
| 长篇 | 80-200 章 | 25-60 万字 | ✅ 完美匹配 |
| 超长篇 | 200-500 章 | 60-150 万字 | ✅ 完全胜任 |

> 💡 **实测标杆**：本项目已用于生成 **420,000 字**（300 章，10 卷），验证了全局连续编号、防崩设定体系、HTML 导引页生成等核心功能在超长篇场景下的可靠性。

## 注意事项

- 不要在存档版本上做任何编辑
- 不要在 在编辑稿/ 之外创建或修改内容
- 生成存档时确保所有章节都已正确排序和合并
- 如果用户没有明确要求存档，不要擅自创建 v1/v2/v3 目录
- **文件编号 = 章编号 = 全局连续三位数，不要每卷从 1 开始**
- **存档时务必生成人物画像 JSON 和 HTML 导引文件**
