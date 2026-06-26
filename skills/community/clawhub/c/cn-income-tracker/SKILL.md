---
name: income-tracker
description: 收入追踪器 - 多平台收入记录、统计分析、趋势图表。适用于自由职业者、创作者、副业者。
version: 1.0.0
author: clawd
tags:
  - income
  - finance
  - tracking
  - analytics
  - visualization
homepage: https://clawhub.com/skills/income-tracker
triggers:
  - "收入追踪"
  - "收入统计"
  - "收益记录"
  - "收入分析"
  - "income tracker"
  - "记录收入"
  - "收入报表"
  - "查看收入"
config:
  DATA_PATH:
    type: string
    required: false
    default: ~/clawd/data/income-tracker.json
    description: 收入数据存储路径
---

# Income Tracker 收入追踪器

一站式收入管理工具，帮助自由职业者、创作者、副业者追踪多平台收入，分析收益趋势。

## 核心功能

### 1. 收入记录
- 多来源收入录入（平台、项目、客户）
- 支持多币种（USD/CNY/USDT等）
- 自动汇率转换
- 备注和标签系统

### 2. 统计分析
- 日/周/月/年收入汇总
- 来源占比分析
- 环比增长率
- 收入预测

### 3. 图表展示
- 收入趋势折线图
- 来源分布饼图
- 月度对比柱状图
- 增长率可视化

## 使用示例

### 记录收入

```
记录收入 100 USDT 来自 a2a市场
记录收入 500 元 来自 外包项目:企业官网
添加收入 50 USD 来源 upwork 备注 logo设计
```

### 查看统计

```
查看本月收入
收入统计 本周
收入报表 2024年3月
收入趋势 最近30天
```

### 分析收入

```
收入来源分析
收入占比图表
收入增长率
预测下月收入
```

## API 调用

```javascript
// 添加收入记录
await handler({
  action: 'add',
  amount: 100,
  currency: 'USDT',
  source: 'a2a-market',
  note: '技能销售'
});

// 查询统计
await handler({
  action: 'stats',
  period: 'month',
  year: 2024,
  month: 3
});

// 获取趋势图
await handler({
  action: 'chart',
  type: 'trend',
  days: 30
});

// 来源分析
await handler({
  action: 'analyze',
  by: 'source'
});
```

## 数据存储

收入数据以 JSON 格式本地存储，支持：

- 自动备份
- 数据导出（CSV/JSON）
- 数据导入
- 云同步（可选）

### 数据结构

```json
{
  "records": [
    {
      "id": "inc_001",
      "amount": 100,
      "currency": "USDT",
      "source": "a2a-market",
      "date": "2024-03-20",
      "note": "技能销售",
      "tags": ["skill", "a2a"]
    }
  ],
  "sources": {
    "a2a-market": { "name": "A2A市场", "type": "platform" },
    "upwork": { "name": "Upwork", "type": "platform" }
  },
  "settings": {
    "baseCurrency": "CNY",
    "timezone": "Asia/Shanghai"
  }
}
```

## 支持的收入来源

### 平台类
- A2A Market
- Upwork
- Fiverr
- Freelancer
- ClawHub

### 项目类
- 外包项目
- 咨询服务
- 培训课程
- 技术支持

### 创作类
- 视频收益
- 文章打赏
- 付费课程
- 会员订阅

## 价格

- 基础功能：免费
- 高级分析：$2.99/月
- 团队版：$9.99/月

## 适合人群

- 自由职业者：管理多平台收入
- 内容创作者：追踪创作收益
- 副业者：记录副业收入
- 小团队：团队收入管理

## 快捷命令

| 命令 | 说明 |
|------|------|
| `收入` | 查看今日收入 |
| `收入+ 金额 来源` | 快速记录收入 |
| `月报` | 本月收入报表 |
| `趋势` | 收入趋势图 |

## 注意事项

1. 数据本地存储，定期备份
2. 支持手动编辑数据文件
3. 汇率使用实时接口
4. 敏感数据请加密存储

## 更新日志

### v1.0.0 (2024-03-20)
- 首次发布
- 支持收入记录、统计、图表
- 多币种支持
- 数据导出功能
