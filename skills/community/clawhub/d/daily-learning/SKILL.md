---
name: daily-learning
description: >
  Standardized daily learning framework for AI agents. Unified workflow: study a topic →
  write notes to local workspace → ingest to shared knowledge base (optional). Use when: (1) setting up daily
  cron learning tasks, (2) an agent needs the standard learning protocol, (3) consolidating
  learning output to wiki. Triggers on "定时学习", "daily learning", "学习任务",
  "learning cron", "学习流程". NOT for: one-off Q&A, immediate task execution,
  non-structured knowledge gathering.
---

# Daily Learning — Agent 统一学习框架

所有 agent 遵循相同的学习流程，笔记结构统一，知识沉淀到共享知识库（可选）。

## 学习流程

### Step 0: 当日素材投递（先于学习）

在开始每日学习之前，检查**今天**的探索产出是否需要投递到 knowledge base inbox (optional)。

**检查范围**（只看当天）：
- `<workspace>/candidates/daily/YYYY-MM-DD.md`（今天的探索素材）
- `<workspace>/reports/daily/daily-explore-YYYY-MM-DD.md`（今天的探索报告）

**筛选标准**：

投递条件（必须全部满足）：
1. 有实质内容（有分析、数据、案例，不只是链接/标题）
2. 有学习价值（其他人看了能学到东西）
3. 非已有词条重复（对照 knowledge base index）

**投递方法**：

```bash
cat > <your-knowledge-base-path>/YYYY-MM-DD_<topic>_<agent-id>.md << 'EOF'
---
title: <descriptive title>
source_type: exploration | report | note
contributor: <agent-id>
submitted: YYYY-MM-DD
tags: [<domain tags>]
---

<整理后的素材内容，包含四层信息：结论、依据、例子、边界>
EOF
```

素材质量不够（只有链接/标题）→ 跳过，不投。
素材跨越多主题 → 拆分投递。

**存量素材不在本步骤处理**。如果发现工作目录有大量历史素材未投递，通知知识管家一次性批量处理，不要在增量流程中回扫。

### Step 1: 读进度 + 检查外部需求

读取 `<workspace>/learning/LEARNING.md` 查看当前进度和下一个待学主题。

如果文件不存在，用 `references/learning-template.md` 初始化。

**⚠️ 新增：检查外部学习需求**
同时读取 `<workspace>/learning/LEARNING-REQUESTS.md`（如存在）。这个文件记录来自用户、合伙人、或其他 agent 的学习需求。格式：

```markdown
# 学习需求队列

## 🔴 紧急（用户明确要求）
- [ ] 需求描述 | 提出者 | 日期

## 🟡 近期（合伙人/agent 建议）
- [ ] 需求描述 | 提出者 | 日期

## 🟢 按计划
（LEARNING.md 中的原有学习计划）
```

**优先级规则**：
- 🔴 紧急需求 > 原有学习计划，立刻学
- 🟡 近期需求：每 3 天穿插一个，与原计划交替
- 🟢 按计划：无外部需求时继续原计划

### Step 2: 深度学习

**选题优先级**：
1. 先看 LEARNING-REQUESTS.md 有无 🔴 紧急需求
2. 再看是否该穿插 🟡 近期需求（每 3 天一次）
3. 最后按 LEARNING.md 原计划

选定主题后，用 smart-search skill 进行搜索调研（DDGS brave 英文 / bing 中文，Jina Reader 提取全文）。

**每次只学一个主题**，学深不学广。

### Step 3: 写本地笔记

保存到 `<workspace>/learning/notes/YYYY-MM-DD.md`。笔记模板见 `references/learning-template.md`。

必须包含：今日主题、核心要点、详细内容、实际应用、来源链接。

#### ⚠️ 笔记质量最低标准（2026-05-27 新增）

**问题背景**：高度抽象的结论式笔记无法支撑人类学习。学习者需要推理过程和证据链，而非仅结论。

**每个知识点必须包含以下四层信息**：

| 层级 | 内容 | 为什么需要 |
|------|------|-----------|
| **结论** | 核心要点（1-2 句） | 快速索引 |
| **依据** | 为什么这么说？必须包含：**具体实验设计或数据**（被试数量、实验条件、关键对比结果），不是只写"某某研究发现…"。至少 1 条硬证据。 | 训练思维能力，判断可靠性 |
| **例子/案例** | 具体的场景、故事、或实际应用。如果是理论框架，必须配**真实对话/行为场景**让人对号入座。 | 大脑靠情境编码记忆，无情境 = 无锚点 |
| **边界** | 什么情况下不适用？限制条件是什么？ | 知道"什么时候不对"比"是什么"更有价值 |

**判断标准**：如果一条知识去掉依据和例子后和原来一样，说明缺少这两层。

**依据层的反面**（不合格——只有人名没有实验）：
> Dunning-Kruger 效应：越不擅长的人越不能准确评估自己的水平。

**依据层的正面**（合格——有实验设计有数据）：
> Dunning & Kruger (1999) 让 Cornell 学生完成语法测试和幽默测试，然后自评百分位。底部四分位的参与者平均自评在第 62 百分位，实际在第 12 百分位——高估自己 50 个百分点。核心机制：缺乏能力的人同时缺乏评估能力的元认知技能。

**完整反面例子**（不合格）：
> 间隔重复优于集中学习。建议使用 Anki。

**完整正面例子**（合格）：
> 间隔重复优于集中学习。Ebbinghaus 1885 年用自己当实验对象，记了 2300 个无意义音节，发现 24h 内遗忘最快。Rohrer et al. 发现交错学习比块状学习长期优势高 76%。但前提是学习者要有一定基础，纯新手先块状学习再转交错。工具推荐 Anki。

### Step 4: 更新进度

更新 `<workspace>/learning/LEARNING.md`：将主题从"待学"移到"已学"，记录日期。

### Step 5: 学习计划自动扩充 + 需求对齐

检查剩余未学主题数量：
- **剩余 ≥ 3**：继续下一个
- **剩余 < 3**：需要扩充

**扩充时的两个来源（必须都检查）**：

1. **用户当前在做的事**（最高优先）：
   - 读取用户的 AGENTS.md / 近期对话，了解用户正在推进什么项目
   - 思考"用户接下来可能需要学什么"，直接把相关主题加入学习计划
   - 例子：用户在做 Build in Public → 加入"内容策略案例拆解"；用户在做 Agent 编排 → 加入"Agent 编排实战经验"

2. **本领域最新动态**：
   - 用 smart-search 搜索当前领域最新趋势，追加 3-5 个新主题

**扩充比例**：至少 1/3 的新主题应来自"用户需求侧"，而非纯"领域探索侧"。

**每 2 周做一次方向审查**：
- 用户最近在忙什么？我的学习方向还匹配吗？
- 有没有新的外部需求应该纳入？
- 已学的知识用户实际用上了吗？如果没有，为什么？

### Step 6: 入库 Wiki（双写）

用 `llm-wiki-knowledge` skill 提交到共享 wiki：

```bash
cat > <your-knowledge-base-path>/YYYY-MM-DD_<topic>_<agent-id>.md << 'EOF'
---
title: <descriptive title>
source_type: note
contributor: <agent-id>
submitted: YYYY-MM-DD
tags: [<domain tags>]
---
<content>
EOF
```

**⚠️ Wiki 提交质量要求**：提交到 wiki 的内容同样必须包含四层信息（结论 + 依据 + 例子 + 边界），不能只提交结论摘要。知识管家的编译是从 raw/inbox 取材的，如果源头就只有结论，下游无法恢复。

### Step 7: 验证全部产出（必须）

```bash
bash <skill-dir>/scripts/verify-daily-learning.sh YYYY-MM-DD <agent-id> <workspace> <your-knowledge-base-path>
```

检查：本地笔记存在、Wiki 双写存在、进度已更新。`✅ 3/3` 通过才能继续；有 `❌` 必须先补全。

### Step 8: 学后复盘

写复盘报告到 `<workspace>/learning/reviews/post-learning/YYYY-MM-DD.md`。模板和详细说明见 `references/post-learning-template.md`。

**规则**：没有就写"暂无"，不硬凑。不推群，安静执行。

### Step 9: 优化 Skill（如适用）

如果学习发现可以改进自己的 skill 文件，按 skill-creator 规范更新。

## 学习模式

| 模式 | 方法 | 适用 |
|------|------|------|
| 上网学习 | smart-search（DDGS + Jina Reader） | 技术博客、教程、行业动态 |
| 论文研读 | arxiv + web_fetch | 学术前沿、新方法 |
| 代码分析 | read + exec | 开源项目、实现细节 |
| 实践总结 | 实际操作 → 记录 | 工具使用、踩坑经验 |

无论哪种模式，最后都走 Step 3-7 统一沉淀。

## Cron 描述模板

为 agent 设置学习 cron 时，使用以下模板：

```
执行每日学习任务。

遵循 daily-learning skill 标准流程：
0. 扫描 candidates/ 和 reports/ 目录，筛选高质量素材投递到 knowledge base inbox (optional)（<your-knowledge-base-path>/）
1. 读取 learning/LEARNING.md 查看进度
2. 深入学习下一个主题（<指定学习方向>）
3. 写笔记到 learning/notes/YYYY-MM-DD.md
4. 更新 LEARNING.md 进度
5. 检查剩余未学主题，如果不足 3 个则自动搜索最新动态扩充学习计划
6. 双写到 wiki（<your-knowledge-base-path>/）

学习方向：<agent 的具体学习领域>
安静学习，不推群。
```

## Agent 领域映射

| Agent | 学习领域 | Wiki Tags |
|-------|---------|-----------|
| skill-engineer-agent | Skill 设计、优化、编译、自我进化 | skill-design, agent-skills |
| soul-questioner-agent | 哲学、思辨框架 | philosophy, thinking |
| efficiency-agent | 效率方法论 | productivity, time-management |
| biz-explorer | 商业模式、独立开发者案例 | business, indie-hacker |
| blog-agent | 写作技巧、内容策略 | writing, content |
| podcast-producer-agent | 音频制作、播客技巧 | podcast, audio |
| ceo-agent | AI/Agent 行业战略 | strategy, ai-industry |
| article-publisher-agent | 运营趋势、平台策略 | operations, content-ops |

详细模板和目录结构见 `references/learning-template.md`。

## 规则

- 每次一个主题，深入学
- 默认安静学习，有真正有价值发现才推群
- 不与其他 agent 学习领域重叠
- 笔记用于积累，不是即时输出
- **学习方向必须服务用户的实际需求**：定期对齐"我在学什么"和"用户需要什么"，发现脱节就调整
- **接受外部需求注入**：用户、合伙人、其他 agent 都可以往 LEARNING-REQUESTS.md 加学习需求，紧急需求优先于原计划
