# Feishu Docx API Reference

## Block 类型 (Block Types)

| 类型 | 值 (Value) | 说明 |
|------|------------|------|
| page | 1 | 页面根节点 |
| text | 2 | 文本块 |
| table | 3 | 表格块 |
| list | 4 | 列表块 |
| image | 5 | 图片块 |
| file | 6 | 文件块 |
| divider | 7 | 分割线块 |
| bitable | 8 | 多维表格块 |
| code | 9 | 代码块 |

## 批量更新块 (Batch Update Blocks)

**API**: `POST /open-apis/docx/v1/documents/{document_id}/blocks/batch_update`

**请求示例**:
```json
{
  "requests": [
    {
      "update_block_request": {
        "block_id": "block_id_1",
        "text": {
          "content": "更新后的内容"
        }
      }
    }
  ]
}
```

## 追加子块 (Append Children)

**API**: `POST /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children`

**请求示例**:
```json
{
  "children": [
    {
      "block_type": 2,
      "text": {
        "content": "追加的文本",
        "text_element_style": {}
      }
    }
  ]
}
```
