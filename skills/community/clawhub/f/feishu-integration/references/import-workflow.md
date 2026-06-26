# Markdown 导入工作流

## 场景

将本地 Markdown 文件导入为飞书在线文档（docx）。

## 流程概览

```
本地 MD 文件
    ↓
上传素材 → 获取 file_token
    ↓
创建导入任务 → 获取 ticket
    ↓
轮询查询 → 获取 doc_token
    ↓
飞书在线文档
```

## 详细步骤

### 步骤 1: 上传素材

**接口**: `POST /drive/v1/medias/upload_all`

```bash
curl -X POST "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all" \
  -H "Authorization: Bearer ${TOKEN}" \
  -F "file_name=demo.md" \
  -F "parent_type=ccm_import_open" \
  -F "size=478" \
  -F 'extra={"obj_type":"docx","file_extension":"md"}' \
  -F "file=@demo.md"
```

**关键参数**:
- `parent_type`: 固定值 `ccm_import_open`
- `extra`: JSON 字符串，指定导入目标类型

**响应**:
```json
{
  "code": 0,
  "data": {
    "file_token": "AzjybrDgHoeeY2xGPYrcZnV7nys"
  }
}
```

### 步骤 2: 创建导入任务

**接口**: `POST /drive/v1/import_tasks`

```bash
curl -X POST "https://open.feishu.cn/open-apis/drive/v1/import_tasks" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "file_token": "AzjybrDgHoeeY2xGPYrcZnV7nys",
    "file_extension": "md",
    "type": "docx",
    "point": {
      "mount_type": 1,
      "mount_key": "nodcnJ9crfeKQuquKgkUgcRh2ag"
    }
  }'
```

**关键参数**:
- `file_token`: 步骤 1 返回的 token
- `point.mount_key`: 目标文件夹 token
- `point.mount_type`: 固定值 `1`

**响应**:
```json
{
  "code": 0,
  "data": {
    "ticket": "7605680347254590654"
  }
}
```

### 步骤 3: 查询导入结果

**接口**: `GET /drive/v1/import_tasks/{ticket}`

```bash
curl -X GET "https://open.feishu.cn/open-apis/drive/v1/import_tasks/7605680347254590654" \
  -H "Authorization: Bearer ${TOKEN}"
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "result": {
      "job_status": 0,
      "token": "V4mYdLUc3oIAklxG1ducsbTQnKc",
      "url": "https://moxunkeji.feishu.cn/docx/V4mYdLUc3oIAklxG1ducsbTQnKc"
    }
  }
}
```

**job_status 说明**:
| 值 | 含义 |
|---|------|
| 0 | 成功 |
| 1 | 进行中 |
| 2 | 失败 |

## 一键导入脚本

使用封装好的函数：

```bash
source /path/to/feishu-api.sh

# 导入 Markdown
feishu_import_md "/path/to/file.md" "folder_token"
```

或命令行：

```bash
./feishu-api.sh import-md /path/to/file.md folder_token
```

## 支持的导入格式

| 源格式 | 扩展名 | 目标类型 |
|-------|-------|---------|
| Markdown | .md, .mark, .markdown | docx |
| 文本 | .txt | docx |
| Word | .docx | docx |
| Word 97-2003 | .doc | docx |
| Excel | .xlsx | sheet / bitable |
| Excel 97-2003 | .xls | sheet |
| CSV | .csv | sheet / bitable |

## 格式兼容性

### 完全支持 ✅

- 标题层级（H1-H6）
- 粗体、斜体
- 有序/无序列表
- 分隔线
- 代码块
- 引用块

### 部分支持 ⚠️

- 表格（转换为飞书表格，样式可能变化）
- 图片（需保证可访问性）
- 链接（保留，但需手动确认）

### 不支持 ❌

- HTML 标签
- 数学公式（LaTeX）
- Mermaid 图表

## 最佳实践

1. **预处理 Markdown**: 移除不支持的格式
2. **图片处理**: 使用网络图片 URL，非本地路径
3. **分批导入**: 大文件拆分，避免超时
4. **验证结果**: 导入后检查格式是否正确

## 故障排查

### 导入失败

检查 `job_status` 和 `job_error_msg`：

```bash
curl ... | jq '.data.result'
```

常见错误：
- `1061109`: 文件名不合规
- `1062009`: 文件大小不匹配
- `1061043`: 文件超出大小限制

### 格式丢失

- 检查 Markdown 语法是否标准
- 避免嵌套过深的结构
- 特殊字符需转义
