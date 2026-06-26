---
name: "content-summary"
version: "1.0.0"
description: "智能内容总结和项目复盘工具"
author: "AI Skills Team"
tags: ["总结", "复盘", "分析", "报告"]
requires: []
---

# AI总结复盘技能

智能内容总结和项目复盘工具，支持多种内容类型。

## 技能描述

提供日报、会议、项目、文章等多种内容的自动总结和复盘功能。提取关键要点、计算目标达成率、识别成功经验和问题。

## 使用场景

- 用户："总结今天的日报" → 提取关键任务和完成情况
- 用户："复盘这个项目" → 分析目标达成率和经验教训
- 用户："总结这篇文章" → 提取主要观点和论据
- 用户："整理会议记录" → 提取决策和行动项

## 工具和依赖

### 工具列表

- `scripts/summary_review.py`：核心总结复盘模块

### API密钥

无（基础版本）

### 外部依赖

- Python 3.7+（仅使用标准库）

## 配置说明

### 支持的内容类型

| 类型 | 说明 | 特殊字段 |
|------|------|----------|
| daily | 日报/工作日志 | completed_tasks, issues |
| meeting | 会议记录 | agenda, decisions, action_items |
| project | 项目总结 | goals, achievements, lessons |
| article | 文章总结 | main_idea, key_arguments |
| general | 通用内容 | key_points, summary |

### 数据存储位置

数据库：`~/.ai_summary.db`

## 使用示例

### 基本用法

```python
from summary_review import AISummaryReview

system = AISummaryReview()

# 内容总结
summary = system.summarize_content(daily_content, 'daily', '工作日报')

# 项目复盘
review = system.review_project(project_data)
```

### 场景1：日报总结

用户："总结我今天的工作"
内容：
```
今天完成了用户模块的开发，修复了3个bug。
遇到了数据库连接问题，已经解决。
明天计划开始订单模块的开发。
```

AI：
```python
summary = system.summarize_content(content, 'daily', '工作日报')
# 返回：关键任务、问题、计划
```

### 场景2：项目复盘

用户："复盘AI助手项目"

AI：
```python
project_data = {
    'name': 'AI助手项目',
    'goals': ['实现对话功能', '添加知识库', '支持多语言'],
    'results': ['对话功能已实现', '知识库完成80%', '中文支持已完成'],
    'metrics': {'用户满意度': 85, '响应时间': 1.2}
}
review = system.review_project(project_data)
# 返回：目标达成率、成功经验、问题识别、改进建议
```

### 场景3：文章总结

用户："总结这篇技术文章"

AI：
```python
summary = system.summarize_content(article_content, 'article', '文章标题')
# 返回：主要观点、关键论据、结论
```

### 场景4：导出Markdown

用户："导出总结为Markdown文件"

AI：
```python
output_path = system.export_to_markdown(summary_id, "output.md")
# 生成格式化的Markdown文件
```

## 复盘维度

项目复盘包含以下维度：

1. **目标达成率**：自动计算目标完成百分比
2. **成功经验**：提取已达成目标的亮点
3. **问题识别**：发现未达成目标和指标异常
4. **改进建议**：基于分析生成具体建议
5. **下一步计划**：自动生成后续行动计划

## 故障排除

### 问题1：总结不够精准

**现象**：提取的关键点不够准确

**解决**：
- 基础版本使用规则提取，可考虑升级到AI增强版（技能06）
- 或使用更清晰的输入格式，分段明确

### 问题2：数据库文件过大

**现象**：历史记录太多，数据库文件大

**解决**：
- 定期清理旧记录
- 或导出重要总结为Markdown后删除数据库记录

### 问题3：导出格式不符合要求

**现象**：Markdown格式需要调整

**解决**：
- 可以编辑导出的Markdown文件
- 或使用自定义模板功能

## 注意事项

1. **总结方式**：基于关键词和句子结构，可能不够精准
2. **复盘建议**：是通用模板，需要根据实际情况调整
3. **人工判断**：建议结合人工判断，不完全依赖自动化
4. **定期清理**：定期清理历史记录，避免数据库过大
5. **AI增强**：如需更强大的总结能力，可使用技能06（AI总结增强版）
