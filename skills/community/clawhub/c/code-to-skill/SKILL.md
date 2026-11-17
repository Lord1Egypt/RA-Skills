---
name: "建筑规范转Skill (code-to-skill)"
description: "建筑规范→AI Skill转换器。将建筑设计规范、国家标准(GB)、行业规程、法律法规转化为可查询的条文系统——按触发条件索引每一条条文，保留应/宜/可/不应/不得的法律效力措辞原文，提取数据表格为结构化JSON，绘制跨规范引用关系图。输入'把这个规范做成skill'/'查这条规范'/'建立规范知识库'即可使用。面向中国建筑设计规范(GB 50xxx系列)优化，也可适配任何地区的技术法规。内置自包含PDF提取引擎（本 skill 自带 scripts/extract.py + book_to_skill/，无需外部安装）。| Convert building codes/GB standards/regulations into structured queryable skills — indexing clauses by trigger, preserving mandatory-force wording, extracting tables as JSON. Use when user says 'code to skill' or '把规范做成skill'."
categories: ["productivity", "engineering"]
tags: ["建筑设计", "建筑设计规范", "建筑规范", "建筑", "规范", "国家标准", "GB标准", "防火规范", "条文", "工程", "building-code", "GB-standards", "regulation", "fire-protection", "code-to-skill", "法规", "审图", "结构设计", "GB50016"]
version: 1.0.6
slug: code-to-skill
author: 51comic
license: MIT-0
compatibility: "OpenClaw 0.5+ / 通用技能运行时；需本地 Python 3.8+，可选 poppler-utils(pdftotext) 提升提取质量；本 skill 自带 scripts/extract.py + book_to_skill/ 自包含引擎，无需外部安装。"
---

<!--
Cross-agent notes (informational; ignored by host agents):
  - Compatible skill roots: OpenClaw (<workspace>/skills/),
    GitHub Copilot CLI (~/.copilot/skills, ~/.agents/skills),
    Claude Code (~/.claude/skills).
  - **Self-contained**: This skill bundles its own PDF extraction engine —
    `scripts/extract.py` (a vendored, self-contained copy that needs no
    external `book-to-skill` install). Usage: `python3 <skill>/scripts/extract.py
    <pdf> --mode text --install-missing ask`.
  - Argument hint: <path-to-regulation-pdf>... [regulation-slug]
-->

# Code-to-Skill · 建筑规范转换器

**将建筑设计规范、国家标准（GB）、行业规程、法律法规转化为结构化的、可查询的 AI Skill。**

Transforms building codes and regulations into queriable rule systems — indexing every clause by its trigger conditions and preserving mandatory-force wording exactly.

## 何时激活 / When to Activate

当用户表达以下意图时使用本技能（匹配 `description` 中的触发关键词）：

- 提到「把这个规范做成skill」「查这条规范」「建立规范知识库」「code to skill」「把规范做成skill」
- 手头有建筑规范 / 国家标准(GB) / 行业规程 / 法律法规的 **PDF**，希望转成可查询的 AI Skill
- 需要把规范条文按触发条件索引、保留「应 / 宜 / 可 / 不应 / 不得」法律效力措辞原文
- 需要把规范数据表格提取为结构化 JSON、绘制跨规范引用关系图

## 何时不激活 / Anti-Triggers

以下情况不要使用本技能，改用更合适的工具：

- 用户只想要**书籍 / 论文的概括摘要**（蒸馏式）→ 用兄弟 skill `book-to-skill`
- 没有提供规范 PDF 却只给了规范编号（如 "GB 50016"）→ 必须先索取 PDF，不要凭记忆编造条文
- 需要**法律意见或合规性判定** → 本技能是检索工具，不替代注册建筑师 / 工程师专业判断
- 纯文本小说、非规范性文档 → 不属于「规范索引」范畴

---

## 核心理念 · Philosophy

**书需要提炼（Distill），但规范需要索引（Index）。**

建筑规范不是叙事文本。它是一套以编号条文构成的决策规则系统："当条件 X 满足时，应/宜/可/不应/不得执行 Y"，每个条文有明确的法律效力层级。这个 Skill 的工作不是概括这些规则，而是让每一条条文都能**按使用场景被检索到**。

**Books need distillation; codes need indexing.**

A building code is not a narrative. It is a system of numbered clauses, each acting as a decision rule: "When condition X, requirement Y applies, with force Z."

**三条不可违反的规则 · Three Inviolable Rules：**

1. **绝不改写强制性条文。** "应"就是"应"，不是"建议"；"不应"就是"不应"，不是"不要"。每条条文的法律效力措辞必须原文保留。
2. **每个编号条文都是可检索目标。** 只要原规范里有"5.5.21"这条条文，Skill 就必须能通过"疏散宽度"→5.5.21 找到它。没有一条条文太小而不值得索引。
3. **表格是数据，不是文字。** 耐火等级表、防火间距表、疏散宽度表——这些是决策输入，不是叙事内容。必须提取为结构化数据（JSON），支持程序化查询。

**与 book-to-skill 的对比：**

| | book-to-skill | code-to-skill |
|---|---|---|
| 输入 · Input | 书籍、论文、文档 | 建筑规范、GB 标准、法规 |
| 核心动作 · Action | 蒸馏 → 概括 | 索引 → 映射 |
| 措辞规则 · Wording | 不复制原文 | **不改写条文** |
| 输出格式 · Output | `chapters/chNN-*.md`（摘要） | `clauses/chNN-*.md`（原文 + 元数据） |
| 数据输出 · Data | `cheatsheet.md`（可视化） | `tables/*.json`（结构化，可查询） |
| 导航方式 · Navigation | `patterns.md` + 词汇表 | `mandatory-map.md` + `cross-refs.md` |

---

## 运行模式 · Modes of Operation

### 1. 全量转换 · Full Conversion（默认）
**触发:** 用户提供规范 PDF 路径
**动作:** 执行全部步骤（Step 0–10）
**产物:** 完整 Skill：SKILL.md + clauses/ + tables/ + cross-refs.md + mandatory-map.md

### 2. 仅分析 · Analyze Only
**触发:** 用户说 "analyze"、"先分析" 或 "I want to review before generating"
**动作:** 执行 Step 0–4，生成提取报告后停止
**产物:** 分析报告，供用户审查后决定是否继续

### 3. 更新/补充 · Update / Supplement
**触发:** 用户已有规范 Skill，要添加地方标准补充或新版本
**动作:** 执行 Step 0–2，然后合并新条文/表格
**产物:** 更新后的已有 Skill

---

## Step 0 — 输入验证 · Input Validation

如果没有提供参数，停止并回复：
> "code-to-skill requires a regulation PDF path. Usage: `code-to-skill <path-to-regulation.pdf> [regulation-slug]`"

全过程：
- 识别输入的 PDF 路径和可选的规范 slug。
- 如果用户只提到规范但没有提供文件，询问："请提供规范 PDF 文件的路径。"
- 如果用户只提供了规范编号（如 "GB 50016"），请他们也提供 PDF 文件——不要凭记忆编造内容。
- 如果最后一个参数看起来是规范 slug（如 `gb-50016-2018`），将其视为 `REGULATION_SLUG`。

---

## Step 1 — 确认规范元数据 · Identify Regulation Metadata

提取前与用户确认：

> "确认以下信息：
> 1. **规范编号**：如 GB 50016-2014（2018 修订版）
> 2. **是否包含条文说明**：PDF 是否有条文说明部分？（条文说明解释了立法意图，Skill 中会单独标注为非强制性参考）
> 3. **目标使用场景**：设计阶段查阅？校审阶段核对？施工阶段参考？"

记录为：`REGULATION_ID`、`HAS_EXPLANATORY_NOTES`、`USE_CASE`。

---

## Step 2 — 提取文本 · Extract Text

本步骤使用内嵌的自包含 `scripts/extract.py` 引擎（随本 skill 一起提供，无需外部安装）。

**操作流程：**

1. 定位本 skill 的 `scripts/extract.py`（通常在 `<skill目录>/scripts/extract.py`）。
2. 如果用不到，也可以复用兄弟 skill `book-to-skill` 的版本（如 workspace 内已安装）：
   - `skills/book-to-skill/scripts/extract.py`（workspace 内）
   - `~/.openclaw/workspace/*/skills/book-to-skill/scripts/extract.py`
   - `~/.agents/skills/book-to-skill/scripts/extract.py`
   - `~/.claude/skills/book-to-skill/scripts/extract.py`
3. 找到后（优先用内嵌版本）用以下命令提取（规范几乎总是 **text** 模式）：

   ```bash
   python3 <extract.py路径> <规范PDF路径> --mode text --install-missing ask
   ```

产出 `<tempdir>/book_skill_work/full_text.txt` 和 `metadata.json`。读 `metadata.json` 查看提取结果。

---

## Step 2.5 — 成本估算 · Pre-flight Cost Estimate

展示以下报告：

```
📋 规范编号: <REGULATION_ID>
📄 页数: ~<N> | 字数: ~<N> | 总 Token: ~<N>K

📊 结构预估:
   检测到的条文（编号条款）: ~<N> 条
   数据表格: ~<N> 个
   引用其他规范: ~<N> 个

💰 Token 成本预估:
   输入（读取 + 提示）: ~<N>K tokens
   输出（生成文件）:      ~<N>K tokens
   合计:                  ~<N>K tokens

📁 将生成的文件:
   SKILL.md + clause-index.md + <N> 个条文文件 + <N> 个表格文件 +
   mandatory-map.md + cross-refs.md + terminology.md

➡  是否开始全量转换？（输入 "analyze only" 可先预览分析报告）
```

**等待用户确认后再继续。**

---

## Step 2.6 — 大规范分段处理 · REPL-style for Large Regulations (> 50k tokens)

```bash
# 查看全文大小
wc -w "$FULL_TEXT_PATH"

# 查找条文编号模式
grep -n -E "^[0-9]+\.[0-9]+\.[0-9]+" "$FULL_TEXT_PATH" | head -60

# 按行范围提取某一段
sed -n '<start>,<end>p' "$FULL_TEXT_PATH"

# 确认表格是否存在
grep -c -i "表[0-9]" "$FULL_TEXT_PATH"
```

中国规范常用的编号格式：`3.2.1`、`第3.2.1条`。

---

## Step 3 — 分析规范结构 · Analyze Regulation Structure

读取 `full_text.txt` 前 8,000 个字符，识别：

- **规范标题** 和 **版本**
- **发布机关**（如：中华人民共和国住房和城乡建设部）
- **章节层次结构**（如 1 总则 / 2 术语 / 3 基本规定 / ...）
- **总章节数和条文数**
- **附录数量**（附录A / B / C...）

然后扫描全文：

```bash
# 提取所有条文编号
grep -oP '^\s*\d+\.\d+\.\d+' "$FULL_TEXT_PATH" | sort -uV > /tmp/clause_numbers.txt
wc -l /tmp/clause_numbers.txt

# 识别所有数据表格
grep -oP '表\d+[\.\-]\d+' "$FULL_TEXT_PATH" | sort -uV > /tmp/table_ids.txt
wc -l /tmp/table_ids.txt

# 识别对其他 GB 标准的引用
grep -oP 'GB\s*\d{4,6}' "$FULL_TEXT_PATH" | sort -u > /tmp/cross_references.txt
wc -l /tmp/cross_references.txt
```

**如果是 "仅分析" 模式：** 在此时输出分析报告并停止。

---

## Step 4 — 确认输出范围 · Confirm Output Scope

询问用户：

> "规范包含 <N> 条条文和 <N> 个数据表。要全量处理还是只做核心章节？
> 1. 全量 — 所有条文 + 所有表格 + 条文说明
> 2. 核心章节 — 只看你常用的几章（请指定章节号）
> 3. 按主题筛选 — 只看某一类内容"

记录为 `SCOPE`。

---

## Step 5 — 确定 Skill 名称和位置 · Determine Name and Destination

从规范编号导出 slug：`{前缀}-{编号}-{年份}` → 如 `gb-50016-2018`。
对于 OpenClaw：`<workspace>/skills/<REGULATION_SLUG>/`。
如果目标已存在，询问：更新/覆盖/重命名。

---

## Step 6 — 创建目录结构 · Create Directory Structure

```bash
mkdir -p "$SKILLS_HOME/<REGULATION_SLUG>/clauses"
mkdir -p "$SKILLS_HOME/<REGULATION_SLUG>/tables"
```

---

## Step 7 — 生成条文文件 ⚠️ · Generate Clause Files

**⚠️ 关键：必须保留原文措辞，绝不改写。这是 code-to-skill 与 book-to-skill 最核心的区别。**

对 Step 3 中识别的每个章节，读取 `full_text.txt` 对应段落，创建 `clauses/ch<NN>-<描述>.md`：

```markdown
# <章节号> <章节标题>

---

## 条文 <X.X.X> <简短主题>

### 原文
> <完整原文 — 逐字复制，不改写。
>   保留所有 应/宜/可/不应/不得。
>   如有子项 (1. 2. 3.)，保留编号。>

### 强制等级
- [ ] 应 (Shall — 强制性要求)
- [ ] 宜 (Should — 推荐性要求)
- [ ] 可 (May — 允许性规定)
- [ ] 不应 (Shall Not — 禁止性要求)
- [ ] 不得 (Must Not — 绝对禁止)

### 触发条件
<条件 → 结果逻辑，用白话解释>

### 关联条文
- 本条 → <条文编号> (<关联关系>)
- 关联规范：<GB xxxx> §<章节>

### 关联数据
- 数据来源：<表号> → [查看数据](../tables/<表号>.md)

### 搜索关键词
`<关键词1>` `<关键词2>` `<关键词3>`
```

### 强制等级标注规则 · Mandatory-force Tagging Rules

| 关键词 | 标注 | 含义 |
|--------|------|------|
| `应` | 应 (Shall) | 强制性要求，违反=不合规 |
| `不应` | 不应 (Shall Not) | 强制性禁止 |
| `不得` | 不得 (Must Not) | 绝对禁止（最强等级） |
| `严禁` | 不得 (Must Not) | 绝对禁止 |
| `必须` | 应 (Shall) | 强制性要求 |
| `宜` | 宜 (Should) | 推荐，但不强制 |
| `不宜` | 不宜 (Should Not) | 不推荐，但不禁止 |
| `可` | 可 (May) | 允许，可选择 |

如果一个条文包含多个子项且强制等级不同，需要对每个子项分别标注。

### 条文说明 · Explanatory Notes

如果 `HAS_EXPLANATORY_NOTES=true`，在条文后追加：

```markdown
### 条文说明
> <条文说明 — 解释立法意图。⚠️ 本部分不具有法律强制力。>
```

---

## Step 8 — 提取数据表和交叉引用 · Extract Data Tables + Cross-references

### 8.1 数据表 → `tables/*.md` + `tables/*.json`

对 Step 3 中识别的每个数据表：

**Markdown 格式 (`tables/<表号>.md`)** — 供 Agent 阅读：

```markdown
# <表号>: <表格描述>
<!-- 来源: <REGULATION_ID> §<章节> -->

| <列1> | <列2> | ... |
|-------|-------|-----|
| ...   | ...   | ... |

## 使用说明
- **适用条件**：在什么设计场景下使用此表
- **引用该表的条文**：3.2.1, 3.2.5, ...
- **注意事项**：表格附注和注意事项
```

**JSON 格式 (`tables/<表号>.json`)** — 供程序化查询：

```json
{
  "table_id": "<表号>",
  "description": "<表格描述>",
  "source": "<REGULATION_ID> §<章节>",
  "columns": ["列1", "列2"],
  "rows": [{"列1": "值", "列2": "值"}],
  "referenced_by": ["3.2.1", "3.2.5"],
  "notes": ["附注1"],
  "units": {"列1": "m", "列2": "h"}
}
```

### 8.2 交叉引用图 → `cross-refs.md`

```markdown
# 交叉引用图 — <REGULATION_ID>

## 内部交叉引用
- 3.2.1 → 3.2.5（耐火等级补充规定）
- 5.5.21 → 5.5.17（疏散宽度与疏散人数联动）
...

## 外部交叉引用
| 本规范条文 | 引用规范 | 引用章节 | 关联关系 |
|----------|---------|---------|---------|
| 3.4.1    | GB 50045 | §6      | 高层建筑叠加 |
| 5.5.21   | GB 50084 | §7.1    | 喷淋联动 |
...

## 入站引用（可选）
| 外部规范 | 外部章节 | 引用了本规范哪条 |
...
```

---

## Step 9 — 生成主 SKILL.md · Generate Master SKILL.md

**⚠️ Token 限制：保持在 4,000 tokens 以内。**

生成 `$SKILLS_HOME/<REGULATION_SLUG>/SKILL.md`：

```markdown
---
name: <regulation-slug>
description: "规范: <REGULATION_ID> — <标题>。按条件查询条文、查阅数据表格、检查跨规范引用关系。"
---

# <REGULATION_ID>

**发布机关**: <发布机关> | **版本**: <年份> | **条文**: ~<N> | **数据表**: <N>

## 如何使用

- 不传参 → 加载规范总纲和强制性等级分布
- 传关键词如 "防火间距"、"疏散宽度" → 匹配条文并展示原文
- 传条文编号如 "5.5.21" → 直接加载该条 + 关联数据表
- "有哪些章节？" → 浏览完整条文索引
- "查表格" → 浏览所有数据表

Agent 每次回答会返回：
1. 条文**原文**（应/宜/可法律效力措辞完整保留）
2. 关联数据表
3. 关联的其他规范条文

---

## 条文索引

| 条文编号 | 主题 | 强制等级 | 触发关键词 |
|---------|------|:---:|---------|
| [3.1.1](clauses/ch03.md#条文-311) | 适用范围 | 应 | `适用范围` `总则` |
...

---

## 章节概览

| 章节 | 内容 | 条文数 | 数据表 |
|------|------|:---:|:---:|
| [1 总则](clauses/ch01-scope.md) | 适用范围和基本原则 | <N> | 0 |
| [2 术语](clauses/ch02-terms.md) | 关键术语定义 | <N> | 0 |
...

---

## 强制性等级分布

| 类型 | 数量 | 说明 |
|------|:---:|------|
| 🔴 应/必须 (Shall) | <N> | 违反 = 不合规 |
| 🟠 不应/不得 (Shall Not) | <N> | 违反 = 不合规 |
| 🟡 宜 (Should) | <N> | 推荐，非强制 |
| 🟢 可 (May) | <N> | 允许项 |

---

## 数据表索引

| 表号 | 描述 | 文件 |
|------|------|------|
| 表3.2.1 | 厂房耐火等级 | [JSON](tables/3.2.1.json) / [MD](tables/3.2.1.md) |
...

---

## 关联规范

- GB <编号> — <标题>（<N> 处引用）
...

---

## ⚠️ 重要提示

1. **条文原文不可改写** — 本 Skill 中的条文均为原文引用，法律效力措辞（应/宜/可/不应/不得）完整保留
2. **条文说明为非强制性参考** — 标注为「条文说明」的内容解释了立法意图，但本身不具有法律强制力
3. **版本差异** — 本 Skill 基于 <REGULATION_ID> 版本生成。如有修订版颁布，应重新生成
4. **地方标准补充** — 本 Skill 仅包含国家标准。地方标准可能有更严格要求，需另行补充
5. **不替代专业判断** — 本 Skill 是规范查阅工具，不能替代注册建筑师/工程师的专业判断

---

## 文件清单

- [clause-index.md](clause-index.md) — 完整条文编号索引
- [clauses/](clauses/) — 按章节分组的条文原文
- [tables/](tables/) — 结构化数据表（Markdown + JSON）
- [cross-refs.md](cross-refs.md) — 跨规范引用关系图
- [mandatory-map.md](mandatory-map.md) — 法律效力矩阵
- [terminology.md](terminology.md) — 规范术语定义
```

---

## Step 9.5 — 安全扫描 + 强制力审计 · Security Scan + Mandatory Force Audit

### A. 安全扫描（使用内嵌工具）

用本 skill 自带的 `tools/scan_generated_skill.py`（无需外部安装），确认路径后执行：

```bash
python3 <本skill目录>/tools/scan_generated_skill.py <生成的规范skill目录>
```

### B. 强制力审计 · Mandatory Force Audit

逐项检查：
1. 每一条条文有且仅有一个强制等级标注。
2. 标注与原文一致（原文"应"→标注"应"，原文"不应"→标注"不应"等）。
3. 随机抽查 5 条条文，与 `full_text.txt` 原文逐字对比。
4. 所有条文引用的数据表在 `tables/` 目录中均存在。

如发现问题，先修正。严重问题（强制等级标注错误）→ 停止并请用户审查。

---

## Step 10 — 清理和报告 · Cleanup and Report

清理提取临时文件（通过 `exec` 或文件工具删除 `<tempdir>/book_skill_work/`）：

```bash
rm -rf /tmp/book_skill_work
```

输出报告：

```
✅ 规范 Skill 已创建: $SKILLS_HOME/<REGULATION_SLUG>/

📋 规范编号: <REGULATION_ID>
📄 页数: ~<N> | 条文: <N> 条 | 数据表: <N> 个

已生成文件:
  SKILL.md              — 主索引 + 强制性等级分布
  clause-index.md       — 完整条文编号索引
  clauses/              — <N> 个条文文件（原文保留）
  tables/               — <N> 个数据表（.md + .json）
  cross-refs.md         — 交叉引用关系图
  mandatory-map.md      — 法律效力矩阵
  terminology.md        — 规范术语定义
  ──────────────────────────────────────────
  总 Token 量: ~<N> tokens（条文按需加载）

使用方法:
  问 "<REGULATION_SLUG>"                  → 加载规范总纲
  问 "<REGULATION_SLUG> 防火间距"          → 查找并展示相关条文
  问 "<REGULATION_SLUG> 5.5.21"           → 加载指定条文 + 关联数据表
  问 "<REGULATION_SLUG> 有什么数据表？"     → 浏览所有数据表
```

---

## 更新/补充工作流 · Update / Supplement Workflow

当需要对已有规范 Skill 做补充时：

### 1. 读取已有 Skill
先读取 SKILL.md 和 cross-refs.md，了解现状。

### 2. 识别补充类型
- **地方标准补充**：创建 `supplements/<地方标准编号>.md`，列出差异条文
- **新版本规范**：建议重新做全量转换。在 `version-history.md` 中记录版本变化
- **条文说明/实施指南**：追加到对应条文的「条文说明」部分

### 3. 合并而不覆盖
- 地方标准：将差异以引用方式添加到相关条文
- 新版本：标记版本差异
- 重新运行 Step 9.5 审计

---

## 质量准则 · Quality Rules

1. **绝不改写强制性条文** — "应"就是"应"
2. **每个编号条文都是可检索目标** — 只要 "3.2.1" 存在，就一定能被找到
3. **表格是数据，不是文字** — JSON 用于程序查询，Markdown 用于阅读
4. **强制等级必须明确** — 每条条文有且仅有一个标注
5. **交叉引用必须完整** — 只要规范里出现了 "GB 50084"，就进入 cross-refs
6. **条文说明必须标注为非强制** — 始终标注 "不具有法律强制力"
7. **主 SKILL.md 应前载索引** — 条文索引和使用指南在前
8. **条文文件按需加载** — 不预先加载全部条文到上下文
9. **版本信息明确** — 每个生成的 Skill 都记录规范版本
10. **不替代专业判断** — 每个 SKILL.md 中必须明确声明

---

## 自包含说明 · Self-contained Engine

本 skill 内置了 PDF 提取引擎（不再依赖外部 `book-to-skill` 安装）：

| 资源 | 路径 | 说明 |
|------|------|------|
| 文本提取入口 | `scripts/extract.py` | 自包含入口，调用 `book_to_skill/` 包 |
| Python 引擎 | `book_to_skill/` | 内置的提取引擎（vendor 自 book-to-skill）|
| 安全扫描工具 | `tools/scan_generated_skill.py` | 自带的生成检查工具 |

如需提取更高质量（含表格布局），可在服务器安装 `poppler-utils`（pdftotext）：
`sudo apt install poppler-utils`。缺省时自动回退到 pypdf / pdfminer，功能仍可用。

## 参考文件 / References

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 本技能主说明（frontmatter + 全流程 Step 0–10 指令） |
| `scripts/extract.py` | 自包含 PDF 文本提取入口 |
| `book_to_skill/` | 内置提取引擎（parsers / cli / config / sanitize / dependencies / utils） |
| `tools/scan_generated_skill.py` | 生成技能的安全扫描 + 强制力审计工具 |
| `skill-card.md` | 技能卡片（发布元数据 / 风险评估 / 输出规范） |
| `_meta.json` | 发布元数据（owner / slug / version） |
| `references/` | 参考与设计说明集 |
| `CHANGELOG.md` | 版本与变更记录 |
| `README.md` | 快速上手与使用说明 |

详见 [references/REFERENCES.md](references/REFERENCES.md)。
