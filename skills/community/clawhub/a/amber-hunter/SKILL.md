---
title: amber-hunter
summary: Long-term memory and knowledge compilation skill for Claude Code — manages memory capsules, insight caching, semantic/keyword hybrid recall, DID E2E encryption, and AI-driven knowledge wiki compiler.
version: 1.2.41
source: ~/.openclaw/skills/amber-hunter/amber_hunter.py
protocol: FastAPI / Bearer Token / localhost-only admin ops
port: 18998
---

# amber-hunter — AI 第二大脑 Skill

## What It Is

amber-hunter 是运行在本地（port 18998）的 FastAPI 服务，为 Claude Code 提供长期记忆能力和知识自动编译能力。

**核心能力矩阵：**

| 能力 | 说明 | 引入版本 |
|------|------|---------|
| 记忆胶囊 | 持久化存储 AI 工作产生的想法/决策/上下文 | v1.0 |
| 混合搜索 | LanceDB 向量 + 关键词联合检索 | v1.2.27 |
| 意图预测 | 根据 session 内容预测下一步最可能的需求 | v1.2.27 |
| DID E2E 加密 | 设备绑定加密，云端隐私保护 | v1.2.24 |
| 知识编译器 | 同类胶囊自动编译成 wiki 概念页 | v1.2.38 |

## 启动

```bash
cd ~/.openclaw/skills/amber-hunter
python3 amber_hunter.py
# 或后台运行
python3 amber_hunter.py &
```

服务启动时：
1. 自动初始化 SQLite 数据库（`memory.db`）
2. 启动编译 daemon（每 6 小时扫描一次覆盖缺口）
3. 冷启动编译（启动时如果有覆盖缺口，立即触发一次）

## 认证

| 操作 | 认证方式 |
|------|---------|
| 所有外部请求 | Bearer Token（从 `/token` 获取，写入 `~/.openclaw/token`）|
| `/token`, `/bind-apikey`, `/master-password` | 强制 localhost 检查 |
| Bearer Token 调用 | 在 `Authorization: Bearer <token>` Header 中传递 |

**Token 获取流程（首次设置）：**
```bash
# 1. 启动服务
python3 amber_hunter.py

# 2. 从本地获取 token（仅 localhost 可访问）
curl http://localhost:18998/token
# 返回: {"token": "xxx"}

# 3. 写入本地配置
echo "Bearer xxx" > ~/.openclaw/token
```

## API 端点总览

### 无需认证（localhost）

| 端点 | 方法 | 说明 |
|------|------|------|
| `GET /status` | GET | 服务状态、版本、平台、胶囊数 |
| `GET /token` | GET | 读取本地 API Token |
| `POST /bind-apikey` | POST | 更新 Huper 云端 API Key（存 Keychain）|
| `POST /master-password` | POST | 设置 master_password（Keychain）|

### 核心 — 胶囊管理（Bearer Token）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/capsules` | GET | 列出胶囊（支持 `category_path` 过滤 + 分页 `limit`）|
| `/capsules` | POST | 创建胶囊 |
| `/capsules/{id}` | GET | 获取单个胶囊详情 |
| `/capsules/{id}` | PATCH | 更新胶囊 |
| `/capsules/{id}` | DELETE | 删除胶囊 |

### 核心 — 记忆召回（Bearer Token）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/recall` | GET | 混合搜索（向量+关键词+LanceDB，rerank）|
| `/rerank` | POST | 强制 LLM 重排候选记忆 |
| `/classify` | GET | 关键词+LLM fallback 分类 |
| `/extract` | POST | 从文本中提取记忆（LLM 驱动）|
| `/ingest` | POST | AI 主动写入记忆（→ 入库或审阅队列）|

**`/recall` 参数：**

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `q` | string | 必填 | 查询文本 |
| `rerank` | bool | false | 是否启用 LLM rerank (deprecated, use rerank_engine) |
| `rerank_engine` | string | "auto" | 重排序引擎：auto \| model \| llm \| none |
| `hyde` | bool | false | 是否启用 HyDE（假设性答案增强检索）v1.2.41 |
| `multi_hop` | bool | false | 是否启用多跳检索 v1.2.41 |
| `limit` | int | 3 | 返回数量 |
| `category_path` | string | "" | MFS路径过滤 |
| `use_insights` | bool | true | 是否优先返回 insight 缓存 |
| `citation` | int | 0 | 1=返回 embedding 裁剪的片段 |

**`/recall` 响应新增字段（v1.2.41）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `rerank_time_ms` | float | reranker 耗时（毫秒） |
| `hyde_time_ms` | float | HyDE 生成耗时（毫秒） |
| `retrieval_hops` | int | 检索跳数（multi_hop 启用时 > 1） |

**`/recall/evaluate` 端点（v1.2.41）：**

| 端点 | 方法 | 说明 |
|------|------|------|
| `/recall/evaluate` | POST | RAG 评测（RAGAS + NDCG@5） |

**`/recall/evaluate` 请求体：**
```json
{"queries": [{"q": "...", "expected_capsule_ids": ["..."]}]}
```

**`/recall/evaluate` 响应：**
```json
{
  "ragas_scores": {"faithfulness": 0.x, "answer_relevancy": 0.x, "context_precision": 0.x},
  "ndcg_at_5": 0.x,
  "evaluated_at": "...",
  "total_queries": 2
}
```

**`/ingest` 参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `content` | string | 记忆内容 |
| `tags` | string | 标签（逗号分隔）|
| `session_key` | string | 来源 session |
| `auto_review` | bool | true=直接入库，false=进审阅队列 |

### 审阅队列（Bearer Token）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/queue` | GET | 列出待审阅记忆 |
| `/queue/{qid}/approve` | POST | 批准写入胶囊 |
| `/queue/{qid}/reject` | POST | 拒绝 |
| `/queue/{qid}/edit` | POST | 修改后批准 |

### 知识编译器 v1.2.38+（Bearer Token）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/concepts` | GET | 列出所有已编译概念页（`?limit=50&offset=0` 分页）|
| `/concepts/{path}` | GET | 获取指定 path 的 wiki 内容 |
| `/admin/compile` | POST | 手动触发编译（`?path=` 指定路径）|
| `/admin/compile/status` | GET | daemon 状态 + 覆盖缺口列表 + **健康指标**（alert/crashes/success_count）|

**编译触发条件：**

| 条件 | 说明 |
|------|------|
| 胶囊数比上次编译时多 ≥100 | 增量触发 |
| 超过 6 小时未编译 | 定时触发 |

**覆盖缺口：** 有 ≥3 个胶囊但无 concept page 的 category_path。

### 管理操作（Bearer Token + localhost）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/admin/backfill-paths` | POST | 批量修复缺失的 category_path |
| `/admin/reindex-vectors` | POST | 重建 LanceDB 向量索引 |
| `/admin/train` | POST | 触发 embedding 模型训练 |
| `/admin/train/status` | GET | 训练状态 |
| `/admin/train/score` | GET | 模型评分 |
| `/admin/train/tags` | GET | 标签统计 |
| `/admin/generate-insights` | POST | 手动生成 insights（按 path）|
| `/stats` | GET | 系统统计 |
| `/admin/export` | GET | 导出备份 |

### DID E2E 加密（Bearer Token）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/did/setup` | POST | 初始化 DID（生成密钥对，存 Keychain）|
| `/did/status` | GET | DID 初始化状态 |
| `/did/register-device` | POST | 注册设备到 DID 网络 |
| `/did/auth/challenge` | POST | 获取 auth challenge |
| `/did/auth/sign-challenge` | POST | 签名 challenge，完成认证 |

### WAL（Write-Ahead Log）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/wal/status` | GET | WAL 状态 |
| `/wal/entries` | GET | 读取 WAL 条目 |
| `/wal/gc` | POST | 触发 WAL GC |

### Session 上下文

| 端点 | 方法 | 说明 |
|------|------|------|
| `/session/summary` | GET | 当前 session 记忆摘要 |
| `/session/files` | GET | 当前 session 相关文件列表 |
| `/session/preload` | GET | 预加载 context（供 Claude Code 使用）|
| `/freeze` | GET/POST | 冻结当前 session 上下文 |

### Profile

| 端点 | 方法 | 说明 |
|------|------|------|
| `/profile` | GET | 完整用户 profile |
| `/profile/{section}` | GET/PUT | 读取/更新 profile 章节 |
| `/profile/build` | POST | 触发 profile 自动构建 |

### Corrections（记忆纠错）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/corrections/stats` | GET | 纠错统计 |
| `/corrections/suggestions` | GET | 纠错建议 |
| `/corrections/apply` | POST | 应用纠错规则 |

### 工具类

| 端点 | 方法 | 说明 |
|------|------|------|
| `GET /` | GET | 根路径，返回欢迎信息 |
| `GET /patterns` | GET | 当前系统运作的 Pattern 列表 |
| `POST /mcp` | POST | MCP（Model Context Protocol）接口 |

## 数据模型

### capsules 表

```sql
CREATE TABLE capsules (
    id              TEXT PRIMARY KEY,     -- 唯一 ID (secrets.token_hex)
    memo            TEXT,                 -- 记忆摘要
    content         TEXT,                  -- 完整内容
    category_path   TEXT,                  -- 分类路径，如 "dev/python"
    tags            TEXT,                  -- 逗号分隔标签
    hotness_score   REAL DEFAULT 0,        -- 热度分
    hit_count       INTEGER DEFAULT 0,     -- 被 recall 命中的次数
    session_id      TEXT,                  -- 来源 session
    encrypted       INTEGER DEFAULT 0,     -- 是否加密
    vector_id       TEXT,                  -- LanceDB 向量 ID
    synced          INTEGER DEFAULT 0,    -- 是否已同步云端
    created_at      REAL,                  -- unix timestamp
    updated_at      REAL,
    content_hash    TEXT                   -- 去重用
)
```

### insights 表（v1.2.17+）

```sql
CREATE TABLE insights (
    id              TEXT PRIMARY KEY,
    capsule_ids     TEXT,          -- JSON array
    summary         TEXT,           -- 纯文本摘要
    path            TEXT,           -- category_path
    concept_slug    TEXT,           -- slug化 path (v1.2.38+)
    wiki_content    TEXT,           -- 完整 markdown (v1.2.38+)
    hotness_score   REAL DEFAULT 0,
    created_at      REAL,
    updated_at      REAL
)
```

### memory_queue 表

```sql
CREATE TABLE memory_queue (
    id          TEXT PRIMARY KEY,
    content     TEXT,
    tags        TEXT,
    session_id  TEXT,
    source      TEXT DEFAULT 'ingest',
    created_at  REAL
)
```

## 配置

配置文件：`~/.openclaw/skills/amber-hunter/config.json`

```json
{
  "auto_sync": true,
  "sync_interval_seconds": 300,
  "embed_model": "BAAI/bge-m3",
  "vector_dim": 1024,
  "rerank_model": "BAAI/bge-reranker-v2-m3",
  "llm_model": "gpt-4o-mini",
  "huper_api_key": "sk-...",
  "key_source": "pbkdf2",
  "compile_interval_hours": 6.0,
  "compile_capsule_threshold": 100
}
```

## 关键行为

### 胶囊创建时的 category_path 推断

`/ingest` 和 `/capsules POST` 会自动从内容中推断 category_path：

```
推理依据：content + tags → LLM 分类
兜底：category_path = "general/default"
```

### `/recall` 混合评分公式

```
final_score = 0.35 * norm_lance + 0.25 * norm_kw + 0.20 * recency + 0.20 * hotness
```

- LanceDB 向量相似度（归一化）
- 关键词 overlap 分
- 近期性（7天衰减）
- 热度分

### wikilinks 注入策略（Knowledge Compiler）

LLM 生成 wikilinks 不稳定（max_tokens=600 时 Related Capsules 部分常被截断）。
最终策略：**代码事后注入**：

```python
wikilinks = " ".join(f"[[{cid}:{short_label}]]" for cid in capsule_ids)
wiki_content = wiki_content.rstrip() + f"\n\n### Related Capsules\n{wikilinks}"
```

### Cold Start 行为

服务启动时：
1. 如果有覆盖缺口，立即触发一次 `_run_batch_compile()`
2. 如果 `auto_train` 启用，触发 embedding 模型训练

## 使用示例

### 创建记忆

```bash
curl -X POST http://localhost:18998/ingest \
  -H "Authorization: Bearer $(cat ~/.openclaw/token)" \
  -H "Content-Type: application/json" \
  -d '{"content": "修了一个版本号测试过时的问题", "tags": "amber-hunter,bugfix"}'
```

### 召回记忆

```bash
curl "http://localhost:18998/recall?query=amber-hunter版本号问题&rerank=true" \
  -H "Authorization: Bearer $(cat ~/.openclaw/token)"
```

### 手动触发知识编译

```bash
# 编译指定 path
curl -X POST "http://localhost:18998/admin/compile?path=knowledge/devops" \
  -H "Authorization: Bearer $(cat ~/.openclaw/token)"

# 查看 daemon 状态和缺口
curl "http://localhost:18998/admin/compile/status" \
  -H "Authorization: Bearer $(cat ~/.openclaw/token)"
```

### 获取已编译的概念页

```bash
# 列出所有概念页
curl "http://localhost:18998/concepts" \
  -H "Authorization: Bearer $(cat ~/.openclaw/token)"

# 获取指定概念页
curl "http://localhost:18998/concepts/knowledge/devops" \
  -H "Authorization: Bearer $(cat ~/.openclaw/token)"
```

## 已知限制

1. **Bearer Token 存在磁盘**：`~/.openclaw/token` 是明文，localhost 以外不安全
2. **向量索引重建昂贵**：`/admin/reindex-vectors` 在大量胶囊时耗时较长
3. **Wiki 编译器依赖 LLM**：LLM 不可用时 `compile_concept_page` 返回 None
4. **DID 注册需要 Huper 云端**：本地 DID setup 后还需要云端注册才生效

## 相关文件

```
amber-hunter/
├── amber_hunter.py      # FastAPI 主文件，所有端点
├── core/
│   ├── db.py            # SQLite 数据层
│   ├── wiki_compiler.py # 知识编译器（v1.2.38）
│   └── llm.py           # LLM 调用封装
├── tests/
│   └── test_api/
│       └── test_status.py  # 状态 API 测试
├── config.json          # 配置文件
└── SKILL.md             # 本文档
```

## 适用场景

**用 amber-hunter 当：**
- 需要 AI 在长时间对话中保持"记忆"
- 需要从历史胶囊中检索相关经验
- 需要将多个相关记忆自动组织成概念页
- 需要加密存储敏感记忆到云端

**不用 amber-hunter 当：**
- 简单 KV 存储（用文件或 SQLite 直接写）
- 需要服务端部署（它是纯本地服务）
- 需要多人实时协作（它是单人设计）
