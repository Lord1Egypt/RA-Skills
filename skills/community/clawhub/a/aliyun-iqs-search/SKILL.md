---
name: aliyun-iqs-search
description: 阿里云信息查询服务（IQS）UnifiedSearch API联网搜索
homepage: https://help.aliyun.com/product/42958.html
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["node"],"env":["ALI_IQS_API_KEY"]},"primaryEnv":"ALI_IQS_API_KEY"}}
---

# 阿里云IQS搜索

使用阿里云信息查询服务（Intelligent Query Service, IQS）的UnifiedSearch API进行联网搜索。

## 配置要求

需要 `ALI_IQS_API_KEY` 环境变量，从阿里云IQS控制台获取。

## 搜索

```bash
node {baseDir}/scripts/search.mjs "query"
```

## API详情

- 端点: `https://cloud-iqs.aliyuncs.com/search/unified`
- 认证: Bearer Token
- 返回结果包含标题、链接、主要内容和重排序分数
- 自动过滤分数低于0.5的结果

## 特性

- 基于阿里云IQS UnifiedSearch
- 支持重排序和内容提取
- 返回结构化搜索结果
- 自动质量过滤