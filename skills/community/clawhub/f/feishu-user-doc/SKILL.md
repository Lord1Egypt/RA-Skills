---
name: feishu-user-doc
description: 以用户（韩博）身份创建飞书文档，确保文档所有者直接是韩博，无需转移。
version: "1.0.0"
---

# feishu-user-doc

用 `lark-cli --as user` 创建文档，owner 直接是韩博，无需后续转移。

## 核心命令

```bash
# 创建文档（owner=韩博）
lark-cli --as user api "POST" "/open-apis/docx/v1/documents" \
  --data '{"title": "文档标题"}'

# 查看返回的 document_id
```

## 实际用法

直接告诉我「创建飞书文档 xxx」，我调用上述命令完成。

## 输出字段

返回 `document_id`（doc_token），用于后续写入内容。
