---
name: chill-beijing
description: 北京下班及周末放松推荐助手 v1.4.0。工作日推荐电影、脱口秀、演出；周末推荐City Walk、京郊游、社交活动、演出。实时抓取猫眼/大麦/美团/小红书数据。
version: 1.4.0
---

# Chill Beijing - 北京放松指南

北京打工人下班及周末去哪儿？实时抓取猫眼、大麦、美团、小红书最新数据，智能推荐。

## Features

- **实时数据抓取** - 猫眼、大麦、美团、小红书最新数据
- **智能分类** - 工作日/周末不同推荐策略
- **耐心等待** - 设置足够超时，确保数据完整抓取
- **最新日期** - 始终使用当日数据，拒绝历史/模拟数据

## Quick Start

```bash
# 获取今日推荐（自动判断工作日/周末）
node ~/.openclaw/skills/chill-beijing/scripts/generate-recommendations.mjs

# 强制获取工作日推荐
node ~/.openclaw/skills/chill-beijing/scripts/generate-recommendations.mjs --workday

# 强制获取周末推荐
node ~/.openclaw/skills/chill-beijing/scripts/generate-recommendations.mjs --weekend

# JSON 格式输出
node ~/.openclaw/skills/chill-beijing/scripts/generate-recommendations.mjs --json
```

## 推荐分类

### 工作日（周一-周四）
| 分类 | 数据源 | 内容 |
|------|--------|------|
| 🎬 电影 | 猫眼/美团 | 当日热映、评分、场次 |
| 🎤 脱口秀 | 大麦/美团 | 开放麦、专场演出 |
| 🎵 演出 | 大麦 | LiveHouse、音乐会、民谣酒馆 |

### 周五（工作日+周末预告）
输出工作日3类 + 周末4类完整推荐

### 周末（周六-周日）
| 分类 | 数据源 | 内容 |
|------|--------|------|
| 🚶 City Walk | 小红书 | 北京 city walk 路线推荐 |
| 🏔️ 京郊/周边游 | 小红书/美团 | 可过夜景点、民宿 |
| 👥 社交活动局 | 小红书 | 桌游、剧本杀、社交聚会 |
| 🎭 演出类 | 大麦/猫眼 | 话剧、演唱会、展览 |

## Data Sources

| 数据源 | 抓取内容 | 超时设置 |
|--------|---------|---------|
| 猫眼电影 | 当日上映电影、评分、场次 | 60秒 |
| 大麦网 | 北京站演出列表 | 60秒 |
| 美团演出 | 脱口秀、LiveHouse | 60秒 |
| 小红书 | City Walk、京郊游、社交局 | 60秒 |

## 技术特性

- **防反爬**：使用 Puppeteer 模拟真实浏览器
- **超时耐心**：单源 60 秒超时，失败自动重试
- **当日数据**：所有抓取带日期参数，确保最新
- **容错降级**：主源失败时使用备用源

## API Usage

```javascript
import { generateRecommendations, getTodayRecommendations } from './scripts/generate-recommendations.mjs';

// 获取今日推荐（自动判断工作日/周末）
const recs = await generateRecommendations();

// 获取结构化数据
const data = await getTodayRecommendations({ format: 'json' });
```

## Files

- `scripts/data-fetcher.mjs` - 数据抓取模块（猫眼/大麦/美团/小红书）
- `scripts/generate-recommendations.mjs` - 推荐生成主程序
- `scripts/formatters.mjs` - 数据格式化工具

## Changelog

### v1.0.0 (2026-03-27)
- 🎉 初始版本
- ✨ 工作日推荐：电影、脱口秀、演出
- ✨ 周末推荐：City Walk、京郊游、社交局、演出
- ✨ 多源数据抓取（猫眼/大麦/美团/小红书）
- ✨ 智能工作日/周末判断

## License

MIT
