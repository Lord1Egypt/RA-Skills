---
name: feishu-doc-exporter
description: Feishu Document Exporter - Batch export Feishu docs to markdown/PDF
metadata:
  openclaw:
    requires:
      bins: []
---

# Feishu Document Exporter

Batch export Feishu documents to markdown or PDF format, features:
- Batch export entire folders
- Preserve document structure and formatting
- Export images as local files
- Support nested folder hierarchy
- Generate table of contents
- Support incremental export

## Usage

```bash
# Export single document to markdown
openclaw feishu-doc-exporter export --url "https://example.com/docx/xxx" --format markdown --output ./export

# Export entire folder recursively
openclaw feishu-doc-exporter export --folder "folder_token" --format pdf --output ./export --recursive

# List all documents in a folder
openclaw feishu-doc-exporter list --folder "folder_token"
```

## Configuration

Required Feishu API permissions:
- `doc:document:read`
- `drive:folder:read`
- `drive:file:read`
