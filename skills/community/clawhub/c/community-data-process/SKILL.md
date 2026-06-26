---
name: community-data-process
description: >
  北汽社群数据导出：数据清洗 → 数据校对 → 数据合并。
  从客户群导出文件中筛选温冷一期和试点店标签数据，
  校对关键指标一致性，增量合并到 BI_社群数据上传表。
  统计日期使用源文件创建时间（下载日期）。
  每天 00:55 自动执行。
---

# 北汽社群数据导出

每日社群数据导出 → 清洗 → 校对 → 合并到 BI 系统。

## 流程概览

```
1. 数据清洗 → 2. 数据校对 → 3. 数据合并 → 4. 最终验证
```

## 使用方式

### 一键执行全流程
```bash
python ~/.openclaw/workspace-pm/skills/community-data-process/run.py
```

### 分步执行
```bash
# 第 1 步：数据清洗
python ~/.openclaw/workspace-pm/skills/community-data-process/run.py clean

# 第 2 步：数据校对
python ~/.openclaw/workspace-pm/skills/community-data-process/run.py audit

# 第 3 步：数据合并
python ~/.openclaw/workspace-pm/skills/community-data-process/run.py merge

# 第 4 步：最终验证
python ~/.openclaw/workspace-pm/skills/community-data-process/run.py verify
```

## 规则

### 清洗规则
- 源文件：Downloads 目录下按**创建时间（下载时间）**排序，取最新的 `客户群导出*.xlsx`
- 筛选条件：O 列（群标签）= 温冷一期 或 试点店
- 数字列格式转换：群人数、员工人数、客户人数、今日入群、今日退群、今日消息 → int

### 校对规则
- 三方对比：源文件 vs 清理后 vs 合并后
- 8 个指标全部一致才通过
- 数据质量：无空值、无负值

### 合并规则
- 模式：增量添加（不去重）
- 列映射：源文件 A-O 列 → 目标文件 E-S 列
- D 列统计日期 = 源文件的**创建时间（下载日期）**，文件是哪天下载的就填哪天（不是脚本执行日期）
- A-C 列留空

### 列映射
| 源文件 | → | 目标文件 | 列名 |
|-------|---|---------|------|
| A | → | E | 群 ID |
| B | → | F | 群名称 |
| C | → | G | 群主 |
| D | → | H | 群管理员 |
| E | → | I | 群人数 |
| F | → | J | 群活跃 |
| G | → | K | 群类型 |
| H | → | L | 员工人数 |
| I | → | M | 客户人数 |
| J | → | N | 今日入群 |
| K | → | O | 今日退群 |
| L | → | P | 今日消息 |
| M | → | Q | 入群时间 |
| N | → | R | 最后发言时间 |
| O | → | S | 群标签 |

## 输出文件

| 文件 | 说明 |
|------|------|
| `客户群导出_清理后_温冷一期 + 试点店_YYYYMMDD.xlsx` | 清洗后数据 |
| `BI_社群数据上传_已更新_YYYYMMDD.xlsx` | 合并后最终文件 |
| `数据校对报告_YYYYMMDD.txt` | 校对报告 |

## 常见问题

### Q1: 今日退群数据不一致
检查是否使用了正确的源文件。不同日期导出的文件数据不同。

### Q2: 统计日期错误
脚本自动读取源文件的下载日期，不需要手动指定。

### Q3: 数字列显示为文本
脚本自动转换 6 个数字列为 int 格式。

## 依赖
- Python 3.11+
- pandas
- openpyxl
