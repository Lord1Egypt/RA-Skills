---
name: 60s-api
description: 60s API 综合技能，提供每日新闻、AI资讯、热搜榜单、天气查询、数据查询、娱乐内容、媒体信息和实用工具。当用户询问新闻、热搜、天气、汇率、农历、笑话、运势、音乐排行、电影票房、翻译、IP查询等中文信息时触发。
license: MIT
metadata:
  author: vikiboss (original), merged by OpenClaw
  version: "1.1.0"
  api_base: https://60s.viki.moe/v2
  tags:
    - news
    - trending
    - weather
    - data
    - entertainment
    - utility
    - china
---

# 60s API 综合技能

基于 [60s API](https://60s.viki.moe) 的一站式中文信息查询技能，免费无需认证，所有接口通过 `curl` 调用。官方文档：https://docs.60s-api.viki.moe

## 全局约定

### 响应格式（encoding 参数）
除特殊说明，**所有接口**均支持 `encoding` query 参数控制返回格式：
- `json`（默认）— 程序化处理
- `text` — 纯文本，人类可读
- `markdown` — AI 友好

```bash
# 示例
curl -s "https://60s.viki.moe/v2/60s?encoding=markdown"
curl -s "https://60s.viki.moe/v2/weibo?encoding=text"
```

### 时间戳字段
涉及时间的字段有两种格式：
- **13位时间戳**：字段名含 `_at` 后缀（如 `updated_at`）
- **格式化字符串**：无后缀（如 `updated` → `"2025/01/13 07:22:32"`）

### 统一字段命名
- `link` — 链接/原文
- `cover` — 封面图/主图

### 响应结构
所有接口统一包裹：`{"code": 200, "message": "...", "data": ...}`
实际数据在 `data` 字段中。

### 国内备用实例
主域名 `60s.viki.moe` 部署在 Deno Deploy，部分地区可能被墙。备用：
- `60api.09cdn.xyz`
- `60s.zeabur.app`
- `60s.crystelf.top`
- `60s.tmini.net`
- `60s.7se.cn`

## 触发条件

当用户提到以下关键词时激活本技能：
- 新闻/AI资讯/今日要闻 → 周期资讯
- 热搜/热榜/微博/知乎/B站/抖音/小红书/豆瓣 → 热搜榜单
- 天气/天气预报/气温 → 天气查询
- 汇率/人民币/美元/金价/油价/农历/历史今天 → 数据查询
- 笑话/段子/运势/一言/摸鱼/KFC/发病文学/答案之书 → 娱乐内容
- 音乐排行/歌词/票房/电视剧/网剧/豆瓣 → 媒体信息
- 翻译/IP查询/二维码/密码/哈希/WHOIS/颜色 → 实用工具

---

## 📰 周期资讯

```bash
# 每天60秒读懂世界
curl -s "https://60s.viki.moe/v2/60s"
curl -s "https://60s.viki.moe/v2/60s?date=2024-01-15"          # 指定日期
curl -s "https://60s.viki.moe/v2/60s?encoding=markdown"        # Markdown格式
curl -sL "https://60s.viki.moe/v2/60s?encoding=image" -o news.png  # 图片

# AI 资讯快报
curl -s "https://60s.viki.moe/v2/ai-news"

# 必应每日壁纸
curl -sL "https://60s.viki.moe/v2/bing" -o bing.jpg

# 实时 IT 资讯
curl -s "https://60s.viki.moe/v2/it-news"

# 当日货币汇率
curl -s "https://60s.viki.moe/v2/exchange-rate?from=USD&to=CNY"

# 历史上的今天
curl -s "https://60s.viki.moe/v2/today-in-history"
curl -s "https://60s.viki.moe/v2/today-in-history?month=1&day=15"

# Epic Games 免费游戏（周更）
curl -s "https://60s.viki.moe/v2/epic"
```

### 60s新闻参数
| 参数 | 必填 | 说明 |
|------|------|------|
| date | 否 | YYYY-MM-DD，默认最新 |
| encoding | 否 | json(默认) / text / markdown / image / image-proxy |

### 60s新闻响应字段
```json
{
  "date": "2024-01-15", "day_of_week": "星期一", "lunar_date": "腊月初五",
  "news": [{"title": "...", "link": "..."}],
  "tip": "每日微语", "image": "https://..."
}
```

---

## 🔥 热搜榜单

```bash
# 社交平台
curl -s "https://60s.viki.moe/v2/weibo"           # 微博热搜
curl -s "https://60s.viki.moe/v2/zhihu"           # 知乎话题榜
curl -s "https://60s.viki.moe/v2/douyin"          # 抖音热搜
curl -s "https://60s.viki.moe/v2/toutiao"         # 头条热搜
curl -s "https://60s.viki.moe/v2/bili"            # 哔哩哔哩热搜
curl -s "https://60s.viki.moe/v2/rednote"         # 小红书热点
curl -s "https://60s.viki.moe/v2/quark"           # 夸克热点

# 百度系
curl -s "https://60s.viki.moe/v2/baidu/hot"       # 百度实时热搜
curl -s "https://60s.viki.moe/v2/baidu/teleplay"  # 百度电视剧榜
curl -s "https://60s.viki.moe/v2/baidu/tieba"     # 百度贴吧话题榜

# 其他
curl -s "https://60s.viki.moe/v2/dongchedi"       # 懂车帝热搜
curl -s "https://60s.viki.moe/v2/hacker-news/top" # Hacker News 热帖
curl -s "https://60s.viki.moe/v2/hacker-news/new" # Hacker News 最新
```

### 响应格式
```json
{
  "data": [
    {"title": "...", "url": "...", "热度": "1234567", "rank": 1}
  ],
  "update_time": "2024-01-15 14:00:00"
}
```

---

## 🌤️ 天气查询

```bash
# 实时天气（官方接口路径）
curl -s "https://60s.viki.moe/v2/weather?query=深圳"

# 天气预报
curl -s "https://60s.viki.moe/v2/weather/forecast?query=深圳"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| query | 是 | 中文城市/区名，如"北京"、"南山区" |

---

## 📊 数据查询

```bash
# 汇率
curl -s "https://60s.viki.moe/v2/exchange-rate?from=USD&to=CNY"

# 农历（开发中，可能不稳定）
curl -s "https://60s.viki.moe/v2/lunar?date=2024-01-15"

# 百科
curl -s "https://60s.viki.moe/v2/baike?keyword=Python"

# 油价
curl -s "https://60s.viki.moe/v2/fuel-price?province=广东"

# 金价
curl -s "https://60s.viki.moe/v2/gold-price"

# 奥运奖牌榜
curl -s "https://60s.viki.moe/v2/olympics"
```

---

## 🎵 媒体信息

### 音乐
```bash
curl -s "https://60s.viki.moe/v2/ncm-rank/list"        # 网易云榜单列表
curl -s "https://60s.viki.moe/v2/ncm-rank/3778678"     # 榜单详情（飙升榜）
curl -s -X POST "https://60s.viki.moe/v2/lyric" \
  -H "Content-Type: application/json" -d '{"keyword":"稻香 周杰伦"}'  # 歌词搜索
```

### 猫眼
```bash
curl -s "https://60s.viki.moe/v2/maoyan/all/movie"       # 全球票房总榜
curl -s "https://60s.viki.moe/v2/maoyan/realtime/movie"  # 实时电影票房
curl -s "https://60s.viki.moe/v2/maoyan/realtime/tv"     # 电视收视排行
curl -s "https://60s.viki.moe/v2/maoyan/realtime/web"    # 网剧实时热度
```

### 豆瓣（周更）
```bash
curl -s "https://60s.viki.moe/v2/douban/weekly/movie"          # 全球口碑电影榜
curl -s "https://60s.viki.moe/v2/douban/weekly/tv_chinese"     # 华语口碑剧集榜
curl -s "https://60s.viki.moe/v2/douban/weekly/tv_global"      # 全球口碑剧集榜
curl -s "https://60s.viki.moe/v2/douban/weekly/show_chinese"   # 华语口碑综艺榜
curl -s "https://60s.viki.moe/v2/douban/weekly/show_global"    # 全球口碑综艺榜
```

---

## 🎉 娱乐内容

```bash
curl -s "https://60s.viki.moe/v2/hitokoto"           # 随机一言
curl -s "https://60s.viki.moe/v2/hitokoto?category=anime"  # 按分类（anime/comic/game/literature/original/internet/other）
curl -s "https://60s.viki.moe/v2/duanzi"             # 随机段子
curl -s "https://60s.viki.moe/v2/dad-joke"           # 英文冷笑话
curl -s "https://60s.viki.moe/v2/luck"               # 随机运势
curl -s "https://60s.viki.moe/v2/kfc"                # KFC疯狂星期四文案
curl -sL "https://60s.viki.moe/v2/moyu" -o moyu.jpg  # 摸鱼日报（图片）
curl -s "https://60s.viki.moe/v2/fabing"             # 随机发病文学
curl -s "https://60s.viki.moe/v2/answer"             # 随机答案之书
curl -s "https://60s.viki.moe/v2/awesome-js"         # 随机 JS 趣味题
# 唱歌音频（音频文件）
curl -sL "https://60s.viki.moe/v2/changya" -o song.mp3
```

---

## 🛠️ 实用工具

```bash
# IP 查询
curl -s "https://60s.viki.moe/v2/ip"              # 本机IP
curl -s "https://60s.viki.moe/v2/ip?ip=8.8.8.8"   # 指定IP

# 翻译（支持109种语言）
curl -s -X POST "https://60s.viki.moe/v2/fanyi" -H "Content-Type: application/json" \
  -d '{"text":"Hello","from":"auto","to":"zh"}'
curl -s "https://60s.viki.moe/v2/fanyi/langs"     # 支持的语言列表

# 二维码
curl -sL "https://60s.viki.moe/v2/qrcode?text=https://example.com&size=300" -o qr.png

# 哈希/解压/压缩
curl -s -X POST "https://60s.viki.moe/v2/hash" -H "Content-Type: application/json" \
  -d '{"text":"hello","algorithm":"sha256"}'  # md5/sha1/sha256/sha512

# 网页 OG 元数据
curl -s -X POST "https://60s.viki.moe/v2/og" -H "Content-Type: application/json" \
  -d '{"url":"https://github.com"}'

# WHOIS
curl -s "https://60s.viki.moe/v2/whois?domain=github.com"

# 密码
curl -s "https://60s.viki.moe/v2/password?length=16&numbers=true&lowercase=true&uppercase=true&symbols=true"
curl -s "https://60s.viki.moe/v2/password/check?password=abc123"  # 密码强度检测

# 颜色工具
curl -s "https://60s.viki.moe/v2/color/random"      # 随机颜色/颜色转换
curl -s "https://60s.viki.moe/v2/color/palette"      # 配色方案/色彩搭配

# 身体健康分析
curl -s "https://60s.viki.moe/v2/health"

# 百度百科
curl -s "https://60s.viki.moe/v2/baike?keyword=Python"
```

---

## 📋 完整接口参考（50+）

### 周期资讯（7）
| 接口 | 方法 | 参数 | 说明 |
|------|------|------|------|
| /v2/60s | GET | date, encoding | 每天60秒新闻 |
| /v2/ai-news | GET | - | AI资讯快报 |
| /v2/bing | GET | - | 必应每日壁纸 |
| /v2/it-news | GET | - | 实时IT资讯 |
| /v2/exchange-rate | GET | from, to | 货币汇率 |
| /v2/today-in-history | GET | month, day | 历史上的今天 |
| /v2/epic | GET | - | Epic免费游戏 |

### 热搜榜单（11）
| 接口 | 方法 | 说明 |
|------|------|------|
| /v2/weibo | GET | 微博热搜 |
| /v2/zhihu | GET | 知乎话题榜 |
| /v2/douyin | GET | 抖音热搜 |
| /v2/toutiao | GET | 头条热搜 |
| /v2/bili | GET | 哔哩哔哩热搜 |
| /v2/rednote | GET | 小红书热点 |
| /v2/quark | GET | 夸克热点 |
| /v2/baidu/hot | GET | 百度实时热搜 |
| /v2/baidu/teleplay | GET | 百度电视剧榜 |
| /v2/baidu/tieba | GET | 百度贴吧话题榜 |
| /v2/dongchedi | GET | 懂车帝热搜 |
| /v2/hacker-news/{type} | GET | HN热帖（top/new/best） |

### 媒体信息（12）
| 接口 | 方法 | 说明 |
|------|------|------|
| /v2/ncm-rank/list | GET | 网易云榜单列表 |
| /v2/ncm-rank/{id} | GET | 网易云榜单详情 |
| /v2/lyric | POST | 歌词搜索 |
| /v2/maoyan/all/movie | GET | 猫眼全球票房总榜 |
| /v2/maoyan/realtime/movie | GET | 实时电影票房 |
| /v2/maoyan/realtime/tv | GET | 电视收视排行 |
| /v2/maoyan/realtime/web | GET | 网剧实时热度 |
| /v2/douban/weekly/movie | GET | 豆瓣全球口碑电影榜 |
| /v2/douban/weekly/tv_chinese | GET | 豆瓣华语口碑剧集榜 |
| /v2/douban/weekly/tv_global | GET | 豆瓣全球口碑剧集榜 |
| /v2/douban/weekly/show_chinese | GET | 豆瓣华语口碑综艺榜 |
| /v2/douban/weekly/show_global | GET | 豆瓣全球口碑综艺榜 |

### 实用功能（15）
| 接口 | 方法 | 参数 | 说明 |
|------|------|------|------|
| /v2/weather | GET | query | 实时天气 |
| /v2/weather/forecast | GET | query | 天气预报 |
| /v2/baike | GET | keyword | 百度百科 |
| /v2/fuel-price | GET | province | 汽油价格 |
| /v2/gold-price | GET | - | 黄金价格 |
| /v2/olympics | GET | - | 奥运奖牌榜 |
| /v2/moyu | GET | - | 摸鱼日报（图片） |
| /v2/lyric | POST | keyword | 歌词搜索 |
| /v2/whois | GET | domain | WHOIS查询 |
| /v2/qrcode | GET | text, size | 生成二维码 |
| /v2/fanyi | POST | text, from, to | 在线翻译 |
| /v2/fanyi/langs | GET | - | 翻译语言列表 |
| /v2/ip | GET | ip | 公网IP |
| /v2/og | POST | url | 链接OG信息 |
| /v2/hash | POST | text, algorithm | 哈希计算 |
| /v2/health | GET | - | 身体健康分析 |
| /v2/password | GET | length, numbers, lowercase, uppercase, symbols | 密码生成 |
| /v2/password/check | GET | password | 密码强度检测 |
| /v2/color/random | GET | - | 随机颜色/颜色转换 |
| /v2/color/palette | GET | - | 配色方案/色彩搭配 |
| /v2/lunar | GET | date | 农历（开发中） |

### 娱乐消遣（10）
| 接口 | 方法 | 说明 |
|------|------|------|
| /v2/hitokoto | GET | 随机一言 |
| /v2/duanzi | GET | 随机段子 |
| /v2/dad-joke | GET | 英文冷笑话 |
| /v2/luck | GET | 随机运势 |
| /v2/kfc | GET | KFC文案 |
| /v2/fabing | GET | 发病文学 |
| /v2/answer | GET | 答案之书 |
| /v2/awesome-js | GET | JS趣味题 |
| /v2/changya | GET | 唱歌音频 |

### 已废弃
| 接口 | 说明 |
|------|------|
| /v2/chemical | 化学元素查询（已失效） |

---

## 使用原则

1. 所有接口免费，无需 API Key
2. 优先使用 `curl` 通过 `exec` 调用
3. POST 请求：`curl -X POST ... -H "Content-Type: application/json" -d '{...}'`
4. 图片/音频接口用 `-sL ... -o file` 保存
5. 展示结果精简到 TOP 5~10
6. 出错时重试一次，仍失败告知用户
7. 天气查询仍以 Open-Meteo 为主（国际/精确数据），60s API 作为中文城市补充

## ⚠️ 重要注意事项

### 天气接口中文参数必须 URL 编码
Deno Deploy 拒绝 curl 直接拼接中文参数（返回 400），必须 URL 编码。使用 `curl -G --data-urlencode`：
```bash
# ❌ 错误（会返回 400）
curl -s "https://60s.viki.moe/v2/weather?query=深圳"

# ✅ 正确（curl -G 自动编码并附加到 URL）
curl -s -G "https://60s.viki.moe/v2/weather" --data-urlencode "query=深圳"
curl -s -G "https://60s.viki.moe/v2/weather/forecast" --data-urlencode "query=深圳"
```

### 天气接口返回数据非常丰富
包含：实时天气、空气质量（AQI/PM2.5等）、日出日落、20项生活指数（穿衣/洗车/运动/雨伞等）、预警信息、逐小时预报。展示时应精简，只取用户关心的信息。

## 相关资源

- API 实例：https://60s.viki.moe
- 官方文档：https://docs.60s-api.viki.moe
- GitHub：https://github.com/vikiboss/60s
- Skills 源码：https://github.com/vikiboss/60s-skills
