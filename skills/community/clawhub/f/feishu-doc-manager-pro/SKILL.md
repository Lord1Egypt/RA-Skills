---
name: feishu-doc-manager
description: |
  飞书文档管理技能。支持创建、读取、写入、删除文档和文档块。当用户需要操作飞书文档时使用此技能。触发条件：(1) 创建飞书文档 (2) 读取飞书文档内容 (3) 写入/追加内容到飞书文档 (4) 删除文档块 (5) 清空文档。
---

# 飞书文档管理器

完整的飞书文档操作技能，支持创建、读取、写入、删除文档。

---

## 前置配置

### 1. 开通权限

在飞书开放平台开通以下权限：

| 权限标识 | 权限名称 | 用途 |
|---------|---------|------|
| `docx:document` | 获取、新建、删除文档 | 创建/删除文档 |
| `docx:document:write_only` | 编辑文档 | 写入/删除块 |
| `docx:document:readonly` | 读取文档 | 读取内容 |
| `docs:permission.member` | 文档权限管理 | 协作者管理 |

### 2. 添加文档应用

在飞书客户端：
1. 打开文档 → 右上角 **"..."**
2. **更多** → **添加文档应用**
3. 搜索应用 → 添加，授予 **"可编辑"** 权限

### 3. 获取 Token

```powershell
$config = Get-Content "$env:USERPROFILE\.openclaw\openclaw.json" | ConvertFrom-Json
$appId = $config.channels.feishu.appId
$appSecret = $config.channels.feishu.appSecret

$body = @{ app_id = $appId; app_secret = $appSecret } | ConvertTo-Json
$resp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" -Method Post -Body $body -ContentType "application/json"
$token = $resp.tenant_access_token
```

---

## 核心操作

### 1. 创建文档

```powershell
$createBody = '{"title":"文档标题","folder_token":""}'
$createResp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/docx/v1/documents" -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($createBody)) -ContentType "application/json; charset=utf-8" -Headers @{ Authorization = "Bearer $token" }

$documentId = $createResp.data.document.document_id
Write-Host "文档 ID: $documentId"
Write-Host "文档链接: https://xxx.feishu.cn/docx/$documentId"
```

### 2. 读取文档内容

```powershell
# 获取文档所有块
$blocksResp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/docx/v1/documents/$documentId/blocks/$documentId/children" -Method Get -Headers @{ Authorization = "Bearer $token" }

foreach ($block in $blocksResp.data.items) {
    Write-Host "类型: $($block.block_type), ID: $($block.block_id)"
}
```

### 3. 写入内容

```powershell
# 写入标题和文本
$writeBody = '{"index":-1,"children":[{"block_type":3,"heading1":{"elements":[{"text_run":{"content":"标题"}}]}},{"block_type":2,"text":{"elements":[{"text_run":{"content":"文本内容"}}]}}]}'

$writeResp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/docx/v1/documents/$documentId/blocks/$documentId/children" -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($writeBody)) -ContentType "application/json; charset=utf-8" -Headers @{ Authorization = "Bearer $token" }
```

**块类型说明：**

| block_type | 类型 | 说明 |
|------------|------|------|
| 2 | text | 普通文本 |
| 3 | heading1 | 一级标题 |
| 4 | heading2 | 二级标题 |
| 12 | bullet | 无序列表 |

### 4. 删除块（重要）

**使用 batch_delete API 批量删除：**

```powershell
# 获取当前块数量
$blocksResp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/docx/v1/documents/$documentId/blocks/$documentId/children" -Method Get -Headers @{ Authorization = "Bearer $token" }
$totalBlocks = $blocksResp.data.items.Count

# 删除所有块（左闭右开区间）
$deleteBody = @{
    start_index = 0
    end_index = $totalBlocks
} | ConvertTo-Json

$delResp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/docx/v1/documents/$documentId/blocks/$documentId/children/batch_delete?document_revision_id=-1" -Method Delete -Body ([System.Text.Encoding]::UTF8.GetBytes($deleteBody)) -ContentType "application/json; charset=utf-8" -Headers @{ Authorization = "Bearer $token" }

if ($delResp.code -eq 0) {
    Write-Host "✅ 删除成功"
}
```

**API 说明：**
- **URL**: `DELETE /documents/:document_id/blocks/:block_id/children/batch_delete`
- **参数**: `start_index`（起始索引）、`end_index`（结束索引，左闭右开）
- **注意**: `start_index` 必须小于 `end_index`

### 5. 清空文档并写入新内容

```powershell
# 1. 获取块数量
$blocksResp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/docx/v1/documents/$documentId/blocks/$documentId/children" -Method Get -Headers @{ Authorization = "Bearer $token" }
$totalBlocks = $blocksResp.data.items.Count

# 2. 删除所有块
if ($totalBlocks -gt 0) {
    $deleteBody = @{ start_index = 0; end_index = $totalBlocks } | ConvertTo-Json
    Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/docx/v1/documents/$documentId/blocks/$documentId/children/batch_delete?document_revision_id=-1" -Method Delete -Body ([System.Text.Encoding]::UTF8.GetBytes($deleteBody)) -ContentType "application/json; charset=utf-8" -Headers @{ Authorization = "Bearer $token" } | Out-Null
}

# 3. 写入新内容
$writeBody = '{"index":-1,"children":[{"block_type":3,"heading1":{"elements":[{"text_run":{"content":"新标题"}}]}},{"block_type":2,"text":{"elements":[{"text_run":{"content":"新内容"}}]}}]}'
Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/docx/v1/documents/$documentId/blocks/$documentId/children" -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($writeBody)) -ContentType "application/json; charset=utf-8" -Headers @{ Authorization = "Bearer $token" }

Write-Host "✅ 文档已更新"
```

---

## Wiki 文档处理

Wiki 文档需要先获取实际的 `obj_token`：

```powershell
# Wiki URL: https://xxx.feishu.cn/wiki/XXXXXXXX
$wikiToken = "SRDiwPCx8iEtx6kreaCckFW3nOb"

# 获取实际文档 ID
$wikiResp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token=$wikiToken" -Method Get -Headers @{ Authorization = "Bearer $token" }
$documentId = $wikiResp.data.node.obj_token

Write-Host "实际文档 ID: $documentId"
```

---

## 常见错误

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 1770032 | 权限不足 | 添加应用为文档协作者 |
| 1770002 | 文档不存在 | 检查 document_id |
| 9499 | JSON 格式错误 | 使用纯 JSON 字符串 |

---

## 完整示例：更新天气文档

```powershell
# 配置
$config = Get-Content "$env:USERPROFILE\.openclaw\openclaw.json" | ConvertFrom-Json
$appId = $config.channels.feishu.appId
$appSecret = $config.channels.feishu.appSecret

# 获取 Token
$body = @{ app_id = $appId; app_secret = $appSecret } | ConvertTo-Json
$resp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" -Method Post -Body $body -ContentType "application/json"
$token = $resp.tenant_access_token

$documentId = "你的文档ID"

# 获取天气
$weather = curl.exe -s "wttr.in/Tianjin?format=3"
$timeStr = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

# 清空文档
$blocksResp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/docx/v1/documents/$documentId/blocks/$documentId/children" -Method Get -Headers @{ Authorization = "Bearer $token" }
if ($blocksResp.data.items.Count -gt 0) {
    $deleteBody = @{ start_index = 0; end_index = $blocksResp.data.items.Count } | ConvertTo-Json
    Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/docx/v1/documents/$documentId/blocks/$documentId/children/batch_delete?document_revision_id=-1" -Method Delete -Body ([System.Text.Encoding]::UTF8.GetBytes($deleteBody)) -ContentType "application/json; charset=utf-8" -Headers @{ Authorization = "Bearer $token" } | Out-Null
}

# 写入天气
$writeBody = '{"index":-1,"children":[{"block_type":3,"heading1":{"elements":[{"text_run":{"content":"天津天气"}}]}},{"block_type":2,"text":{"elements":[{"text_run":{"content":"' + $weather + '"}}]}},{"block_type":2,"text":{"elements":[{"text_run":{"content":"更新时间: ' + $timeStr + '"}}]}}]}'
Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/docx/v1/documents/$documentId/blocks/$documentId/children" -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($writeBody)) -ContentType "application/json; charset=utf-8" -Headers @{ Authorization = "Bearer $token" }

Write-Host "✅ 天气已更新"
```

---

## 参考文档

- [飞书文档 API 文档](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document)
- [删除块 API](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/children/batch_delete)