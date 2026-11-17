# Feishu Wiki Document Read & Attachment Download Pipeline
# 飞书知识库文档读取与附件下载流水线

End-to-end pipeline for reading Feishu wiki documents and downloading embedded attachments to local disk.

从飞书知识库文档中读取内容并下载嵌入附件到本地的完整流水线。

## What it does / 功能说明

Takes you from a Feishu wiki URL or token all the way to downloaded files on your machine:

从一个飞书知识库 URL 或 token 出发，完成以下全流程：

1. **Resolve / 解析节点** — wiki token -> node details (obj_type, obj_token, space_id)
2. **Read / 读取文档** — document content and extract embedded file/image tokens
3. **Download / 下载文件** — attachments using the correct method based on node type
4. **Parse / 解析内容** — downloaded files (.xlsx, .txt, .md, .pdf, etc.)

## When to use / 使用场景

- User shares a Feishu wiki URL and wants to read or download its contents
  用户分享了一个飞书知识库链接，需要读取或下载其中的内容
- User needs to extract attachments (Office files, images, PDFs) from wiki documents
  需要从知识库文档中提取附件（Office 文件、图片、PDF 等）
- You need to handle the "which download method?" question (docs +media-download vs drive +download)
  需要判断使用哪种下载方式（docs +media-download 还是 drive +download）

## Key gotchas covered / 覆盖的关键坑点

- **obj_type routing / 节点类型路由**: `docx` nodes use `docs +fetch` + `docs +media-download`; `file` nodes use `drive +download`. Using the wrong method returns 403.
  `docx` 类型节点用 `docs +fetch` 加 `docs +media-download`；`file` 类型节点用 `drive +download`。用错方法会返回 403。
- **Windows path bug / Windows 路径问题**: `--output` with absolute backslash paths writes files to the wrong directory. The skill documents the `cd` + relative path workaround.
  在 Windows 上使用反斜杠绝对路径会导致文件写入错误目录，技能文档中记录了 `cd` + 相对路径的解决方案。
- **Multi-scope auth / 多权限分步授权**: Up to 4 independent authorization flows may be needed. The skill provides a pre-auth checklist to minimize back-and-forth.
  最多需要 4 个独立的授权流程，技能提供了预授权清单以减少反复操作。

## Prerequisites / 前置条件

- `lark-cli` installed (via Feishu connector in QoderWork)
  已安装 `lark-cli`（通过 QoderWork 的飞书连接器）
- Feishu connector enabled
  已启用飞书连接器

## Tags

feishu, wiki, document, pipeline, download, attachment, lark-cli, knowledge-base, media-download, authorization

## Related skills / 相关技能

This pipeline orchestrates commands from `lark-wiki`, `lark-doc`, and `lark-drive`. If you only need individual operations, use those skills directly.

本流水线编排了 `lark-wiki`、`lark-doc` 和 `lark-drive` 三个技能的命令。如果只需要单独操作，可直接使用对应技能。
