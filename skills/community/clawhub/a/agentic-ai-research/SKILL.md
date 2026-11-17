---
name: agentic-ai-research
version: 1.1.1
display_name: Agentic研究综述
display_name_en: Agentic AI Research
description: "检索顶会顶刊的 Agentic AI 最新研究成果，产出一份给人看的文献综述。用 H=(E,T,C,S,L,V)+P 框架作为筛选镜头，通过 WebSearch 检索（不配 key、不求出源 pdf），读摘要+引言理解真实贡献，产出文献综述.md，可选经确认后接入内置 wiki-creator 组件完成 wiki 化。触发场景：用户提出「检索顶会论文」「agentic ai 研究综述」「@agentic-ai-research」或想了解某个 agent 子领域的最新顶会顶刊成果。"
description_en: "Search the latest Agentic AI research from top conferences and journals to produce a human-readable literature review. Uses the H=(E,T,C,S,L,V)+P framework as a filtering lens, searches via WebSearch (no API keys, no source PDF downloads), reads abstracts + introductions to understand real contributions, and outputs a literature review .md, optionally compiling it into the built-in wiki-creator component after user confirmation. Trigger when the user asks about top conference papers, agentic ai research review, @agentic-ai-research, or wants to understand the latest top-tier research in a specific agent subfield."
license: MIT
metadata:
  permissions:
    file_read: true
    file_write: true
    network: true
---

# Agentic AI 顶会顶刊研究检索

> 用 H=(E,T,C,S,L,V)+P 框架作**筛选镜头**，检索顶会顶刊的 Agentic AI 最新成果，产出一份**给人看的文献综述.md**，可选经确认后 wiki 化。

---

## 定位与铁律

1. **镜头不是牢笼**：H 六层只是"筛选和归类"的镜头，**不是输出结构**。最终产出的是"给人看的文献综述"，不是"六层映射表"。
2. **案例先行**：读论文要理解它的**真实贡献**（提出了什么、解决了什么），不是靠标题/摘要贴六层标签。
3. **给人看**：产出物面向用户（人），要写得清楚、有可读性，不堆术语。
4. **禁止偷懒检索**：检索不充分就写综述 = 偷懒。必须通过下方"检索充分性门槛"才能动笔写综述。

---

## 范围模式（先判定，门槛随之变化）

动笔前先判定本次属于哪种范围模式；用户没明说时默认 A，并一句话向用户确认。

- **模式 A · 全领域六层综述**：用户要"某 agent 方向的整体研究综述"。此时六层是**覆盖清单**。
- **模式 B · 单子领域综述**：用户只聚焦一个子领域（如"上下文压缩""多智能体协作"）。此时六层只作**归类镜头**，不是必须逐层填满的配额——这正是铁律 1"镜头不是牢笼"的落地。

## 检索充分性门槛（防偷懒，按模式判定）

| 门槛 | 模式 A（全领域） | 模式 B（单子领域） |
|---|---|---|
| 数量 | 六层每层 ≥ 2 篇；总数 ≥ 12 篇；留口（顶级机构架构框架）≥ 1 篇 | 聚焦层 ≥ 6 篇，相关层各 ≥ 2 篇；无关层可为空 |
| 覆盖自检 | 逐层过 checklist：E/T/C/S/L/V 都覆盖了吗？缺哪层补哪层 | 只检聚焦层 + 相关层的覆盖度，不强制全六层 |
| 空缺处理 | 某层确实缺 → 标"该层近期无显著成果"，不得硬凑 | 未涉及的层一句话说明"本次聚焦 X，未展开 Y/Z"，不算空缺 |
| 检索日志 | 综述末尾披露：搜了几轮、用了哪些关键词、每层覆盖几篇，并注明哪几层在第几轮饱和 | 同左 |

> 通用红线（两模式都适用）：找不到的层**如实标注**，不得用其它层硬凑、不得假装覆盖。判定"是否偷懒"只看**尚未饱和的层有没有认真搜**，不看绝对篇数是否凑满六层。

---

## 多轮检索机制（三轮递进）

检索走三轮，不许跳过、不许一轮带过。**以"饱和"为正当结束信号，以"轮数下限"为防敷衍兜底**——二者优先级见文末，避免"既让停又逼满"的矛盾。

**第一轮 · 泛搜摸底（≥2 轮）**
- 搜主题本身 + "survey / review / awesome list"，摸清该方向今年的代表性工作和已有综述。

**第二轮 · 逐层精搜（每层 ≥2 关键词，中英结合）**
- 模式 A：按 E→T→C→S→L→V 顺序，每层用 2 个不同关键词各搜一次（中文词 + 英文词）。
- 模式 B：只精搜聚焦层 + 相关层，每层 2 个关键词；无关层不搜。
- 例：C 层 → "context compression" + "上下文压缩 记忆"。

**第三轮 · 查漏补缺（≥2 轮）**
- 对照覆盖清单，缺哪层补哪层；对偏薄的层搜"层名 + 2025/2026"补足。

**饱和信号（正当结束）**：某层连续 2 轮搜索无新增成果 → 该层**饱和，停止该层检索**。这是正常收敛，不算偷懒。

**轮数下限（防敷衍兜底，只约束"尚未饱和"的层）**：
- 模式 A 总轮数 ≥ 16（泛搜 2 + 精搜 12 + 查漏 2）；模式 B ≥ 8（泛搜 2 + 聚焦精搜 4 + 查漏 2）。
- 下限用于防止"每层只搜一次就草草收工"，**不是逼你对已饱和的层重复空搜**。
- **冲突时以饱和为准**：若因各层提前饱和而未跑满下限，只要在检索日志里注明"哪几层在第几轮饱和"，即视为达标，免除剩余轮数。

---

## 检索方式（硬约束）

- **只用 WebSearch**：不接 arXiv/Semantic Scholar API，不配 key，不求出源 pdf。
- **读论文程度**：读摘要 + 引言（理解真实贡献）；不够时补方法部分。其余细节用户自行阅读。

---

## 筛选镜头（H 六层 + P + 留口）

六层用于判断"这篇论文落在哪个维度"：E 执行循环、T 工具注册、C 上下文管理、S 状态存储、L 生命周期钩子、V 评估接口；P 是架构范式。

**留口（重要）**：如果是**顶会最新的 agent 架构设计框架**（完整设计了一个 harness/agent 运行时），即使不完全映射到六层，也保留——但条件严格：**必须是顶级机构、大厂的论文**。

---

## 工作流

1. **澄清主题 + 判定范围模式**：问清子领域（如"上下文压缩""多智能体协作""agent 架构"）、目标会议/期刊范围、时间范围（默认近 1–2 年），并据此判定是**模式 A（全领域六层）还是模式 B（单子领域）**。用户没说明时给默认假设（含默认模式），一句话简短确认即可，不要反复追问。
2. **分层检索**：按当前模式把主题翻译成检索关键词（如 C 层 → context compression / memory distillation；模式 B 只译聚焦层 + 相关层），用 WebSearch **多轮检索**，直到满足对应模式的"检索充分性门槛"。
3. **筛选**：用六层镜头 + 留口规则筛选，淘汰映射不清且非顶级机构的。
4. **读摘要+引言**：理解每篇的真实贡献，记录"谁做的、提出了什么、解决了什么"。
5. **覆盖自检**：按模式过 checklist——模式 A 逐层确认无空缺；模式 B 只确认聚焦层 + 相关层达标，无关层一句话说明即可。达标才进入下一步。
6. **写文献综述.md**：见下方模板，实际输出给用户。
7. **wiki 化（可选）**：经用户确认后，用内置 wiki-creator 组件把文献综述.md 编译进本地知识库。必须走「wiki 化」专节的确认门，未确认不写入。

---

## 文献综述.md 模板（给人看）

```markdown
# <主题> Agentic AI 顶会顶刊研究综述

> 检索范围：<会议/期刊> · <时间范围> · 数据来源：WebSearch

## 一、综述概览
<一段话：这个方向这一年最重要的进展是什么，趋势如何>

## 二、按维度分类的研究成果
### E 执行循环
- **<论文/成果名>**（<机构>，<会议/年份>）
  <一句话：提出了什么、解决了什么>
  <1-2 句：核心机制，白话讲清>

### T 工具注册
...

### C 上下文管理
...

### S 状态存储
...

### L 生命周期钩子
...

### V 评估接口
...

### 架构设计框架（留口）
- <顶级机构/大厂的完整 agent 架构框架成果>

## 三、趋势与小结
<几条可迁移的启示，给用户参考>
```

> **模板按模式裁剪**：模式 A 逐层填 E/T/C/S/L/V + 留口；**模式 B 只填聚焦层与相关层**，其余层并为一句"本次聚焦 X，未展开 Y/Z"，不硬撑出空的六层小节。

---

## wiki 化（可选 · 写入前必须确认）

> 本步骤**完全可选**。默认可只交付《文献综述.md》，不碰 wiki。任何 wiki 写入动作都必须先过下方「确认门」。

接收主体已从旧版外部组件 `llm-wiki` 替换为**内置本地组件**（随本技能打包的 `scripts/`，无网络、无第三方服务）。实现边界详见 `README.md`。

### 确认门（硬约束，不可跳过）

执行任何 wiki 写入**之前**，必须先向用户一次性展示以下四项，并取得用户明确同意（如「确认」「继续」）。未确认，禁止写入：

1. **写入路径**：`<wiki-root>/raw/` 与 `<wiki-root>/wiki/` 的**绝对路径**。
2. **接收主体**：内置本地组件（`scripts/`，实现边界见 `README.md`）。
3. **内容范围**：仅把《文献综述.md》复制到 `raw/`，并据此生成 wiki 页面。
4. **动作清单**：将新建/修改哪些目录与文件（逐条列出）。

### 路径收敛（硬约束）

- 根目录**只走项目内**，固定为 `<project>/.wiki-creator`，用 `--root` 显式指定；**禁止**写入全局 `~/.wiki-creator/`。
- **禁止**写入 `~/.workbuddy/wiki-knowledge/` 或任何 home 下的路径。
- 项目根判定：从当前工作目录向上查找 `.git` / `.vscode` / `package.json` 等项目标记，命中即 `<project-root>/.wiki-creator`；找不到时以当前工作目录为项目根。

### 执行步骤（确认后）

1. `python scripts/init_wiki.py --root <project>/.wiki-creator`（首次；已存在则跳过）。
2. 把《文献综述.md》**复制**到 `<wiki-root>/raw/`（复制，不移动；重名时改名或询问，不静默覆盖）。
3. `python scripts/parse_raw.py <wiki-root>/raw/文献综述.md` 解析出干净 markdown。
4. 按 H 六层归纳主题，写入 `<wiki-root>/wiki/SCHEMA.md`（写法见 `references/schema-guide.md`），**交用户确认**。
5. 按 `references/page-authoring.md` 提炼实体建页（每篇论文一页，标 `topic` + `sources` + `§来源`）。
6. `python scripts/build_index.py --root <wiki-root>` 生成索引。
7. 输出编译报告：建了哪些主题、哪些页、悬空链接。

### 增量更新（知识库已存在、只新增 / 修改 raw 资料时，可选）

此时**不要整库重写**：

1. `python scripts/diff.py --root <wiki-root>` 比对哈希，得到 new / changed / 受影响页清单。
2. 按 `references/cascade-update.md` 的受控三步（定位 → 分类 merge/ref-only/conflict → 单次限流 20 页）增量更新；矛盾写 `.conflicts.md`，不静默覆盖。
3. 重新跑 `build_index.py` 刷新索引、反链、graph、manifest。

> 组件规范（SCHEMA 写法见 `references/schema-guide.md`、建页见 `references/page-authoring.md`、增量见 `references/cascade-update.md`；单页 < 1500 字、kebab-case slug、无来源断言由 lint 标红、矛盾不静默覆盖）。

---

## 输出规范

1. 文献综述.md 是**最终交付物**，实际写出来给用户看。
2. 每篇论文写"机构 + 会议/年份 + 一句话贡献 + 1-2 句白话机制"，可读性优先，不堆术语。
3. 检索范围、筛选决策（哪些入选、哪些淘汰）在综述开头**披露**。
4. 可选：经用户确认后，用内置 wiki-creator 组件完成 wiki 化（见「wiki 化」专节）。
