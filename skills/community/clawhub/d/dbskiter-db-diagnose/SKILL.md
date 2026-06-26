---
name: db-diagnose
description: |
  数据库诊断与优化，支持SQL诊断、慢查询分析、索引推荐、性能快照。

  使用场景：
  - 用户说"数据库慢了" -> 执行 slow-queries
  - 用户说"SQL有问题" -> 执行 sql "<SQL>"
  - 用户说"推荐索引" -> 执行 recommend-indexes
  - 用户说"全面检查" -> 执行 report
  - 用户说"性能分析" -> 执行 performance-snapshot
  - 用户说"瓶颈分析" -> 执行 bottleneck

  用法：
  - dbskiter --output-mode=ai --database=<name> diagnose slow-queries
  - dbskiter --output-mode=ai --database=<name> diagnose sql "SELECT * FROM users"
  - dbskiter --output-mode=ai --database=<name> diagnose recommend-indexes
  - dbskiter --output-mode=ai --database=<name> diagnose report
  - dbskiter --output-mode=ai --database=<name> diagnose performance-snapshot
  - dbskiter --output-mode=ai --database=<name> diagnose bottleneck
---

# 数据库诊断 Skill

## 何时使用

当用户提到以下关键词时，使用此skill：

| 用户说法 | 执行命令 | 说明 |
|---------|---------|------|
| "数据库慢了" | `dbskiter --output-mode=ai --database=<name> diagnose slow-queries` | 查看慢查询 |
| "SQL有问题" | `dbskiter --output-mode=ai --database=<name> diagnose sql "<SQL>"` | 诊断特定SQL |
| "加什么索引" | `dbskiter --output-mode=ai --database=<name> diagnose recommend-indexes` | 获取索引建议 |
| "检查一下" | `dbskiter --output-mode=ai --database=<name> diagnose report` | 全面诊断报告 |
| "有锁吗" | `dbskiter --output-mode=ai --database=<name> diagnose locks` | 查看锁情况 |
| "性能分析" | `dbskiter --output-mode=ai --database=<name> diagnose performance-snapshot` | 采集性能快照 |
| "瓶颈分析" | `dbskiter --output-mode=ai --database=<name> diagnose bottleneck` | 分析性能瓶颈 |
| "CPU高" | `dbskiter --output-mode=ai --database=<name> diagnose performance-snapshot` | 查看CPU指标 |
| "IO高" | `dbskiter --output-mode=ai --database=<name> diagnose bottleneck` | 查看IO瓶颈 |

## 数据库支持

### 统一性能模型支持

| 数据库 | 性能快照 | 瓶颈分析 | 慢查询 | 状态 |
|-------|---------|---------|--------|------|
| MySQL | 支持 | 支持 | 支持 | 生产就绪 |
| Oracle | 支持 | 支持 | 支持 | 生产就绪 |
| PostgreSQL | 支持 | 支持 | 支持 | 生产就绪 |

**说明**：
- MySQL：支持5.7/8.0，自动降级（performance_schema -> information_schema -> SHOW STATUS）
- Oracle：支持11g/12c/19c/21c，自动降级（AWR -> V$视图 -> 基础统计），支持RAC
- PostgreSQL：支持10-16，自动降级（pg_stat_statements -> pg_stat_activity），支持pg_stat_kcache扩展

## 核心命令

### 1. 查看慢查询
```bash
dbskiter --database=<数据库名> diagnose slow-queries
```
**默认行为**：返回最近7天最慢的10个查询

**可选参数**：
- `--limit=5`：只看前5条
- `--min-duration=0.5`：超过0.5秒的查询

### 2. 诊断SQL
```bash
dbskiter --database=<数据库名> diagnose sql "SELECT * FROM users WHERE email = 'test@test.com'"
```
**输出**：评分、问题列表、优化建议

### 3. 推荐索引
```bash
dbskiter --database=<数据库名> diagnose recommend-indexes
```
**默认行为**：分析所有表，推荐高价值索引

**可选参数**：
- `--table=users`：只分析指定表

### 4. 查看锁
```bash
dbskiter --database=<数据库名> diagnose locks
```
**输出**：当前锁等待情况

### 5. 性能快照（新增）
```bash
dbskiter --database=<数据库名> diagnose performance-snapshot
```
**输出**：CPU、IO、内存、并发、锁等多维度性能指标

**适用场景**：
- 数据库整体性能评估
- 容量规划前的基线采集
- 性能问题的全面诊断

**输出示例**：
```json
{
  "summary": "性能快照采集完成",
  "data": {
    "snapshot": {
      "timestamp": "2026-04-24T10:30:00",
      "metrics": [
        {
          "name": "active_session_ratio",
          "value": 75.5,
          "unit": "%",
          "category": "cpu",
          "severity": "high"
        }
      ],
      "slow_queries": [...],
      "active_sessions": 15,
      "total_sessions": 100
    },
    "bottlenecks": [...]
  }
}
```

### 6. 瓶颈分析（新增）
```bash
dbskiter --database=<数据库名> diagnose bottleneck
```
**输出**：自动识别性能瓶颈并给出优化建议

**适用场景**：
- 数据库性能下降时的快速诊断
- 定位CPU/IO/锁等具体瓶颈

**输出示例**：
```json
{
  "summary": "发现3个性能瓶颈",
  "data": {
    "bottlenecks": [
      {
        "category": "cpu",
        "severity": "high",
        "metrics": [...],
        "suggestion": "检查高CPU消耗的SQL，考虑优化或增加CPU资源"
      }
    ],
    "severity_summary": {
      "critical": 0,
      "high": 1,
      "medium": 2,
      "low": 0
    },
    "recommendations": [
      "[cpu] 检查高CPU消耗的SQL，考虑优化或增加CPU资源"
    ]
  }
}
```

### 7. 综合报告
```bash
dbskiter --database=<数据库名> diagnose report
```
**输出**：慢查询 + 索引建议 + 锁情况 + 总体评分

## AI决策流程

### 场景1：用户说"数据库慢了"

```
步骤1：执行 dbskiter --database=<name> diagnose performance-snapshot
步骤2：查看返回的bottlenecks，确定瓶颈类型
步骤3：如果是慢查询导致，执行 dbskiter --database=<name> diagnose slow-queries
步骤4：根据诊断结果，执行 dbskiter --database=<name> diagnose recommend-indexes
步骤5：总结给用户："发现X个性能瓶颈，主要是XX问题，建议..."
```

### 场景2：用户说"CPU使用率很高"

```
步骤1：执行 dbskiter --database=<name> diagnose performance-snapshot
步骤2：查看metrics中category为cpu的指标
步骤3：如果active_session_ratio高，执行 dbskiter --database=<name> diagnose slow-queries
步骤4：给出优化建议
```

### 场景3：用户说"帮我优化这个SQL"

```
步骤1：执行 dbskiter --database=<name> diagnose sql "<SQL>"
步骤2：如果评分<70，执行 dbskiter --database=<name> diagnose recommend-indexes
步骤3：给出优化后的SQL和建议
```

### 场景4：用户说"做个全面检查"

```
步骤1：执行 dbskiter --database=<name> diagnose performance-snapshot（查看当前性能状态）
步骤2：执行 dbskiter --database=<name> diagnose report（获取综合报告）
```
