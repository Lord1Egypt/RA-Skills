---
name: dingtalk-bitable
description: "钉钉多维表格 API 集成 - 表格管理、数据 CRUD。Use when: user asks about DingTalk bitable, table, database, spreadsheet."
metadata: { "openclaw": { "emoji": "📊", "requires": { "python": ["requests"] } } }
---

# DingTalk Bitable 技能

钉钉多维表格（Bitable）API 集成，提供表格管理、数据增删改查等功能。

## 功能

### 📊 表格管理
- 获取表格列表
- 创建新表格
- 获取表格结构（字段/列）
- 删除表格

### 📝 数据操作
- 查询记录（支持筛选、排序）
- 新增记录
- 更新记录
- 删除记录
- 批量操作

### 🔍 高级功能
- 字段管理（添加/修改/删除字段）
- 视图管理
- 数据导入导出

## 配置

### 钉钉应用权限

需要在钉钉开放平台申请以下权限：
- 多维表格权限
- 应用访问权限

### 凭证配置

技能自动从 openclaw.json 的钉钉 channel 配置中读取凭证，无需额外配置。

## 工具

### bitable_list
获取表格列表

**参数：**
- `space_id` (可选): 空间 ID
- `limit` (可选): 返回数量限制，默认 20

### bitable_get_meta
获取表格元数据

**参数：**
- `app_token` (必需): 表格应用 token（从 URL 获取）

### bitable_list_fields
获取表格字段列表

**参数：**
- `app_token` (必需): 表格应用 token
- `table_id` (必需): 表格 ID

### bitable_list_records
查询记录

**参数：**
- `app_token` (必需): 表格应用 token
- `table_id` (必需): 表格 ID
- `filter` (可选): 筛选条件
- `sort` (可选): 排序字段
- `page_size` (可选): 每页数量，默认 100
- `page_token` (可选): 分页 token

### bitable_get_record
获取单条记录

**参数：**
- `app_token` (必需): 表格应用 token
- `table_id` (必需): 表格 ID
- `record_id` (必需): 记录 ID

### bitable_create_record
新增记录

**参数：**
- `app_token` (必需): 表格应用 token
- `table_id` (必需): 表格 ID
- `fields` (必需): 字段值（JSON 对象）

### bitable_update_record
更新记录

**参数：**
- `app_token` (必需): 表格应用 token
- `table_id` (必需): 表格 ID
- `record_id` (必需): 记录 ID
- `fields` (必需): 要更新的字段值

### bitable_delete_record
删除记录

**参数：**
- `app_token` (必需): 表格应用 token
- `table_id` (必需): 表格 ID
- `record_id` (必需): 记录 ID

### bitable_create_field
添加字段

**参数：**
- `app_token` (必需): 表格应用 token
- `table_id` (必需): 表格 ID
- `field_name` (必需): 字段名称
- `field_type` (必需): 字段类型（Text/Number/Date/SingleSelect/MultiSelect/Checkbox/User/Phone/URL）

## 使用示例

```
# 获取表格列表
bitable_list limit=10

# 获取表格元数据（从 URL /base/XXX 或 /wiki/XXX 获取 app_token）
bitable_get_meta app_token="Stbqxxxxxxxxxxxxxx"

# 查看表格字段
bitable_list_fields app_token="Stbqxxxxxxxxxxxxxx" table_id="tblxxxxxxxxxxxxxx"

# 查询记录
bitable_list_records app_token="Stbqxxxxxxxxxxxxxx" table_id="tblxxxxxxxxxxxxxx" page_size=50

# 新增记录
bitable_create_record app_token="Stbqxxxxxxxxxxxxxx" table_id="tblxxxxxxxxxxxxxx" fields='{"姓名":"张三","部门":"研发部","入职日期":"2026-03-19"}'

# 更新记录
bitable_update_record app_token="Stbqxxxxxxxxxxxxxx" table_id="tblxxxxxxxxxxxxxx" record_id="recxxxxxxxxxxxxxx" fields='{"部门":"产品部"}'

# 删除记录
bitable_delete_record app_token="Stbqxxxxxxxxxxxxxx" table_id="tblxxxxxxxxxxxxxx" record_id="recxxxxxxxxxxxxxx"

# 添加字段
bitable_create_field app_token="Stbqxxxxxxxxxxxxxx" table_id="tblxxxxxxxxxxxxxx" field_name="手机号" field_type="Phone"
```

## 字段类型说明

| 类型 | 说明 | 示例值 |
|------|------|--------|
| Text | 文本 | "张三" |
| Number | 数字 | 123 |
| Date | 日期 | 1710835200000 (毫秒时间戳) |
| SingleSelect | 单选 | "选项 A" |
| MultiSelect | 多选 | ["选项 A", "选项 B"] |
| Checkbox | 复选框 | true |
| User | 成员 | [{"id":"zhangsan"}] |
| Phone | 手机号 | "13800138000" |
| URL | 链接 | {"text":"显示文本","link":"https://..."} |

## 实现位置

技能实现位于：`/volume1/openclaw/workspace/skills/dingtalk-bitable/`

包含文件：
- `SKILL.md` - 技能定义
- `dingtalk_bitable.py` - API 实现
- `run.py` - 工具执行入口
- `manifest.json` - 工具定义

## 错误处理

- 凭证无效：返回认证错误
- 权限不足：提示需要申请的权限
- API 限流：自动重试
- 表格不存在：返回明确的错误信息

## 相关资源

- 钉钉开放平台文档：https://open.dingtalk.com/document/orgapp/overview-of-dingtalk-tables
- API 参考：https://open.dingtalk.com/document/orgapp
