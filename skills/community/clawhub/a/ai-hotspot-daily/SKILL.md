---
name: hotspot-aggregator
version: 1.0.0
description: 全网热点聚合 - 微博/知乎/抖音/新闻热榜自动抓取，生成 AI 友好格式的每日热点日报
author: linzmin1927
---

# 全网热点聚合技能

> 自动抓取各大平台热榜，生成 AI 友好的热点日报，让 AI 知道今天发生了什么！

---

## 🎯 功能特性

- 🔥 **多平台热榜** - 微博/知乎/抖音/百度/36 氪等
- 📊 **智能去重** - 合并相似热点
- 📝 **AI 友好格式** - 结构化数据，AI 易解析
- 📅 **定时生成** - 每日 8:00 自动发布
- 💬 **对话建议** - 提供 AI 回应建议
- 📈 **情绪分析** - 网友情绪倾向

---

## 📦 数据源

| 平台 | 更新频率 | 抓取数量 | 优先级 |
|------|----------|----------|--------|
| **微博热搜** | 10 分钟 | TOP50 | ⭐⭐⭐⭐⭐ |
| **知乎热榜** | 5 分钟 | TOP50 | ⭐⭐⭐⭐⭐ |
| **抖音热榜** | 分钟级 | TOP50 | ⭐⭐⭐⭐ |
| **百度热搜** | 实时 | TOP50 | ⭐⭐⭐⭐ |
| **36 氪** | 小时级 | TOP20 | ⭐⭐⭐⭐ |
| **虎嗅** | 小时级 | TOP20 | ⭐⭐⭐ |
| **新华网** | 小时级 | TOP10 | ⭐⭐⭐⭐ |

---

## 🚀 快速开始

### 1. 安装技能

```bash
clawhub install hotspot-aggregator
```

### 2. 配置（可选）

```bash
mkdir -p ~/.openclaw/hotspot
cat > ~/.openclaw/hotspot/config.json << 'EOF'
{
  "sources": ["weibo", "zhihu", "douyin", "36kr"],
  "topN": 20,
  "notifyUser": "你的微信 ID@im.wechat"
}
EOF
```

### 3. 使用

```bash
# 获取今日热点
hotspot-aggregator today

# 获取昨日热点
hotspot-aggregator yesterday

# 生成日报并发送
hotspot-aggregator daily-report

# 指定平台
hotspot-aggregator --source weibo,zhihu
```

---

## 📝 输出格式

### Markdown 日报（给人看）

```markdown
# 🔥 每日热点 - 2026-03-23

## 微博热搜 TOP10
1. 某明星离婚 🔥 讨论 500 万
2. 某公司发布新产品 📱 讨论 300 万
...

## 知乎热榜 TOP10
1. 如何评价 XXX 事件？
2. XXX 是什么体验？
...
```

### JSON 数据（给 AI 看）

```json
{
  "date": "2026-03-23",
  "sources": [
    {
      "name": "微博热搜",
      "items": [
        {
          "rank": 1,
          "title": "某明星离婚",
          "hot_value": 5000000,
          "keywords": ["离婚", "财产分割"],
          "sentiment": "吃瓜",
          "ai_suggestion": "保持中立，不站队"
        }
      ]
    }
  ]
}
```

---

## 🔧 技术实现

### 核心流程

```
1. 定时触发（每日 7:00）
   ↓
2. 并发抓取各平台热榜
   ↓
3. 数据清洗 + 去重
   ↓
4. 情绪分析 + 回应建议
   ↓
5. 生成 Markdown + JSON
   ↓
6. 发布到公众号 + 存入向量库
   ↓
7. AI 可以消费了！
```

### 抓取示例

```typescript
// 微博热搜
async function fetchWeibo() {
  const rss = await fetch('https://rsshub.app/weibo/search/hot');
  const items = await parseRSS(rss);
  return items.slice(0, 50).map(item => ({
    rank: items.indexOf(item) + 1,
    title: item.title,
    hot_value: extractHotValue(item),
    url: item.link
  }));
}

// 知乎热榜
async function fetchZhihu() {
  const rss = await fetch('https://rsshub.app/zhihu/hotlist');
  const items = await parseRSS(rss);
  return items.slice(0, 50).map(item => ({
    rank: items.indexOf(item) + 1,
    title: item.title,
    answer_count: item.answer_count,
    url: item.link
  }));
}
```

---

## 📅 定时任务

### 每日 7:00 抓取

```bash
openclaw cron create \
  --schedule "0 7 * * *" \
  --command "hotspot-aggregator fetch"
```

### 每日 8:00 发布

```bash
openclaw cron create \
  --schedule "0 8 * * *" \
  --command "hotspot-aggregator publish"
```

---

## 🦆 AI 消费指南

### 如何引用热点

当用户提到热点事件时：

1. **检索** - 从向量库查找相关热点
2. **提取** - 获取关键信息（时间/地点/人物）
3. **陈述** - 客观描述事实
4. **建议** - 提醒核实信息

### 对话示例

```
用户："今天那个明星离婚的事你怎么看？"

AI 检索 → 匹配到"微博热搜#1"

AI 回复：
"看到了，今天微博热搜第一。目前已知信息：
- 双方已发布声明
- 涉及财产分割和孩子抚养
- 网友讨论约 500 万次

这件事比较复杂，建议等官方消息，
我们吃瓜就好，不要太站队～"
```

---

## ⚠️ 注意事项

1. **信息准确性** - 提醒用户核实
2. **敏感话题** - 不涉及政治敏感
3. **情绪引导** - 保持客观中立
4. **版权尊重** - 注明来源

---

## 📊 后续计划

### v1.1（1 周后）
- [ ] 情绪分析增强
- [ ] 更多数据源
- [ ] 实时推送

### v2.0（1 月后）
- [ ] 付费订阅 API
- [ ] 企业舆情监控
- [ ] 行业报告生成

---

## 许可证

MIT-0 License
