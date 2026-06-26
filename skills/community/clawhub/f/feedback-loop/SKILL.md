---
name: feedback-loop
version: 1.0.0
description: Feedback Loop - Collect, analyze, and act on user feedback for continuous agent improvement
author: OpenClaw
license: MIT
tags:
  - feedback
  - analytics
  - improvement
  - tracking
  - agent-optimization
cli:
  command: feedback-loop
  entry: bin/cli.js
dependencies: []
---

# Feedback Loop Skill

反馈循环器 - 一个完整的反馈收集、分析和改进跟踪系统，用于 OpenClaw 代理的持续优化。

## 功能概述

### 核心功能

1. **反馈收集（Feedback Collection）**
   - 显式反馈：用户主动评分、评论
   - 隐式反馈：从交互模式自动检测（完成、重试、放弃等）
   - 自动检测：基于会话模式智能识别反馈信号

2. **反馈分析（Feedback Analysis）**
   - 聚类分析：按类别、情感、评分分组
   - 趋势分析：时间序列趋势检测
   - 情感分析：正/负/中性情感分布
   - 模式检测：识别 recurring issues、行为模式等

3. **改进建议生成（Improvement Suggestions）**
   - 基于分析结果自动生成可执行的改进建议
   - 优先级排序（high/medium/low）
   - 包含具体 action items 和预期影响

4. **效果跟踪（Effect Tracking）**
   - 跟踪建议实施进度
   - 测量实施前后的影响
   - 生成综合报告

## 安装

```bash
# 通过 ClawHub 安装（推荐）
clawhub install feedback-loop

# 或手动安装
cd ~/.openclaw/workspace/skills/feedback-loop
npm install
npm link
```

## 使用方法

### CLI 命令

#### 1. 提供反馈（provide）

**显式反馈：**
```bash
feedback-loop provide --type explicit --rating 5 --comment "Excellent response!" --category accuracy
```

**隐式反馈：**
```bash
feedback-loop provide --type implicit --signal completion --sessionId sess123
feedback-loop provide --type implicit --signal retry --metrics '{"retryCount": 3}'
```

**参数说明：**
- `--type`: feedback 类型（explicit 或 implicit）
- `--rating`: 评分（1-5, thumbs_up, thumbs_down）
- `--comment`: 可选评论
- `--category`: 反馈类别（accuracy, speed, helpfulness 等）
- `--signal`: 隐式信号类型（completion, retry, abandon, correction 等）
- `--sessionId`: 会话标识符
- `--metrics`: JSON 格式的性能指标
- `--context`: JSON 格式的上下文信息

#### 2. 分析反馈（analyze）

```bash
# 分析最近一周的反馈
feedback-loop analyze --range week

# 只分析显式反馈
feedback-loop analyze --explicit-only

# 分析最近一个月的数据，输出 JSON
feedback-loop analyze --range month --output json
```

**参数说明：**
- `--range`: 时间范围（day, week, month, all）
- `--explicit-only`: 仅分析显式反馈
- `--output`: 输出格式（json, pretty）

#### 3. 生成建议（suggest）

```bash
# 生成最多 5 条建议
feedback-loop suggest --max 5

# 专注于特定类别
feedback-loop suggest --focus quality --max 10
```

**参数说明：**
- `--max`: 最大建议数量
- `--focus`: 专注的类别
- `--output`: 输出格式

#### 4. 跟踪进度（track）

```bash
# 跟踪建议实施进度
feedback-loop track fb_123456 --phase implementation --status in_progress

# 标记为已完成
feedback-loop track fb_123456 --phase deployed --status completed --notes "Successfully implemented"
```

**参数说明：**
- `--phase`: 实施阶段（planning, implementation, testing, deployed）
- `--status`: 状态（in_progress, completed, blocked）
- `--notes`: 附加说明
- `--metrics`: JSON 格式的进度指标

#### 5. 查看统计（stats）

```bash
feedback-loop stats
feedback-loop stats --output json
```

#### 6. 列出数据（list）

```bash
# 列出反馈
feedback-loop list feedback --limit 10
feedback-loop list feedback --type explicit

# 列出建议
feedback-loop list suggestions --status pending
feedback-loop list suggestions --category quality

# 列出跟踪记录
feedback-loop list tracking --phase implementation
```

#### 7. 生成报告（report）

```bash
feedback-loop report
feedback-loop report --output json
```

#### 8. 导出数据（export）

```bash
feedback-loop export --format json --output data.json
feedback-loop export --format csv --output data.csv
```

### 编程接口

```javascript
const FeedbackLoop = require('./src/index');

const fl = new FeedbackLoop();

// 提供反馈
fl.provide({
  type: 'explicit',
  rating: 5,
  comment: 'Great!',
  category: 'helpfulness'
});

// 分析
const analysis = fl.analyze({ timeRange: 'week' });

// 生成建议
const suggestions = fl.suggest({ maxSuggestions: 5 });

// 跟踪
fl.track(suggestionId, {
  phase: 'implementation',
  status: 'in_progress'
});

// 获取统计
const stats = fl.getStats();

// 获取报告
const report = fl.getReport();
```

## 触发方式

### 主动收集
- 在会话结束时自动请求评分
- 定期生成分析报告
- 检测到低满意度时触发改进流程

### 自动检测
- 高重试率 → 推断用户遇到困难
- 快速完成 → 推断用户满意
- 早期放弃 → 推断响应不符合期望
- 多次追问 → 推断高参与度

## 数据结构

### 反馈记录
```json
{
  "id": "fb_1234567890_abc123",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "type": "explicit",
  "sessionId": "sess_123",
  "rating": 5,
  "comment": "Excellent response!",
  "category": "accuracy",
  "metadata": {},
  "source": "cli"
}
```

### 隐式反馈
```json
{
  "id": "fb_1234567890_def456",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "type": "implicit",
  "sessionId": "sess_123",
  "signal": "completion",
  "metrics": { "responseTime": 2500 },
  "context": { "autoDetected": true },
  "inferredSentiment": "positive"
}
```

### 改进建议
```json
{
  "id": "fb_1234567890_ghi789",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "title": "Address recurring issues in accuracy",
  "description": "5 negative feedback items identified...",
  "category": "accuracy",
  "priority": "high",
  "actionItems": [...],
  "expectedImpact": "Reduce negative feedback...",
  "status": "pending"
}
```

## 最佳实践

1. **定期分析**：每周运行一次分析，及时发现趋势
2. **快速响应**：对高优先级建议立即采取行动
3. **持续跟踪**：记录每个建议的实施进度
4. **衡量影响**：实施后对比前后数据
5. **闭环管理**：确保每个反馈都有对应的改进行动

## 文件结构

```
feedback-loop/
├── SKILL.md           # 技能文档
├── package.json       # 项目配置
├── bin/
│   └── cli.js         # CLI 入口
├── src/
│   ├── index.js       # 主入口
│   ├── storage.js     # 数据存储
│   ├── collector.js   # 反馈收集
│   ├── analyzer.js    # 反馈分析
│   ├── suggester.js   # 建议生成
│   └── tracker.js     # 效果跟踪
├── data/              # 数据目录（自动生成）
│   ├── feedback.json
│   ├── analysis.json
│   ├── suggestions.json
│   └── tracking.json
└── test/
    └── run.js         # 测试脚本
```

## 注意事项

- 数据存储在 `data/` 目录下，定期备份重要数据
- 建议设置定期清理策略，避免数据文件过大
- 敏感反馈数据应注意隐私保护

## 版本历史

- **1.0.0** - 初始版本
  - 完整的反馈收集功能
  - 多维度分析能力
  - 智能建议生成
  - 效果跟踪系统
