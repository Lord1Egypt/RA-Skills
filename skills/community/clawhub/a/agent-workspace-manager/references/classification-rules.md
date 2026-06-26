# Document Classification Rules

Detailed rules for determining where each document belongs.

## Classification Decision Tree

```
START: What is the primary purpose of this document?
│
├─► Records an event, conversation, or time-based info
│   └─► memory/
│
├─► Contains stable knowledge that won't change often
│   └─► knowledge/
│
├─► Relates to work that needs to be done
│   └─► tasks/
│
├─► Explains why a choice was made
│   └─► decisions/
│
├─► Defines how the user likes things done
│   └─► preferences/
│
├─► Is a pattern or format to reuse
│   └─► templates/
│
└─► Is outdated but might have value
    └─► archives/
```

## Detailed Category Definitions

### memory/

**Purpose:** Time-based records that may expire or become outdated.

**Include:**
- Conversations with timestamps
- Event logs
- Daily/weekly summaries
- Session records
- Notifications received

**Exclude:**
- Timeless knowledge (→ knowledge/)
- Ongoing tasks (→ tasks/)
- Preferences (→ preferences/)

**Naming convention:** `{YYYY-MM-DD}-{topic}.md` or `{category}/{topic}.md`

### knowledge/

**Purpose:** Stable information that remains valid over time.

**Include:**
- Domain expertise
- Technical documentation
- Reference materials
- How-to guides
- Concept explanations

**Exclude:**
- Time-sensitive info (→ memory/)
- Tasks (→ tasks/)
- Personal preferences (→ preferences/)

**Naming convention:** `{domain}-{topic}.md` or `{domain}/{topic}.md`

### tasks/

**Purpose:** Work items with clear action or completion criteria.

**Include:**
- Active tasks
- Todo items
- Project items
- Work in progress
- Pending requests

**Exclude:**
- Completed work (→ archives/)
- Decisions (→ decisions/)
- Reference info (→ knowledge/)

**Naming convention:** `{status}-{task-name}.md` or `{status}/{task-name}.md`

### decisions/

**Purpose:** Records of significant choices and their rationale.

**Include:**
- Major decisions with reasoning
- Trade-off analyses
- Option comparisons
- Policy choices

**Exclude:**
- Task lists (→ tasks/)
- General knowledge (→ knowledge/)
- Meeting notes (→ memory/)

**Naming convention:** `{YYYY-MM-DD}-{decision-topic}.md`

### preferences/

**Purpose:** User-specific settings and preferences.

**Include:**
- Communication style preferences
- Tool preferences
- Formatting preferences
- Personal settings

**Exclude:**
- Tasks (→ tasks/)
- Knowledge (→ knowledge/)
- Decisions (→ decisions/)

**Naming convention:** `{category}-preferences.md`

### templates/

**Purpose:** Reusable patterns and formats.

**Include:**
- Document templates
- Code templates
- Message templates
- Report formats

**Exclude:**
- Actual documents (→ appropriate directory)
- Knowledge about templates (→ knowledge/)

**Naming convention:** `{purpose}-template.md`

### archives/

**Purpose:** Preserved content that is no longer active.

**Include:**
- Completed tasks
- Expired information
- Historical records
- Deprecated content

**Exclude:**
- Active content (→ appropriate directory)

**Naming convention:** `{YYYY-MM-DD}-{original-name}.md`

## Common Misclassification Examples

| Wrong Placement | Correct Placement | Reason |
|-----------------|-------------------|--------|
| `knowledge/daily-log.md` | `memory/daily-log.md` | Daily logs are time-based |
| `tasks/api-reference.md` | `knowledge/api-reference.md` | API reference is stable knowledge |
| `memory/user-preferences.md` | `preferences/user-preferences.md` | Preferences are not time-based |
| `knowledge/archived-project.md` | `archives/archived-project.md` | Archived content belongs in archives |
| `tasks/decision-001.md` | `decisions/decision-001.md` | Decisions have their own category |

## Content Freshness Indicators

Signs a document needs attention:

- **Expired:** Timestamp > retention period, content no longer relevant
- **Duplicate:** Similar content exists in multiple files
- **Stale:** Known to be outdated by newer information
- **Orphan:** No references, unclear purpose
- **Misplaced:** In wrong directory for its function

## Code File Classification (NEW)

### SQL Files (.sql)

| Type | Directory | Example |
|------|-----------|---------|
| Core business SQL | `knowledge/sql/` | `神策宽表转JSON.sql` |
| Query templates | `templates/sql/` | `每日简报查询.sql` |
| Historical versions | `archives/sql_versions/` | `神策宽表转JSON_v1.sql` |
| Test/validation SQL | `scripts/` | `test_unique_id.sql` |

**Naming Rules:**
- ✅ **DO:** `神策宽表转JSON.sql` (semantic name)
- ❌ **DON'T:** `神策宽表转JSON_v1.sql` (version number)
- ❌ **DON'T:** `神策宽表转JSON_最终版.sql` (functional suffix)
- ❌ **DON'T:** `神策宽表转JSON_修正版.sql` (functional suffix)

**Version Management:**
1. Keep only ONE active version in `knowledge/sql/`
2. Archive old versions to `archives/sql_versions/`
3. Use timestamp prefix if needed: `20260325_神策宽表转JSON.sql`

### Python Files (.py)

| Type | Directory | Example |
|------|-----------|---------|
| Utility scripts | `scripts/` | `query_daily_report.py` |
| Core scripts | `scripts/` | `data_processor.py` |

### Shell Files (.sh)

| Type | Directory | Example |
|------|-----------|---------|
| Utility scripts | `scripts/` | `backup.sh` |
| Automation scripts | `scripts/` | `daily_cleanup.sh` |

## Duplicate File Detection

### Detection Methods

#### 1. Name Pattern Detection

Find files with version suffixes:
```bash
# SQL files with version patterns
find . -name "*.sql" | grep -E "(_v[0-9]|_最终|_完整|_修正|_修复|_简化|_精确)"

# Markdown files with version patterns
find . -name "*.md" | grep -E "(_v[0-9]|_最终|_完整)"
```

#### 2. Content Similarity Detection

Files with >80% content overlap are duplicates.

#### 3. Functional Similarity Detection

Multiple files serving the same purpose (e.g., multiple "神策宽表转JSON" SQL files).

### Handling Duplicates

```
Found duplicate files?
│
├─► Is there a clear latest version?
│   │
│   ├─► Yes: 
│   │   1. Keep latest in appropriate directory
│   │   2. Archive others with timestamp
│   │   3. Remove version suffixes
│   │
│   └─► No: 
│       1. Compare modification times
│       2. Compare file sizes
│       3. Review content to determine best version
│
└─► Archive process:
    1. mv file_v2.sql ../archives/sql_versions/file.sql
    2. Document which version was kept
```

## Merge vs Archive Decision

```
Is the content unique and valuable?
│
├─► Yes: Can it be merged with a similar file?
│        │
│        ├─► Yes: Merge, preserve all key info
│        │
│        └─► No: Archive with timestamp
│
└─► No: Is it completely redundant?
         │
         ├─► Yes: Safe to remove
         │
         └─► No: Archive (be conservative)
```

## File Naming Best Practices

### DO (Recommended)

- ✅ Use semantic names: `api-reference.md`, `神策宽表转JSON.sql`
- ✅ Use timestamps for archives: `20260325_old_report.md`
- ✅ Use hyphens for multi-word names: `daily-report.md`
- ✅ Keep names concise but descriptive

### DON'T (Avoid)

- ❌ Version numbers: `report_v1.md`, `report_v2.md`
- ❌ Functional suffixes: `report_final.md`, `report_完整版.md`
- ❌ Status suffixes: `report_done.md`, `report_已完成.md`
- ❌ Person names: `张政_report.md`
- ❌ Overly long names: `detailed_comprehensive_user_behavior_analysis_report_20260325.md`

### When to Create New File

- Different purpose → New file
- Same purpose, content update → Update existing file, archive old version
- Same purpose, major restructure → New file with clear name, archive old

## Common Misclassification Examples (Updated)

| Wrong Placement | Correct Placement | Reason |
|-----------------|-------------------|--------|
| `knowledge/daily-log.md` | `memory/daily-log.md` | Daily logs are time-based |
| `tasks/api-reference.md` | `knowledge/api-reference.md` | API reference is stable knowledge |
| `memory/user-preferences.md` | `preferences/user-preferences.md` | Preferences are not time-based |
| `knowledge/archived-project.md` | `archives/archived-project.md` | Archived content belongs in archives |
| `tasks/decision-001.md` | `decisions/decision-001.md` | Decisions have their own category |
| `docs/神策宽表转JSON.sql` | `knowledge/sql/神策宽表转JSON.sql` | SQL belongs in knowledge/sql/ (NEW) |
| `神策宽表转JSON_v2.sql` | `archives/sql_versions/神策宽表转JSON_v2.sql` | Old versions belong in archives (NEW) |
| `神策宽表转JSON_最终版.sql` | Rename to `神策宽表转JSON.sql` | Remove functional suffixes (NEW) |
