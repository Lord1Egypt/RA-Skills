---
created: 2026-03-28
updated: 2026-03-28
last_accessed: 2026-03-28
access_count: 1
study_count: 1
category: agent-design
volatility: medium
confidence: high
status: active
---

# 基于文件系统的 Agent Memory 架构

> 2026年3月学习：SOTA RAG & Memory without the database

## 核心发现

### "No Database" 趋势

**2026年新趋势**：不使用向量数据库，直接使用文件系统 + Git 实现 Agent Memory。

**关键论点**：
- 向量数据库增加了复杂度和依赖
- 文件系统 + Git 已经足够强大
- 简单的方案更容易维护和调试

## 架构对比

### 传统方案（Vector DB）

```
Agent → Embedding Model → Vector Database → Retrieval
                              ↓
                         (Pinecone/Weaviate/Chroma)
```

**问题**：
- 需要额外的基础设施
- 增加了部署复杂度
- 数据存储在外部系统
- 难以版本控制和审计

### 文件系统方案（File-based）

```
Agent → File System + Git → Simple Search/Grep
            ↓
        (Markdown files)
```

**优势**：
- 零额外依赖
- 天然支持版本控制（Git）
- 人类可读可编辑
- 易于备份和迁移

## 我们的架构验证

### 我们已经在用这个方案

**evo-skill-creator 的 memory/ 架构**：
```
memory/
├── learning-plan.md
├── backlog.md
├── agents-registry.md
├── watchlist.md
├── knowledge/
│   ├── agent-design/
│   ├── frameworks/
│   └── ...
└── evolution-log.md
```

**这就是 File-based Memory！**

### 我们的优势

1. **结构化 + 人类可读**
   - Markdown 格式
   - 清晰的目录结构
   - 可以直接编辑

2. **版本控制**
   - 可以用 Git 跟踪变化
   - 可以回滚到历史版本
   - 可以看到知识演化过程

3. **零依赖**
   - 不需要数据库
   - 不需要向量化服务
   - 只需要文件系统

4. **可移植**
   - 整个 memory/ 目录可以直接复制
   - 可以在任何环境运行
   - 可以轻松备份

### 我们的不足

1. **缺少语义检索**
   - 目前只能靠文件名和目录结构
   - 没有"找相关知识"的能力
   - 需要手动定位文件

2. **缺少自动索引**
   - 知识增多后难以快速定位
   - 没有"知识地图"
   - 依赖人工组织

3. **缺少智能检索**
   - 不能"问问题找答案"
   - 不能"根据任务找相关知识"
   - 检索效率低

## 改进方向

### 短期：增强文件系统检索

1. **知识索引文件**
   - `memory/knowledge/INDEX.md`
   - 列出所有知识文件 + 关键词
   - 手动维护，但有总比没有好

2. **标签系统**
   - 在 YAML frontmatter 中加 tags
   - 可以按标签快速过滤
   - 例如：`tags: [memory, architecture, 2026]`

3. **全文搜索工具**
   - 使用 Grep 工具搜索关键词
   - 在唤醒时根据任务搜索相关知识
   - 简单但有效

### 中期：轻量级语义检索

4. **本地 Embedding**
   - 使用轻量级模型（如 sentence-transformers）
   - 为每个知识文件生成 embedding
   - 存储在 `.embeddings/` 目录（不提交到 Git）

5. **相似度搜索**
   - 根据任务描述找相似知识
   - 不需要向量数据库，直接计算余弦相似度
   - 结果缓存到本地

### 长期：智能知识助手

6. **知识检索工具**
   - 为子智能体提供 `search_knowledge` 工具
   - 输入：问题或任务描述
   - 输出：相关知识文件列表

7. **自动知识组织**
   - 定期分析知识文件
   - 自动生成知识地图
   - 识别知识缺口

## 与向量数据库的对比

### 何时需要向量数据库？

**需要的场景**：
- 海量数据（百万级文档）
- 实时检索要求（毫秒级）
- 多租户隔离
- 复杂的过滤条件

**不需要的场景**：
- 个人知识库（我们的场景）
- 中小规模数据（< 10000 文件）
- 可以接受秒级检索
- 单用户或小团队

### 我们的选择

**当前阶段**：文件系统完全够用
- 知识文件数量：< 100
- 检索频率：不高
- 可读性和可维护性更重要

**未来扩展**：可以混合方案
- 核心知识：文件系统（人类可读）
- 大量案例：向量数据库（机器检索）
- 两者互补，不是替代

## 最佳实践

### 1. 文件命名规范

```
knowledge/
├── agent-design/
│   ├── meta-agent-recursive-improvement.md  # 描述性名称
│   ├── context-engineering.md               # 短横线分隔
│   └── skill-evolution-limitations.md       # 小写字母
```

### 2. 目录结构设计

```
按主题分类，不超过 3 层：
knowledge/
├── agent-design/      # 一级：领域
├── frameworks/        # 一级：领域
└── ai-models/         # 一级：领域
```

### 3. 元数据标准

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
category: agent-design
tags: [memory, architecture, file-system]
volatility: medium
confidence: high
---
```

### 4. 内容组织

- 每个文件聚焦一个主题
- 使用清晰的标题层次
- 包含"与其他知识的连接"段落
- 提供"行动建议"

## 关键洞察

### 1. 简单 > 复杂

**Occam's Razor**：
- 能用文件系统解决，就不要用数据库
- 能用 Markdown 解决，就不要用复杂格式
- 能用 Grep 解决，就不要用 AI 检索

### 2. 人类可读 > 机器优化

**为什么**：
- 知识需要人类审查和修正
- 调试时需要直接查看
- 迁移时需要理解内容

### 3. 版本控制是核心能力

**Git 的价值**：
- 知识演化历史
- 错误可以回滚
- 多人协作基础
- 审计和追溯

## 与其他知识的连接

### 连接 #11: 上下文工程

- 文件系统 memory 是"上下文卸载"的实现
- 不把所有知识塞进上下文窗口
- 按需加载相关知识

### 连接 #12: 多 Agent 上下文协同

- 文件系统天然支持共享
- 多个 Agent 可以读写同一个 memory/
- Git 提供了版本控制和冲突解决

### 连接 #13: 知识生命周期管理

- 文件系统 + YAML frontmatter = 完美组合
- 可以轻松实现过时检测
- 可以自动归档和压缩

## 行动建议

### 立即可做

1. **为现有知识文件补充 tags**
   - 在 YAML frontmatter 中加 tags 字段
   - 便于后续按标签检索

2. **创建知识索引**
   - `memory/knowledge/INDEX.md`
   - 列出所有知识文件 + 一句话描述

### 中期规划

3. **实现知识检索工具**
   - 简单的关键词搜索
   - 基于 Grep 的全文检索
   - 返回相关文件列表

4. **为子智能体提供检索能力**
   - 在 SKILL.md 中提供检索指引
   - 教会子智能体如何搜索知识库

### 长期愿景

5. **探索轻量级语义检索**
   - 本地 embedding 模型
   - 不依赖外部服务
   - 可选功能，不是必需

## 参考资料

- SOTA RAG & Memory without the database (2026)
- File-based RAG Memory (nijho.lt)
- Fast Agentic Memory via Query-aware Indexing (arXiv 2601.08160)
- AI Agent Memory Systems Implementation Guide (2026)

## 元数据说明

- **volatility: medium** - 文件系统方案相对稳定，但检索技术在演进
- **confidence: high** - 我们已经在实践这个方案，有实际经验
- **study_count: 1** - 首次系统化学习，但已有实践基础
