---
name: feishu-bitable
description: |
  Feishu/Lark Bitable CRUD skill. Teaches your agent to correctly use feishu_bitable_* tools
  for creating, reading, updating records in Feishu Bitable. Handles both /wiki/ and /base/ URL
  formats automatically — resolves wiki node_token to real bitable app_token before any operation.
  Use when: agent needs to read/write Feishu Bitable (multidimensional spreadsheet) data.
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      plugins: ["feishu"]
---

# 飞书多维表格 CRUD Skill / Feishu Bitable CRUD

教会 OpenClaw Agent 正确操作飞书（Lark）多维表格，避免常见的 token 混淆错误。

## 为什么需要这个 Skill？

OpenClaw 内置的 `feishu_bitable_*` 工具已经支持多维表格 CRUD，但 Agent 常常犯一个错误：
**直接把飞书链接中的 token 当作 `app_token` 使用**，导致 `91402 NOTEXIST` 错误。

这在飞书知识库（wiki）嵌入的多维表格中尤其常见 — wiki URL 中的 token 是 `node_token`，不是 bitable 的 `app_token`。

这个 Skill 教会 Agent：
1. **始终先调用 `feishu_bitable_get_meta`** 解析 URL，获取真实的 `app_token`
2. 再用解析得到的 `app_token` 执行后续 CRUD 操作

## 安装

```bash
clawhub install feishu-bitable-crud
```

或手动复制到 `~/.openclaw/workspace/skills/feishu-bitable/`。

## 前提条件

1. **飞书插件已启用** — `openclaw.json` 中配置了飞书 channel（appId + appSecret）
2. **应用权限** — 在飞书开放平台后台开通以下权限：
   - `bitable:app` — 管理多维表格
   - `bitable:app:readonly` — 读取多维表格
   - `wiki:wiki:readonly` — 读取知识库（wiki URL 解析需要）
3. **资源权限** — 在飞书多维表格的「分享」设置中，将你的应用添加为协作者

## 核心规则

**当用户给出包含 `/wiki/` 的飞书链接时，必须先用 `feishu_bitable_get_meta` 解析出真实的 `app_token`，再进行后续操作。绝对不能直接把 wiki 的 node_token 当作 app_token 使用。**

## URL 格式说明

飞书多维表格有两种链接格式：

1. **Base 格式**（直链）：`https://xxx.feishu.cn/base/AppToken123?table=tblXXX`
   - `AppToken123` 就是 `app_token`，可直接使用
2. **Wiki 格式**（知识库嵌入）：`https://xxx.feishu.cn/wiki/NodeToken456`
   - `NodeToken456` 是 wiki 的 `node_token`，**不是** bitable 的 `app_token`
   - 必须先调用 `feishu_bitable_get_meta` 解析

## 标准操作流程

### 第一步：解析 URL，获取 app_token 和 table_id

无论用户给的是 wiki 还是 base 链接，都先调用 `feishu_bitable_get_meta`：

```
feishu_bitable_get_meta({ url: "用户给的完整URL" })
```

返回值包含：
- `app_token`：真实的多维表格 token（后续所有操作都用这个）
- `table_id`：如果 URL 带 `?table=` 参数则有
- `tables`：表格列表（如果没指定 table_id）

**重要**：记住返回的 `app_token`，后续所有操作都使用它，不要再用 URL 里的 token。

### 第二步：获取表结构（字段列表）

```
feishu_bitable_list_fields({ app_token: "上一步获取的app_token", table_id: "table_id" })
```

返回每个字段的 `field_name`、`type`、`type_name`，写入数据时字段名必须与此一致。

### 第三步：执行操作

#### 写入记录
```
feishu_bitable_create_record({
  app_token: "app_token",
  table_id: "table_id",
  fields: {
    "字段名1": "文本值",
    "字段名2": 123,
    "字段名3": { text: "显示文本", link: "https://example.com" }
  }
})
```

#### 查询记录
```
feishu_bitable_list_records({
  app_token: "app_token",
  table_id: "table_id",
  page_size: 100
})
```

#### 更新记录
```
feishu_bitable_update_record({
  app_token: "app_token",
  table_id: "table_id",
  record_id: "recXXX",
  fields: { "字段名": "新值" }
})
```

#### 创建新表格
```
feishu_bitable_create_app({ name: "表格名称" })
```

#### 创建字段
```
feishu_bitable_create_field({
  app_token: "app_token",
  table_id: "table_id",
  field_name: "新字段名",
  field_type: 1
})
```

## 字段类型对照

| type | type_name | 写入格式 |
|------|-----------|----------|
| 1 | Text | `"字符串"` |
| 2 | Number | `123` 或 `45.6` |
| 3 | SingleSelect | `"选项名"` |
| 4 | MultiSelect | `["选项A", "选项B"]` |
| 5 | DateTime | `1700000000000`（毫秒时间戳） |
| 7 | Checkbox | `true` 或 `false` |
| 11 | User | `[{ id: "ou_xxx" }]` |
| 13 | Phone | `"13800138000"` |
| 15 | URL | `{ text: "显示文本", link: "https://..." }` |
| 17 | Attachment | 不支持直接写入 |

## 常见错误及解决

| 错误码 | 含义 | 解决方法 |
|--------|------|----------|
| 91402 NOTEXIST | app_token 无效 | 检查是否把 wiki node_token 当成了 app_token，必须先用 `feishu_bitable_get_meta` 解析 |
| 131005 not found | 表格不存在 | 检查 table_id 是否正确 |
| 99991672 Access denied | 权限不足 | 需要在飞书开放平台后台开通 `bitable:bitable` 等权限 |

## 完整示例：用户给 wiki 链接，写入数据

```
用户：把数据写入 https://xxx.feishu.cn/wiki/Abc123Def

Step 1: feishu_bitable_get_meta({ url: "https://xxx.feishu.cn/wiki/Abc123Def" })
        → { app_token: "RealToken789", tables: [{ table_id: "tbl001", name: "Sheet1" }] }

Step 2: feishu_bitable_list_fields({ app_token: "RealToken789", table_id: "tbl001" })
        → { fields: [{ field_name: "标题", type: 1 }, { field_name: "链接", type: 15 }] }

Step 3: feishu_bitable_create_record({
          app_token: "RealToken789",
          table_id: "tbl001",
          fields: {
            "标题": "示例数据",
            "链接": { text: "点击查看", link: "https://example.com" }
          }
        })
```
