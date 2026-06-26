---
name: aliyun-unified-search
description: Perform web searches using Alibaba Cloud Unified Search API. Returns relevant results with content snippets, scores, and metadata. Use this skill when the user needs to search the web for information, especially for Chinese content or when requiring time-filtered search results.
homepage: https://help.aliyun.com/zh/document_detail/2883041.html?spm=a2c4g.11186623.help-menu-2837261.d_4_0_2_3_0.153cda16tmvRJQ
---

# Aliyun Unified Search

使用阿里云统一搜索API进行网页搜索，获取相关结果、内容摘要和元数据。

## Authentication

设置环境变量：
```bash
export ALIYUN_IQS_API_KEY="your-api-key-here"
```

获取API-KEY：[创建并查看凭证](https://help.aliyun.com/zh/document_detail/2872258.html)

## Quick Start

### Using the Script

```bash
node {baseDir}/scripts/search.mjs "搜索问题"
node {baseDir}/scripts/search.mjs "搜索问题" --time-range OneWeek
node {baseDir}/scripts/search.mjs "搜索问题" --category finance
node {baseDir}/scripts/search.mjs "搜索问题" --time-range OneDay --category news
```

### Examples

```bash
# 基本搜索
node {baseDir}/scripts/search.mjs "云栖大会"

# 搜索最近一周的内容
node {baseDir}/scripts/search.mjs "AI人工智能" --time-range OneWeek

# 搜索金融类内容
node {baseDir}/scripts/search.mjs "股票市场" --category finance

# 搜索最近一天的新闻
node {baseDir}/scripts/search.mjs "科技新闻" --time-range OneDay --category news

# 输出原始JSON
node {baseDir}/scripts/search.mjs "杭州美食" --json
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--time-range <range>` | 时间范围: `OneDay`, `OneWeek`, `OneMonth`, `OneYear`, `NoLimit` | `NoLimit` |
| `--category <category>` | 查询分类: `finance`, `law`, `medical`, `internet`, `tax`, `news_province`, `news_center` | - |
| `--json` | 输出原始JSON | false |

## Time Range Options

| Value | Description |
|-------|-------------|
| `OneDay` | 1天内 |
| `OneWeek` | 1周内 |
| `OneMonth` | 1月内 |
| `OneYear` | 1年内 |
| `NoLimit` | 无限制（默认） |

## Category Options

| Value | Description |
|-------|-------------|
| `finance` | 金融 |
| `law` | 法律 |
| `medical` | 医疗 |
| `internet` | 互联网（精选） |
| `tax` | 税务 |
| `news_province` | 新闻省级 |
| `news_center` | 新闻中央 |

## Tips

- **尽可能将query限制在30个字符以内**，可以在调用接口前通过模型做Query改写
- **一般通用场景不要指定category**，会影响召回效果
- **engineType固定为Generic**，返回10条结果

## API Document Reference

详见参考文档：`https://help.aliyun.com/zh/document_detail/2883041.html?spm=a2c4g.11186623.help-menu-2837261.d_4_0_2_3_0.153cda16tmvRJQ`
