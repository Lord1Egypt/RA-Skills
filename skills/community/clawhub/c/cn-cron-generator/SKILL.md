name: Cron表达式生成器
version: "1.0.0"
description: "Cron表达式生成器。图形化配置定时任务，支持中文自然语言描述转Cron，可视化预览下次执行时间。纯Python标准库，无需API Key。"
license: MIT-0
tags:
  - tools


# Cron表达式生成器

Cron表达式生成器。将中文自然语言转为标准Cron表达式。

## 功能

- **中文转Cron**：「每天9点」→ `0 9 * * *`
- **Cron验证**：检查表达式是否合法
- **执行预览**：显示未来5次执行时间
- **常见模板**：每小时/每天/每周/每月快捷生成

## 安装要求

- Python 3.6+
- 无外部依赖

## 使用方法

```bash
# 中文描述生成
python3 scripts/cron_generator.py "每天早上9点"

# 验证Cron表达式
python3 scripts/cron_generator.py "0 9 * * 1-5"

# 查看下次执行时间
python3 scripts/cron_generator.py "0 */2 * * *"
```

## 示例

输入：`每天早上9点`
输出：`Cron: 0 9 * * *` + 未来5次执行时间

## 分类

开发工具

## 关键词

cron, 定时任务, 调度, scheduler, 自动化

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
