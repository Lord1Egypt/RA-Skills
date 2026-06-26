---
name: feishu-file-manager
description: |
  飞书云盘文件管理技能。用于读取、下载和管理飞书云盘中的文件。
  当用户需要：访问飞书文件、下载文档、读取PDF/Word/PPT文件、分析飞书云盘内容时使用。
  核心方法：使用 tenant_access_token 调用 Drive API 下载文件，解析内容返回给用户。
---

# Feishu File Manager | 飞书文件管理器

## 快速开始

### 1. 获取凭据

飞书凭据在 `~/.openclaw/openclaw.json` 中：
```json
{
  "channels": {
    "feishu": {
      "appId": "cli_xxx",
      "appSecret": "xxx"
    }
  }
}
```

### 2. 获取 Token

```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id": "cli_xxx", "app_secret": "xxx"}'
```

返回：`{"tenant_access_token": "t-xxx", "expire": 7200, "msg": "ok"}`

**Token 有效期**：约 2 小时，超时后重新获取

### 3. 访问文件

#### 3.1 从链接提取文件 Token

| 链接格式 | Token 位置 |
|----------|------------|
| `/file/XXXXX` | `XXXXX` |
| `/docx/XXXXX` | `XXXXX` |
| `/drive/folder/XXXXX` | `XXXXX` |

#### 3.2 下载文件

```bash
curl -s -X GET 'https://open.feishu.cn/open-apis/drive/v1/files/{file_token}/download' \
  -H 'Authorization: Bearer {tenant_access_token}' \
  -o /tmp/filename.ext
```

#### 3.3 读取内容

| 文件类型 | 读取方法 |
|----------|----------|
| .docx | Python unzip 解析 `word/document.xml` |
| .pdf | pdftotext 或 pdf 工具 |
| .pptx | python-pptx 库 |
| .xlsx | openpyxl 库 |

## 权限清单 | Required Permissions

### 云盘 Drive

| 权限 scope | 说明 |
|-----------|------|
| `drive:drive` | 云盘能力总览 |
| `drive:file` | 文件基础操作 |
| `drive:file:readonly` | 只读文件 |
| `drive:file:download` | 下载文件 |
| `drive:drive:readonly` | 只读云盘元信息 |

### 文档 Docx

| 权限 scope | 说明 |
|-----------|------|
| `docx:document` | 文档基础能力 |
| `docx:document:readonly` | 只读文档内容 |
| `docx:document:write_only` | 写入文档 |

### 表格 Sheets

| 权限 scope | 说明 |
|-----------|------|
| `sheets:spreadsheet` | 表格基础能力 |
| `sheets:spreadsheet:read` | 读取表格 |

### 多维表格 Bitable

| 权限 scope | 说明 |
|-----------|------|
| `bitable:app` | 多维表格应用 |
| `bitable:app:readonly` | 只读多维表格 |

### 知识库 Wiki

| 权限 scope | 说明 |
|-----------|------|
| `wiki:wiki` | 知识库基础 |
| `wiki:node:read` | 读取知识库节点 |

## 验证方法 | Validation

### 验证 Token 有效性

```bash
curl -s 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id": "cli_xxx", "app_secret": "xxx"}'
```

- 返回 `{"msg": "ok"}` = 有效
- 返回 `{"msg": "invalid app_id or app_secret"}` = 无效

### 验证文件访问权限

```bash
curl -s 'https://open.feishu.cn/open-apis/drive/v1/files/{file_token}' \
  -H 'Authorization: Bearer {token}'
```

- 返回文件信息 = 有权限
- 返回 `{"code": 99, "msg": "file not found"}` = 无权限或文件不存在

### 验证文件夹访问

```bash
curl -s 'https://open.feishu.cn/open-apis/drive/v1/files?parent_node={folder_token}' \
  -H 'Authorization: Bearer {token}'
```

- 返回文件列表 = 有权限
- 返回空列表可能无权限或文件夹为空

## 错误处理 | Error Handling

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 99 | 文件不存在/无权限 | 检查 token 或文件是否分享给机器人 |
| 404 | API 路径错误 | 检查 API URL |
| 401 | Token 过期 | 重新获取 tenant_access_token |
| 10001 | 系统错误 | 稍后重试 |

## 文件读取示例

### Python 读取 DOCX

```python
from zipfile import ZipFile
import re

def read_docx(filepath):
    with ZipFile(filepath) as z:
        with z.open('word/document.xml') as f:
            content = f.read().decode('utf-8')
            text = re.sub(r'<[^>]+>', '', content)
            return ' '.join(text.split())
```

### 读取 PDF

```bash
pdftotext file.pdf - | head -100
```

### 读取 PPTX

```python
from pptx import Presentation

def read_pptx(filepath):
    prs = Presentation(filepath)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return '\n'.join(text)
```

## 工作流总结

1. **获取/刷新 token** → 调用 auth API
2. **提取文件 token** → 从飞书链接解析
3. **下载文件** → 调用 drive API
4. **解析内容** → 根据文件类型选择解析方法
5. **返回结果** → 给用户

## 注意事项

- Token 有时效性（约2小时），长时间操作需刷新
- 文件必须分享给机器人才能访问
- 即使文件夹可访问，未分享的文件仍会返回 404
- 大文件建议先检查文件大小：`curl -I .../download` 获取 Content-Length
