# AI Folder Organize — API 参考

## 基础信息

- **Base URL**: 由 `discover.js` 发现，格式为 `http://127.0.0.1:{port}`
- **响应格式**: `{ "success": true, ... }` 或 `{ "success": false, "error": "..." }`
- **数据编码**: 所有请求与响应必须使用 **UTF-8** 编码。包含中文字符的 POST 请求必须以 UTF-8 字节流发送（Header 指定 `Content-Type: application/json; charset=utf-8`）
- **GET** 用于数据查询；**POST** 用于触发客户端操作

---

## GET /api/workspaces

获取所有已注册工作区。

**返回**:

```json
{
  "success": true,
  "data": [{ "id": 1, "path": "D:\\Workspace\\Downloads", "name": "Downloads", "type": "PRIVATE" }]
}
```

---

## GET /api/analysis/queue-status

查询分析队列积压状态。

**返回**:

```json
{
  "success": true,
  "systemIdle": false,
  "queueLength": 45,
  "currentProcessingFile": "D:\\Workspace\\Downloads\\IMG_102.jpg"
}
```

---

## GET /api/analysis/progress

查询分析进度。

**返回**:

```json
{
  "success": true,
  "isIdle": false,
  "analysis": { "status": "processing", "progressPercentage": 75.0 },
  "organizePage": { "status": "idle", "progressPercentage": 0 }
}
```

---

## GET /api/files/analysis-data

查询文件分析数据。

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `fileId` | number | 否 | 文件 ID，提供时查单个文件；不提供时分页返回列表 |
| `fields` | string | 否 | 逗号分隔，可选值: `description`, `smartName`, `tags`, `metadata`, `qualityScore`, `content` |
| `limit` | number | 否 | 分页大小（默认 10） |
| `offset` | number | 否 | 分页偏移（默认 0） |

**返回（单个文件）**:

```json
{
  "success": true,
  "fileFingerprint": "abc123",
  "smartName": "项目计划_v3",
  "description": "这是一份项目计划文档...",
  "size": 1024000,
  "type": "document",
  "mimeType": "application/pdf",
  "author": "张三",
  "language": "zh-CN",
  "path": "D:\\Workspace\\Downloads\\项目计划.pdf",
  "name": "项目计划.pdf",
  "parentArchive": null,
  "unitId": "unit_1",
  "thumbnailPath": null
}
```

**返回（列表）**:

```json
{
  "success": true,
  "data": [ ... ]
}
```

---

## GET /api/files/search

全文搜索文件。

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keyword` | string | 是 | 搜索关键词 |
| `workspaceId` | number | 否 | 工作区 ID（仅 `scope=real` 时有效） |
| `scope` | string | 否 | `real`（默认）, `virtual`, `all` |
| `virtualDirectoryId` | number | 否 | 虚拟目录 ID（仅 `scope=virtual` 时有效） |
| `limit` | number | 否 | 分页大小（默认 20） |
| `offset` | number | 否 | 分页偏移（默认 0） |

**返回**:

```json
{
  "success": true,
  "data": [{ "id": 1, "path": "D:\\...\\file.txt", "name": "file.txt", "scope": "real" }]
}
```

---

## GET /api/organize/templates

获取整理方案提示词（**不调用本地 AI**）。

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `workspaceId` | number | 是 | 工作区 ID |
| `userInstruction` | string | 否 | 用户视角要求，如"大学生视角" |

**返回**:

```json
{
  "success": true,
  "workspaceId": 1,
  "workspacePath": "D:\\Workspace\\Downloads",
  "fileCount": 150,
  "systemPrompt": "你是一名资深内容归类专家...",
  "userPrompt": "### 文件数据\n..."
}
```

### 使用方式

接口返回的 `systemPrompt` 和 `userPrompt` **不是最终结果**，而是需要提交给 AI 模型的提示词：

1. 将 `systemPrompt` 作为 system 消息
2. 将 `userPrompt` 作为 user 消息
3. 提交给当前 AI 模型推理
4. 模型输出 3 份整理方案，每份包含 `name`, `perspective`, `strategy`

---

## GET /api/virtual-directories

查询虚拟目录列表。

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `workspaceId` | number | 是 | 工作区 ID |
| `depth` | number | 否 | 限制返回层级 |

**返回**:

```json
{
  "success": true,
  "data": [{ "id": 1, "name": "我的虚拟目录", "workspaceId": 1 }]
}
```

---

## POST /api/organize/apply-plan

将 AI 生成的整理方案提交到客户端的自定义虚拟目录弹窗中。客户端将自动切换到整理页面、弹窗并预填方案数据，等待用户确认。

**请求体**:

```json
{
  "name": "encodeURIComponent(\"学生作业整理方案\")",
  "perspective": "encodeURIComponent(\"从大学生的视角，按学期和课程分类\")",
  "strategy": "encodeURIComponent(\"根目录：按学期（2024秋/2025春）→ 子目录：按课程名称 → 文件：按类型（作业/实验/报告）\")"
}
```

> **重要编码说明**：
>
> 1. 所有 POST 请求必须以 **UTF-8** 编码传输（Header 设置 `Content-Type: application/json; charset=utf-8`）。
> 2. 在 **Windows PowerShell (Invoke-RestMethod)** 环境中，由于默认 ANSI 编码会将中文损毁为问号 `?`，须使用 `[System.Text.Encoding]::UTF8.GetBytes($jsonString)` 将字符串转为 UTF-8 字节数组后通过 `-Body` 发送。
> 3. 或者使用 `encodeURIComponent()` 对中文/Unicode 字段进行 URI 编码后再发送，服务端会自动解包并还原。

| 字段          | 类型   | 必填 | 说明                                      |
| ------------- | ------ | ---- | ----------------------------------------- |
| `name`        | string | 是   | 虚拟目录名称（方案标题），须 URI 编码     |
| `strategy`    | string | 是   | 整理策略描述（树形结构说明），须 URI 编码 |
| `perspective` | string | 否   | 用户视角说明，须 URI 编码                 |

**返回**:

```json
{
  "success": true,
  "message": "整理方案已发送到整理页面"
}
```

**错误**:

```json
{
  "success": false,
  "error": "缺少必填字段: name"
}
```
