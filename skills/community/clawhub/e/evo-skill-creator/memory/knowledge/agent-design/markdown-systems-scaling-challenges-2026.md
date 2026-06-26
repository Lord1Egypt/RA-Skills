---
created: 2026-03-29
updated: 2026-03-29
last_accessed: 2026-03-29
access_count: 1
study_count: 1
category: agent-design
volatility: high
confidence: medium
status: active
---

# Markdown-Based Agentic Systems 的多租户扩展挑战（2026）

> 学习日期：2026-03-29
> 来源：The Next Gen Tech Insider、多个 2026 年 3 月的行业报告
> 学习次数：1

## 核心问题

**标题**："Markdown-Based Agentic Systems Face Multi-Tenancy Scaling Challenges"

**背景**：
- 2024-2025：Markdown-based agent systems（如 SKILL.md、AGENT.md）成为主流
- 2026：随着企业采用，多租户和规模化问题开始暴露

## 主要挑战

### 1. 多租户隔离问题

**问题描述**：
- 文件系统天然不支持多租户隔离
- 不同用户/团队的 agent 共享同一文件系统时，容易互相干扰
- 权限控制粒度粗糙（文件级 vs 记录级）

**影响**：
- 企业环境中，A 团队的 agent 可能读取到 B 团队的敏感数据
- 无法实现细粒度的访问控制（如"只能读取自己创建的记录"）

**我们的现状**：
- 我们的 memory/ 架构是单租户设计
- 每个智能体有独立的 memory 目录，天然隔离
- 但如果未来要支持"多个用户共享同一智能体"，会遇到这个问题

### 2. 并发写入冲突

**问题描述**：
- 多个 agent 同时写入同一 Markdown 文件时，容易产生冲突
- 文件系统没有事务机制，无法保证原子性
- Git 合并冲突需要人工介入

**影响**：
- 调度系统中，多个任务同时执行时可能互相覆盖
- execution.log 追加写入可能丢失部分日志

**我们的现状**：
- 我们目前是"乐观并发"——假设不会冲突
- execution.log 追加写入，理论上有冲突风险
- 如果未来接入 scheduler 高频调度，这个问题会放大

### 3. 查询性能瓶颈

**问题描述**：
- 文件系统扫描（grep/find）在大规模数据时性能下降
- 无法实现高效的语义检索（需要向量相似度搜索）
- 复杂查询（如"找出最近 30 天访问过的、包含关键词 X 的、由用户 Y 创建的文件"）需要多次扫描

**影响**：
- knowledge/ 目录文件数量增长到数百个时，检索变慢
- 无法实现"智能推荐"（如"你可能需要这些知识"）

**我们的现状**：
- 我们目前依赖 Grep 工具进行内容搜索
- 文件数量还不多（~20 个），性能尚可
- 但缺少语义检索能力（如"找出与当前任务相关的知识"）

### 4. 结构化数据存储困难

**问题描述**：
- Markdown 适合文档，不适合结构化数据
- 无法高效存储和查询表格数据（如 agents-registry）
- 数据一致性难以保证（如字段格式不统一）

**影响**：
- agents-registry.md 是表格，但 Markdown 表格难以程序化操作
- 无法实现"查询所有状态为 active 的智能体"这样的结构化查询

**我们的现状**：
- agents-registry.md 是 Markdown 表格，人类可读但机器难解析
- 如果未来要实现"批量升级所有子智能体"，需要解析表格

## 2026 年的解决方案趋势

### 1. 混合架构（Hybrid Architecture）

**核心思想**：文件系统 + 数据库，各取所长。

**架构设计**：
```
┌─────────────────────────────────────┐
│  Agent Memory Layer                 │
├─────────────────────────────────────┤
│  File System (Markdown)             │  ← 人类可读、版本控制
│  - 知识文档 (knowledge/)            │
│  - 学习计划 (learning-plan.md)      │
│  - 报告 (output/report/)            │
├─────────────────────────────────────┤
│  Lightweight DB (SQLite/DuckDB)     │  ← 结构化查询、高性能
│  - 执行日志 (execution_log)         │
│  - 智能体注册表 (agents_registry)   │
│  - 知识索引 (knowledge_index)       │
└─────────────────────────────────────┘
```

**分工原则**：
- **文件系统**：存储需要人类阅读、编辑、版本控制的内容
- **数据库**：存储需要高频查询、结构化操作的数据

### 2. 文件系统增强（Enhanced File System）

**Bossa 方案**：MCP + CLI 文件系统持久化
- 通过 MCP (Model Context Protocol) 提供统一接口
- CLI 工具管理文件系统 memory
- 支持事务性写入（避免并发冲突）

**Observable File Systems**：
- 为文件系统增加可观测性
- 监控文件访问模式、热点文件
- 自动识别过时文件

### 3. 轻量级索引（Lightweight Indexing）

**核心思想**：不使用向量数据库，但增加索引层。

**实现方式**：
- 为每个知识文件生成元数据（tags、keywords、summary）
- 创建 INDEX.md 作为知识目录
- 使用 Grep + 元数据实现"伪语义检索"

**我们可以借鉴**：
- 为 knowledge/ 文件补充 YAML frontmatter（已经在做）
- 创建 knowledge/INDEX.md 作为知识索引
- 实现简单的"知识推荐"功能

## 对我们的启示

### 短期（立即可做）

1. **增强元数据**：
   - 为所有 knowledge/ 文件补充完整的 YAML frontmatter
   - 增加 tags 字段（如 `tags: [memory, architecture, 2026]`）

2. **创建知识索引**：
   - 创建 `memory/knowledge/INDEX.md`
   - 按类别、标签组织知识清单

3. **结构化日志**：
   - 将 execution.log 从纯文本升级为 JSONL 格式
   - 便于程序化查询和分析

### 中期（需要设计）

1. **agents-registry 结构化**：
   - 考虑将 agents-registry.md 改为 agents-registry.yaml
   - 或者同时维护 .md（人类可读）和 .yaml（机器可读）

2. **并发写入保护**：
   - 为 execution.log 实现文件锁机制
   - 或者使用 SQLite 存储日志

3. **知识检索工具**：
   - 实现 `search_knowledge` 工具（基于 Grep + 元数据）
   - 支持"找出与当前任务相关的知识"

### 长期（探索方向）

1. **混合架构**：
   - 评估是否需要引入 SQLite 存储结构化数据
   - 保持文件系统为主，数据库为辅

2. **多租户支持**：
   - 如果未来要支持"多用户共享智能体"
   - 需要设计权限隔离机制

3. **可观测性**：
   - 监控 memory/ 的访问模式
   - 自动识别热点知识和过时知识

## 核心结论

**Markdown-based systems 不是银弹**：
- 小规模、单租户场景：文件系统完全够用
- 大规模、多租户场景：需要混合架构

**我们的定位**：
- 当前是小规模、单租户场景
- 文件系统架构是正确的选择
- 但需要提前准备扩展能力（元数据、索引、结构化日志）

**不要过早优化**：
- 不要现在就引入数据库
- 先把文件系统用到极致
- 等真正遇到瓶颈再升级

## 参考资料

- [Markdown-Based Agentic Systems Face Multi-Tenancy Scaling Challenges](https://www.thenextgentechinsider.com/pulse/markdown-based-agentic-systems-face-multi-tenancy-scaling-challenges)
- [Bossa Launches Persistent Filesystem Memory for AI Agents via MCP and CLI](https://www.thenextgentechinsider.com/pulse/bossa-launches-persistent-filesystem-memory-for-ai-agents-via-mcp-and-cli)
- [Observable file systems for agents](https://blog.chudioranu.com/posts/agent-file-systems-observability/)
- [Instructions.md vs Skills.md vs Agent.md vs Agents.md](https://priyankavergadia.substack.com/p/how-to-structure-skillmd-agentsmd)
