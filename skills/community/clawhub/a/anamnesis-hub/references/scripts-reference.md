# Scripts Reference — anamnesis-hub 脚本说明

> 所有脚本的统一参考：用途、触发方式、依赖关系、关键参数。
> 最后更新：2026-05-17 | v1.13.1

---

## 一、脚本总表

| 脚本 | 位置 | 用途 | cron 触发 |
|------|------|------|-----------|
| `auto-setup.sh` | `scripts/` | 一键安装交互脚本 | 手动 |
| `auto_memory_extract.py` | `user_workspace/scripts/` | 两阶段记忆提取（ARCHIVE → MEMORY） | 18:30 / 22:30 CST |
| `session-extract.py` | `user_workspace/scripts/` | 会话 JSONL 扫描 → .learnings/ + memory/ | 22:00 CST |
| `daily-memory-pipeline.sh` | `user_workspace/scripts/` | 统一编排 6 阶段管线 | 可作单一 cron |
| `sync-cloud-pull.py` | `user_workspace/scripts/` | MemOS Cloud → 本地 | 18:00 / 20:00 / 22:00 CST |
| `sync-cloud-push.py` | `user_workspace/scripts/` | 本地 → MemOS Cloud | 18:00 / 20:00 / 22:00 CST |
| `sync-vector-index.py` | `user_workspace/scripts/` | 向量库 → MEMORY_INDEX.md | 随 sync-push |
| `sync-all.sh` | `user_workspace/scripts/` | sync 三合一编排 | 18:00 / 20:00 / 22:00 CST |
| `seed-facts-db.py` | `scripts/` | 从 ARCHIVE.md 初始化 facts.sqlite | 手动 |
| `facts_activation.py` | `scripts/` | Hebbian 激活 + 衰减 | 手动或 cron |
| `candidates_review.py` | `scripts/` | P3 记忆候选审核 | 手动 |
| `check_current_session.py` | `scripts/` | 查看最近会话（调试用） | 手动 |
| `write_file.py` | `scripts/` | 跨平台文本写入（UTF-8/BOM/CRLF） | 被调用 |

---

## 二、脚本详解

### 2.1 auto-setup.sh

**用途**：一键交互式安装 anamnesis-hub 环境。

```bash
cd /home/victor/github/anamnesis-hub
bash scripts/auto-setup.sh
```

**交互步骤**：
1. 检查 Ollama 是否安装 → 建议安装或跳过
2. 下载 `bge-m3` embedding 模型
3. 检测 `subconscious-personality-guardian` 冲突插件 → 自动加入禁用列表
4. 安装 memory-core 插件
5. 配置 `openclaw.json`（自动插入推荐配置）
6. 安装 MemOS Cloud 插件（可选）
7. 创建 `memory/` 目录
8. 设置 Dreaming cron（03:00 UTC）

**参数**：
| 参数 | 说明 |
|------|------|
| `--skip-ollama` | 跳过 Ollama 安装（已安装时用） |
| `--skip-memos` | 跳过 MemOS Cloud 安装 |
| `--dry-run` | 预览模式，不实际执行 |

---

### 2.2 auto_memory_extract.py

**用途**：两阶段记忆提取管道，从 MemOS Cloud 拉取的缓存文件中提取有价值记忆，写入 ARCHIVE.md（阶段一）和 MEMORY.md（阶段二）。

```bash
python3 user_workspace/scripts/auto_memory_extract.py --mode full --days 1
```

**核心参数**：
| 参数 | 说明 |
|------|------|
| `--mode status` | 查看缓存文件状态，不执行提取 |
| `--mode dry-run` | 测试模式，输出预览 |
| `--mode full` | 生产模式执行提取 |
| `--days N` | 拉取最近 N 天的 memos-cloud 缓存 |

**Pipeline 流程（两通道）**：
```
memos-cloud-YYYY-MM-DD.md
    ↓
┌─ 通道A: qwen3:8b 过滤去重 ─→ {add: [...], update: [], remove: []}
└─ 通道B: memos-extractor-0.6b 结构化提取 ─→ memory_detail_list + preference_detail_list
    ↓ 交叉验证（宽松 OR 逻辑）
    ↓ SHA-256 去重
    ↓
Stage 1 → ARCHIVE.md（完整条目，hash:xxxxxx 标记）
Stage 2 → MEMORY.md（一行摘要索引）
```

**关键配置**（读取环境变量或 `~/.openclaw/.env`）：
- `MEMOS_API_KEY` — MemOS Cloud API Token
- `OLLAMA_BASE=http://127.0.0.1:11434`
- `LLM_MODEL=qwen3:8b`

**NOISE_KEYWORDS**：标题含以下关键词的条目跳过不处理：
```
Cron delivery check, Cron delivery process, OpenClaw doctor,
Dreams of a rack, Dashboard URL, Wiki同步, Cron delivery result,
无待投递, 已搬运, heartbeat, HEARTBEAT, cron-delivery
```

---

### 2.3 session-extract.py

**用途**：扫描 sessions 目录的 `.jsonl` 文件，通过 MemOS extractor + reranker 两遍提取，写入 `.learnings/ERRORS.md`（错误记录）和 `memory/YYYY-MM-DD.md`（日记忆）。

```bash
python3 user_workspace/scripts/session-extract.py --days 5
python3 user_workspace/scripts/session-extract.py --full    # 全量
python3 user_workspace/scripts/session-extract.py --cleanup # 提取后清理可回收文件
python3 user_workspace/scripts/session-extract.py --reset  # 重置处理状态
```

**核心参数**：
| 参数 | 说明 |
|------|------|
| `--days N` | 拉取最近 N 天（默认 5） |
| `--full` | 全量模式（等同于 `--days` 不限） |
| `--pass-num 1\|2` | 分析遍次：1=首次全量，2=查漏补缺 |
| `--cleanup` | 提取完成后清理可回收文件 |
| `--reset` | 重置 processedIds 状态，重新全量运行 |
| `--dry-run` | 测试模式 |

**两遍流程**：
```
Pass 1: .jsonl → .analyzed1.jsonl
  → .learnings/ERRORS.md（踩坑记录）
  → .learnings/LEARNINGS.md（经验教训）

Pass 2: .analyzed1.jsonl → .analyzed2.jsonl → trash
  → memory/YYYY-MM-DD.md
```

**保护逻辑**：
- 自动跳过最新 2 条会话（main + qqbot），防止正在运行的会话被重命名
- `cleanup_trashable_files()` 通过 sessions.json 双重保护 main 和 qqbot 会话

**可回收文件类型**：
| 类型 | 模式 | 保护 |
|------|------|------|
| trajectory | `*.trajectory.jsonl` | 清理 |
| trajectory-path | `*.trajectory-path.json` | 清理 |
| analyzed1 | `*.analyzed1` | 清理 |
| analyzed2 | `*.analyzed2` | 清理 |
| reset | `*.jsonl.reset.*` | 清理 |
| deleted | `*.deleted.*` | 清理 |

**状态文件**：`memory/.session-extract-state.json`（记录 processedIds）

**reranker 三路 query**：
```python
QUERIES = [
    ("问题解决", "问题解决 错误修复 配置调试..."),   # THRESHOLD_PROBLEM=0.15
    ("偏好经验", "偏好 习惯 用户喜欢 用户要求..."),   # THRESHOLD_PREF=0.20
    ("技术细节", "error message报错 账号密码 key..."),  # THRESHOLD_TECH=0.15
]
# 宽松 OR 逻辑：通过任一 query 即保留
```

---

### 2.4 daily-memory-pipeline.sh

**用途**：统一编排日终管线，替代三个独立 cron 任务。

```bash
bash user_workspace/scripts/daily-memory-pipeline.sh full    # 全量运行
bash user_workspace/scripts/daily-memory-pipeline.sh sync-only  # 仅同步
bash user_workspace/scripts/daily-memory-pipeline.sh extract-only # 仅提取
bash user_workspace/scripts/daily-memory-pipeline.sh status     # 查看状态
```

**6 阶段流程**：
```
18:00 ─┬─ 阶段1: sync-pull  (Cloud → local)
       │
18:30 ─┼─ 阶段2: auto-memory v3 (ARCHIVE.md → MEMORY.md)
       │
18:40 ─┼─ 阶段3: sync-push + reindex (local → Cloud)
       │
22:00 ─┼─ 阶段4: session-extract (JSONL → .learnings/ + memory/)
       │
22:05 ─┤─ 阶段5: facts.db decay (激活 * 0.95)
       │
22:06 ─┴─ 阶段6: healthcheck (MEMORY.md/ARCHIVE.md 行数 + facts.db 统计)
```

**日志输出**：每次运行写入 `memory/.pipeline-run-YYYY-MM-DD.log`

**非致命错误**：所有阶段失败时记录 ⚠️ 而不中断管线

---

### 2.5 sync-cloud-pull.py / sync-cloud-push.py / sync-all.sh

**用途**：三方同步脚本，保持 MemOS Cloud ↔ 本地 Markdown ↔ 向量库三者一致。

**sync-all.sh** 是编排脚本，同时调用 pull、push 和 index：
```bash
bash user_workspace/scripts/sync-all.sh
```

**sync-cloud-pull.py**：从 MemOS Cloud API 拉取新条目，写入 `memos-cloud-YYYY-MM-DD.md`
**sync-cloud-push.py**：将本地 Markdown 变化推送到 MemOS Cloud（增量，只推 SHA256 变化的文件）

**排除文件**（不推送到云）：
- `memos-cloud-*.md`
- `MEMORY_INDEX.md`
- `DREAMS.md`
- `.sync-*.json`

---

### 2.6 seed-facts-db.py

**用途**：从 ARCHIVE.md 初始化 facts.sqlite 结构化知识图谱。

```bash
python3 scripts/seed-facts-db.py
```

提取 ARCHIVE.md 中的结构化条目，写入 facts.sqlite（entity/key/value + activation），用于精确查询和热度追踪。

---

### 2.7 facts_activation.py

**用途**：Hebbian 激活 + 每日衰减，维持 facts 热度分级（HOT/WARM/COOL）。

```bash
python3 scripts/facts_activation.py
```

**激活规则**：每次查询触发 `activation += 0.5, access_count += 1`
**衰减规则**：非永久 facts 每日 `activation *= 0.95`（下限 0.005）
**分级**：
| 等级 | 阈值 | 说明 |
|------|------|------|
| HOT | > 2.0 | 高频访问 facts |
| WARM | 0.02 ~ 2.0 | 正常 facts |
| COOL | < 0.02 | 待审核 GC 候选 |

---

### 2.8 candidates_review.py

**用途**：P3 记忆候选审核机制，人工确认后再写入 ARCHIVE.md。

```bash
python3 scripts/candidates_review.py list          # 列出待审
python3 scripts/candidates_review.py approve --id X # 批准写入ARCHIVE.md
python3 scripts/candidates_review.py reject --id X  # 拒绝
python3 scripts/candidates_review.py approve-all   # 批准所有
python3 scripts/candidates_review.py stats          # 统计
```

**状态文件**：`memory/.candidates/review-state.json`

---

### 2.9 check_current_session.py

**用途**：调试脚本，列出最近 5 个会话及其时间、路径、sessionKey。

```bash
python3 scripts/check_current_session.py
```

输出示例：
```
Top 5 most recent sessions:
  [1] 2026-05-17 01:05:00 | 06d8446a-35df-4b1d-9230-d307b724fe6a.jsonl ← CURRENT SESSION (DO NOT RENAME)
       sessionKey: c4e539d2-3c6c-43e8-9629-9ceb2d4e548c
       path: /home/victor/.openclaw/agents/main/sessions/06d8446a-35df-4b1d-9230-d307b724fe6a.jsonl
  [2] 2026-05-16 22:30:00 | 6b6ebef5-a2f0-4096-b2e9-5acac0e0622b.jsonl
```

---

### 2.10 write_file.py

**用途**：跨平台文本写入，自动处理 UTF-8 编码、BOM、CRLF 换行符。

**不能直接调用**（被其他脚本间接调用）：
```bash
python3 scripts/write_file.py --path /tmp/test.txt --content-file /tmp/content.txt
```

或通过 `cross-platform-writer` skill 拦截所有 `write` 工具调用。

---

## 三、Cron 调度参考

### 完整 cron 配置表

```cron
# ┌─────────── minute (0-59)
# │ ┌───────── hour (0-23, UTC)
# │ │ ┌─────── day of month (1-31)
# │ │ │ ┌───── month (1-12)
# │ │ │ │ ┌── day of week (0-7, 0=Sun)
# │ │ │ │ │
# ▼ ▼ ▼ ▼ ▼
# ↓ ↓ ↓ ↓ ↓

# Dreaming — 每日 UTC 03:00 (CST 11:00)
0 3 * * *  /home/victor/github/anamnesis-hub/scripts/daily-memory-pipeline.sh full >> /home/victor/.openclaw/workspace/memory/.pipeline-run-$(date +\%Y-\%m-\%d).log 2>&1

# 三方同步 — CST 18:00 / 20:00 / 22:00 (= UTC 10:00 / 12:00 / 14:00)
0 10,12,14 * * *  bash /home/victor/.openclaw/workspace/user_workspace/scripts/sync-all.sh

# auto-memory v3 — CST 18:30 / 22:30 (= UTC 10:30 / 14:30)
30 10,14 * * *  python3 /home/victor/.openclaw/workspace/user_workspace/scripts/auto_memory_extract.py --mode full --days 1

# session-extract — CST 22:00 (= UTC 14:00)
0 14 * * *  python3 /home/victor/.openclaw/workspace/user_workspace/scripts/session-extract.py --days 5 --cleanup

# facts 衰减 — CST 22:05 (= UTC 14:05)
5 14 * * *  python3 /home/victor/.openclaw/workspace/user_workspace/scripts/facts_activation.py
```

> 注：daily-memory-pipeline.sh 已覆盖大部分阶段，可作为单一 cron 替代上述多个独立任务。

---

## 四、依赖关系图

```
auto-setup.sh
  ├── 安装 Ollama + bge-m3
  ├── 安装 memory-core 插件
  ├── 配置 openclaw.json
  └── 安装 MemOS Cloud 插件（可选）

daily-memory-pipeline.sh
  ├── 阶段1: sync-cloud-pull.py
  ├── 阶段2: auto_memory_extract.py
  │     └── 调用 memos-extractor-0.6b API + qwen3:8b
  ├── 阶段3: sync-cloud-push.py + openclaw memory index
  ├── 阶段4: session-extract.py
  │     └── 调用 memos-extractor + memos-reranker API
  ├── 阶段5: facts_activation.py (inline)
  └── 阶段6: healthcheck (inline)

candidates_review.py
  └── 读取 memory/.candidates/review-state.json
  └── 写入 ARCHIVE.md

seed-facts-db.py
  └── 读取 ARCHIVE.md
  └── 写入 facts.sqlite

write_file.py
  └── 被 auto_memory_extract.py / session-extract.py 间接调用
  └── cross-platform-writer skill 拦截所有 write 工具
```

---

## 五、常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| extractor 返回 400 | tokens 超限 | 自动减半重试 |
| sync-pull 无反应 | MEMOS_API_KEY 未设置 | 检查 `~/.openclaw/.env` |
| session-extract 跳过所有文件 | pass 筛选模式错误 | 确认通配符 `.jsonl` vs `.analyzed1` |
| facts.db 无数据 | 未运行 seed-facts-db.py | 先执行 seed 初始化 |
| 跨平台写入乱码 | 未用 write_file.py | 所有文本写入统一走 cross-platform-writer |