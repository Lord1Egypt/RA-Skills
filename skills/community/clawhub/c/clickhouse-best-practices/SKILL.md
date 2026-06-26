---
name: clickhouse-best-practices
description: "ClickHouse 数据库优化专家技能。MUST USE when reviewing ClickHouse schemas, queries, or configurations. 审查 CREATE TABLE、ALTER TABLE、SELECT、JOIN、聚合查询、写入策略和配置。包含 28 条规则，涵盖表结构设计、查询优化和数据写入三大类。关键词：ClickHouse, ORDER BY, PRIMARY KEY, MergeTree, ReplacingMergeTree, LowCardinality, 分区, JOIN, mutation, 批量写入"
---

# ClickHouse 最佳实践专家

全面的 ClickHouse 指南，涵盖表结构设计、查询优化和数据写入。包含 3 大类（表结构、查询、写入）共 28 条规则，按影响程度排序。

> **官方文档：** [ClickHouse 最佳实践](https://clickhouse.com/docs/best-practices)

## 核心职责

1. **表结构审查**：分析 CREATE TABLE 和 ALTER TABLE 语句，确保设计最优
2. **查询优化**：审查 SELECT、JOIN 和聚合查询的性能表现
3. **写入策略**：指导用户进行批量写入、异步写入以及避免 mutation 操作
4. **问题排查**：帮助诊断和修复常见的 ClickHouse 性能问题

## 如何应用本技能

**优先级顺序：**
1. 检查 `rules/` 目录中是否有适用的规则
2. 如果有规则：应用规则并使用"根据 `规则名称`..."的格式引用
3. 如果没有规则：使用 LLM 的 ClickHouse 知识或搜索官方文档
4. 如果不确定：使用网络搜索获取当前最佳实践
5. 务必标注来源：规则名称、"ClickHouse 通用指南"或具体 URL

**为什么规则优先：** ClickHouse 具有特殊的行为特性（列式存储、稀疏索引、合并树机制），在这些场景下，通用的数据库直觉可能会产生误导。

## 审查输出格式

审查表结构、查询或配置时，请按以下格式组织输出：

```
## 检查的规则
- `规则名称-1` - 符合规范 / 存在问题

## 发现

### 问题项
- **`规则名称`**：问题描述
  - 当前状态：[代码当前的做法]
  - 应该做到：[正确的做法]
  - 修复方案：[具体的修改建议]

### 符合规范项
- `规则名称`：简要说明为什么符合规范

## 建议
[按优先级排列的修改建议，并引用相关规则]
```

## 审查流程

### 表结构审查（CREATE TABLE, ALTER TABLE）
**规则文件：**
1. `rules/schema-pk-plan-before-creation.md`
2. `rules/schema-pk-cardinality-order.md`
3. `rules/schema-pk-prioritize-filters.md`
4. `rules/schema-types-native-types.md`
5. `rules/schema-types-minimize-bitwidth.md`
6. `rules/schema-types-lowcardinality.md`
7. `rules/schema-types-avoid-nullable.md`
8. `rules/schema-partition-low-cardinality.md`
9. `rules/schema-partition-lifecycle.md`

**检查清单：**
- PRIMARY KEY / ORDER BY 列顺序（从低基数到高基数）
- 数据类型是否匹配实际数据范围
- 对合适的字符串列应用 LowCardinality
- 分区键基数有界（100-1,000 个值）
- 如果使用 ReplacingMergeTree 需有版本列

### 查询审查（SELECT, JOIN, 聚合）
**规则文件：**
1. `rules/query-join-choose-algorithm.md`
2. `rules/query-join-filter-before.md`
3. `rules/query-join-use-any.md`
4. `rules/query-index-skipping-indices.md`
5. `rules/schema-pk-filter-on-orderby.md`

**检查清单：**
- 过滤条件使用 ORDER BY 前缀列
- JOIN 前先过滤表数据
- 根据表大小选择正确的 JOIN 算法
- 对非 ORDER BY 过滤列使用跳数索引

### 写入策略审查
**规则文件：**
1. `rules/insert-batch-size.md`
2. `rules/insert-mutation-avoid-update.md`
3. `rules/insert-mutation-avoid-delete.md`
4. `rules/insert-async-small-batches.md`
5. `rules/insert-optimize-avoid-final.md`

**检查清单：**
- 每次 INSERT 批量大小 10K-100K 行
- 频繁变更不要使用 ALTER TABLE UPDATE
- 更新场景使用 ReplacingMergeTree 或 CollapsingMergeTree
- 高频小批量写入启用异步插入

## 规则分类（按优先级排序）

| 优先级 | 分类 | 影响程度 | 前缀 | 关注点 | 规则数量 |
|--------|------|----------|------|--------|----------|
| 1 | 主键选择 | 关键 | `schema-pk-` | ORDER BY 列顺序 | 4 |
| 2 | 数据类型选择 | 关键 | `schema-types-` | 原生类型、LowCardinality | 5 |
| 3 | JOIN 优化 | 关键 | `query-join-` | 算法选择、过滤优化 | 5 |
| 4 | 批量写入 | 关键 | `insert-batch-` | 每次 INSERT 10K-100K 行 | 1 |
| 5 | 避免 Mutation | 关键 | `insert-mutation-` | ReplacingMergeTree 替代 UPDATE | 2 |
| 6 | 分区策略 | 高 | `schema-partition-` | 低基数、生命周期管理 | 4 |
| 7 | 跳数索引 | 高 | `query-index-` | bloom_filter、minmax | 1 |
| 8 | 物化视图 | 高 | `query-mv-` | 增量/可刷新物化视图 | 2 |
| 9 | 异步写入 | 高 | `insert-async-` | 服务端缓冲 | 2 |
| 10 | 避免 OPTIMIZE | 高 | `insert-optimize-` | 让后台合并自然进行 | 1 |
| 11 | JSON 使用 | 中等 | `schema-json-` | 动态 schema | 1 |

## 快速参考

### 表结构设计 - 主键（关键）
- `schema-pk-plan-before-creation` - 建表前规划 ORDER BY（不可更改）
- `schema-pk-cardinality-order` - 列按基数从低到高排序
- `schema-pk-prioritize-filters` - 包含常用过滤列
- `schema-pk-filter-on-orderby` - 查询过滤必须使用 ORDER BY 前缀

### 表结构设计 - 数据类型（关键）
- `schema-types-native-types` - 使用原生类型，不要全用 String
- `schema-types-minimize-bitwidth` - 使用能容纳数据的最小数值类型
- `schema-types-lowcardinality` - 唯一值 <10K 的字符串用 LowCardinality
- `schema-types-enum` - 有限值集合用 Enum 并启用校验
- `schema-types-avoid-nullable` - 避免 Nullable，改用 DEFAULT

### 表结构设计 - 分区（高）
- `schema-partition-low-cardinality` - 分区数量控制在 100-1,000
- `schema-partition-lifecycle` - 分区用于数据生命周期管理，而非查询优化
- `schema-partition-query-tradeoffs` - 理解分区裁剪的权衡
- `schema-partition-start-without` - 考虑先不分区

### 表结构设计 - JSON（中等）
- `schema-json-when-to-use` - 动态 schema 用 JSON；已知结构用类型化列

### 查询优化 - JOIN（关键）
- `query-join-choose-algorithm` - 根据表大小选择算法
- `query-join-use-any` - 只需一条匹配时用 ANY JOIN
- `query-join-filter-before` - JOIN 前先过滤
- `query-join-consider-alternatives` - 字典/宽表 vs JOIN
- `query-join-null-handling` - join_use_nulls=0 使用默认值

### 查询优化 - 索引（高）
- `query-index-skipping-indices` - 非 ORDER BY 过滤列使用跳数索引

### 查询优化 - 物化视图（高）
- `query-mv-incremental` - 实时聚合用增量物化视图
- `query-mv-refreshable` - 复杂 JOIN 用可刷新物化视图

### 写入策略 - 批量（关键）
- `insert-batch-size` - 每次 INSERT 10K-100K 行

### 写入策略 - 异步（高）
- `insert-async-small-batches` - 高频小批量用异步写入
- `insert-format-native` - Native 格式性能最佳

### 写入策略 - Mutation（关键）
- `insert-mutation-avoid-update` - 用 ReplacingMergeTree 替代 ALTER UPDATE
- `insert-mutation-avoid-delete` - 用轻量级 DELETE 或 DROP PARTITION

### 写入策略 - 优化（高）
- `insert-optimize-avoid-final` - 让后台合并自然进行

## 适用场景

本技能适用于：
- CREATE TABLE 语句
- ALTER TABLE 修改
- ORDER BY 或 PRIMARY KEY 相关讨论
- 数据类型选择问题
- 慢查询排查
- JOIN 优化需求
- 数据写入管道设计
- 更新/删除策略问题
- ReplacingMergeTree 或特殊引擎使用
- 分区策略决策

## 重要提示

- 建议修改前务必在真实数据上测试
- 给出建议时要考虑各种权衡因素
- 适时引用 ClickHouse 官方文档
- 关注 ClickHouse 版本特性（24.x 及以上版本）
