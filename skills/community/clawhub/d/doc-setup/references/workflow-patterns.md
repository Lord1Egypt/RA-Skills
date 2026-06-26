# Workflow Patterns

## Pattern 1: Documentation from GitHub Repo

**Scenario:** User wants to organize docs from `github.com/user/repo`

**Steps:**
1. List all `.md` files in `docs/` directory
2. Map topics from filenames and headers
3. Create `00-index.md` with topic list
4. For each topic, create `NN-topic.md`:
   - Fetch raw content from GitHub
   - Summarize (not copy-paste)
   - Extract key tables/decision matrices
   - Add source link
5. Mark all as living documents

**Example:**
```
Source: github.com/openclaw/openclaw/tree/main/docs
    ↓
Topics: gateway, channels, agents, tools, models...
    ↓
Files: 00-index.md, 01-gateway.md, 02-channels.md...
```

---

## Pattern 2: Documentation from Website

**Scenario:** User wants to organize docs from `docs.example.com`

**Steps:**
1. Fetch main page / sitemap
2. Identify all linked documentation pages
3. Group by topic/category
4. Create numbered files per topic
5. Include original URLs for every section

**Challenge:** Websites don't always have clean structure. May need to infer topics from content.

---

## Pattern 3: Multi-Source Documentation

**Scenario:** User has docs from multiple sources (GitHub + website + PDF)

**Steps:**
1. Identify primary source (most authoritative)
2. Create source attribution for each file
3. Cross-reference between sources
4. Note conflicts or differences
5. Prefer primary source when conflicting

---

## Pattern 4: Living Document Maintenance

**Scenario:** Documentation was organized 3 months ago, user wants update

**Steps:**
1. Read existing `00-index.md` to see current structure
2. Check source for new/updated pages
3. Update existing files (merge changes)
4. Add new topics if needed
5. Update `Last updated:` timestamp
6. Add changelog entry if significant changes

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why Bad | Do Instead |
|--------------|---------|------------|
| Copy-paste raw docs | Wastes tokens, no value add | Summarize and structure |
| No source links | Can't verify, becomes stale | Always include URL |
| Flat structure (all in one file) | Hard to navigate | Numbered topical files |
| Static documents | Become outdated | Mark as living, update |
| Generic summaries | Lose specificity | Include verbatim quotes for key claims |

---

_Last updated: 2026-05-22
