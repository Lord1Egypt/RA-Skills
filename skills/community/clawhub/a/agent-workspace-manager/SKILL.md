---
name: agent-workspace-manager
description: Manage and optimize agent workspace directory structure. Use when: (1) initializing a new agent workspace with proper structure, (2) auditing document placement to ensure files are in correct functional directories, (3) cleaning up expired or redundant content, (4) detecting need for directory structure expansion, or (5) maintaining workspace health across multiple agents. Triggers on phrases like "organize workspace", "cleanup agent directory", "workspace structure", "optimize agent files".
---

# Agent Workspace Manager

## Overview

This skill provides a systematic approach to organizing and maintaining agent workspace directories. It ensures documents are placed in appropriate functional directories, detects structure issues, and maintains content freshness.

## Core Capabilities

### 1. Structure Initialization

Initialize a standardized workspace structure for new agents:

```
workspace/
├── MEMORY.md              # Core memory index (agent reads this first)
├── memory/                # Time-based memory fragments
├── knowledge/             # Stable domain knowledge
│   └── sql/               # Core business SQL (NEW)
├── tasks/                 # Temporary/project-specific items
├── decisions/             # Decision records with rationale
├── preferences/           # User preferences and settings
├── archives/              # Expired but preserved content
│   └── sql_versions/      # Historical SQL versions (NEW)
├── templates/             # Reusable templates
│   └── sql/               # Reusable SQL templates (NEW)
└── scripts/               # Scripts and utilities (NEW)
```

**Usage:** When setting up a new workspace, create this structure to enable efficient information retrieval.

### 2. Document Classification

Every document must be placed in a directory matching its functional purpose:

| Document Type | Directory | Characteristics |
|---------------|-----------|-----------------|
| Events, conversations, time-based records | `memory/` | Has timestamp, may expire |
| Domain knowledge, technical docs | `knowledge/` | Stable, long-term valid |
| **Core business SQL** | `knowledge/sql/` | **Long-term used SQL** |
| Tasks, todos, project items | `tasks/` | Temporary, project-bound |
| Important choices with rationale | `decisions/` | Decision history, traceable |
| User habits, preferences | `preferences/` | Personalization config |
| Expired but valuable content | `archives/` | Preserved for reference |
| **Historical SQL versions** | `archives/sql_versions/` | **Deprecated SQL** |
| Reusable patterns, templates | `templates/` | Copy-paste ready |
| **Reusable SQL templates** | `templates/sql/` | **Standard queries** |
| **Scripts (.py, .sh)** | `scripts/` | **Utility scripts** |

**Classification Rule:** Before creating any document, determine its primary function. Place it in the matching directory. Never place files in incorrect directories.

### 3. Code File Classification (NEW)

Code files (SQL, Python, Shell, etc.) must follow these rules:

| File Type | Directory | Purpose |
|-----------|-----------|---------|
| `.sql` (core business) | `knowledge/sql/` | Long-term used SQL queries |
| `.sql` (templates) | `templates/sql/` | Reusable standard queries |
| `.sql` (historical) | `archives/sql_versions/` | Deprecated SQL versions |
| `.py` (scripts) | `scripts/` | Python utility scripts |
| `.sh` (scripts) | `scripts/` | Shell utility scripts |
| `.json` (config) | `config/` or root | Configuration files |

**SQL File Naming Rules:**
- ✅ **DO:** Use semantic names: `神策宽表转JSON.sql`
- ❌ **DON'T:** Use version suffixes: `神策宽表转JSON_v1.sql`, `神策宽表转JSON_最终版.sql`
- ❌ **DON'T:** Use functional suffixes: `神策宽表转JSON_修正版.sql`, `神策宽表转JSON_完整版.sql`

**When to Create New Version:**
- If SQL needs update, modify the existing file
- Archive old version to `archives/sql_versions/` with timestamp if needed
- Keep only ONE active version in `knowledge/sql/`

### 4. Workspace Health Check

Run health checks to identify issues:

- **Misplaced files:** Documents in wrong directories
- **Duplicates:** Similar content in multiple files
- **Code file duplicates:** Multiple versions of same SQL/script (NEW)
- **Stale content:** Outdated information that needs refresh
- **Orphan files:** Files without clear purpose or references
- **Naming violations:** Files with version suffixes (NEW)

**Output:** A report with specific file recommendations.

### 5. Duplicate File Detection (ENHANCED)

Detect duplicate files using these methods:

#### For Document Files (.md)
1. **Name similarity:** Files with similar names (e.g., `report-v1.md` and `report-v2.md`)
2. **Content similarity:** Files with >80% content overlap
3. **Functional similarity:** Files serving the same purpose

#### For Code Files (.sql, .py, .sh)
1. **Version suffixes:** Files with `_v1`, `_v2`, `_final`, `_修正版`, `_完整版` etc.
2. **Same functionality:** Multiple SQL files for the same transformation/query
3. **Timestamp in name:** Files with timestamps that could be archived

**Detection Command:**
```bash
# Find SQL files with version suffixes
find . -name "*.sql" -type f | grep -E "(_v[0-9]|_最终|_完整|_修正|_修复)"

# Find duplicate MD files by name pattern
find . -name "*.md" -type f | grep -E "(_v[0-9]|_最终|_完整)"
```

### 6. Content Freshness Maintenance

Maintain document freshness through:

1. **Merge:** Combine duplicate or similar files, preserving all key information
2. **Archive:** Move expired content to `archives/` with timestamp
3. **Refresh:** Update stale knowledge with latest information
4. **Prune:** Remove truly redundant content (only when no key info is lost)
5. **Consolidate:** Merge multiple versions into one, archive old versions (NEW)

**Safety Principle:** Never delete content that might contain unique valuable information. Archive instead.

### 7. Structure Extension Detection

When existing directories cannot accommodate new functional needs:

1. **Detect:** Identify documents that don't fit current categories
2. **Propose:** Suggest new directories or structure reorganization
3. **Implement:** Create new directories following naming conventions
4. **Document:** Update this skill's structure reference

**Example:** If `knowledge/` grows too large with mixed domain types, split into `knowledge/product/`, `knowledge/technical/`, `knowledge/business/`.

## Workflow

### For New Workspace Setup

1. Determine agent type (personal assistant, project manager, knowledge base, etc.)
2. See [references/structure-templates.md](references/structure-templates.md) for appropriate template
3. Create directories and initial files
4. Set up MEMORY.md as the entry point

### For Workspace Audit

1. Scan all files in workspace
2. Classify each file by function
3. Check for misplaced files
4. Detect duplicate files (including code files)
5. Generate health report
6. Propose fixes for user approval

### For Content Cleanup

1. Identify duplicates/similar files
2. Detect version-suffixed files (NEW)
3. Propose merge candidates
4. Identify expired content
5. Archive with preservation
6. Verify no key information is lost

### For Code File Cleanup (NEW)

1. Scan all code files (.sql, .py, .sh)
2. Identify files with version suffixes
3. Determine the latest/best version
4. Keep latest in appropriate directory (knowledge/sql/ or templates/sql/)
5. Archive old versions to archives/sql_versions/
6. Remove version suffixes from filenames

## Resources

### references/

- **structure-templates.md** - Pre-defined workspace templates for different agent types
- **classification-rules.md** - Detailed rules for document classification (UPDATED)

## Multi-Agent Sharing

This skill is designed to be copyable across agents:

1. Install the same skill in multiple agent workspaces
2. Each agent follows the same structure conventions
3. Shared knowledge can be exchanged between agents
4. Consistent structure enables cross-agent collaboration

## Changelog

### v1.1 (2026-03-25)
- Added code file classification rules (SQL, Python, Shell)
- Added duplicate file detection methods
- Added file naming best practices
- Enhanced workspace health check to detect version-suffixed files
- Added SQL-specific cleanup workflow
