---
name: batch-search-monitor
description: 批量搜索监控 - 关键词定时搜索、结果告警、数据导出
---

# Batch Search Monitor

定时监控关键词搜索结果，自动告警，支持数据导出。

## 功能

- ✅ 多关键词批量监控
- ✅ 定时自动搜索
- ✅ 结果变化告警
- ✅ 数据导出 (CSV/Excel)
- ✅ 支持 8 个中文搜索引擎

## 使用

```bash
# 添加监控任务
clawhub monitor add --keywords "AI 技能，ClawHub" --engine "baidu" --interval 60

# 查看监控任务
clawhub monitor list

# 导出结果
clawhub monitor export --task-id 1 --format csv

# 删除任务
clawhub monitor remove --task-id 1
```

## 示例

### 监控竞品动态

```bash
clawhub monitor add \
  --keywords "竞品公司名" \
  --engine "bing-cn" \
  --interval 120 \
  --notify true
```

### 监控品牌提及

```bash
clawhub monitor add \
  --keywords "我的品牌" \
  --engine "sogou-wechat" \
  --interval 60 \
  --notify true
```

## 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 1 个任务，60 分钟间隔 |
| Pro 版 | ¥99 | 10 个任务，10 分钟间隔 |
| 订阅版 | ¥29/月 | 无限任务，5 分钟间隔 + 邮件告警 |
