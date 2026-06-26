# Knowledge Intake Governance / 知识库资料接入治理

## Role / 角色

This module governs research intake from web pages, uploaded files, local files, cloud documents, PDFs, spreadsheets, slides, images, datasets, email attachments, and manual notes.

本模块治理来自网页、上传文件、本地文件、云端文档、PDF、表格、幻灯片、图片、数据集、邮件附件和人工笔记的研究资料接入。

## Source Types / 来源类型

```text
web_page
pdf
docx
spreadsheet
slide_deck
image
email_attachment
cloud_doc
manual_note
local_file
dataset
api_result
```

## Intake Pipeline / 接入流程

1. Receive or search material / 接收或搜索资料
2. Classify source type / 分类来源类型
3. Extract text, tables, images, metadata, and provenance / 提取文本、表格、图片、元数据和来源信息
4. Evaluate trust level / 评估可信度
5. Detect duplicates and conflicts / 检测重复和冲突
6. Stage content / 暂存内容
7. Review or auto-approve according to policy / 按策略审核或自动批准
8. Archive to knowledge base / 归档到知识库
9. Record audit log / 记录审计日志
10. Synthesize across sources / 多来源综合分析

## Trust Levels / 可信度等级

```text
trusted
allowed
review
blocked
```

## Status Values / 状态值

```text
searched
received
extracted
staged
needs-review
approved
archived
rejected
blocked
expired
superseded
```

## Default Policies / 默认策略

- Web pages from official government, standards bodies, academic institutions, or primary company sources may be `trusted` or `allowed` depending on topic.
- User-uploaded files are not automatically trusted; they are usually `allowed` or `review` until classified.
- Sensitive files such as contracts, customs documents, inspection reports, financial documents, and private email attachments require review before permanent archive.
- Spreadsheets should be checked for date range, field definitions, source provenance, formulas, and hidden assumptions before ingestion.
- Images and OCR-derived content require review unless the user confirms the extraction.
- Cloud upload requires explicit confirmation unless a trusted auto-upload policy is configured.

- 政府、标准机构、学术机构或公司一手来源网页可根据主题标记为 `trusted` 或 `allowed`。
- 用户上传文件不自动视为可信；通常先标记为 `allowed` 或 `review`。
- 合同、海关文件、检测报告、财务文件和私人邮件附件等敏感资料必须审核后才能永久归档。
- 表格入库前应检查日期范围、字段定义、来源、公式和隐藏假设。
- 图片和 OCR 内容除非用户确认，否则需要审核。
- 云端上传必须明确确认，除非已配置可信自动上传策略。

## Knowledge Record / 知识记录

Every archived item should include:

每条归档资料应包含：

- record_id
- title
- source_type
- source_name
- source_url or file_name
- file_hash when available
- topic
- market
- language
- trust_level
- status
- summary
- key_facts
- extracted_tables
- related_records
- decision
- decision_by
- decision_time
- archive_target
- audit_log_id
