---
name: feishu-wiki-query
description: 飞书知识库文档查询技能。当用户询问需要查询飞书知识库中的文档时使用此技能，包括：查询动物信息、查看排期、读取文档内容、处理文档中的图片、画板和电子表格等。触发场景包括：用户说"查一下xx动物"、"看看排期"、"查询知识库"、"食堂菜谱"等。
---

# 飞书知识库查询

## 概述

本技能用于查询飞书知识库中的文档内容，支持读取文本、图片、画板、电子表格等多种类型的文档内容。

**本技能支持用户自定义知识库配置**，安装后可随时添加/移除知识库。

## 配置文件

配置存储在：`~/.openclaw/workspace/skills/feishu-wiki-query/config.json`

首次使用前需要先进行配置。

## 首次配置

用户首次使用时，提示：

> 🎀 欢迎使用飞书知识库查询技能！
> 请先配置你的知识库地址~
>
> 方式：发送 `添加知识库 [知识库名称] [知识库URL]`
> 例如：`添加知识库 我的知识库 https://my.feishu.cn/wiki/XEMRwElx2iMzHhkkVdCcpj0tnDg`
>
> 知识库 URL 就是你在浏览器打开知识库时地址栏的地址～

## 配置管理命令

### 添加知识库

```
添加知识库 [名称] [知识库URL]
```

示例：
```
添加知识库 海洋动物专区 https://my.feishu.cn/wiki/XEMRwElx2iMzHhkkVdCcpj0tnDg
添加知识库 技术文档 https://my.feishu.cn/wiki/abcdefg1234567
```

**自动解析：** 从 URL 中提取 node_token，并通过 API 获取 space_id，全程无需用户手动提供。

### 移除知识库

```
移除知识库 [名称]
```

### 查看已配置的知识库

```
查看知识库
```

### 重置配置

```
重置知识库配置
```

⚠️ 此操作会清空所有已配置的知识库，请谨慎使用！

## 添加知识库时的自动解析流程

当用户输入 `添加知识库 [名称] [URL]` 时：

1. **解析 URL 获取 node_token**
   - URL 格式：`https://my.feishu.cn/wiki/{node_token}`
   - 提取 `node_token` = URL 路径最后一段

2. **获取 space_id**
   ```python
   feishu_wiki {
     action: "get",
     token: "解析出的node_token"
   }
   ```
   从返回中获取 `space_id`

3. **保存配置**
   将以下内容写入 `config.json`：
   ```json
   {
     "version": 1,
     "updated_at": "当前时间",
     "knowledge_bases": [
       {
         "name": "用户提供的名称",
         "space_id": "获取到的space_id",
         "root_node_token": "解析出的node_token"
       }
     ]
   }
   ```

## 查询流程

### 步骤1：浏览知识库目录

首先获取首页目录（使用配置中的 space_id 和首页 node_token）：

如果只有一个知识库，直接使用：
```python
feishu_wiki {
  action: "nodes",
  space_id: "配置中的space_id",
  parent_node_token: "配置中的首页node_token"
}
```

如果有多个知识库，先询问用户要查询哪个：
> 你想查询哪个知识库？
> 1. 海洋动物专区
> 2. 技术文档
> ...

用户选择后，使用对应的 space_id 和 node_token。

### 步骤2：进入子目录

必须加 `parent_node_token` 参数才能读到子目录！
```python
feishu_wiki {
  action: "nodes",
  space_id: "space_id",
  parent_node_token: "当前目录的node_token"
}
```

### 步骤3：递归深入找到目标文档

重复步骤2，直到找到目标文档。

### 步骤4：读取文档内容

```python
feishu_doc {
  action: "read",
  doc_token: "obj_token"
}
```

## 通过 URL 解析获取 space_id

如果用户提供了知识库的 wiki URL（如 `https://my.feishu.cn/wiki/XEMRwElx2iMzHhkkVdCcpj0tnDg`），可以尝试自动获取 space_id：

```python
# URL 中的 node_token
node_token = "XEMRwElx2iMzHhkkVdCcpj0tnDg"

# 尝试获取节点信息（可能包含 space_id）
feishu_wiki {
  action: "get",
  token: node_token
}
```

> 注意：部分节点可能无法直接获取 space_id，此时请让用户提供正确的 space_id。

## 文档Blocks类型

常用 block_type 对照表：

| block_type | 含义 |
|------------|------|
| 1 | Page（页面） |
| 2 | Text（文本段落） |
| 4 | Heading2（二级标题） |
| 27 | Image（图片） |
| 43 | Whiteboard（画板） |

## 处理图片内容

当文档包含图片时，`feishu_doc { action: "read" }` 会返回提示：
> "This document contains Image which are NOT included in the plain text above."

### 处理步骤：

1. **列出所有 Blocks**
   ```python
   feishu_doc {
     action: "list_blocks",
     doc_token: "文档token"
   }
   ```

2. **找到图片 Block**
   - 图片的 `block_type` 是 `27`
   - 图片 token 在 `block.image.token` 字段

3. **下载图片**
   ```bash
   curl "https://open.feishu.cn/open-apis/drive/v1/medias/{image_token}/download" \
     -H "Authorization: Bearer {token}"
   ```

## 处理画板（Whiteboard）内容

当文档包含画板时（block_type=43）：

1. **获取画板的 whiteboard_id**
   - 用 `list_blocks` 列出所有 blocks
   - 找到 `block_type=43` 的 block，其 `block_id` 即为 `whiteboard_id`

2. **获取画板内容**
   ```bash
   curl "https://open.feishu.cn/open-apis/board/v1/whiteboards/{whiteboard_id}/nodes" \
     -H "Authorization: Bearer {token}"
   ```
   - 需权限：`board:whiteboard:node:read`

## 发送图片给用户

当需要将知识库中的图片发送给用户时，使用以下Python脚本：

```python
import requests
import json

# 1. 获取 tenant_access_token
token_resp = requests.post(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    json={
        "app_id": "cli_a938e5e808b8dbca",
        "app_secret": "0ejwDP7CVN11Mm3PPhtYtfnMQONSJjDo"
    }
)
token = token_resp.json()["tenant_access_token"]

# 2. 上传图片
with open('/tmp/图片.png', 'rb') as f:
    img_resp = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/images",
        headers={"Authorization": f"Bearer {token}"},
        files={"image": ("图片.png", f.read(), "image/png")},
        data={"image_type": "message"}
    )
image_key = img_resp.json()["data"]["image_key"]

# 3. 发送图片消息（需提供接收者的 open_id）
msg_resp = requests.post(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={
        "receive_id": "用户open_id",
        "msg_type": "image",
        "content": json.dumps({"image_key": image_key})
    }
)
```

## 处理电子表格（Sheet）

当知识库中的文档类型是 `sheet`（电子表格）时，需要使用 Sheets API 处理。

### 重要前提

**必须开通 `sheets:spreadsheet` 权限**（不是 readonly）！否则会返回 404。

### 读取电子表格步骤

#### 步骤1：获取工作表列表

```python
# API 路径：/sheets/v3/spreadsheets/{spreadsheetToken}/sheets/query
curl "https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{sheet_token}/sheets/query" \
  -H "Authorization: Bearer {token}"
```

返回示例：
```json
{
  "data": {
    "sheets": [{
      "sheet_id": "b56f8e",
      "title": "Sheet1",
      "resource_type": "sheet"
    }]
  }
}
```

#### 步骤2：读取表格数据

使用 v2 API 读取数据：
```python
# API 路径：/sheets/v2/spreadsheets/{spreadsheetToken}/values/{sheetId}!A1:Z100
curl "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{sheet_token}/values/b56f8e!A1:Z100" \
  -H "Authorization: Bearer {token}"
```

返回示例：
```json
{
  "data": {
    "valueRange": {
      "range": "b56f8e!A1:Z100",
      "values": [
        ["", "周一", "周二", "周三", "周四", "周五", "周六", "周日"],
        ["早饭", "油条", "油条", "油条", "油条", "包子", "包子", "包子"],
        ["午饭", "鱼香茄子", "鱼香茄子", "鱼香茄子", "鱼香茄子", "鱼香茄子", "鱼香茄子", "鱼香茄子"],
        ["晚饭", "红烧肉", "红烧肉", "红烧肉", "红烧肉", "红烧肉", "红烧肉", "红烧肉"]
      ]
    }
  }
}
```

### 完整读取电子表格示例

```python
import requests
import json

# 获取 token
token_resp = requests.post(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    json={
        "app_id": "cli_a938e5e808b8dbca",
        "app_secret": "0ejwDP7CVN11Mm3PPhtYtfnMQONSJjDo"
    }
)
token = token_resp.json()["tenant_access_token"]

sheet_token = "电子表格的obj_token"

# 1. 获取工作表 ID
sheets_resp = requests.get(
    f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{sheet_token}/sheets/query",
    headers={"Authorization": f"Bearer {token}"}
)
sheet_id = sheets_resp.json()["data"]["sheets"][0]["sheet_id"]

# 2. 读取表格数据（使用 v2 API）
values_resp = requests.get(
    f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{sheet_token}/values/{sheet_id}!A1:Z100",
    headers={"Authorization": f"Bearer {token}"}
)
values = values_resp.json()["data"]["valueRange"]["values"]

# 3. 格式化输出（过滤空值）
for row in values:
    if any(cell is not None for cell in row):
        print(row)
```

### 注意事项

1. **获取工作表用 v3，读取数据用 v2** - 这是飞书 API 的现状
2. **必须开通 `sheets:spreadsheet` 权限** - 否则返回 404
3. **表格数据可能很大** - 建议只读取需要的范围，如 `A1:Z100`

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `Search is not available` | 知识库搜索未开放 | 改用 `nodes` 遍历 |
| `Missing access token` | token 过期 | 重新获取 tenant_access_token |
| `receive_id_type is required` | 发送消息缺参数 | URL 加 `?receive_id_type=open_id` |
| `WrongBaseToken` | token 格式错误 | 确认使用的是正确的 token 类型 |
| `NOTEXIST` | 文档不存在或无权访问 | 检查 token 是否正确 |
| `404 page not found` (sheets) | 缺少 `sheets:spreadsheet` 权限 | 在飞书后台开通该权限 |
| 读取表格返回空数据 | 使用的 API 版本不对 | 确认用 v2 API 读取值 |
| 未配置知识库 | 首次使用未配置 | 按上方"首次配置"步骤进行配置 |

## 输出格式

查询完成后，必须标注信息来源：
- "📋 来源：飞书知识库 - [知识库名称]"
- "📋 来源：飞书知识库 - 动物园排班表"
