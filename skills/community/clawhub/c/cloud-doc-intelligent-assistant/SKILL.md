---
name: cloud-doc-intelligent-assistant
version: 0.5.0
description: 多云文档抓取与存储工具，支持阿里云、腾讯云、百度云、火山引擎的产品文档抓取、本地存储、变更检测和跨云文档获取。本 skill 不调用大模型，只负责数据采集和 diff，总结、摘要、对比分析由调用方（客户端大模型）完成。当用户提问涉及阿里云、腾讯云、百度云、火山引擎中任意一个云厂商时，必须调用此 skill。如果用户提问涉及云产品功能但未指明具体云厂商（如"总结一下安全组"），需要先追问用户是哪个云厂商。
author: anthonybinaruth-dotcom
license: MIT
repository: https://github.com/anthonybinaruth-dotcom/cloud-doc-skill/tree/master
homepage: https://github.com/anthonybinaruth-dotcom/cloud-doc-skill
keywords:
  - documentation
  - cloud
  - monitoring
  - aliyun
  - tencent
  - baidu
  - volcano
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["python3"],"packages":["requests>=2.31.0","beautifulsoup4>=4.12.0","lxml>=4.9.0","sqlalchemy>=2.0.0","pyyaml>=6.0.0","click>=8.1.0"]}}}
runtime:
  language: python
  version: ">=3.10"
skills:
  - name: fetch_doc
    description: 抓取指定云厂商的单篇文档（doc_ref），或从本地数据库查询已存储的文档（product）
    entry: scripts/entry.py
    parameters:
      cloud: 云厂商标识（aliyun/tencent/baidu/volcano）
      product: 产品名称（可选，从本地数据库查询）
      doc_ref: 文档标识（可选，直接从 API 抓取）
      max_pages: product 模式最多返回篇数（默认 10）
      keyword: 额外搜索关键词（可选）
  - name: check_changes
    description: 从本地数据库读取已存储文档，重新抓取最新版本并对比变更
    entry: scripts/entry.py
    parameters:
      cloud: 云厂商标识
      product: 产品名称
      days: 检查最近 N 天（默认 7）
      max_pages: 最多检查篇数（默认 200）
      keyword: 额外搜索关键词（可选）
  - name: compare_docs
    description: 获取两个云厂商的产品文档原始内容，供调用方对比分析
    entry: scripts/entry.py
    parameters:
      left: 左侧文档配置（cloud + product 或 doc_ref）
      right: 右侧文档配置（cloud + product 或 doc_ref）
      focus: 对比关注点（可选，传递给调用方参考）
  - name: summarize_diff
    description: 对新旧版本文档进行 diff，返回变更类型和 diff 内容
    entry: scripts/entry.py
    parameters:
      title: 文档标题
      old_content: 旧版本内容
      new_content: 新版本内容
      focus: 关注重点（可选）
      url: 文档 URL（可选）
  - name: run_monitor
    description: 从本地数据库读取已存储文档，批量重新抓取检测变更，可推送通知
    entry: scripts/entry.py
    parameters:
      clouds: 云厂商列表
      products: 产品列表
      mode: 巡检模式（check_now/scheduled）
      days: 检查最近 N 天（默认 1）
      max_pages: 每个产品最多检查篇数（默认 50）
      send_notification: 是否发送通知（默认 false）
permissions:
  network:
    outbound:
      - https://help.aliyun.com/*
      - https://cloud.tencent.com/*
      - https://cloud.baidu.com/*
      - https://www.volcengine.com/*
      - ${AIFLOW_WEBHOOK_URL}
      - ${RULIU_WEBHOOK_URL}
    description: |
      访问云厂商公开文档 API 抓取文档内容。
      变更通知会发送到用户配置的 webhook 地址。
  filesystem:
    read:
      - config.yaml
    write:
      - data/*.db
      - logs/*.log
      - notifications/*.md
    description: |
      读取配置文件（config.yaml）。
      写入 SQLite 数据库（data/）、日志文件（logs/）和通知文件（notifications/）。
  environment:
    read:
      - AIFLOW_WEBHOOK_URL
      - RULIU_WEBHOOK_URL
      - CLOUD_DOC_MONITOR_LOAD_DOTENV
    description: |
      读取环境变量用于 webhook 配置。
security_notice: |
  ⚠️ 安全提示：
  1. 本 skill 不调用任何大模型 API，不会将文档内容发送到第三方 AI 服务。
  2. 文档内容存储在本地 SQLite 数据库中。
  3. 本工具使用云厂商的公开文档 API，无需认证，但请遵守合理使用原则。
  4. 默认请求间隔 1 秒，请勿设置过小的值。
  5. 如因不当使用导致 IP 被封禁，使用者需自行承担责任。
---

# 多云文档抓取工具

本 skill 负责从四大云厂商（阿里云、腾讯云、百度云、火山引擎）抓取产品文档，存储到本地 SQLite 数据库，并提供变更检测能力。

**核心设计原则：skill 只做数据采集和 diff，不调用大模型。总结、摘要、对比分析由调用方（客户端大模型）根据返回的原始文档内容自行完成。**

## 触发规则

1. 用户提问提到阿里云、腾讯云、百度云、火山引擎中任意一个 → **必须调用此 skill**
2. 用户提问涉及云产品功能但未指明云厂商（如"总结一下安全组"、"VPC 是什么"） → **先追问用户是哪个云厂商**，确认后再调用
3. 用户提到多个云厂商并要求对比 → 使用 `compare_docs` 获取两侧文档，自行对比分析
4. 用户要求巡检或监控 → 按"巡检流程"章节操作

## 安装

```bash
pip install .
# 或开发模式
pip install -r requirements.txt
```

安装后可用 `cloud-doc-skill` 命令，未安装时用 `python scripts/entry.py`。

## 调用格式

```bash
cloud-doc-skill <skill_name> '<params_json>'
# 或
python scripts/entry.py <skill_name> '<params_json>'
```

## 数据流

```
调用方（AI）通过浏览器收集文档 URL
    ↓
fetch_doc + doc_ref 逐篇抓取 → 存入本地 SQLite
    ↓
check_changes 从数据库读取 → 重新抓取 → 对比 diff → 返回变更列表
    ↓
compare_docs 获取两侧文档原始内容 → 返回给调用方
    ↓
调用方（AI）根据返回的原始内容自行总结、对比、生成报告
```

## Skills 详解

### fetch_doc — 抓取/查询文档

两种模式：

1. `doc_ref` 模式：从云厂商 API 实时抓取单篇文档，存入本地数据库
2. `product` 模式：从本地数据库按关键词查询已存储的文档（不发网络请求）

```bash
# doc_ref 模式 — 各云厂商格式
cloud-doc-skill fetch_doc '{"cloud": "aliyun", "doc_ref": "/vpc/product-overview/what-is-vpc"}'
cloud-doc-skill fetch_doc '{"cloud": "tencent", "doc_ref": "215/20046"}'
cloud-doc-skill fetch_doc '{"cloud": "baidu", "doc_ref": "VPC/qjwvyu0at"}'
cloud-doc-skill fetch_doc '{"cloud": "volcano", "doc_ref": "6401/70538"}'

# product 模式 — 从本地数据库查询
cloud-doc-skill fetch_doc '{"cloud": "aliyun", "product": "VPC"}'
cloud-doc-skill fetch_doc '{"cloud": "tencent", "product": "私有网络", "keyword": "子网"}'
```

参数：
- `cloud`（必填）：`aliyun` | `tencent` | `baidu` | `volcano`
- `doc_ref`：文档标识，直接从 API 抓取
- `product`：产品名称，从本地数据库查询
- `max_pages`：product 模式最多返回篇数（默认 10）
- `keyword`：额外搜索关键词

返回示例（doc_ref 模式）：
```json
{
  "machine": {
    "cloud": "aliyun",
    "mode": "doc_ref",
    "items": [
      {
        "title": "什么是专有网络",
        "url": "https://help.aliyun.com/zh/vpc/product-overview/what-is-vpc",
        "doc_ref": "https://help.aliyun.com/zh/vpc/product-overview/what-is-vpc",
        "content": "专有网络VPC（Virtual Private Cloud）是...",
        "last_modified": "2024-03-15T10:30:00"
      }
    ],
    "total": 1
  },
  "human": { "summary_text": "成功抓取 1 篇文档。" },
  "error": null
}
```

**调用方拿到 `content` 后，自行进行总结、摘要等操作。**

### check_changes — 检测变更

从本地数据库读取已存储的文档，逐篇重新抓取最新版本，与旧版本对比，返回变更列表和 diff。

**前提：需要先通过 `fetch_doc` + `doc_ref` 抓取过文档，数据库中有基线数据。**

```bash
cloud-doc-skill check_changes '{"cloud": "aliyun", "product": "vpc", "days": 7}'
cloud-doc-skill check_changes '{"cloud": "baidu", "product": "DNS", "days": 30}'
```

参数：
- `cloud`（必填）：云厂商标识
- `product`（必填）：产品名称（用于从本地数据库搜索）
- `days`：检查最近 N 天（默认 7）
- `max_pages`：最多检查篇数（默认 200）
- `keyword`：额外搜索关键词

返回示例：
```json
{
  "machine": {
    "cloud": "aliyun",
    "product": "vpc",
    "days": 7,
    "total_checked": 15,
    "changes": [
      {
        "change_type": "major",
        "title": "VPC 配额限制",
        "url": "https://help.aliyun.com/zh/vpc/...",
        "doc_ref": "https://help.aliyun.com/zh/vpc/...",
        "old_hash": "abc123",
        "new_hash": "def456",
        "diff": "--- old\n+++ new\n@@ -10,3 +10,5 @@\n..."
      }
    ],
    "fetch_errors": 0
  },
  "human": { "summary_markdown": "检查了 15 篇文档，最近 7 天内无变更。" },
  "error": null
}
```

**调用方拿到 `changes` 列表和 `diff` 后，自行生成变更摘要。**

### compare_docs — 获取两侧文档

获取两个云厂商的产品文档原始内容，返回给调用方进行对比分析。skill 本身不做对比。

```bash
# doc_ref 模式（推荐）
cloud-doc-skill compare_docs '{"left": {"cloud": "aliyun", "doc_ref": "/vpc/product-overview/what-is-vpc"}, "right": {"cloud": "tencent", "doc_ref": "215/20046"}}'

# product 模式（从本地数据库查询）
cloud-doc-skill compare_docs '{"left": {"cloud": "aliyun", "product": "vpc"}, "right": {"cloud": "tencent", "product": "私有网络"}, "focus": "能力差异"}'
```

参数：
- `left`（必填）：`cloud` + `product` 或 `doc_ref`
- `right`（必填）：`cloud` + `product` 或 `doc_ref`
- `focus`：对比关注点（传递给调用方参考）

返回示例：
```json
{
  "machine": {
    "left": { "cloud": "aliyun", "product": "vpc", "title": "什么是专有网络", "content": "..." },
    "right": { "cloud": "tencent", "product": "私有网络", "title": "私有网络概述", "content": "..." },
    "focus": "能力差异"
  },
  "human": { "summary_text": "已获取 aliyun/什么是专有网络 和 tencent/私有网络概述 的文档内容，请对比分析。" },
  "error": null
}
```

**调用方拿到两侧 `content` 和 `focus` 后，自行进行对比分析。**

### summarize_diff — 文档 Diff

对新旧两个版本的文档内容进行 diff，返回变更类型（minor/major/structural）和 diff 内容。

```bash
cloud-doc-skill summarize_diff '{"title": "VPC API 文档", "old_content": "旧版本...", "new_content": "新版本..."}'
```

参数：
- `title`（必填）：文档标题
- `old_content`（必填）：旧版本内容
- `new_content`（必填）：新版本内容
- `focus`：关注重点（可选）
- `url`：文档 URL（可选）

返回示例：
```json
{
  "machine": {
    "title": "VPC API 文档",
    "change_type": "major",
    "focus": null,
    "diff": "--- old\n+++ new\n...",
    "old_hash": "abc123",
    "new_hash": "def456"
  },
  "human": { "summary_text": "文档《VPC API 文档》发生了 major 级别的变更，请根据 diff 内容进行分析。" },
  "error": null
}
```

**调用方拿到 `diff` 和 `change_type` 后，自行生成变更摘要。**

### run_monitor — 批量巡检

从本地数据库读取已存储的文档，批量重新抓取检测变更，可推送通知。

```bash
cloud-doc-skill run_monitor '{"clouds": ["aliyun", "tencent", "baidu", "volcano"], "products": ["vpc"], "days": 1, "send_notification": true}'
```

参数：
- `clouds`（必填）：云厂商列表
- `products`（必填）：产品列表
- `mode`：`check_now`（默认）或 `scheduled`
- `days`：检查最近 N 天（默认 1）
- `max_pages`：每个产品最多检查篇数（默认 50）
- `send_notification`：是否发送通知（默认 false）

## 巡检流程（调用方必读）

巡检时，**不要直接调用 run_monitor**，按以下流程操作：

### 第一步：确定百度云的产品子功能

用户指定要巡检的产品大类（如 VPC / CSN / DNS / VPN），用浏览器访问百度云文档侧边栏，列出子功能清单。

**为什么以百度云为基准？** 其他云厂商的部分子功能可能是独立产品（如阿里云弹性网卡是独立产品 ENI），百度云的产品划分相对集中，适合作为基准。

### 第二步：映射到其他三个云厂商

用浏览器访问阿里云、腾讯云、火山引擎的文档，找到对应的产品/功能页面。

| 百度云子功能 | 阿里云 | 腾讯云 | 火山引擎 |
| --- | --- | --- | --- |
| VPC 基础 | vpc | 私有网络 | 私有网络 |
| 弹性网卡 | eni（独立产品） | 弹性网卡（独立产品） | 私有网络（弹性网卡章节） |
| 高可用虚拟IP | vpc（HAVIP章节） | 高可用虚拟IP | 私有网络（HAVIP章节） |

### 第三步：收集文档 URL

用浏览器访问各云厂商文档页面，从侧边栏收集所有文档 URL。

### 第四步：逐篇抓取

```bash
cloud-doc-skill fetch_doc '{"cloud": "baidu", "doc_ref": "VPC/qjwvyu0at"}'
cloud-doc-skill fetch_doc '{"cloud": "aliyun", "doc_ref": "/vpc/product-overview/what-is-vpc"}'
# ... 每次调用间隔 ≥ 1 秒
```

### 第五步：分析和报告

- `check_changes` 检测变更 → 调用方根据 diff 生成变更摘要
- `compare_docs` 获取两侧文档 → 调用方进行对比分析
- `run_monitor` 汇总 + 发送通知

### 流程总结

```
用户指定产品大类
  → 浏览器访问百度云文档，列出子功能清单
  → 浏览器映射到其他三云
  → 浏览器收集侧边栏文档 URL
  → fetch_doc 逐篇抓取（doc_ref，间隔 ≥ 1秒）
  → check_changes / compare_docs 获取数据
  → 调用方自行总结、对比、生成报告
  → run_monitor 发送通知
```

## doc_ref 格式说明

各云厂商的 doc_ref 格式不同，从文档 URL 中提取：

| 云厂商 | URL 格式 | doc_ref 格式 | 示例 |
| --- | --- | --- | --- |
| 阿里云 | `help.aliyun.com/zh/{path}` | URL 路径 | `/vpc/product-overview/what-is-vpc` |
| 腾讯云 | `cloud.tencent.com/document/product/{pid}/{did}` | `product_id/doc_id` | `215/20046` |
| 百度云 | `cloud.baidu.com/doc/{PRODUCT}/s/{slug}` | `PRODUCT/slug` | `VPC/qjwvyu0at` |
| 火山引擎 | `volcengine.com/docs/{lib_id}/{doc_id}` | `lib_id/doc_id` | `6401/70538` |

## 支持的云厂商

| 云厂商 | cloud 值 | 产品标识格式 | 示例 |
| --- | --- | --- | --- |
| 阿里云 | `aliyun` | alias 路径 | `vpc`、`ecs`、`dns` |
| 腾讯云 | `tencent` | 中文产品名 | `私有网络`、`VPN 连接` |
| 百度云 | `baidu` | 大写产品代码 | `VPC`、`DNS`、`CSN` |
| 火山引擎 | `volcano` | 中文产品名 | `私有网络`、`NAT网关` |

## 返回结构

所有 skill 返回统一 JSON：

```json
{
  "machine": { ... },
  "human": { "summary_text": "..." },
  "error": null
}
```

- `machine`：结构化数据，包含文档内容、变更列表、diff 等
- `human`：简短的人类可读文本
- `error`：正常为 `null`，出错时包含 `code` 和 `message`

错误码：`MISSING_PARAM` | `INVALID_PARAM` | `CRAWL_FAILED`

## 配置

`config.yaml` 核心配置：

```yaml
crawler:
  request_delay: 1.0  # 请求间隔（秒），建议 1-2 秒
  max_retries: 2
  timeout: 15

storage:
  db_path: "./data/docs.db"

notifications:
  - type: "file"
    enabled: true
    output_dir: "./notifications"
```

## 速率控制

- `fetch_doc`（doc_ref）和 `check_changes` 会发起网络请求，遵守 request_delay
- `fetch_doc`（product）和 `compare_docs`（product）从本地数据库读取，无网络请求
- 巡检时由调用方控制调用频率，建议每次 fetch_doc 间隔 ≥ 1 秒
- 如遇 429/403 错误，增加 request_delay
