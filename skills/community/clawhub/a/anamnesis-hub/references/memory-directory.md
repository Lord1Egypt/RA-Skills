# memory/ 目录结构详解

> 最后更新：2026-05-16 (v1.13.1)
> 本文档说明 `~/.openclaw/workspace/memory/` 下所有文件的作用及其与记忆架构的关系。

---

## 目录总览

```
memory/
├── YYYY-MM-DD.md              # L1 短时记忆日志
├── MEMORY_INDEX.md            # 向量索引快照（自动生成）
├── projects/                  # P2: 项目独立记忆
│   ├── README.md
│   └── {slug}.md
├── .dreams/                   # Dreaming 管线工作目录
│   ├── daily-ingestion.json
│   ├── events.jsonl
│   ├── phase-signals.json
│   ├── session-corpus/
│   ├── session-ingestion.json
│   └── short-term-recall.json
├── archive/                   # 归档记录
├── dreaming/                  # Dreaming 产出目录
│   └── light/
│       └── YYYY-MM-DD.md
├── .sync-cloud-state.json     # Cloud 同步游标
├── .sync-push-state.json      # Cloud 推送状态
├── .session-extract-state.json # 会话提取状态
├── .cron-delivery-heartbeat.json # 心跳消息队列
├── .cron-delivery.json        # 历史投递记录
├── .gateway-pid.json          # Gateway 进程跟踪
└── .pipeline-run-YYYY-MM-DD.log # 管道运行日志
```

---

## 一、L1 短时记忆日志 (`YYYY-MM-DD.md`)

| 属性 | 值 |
|------|-----|
| **来源** | Agent 会话中自主写入 / session-extract.py 提取 |
| **内容** | 当日会话摘要、关键决策、技术笔记、待办事项 |
| **格式** | 自由 Markdown，人工可编辑 |
| **生命周期** | 30-90 天保留 |
| **与记忆架构关系** | **核心 L1 层** — 向量搜索的主要语料来源 |

---

## 二、向量索引快照 (`MEMORY_INDEX.md`)

| 属性 | 值 |
|------|-----|
| **来源** | `sync-vector-index.py` 自动生成，三方同步时更新 |
| **生成方式** | FTS5 BM25 聚类，score > 0.65 的高权重 chunks |
| **内容** | 来源分布（memory/sessions 占比）、高频文件 Top10、最近更新文件 |
| **频率** | 每日更新 |
| **与记忆架构关系** | **辅助可读层** — 不是检索用，是人类可读的索引健康快照 |

### 示例内容

```markdown
# 向量索引快照

> 总索引: 1394 个语义块, 2 个来源

## 📊 来源分布
- **memory**: 1331 chunks (95%)
- **sessions**: 63 chunks (5%)

## 📂 高频文件
- memory/2026-05-12.md → 242 chunks
```

### 注意事项
- ❌ **不要**写入 L2 或 ARCHIVE —— 它是自动生成的衍生数据
- ✅ 用于验证向量库是否正常工作（chunk 数量/分布是否合理）

---

## 三、P2 项目记忆 (`projects/`)

| 属性 | 值 |
|------|-----|
| **来源** | 手动创建 + Agent 维护 |
| **内容** | 每个 GitHub 项目独立一个 `{slug}.md` |
| **格式** | 标准模板：项目名、GitHub URL、状态、关键决策、待办 |
| **与记忆架构关系** | **L2c 扩展** — 防止项目记忆污染主 MEMORY.md |

### 当前活跃项目

| 文件 | GitHub | 说明 |
|------|--------|------|
| `clawguard.md` | VictorQR/clawguard | 安全守护插件 |
| `anamnesis-hub.md` | VictorQR/anamnesis-hub | 记忆架构 hub |
| `openclaw-dir-inventory.md` | VictorQR/openclaw-dir-inventory | 目录清单管理 |

---

## 四、状态文件 (`.json`)

### 4.1 `.sync-cloud-state.json`

追踪 MemOS Cloud 同步游标，防止重复拉取。

```json
{
  "lastPullTime": "2026-05-15 22:03:32",
  "lastPage": 6,
  "hasMore": false
}
```

| 字段 | 说明 |
|------|------|
| `lastPullTime` | 上次拉取的时间戳 |
| `lastPage` | 上次拉取的页码 |
| `hasMore` | 是否还有更多数据 |

**使用者**: `sync-cloud-pull.py`

---

### 4.2 `.sync-push-state.json`

追踪本地文件 SHA-256 哈希，用于云端增量推送比对。

```json
{
  "files": {
    "MEMORY.md": "abc123...",
    "ARCHIVE.md": "def456..."
  }
}
```

| 字段 | 说明 |
|------|------|
| `files` | 文件名 → SHA-256 哈希映射 |

**使用者**: `sync-cloud-push.py`

---

### 4.3 `.session-extract-state.json`

追踪已处理的会话 ID，防止重复提取。

```json
{
  "version": 1,
  "lastRun": "2026-05-15",
  "processedIds": ["62463b70-...", "8fc31a7c-..."]
}
```

| 字段 | 说明 |
|------|------|
| `version` | 状态格式版本 |
| `lastRun` | 上次运行日期 |
| `processedIds` | 已处理的 session ID 列表 |

**使用者**: `session-extract.py`

---

### 4.4 `.cron-delivery-heartbeat.json`

心跳消息投递队列。

```json
{
  "pending": []
}
```

| 字段 | 说明 |
|------|------|
| `pending` | 待投递消息数组 |

**使用者**: HEARTBEAT.md 心跳机制

---

### 4.5 `.cron-delivery.json`

历史投递记录，用于审计和调试。

---

### 4.6 `.gateway-pid.json`

OpenClaw Gateway 进程 ID 追踪，用于健康检查。

---

## 五、管线日志

### `.pipeline-run-YYYY-MM-DD.log`

统一日终管线的运行日志。

```bash
[18:00:01] 📋 daily-memory-pipeline start — stage: full
[18:00:02] ↓ 阶段1: sync-pull
[18:05:30] 🧠 阶段2: auto-memory v3
[18:05:35]   归档: 3 新增 / 12 重复跳过
[18:06:00] ↑ 阶段3: sync-push + reindex
[22:00:01] 📊 阶段4: session-extract
[22:05:30] ⏳ 阶段5: activation decay
[22:05:31]    facts.db: 55 facts decayed
[22:05:32] 🏥 阶段6: healthcheck
[22:05:32]    MEMORY.md: 88 行 ✅
```

**使用者**: `daily-memory-pipeline.sh`

---

## 六、Dreaming 目录 (`.dreams/`)

| 文件 | 说明 |
|------|------|
| `daily-ingestion.json` | 每日摄入数据（Dreaming 输入） |
| `events.jsonl` | Dreaming 事件日志 |
| `phase-signals.json` | 阶段信号（REM/DeepSeek/Promotion 状态） |
| `session-corpus/` | 会话分析语料库 |
| `session-ingestion.json` | 会话摄入状态 |
| `short-term-recall.json` | 短时召回状态 |

**注意**: 这是 memory-core 插件的内部数据，**不要手动修改**。

---

## 七、dreaming/ 产出目录

`dreaming/light/YYYY-MM-DD.md` — Dreaming 每日分析结果摘要。

**用途**: 被 auto_memory_extract.py 消费，作为记忆提取的补充语料源（P1 整合后）。

---

## 八、文件分类速查

| 类别 | 文件 | 可手动编辑 | 可删除 | 来源 |
|------|------|----------|--------|------|
| 🔴 核心记忆 | `YYYY-MM-DD.md` | ✅ | ❌ (30天内) | Agent + session-extract |
| 🔴 核心记忆 | `projects/*.md` | ✅ | ❌ | 手动 + Agent |
| 🟡 自动衍生 | `MEMORY_INDEX.md` | ❌ | ✅ (会重建) | sync-vector-index.py |
| 🟡 自动衍生 | `dreaming/light/*.md` | ❌ | ✅ | Dreaming |
| 🟢 状态文件 | `.sync-*.json` | ❌ | ⚠️ (重置状态) | sync 脚本 |
| 🟢 状态文件 | `.session-extract-state.json` | ❌ | ⚠️ (重置进度) | session-extract |
| 🟢 状态文件 | `.cron-delivery*.json` | ✅ | ⚠️ | cron 系统 |
| 🟢 状态文件 | `.gateway-pid.json` | ❌ | ✅ | Gateway |
| 🔵 管线日志 | `.pipeline-run-*.log` | ❌ | ✅ (7天后) | daily-memory-pipeline.sh |
| ⚫ 内部数据 | `.dreams/` | ❌ | ❌ | memory-core 插件 |
| ⚫ 历史归档 | `archive/` | ❌ | ⚠️ | 操作记录 |

---

## 九、与记忆架构层级映射

```
L0 (memory-core SQLite + sqlite-vec)
    ↑ 索引自
L1 memory/YYYY-MM-DD.md  ← session-extract.py
    ↑ Dreaming 提升至
L2a MEMORY.md (索引层 ~88行)
    ↓ 双向索引 ←→
L2b ARCHIVE.md (档案层 ~218行)
    ↓ seed-facts-db.py
L2c facts.sqlite (结构化)
    ↑ 激活/衰减
    facts_activation.py
```


## 十、P3 记忆候选审核 (`.candidates/`)

| 属性 | 值 |
|------|-----|
| **路径** | `memory/.candidates/` |
| **脚本** | `scripts/candidates_review.py` |
| **流程** | Dreaming 产出 → candidates.json → 待审队列 → 用户确认 → ARCHIVE.md |

### 命令

```bash
python3 candidates_review.py list           # 列出待审
python3 candidates_review.py approve --id X # 批准写入ARCHIVE.md
python3 candidates_review.py reject --id X  # 拒绝
python3 candidates_review.py approve-all    # 全批准
python3 candidates_review.py stats          # 统计
```

## 十一、LCM 替代方案 (P3)

OpenClaw 不支持 `memoryFlush` 配置键。LCM 通过 **AGENTS.md 规则** 实现：
- 会话中确认的关键决策，必须在 compaction 前写入 `memory/YYYY-MM-DD.md`
- 禁止仅在对话中给出约束而不写入文件（夏季悦失控案例）
