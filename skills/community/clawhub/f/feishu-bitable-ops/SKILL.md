---
name: feishu-bitable-ops
description: 飞书多维表格（Bitable）操作技能。处理 wiki URL 与 base URL 的 token 区分、字段类型写入格式、批量操作。当需要读写飞书多维表格、创建记录、查询数据、管理字段时使用。
---

# 飞书多维表格操作

## 核心原则

**Wiki URL ≠ 直接可用**：`/wiki/` 链接里的 token 是 `node_token`，不是 `app_token`，必须先解析。

## URL 解析规则

| URL 格式 | Token 类型 | 处理方式 |
|---------|-----------|---------|
| `.../base/AppToken` | 直接就是 `app_token` | 可直接用 |
| `.../wiki/NodeToken` | `node_token` | 必须用 `feishu_wiki_space_node get` 解析出 `obj_token` |

```bash
# wiki URL → 获取真实 app_token
feishu_wiki_space_node(action="get", token="NodeToken")
# 返回的 obj_token 才是 bitable 的 app_token
```

## 操作流程

### 1. 获取 app_token

```bash
# base URL（直链）
app_token = "AppToken"（直接用）

# wiki URL
obj_token = feishu_wiki_space_node(get, token="NodeToken").obj_token
app_token = obj_token
```

### 2. 获取 table_id 和字段结构

```bash
# 列出所有数据表
feishu_bitable_app_table(action="list", app_token="app_token")

# 列出所有字段（字段名 + 类型）
feishu_bitable_app_table_field(action="list", app_token="app_token", table_id="table_id")
```

### 3. CRUD 操作

```bash
# 查记录（支持筛选、排序、分页）
feishu_bitable_app_table_record(action="list", app_token="app_token", table_id="table_id", filter=..., sort=..., page_size=50)

# 写入单条记录
feishu_bitable_app_table_record(action="create", app_token="app_token", table_id="table_id", fields={...})

# 批量写入（最多500条/次）
feishu_bitable_app_table_record(action="batch_create", app_token="app_token", table_id="table_id", records=[...])

# 更新记录
feishu_bitable_app_table_record(action="update", app_token="app_token", table_id="table_id", record_id="recxxx", fields={...})

# 删除记录
feishu_bitable_app_table_record(action="delete", app_token="app_token", table_id="table_id", record_id="recxxx")
```

## 字段类型写入格式

| 类型 | type 值 | 写入格式 | 示例 |
|------|---------|---------|------|
| 文本 | 1 | `"字符串"` | `"版本 v1.0"` |
| 数字 | 2 | `数字` | `123` 或 `45.6` |
| 单选 | 3 | `"选项名"` | `"Beta"` |
| 多选 | 4 | `["选项A","选项B"]` | `["A","B"]` |
| 日期 | 5 | `毫秒时间戳` | `1746070800000` |
| 复选框 | 7 | `true` / `false` | `true` |
| 人员 | 11 | `[{id: "ou_xxx"}]` | `[{id: "ou_39e815b447d128baf299b7cc6be9f1db"}]` |
| 超链接 | 15 | `{text: "显示文本", link: "https://..."}` | `{text: "文档", link: "https://..."}` |
| 附件 | 17 | 不支持写入 | — |

**日期时间戳**：如需设为指定时间，用 `new Date("2026-04-13T17:00:00+08:00").getTime()` 生成。

## 批量操作

```bash
# 批量创建（单次最多500条）
records = [
  {fields: {"字段1": "值1", "字段2": "值2"}},
  {fields: {"字段1": "值3", "字段2": "值4"}}
]
feishu_bitable_app_table_record(action="batch_create", app_token="app_token", table_id="table_id", records=records)
```

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `91402 NOTEXIST` | 用 wiki node_token 当 app_token | 先用 wiki get 解析 |
| `131005 not found` | table_id 错误 | 先 list 确认 table_id |
| `99991672 Access denied` | 应用没有多维表格权限 | 飞书开放平台开通 `bitable:app` 权限 |
| `WrongRequestBody`（字段创建） | 超链接字段传了 property | 超链接 type=15 时不要传 property |

## 多维表格 URL 格式

- **Base 直链**：`https://xxx.feishu.cn/base/AppToken?table=tblXXX`
- **Wiki 嵌入**：`https://xxx.feishu.cn/wiki/NodeToken`

从浏览器地址栏复制链接时，一定要注意区分是 `/base/` 还是 `/wiki/`。
