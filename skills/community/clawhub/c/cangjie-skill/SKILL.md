---
name: book2skill
description: "把一本书里沉淀的方法论蒸馏成一组原子化、可被Agent调用的skills，同时产出给人看的笔记和话术库。触发：用户说'帮我拆《XX》''把XX蒸馏成skill''distill this book into skills'时。不做书摘/读后感/作者人设角色扮演。"
tags: [skill-creation, knowledge-distillation, methodology]
version: 2.0.0
author: "花叔 AlchainHust (原版) · mac-openclaw-manager (改造版)"
license: MIT
---

# book2skill — 把一本书蒸馏成一组可执行 skills 的元 skill

> 📦 改造版 v2.0.0 · 基于原版 book2skill 新增阶段5（人性化输出）
> 原版作者：花叔 AlchainHust · MIT License
> 改造内容：新增 methodology/07-stage5-human-output.md + LEARNING_NOTE.md.template + TALKING_POINTS.md.template

## 使命

把一本书里沉淀的方法论，拆解成一组**原子化、可被 agent 在真实场景下调用**的 skills，让读者真正用起来——同时产出**给人看的笔记和话术库**。

**边界**：
- ✅ 做：方法论 / 决策框架 / 清单 / 原则 / 概念体系的蒸馏，学习笔记，话术库
- ❌ 不做：书摘 / 读后感 / 作者人设角色扮演（后者请用 nuwa-skill）

## 核心方法论：RIA-TV++

一个五阶段 + 并行提取 + 三重验证 + darwin 兼容测试的流水线。详见 `methodology/00-overview.md`。

```
阶段 0: Adler 整书理解     → BOOK_OVERVIEW.md
阶段 1: 5 个 agent 并行提取 → 候选方法论单元池
阶段 1.5: 三重验证筛选      → 通过的单元
阶段 2: RIA++ 构造 skill    → 每个 skill 的 SKILL.md
阶段 3: Zettelkasten 链接   → INDEX.md
阶段 4: 压力测试 (darwin兼容) → test-prompts.json + 回炉淘汰
🆕 阶段 5: 人性化输出       → LEARNING_NOTE.md + TALKING_POINTS.md
```

## 何时调用此 skill

用户说类似：
- "帮我拆《穷查理宝典》"
- "把毛选蒸馏成 skill"
- "distill this book into skills: <path>"
- "我想把这本书的方法论做成可用的 skill"

## 输入要求

在开始前**必须**从用户处确认：
1. **书的文本来源**：PDF / EPUB / TXT 文件路径，或可访问的纯文本。**不要**在没有文本的情况下"凭记忆"拆书 — 宁可停下来问用户要。
2. **书名 + 作者 + 出版年**：用于目录命名和审计。
3. **是否首次试点**：如果用户是第一次用 book2skill，建议先拆 1 本验证流程再批量。

## 异常处理

| 场景 | 处理动作 |
|------|---------|
| 文本路径无效/无法访问 | 暂停并明确告知用户「无法读取，请检查路径或直接粘贴文本」，不等、不猜、不跳过 |
| 用户未提供文本直接说「开始拆」 | 反问确认文本来源，不凭记忆拆书 |
| 子 agent 并行提取超时/失败 | 单个失败：用主 agent 补跑该 extractor；多个失败：降级为串行提取，逐项确认后再继续 |
| 阶段0用户不确认骨架 | 最多等 2 轮追问后接受用户说「继续」，不做无确认的下一步 |
| 候选单元全部被三重验证淘汰 | 展示 rejected/ 清单给用户，询问「放宽标准 / 换书 / 放弃」，不做空输出 |
| 压力测试通过率 <80% | 强制回炉阶段2，不跳过，不表面修补 |

## 输出结构

```
books/<book-slug>/
├── BOOK_OVERVIEW.md           # 阶段 0 产出：主旨/骨架/术语/批判
├── INDEX.md                   # 阶段 3 产出：skill 总览 + 引用图
├── LEARNING_NOTE.md           # 🆕 阶段 5 产出：给人看的笔记
├── TALKING_POINTS.md          # 🆕 阶段 5 产出：话术库
├── candidates/                # 阶段 1 产出：原始候选池（审计用）
├── rejected/                  # 阶段 1.5 淘汰的单元 + 原因（审计用）
├── <skill-slug-1>/
│   ├── SKILL.md
│   └── test-prompts.json      # darwin-skill 兼容格式
├── <skill-slug-2>/
│   └── ...
```

## 执行流程（严格按顺序）

### 阶段 0 — 整书理解

1. 读取用户提供的书本文本。大文件分块阅读。
2. 执行 `methodology/01-stage0-adler.md` 中的 Adler 四步（结构 / 解释 / 批判 / 应用）。
3. 按 `templates/BOOK_OVERVIEW.md.template` 填充，写入 `books/<slug>/BOOK_OVERVIEW.md`。
4. 把产出展示给用户确认："骨架我理解对了吗？有没有你希望重点突出的方向？" 得到确认再进入阶段 1。

### 阶段 1 — 5 个 sub-agent 并行提取

**并行** spawn 5 个 Task sub-agents（使用 Agent 工具，一次调用中发起 5 个）：

| sub-agent | 读取的 prompt | 产出 |
|---|---|---|
| 框架提取器 | `extractors/framework-extractor.md` | 决策框架 / 思维模型 |
| 原则提取器 | `extractors/principle-extractor.md` | 原则 / 清单 / 规则 |
| 案例提取器 | `extractors/case-extractor.md` | 作者在书中亲自使用过的实例 |
| 反例提取器 | `extractors/counter-example-extractor.md` | 书中警告的失败模式 |
| 术语提取器 | `extractors/glossary-extractor.md` | 关键概念词典 |

每个 sub-agent 独立读书、独立提取、独立输出到 `books/<slug>/candidates/<type>.md`。

**模型选择**：子 agent 模型推荐 doubao-lite（系数0.5，Lite套餐内几乎免费），备选 DSF（按量¥0.05/1M token）。doubao-lite 在 benchmark 中 6s 完成、质量与 DSF 持平，且成本远低于 DSV4 Pro。

### 阶段 1.5 — 三重验证筛选

读取 `methodology/03-stage1.5-triple-verify.md`，对每个候选单元执行：

- **V1 跨域**：书中至少 2 个独立段落有佐证？
- **V2 预测力**：能用它回答一个书里没明说的新问题吗？
- **V3 独特性**：不是任何聪明人都会说的常识吗？

通过的进入阶段 2。不通过的写入 `books/<slug>/rejected/` 并附原因 — 保留审计轨迹，也允许用户事后捞回。

### 阶段 2 — RIA++ 构造 skill

对每个通过的单元，按 `templates/SKILL.md.template` 填充：

- **R (Reading)**：原文引用 ≤150 字/段
- **I (Interpretation)**：用自己的话重写方法论骨架（避免照搬译本）
- **A1 (Past Application)**：书中作者用过的案例
- **A2 (Future Trigger)** ★：用户在什么情境下会需要这个 → skill 的 `description` 字段
- **E (Execution)**：1-2-3 可执行步骤
- **B (Boundary)**：什么时候不适用 / 来自阶段 0 批判阶段的作者盲点

细则见 `methodology/04-stage2-ria-plus.md`。

### 阶段 3 — Zettelkasten 链接

按 `methodology/05-stage3-zettelkasten.md`：
1. 找出 skill 之间的引用关系（A 依赖 B / A 对比 B / A 组合 B）
2. 在每个 SKILL.md 末尾补"相关 skills"段
3. 按 `templates/INDEX.md.template` 生成 `INDEX.md`（含引用图 mermaid）

### 阶段 4 — 压力测试（darwin 兼容）

对每个 skill 按 `methodology/06-stage4-pressure-test.md`：
1. 设计 5–10 条测试 prompt，按 `templates/test-prompts.json.template` 写入 `test-prompts.json`
2. 至少包括 3 类：**应调用** / **不应调用（诱饵）** / **边界模糊**
3. 本地跑一遍，**未过的回炉重做阶段 2** — 不做"表面修补"
4. 全部通过后通知用户："已完成，可一键喂给 darwin-skill 自动进化"

### 🆕 阶段 5 — 人性化输出

按 `methodology/07-stage5-human-output.md`：
1. **收集复用素材** — 从 BOOK_OVERVIEW.md + INDEX.md + 各skill的RIA++段提取已有内容
2. **写学习笔记** → `LEARNING_NOTE.md`（按 `templates/LEARNING_NOTE.md.template`）
   - 一句话类比开篇
   - 每个方法论大白话解释 + 一句话案例
   - 批判视角独立成段
   - ≤3000字
3. **写话术库** → `TALKING_POINTS.md`（按 `templates/TALKING_POINTS.md.template`）
   - ≥10条话术，每条≤100字
   - 每条配场景标签
   - 话术 = 你能自然说出口的，不是作者的金句
4. **质量检查** — 两份文档读起来像朋友聊天，不像教科书

此阶段基于阶段0-4的已有分析结果，不额外消耗大量 token。

## 质量红线（违反则阻止输出）

1. 每个 skill 必须通过**全部**三重验证
2. 每个 skill 必须有完整的 R / I / A1 / A2 / E / B 六段
3. 原文引用 ≤150 字/段
4. 每个 skill 必须有 `test-prompts.json`，且包含诱饵测试（不应调用的场景）
5. `description` 字段必须明确 trigger 条件，不能只是"一个关于 X 的 skill"
6. 🆕 LEARNING_NOTE.md 必须有类比开篇
7. 🆕 TALKING_POINTS.md 话术 ≥10条

## 与 nuwa-skill / darwin-skill 的生态定位

- **nuwa-skill**：蒸馏人（思维方式 / 表达 DNA）
- **book2skill**（本 skill）：蒸馏书（方法论 / 框架 / 原则） + 人性化输出
- **darwin-skill**：进化任意 skill

三者咬合：本 skill 输出的 `test-prompts.json` 严格遵循 darwin-skill 格式，以便产出的 skill 可直接接入 darwin 做自动进化。

## 调用惯例

- **永远先试点 1 本** — 除非用户明确说"批量"
- **阶段之间主动汇报进度** — 不要静默跑完再 dump 结果
- **不凭记忆拆书** — 没文本就停下来问
- **保留审计轨迹** — candidates/ 和 rejected/ 都要留
