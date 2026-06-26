---
name: daily-viz
description: Daily life tracking and data visualization. Record mood, exercise, sleep, work hours and generate beautiful charts and insights. Perfect for habit building and self-improvement.
version: 1.0.0
author: 军哥
tags: [tracking, visualization, habits, productivity, health]
---

# Daily Viz - 日常可视化

## 功能

### 1. 快速记录
```
/记录 心情:开心 运动:30分钟 睡眠:8小时 工作:6小时
/打卡 早起
/心情 😊
```

### 2. 查看数据
```
/查看 本周心情
/查看 本月运动统计
/查看 睡眠趋势
```

### 3. 生成报告
```
/报告 周度
/报告 月度 --export pdf
/分享 本周成就
```

### 4. 智能建议
```
/分析 我的作息规律
/建议 如何改善睡眠质量
```

## 数据存储

所有数据保存在 `~/.daily-viz/data/` 目录，支持：
- 本地 JSON 存储
- 可选的云同步（高级版）
- 数据导出/导入

## 隐私

- 所有数据本地存储
- 不上传任何个人信息
- 支持数据加密（高级版）
