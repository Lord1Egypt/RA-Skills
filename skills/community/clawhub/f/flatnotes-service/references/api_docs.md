# Flatnotes API 完整文档

**服务地址**: `https://your-flatnotes-host/`

## 认证

服务使用 Bearer Token 认证（如已启用）。在请求头中添加：
```
Authorization: Bearer <token>
```

## 端点列表

### 1. 健康检查
```
GET /health
```
返回: `"OK"` - 表示服务正常运行

### 2. 认证检查
```
GET /api/auth-check
```
返回: `"OK"` - 表示用户已认证

### 3. 获取笔记
```
GET /api/notes/{title}
```
参数:
- `title` (路径参数): 笔记标题

返回: Note 对象
```json
{
  "title": "string",
  "content": "string|null",
  "lastModified": number
}
```

### 4. 创建笔记
```
POST /api/notes
```
请求体:
```json
{
  "title": "string",      // 必填
  "content": "string"     // 可选
}
```

### 5. 更新笔记
```
PATCH /api/notes/{title}
```
参数:
- `title` (路径参数): 原笔记标题

请求体:
```json
{
  "newTitle": "string",   // 新标题（可选）
  "newContent": "string"  // 新内容（可选）
}
```

### 6. 删除笔记
```
DELETE /api/notes/{title}
```

### 7. 搜索笔记
```
GET /api/search?term={keyword}&sort={sort}&order={order}&limit={limit}
```
参数:
- `term` (必填): 搜索关键词
- `sort` (可选): 排序方式 - `score`|`title`|`lastModified` (默认: score)
- `order` (可选): 排序顺序 - `asc`|`desc` (默认: desc)
- `limit` (可选): 返回结果数量限制

返回: SearchResult 数组
```json
[
  {
    "title": "string",
    "lastModified": number,
    "score": number|null,
    "titleHighlights": "string|null",
    "contentHighlights": "string|null",
    "tagMatches": ["string"]|null
  }
]
```

### 8. 获取所有标签
```
GET /api/tags
```
返回: 标签字符串数组 `["tag1", "tag2", ...]`

### 9. 获取配置
```
GET /api/config
```
返回配置信息，包含认证类型等

### 10. 上传附件
```
POST /api/attachments
```
Content-Type: `multipart/form-data`

参数:
- `file`: 文件内容

返回:
```json
{
  "filename": "string",
  "url": "string"
}
```

### 11. 下载附件
```
GET /api/attachments/{filename}
```

## 数据模型

### Note
| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 笔记标题（唯一标识） |
| content | string\|null | 笔记内容（Markdown格式） |
| lastModified | number | 最后修改时间戳 |

### NoteCreate
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 笔记标题 |
| content | string | 否 | 笔记内容 |

### NoteUpdate
| 字段 | 类型 | 说明 |
|------|------|------|
| newTitle | string\|null | 新标题 |
| newContent | string\|null | 新内容 |

### SearchResult
| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 笔记标题 |
| lastModified | number | 最后修改时间 |
| score | number\|null | 搜索匹配分数 |
| titleHighlights | string\|null | 标题高亮片段 |
| contentHighlights | string\|null | 内容高亮片段 |
| tagMatches | string[]\|null | 匹配的标签 |

## 使用示例

### 创建笔记
curl 示例:
```bash
curl -X POST https://your-flatnotes-host/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "我的笔记", "content": "# 标题\n\n内容"}'
```

### 搜索笔记
curl 示例:
```bash
curl "https://your-flatnotes-host/api/search?term=关键词&sort=score&limit=10"
```

### 更新笔记
curl 示例:
```bash
curl -X PATCH https://your-flatnotes-host/api/notes/我的笔记 \
  -H "Content-Type: application/json" \
  -d '{"newContent": "# 新标题\n\n新内容"}'
```
