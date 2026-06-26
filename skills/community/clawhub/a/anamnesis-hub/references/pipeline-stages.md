# Pipeline Stages — 日终管线 6 阶段详解

> 每日统一管线流程：CST 18:00 → 22:00，覆盖 sync、extract、decay、healthcheck。
> 最后更新：2026-05-17 | v1.13.1

---

## 一、管线总览

```
时间 (CST)      阶段                      脚本                          状态
──────────────────────────────────────────────────────────────────────
18:00           阶段1: sync-pull          sync-cloud-pull.py            ✅
18:30           阶段2: auto-memory v3     auto_memory_extract.py        ✅
18:40           阶段3: sync-push+reindex  sync-cloud-push.py            ✅
                               +         openclaw memory index --force
20:30           阶段X: Session 分析       Session Analysis Daily     ✅
22:00           阶段4: session-extract   session-extract.py            ✅
22:05           阶段5: facts decay       facts_activation.py (inline)  ✅
22:06           阶段6: healthcheck       healthcheck (inline)          ✅
```

统一编排脚本：`daily-memory-pipeline.sh`

---

## 二、阶段详解

### 阶段 1：sync-pull — Cloud → 本地

**时间**：18:00 CST | **脚本**：`sync-cloud-pull.py` | **日志**：`memory/.pipeline-run-YYYY-MM-DD.log`

**输入**：MemOS Cloud API（`GET /api/memo`）
**输出**：`user_workspace/memos-cloud-cache/memos-cloud-YYYY-MM-DD.md`

**流程**：
1. 读取 `.sync-cloud-state.json` 的 `lastPullTime` 作为游标
2. 请求 `create_time >= lastPullTime` 的条目
3. 追加到 `memos-cloud-YYYY-MM-DD.md`
4. 更新 `.sync-cloud-state.json`

**失败处理**：非致命错误，记录 ⚠️ 继续管线
**依赖**：MemOS API Token（`MEMOS_API_KEY` 环境变量或 `~/.openclaw/.env`）

---

### 阶段 2：auto-memory v3 — 两阶段提取

**时间**：18:30 CST | **脚本**：`auto_memory_extract.py` | **日志**：stdout → 管道日志

**输入**：`user_workspace/memos-cloud-cache/memos-cloud-*.md`
**输出**：
- 阶段1 → `ARCHIVE.md`（完整条目，SHA-256 去重，hash 标记）
- 阶段2 → `MEMORY.md`（一行摘要索引）

**Pipeline 内部流程**：
```
memos-cloud-YYYY-MM-DD.md
    ↓
┌─ 通道A: qwen3:8b 过滤去重 ─→ {add: [...], update: [], remove: []}
│   提取 prompt：与已有 MEMORY.md 对比去重，输出 JSON
└─ 通道B: memos-extractor-0.6b API 结构化提取
│   → memory_detail_list + preference_detail_list
    ↓ 交叉验证（宽松 OR 逻辑）
    ↓ 过滤 NOISE_KEYWORDS
    ↓ SHA-256 去重（已有 hash 不写入）
    ↓
Stage 1: ARCHIVE.md
  - 写入完整条目：<!-- hash:{16位hash} -->
  - 组织在 ## Auto-Extracted 历史归档 下
  - 同一日期内的条目归并到同一 ### YYYY-MM-DD 块
    ↓
Stage 2: MEMORY.md
  - 更新/追加一行：Auto-Extracted ({date}): {n} 条新记忆 → ARCHIVE.md:{line}
  - 不写入详细内容，只做索引
```

**去重机制**：
- SHA-256(content) 前 16 位 → `<!-- hash:xxxxxxxxxxxxxxxx -->`
- 已在 ARCHIVE.md 存在 hash 的条目跳过
- NOISE_KEYWORDS 过滤：标题含系统级噪音关键词的条目跳过

**输出示例**：
```json
{
  "status": "ok",
  "pipeline": "two-stage (archive → summarize)",
  "stage1_archive": {"added": 3, "skipped": 12, "section_line": 88},
  "stage2_memory": {"memory_md_updated": true, "summary": "Auto-Extracted (2026-05-17): 3 条新记忆 → ARCHIVE.md:88"},
  "summary": {
    "total_candidates": 5,
    "added_after_dedup": 3,
    "duplicates_skipped": 12,
    "qwen3_count": 4,
    "extractor_count": 3,
    "extractor_extra": 1
  }
}
```

**失败处理**：非致命错误，记录 ⚠️ 继续管线

---

### 阶段 3：sync-push + reindex — 本地 → Cloud + 向量

**时间**：18:40 CST | **脚本**：`sync-cloud-push.py` + `openclaw memory index --force` | **日志**：stdout → 管道日志

**输入**：本地 Markdown 文件（MEMORY.md、ARCHIVE.md、memory/YYYY-MM-DD.md）
**输出**：
- MemOS Cloud（`POST /api/memo`，增量推送）
- 向量索引（`memory-core` rebuild）

**流程**：
1. 读取 `.sync-push-state.json` 中各文件的 SHA256 哈希
2. 计算当前文件哈希，与存储的哈希比对
3. 只推送变化的文件（SHA256 不同）
4. 更新 `.sync-push-state.json`
5. 执行 `openclaw memory index --force` 重建向量索引

**排除文件**（不推送）：
- `memos-cloud-*.md`（来自云端）
- `MEMORY_INDEX.md`（自动生成的本地衍生文件）
- `DREAMS.md`（瞬态分析输出）
- `.sync-*.json`（内部状态文件）

**失败处理**：非致命错误，记录 ⚠️ 继续管线

---

### 阶段 4：session-extract — JSONL → .learnings + memory

**时间**：22:00 CST | **脚本**：`session-extract.py` | **日志**：stdout → 管道日志

**输入**：`~/.openclaw/agents/main/sessions/*.jsonl`
**输出**：
- `.learnings/ERRORS.md`（踩坑记录）
- `.learnings/LEARNINGS.md`（经验教训）
- `memory/YYYY-MM-DD.md`（日记忆）
- 状态文件：`memory/.session-extract-state.json`

**两遍流程**：
```
Pass 1: 未处理的 .jsonl → .analyzed1
  → 提取问题解决类内容 → .learnings/ERRORS.md
  → 提取偏好经验类内容 → .learnings/LEARNINGS.md

Pass 2: .analyzed1.jsonl → .analyzed2.jsonl → gio trash
  → 提取技术细节类内容 → memory/YYYY-MM-DD.md
```

**保护逻辑**：
- 自动跳过最新 2 条会话（main + qqbot），防止正在运行的会话被重命名
- `cleanup_trashable_files()` 通过 sessions.json 保护 main 和 qqbot 会话

**reranker 三路 query（宽松 OR 逻辑）**：
| Query | 内容 | 阈值 |
|-------|------|------|
| 问题解决 | 问题解决 错误修复 配置调试... | 0.15 |
| 偏好经验 | 偏好 习惯 用户喜欢 用户要求... | 0.20 |
| 技术细节 | error message报错 账号密码 key配置... | 0.15 |

**可回收文件**：`.trajectory.jsonl`、`.trajectory-path.json`、`.analyzed1`、`.analyzed2`、`.jsonl.reset.*`、`.deleted.*`

**失败处理**：非致命错误，记录 ⚠️ 继续管线

---

### 阶段 5：facts decay — 激活衰减

**时间**：22:05 CST | **实现**：内联在 `daily-memory-pipeline.sh` 中 | **数据库**：`~/.openclaw/memory/facts.sqlite`

**流程**：
```python
UPDATE facts SET activation = activation * 0.95 WHERE permanent = 0 AND activation > 0.01
```
- 非永久 facts：`activation *= 0.95`（下限 0.005）
- 永久 facts：不参与衰减
- 记录受影响行数到日志

**分级阈值**：
| 等级 | 条件 | 说明 |
|------|------|------|
| HOT | activation > 2.0 | 高频 facts |
| WARM | 0.02 ≤ activation ≤ 2.0 | 正常 facts |
| COOL | activation < 0.02 | GC 候选，待审核 |

---

### 阶段 6：healthcheck — 健康检查

**时间**：22:06 CST | **实现**：内联在 `daily-memory-pipeline.sh` 中

**检查项**：
| 检查项 | 阈值 | 超标处理 |
|--------|------|----------|
| MEMORY.md 行数 | ≤ 100 | ⚠️ 记录警告 |
| ARCHIVE.md 行数 | ≤ 250 | ⚠️ 记录警告 |
| facts.db 总数 | — | 记录统计 |
| facts.db HOT 数量 | — | 记录统计 |
| facts.db COOL 数量 | — | 记录统计 |

**输出示例**：
```
[22:06:01] 🏥 阶段6: healthcheck
[22:06:02]    MEMORY.md: 88 行 ✅
[22:06:02]    ARCHIVE.md: 218 行 ✅
[22:06:03]    facts.db: 55 total / 3 HOT / 12 COOL
```

---

## 三、失败处理策略

所有 6 阶段均采用**非致命错误**策略：
- 阶段失败 → 记录 ⚠️ 到日志 → 继续下一阶段
- 不会因单阶段失败中断整条管线
- 需要人工干预的场景：API Token 过期、磁盘空间不足、sessions.json 损坏

**失败恢复**：
| 阶段 | 失败场景 | 恢复方式 |
|------|----------|----------|
| sync-pull | 网络断开 | 下次 cron 自动重试（基于游标） |
| auto-memory | API 超时 | 下次 cron 自动重试 |
| sync-push | Token 过期 | 手动刷新 token 后重试 |
| session-extract | 文件锁定 | 保护机制生效，不会处理运行中的会话 |
| facts decay | db 不存在 | 跳过，继续管线 |
| healthcheck | 文件不存在 | 记录 ⚠️，不影响管线 |

---

## 四、日志文件

每次完整运行生成：`memory/.pipeline-run-YYYY-MM-DD.log`

**结构**：
```
[18:00:01] 📋 daily-memory-pipeline start — stage: full
[18:00:02] ↓ 阶段1: sync-pull (Cloud → local)
[18:05:30] 🧠 阶段2: auto-memory v3
[18:05:35]   归档: 3 新增 / 12 重复跳过
[18:06:00] ↑ 阶段3: sync-push + reindex
20:30           阶段X: Session 分析       Session Analysis Daily     ✅
[22:00:01] 📊 阶段4: session-extract
[22:00:05]   提取: 2 errors / 3 lessons
[22:05:01] ⏳ 阶段5: activation decay
[22:05:02]    facts.db: 55 facts decayed
[22:06:01] 🏥 阶段6: healthcheck
[22:06:02]    MEMORY.md: 88 行 ✅
[22:06:02]    ARCHIVE.md: 218 行 ✅
[22:06:03] ✅ pipeline complete — stage: full
```

---

## 五、独立运行 vs 统一管线

| 运行方式 | 命令 | 适用场景 |
|----------|------|----------|
| 独立运行（单阶段） | `python3 auto_memory_extract.py --mode full` | 调试单阶段 |
| 统一管线（全部） | `bash daily-memory-pipeline.sh full` | 生产环境推荐 |
| 仅同步 | `bash daily-memory-pipeline.sh sync-only` | 快速同步 |
| 仅提取 | `bash daily-memory-pipeline.sh extract-only` | 离线调试 |
| 查看状态 | `bash daily-memory-pipeline.sh status` | 快速检查 |

**推荐配置**：使用 `daily-memory-pipeline.sh full` 作为单一 cron 任务，替代多个独立 cron，避免时序依赖问题。
### 阶段 X：Session 分析 — 历史会话深度分析

**时间**：20:30 CST | **Job**：`Session Analysis Daily` | **触发**：cron agentTurn | **日志**：cron 投递队列

**输入**：已索引的 sessions JSONL + `memory_search` 搜索结果
**输出**：`memory/YYYY-MM-DD.md`（分析摘要）

**流程**：
1. `openclaw memory index --force` — 确保 bge-m3 索引最新
2. `memory_search` — 搜索过去 24-48 小时内的新会话内容
3. **OpenClaw 默认模型深度分析** — 使用 `minimax/MiniMax-M2.7`（主模型）或配置的默认回退模型，分析已索引的会话内容，提取：
   - 关键决策和教训
   - 偏好和习惯的变化
   - 重要上下文更新
4. `openclaw memory rem-backfill --path ./memory --stage-short-term` — 写入数据库
5. 将分析摘要追加到 `memory/YYYY-MM-DD.md`
6. 汇报摘要写入 `memory/.cron-delivery-heartbeat.json`

**关键说明**：
- 使用 OpenClaw **默认模型**（主模型 `minimax/MiniMax-M2.7`，回退 `deepseek-v4-flash`），无需额外配置 DeepSeek
- 不是脚本管道，而是 **agentTurn payload**，完全由 agent 的工具驱动
- 属于日间（而非日终）分析，在 session-extract 之前运行，提前捕获重要决策

**状态文件**：无（纯 agent workflow）
**失败处理**：非致命，记录 ⚠️ 到 cron 投递队列后继续

