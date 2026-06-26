---
name: doc-manager
description: Manage document generation, storage, and tracking with automatic URL generation. Use when creating professional documents, reports, analyses, guides, or any content that needs to be stored with metadata, indexed, and accessed via URL. Automatically creates timestamped document folders, metadata files, maintains searchable index, and returns direct access URLs.
---

# Document Manager

Centralized document management system for creating, storing, tracking, and accessing professional documents with automatic URL generation.

## Quick Start

When generating a document:

1. **Specify document type** (Report, Analysis, Guide, etc.)
2. **Provide title and content**
3. **System creates folder** with metadata automatically
4. **Return URL** for immediate preview

## Core Workflow

### Document Creation

Each document gets a timestamped folder:

```
docs/
└── doc-{YYYYMMDD}-{slug}/
    ├── README.md          # Metadata & description
    ├── content.md         # Main content (markdown)
    └── index.json         # Tracking data (JSON)
```

### Metadata Format (README.md)

```markdown
# Document Title

**Type:** Report / Analysis / Guide / etc.
**Created:** 2026-03-30 15:50 GMT+8
**Purpose:** What this document is about
**Status:** Draft / Final / Archived

## Quick Summary
- Key point 1
- Key point 2
```

### URL Access Pattern

All documents accessible via:
```
http://45.197.148.41:18792/docs/doc-{YYYYMMDD}-{slug}/content.md
```

Example:
```
http://45.197.148.41:18792/docs/doc-20260330-deployment-guide/content.md
```

### Master Index

View all documents at:
```
http://45.197.148.41:18792/docs/INDEX.md
```

## Common Tasks

### Generate New Document

Tell me:
- Document type (Report, Analysis, Guide, Proposal, etc.)
- Title
- Content

I will:
1. Create timestamped folder
2. Generate README.md with metadata
3. Store content in content.md
4. Create index.json for tracking
5. Update INDEX.md
6. Return the URL

### List All Documents

Ask: "你目前都有哪些文档？"

I will read `docs/INDEX.md` and show all available documents with direct links.

### Update Existing Document

Request changes to any document. I will:
1. Create a new version folder (new timestamp)
2. Apply changes
3. Update INDEX.md
4. Return new URL

### Archive Old Documents

Move outdated documents to `docs/archive/` and remove from INDEX.md.

## Best Practices

- **Metadata is mandatory** - Every document needs clear README.md
- **Descriptive slugs** - Use meaningful names (e.g., `quarterly-report-q1`, not `doc1`)
- **Keep index current** - INDEX.md updated immediately after creation
- **Version by timestamp** - New versions get new timestamps, old versions stay accessible
- **Archive regularly** - Move outdated docs to archive folder

## File Structure

```
/home/node/clawd/
├── docs/
│   ├── INDEX.md                         # Master index
│   ├── doc-20260330-deployment-guide/
│   │   ├── README.md                    # Metadata
│   │   ├── content.md                   # Main content
│   │   └── index.json                   # Tracking
│   ├── doc-20260330-test/
│   │   ├── README.md
│   │   ├── content.md
│   │   └── index.json
│   └── archive/                         # Old versions
├── skills/doc-manager/
│   ├── SKILL.md                         # This file
│   └── scripts/doc-manager.py           # Management script
└── md-server.js                         # Markdown server (port 18792)
```

## Server Configuration

- **Port:** 18792
- **Base URL:** http://45.197.148.41:18792
- **Root Directory:** /home/node/clawd
- **Status:** Running

## Integration Points

When you request a document:
1. I create the folder structure
2. Generate all metadata files
3. Write content
4. Update master index
5. Send you the direct URL

You can:
- Click URL to preview immediately
- Ask for document list anytime
- Request updates to any document
- Archive old versions
