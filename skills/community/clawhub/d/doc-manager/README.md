# doc-manager Skill

Document management system for OpenClaw with automatic URL generation and tracking.

## Features

- ✅ Automatic document folder creation with timestamps
- ✅ Metadata generation (README.md, index.json)
- ✅ Master index maintenance (INDEX.md)
- ✅ Direct URL access to all documents
- ✅ Document versioning via timestamps
- ✅ Archive management
- ✅ Markdown rendering to HTML

## Quick Start

### Generate a Document

```python
python3 scripts/doc-manager.py create "Report Title" "Report" content.md
```

### List All Documents

```python
python3 scripts/doc-manager.py list
```

### Update Index

```python
python3 scripts/doc-manager.py update-index
```

### Archive a Document

```python
python3 scripts/doc-manager.py archive report-q1
```

## File Structure

```
doc-manager/
├── SKILL.md                 # Skill documentation
├── scripts/
│   └── doc-manager.py       # Management script
└── README.md                # This file
```

## Configuration

- **Base URL:** http://45.197.148.41:18792
- **Docs Root:** /home/node/clawd/docs
- **Server Port:** 18792
- **Markdown Server:** Node.js (md-server.js)

## Usage in OpenClaw

When you ask me to generate a document:

1. I create a timestamped folder: `doc-{YYYYMMDD}-{slug}/`
2. Generate metadata files (README.md, index.json)
3. Store content in content.md
4. Update INDEX.md
5. Return the direct URL

You can then:
- Click the URL to preview
- Ask "你目前都有哪些文档？" to list all
- Request updates or archival

## Document URL Format

```
http://45.197.148.41:18792/docs/doc-{YYYYMMDD}-{slug}/content.md
```

Example:
```
http://45.197.148.41:18792/docs/doc-20260330-deployment-guide/content.md
```

## Master Index

View all documents:
```
http://45.197.148.41:18792/docs/INDEX.md
```
