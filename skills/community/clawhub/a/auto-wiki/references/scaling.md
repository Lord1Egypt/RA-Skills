# Wiki Scaling Solution

> Default mode (grep + index.md) works for < 500 pages. Beyond that, enable SQLite index layer.
> Zero additional dependencies—Python 3 built-in sqlite3 + FTS5.

## Three-Tier Retrieval Strategy

| Tier | Page Count | Retrieval Method | Trigger |
|------|------------|------------------|---------|
| L0 | < 50 | Read index.md + directly read pages | Default |
| L1 | 50-500 | Hierarchical index + grep keywords | Auto-switch when pages > 50 |
| L2 | 500+ | SQLite FTS5 + BM25 ranking | Pages > 500 or manual enable |

---

## L1: Hierarchical Index (50-500 pages)

When page count exceeds 50, index.md splits into hierarchical structure:

```
.wiki/{topic}/
├── index.md              # Top-level index (only category summary + links to sub-indexes)
├── entities/
│   └── _index.md         # Entity sub-index (titles + one-liners for all pages in dir)
├── concepts/
│   └── _index.md         # Concept sub-index
├── sources/
│   └── _index.md         # Source sub-index
└── analyses/
    └── _index.md         # Analysis sub-index
```

**Top-level index.md becomes navigation page**:

```markdown
# {topic} Wiki Index

> 287 pages | Last updated: 2026-04-06

## Overview
- Sources: 45 → [sources/_index.md]
- Entities: 120 → [entities/_index.md]
- Concepts: 87 → [concepts/_index.md]
- Analyses: 35 → [analyses/_index.md]

## Recent Ingest (last 10)
- 2026-04-06: policy-doc → Updated 8 pages
- 2026-04-05: annual-report → Updated 5 pages
...

## Top 10 Entities (most referenced)
- [[alpha-corp]] (23 references)
- [[national-council-ssf]] (18 references)
...
```

Agent queries read top-level index to locate category, then read corresponding sub-index to locate specific pages, avoiding loading all at once.

---

## L2: SQLite FTS5 Index (500+ pages)

### Principle

Wiki pages (markdown) remain the data source. SQLite is just an index—can be rebuilt from pages if lost.

```
.wiki/{topic}/
├── search.db            # SQLite index file (auto-generated, rebuildable)
├── index.md             # Keep (for human browsing)
├── meta.yaml
└── ...
```

### Schema

```sql
-- Pages table
CREATE TABLE pages (
    slug TEXT PRIMARY KEY,        -- Filename (without .md)
    type TEXT NOT NULL,           -- source/entity/concept/analysis
    title TEXT NOT NULL,
    content TEXT NOT NULL,         -- Full body text
    confidence TEXT DEFAULT 'high',
    created TEXT,
    updated TEXT,
    sources TEXT                   -- JSON array of source slugs
);

-- FTS5 full-text index (built-in BM25 ranking)
CREATE VIRTUAL TABLE pages_fts USING fts5(
    title,
    content,
    content='pages',
    content_rowid='rowid',
    tokenize='unicode61'          -- Supports Chinese tokenization
);

-- Wikilink relationship table
CREATE TABLE links (
    from_slug TEXT NOT NULL,
    to_slug TEXT NOT NULL,
    PRIMARY KEY (from_slug, to_slug)
);

-- Trigger: Auto-update FTS index when pages change
CREATE TRIGGER pages_ai AFTER INSERT ON pages BEGIN
    INSERT INTO pages_fts(rowid, title, content)
    VALUES (new.rowid, new.title, new.content);
END;
```

### Index Build Script

Agent auto-executes after ingest (if search.db exists):

```python
#!/usr/bin/env python3
"""Rebuild SQLite FTS5 index from wiki markdown files."""
import sqlite3, os, re, json, yaml
from pathlib import Path

def parse_page(path):
    """Parse markdown page, extract frontmatter and body."""
    text = path.read_text(encoding='utf-8')
    if text.startswith('---'):
        _, fm, body = text.split('---', 2)
        meta = yaml.safe_load(fm)
        return meta, body.strip()
    return {}, text

def extract_links(content):
    """Extract [[wikilink]]."""
    return re.findall(r'\[\[([^\]]+)\]\]', content)

def build_index(wiki_dir):
    db_path = wiki_dir / 'search.db'
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()

    # Create tables (if not exist)
    c.executescript('''
        CREATE TABLE IF NOT EXISTS pages (
            slug TEXT PRIMARY KEY, type TEXT, title TEXT,
            content TEXT, confidence TEXT, created TEXT,
            updated TEXT, sources TEXT
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS pages_fts USING fts5(
            title, content, content='pages', content_rowid='rowid',
            tokenize='unicode61'
        );
        CREATE TABLE IF NOT EXISTS links (
            from_slug TEXT, to_slug TEXT,
            PRIMARY KEY (from_slug, to_slug)
        );
    ''')

    # Clear and rebuild
    c.execute('DELETE FROM pages')
    c.execute('DELETE FROM links')
    c.execute("INSERT INTO pages_fts(pages_fts) VALUES('delete-all')")

    # Traverse all md files
    for subdir in ['sources', 'entities', 'concepts', 'analyses']:
        dir_path = wiki_dir / subdir
        if not dir_path.exists():
            continue
        for f in dir_path.glob('*.md'):
            if f.name.startswith('_'):
                continue
            slug = f.stem
            meta, body = parse_page(f)
            c.execute(
                'INSERT OR REPLACE INTO pages VALUES (?,?,?,?,?,?,?,?)',
                (slug, meta.get('type',''), meta.get('title',''),
                 body, meta.get('confidence','high'),
                 meta.get('created',''), meta.get('updated',''),
                 json.dumps(meta.get('sources',[])))
            )
            for link in extract_links(body):
                c.execute('INSERT OR IGNORE INTO links VALUES (?,?)', (slug, link))

    # Rebuild FTS
    c.execute("INSERT INTO pages_fts(pages_fts) VALUES('rebuild')")

    conn.commit()
    count = c.execute('SELECT COUNT(*) FROM pages').fetchone()[0]
    conn.close()
    return count

if __name__ == '__main__':
    import sys
    wiki_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    n = build_index(wiki_dir)
    print(f'Indexed {n} pages → {wiki_dir}/search.db')
```

### Query Method

Agent uses Python to query SQLite in query operation:

```python
#!/usr/bin/env python3
"""BM25 search wiki pages."""
import sqlite3, sys, json

def search(db_path, query, limit=10):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # BM25 ranking: FTS5 built-in, smaller rank = more relevant
    results = c.execute('''
        SELECT p.slug, p.type, p.title, p.confidence,
               snippet(pages_fts, 1, '>>>', '<<<', '...', 30) as snippet,
               rank
        FROM pages_fts
        JOIN pages p ON pages_fts.rowid = p.rowid
        WHERE pages_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    ''', (query, limit)).fetchall()
    conn.close()
    return results

if __name__ == '__main__':
    db = sys.argv[1]
    q = sys.argv[2]
    for slug, type_, title, conf, snippet, rank in search(db, q):
        print(f'[{type_}] {title} ({slug}) confidence={conf} rank={rank:.2f}')
        print(f'  {snippet}')
        print()
```

**Usage example**:

```bash
# Build index
python3 build_index.py .wiki/enterprise-annuity/

# BM25 search
python3 search.py .wiki/enterprise-annuity/search.db "trustee market share"

# Output
# [entity] Alpha Corp Pension Business (alpha-corp) confidence=high rank=-3.42
#   ...trustee>>>market share<<<approx 15%...
# [analysis] Trustee Market Landscape Comparison (trustee-market-comparison) confidence=high rank=-2.87
#   ...each>>>trustee<<<>>>market share<<<change...
```

### Backlink Query

```sql
-- Who references alpha-corp?
SELECT from_slug FROM links WHERE to_slug = 'alpha-corp';

-- Who does alpha-corp reference?
SELECT to_slug FROM links WHERE from_slug = 'alpha-corp';

-- Most isolated pages (fewest incoming links)
SELECT p.slug, p.title, COUNT(l.from_slug) as inlinks
FROM pages p
LEFT JOIN links l ON l.to_slug = p.slug
GROUP BY p.slug
ORDER BY inlinks ASC
LIMIT 10;

-- Most central pages (most referenced)
SELECT p.slug, p.title, COUNT(l.from_slug) as inlinks
FROM pages p
LEFT JOIN links l ON l.to_slug = p.slug
GROUP BY p.slug
ORDER BY inlinks DESC
LIMIT 10;
```

### Lint Enhancement

In L2 mode, lint can efficiently execute via SQL:

```sql
-- Find contested pages
SELECT slug, title FROM pages WHERE confidence = 'contested';

-- Find orphans (no incoming links + not source type)
SELECT p.slug, p.title FROM pages p
LEFT JOIN links l ON l.to_slug = p.slug
WHERE l.from_slug IS NULL AND p.type != 'source';

-- Find broken links (wikilink target doesn't exist)
SELECT l.from_slug, l.to_slug FROM links l
LEFT JOIN pages p ON p.slug = l.to_slug
WHERE p.slug IS NULL;

-- Find stale pages (6 months no update + low confidence)
SELECT slug, title, updated, confidence FROM pages
WHERE updated < date('now', '-6 months')
AND confidence IN ('low', 'medium');

-- Coverage stats
SELECT type, COUNT(*) as count,
       SUM(CASE WHEN confidence = 'contested' THEN 1 ELSE 0 END) as contested
FROM pages GROUP BY type;
```

---

## When to Upgrade

| Signal | Recommendation |
|--------|----------------|
| index.md exceeds 200 lines | Enable L1 hierarchical index |
| grep search > 5 seconds | Enable L2 SQLite index |
| Page count > 500 | Must enable L2 |
| Need backlink queries | Enable L2 (links table) |
| Need BM25 ranking | Enable L2 (FTS5) |
| Multi-user collaboration / vector retrieval | Beyond Skill scope → Migrate to external platform |

**Upgrade is non-destructive**—wiki pages (markdown) remain unchanged, only adds search.db alongside. Delete search.db, wiki remains fully usable, just falls back to grep retrieval.
