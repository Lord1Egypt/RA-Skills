---
name: feishu-doc-pipeline
display_name: Feishu Wiki Doc Pipeline
slug: feishu-doc-pipeline
summary: "Complete pipeline for reading Feishu wiki docs and downloading embedded attachments. Covers auth, node routing, and Windows path workaround. / 飞书知识库文档读取与附件下载完整流水线，涵盖分步授权、节点类型路由和 Windows 路径处理。"
categories: Feishu / Lark, Automation
topics: feishu, wiki, document, pipeline, download, attachment, lark-cli, knowledge-base, media-download, authorization
description: Complete pipeline for reading Feishu wiki documents and downloading embedded attachments. Use when the user needs to go from a wiki URL/token to reading document content, extracting embedded file tokens, and downloading files locally. Covers multi-scope authorization, obj_type routing (docx vs file nodes), and Windows path workaround. Trigger terms: wiki download, knowledge base attachments, feishu file extraction, wiki pipeline.
version: 1.0.0
tags: feishu, wiki, document, pipeline, download, attachment, lark-cli, knowledge-base, media-download, authorization
---

# Feishu Wiki Document Read & Attachment Download Pipeline

End-to-end pipeline: wiki URL/token -> resolve node -> read document -> extract embedded tokens -> download files to local disk.

## Prerequisites

- `lark-cli` installed and on PATH (typically `~/.qoderworkcn/bin/lark-cli` or `lark-cli.cmd` on Windows)
- Feishu connector enabled in QoderWork

### Required Permission Scopes

The pipeline needs up to **4 independent scopes**, depending on what the wiki contains:

| Scope | When Needed | Command |
|-------|------------|---------|
| `wiki:node:read` | Always (resolving wiki tokens) | `lark-cli auth login --scope "wiki:node:read" --no-wait --json` |
| `docx:document:readonly` | When wiki contains docx documents | `lark-cli auth login --scope "docx:document:readonly" --no-wait --json` |
| `docs:document.media:download` | When downloading embedded images/files from docx | `lark-cli auth login --scope "docs:document.media:download" --no-wait --json` |
| `drive:file:download` | When wiki nodes are uploaded files (obj_type: file) | `lark-cli auth login --scope "drive:file:download" --no-wait --json` |

**Important:** Each scope requires a separate authorization flow. Run `--no-wait --json` to get the device verification URL, have the user open it in browser, then complete with `lark-cli auth login --device-code "<code>"`.

## Core Workflow

### Step 1: Resolve Wiki Token to Node Details

Given a wiki URL (`https://xxx.feishu.cn/wiki/<wiki_token>`) or raw token:

```bash
lark-cli wiki spaces get_node --params '{"token":"<wiki_token>"}' --as user --format json
```

Response gives you:
- `node.obj_token` - the actual document/file token
- `node.obj_type` - determines the download path (critical!)
- `node.space_id` - for listing child nodes
- `node.title` - human-readable name

To list all child nodes under this node:

```bash
lark-cli wiki +node-list --space-id "<space_id>" --parent-node-token "<wiki_token>" --as user --format json
```

Or list all root-level nodes in a space:

```bash
lark-cli wiki +node-list --space-id "<space_id>" --as user --format json
```

### Step 2: Route by obj_type

This is the critical branching point. **Different obj_type values require completely different download approaches.**

#### obj_type: docx (online document)

Read the document content:

```bash
lark-cli docs +fetch --api-version v2 --doc "<obj_token>" --as user
```

The output is XML (default) or Markdown. Embedded files appear as tagged elements:
- `<image token="TOKEN">` - embedded images
- `<file token="TOKEN" name="filename.ext">` - embedded attachments
- `<sheet token="TOKEN" sheet-id="ID">` - embedded spreadsheets
- `<bitable token="TOKEN" table-id="ID">` - embedded bitables

Extract the `token` attribute from `<image>` and `<file>` tags for downloading.

#### obj_type: file (uploaded file)

The node IS the file itself (e.g., an uploaded .xlsx, .txt, .pdf). Download directly:

```bash
cd "<target_directory>" && lark-cli drive +download --file-token "<obj_token>" --output "<filename>" --as user --overwrite
```

**Do NOT use `docs +media-download` for file-type nodes** - it will return 403.

#### obj_type: sheet / bitable

Hand off to `lark-sheets` or `lark-base` skill respectively.

### Step 3: Download Files

#### For embedded media (from docx content):

```bash
cd "<target_directory>" && lark-cli docs +media-download --token "<file_token>" --output "<filename>" --as user --overwrite
```

#### For file-type wiki nodes:

```bash
cd "<target_directory>" && lark-cli drive +download --file-token "<obj_token>" --output "<filename>" --as user --overwrite
```

### Step 4: Parse Downloaded Content

After download, read and parse the files:
- `.txt` / `.md` - read directly with Read tool
- `.xlsx` - use Python (openpyxl or pandas) or the `xlsx` skill
- `.pdf` - use the `pdf` skill
- Images - use Read tool for visual inspection

## Windows Path Handling

**This is a common pitfall on Windows.** When using `--output` with an absolute path containing backslashes (e.g., `"C:\Users\...\file.xlsx"`), the quotes may be embedded into the path string, causing the file to be written to an unexpected location (typically the QoderWork installation directory).

### Correct Approach

Always `cd` to the target directory first, then use a **relative filename** for `--output`:

```bash
# CORRECT
cd "C:\Users\zhong\.qoderworkcn\workspace\xxx" && lark-cli docs +media-download --token "abc123" --output myfile.xlsx --as user --overwrite

# WRONG - file may end up in QoderWork install dir
lark-cli docs +media-download --token "abc123" --output "C:\Users\zhong\.qoderworkcn\workspace\xxx\myfile.xlsx" --as user --overwrite
```

### If Files Land in Wrong Location

Check `C:\Users\<username>\AppData\Local\Programs\QoderWork CN\` for misplaced files, then move them:

```bash
mv "/c/Users/zhong/AppData/Local/Programs/QoderWork CN/filename" "/c/Users/zhong/.qoderworkcn/workspace/xxx/"
```

## Troubleshooting

### 403 on docs +media-download

The token belongs to a wiki file node (`obj_type: file`), not an embedded media element. Switch to `drive +download --file-token <token>`.

### 403 on drive +download

The `drive:file:download` scope has not been authorized. Run:
```bash
lark-cli auth login --scope "drive:file:download" --no-wait --json
```
Then complete the device verification flow.

### Authorization loop (keeps asking for more scopes)

This happens when the pipeline encounters a new operation that needs a scope not yet authorized. To minimize back-and-forth, **pre-authorize all 4 scopes upfront** before starting the pipeline:

```bash
lark-cli auth login --scope "wiki:node:read" --no-wait --json
# complete auth, then:
lark-cli auth login --scope "docx:document:readonly" --no-wait --json
# complete auth, then:
lark-cli auth login --scope "docs:document.media:download" --no-wait --json
# complete auth, then:
lark-cli auth login --scope "drive:file:download" --no-wait --json
```

Scopes are cumulative - once authorized, they persist across sessions.

### wiki +node-list returns empty

The node may have no children, or you may be querying the wrong `space_id`. Use `wiki spaces get_node` to confirm the correct `space_id` for the node.

## Quick Reference

```
User provides wiki URL/token
        |
        v
wiki spaces get_node --> obj_token, obj_type, space_id
        |
        +--> obj_type: docx
        |       |
        |       +--> docs +fetch (read content)
        |       +--> Extract <image>/<file> tokens from XML
        |       +--> docs +media-download (per token)
        |
        +--> obj_type: file
        |       |
        |       +--> drive +download (direct)
        |
        +--> obj_type: sheet/bitable
                |
                +--> Hand off to lark-sheets / lark-base
```
