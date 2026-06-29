---
name: chukonu-search-patent
version: 1.0.0
description: "专利搜索：通过 Chukonu remote MCP server 检索中国(CNIPA)与欧洲(EPO)专利。支持标题/摘要/权利要求/全文布尔查询、IPC 五级分类、申请人/发明人、专利类型、日期与引证数值范围等字段化高级检索，单篇取著录项/权项/全文。只读、OAuth 登录、强制分页。"
tags: [patent, search, ip, mcp, cnipa, epo, prior-art]
metadata:
  transport: streamable-http
  requires:
    mcp:
      - name: chukonu
        url: "https://search.houdutech.cn/mcp/"
        transport: streamable-http
        auth: oauth
  setup:
    - "openclaw mcp add chukonu --url https://search.houdutech.cn/mcp/ --transport streamable-http --auth oauth"
    - "openclaw mcp login chukonu"
---

# chukonu-search-patent

通过 Chukonu 的 **remote MCP server** 检索专利。本 skill 不调用本地二进制，也不需要 API key —— 它把
OpenClaw 接到托管的 `chukonu` MCP server（OAuth 登录，只读检索）。

## 一次性接入（首次使用前）

```bash
openclaw mcp add chukonu \
  --url https://search.houdutech.cn/mcp/ \
  --transport streamable-http \
  --auth oauth
openclaw mcp login chukonu      # 弹浏览器完成 OAuth（Google 或 WeChat），token 由 host 保管
```

接入后会出现 3 个只读 tool：`patent_search`、`fetch`、`usage`。

## 何时使用本 skill

- 检索特定主题/技术的专利（关键词或一段技术描述）
- 已知申请号取著录项 / 权利要求 / 全文
- 按 IPC 分类、年份、申请人/发明人、专利类型、引证次数等结构化筛选

不适用于：网页/新闻/学术论文搜索（本服务第一版只做专利）。

## 工具

### 1. `patent_search` —— 唯一检索入口

简单关键词（自由文本快路径，等价标题+摘要+权利要求 `tiabc`）：

```
patent_search(query="图像识别 OR 深度学习", size=10)
```

高级检索：叠加下列字段化参数（任意组合，至少一个搜索字段；`query` 与 `tiabc` 互斥）。文本字段支持 `OR` 布尔。

| 类别 | 参数 |
|---|---|
| 文本（支持 OR） | `title` 标题 · `abstract_content` 摘要 · `claim` 权利要求 · `title_abstract_content` · `tiabc`(标题+摘要+权项) · `full`(全文) |
| IPC 五级 | `class_ipc`(精确, 如 `G06T11/60`) · `class_ipc_main` 主分类 · `class_ipc_section`(`G`) · `class_ipc_class`(`G06`) · `class_ipc_subclass`(`G06F`) · `class_ipc_group`(`G06F17`) |
| 主体 | `ap` 原始申请人 · `first_ap` 第一申请人 · `inventor` 发明人 · `first_in` 第一发明人 |
| 号 & 类型 | `an` 申请号 · `pn` 公开号 · `patent_type`(逗号分隔; A=发明申请 B=发明授权 U=实用新型 F=外观设计) |
| 范围 | `application_date='[YYYYMMDD TO YYYYMMDD]'`(`*` 表开放端) · `no_ap`/`no_in`/`citation_number_of_times`/`citation_forward_number_of_times='X'` 或 `'X TO Y'` |
| 兜底 | `extra={...}` 透传未在 schema 暴露的字段（province/city/publication_date 等） |
| 分页 | `size` 默认 20、上限 100 · `cursor` 来自上一次响应的 `next_cursor` · `dataset='cn_abstract'`(默认) 或 `'epo_docdb'` |

示例：

```
patent_search(class_ipc_main="G06F OR G06N", first_ap="华为技术有限公司",
              application_date="[20200101 TO 20231231]", patent_type="A,B", size=10)
```

单条结果 `metadata` 含**全著录项**（IPC 五级 / 申请人 / 发明人 / 各类日期 / 引证计数 / 公开号·申请号 …），
但**不含 claims / 全文**——取全文用 `fetch`。给用户呈现时建议保留：申请号、标题、申请人、申请日、IPC、公开号、score。

### 2. `fetch` —— 取单篇文档体

```
fetch(id="patent:cn_abstract:CN202510299981.2", part="record")
```

- `id` 形如 `patent:<dataset>:<application_number>`，直接用 `patent_search` 结果里的 `id`。
- `part`：`record`(默认，全著录项，无 claims) / `claims`(权项文本，强制分页，重传 `next_cursor` 取下一段) /
  `description` / `fulltext`（待全文/PDF 语料，当前返回 `null`+note）。`pdf_url` 字段恒在（当前 `null`）。

### 3. `usage` —— 查配额

```
usage()
```

返回 `{quota_total, used, remaining, reset_at_utc, reset_in_seconds}`。长 agent run 里建议先查一次，
临近 `QUOTA_EXCEEDED` 提前收手。

## 决策准则

- 用户给主题词/技术描述 → `patent_search(query=…)`，必要时叠加 `patent_type` / `application_date` / `class_ipc_main`
- 用户给结构化条件（申请人/发明人/IPC/日期/引证）→ `patent_search` 对应字段组合
- 用户给申请号 → 先 `fetch(id="patent:<dataset>:<an>", part="record")`；要权项再 `part="claims"`
- 召回很多时用 `next_cursor` 翻页，而不是反复换词重搜

## 错误处理

| code | 应对 |
|---|---|
| `UNAUTHORIZED` | 重跑 `openclaw mcp login chukonu` 重新授权 |
| `QUOTA_EXCEEDED` | 已达每日配额；告知用户 `retry_after`/次日重置，或先 `usage()` 确认 |
| `INVALID_ARGUMENT` / `INVALID_QUERY_SYNTAX` | 核对字段名/格式（日期 `[YYYYMMDD TO YYYYMMDD]`、`patent_type` 代码、`query` 与 `tiabc` 互斥）后重试 |
| `INVALID_CURSOR` | cursor 失效或 dataset/scope 不一致；不带 cursor 重新检索 |
| `BACKEND_UNAVAILABLE` | 上游暂时不可用，稍后重试 |
