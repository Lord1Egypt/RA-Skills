# 飞书 API 参考文档

## Token 相关

### 获取 tenant_access_token

**接口**: `POST /auth/v3/tenant_access_token/internal`

**请求体**:
```json
{
  "app_id": "cli_xxx",
  "app_secret": "xxx"
}
```

**响应**:
```json
{
  "code": 0,
  "msg": "ok",
  "tenant_access_token": "t-xxx",
  "expire": 7200
}
```

**注意**: 有效期 2 小时，需提前刷新。

---

## 文档 API

### 读取文档

**接口**: `GET /docx/v1/documents/{document_id}`

**响应字段**:
- `title`: 文档标题
- `content`: 文档内容（纯文本）
- `block_count`: 块数量
- `block_types`: 块类型统计

### 列出文档块

**接口**: `GET /docx/v1/documents/{document_id}/blocks`

**块类型**:
| 类型 | 说明 |
|-----|------|
| Page | 页面 |
| Text | 文本 |
| Heading1-3 | 标题 |
| Bullet | 无序列表 |
| Ordered | 有序列表 |
| Code | 代码块 |
| Quote | 引用块 |
| Divider | 分隔线 |

### 写入文档内容

**接口**: `PUT /docx/v1/documents/{document_id}/content`

**注意**: 会替换整个文档内容。

### 追加文档内容

**接口**: `POST /docx/v1/documents/{document_id}/content`

**注意**: 
- 每次追加内容到文档末尾
- 多个 Markdown 元素会并发处理，可能乱序
- **建议**: 每次只追加一个块，保证顺序

---

## 知识库 API

### 列出知识空间

**接口**: `GET /wiki/v2/spaces`

**响应**:
```json
{
  "spaces": [
    {
      "space_id": "xxx",
      "name": "空间名称",
      "description": "描述"
    }
  ]
}
```

### 列出空间节点

**接口**: `GET /wiki/v2/spaces/{space_id}/nodes`

### 创建知识库节点

**接口**: `POST /wiki/v2/spaces/{space_id}/nodes`

**请求体**:
```json
{
  "obj_type": "docx",
  "title": "节点标题"
}
```

---

## 云空间 API

### 列出文件

**接口**: `GET /drive/v1/files`

**查询参数**:
- `folder_token`: 文件夹 token（不传则列根目录）

### 上传文件

**接口**: `POST /drive/v1/files/upload_all`

**表单参数**:
| 参数 | 说明 |
|-----|------|
| file_name | 文件名 |
| parent_type | 固定值 `explorer` |
| parent_node | 文件夹 token |
| size | 文件大小（字节） |
| file | 文件内容 |

---

## 导入 API

### 上传素材

**接口**: `POST /drive/v1/medias/upload_all`

**用途**: 上传临时文件用于导入

**表单参数**:
| 参数 | 说明 |
|-----|------|
| file_name | 文件名 |
| parent_type | 固定值 `ccm_import_open` |
| size | 文件大小 |
| extra | JSON 字符串，如 `{"obj_type":"docx","file_extension":"md"}` |
| file | 文件内容 |

### 创建导入任务

**接口**: `POST /drive/v1/import_tasks`

**请求体**:
```json
{
  "file_token": "素材token",
  "file_extension": "md",
  "type": "docx",
  "point": {
    "mount_type": 1,
    "mount_key": "目标文件夹token"
  }
}
```

**支持导入格式**:
| 源文件 | 目标类型 |
|-------|---------|
| md, mark, markdown | docx |
| txt | docx |
| docx | docx |
| doc | docx |
| xlsx, xls, csv | sheet / bitable |

### 查询导入任务

**接口**: `GET /drive/v1/import_tasks/{ticket}`

**响应**:
```json
{
  "result": {
    "job_status": 0,  // 0=成功
    "token": "文档token",
    "url": "文档链接"
  }
}
```

---

## 错误码速查

| 错误码 | 说明 | 处理 |
|-------|------|------|
| 0 | 成功 | - |
| 9499 | 参数类型错误 | 检查数据类型 |
| **1061045** | **频率限制（重要）** | **立即停止，sleep 1-2秒后重试，降低请求频率** |
| 1062008 | checksum 错误 | 检查文件校验 |
| 1062009 | 文件大小不匹配 | 检查 size 参数 |
| 99992402 | 参数验证失败 | 检查必填字段 |

### 错误码 1061045 详细处理

**触发条件**：
- 每秒请求超过 5 次（QPS > 5）
- 或单日请求超过 10,000 次

**处理步骤**：
1. 立即停止当前批量操作
2. 添加延迟：`sleep 1` 或 `sleep 0.2`
3. 降低并发数，确保 QPS ≤ 5
4. 重试失败的请求

**预防方法**：
```bash
# 批量操作时添加间隔
for item in "${items[@]}"; do
    # 执行 API 调用
    feishu_api_call "$item"
    
    # 每5个请求暂停1秒
    count=$((count + 1))
    if [ $((count % 5)) -eq 0 ]; then
        sleep 1
    fi
done
```

---

## 最佳实践

1. **Token 管理**: 使用缓存机制，避免频繁获取
2. **文档写入**: 单块逐个追加，保证顺序
3. **文件导入**: 使用素材上传接口，非直接上传
4. **错误处理**: 检查 code 字段，非 0 即失败
5. **频率控制**: 注意 QPS 限制（5 QPS）
