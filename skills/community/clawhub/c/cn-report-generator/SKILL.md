---
name: cn-report-generator
version: 1.0.0
description: |
  企业日报/周报自动生成。从MEMORY.md和daily log自动生成结构化报告，
  支持日报/周报/月报模板。
metadata:
  openclaw:
    emoji: "📊"
    category: "productivity"
    tags: ["report", "daily", "weekly", "automation", "chinese"]
---

# 企业日报/周报自动生成

## 功能概述

自动从工作记录生成结构化日报、周报、月报，告别手动整理。

## 使用方法

### 生成日报

```
帮我生成今天的日报
```

### 生成周报

```
帮我生成本周的周报
```

### 生成月报

```
帮我生成本月的月报
```

## 执行流程

### 日报生成

1. 读取今日工作记录（从`memory/YYYY-MM-DD.md`）
2. 提取完成事项、进行中事项、问题、明日计划
3. 按模板生成结构化日报
4. 保存到`~/reports/daily/YYYY-MM-DD.md`

### 周报生成

1. 读取本周7天的daily log
2. 汇总本周完成事项、待办事项、关键成果
3. 生成周报摘要
4. 保存到`~/reports/weekly/YYYY-WW.md`

### 月报生成

1. 读取本月所有daily log
2. 汇总月度成果、数据统计、问题复盘
3. 生成月报
4. 保存到`~/reports/monthly/YYYY-MM.md`

## 数据来源

- `MEMORY.md` — 长期记忆和任务清单
- `memory/YYYY-MM-DD.md` — 每日工作日志
- `memory/in_progress.md` — 进行中的任务

## 报告模板

### 日报模板

```markdown
# YYYY年MM月DD日 工作日报

## ✅ 今日完成
- [事项1]
- [事项2]

## 🚧 进行中
- [事项]（预计完成时间）

## ⚠️ 问题与风险
- [问题描述]

## 📅 明日计划
- [计划事项]
```

### 周报模板

```markdown
# YYYY年第WW周 工作周报

## 本周成果
- [成果1]
- [成果2]

## 数据统计
- 完成事项：X项
- 进行中：Y项
- 问题解决：Z项

## 问题与解决方案
- [问题描述] → [解决方案]

## 下周计划
- [计划事项]
```

## 输出位置

- 日报：`~/reports/daily/YYYY-MM-DD.md`
- 周报：`~/reports/weekly/YYYY-WW.md`
- 月报：`~/reports/monthly/YYYY-MM.md`

## 注意事项

- 需要定期维护daily log（记录每日工作）
- 报告质量取决于工作记录的完整性
- 建议每天下班前记录当日工作

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
