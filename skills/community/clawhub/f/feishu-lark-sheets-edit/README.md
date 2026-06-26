# feishu-lark-sheets-edit

> OpenClaw skill — Read, write and manage Lark/Feishu Sheets, and download Lark/Feishu cloud files via OpenAPI.

## What it does

- **Read/export** cell values from Lark/Feishu Sheets to CSV or JSON
- **Write/update** cell values (single range or batch)
- **Add** new sheet tabs to a spreadsheet
- **Clone** an existing sheet tab's values into a new tab
- **List** all sheet tabs in a spreadsheet
- **Download** cloud files (PDF, documents, etc.) from Lark/Feishu Drive
- **Extract** text and images from downloaded PDFs automatically (pdfplumber + pypdf, auto pip-installed)
- **Garbled PDF fallback**: renders pages to images for AI visual reading (scanned docs, special fonts)

## Installation

```bash
clawhub install feishu-lark-sheets-edit
```

Or search and install from within OpenClaw:

```bash
clawhub search feishu-lark-sheets-edit
```

Once installed, use `/feishu-lark-sheets-edit` in any OpenClaw session.

## Quick start

```
# Read a sheet range to CSV
/feishu-lark-sheets-edit export --token SPREADSHEET_TOKEN --range 'SHEET_ID!A1:Z200' --csv /tmp/out.csv

# Write values to a range
/feishu-lark-sheets-edit write --token SPREADSHEET_TOKEN --range 'SHEET_ID!A1:C2' --values '[["a","b","c"]]'

# List all sheet tabs
/feishu-lark-sheets-edit list-sheets --token SPREADSHEET_TOKEN

# Add a new sheet tab
/feishu-lark-sheets-edit add-sheet --token SPREADSHEET_TOKEN --title 'NewSheet'

# Clone a sheet
/feishu-lark-sheets-edit clone-sheet --token SPREADSHEET_TOKEN --source-sheet-id SOURCE_SHEET_ID --title 'Copy'

# Download a cloud file (PDF auto-extracts text + images)
/feishu-lark-sheets-edit download --url "https://.../file/YOUR_FILE_TOKEN" --out /tmp/report.pdf
# → /tmp/report.pdf  (original)
# → /tmp/report.txt  (extracted text)
# → /tmp/report_images/  (extracted images)
```

## Requirements

- `python3` + `pip` on PATH
- Feishu/Lark app credentials in `~/.openclaw/openclaw.json` (under `channels.feishu`)
- The app must have the required API permissions enabled in the Feishu/Lark developer console (see below)
- PDF extraction: `pdfplumber`, `pypdf`, `pymupdf` are auto-installed via pip on first use, no system dependencies needed

## App Permissions (开发者后台权限配置)

在飞书/Lark 开发者后台 → 应用 → 权限管理中，需要开通以下权限：

### 电子表格 (Sheets)

| 权限 Scope | 说明 | 用于 |
|------------|------|------|
| `sheets:spreadsheet` | 查看、编辑和管理电子表格 | 读写单元格、添加/管理工作表 |

或使用更宽的云空间权限：

| 权限 Scope | 说明 | 用于 |
|------------|------|------|
| `drive:drive` | 查看、编辑和管理云空间中所有文件 | 包含 Sheets 读写 + 文件下载 |

> 只读场景可用 `sheets:spreadsheet:readonly` 或 `drive:drive:readonly`。

### 云文档文件下载 (Drive File Download)

开通以下任一权限即可：

| 权限 Scope | 说明 |
|------------|------|
| `drive:drive` | 查看、编辑和管理云空间中所有文件（最宽） |
| `drive:drive:readonly` | 查看、评论和下载所有文件 |
| `drive:file` | 上传和下载文件 |
| `drive:file:readonly` | 查看和下载文件 |
| `drive:file:download` | 仅下载文件（最小权限） |

### 推荐最小权限组合

| 使用场景 | 需要的 Scope |
|---------|-------------|
| 只读电子表格 | `sheets:spreadsheet:readonly` |
| 读写电子表格 | `sheets:spreadsheet` |
| 只下载文件 | `drive:file:download` |
| 读写表格 + 下载文件 | `sheets:spreadsheet` + `drive:file:download` |
| 全部功能（最简单） | `drive:drive` |

> **注意：** 除了开通权限，还需将目标电子表格/文件共享给应用（机器人）身份，应用才能访问。

## Security & Credentials

This skill reads `appId` and `appSecret` from `~/.openclaw/openclaw.json` (`channels.feishu`) to obtain Lark/Feishu API access tokens. Credentials are only sent to official Feishu/Lark OpenAPI endpoints for token exchange — they are never logged, cached, or sent elsewhere.

## Files

| File | Purpose |
|------|---------|
| `scripts/sheets_export.py` | Read/export ranges to CSV or JSON |
| `scripts/sheets_write.py` | Write cells, add/clone sheet tabs |
| `scripts/file_download.py` | Download cloud files, auto-extract PDF text and images |
| `references/lark-sheets-api.md` | Lark Sheets OpenAPI reference |
