# 媒体源配置指南

## 目录
- [配置文件格式](#配置文件格式)
- [RSS源配置](#rss源配置)
- [常见媒体源示例](#常见媒体源示例)
- [配置文件示例](#配置文件示例)

## 概览
本指南说明如何配置媒体源数据，支持RSS订阅源、API接口等数据源。

## 配置文件格式

媒体源配置文件使用JSON格式，命名为 `sources.json`，放在当前工作目录下。

### 完整格式结构
```json
{
  "sources": [
    {
      "name": "来源名称",
      "url": "RSS源URL或API地址",
      "category": "分类",
      "type": "rss|api",
      "enabled": true
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `sources` | 数组 | 是 | 媒体源列表 |
| `name` | 字符串 | 是 | 来源名称，用于标识和显示 |
| `url` | 字符串 | 是 | RSS订阅地址或API接口地址 |
| `category` | 字符串 | 否 | 分类标签，如"科技"、"商业"等，默认"未分类" |
| `type` | 字符串 | 否 | 类型标识，默认"rss" |
| `enabled` | 布尔 | 否 | 是否启用该源，默认true |

## RSS源配置

### 如何获取RSS地址
1. 访问目标网站
2. 查找页面中的"RSS"、"订阅"、"Feed"链接
3. 复制RSS链接地址（通常以.xml或/rss结尾）

### 常见RSS路径
- `https://example.com/rss`
- `https://example.com/feed`
- `https://example.com/rss.xml`

## 常见媒体源示例

### 科技类媒体
```json
{
  "name": "36氪",
  "url": "https://36kr.com/feed",
  "category": "科技"
},
{
  "name": "TechCrunch",
  "url": "https://techcrunch.com/feed/",
  "category": "科技"
},
{
  "name": "InfoQ",
  "url": "https://www.infoq.cn/feed",
  "category": "技术"
}
```

### 商业财经
```json
{
  "name": "财新网",
  "url": "https://www.caixin.com/rss/",
  "category": "财经"
},
{
  "name": "虎嗅网",
  "url": "https://www.huxiu.com/rss/0.xml",
  "category": "商业"
}
```

### 综合新闻
```json
{
  "name": "BBC News",
  "url": "http://feeds.bbci.co.uk/news/rss.xml",
  "category": "综合"
},
{
  "name": "新华网",
  "url": "http://www.xinhuanet.com/politics/news_politics.xml",
  "category": "综合"
}
```

### 行业专业媒体
```json
{
  "name": "AI News",
  "url": "https://artificialintelligence-news.com/feed/",
  "category": "人工智能"
},
{
  "name": "The Verge",
  "url": "https://www.theverge.com/rss/index.xml",
  "category": "科技产品"
}
```

## 配置文件示例

### 示例1：简单配置（仅RSS源）
```json
{
  "sources": [
    {
      "name": "36氪",
      "url": "https://36kr.com/feed",
      "category": "科技"
    },
    {
      "name": "虎嗅网",
      "url": "https://www.huxiu.com/rss/0.xml",
      "category": "商业"
    },
    {
      "name": "InfoQ",
      "url": "https://www.infoq.cn/feed",
      "category": "技术"
    }
  ]
}
```

### 示例2：完整配置（包含禁用源）
```json
{
  "sources": [
    {
      "name": "36氪",
      "url": "https://36kr.com/feed",
      "category": "科技",
      "type": "rss",
      "enabled": true
    },
    {
      "name": "TechCrunch",
      "url": "https://techcrunch.com/feed/",
      "category": "科技",
      "type": "rss",
      "enabled": true
    },
    {
      "name": "暂不使用的源",
      "url": "https://example.com/feed",
      "category": "其他",
      "type": "rss",
      "enabled": false
    }
  ]
}
```

### 示例3：分类配置
```json
{
  "sources": [
    {
      "name": "36氪",
      "url": "https://36kr.com/feed",
      "category": "科技"
    },
    {
      "name": "财新网",
      "url": "https://www.caixin.com/rss/",
      "category": "财经"
    },
    {
      "name": "新华网",
      "url": "http://www.xinhuanet.com/politics/news_politics.xml",
      "category": "综合"
    },
    {
      "name": "AI News",
      "url": "https://artificialintelligence-news.com/feed/",
      "category": "人工智能"
    }
  ]
}
```

## 注意事项
1. 确保RSS源地址可访问且格式正确
2. 定期检查源是否失效，及时更新配置
3. 合理设置分类，便于后续智能体分析和整理
4. 避免配置过多源，影响收集效率
5. 遵守目标网站的使用条款和robots.txt规则
