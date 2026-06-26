---
name: feishu-bitable-permission-checker
description: 飞书多维表格文档权限检查工具。当用户提供一个飞书多维表格（bitable）URL 或 app_token 时，自动提取【链接地址】列，逐一检查每个链接的飞书文档（docx/wiki）阅读权限，最终输出【有权限文档列表】和【无权限文档列表】。触发词：检查文档权限、批量检查权限、哪些文档我能看、多维表格链接权限检查。
---

# Feishu Bitable Permission Checker

输入一个飞书多维表格，提取「链接地址」列，批量检查飞书文档阅读权限。

## 工作流程

### Step 1：解析多维表格

支持两种输入格式：
- **完整 URL**：`https://asiainfo.feishu.cn/base/FDo4bVmnVaYRJlslJttcPwgwnfh?table=tblRjin7OM9XvEDL&view=vew3qPDrS3`
- **仅 app_token**：`FDo4bVmnVaYRJlslJttcPwgwnfh`（需同时提供 table_id）

从 URL 中提取：
- `app_token`：第一个路径段（如 `FDo4bVmnVaYRJlslJttcPwgwnfh`）
- `table_id`：从 `table=` 参数获取（如 `tblRjin7OM9XvEDL`）

### Step 2：查找「链接地址」列字段 ID

调用 `feishu_bitable_app_table_field` 获取表结构：

```
feishu_bitable_app_table_field(
  action="list",
  app_token="<app_token>",
  table_id="<table_id>"
)
```

在返回的 `fields` 数组中找到 `field_name` 为「链接地址」的字段，记录其 `field_id`。

> 注意：如果字段名不是「链接地址」，根据实际字段名调整查询参数。

### Step 3：提取所有链接地址

调用 `feishu_bitable_app_table_record` 获取所有记录：

```
feishu_bitable_app_table_record(
  action="list",
  app_token="<app_token>",
  table_id="<table_id>",
  field_names=["员工姓名", "链接地址"],
  page_size=500
)
```

解析每条记录的 `fields`，提取：
- `员工姓名`：主键字段，用于标识文档归属
- `链接地址`：目标文档 URL（docx 或 wiki）

### Step 4：批量检查文档权限

对每个链接，调用 `feishu_fetch_doc` 验证读取权限：

```
feishu_fetch_doc(doc_id="<doc_id>")
```

- `doc_id` 从 URL 路径段提取（docx 或 wiki token）
- 解析返回结果：
  - `success=true` + `message="Document fetched successfully"` → **有权限**
  - `error` 中包含 `forBidden` → **无权限**
  - `error` 中包含 `request trigger frequency limit` → **限流**，稍后重试

#### 权限判断逻辑

```
if success == true:
    → 有权限
elif "forBidden" in error:
    → 无权限
elif "frequency limit" in error:
    → 限流，延迟3秒后重试一次
else:
    → 视为无权限
```

#### 限流处理

飞书 API 有频率限制（10-20 QPS）。每个文档最多重试 2 次：
1. 首次失败 → 等 3 秒 → 重试
2. 重试仍失败 → 等 5 秒 → 再重试
3. 仍失败 → 标记为无权限

每次最多并发 10 个请求，超出时拆分为多批次（间隔 1 秒）。

### Step 5：输出结果

按以下格式输出：

```
## 权限检查结果

### ✅ 有阅读权限（{n} 人）

| 序号 | 员工姓名 | 文档标题 | 链接 |
|------|----------|----------|------|
| 1 | 张三 | 标题 | [链接](url) |

### ❌ 无阅读权限（{m} 人）

| 序号 | 员工姓名 | 链接 |
|------|----------|------|
| 1 | 李四 | [链接](url) |
```

## 关键约束

1. **权限隔离**：只向 owner 报告结果，不在群聊中暴露文档内容
2. **不重复输出**：同一批文档只报告一次结果，不分段重复发送
3. **限流优先重试**：限流错误不等同于无权限，必须重试
4. **URL 清洗**：链接中的查询参数（如 `?from=from_copylink`）不影响 doc_id 提取，只取路径段

## 工具依赖

- `feishu_bitable_app_table_field`：查字段结构
- `feishu_bitable_app_table_record`：批量读记录
- `feishu_fetch_doc`：验证文档可读性

详细字段类型和 API 行为见 `references/api_notes.md`。
