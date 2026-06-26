---
name: douyin-scraper
description: 爬取抖音热榜和搜索建议数据，支持关键词搜索、热榜获取、搜索建议等功能。无需登录即可使用。
version: 2.0.0
---

# 抖音爆款爬虫 Skill

## 功能概述

获取抖音热榜和搜索数据。当前版本使用抖音 Web API，**无需登录**。

## 功能特性

- 🔥 **热榜获取** - 获取当前抖音热搜榜 (无需登录)
- 🔍 **关键词搜索** - 在热榜中匹配关键词 + 获取搜索建议 (无需登录)
- 💡 **搜索建议** - 获取关键词联想 (无需登录)

## ⚠️ 重要说明

抖音搜索 API 需要登录态，当前版本在**无登录**环境下使用以下替代方案：
- 热榜 API：直接获取当前热搜话题
- 搜索建议 API：获取关键词联想
- 搜索时：先在热榜中匹配，再补充搜索建议

如需完整搜索功能，需要提供抖音登录 Cookie。

## 安装

```bash
cd <skill-dir>
npm install
```

Playwright 浏览器（可选，用于完整搜索）:
```bash
npx playwright install chromium
```

## 使用方法

### Node.js 版本

```bash
# 搜索关键词
node scripts/douyin_scraper.js search "海鲜" 20

# 获取热榜
node scripts/douyin_scraper.js hot 50

# 获取搜索建议
node scripts/douyin_scraper.js suggest "海鲜售卖"

# 保存到文件
node scripts/douyin_scraper.js search "海鲜" 10 --output result.json
```

### Python 版本

```bash
# 搜索关键词
python scripts/scraper.py search --keyword "海鲜" --limit 20

# 获取热榜
python scripts/scraper.py hot --limit 50

# 获取搜索建议
python scripts/scraper.py suggest --keyword "海鲜售卖"
```

## 自然语言处理指南

当用户用自然语言请求抖音相关数据时，按以下规则解析：

### 搜索意图识别

| 用户说法 | 意图 | 命令 |
|---------|------|------|
| 搜索一下海鲜视频 / 找一些海鲜视频 | 搜索 | `search "海鲜"` |
| 看看抖音热榜 / 抖音最近什么火 | 热榜 | `hot` |
| 海鲜相关的搜索建议 | 建议 | `suggest "海鲜"` |
| 海鲜售卖视频文案 | 搜索 | `search "海鲜售卖"` |
| 分析这个视频链接 xxx | 暂不支持 | 提示用户 |

### 关键词提取

从自然语言中提取关键词：
- "搜索一下**海鲜**视频" → 关键词: `海鲜`
- "找一些**海鲜售卖**相关的视频" → 关键词: `海鲜售卖`
- "**小龙虾**怎么做" → 关键词: `小龙虾`
- "最近**美食**领域什么火" → 关键词: `美食` (搜索热榜匹配)

### 执行流程

1. 解析用户意图 (搜索/热榜/建议)
2. 提取关键词
3. 执行对应命令
4. 格式化展示结果

## 输出数据格式

### 搜索结果

```json
{
  "keyword": "海鲜",
  "matched_hot": [
    {
      "rank": 1,
      "word": "海鲜话题",
      "hot_value": 5000000,
      "video_count": 10
    }
  ],
  "suggestions": [
    { "word": "海鲜小哥", "group_id": "xxx" }
  ],
  "hot_list": [...],
  "note": "在热榜中找到 1 个匹配话题"
}
```

### 热榜数据

```json
[
  {
    "rank": 1,
    "word": "热搜话题",
    "hot_value": 12000000,
    "video_count": 6,
    "group_id": "xxx",
    "sentence_id": "xxx"
  }
]
```

## 注意事项

1. **请求频率** - 避免频繁调用，建议间隔 >5 秒
2. **数据用途** - 仅供学习和研究
3. **API 限制** - 搜索 API 需登录，热榜和建议 API 无需登录
4. **IP 风控** - 异常请求可能导致 IP 被限

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| API 返回 2483 | 搜索需要登录，使用 `hot` 或 `suggest` 替代 |
| 网络超时 | 检查网络连接，重试 |
| 无匹配结果 | 关键词可能不在热榜，尝试 `suggest` 获取相关词 |
