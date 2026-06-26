# 云厂商 API 契约

本文档记录 crawler 依赖的在线接口。API 字段映射变化时需同步更新。

## 设计说明

当前架构下，skill 主要使用各云厂商的**文档详情接口**（通过 doc_ref 精准抓取）。搜索/发现接口仍保留在代码中作为兜底，但推荐的工作流是由调用方（AI）通过浏览器收集文档 URL，再用 doc_ref 逐篇抓取。

## 统一输出字段

所有云厂商的详情抓取最终落到统一的 `Document` 结构：

| 字段 | 说明 |
| --- | --- |
| `url` | 文档完整 URL |
| `title` | 文档标题 |
| `content` | 纯文本内容（HTML 已解析） |
| `content_hash` | 内容 SHA256 哈希 |
| `last_modified` | 最后修改时间 |
| `metadata` | 云厂商特有字段（image_urls, product_id, doc_id 等） |

## 阿里云

| 项目 | 值 |
| --- | --- |
| 代码文件 | `src/crawler.py` |
| 详情接口 | `https://help.aliyun.com/help/json/document_detail.json` |
| doc_ref 格式 | alias 路径，如 `/vpc/product-overview/what-is-vpc` |
| 更新时间字段 | `lastModifiedTime`（毫秒时间戳） |
| 搜索接口（兜底） | `https://help.aliyun.com/help/json/search.json` |

## 腾讯云

| 项目 | 值 |
| --- | --- |
| 代码文件 | `src/tencent_crawler.py` |
| 详情接口 | `https://cloud.tencent.com/document/cgi/document/getDocPageDetail` |
| doc_ref 格式 | `product_id/doc_id`，如 `215/20046` |
| 更新时间字段 | 优先 `recentReleaseTime` |
| 搜索接口（兜底） | `https://cloud.tencent.com/portal/search/api/result/startup` |

## 百度云

| 项目 | 值 |
| --- | --- |
| 代码文件 | `src/baidu_crawler.py` |
| 详情接口 | `https://bce.bdstatic.com/p3m/bce-doc/online/{PRODUCT}/doc/{PRODUCT}/s/page-data/{slug}/page-data.json` |
| doc_ref 格式 | `PRODUCT/slug`，如 `VPC/qjwvyu0at` |
| 更新时间字段 | `fields.date` |
| 搜索接口（兜底） | `https://cloud.baidu.com/api/portalsearch` |

## 火山引擎

| 项目 | 值 |
| --- | --- |
| 代码文件 | `src/volcano_crawler.py` |
| 详情接口 | `https://www.volcengine.com/api/doc/getDocDetail` |
| doc_ref 格式 | `lib_id/doc_id`，如 `6401/70538` |
| 更新时间字段 | `UpdatedTime` |
| 搜索接口（兜底） | `https://www.volcengine.com/api/search/searchAll` |
| 特殊要求 | 需要 `x-use-bff-version: 1` 和 `referer` 请求头 |
