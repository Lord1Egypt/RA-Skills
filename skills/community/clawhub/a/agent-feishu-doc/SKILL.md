---
name: agent-feishu-doc
description: "Guide for OpenClaw agents to create, read, and edit Feishu/Lark documents via API. Use when: (1) creating a new Feishu doc and writing content, (2) reading an existing doc by ID or URL, (3) setting document permissions to public/anyone editable, (4) troubleshooting agent-to-agent Feishu doc collaboration. Triggers on: 飞书文档, create Feishu doc, write to Feishu doc, feishu_doc tool."
---

# Agent Feishu Doc Guide

## Quick Reference

| Operation | API Endpoint |
|----------|--------------|
| Create doc | `POST /drive/v1/documents` |
| Get doc metadata | `GET /drive/v1/documents/{id}` |
| Get doc blocks | `GET /drive/v1/documents/{id}/blocks` |
| Add blocks | `POST /drive/v1/documents/{id}/blocks/{parent_id}/children` |
| Set public perm | `PATCH /drive/v1/permissions/{id}/public?type=docx` |

## Workflow

### 1. Create Document
```bash
curl -X POST "https://open.feishu.cn/open-apis/drive/v1/documents" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"title": "文档标题"}'
```

### 2. Write Content (Block API)
```bash
curl -X POST "https://open.feishu.cn/open-apis/drive/v1/documents/{doc_id}/blocks/{block_id}/children" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"children": [{"block_type": 2, "text": {"elements": [{"text_run": {"content": "内容"}}]}}]}'
```

**Block types:** `2`=text, `3`=h1, `4`=h2, `7`=bullet (⚠️ may error, use text instead)

### 3. Set Public Permissions
```bash
curl -X PATCH "https://open.feishu.cn/open-apis/drive/v1/permissions/{doc_id}/public?type=docx" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "link_share_entity": "anyone_editable",
    "external_access_entity": "anyone_can_edit",
    "security_entity": "anyone_can_edit",
    "comment_entity": "anyone_can_edit",
    "share_entity": "anyone"
  }'
```

## Reading Docs
- **By URL**: Use `web_fetch` tool on `https://feishu.cn/docx/{doc_id}`
- **By ID**: Call GET `/drive/v1/documents/{id}` then `/blocks`

## Prerequisites
1. Agent's Feishu app must be added as doc collaborator, OR doc set to public
2. For cross-agent collaboration: set `tools.sessions.visibility: "all"` in openclaw.json

## Troubleshooting
- **Cannot access doc**: Add agent's app as collaborator in Feishu, or set doc to public
- **Block API error 9499**: Avoid `block_type: 7` (bullet), use plain text blocks instead
- **Cross-agent visibility**: Add `"tools": {"sessions": {"visibility": "all"}}` to openclaw.json

For detailed API specs, permissions guide, and example workflows, see `references/guide.md`.
