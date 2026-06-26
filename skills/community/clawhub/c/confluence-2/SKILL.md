---
name: confluence
description: Confluence Cloud 集成。空间/页面 CRUD、标签、评论、子页面、CQL 搜索。通过 MorphixAI 代理安全访问 Confluence Cloud API（v2 CRUD + v1 搜索）。
metadata:
  openclaw:
    emoji: "📄"
    requires:
      env: [MORPHIXAI_API_KEY]
---

# Confluence Cloud

通过 `mx_confluence` 工具管理 Confluence 工作区：空间浏览、页面 CRUD、标签管理、评论、子页面导航、CQL 搜索。

## 前置条件

1. **安装插件**: `openclaw plugins install openclaw-morphixai`
2. **获取 API Key**: 访问 [morphix.app/api-keys](https://morphix.app/api-keys) 生成 `mk_xxxxxx` 密钥
3. **配置环境变量**: `export MORPHIXAI_API_KEY="mk_your_key_here"`
4. **链接账号**: 访问 [morphix.app/connections](https://morphix.app/connections) 链接 Confluence 账号，或通过 `mx_link` 工具链接（app: `confluence`）

## 核心操作

### 列出空间

```
mx_confluence:
  action: list_spaces
  limit: 10
  type: "global"
```

> `type` 可选值：`global`（团队空间）、`personal`（个人空间）

### 获取空间详情

```
mx_confluence:
  action: get_space
  space_id: "163843"
```

### 列出页面

```
mx_confluence:
  action: list_pages
  space_id: "163843"
  limit: 20
  sort: "-modified-date"
```

> 省略 `space_id` 列出所有空间的页面。

### 获取页面详情

```
mx_confluence:
  action: get_page
  page_id: "163923"
  body_format: "storage"
```

> `body_format` 可选值：`storage`（HTML）、`atlas_doc_format`（ADF）、`view`（渲染后 HTML）

### 创建页面

```
mx_confluence:
  action: create_page
  space_id: "163843"
  title: "会议纪要 2026-02-25"
  body: "<h2>议题</h2><p>1. 项目进度回顾</p><p>2. 下周计划</p>"
  parent_id: "163924"
```

> `body` 使用 Confluence Storage Format（HTML 子集）。`parent_id` 可选，省略则创建为顶级页面。

### 更新页面

```
mx_confluence:
  action: update_page
  page_id: "163923"
  title: "更新后的标题"
  body: "<p>更新后的内容</p>"
  version: 2
```

> **必须提供** `version`（当前版本号 + 1），否则更新失败。先用 `get_page` 获取当前版本号。

### 删除页面

```
mx_confluence:
  action: delete_page
  page_id: "163923"
```

### 获取子页面

```
mx_confluence:
  action: get_child_pages
  page_id: "163923"
  limit: 20
  sort: "-modified-date"
```

### 获取页面标签

```
mx_confluence:
  action: get_page_labels
  page_id: "163923"
```

### 添加标签

```
mx_confluence:
  action: add_page_label
  page_id: "163923"
  label: "important"
```

### 删除标签

```
mx_confluence:
  action: delete_page_label
  page_id: "163923"
  label_id: "12345"
```

> 先用 `get_page_labels` 获取 label ID。

### 获取页面评论

```
mx_confluence:
  action: get_page_comments
  page_id: "163923"
  body_format: "storage"
  limit: 10
```

### 添加评论

```
mx_confluence:
  action: add_page_comment
  page_id: "163923"
  body: "<p>这是一条评论</p>"
```

### CQL 搜索

```
mx_confluence:
  action: search
  cql: "type=page AND space.key=SOP AND title~\"API\""
  limit: 10
```

> CQL 常用语法：
> - `type=page` / `type=blogpost` — 内容类型
> - `space.key=XX` — 指定空间
> - `title~"关键词"` — 标题模糊搜索
> - `text~"关键词"` — 全文搜索
> - `creator=currentUser()` — 当前用户创建的
> - `lastModified >= "2026-01-01"` — 时间范围

## 常见工作流

### 浏览团队文档

```
1. mx_confluence: list_spaces → 找到目标空间
2. mx_confluence: list_pages, space_id: "xxx", sort: "-modified-date"
3. mx_confluence: get_page, page_id: "xxx", body_format: "storage" → 查看内容
```

### 创建并更新文档

```
1. mx_confluence: list_spaces → 选择空间
2. mx_confluence: create_page, space_id: "xxx", title: "...", body: "..."
3. mx_confluence: get_page → 获取版本号
4. mx_confluence: update_page, version: N+1 → 更新内容
```

## 注意事项

- CRUD 操作使用 Confluence Cloud v2 API；CQL 搜索使用 v1 API（v2 无搜索端点）
- 页面内容格式为 Confluence Storage Format（HTML 子集）
- 更新页面时必须提供正确的 `version` 号（当前版本 + 1）
- CQL 搜索功能强大，建议充分利用
- `account_id` 参数通常省略，工具自动检测已链接的 Confluence 账号
