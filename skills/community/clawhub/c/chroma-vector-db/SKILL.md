---
name: chroma-vector-db
description: |-
  Chroma 向量数据库：Rust 内核（v1.0.0+ 重写，2025-03），多语言客户端SDK。单节点用 PersistentClient（SQLite + 本地 HNSW）或 EphemeralClient（内存）；分布式 / 云用 SPANN + BLOCKFILE on S3/GCS。
  Chroma vector database: Rust core (v1.0.0+ rewrite, 2025-03) with multi-language client SDKs. Single-node uses PersistentClient (SQLite + local HNSW) or EphemeralClient (in-memory); distributed/cloud uses SPANN + BLOCKFILE on S3/GCS. 25+ EmbeddingFunction providers shipped.
license: MIT-0
compatibility: AI engineering knowledge skill — host AI consumes seed.yaml directly. No installation required.
metadata:
  version: "v0.1.0"
  blueprint_id: "finance-bp-138"
  blueprint_source: "chroma-core/chroma"
  blueprint_commit: "598f85f0872746b1e821ffddca5c1e7058cd8b9e"
  category: ai-engineering
  doramagic_url: "https://doramagic.ai/zh/crystal/chroma-vector-db"
  openclaw:
    skillKey: chroma-vector-db
    category: ai-engineering
    primaryEnv: knowledge
---
# 这个 skill 适合什么用户？能做哪些任务？

## 概览

Chroma 是 Rust 内核的开源向量数据库（github.com/chroma-core/chroma，v1.0.0+ 2025-03 重写）。单节点模式用 PersistentClient（SQLite 元数据 + 本地 HNSW 索引）或 EphemeralClient（内存）；分布式 / 云模式用 SPANN 索引+ 自研 BLOCKFILE 存储 on S3/GCS。

数据路径：Client Factory → API 层（v1.0.0 起 Rust 默认）→ Segment 层（本地 2 段 / 分布式 3 段）→ Index（HNSW 或 SPANN）→ 持久化。Embed...

**Doramagic 晶体页**: https://doramagic.ai/zh/crystal/chroma-vector-db

## 知识规模

- **52 条约束** (3 fatal + 49 non-fatal)
- 上游源码: `chroma-core/chroma` @ commit `598f85f0`
- 蓝图 ID: `finance-bp-138`

## 用法

Host AI（Claude Code / Cursor / OpenClaw）读 `references/seed.yaml`，按其中的：
- `intent_router` 匹配用户意图
- `architecture` 理解项目架构
- `constraints` 应用 anti-pattern 约束
- `business_decisions` 参考核心设计决策

## FAQ 摘要

### 这个 skill 适合什么用户？能做哪些任务？
适合需要向量数据库支持 RAG / 推荐 / 语义搜索的工程师：原型开发用EphemeralClient，本地小规模用 PersistentClient，生产分布式用云SPANN。25+ EmbeddingFunction 一键切换。访问 doramagic.ai/r/chroma 查看完整用例。

### 需要准备什么环境？依赖什么？
**SQLite ≥ 3.35.0 是硬要求**（chromadb/__init__.py:137-155 检查并 raise，Colab 自动 hot-swap 到 pysqlite3-binary）。Python ≥ 3.9。服务端 / 分布式需要 Rust 工具链或预构建 docker。可选：hosted EF 的 provider API key（OpenAI / Cohere 等）。

### 会踩哪些坑？这个 skill 怎么防护？
本 skill 内置 52 条约束（3 条 fatal）。典型踩坑：(1) cosine 实现实际是 `1 - dot(a,b)`，假定向量预归一化——未归一化数据score 会偏；(2) v1.0.0 Rust 默认静默忽略 4 个旧 Python 设置（chroma_server_nofile 等）——配置文件没报错但不生效；

---

完整文档: 见 `references/seed.yaml` (v6.1 schema). 浏览页: https://doramagic.ai/zh/crystal/chroma-vector-db
