---
name: feishu-docx
description: 飞书云文档（docx）的创建与编辑技能。支持通过 API 创建文档、追加内容、批量更新块等操作。使用此技能需要提供 App ID 和 App Secret。
---

# Feishu Docx Skill

本技能封装了飞书云文档（docx）API 的核心操作，允许老大快速对飞书文档进行读写操作。

## 认证信息

使用该技能前，需确保已设置以下环境变量或在代码中显式传入：
- `FEISHU_APP_ID`: cli_a92c5076b7789cd2
- `FEISHU_APP_SECRET`: 9jPdCn49G54RFoEoDPUCVcptnWZnTZqp

## 核心工作流

1. **获取访问令牌**: 使用 `tenant_access_token` 进行应用级别的认证。
2. **创建文档**: 调用 `POST /open-apis/docx/v1/documents` 创建一个空的或指定标题的文档。
3. **写入/编辑内容**:
    - 追加块：`POST /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children`
    - 批量更新：`POST /open-apis/docx/v1/documents/{document_id}/blocks/batch_update`

## 使用示例 (Python)

```python
from scripts.feishu_docx_client import FeishuDocx

client = FeishuDocx(app_id="cli_a92c5076b7789cd2", app_secret="9jPdCn49G54RFoEoDPUCVcptnWZnTZqp")

# 1. 创建文档
doc_id = client.create_document("测试文档")

# 2. 追加文本
client.append_text(doc_id, "这是由 OpenClaw 写入的内容。")
```

## 资源

- **客户端脚本**: `scripts/feishu_docx_client.py` 封装了常用的 API 调用。
- **参考文档**: 请参考 [REFERENCES.md](references/api_reference.md) 了解更多 Block 类型和 API 细节。
