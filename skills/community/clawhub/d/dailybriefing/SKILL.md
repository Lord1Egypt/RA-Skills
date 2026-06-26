---
name: daily-briefing
description: Generate daily morning briefings with weather, traffic limits, and news. Provides structured data collection scripts for stable, reproducible briefing generation.
---

# Daily Briefing Skill

每日晨报生成工具，提供稳定、可复现的数据获取和简报生成能力。

## Features

- **稳定的数据获取** - 使用结构化脚本获取天气、限行，配合搜索获取新闻，减少随机性
- **新闻精选规则** - 共20条新闻，分类为：国际新闻5条、科技新闻5条、互联网5条、热点事件5条，自动过滤重复
- **本地缓存** - 30分钟数据缓存，避免重复请求
- **容错设计** - API 失败时提供备用数据
- **多种输出格式** - 支持文本、JSON、简化版等多种格式
- **全自动化** - 新闻由搜索+AI整理，无需手动筛选

## Quick Start

```bash
# 生成今日晨报（完整版，含天气+限行，新闻由AI搜索整理）
node scripts/generate-briefing.mjs

# 生成次日晨报
node scripts/generate-briefing.mjs --tomorrow

# 生成简化版（天气+限行，无新闻）
node scripts/generate-briefing.mjs --simple

# 生成无新闻版本
node scripts/generate-briefing.mjs --no-news

# JSON 格式输出
node scripts/generate-briefing.mjs --json
```

**完整晨报生成流程（推荐）**：

1. 执行脚本获取天气和限行：
```bash
node ~/.openclaw/skills/daily-briefing/scripts/generate-briefing.mjs --no-news
```

2. AI 使用 kimi_search 工具搜索新闻：
   - 搜索关键词：`国际新闻 {今日日期}`（5条）
   - 搜索关键词：`科技新闻 AI {今日日期}`（5条）
   - 搜索关键词：`互联网 产业 {今日日期}`（5条）
   - 搜索关键词：`今日热点 社会 {今日日期}`（5条）
   
   *注：{今日日期} 格式为"2026年3月27日"，根据实际日期动态替换*

3. AI 按规则整理新闻并生成完整简报

## API Usage

```javascript
import { generateBriefing, generateBriefingData } from './scripts/generate-briefing.mjs';

// 生成完整晨报（含新闻）
const briefing = await generateBriefing({
  city: 'Beijing',
  dayOffset: 0,  // 0=今天, 1=明天
  includeNews: true
});

// 生成结构化数据
const data = await generateBriefingData({ dayOffset: 0 });
```

## Data Sources

| 数据类型 | 来源 | 更新频率 | 方式 |
|---------|------|---------|------|
| 天气 | wttr.in API | 实时 | curl |
| 限行 | 本地规则配置 | 按周期更新 | 代码计算 |
| 新闻 | Kimi Search 实时搜索 | 实时 | 搜索+AI整理 |

## 新闻精选规则

简报新闻共 **20条**，按以下分类：

| 分类 | 条数 | 内容范围 |
|------|------|---------|
| 🌍 国际新闻 | 5条 | 国际政治、地缘冲突、全球经济 |
| 💻 科技新闻 | 5条 | AI、航天、芯片、科研突破 |
| 🌐 互联网/产业 | 5条 | 互联网大厂、AI应用、产业动态 |
| 🔥 热点事件 | 5条 | 国内时事、体育、社会热点 |

**过滤规则**：
- 自动过滤重复报道（同一事件只保留最权威来源）
- 过滤广告/推广内容
- 过滤与已有新闻高度相似的内容

## 北京限行规则（2025.12.29-2026.03.29）

| 星期 | 限行尾号 | 时间 | 范围 |
|------|---------|------|------|
| 周一 | 3和8 | 07:00-20:00 | 五环路以内 |
| 周二 | 4和9 | 07:00-20:00 | 五环路以内 |
| 周三 | 5和0 | 07:00-20:00 | 五环路以内 |
| 周四 | 1和6 | 07:00-20:00 | 五环路以内 |
| 周五 | 2和7 | 07:00-20:00 | 五环路以内 |
| 周末 | 不限行 | - | - |

## Cron Job Integration

配合 OpenClaw Cron 使用示例：

```json
{
  "id": "daily-briefing-morning",
  "agentId": "main",
  "name": "每日晨报-晨间",
  "schedule": {
    "kind": "cron",
    "expr": "0 15 7 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "生成每日晨报：\n\n1. 获取天气和限行数据：\n```bash\nnode /root/.openclaw/skills/daily-briefing/scripts/generate-briefing.mjs --no-news\n```\n\n2. 使用 kimi_search 搜索今日新闻（共20条）：\n   - 国际新闻 5条（关键词：国际新闻 全球 今日日期）\n   - 科技新闻 5条（关键词：科技新闻 AI 人工智能 今日日期）\n   - 互联网/产业 5条（关键词：互联网 产业 今日日期）\n   - 热点事件 5条（关键词：今日热点 社会 今日日期）\n\n3. 按以下规则整理：\n   - 过滤重复报道（同一事件只保留一条）\n   - 每条新闻配简短摘要（80字内）\n   - 按分类输出格式\n\n4. 合并天气+限行+新闻，生成完整简报"
  }
}
```

## 优势对比

| 维度 | 旧方式（纯AI生成） | 新方式（Skill+脚本） |
|------|------------------|-------------------|
| 天气准确性 | 依赖AI调用工具，可能失败 | ✅ 专用脚本，带缓存和容错 |
| 限行准确性 | AI可能记忆错误 | ✅ 代码化规则，准确计算 |
| 新闻时效性 | AI抓取可能遗漏 | ✅ 脚本化抓取，结构化分类 |
| 执行时间 | 不稳定（10-60秒） | ✅ 快速（3-10秒，有缓存） |
| 随机性 | 高 | ✅ 低（固定代码逻辑） |
| 可维护性 | 低（改提示语） | ✅ 高（改代码即可） |

## Files

- `scripts/data-collector.mjs` - 天气、限行数据获取
- `scripts/news-search.mjs` - 新闻搜索与分类整理模块
- `scripts/generate-briefing.mjs` - 简报生成主程序
- `.cache/` - 数据缓存目录（30分钟TTL）

## Changelog

### v1.2.0 (2026-03-27)
- ✨ 更新新闻获取方式：搜索+AI整理（替代原网页抓取）
- ✨ 新增新闻精选规则：20条 = 国际5+科技5+互联网5+热点5
- ✨ 新增自动去重和过滤机制
- 🔧 优化简报格式，分类更清晰

### v1.1.0 (2026-03-19)
- ✨ 新增新闻自动抓取功能（网易、新浪）
- ✨ 新闻自动分类（国际/国内/科技/财经/社会）
- ✨ 新增 `--no-news` 参数
- 🔧 优化缓存机制

### v1.0.0 (2026-03-19)
- 🎉 初始版本
- ✨ 天气数据获取（wttr.in）
- ✨ 限行规则代码化
- ✨ 简报生成功能

## License

MIT
