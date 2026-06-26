---
name: dream-selfimproving
description: "让AI拥有进化能力——每晚自动复盘当天对话，提取洞察，更新记忆，并自动学习新技能、淘汰低频技能。越用越聪明，真正实现"用进废退"的自主进化。"
metadata:
  openclaw:
    requires:
      bins:
        - python
      env:
        SWARMRECALL_API_KEY:
          description: "可选。云端去重/矛盾检测密钥。不设置则仅本地运行。"
          required: false
    notes: |
      运行时通过 `openclaw env get` / `openclaw cron list` 动态获取，无需预先声明环境变量。

      Cron编辑：update-cron-date.py 通过 'openclaw cron edit' 修改 dream cron 作业消息。
      ⚠️ 特权操作，需使用 --confirm 标志：python update-cron-date.py --confirm
      详情见下方 ## 安全说明 章节。
  meta:
    name: "dream-AI进化的梦之核"
    tagline: "让AI每晚进化一次，越用越聪明，用进废退自主进化"
    category: memory
    tags: [AI, memory, distillation, RAG, self-improving, 夜间蒸馏, 知识图谱, 用进废退, 技能进化, 全自动技能开发]
---

# Dream Self-improving — 夜间记忆蒸馏与自我进化

> 🧠 **v5.1 技能进化插件** — AI自主学习、用进废退、全自动技能开发 + 完整每日汇报

## 现状

**Phase 3（✅ 已实现）：** OpenClaw Hook `hippocampus` 监听每条消息，实时写入 `memory/logs/`
**Phase 3（✅ 已实现）：** `dream.py v4.x` 定时蒸馏 + M-FLOW Bundle Search检索
**Phase 3（✅ 已实现）：** `dream.py v4.x` Long-Term RAG 长记忆层

**Phase 4（✅ 已实现）：** `dream.py v5.0` 技能用进废退 + 全自动技能开发 + 完整每日汇报

---

## v5.1 技能进化插件（v2.0 大幅增强）

### GapDetector v2.0 — 新增 SKILL.md 草稿自动生成

`extensions/skill_explorer/gap_detector.py` v2.0 整合 skill-evolver 核心逻辑：

| 新增方法 | 功能 |
|---------|------|
| `get_active_capabilities()` | 从 `~/.skill_scoreboard/scores.json` 推断用户能力需求 |
| `scan_shared_skills()` | 扫描 `~/SharedSkills/` 所有技能清单 |
| `detect_gaps_from_scores()` | 基于评分数据检测能力缺口（比原有任务分析更精准） |
| `generate_skill_draft()` | 为缺口生成**完整 SKILL.md 草稿**（含触发词、使用场景、步骤、工具） |
| `detect_and_generate()` | 一次性执行缺口检测 + 草稿生成 + 过时技能扫描 |

**SKILL.md 草稿模板库**（已实现）：

| 能力 | 生成的技能名 | 触发词示例 |
|------|------------|-----------|
| 搜索/研究 | `deep-researcher` | 帮我调研、搜索论文 |
| 图片生成 | `image-generator` | AI画图、生成插画 |
| 网页抓取 | `web-scraper` | 爬取数据、提取网页内容 |
| Shell命令 | `shell-automation` | 写脚本、批处理 |
| Git操作 | `git-assistant` | commit、PR、解决冲突 |
| 飞书集成 | `feishu-integration` | 飞书文档、飞书消息 |
| 视频生成 | `video-generator` | 生成视频、AI视频 |
| 文档总结 | `doc-summarizer` | 总结文档、长文章摘要 |
| 数据分析 | `data-analyst` | 分析数据、生成图表 |
| PPT制作 | `ppt-generator` | 制作PPT、演示文稿 |
| 翻译 | `translator` | 中英互译、润色英文 |
| 通用 | `{能力英文名}` | 能力名本身 |

**E6/E8 流程更新（dream.py v5.1）**：
1. `GapDetector.detect_and_generate()` → 同时获取缺口列表 + SKILL.md 草稿
2. 对每个高优先级缺口 → `generate_skill_draft()` 生成完整草稿
3. 草稿直接写入 `~/SharedSkills/{skill_name}/SKILL.md`
4. 同时创建占位脚本 `scripts/main.py`
5. 草稿内容同步保存到每日汇报的 `skill_development.drafts` 字段

**与 skill-evolver 共用数据源**：`~/.skill_scoreboard/scores.json`

---

## v5.0 技能进化插件（原有架构）

### 五大扩展模块

| 模块 | 功能 | 关键类 |
|------|------|--------|
| **skill_evolution** | 技能评分（调用×质量×衰减）+ 用进废退引擎 + 技能注册表 | `SkillScorer`, `DecayEngine`, `SkillRegistry` |
| **work_review** | 工作复盘分析 + 明日计划生成 | `WorkAnalyzer`, `TomorrowPlanner` |
| **skill_explorer** | 技能缺口检测 + 自主学习 | `GapDetector`, `SkillLearner` |
| **skill_developer** | 全自动技能生成（AI生成+质量评估+注册） | `SkillGenerator`, `SkillQualityAssessor` |
| **reporter** | 每日完整汇报（六大模块） | `DailyReporter`, `SkillReportGenerator` |

### 用进废退评分体系

技能活跃度 = 调用次数 × 质量系数 × 时间衰减

| 等级 | 标识 | 分值范围 | 说明 |
|------|------|----------|------|
| 高度活跃 | 🔥 | ≥80 | 调用频繁，持续进化 |
| 正常 | 📈 | 60-79 | 稳定使用 |
| 低活跃 | 💤 | 40-59 | 使用较少，建议复习 |
| 休眠 | 🗄️ | 20-39 | 长期未用，待激活 |
| 已归档 | ⚰️ | <20 | 彻底停用 |

**衰减规则：**
- 30天未用：×50%
- 90天未用：×20%
- 180天未用：自动归档

### 每日汇报（六大模块）

与早7点+晚10点蒸馏同步执行，完整汇报保存为 `daily-report-YYYY-MM-DD.md`：

1. **📝 今日总结** — 工作完成情况、未完成原因、阻碍因素
2. **📋 明日计划** — 继续任务 + 新任务 + 技能开发计划
3. **🛠️ 技能开发** — 新技能生成（AI全自动）、技能改进
4. **📈 技能评分** — Top 10 活跃度排行 + 用进废退变化
5. **🎯 精进点** — 学到的新东西、改进方向
6. **💭 个人感想** — AI 自我反思

### 扩展模块目录结构

```
extensions/
├── __init__.py
├── skill_evolution/     # 用进废退核心
│   ├── scorer.py        # 技能评分器
│   ├── decay.py         # 衰减引擎
│   └── registry.py      # 技能注册表
├── work_review/         # 工作复盘
│   ├── analyzer.py      # 工作分析器
│   └── planner.py       # 明日计划生成器
├── skill_explorer/      # 技能探索
│   ├── gap_detector.py  # 缺口检测器
│   └── learner.py       # 技能学习器
├── skill_developer/     # 技能开发
│   ├── templates.py     # 技能模板库
│   ├── generator.py     # 技能生成器
│   └── quality.py       # 质量评估器
└── reporter/            # 汇报生成
    ├── daily_report.py  # 每日汇报生成器
    └── skill_report.py  # 技能专项报告
```

---

## 核心升级：Long-Term RAG

参考 MetaGPT 的 RoleZeroLongTermMemory 设计，新增短长记忆合并机制：

```
short-term-recall.json  ←  活跃recall条目（上限200条）
memory/.rag/longterm.jsonl  ←  老旧条目RAG存储
```

**晋升条件：**
- 条目 age > 30天（从最后召回时间算）
- 且 recallCount < 3（未被频繁召回）

**召回流程：**
1. 蒸馏前，从当日高权重条目提取关键词
2. 用关键词查询 RAG，召回相关旧记忆
3. 旧记忆注入蒸馏上下文，让 AI 知道"之前有过什么"

**效果：** 记忆越来越精准，不像以前每次都从零开始。

---

## 完整链路

```
用户对话
   ↓
OpenClaw Hook: message:preprocessed
   ↓
丘脑过滤（Thalamus）→ 杏仁核标记（Amygdala）→ 海马体存储（memory/logs/）
   ↓
cron 触发（早7点/晚10点）
dream.py v4.x
   ↓
[4.5] RAG查询 — 从当日条目提取关键词 → 查询memory/.rag/longterm.jsonl → 注入蒸馏上下文
   ↓
Bundle Search检索（替代简单grep）
   ↓
杏仁核标记融合 → Auditor审计 → 分析皮层模式识别 → 前额叶蒸馏规划
   ↓
[4.6] RAG晋升 — 30天+未召回条目 → 写入longterm.jsonl
   ↓
归档区 → 真相文件写回 → 梦境报告
```

---

## M-FLOW 核心架构

### 倒锥知识图谱（Inverted Cone）

所有记忆组织为**四层有向图**，形成倒锥结构：

```
          锥尖（容易精确命中）
             ↓
    ┌─────────────────────────┐
    │  L4 Entity             │  ← 用户/项目/系统等实体节点
    │  L3 FacetPoint         │  ← 具体属性、特征、标签
    │  L2 Facet               │  ← 一组相关特征
    │  L1 Episode（锥底）     │  ← 最终返回的知识单元
    └─────────────────────────┘
          锥底（返回给用户）
```

**搜索逻辑（Bundle Search）：**
1. **锥尖广撒网**：查询向量化后同时在4层搜索，每个集合返回最多100个候选
2. **投影到图中**：命中点作为入口，提取周围子图（边+邻居+连接关系）
3. **代价传播**：沿边从锥尖向锥底传播，Episode得分 = 所有路径中最小代价

**三条核心设计原则：**

| 原则 | 说明 | 对应效果 |
|------|------|---------|
| **边携带语义** | 每条边附带自然语言描述，参与检索 | 不是被动连接，是主动语义过滤器 |
| **路径最小代价** | 一条强证据链就足以证明相关性 | 不被无关路径稀释分数 |
| **惩罚直接命中Episode** | 直接匹配摘要反而加惩罚 | 偏好精准锚点路径，防止宽泛匹配 |

---

## 脑区协同架构

**① 丘脑（Thalamus）— 注意力门控**
> 过滤纯问候/简单确认，只记录有意义的事件
> 标记类型：event / decision / correction / completed / insight / error

**② 杏仁核（Amygdala）— 情绪标记**
> correction/error/decision/completed/insight 携带 HIGH 权重，优先蒸馏

**③ 海马体（Hippocampus）— M-FLOW图存储 + RAG**

Phase 1：`memory/logs/` 追加日志（Episode层）

Phase 2：构建M-FLOW图结构：

```
Episode (L1)              ← daily log / topic file
  ↓ semantic edge
Facet (L2)                ← grouping: correction_group, project_xxx
  ↓ semantic edge  
FacetPoint (L3)           ← specific tag: error.timeout, user.pref
  ↓ semantic edge
Entity (L4)               ← user, project, tool, skill
```

**FacetPoint** = type + topic + keywords 的向量描述（向量化后参与Bundle Search）
**语义边描述** = "这个FacetPoint为什么属于这个Episode" 的自然语言说明

**④ 前额叶（Prefrontal Cortex）— Bundle Search + RAG召回 + 蒸馏规划**

Bundle Search检索替代简单grep：
```
查询 → 向量化 → 4层锥形搜索 → 代价传播 → 最小路径Episode
```

RAG召回（v4.x新增）：
```
当日关键词 → 查询longterm.jsonl → 召回相关旧记忆 → 注入蒸馏上下文
```

**⑤ 蓝斑核（Locus Coeruleus）— 警觉与新鲜度信号**
> freshness分数——最近被提及的记忆权重更高

---

## Long-Term RAG Layer 详解

### 存储结构

```
memory/
├── .dreams/
│   └── short-term-recall.json   # 活跃recall条目（上限200条）
└── .rag/
    └── longterm.jsonl          # 老旧条目RAG存储（JSONL格式）
```

### 晋升机制

```python
# 晋升条件
if age_days > 30 and recall_count < 3:
    promote_to_longterm_rag(entry)
```

### 召回机制

```python
# 蒸馏前
keywords = [v['snippet'][:100] for v in tagged.values()][:20]
query = ' '.join(keywords[:5])
rag_results = query_longterm_rag(query, k=5)

# 召回结果注入蒸馏上下文
learnings['LEARNINGS.md'] += f"\n\n## Long-Term Memory (RAG)\n{rag_text}"
```

### 手动命令

```bash
# 查看短/长记忆状态
python skills/dream-selfimproving/scripts/longterm_rag.py --status

# 手动晋升老条目
python skills/dream-selfimproving/scripts/longterm_rag.py --promote

# 搜索长记忆
python skills/dream-selfimproving/scripts/longterm_rag.py --query "关键词"
```

---

## Pattern Library

Patterns are reusable response templates extracted from recurring learnings:

```
memory/patterns/
└── p-xxx.md           # Pattern files with trigger + response
```

**Pattern格式（含M-FLOW元数据）：**

```yaml
---
name: pattern名称
trigger: 什么情况下触发
response: 如何响应
examples: [案例1, 案例2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
# M-FLOW 元数据
entity: pattern          # L4 Entity
facets: [tag1, tag2]    # L3 FacetPoints
episode_id: p-xxx        # L1 Episode
---
```

---

## Memory Taxonomy & M-FLOW映射

| Memory Type | L4 Entity | L3 FacetPoints | L1 Episode |
|------------|-----------|-----------------|--------------|
| **user** | user.luyi | role, pref, goal, communication_style | topics/user_*.md |
| **feedback** | feedback | correction, error, insight, confirmation | topics/feedback_*.md |
| **project** | project.{name} | decision, tool, deadline, context | topics/project_*.md |
| **reference** | reference | credential, link, skill, system | topics/reference_*.md |
| **longterm** | (RAG) | aged, promoted | .rag/longterm.jsonl |

---

## Directory Structure (v4.x)

```
memory/
├── graph/                         # M-FLOW 知识图谱
│   ├── entities.json              # L4 Entity 节点列表
│   ├── facetpoints.json           # L3 FacetPoint 节点列表
│   ├── facets.json                # L2 Facet 节点列表
│   ├── episodes.json              # L1 Episode 节点列表
│   ├── edges.json                 # 语义边（含描述文本）
│   └── index.json                 # 图索引 + 向量锚点
├── logs/
│   └── YYYY/MM/YYYY-MM-DD.md     # Daily append-only logs (Episode)
├── topics/                        # Distilled topic memories
│   ├── user_xxx.md
│   ├── feedback_xxx.md
│   ├── project_xxx.md
│   └── reference_xxx.md
├── patterns/                      # Pattern Library
│   └── p-xxx.md
├── episodes/                      # Project narratives
├── .dreams/
│   └── short-term-recall.json     # 活跃recall条目（上限200条）
├── .rag/
│   └── longterm.jsonl             # Long-Term RAG（v4.x新增）
├── procedures.md                  # Workflow preferences
├── archive.md                     # Compressed old entries
├── dream-log.md                   # Dream cycle reports
└── MEMORY.md                      # INDEX only

.learnings/                        # self-improving-agent
├── LEARNINGS.md
├── ERRORS.md
└── FEATURE_REQUESTS.md
```

---

## Health Score (v4.x)

| Metric | Weight | Formula |
|--------|--------|---------|
| Freshness | 0.20 | entries_referenced_last_30_days / total |
| Coverage | 0.20 | categories_updated_last_14_days / 10 |
| Coherence | 0.20 | entries_with_semantic_edges / total |
| **Graph Connectivity** | 0.20 | connected_components_ratio |
| Efficiency | 0.10 | max(0, 1 - line_count/500) |
| Reachability | 0.10 | Bundle Search路径覆盖率 |

---

## Dream Distillation Steps (v5.0)

When cron triggers:

1. **Bundle Search预热**：用今日日志构建临时图结构，快速验证图连通性
2. Read `memory/logs/{date}.md`
3. Read `.learnings/LEARNINGS.md`, `.learnings/ERRORS.md`, `.learnings/FEATURE_REQUESTS.md`
4. Read `MEMORY.md`, topic files, `graph/index.json`, `procedures.md` for context
5. **Snapshot BEFORE**: count entries, decisions, lessons, procedures
6. **[4.x] 技能积分榜读取**：调用 `score_tracker.py today`，获取今日技能王 + 调用统计，注入蒸馏上下文
7. **[4.5] RAG召回**：从当日条目提取关键词 → 查询longterm.jsonl → 注入蒸馏上下文
8. **图增强检索**：对每个learnings entry执行Bundle Search，找到相关Episode
9. **Distillation Agent**: Run sub-agent on raw entries + learnings + RAG results → produce:
   - 3-5 genuine insights ("I learned that...")
   - 1-3 tomorrow action items
   - 0-3 topic files to write to `memory/topics/`
   - Health metric interpretation
   - 技能积分榜洞察（若有数据）
10. **[4.6] RAG晋升**：30天+未召回条目 → 写入longterm.jsonl
11. **更新图结构**：
    - 新Episode写入 `graph/episodes.json`
    - 新FacetPoint写入 `graph/facetpoints.json`
    - 新边写入 `graph/edges.json`（含语义描述）
12. Write topic files (from Distillation Agent output)
13. Update truth files (`user_state.md`, `pending.md`)
14. Update `graph/index.json` entry metadata + 重新计算向量锚点
15. Compute health metrics → update `graph/index.json` stats
16. Archive eligible entries → append to `archive.md`
17. Update `MEMORY.md` index (max 200 lines)
18. **Snapshot AFTER**: calculate deltas
19. Write dream report to `memory/dreams/{date}.md` and `dream-log.md`
20. **v5.0 技能扩展模块**：执行 skill_evolution + work_review + skill_explorer + skill_developer + reporter
21. **v5.0 每日汇报**：生成 `daily-report-{date}.md` 完整六大模块汇报
22. **[Optional SwarmRecall]**: 如果配置了API key，执行云端图同步

---

## Dream Report Format (v5.0)

```markdown
# 🌙 Dream Report — {date}

## 🧠 系统状态
- 原始日志条目 | recall store 总数 | Auditor AI味 | 蓝斑核健康

## 🫀 蓝斑核健康评分 (v4.0 M-FLOW)
- 新鲜度 | 连贯性 | 覆盖度 | 图连通性 | 效率 | 可达性

## 🧠 M-FLOW 知识图谱状态
- L4 Entity | L3 FacetPoint | L1 Episode | 语义边
- Bundle Search 结果

## 🏆 技能积分榜（v4.x 新增）
- 今日技能王 + 调用次数 + 积分
- 原始榜单摘要（若有数据；无数据时此节不显示）

## 💡 我学到了
- {genuine insight 1（含技能积分洞察）}
- {genuine insight 2}

## 🎯 明日重点
- {actionable item 1}
- {actionable item 2}

## 🔁 重复模式（≥3次）
## 🗄️ 归档候选
## Patterns Updated
```

---

## User Prompts

- "dream report" / "梦境报告" → read and display latest dream report
- "dream" / "做梦" → run distillation now
- "/dream status" → show M-FLOW graph stats, health score, pattern count
- "/dream search {query}" → run Bundle Search and show top results
- "/dream rag status" → show RAG status (from longterm_rag.py)

---

---

## 🔒 安全说明

### update-cron-date.py 的 --confirm 标志

此脚本用于修改 OpenClaw cron 作业，属于**特权操作**。

- `--confirm` 标志是安全机制，防止意外执行
- 无此标志时，脚本只显示将要做什么但不会实际修改
- 使用前请确保您了解 cron 作业的当前状态：
  ```bash
  openclaw cron list
  ```

### SWARMRECALL_API_KEY 环境变量

- **声明位置：** `metadata.openclaw.requires.env.SWARMRECALL_API_KEY`
- **用途：** 可选。云端去重/矛盾检测（需连接 SwarmRecall 服务）
- **默认值：** 不设置则仅本地运行，无云端功能
- **获取方式：** 向 SwarmRecall 服务注册获取

### 文件访问范围

此技能会访问和修改以下位置的文件：
- `~/.openclaw/workspace/memory/logs/` — 对话日志
- `~/.openclaw/workspace/memory/.dreams/` — 梦境报告
- `~/.openclaw/workspace/memory/.rag/` — 长记忆 RAG 存储
- `~/.openclaw/workspace/memory/.truth/` — 真相文件
- `~/.openclaw/workspace/memory/.learnings/` — 学习记录
- `~/.openclaw/hooks/hippocampus/` — Hook 配置
- OpenClaw cron 条目（通过 update-cron-date.py）

**诊断参考：** `references/diagnostic-checklist.md` — 快速健康检查命令清单

---

## Known Issues & Pitfalls

### 月份目录不存在导致日志静默丢失

**问题现象：**
- `memory/logs/YYYY/MM/` 月份目录不存在时，`append_to_log()` 会静默失败（不抛异常）
- `mkdir(parents=True, exist_ok=True)` 只创建最后一级目录；如果 `YYYY/` 存在但 `MM/` 不存在，且代码写的是 `mkdir("2026/05", parents=True)` → 不会创建 `2026/` 本身
- 实际路径行为：第 3 行 `log_dir = LOGS_DIR / year / month` 后直接 `ensure_dir(log_dir)`，如果 `2026/` 存在但 `05/` 不存在 → 正常创建；**但如果整个 `YYYY/` 不存在则失败**

**排查：**
```bash
ls -la ~/.openclaw/workspace/memory/logs/2026/
# 如果 05/ 目录不存在，说明本月还没有消息被记录
```

**手动修复：**
```bash
mkdir -p ~/.openclaw/workspace/memory/logs/2026/05
```

### Cron 定时任务可能不按时执行

**问题现象：**
- 梦境报告时间戳显示 `generated_at` 与日志日期不匹配
- 例如：4/30 的日志缺失，但 5/1 00:54 生成的快照实际记录的是 4/29 数据
- Cron list 为空但记忆里记录了 cron 任务（配置不在 Hermes 这边）

**排查步骤：**
1. 检查 `~/.skill_scoreboard/daily/` 文件时间戳是否连续
2. 检查 `~/.hermes/cron/output/` 是否有对应日志
3. 通过 `openclaw cron list` 确认实际 cron 配置（如果 openclaw CLI 可用）
4. 如果 cron list 为空但快照在跑 → 任务配置在 OpenClaw 平台端，不在本地

### 浏览器访问问题

**问题：** 在 WSL 环境中访问 `localhost:3012`（OpenClaw-Admin）可能失败，Chrome 报错 `libnspr4.so: cannot open shared object file`

**解决：** 不依赖浏览器，用 API 直接调 OpenClaw：
```bash
# 查看 cron 任务
openclaw cron list

# 查看环境变量
openclaw env get
```

### 404 错误溯源

**场景：** 飞书消息后出现 "Auxiliary title generation failed: HTTP 404"，用户不知道来源

**排查方向：**
1. 检查 Hermes cron output 日志 (`~/.hermes/cron/output/`)
2. 检查 skill-scoreboard 快照是否在那个时间点生成
3. 检查 OpenClaw Gateway 内部是否有辅助标题生成的定时任务
4. 如果 cron list 为空 → 任务在 OpenClaw 平台端而非本地

## Scripts

- `dream.py` — Phase 2 蒸馏脚本（v4.x，M-FLOW Bundle Search + RAG召回/晋升 + 技能积分榜融合）
- `update-cron-date.py` — 每日 cron 日期注入 ⚠️ 特权操作，需 --confirm
- `graph-builder.py` — 从日志构建M-FLOW图结构
- `bundle-search.py` — Bundle Search检索实现
- `longterm_rag.py` — Long-Term RAG 管理脚本（v4.x新增）

> dream.py 蒸馏前自动调用 `~/SharedSkills/skill-scoreboard/scripts/score_tracker.py today`，将今日技能王 + 积分注入蒸馏上下文和梦境报告，无需额外配置。

---

## Phase 1 启用（hippocampus hook）

**Hook 目录：** `~/.openclaw/hooks/hippocampus/`
**已配置：** `openclaw.json` 中 `hooks.internal.entries.hippocampus: enabled: true`

**功能：** 监听 `message:preprocessed` 事件，自动记录对话到 `memory/logs/YYYY/MM/YYYY-MM-DD.md`

**丘脑过滤规则：**
- 纯问候 / 简单确认（<20字）不记录
- 高权重标记：correction / error / decision / completed / insight

重启 gateway 后生效：
```bash
schtasks /run /tn "OpenClaw Gateway"
```

---

## M-FLOW vs 旧架构对比

| 维度 | 旧架构（平坦检索） | M-FLOW（倒锥图路由） |
|------|-------------------|----------------------|
| **存储结构** | 平面文件列表 | 四层有向图 |
| **检索方式** | grep / 向量相似度 | Bundle Search代价传播 |
| **关系表示** | 简单link引用 | 带语义描述的边 |
| **短长记忆** | 无分层 | 30天老化晋升RAG |

---

### OpenClaw ↔ Hermes 记忆同步
- 脚本位置：`~/.hermes/scripts/sync_openclaw_memory.py`
- 功能：双向桥接 OpenClaw sqlite 记忆库与 Hermes 扁平记忆文件
- 使用：`python3 ~/.hermes/scripts/sync_openclaw_memory.py [--dry-run]`
- 详情见 `references/hermes-openclaw-memory-sync.md`

## 与MetaGPT对比

| 维度 | MetaGPT RoleZeroLongTermMemory | Dream Long-Term RAG |
|------|-------------------------------|---------------------|
| **RAG引擎** | Chroma + LLMRanker | JSONL + 关键词匹配 |
| **召回触发** | memory_k 溢出 或 用户需求 | 每次蒸馏前 |
| **晋升条件** | count > memory_k | age > 30天 且 recallCount < 3 |
| **向量化** | embedding 模型 | 词袋模型（简化版） |
| **复杂度** | 依赖 Chroma/llama-index | 纯 Python，无外部依赖 |
