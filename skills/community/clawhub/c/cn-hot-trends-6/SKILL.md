---
name: cn-hot-trends
description: |
  中文全平台热搜聚合。一键获取知乎、微博、百度、B站、抖音、头条6大平台热搜榜单。
  中文优先，无需API Key，开箱即用。
  当用户说"热搜"、"热点"、"今日热点"、"什么火"、"热搜榜"、"全平台热搜"、"趋势"时触发。
  Keywords: 热搜, 热榜, 热点, 趋势, trending, hot search, 中文热搜, 全平台.
metadata: {"openclaw": {"emoji": "🔥"}}
---

# CN Hot Trends — 中文全平台热搜聚合

一键获取6大中文平台热搜榜单，AI选题+运营必备。

## 支持平台

| 平台 | 数据来源 | 默认条数 |
|------|---------|---------|
| 知乎 | 知乎热榜API | 10 |
| 微博 | 微博热搜API | 10 |
| 百度 | 百度热搜API | 10 |
| B站 | B站排行榜API | 10 |
| 抖音 | 抖音热榜API | 10 |
| 今日头条 | 头条热榜API | 10 |

## 快速开始

```bash
# 全平台热搜（默认各10条）
python3 scripts/fetch_trends.py

# 指定平台
python3 scripts/fetch_trends.py --platform zhihu

# 指定条数
python3 scripts/fetch_trends.py --platform weibo --limit 5

# 输出JSON
python3 scripts/fetch_trends.py --json

# AI选题推荐（基于热搜生成内容选题）
python3 scripts/fetch_trends.py --recommend
```

## 输出格式

### 文本模式（默认）
```
🔥 今日热搜速览（2026-04-12）

📍 知乎 | 10条
  1. 华为自离N+1回归  🔥335万
  2. 美国3月CPI创近两年最大涨幅  🔥236万
  ...

📍 微博 | 10条
  1. 男子微信群侮辱全红婵被拘  🔥106万
  ...

📊 AI选题推荐：
  1. 华为N+1回归→ 职场权益视角（知乎/公众号）
  2. CPI上涨 → 普通人应对策略（小红书）
```

### JSON模式
```json
[{
  "platform": "知乎",
  "title": "华为自离N+1回归",
  "heat": 3350000,
  "heat_display": "335万",
  "url": "https://...",
  "excerpt": "..."
}]
```

## AI选题推荐（--recommend）

基于热搜数据，自动生成：
1. **选题方向**：结合热度+平台特性推荐
2. **目标平台**：知乎/小红书/公众号匹配
3. **切入角度**：差异化建议

## 平台参数

`--platform` 可选值：`zhihu` `weibo` `baidu` `bilibili` `douyin` `toutiao` `all`（默认）

## 数据来源

所有数据均来自平台公开API，无需登录、无需API Key。

## 注意事项

- 部分平台API可能因地域限制不可用，脚本会自动跳过
- SSL证书问题已做双层降级处理（优先验证→失败回退）
- 不存储任何用户数据
