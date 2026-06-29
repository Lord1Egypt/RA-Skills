---
name: axiom-markdown-link-auditor
description: Markdown link auditor — find broken internal links, flag dead external links (HEAD requests), report orphan pages. Use when you maintain docs. Pure stdlib + urllib (no LLM).
version: 0.1.2
license: Apache-2.0
---

# axiom-markdown-link-auditor

**Version:** 0.1.2
**Axioma Tools**

Audits a markdown documentation set for broken links and orphan pages.

## What this skill does

- Finds broken internal links
- Optional HEAD-check on external links
- Reports orphan pages (no incoming links)
- JSON output for CI integration

## When to use this skill

- ✅ Audit docs before deployment
- ✅ CI gate on broken links
- ✅ Find orphan pages in your wiki
- ❌ Render markdown to HTML (use a markdown lib)

## Usage

```bash
python3 axiom_markdown_link_auditor.py ./docs/
python3 axiom_markdown_link_auditor.py README.md --check-external --json
```

```python
from axiom_markdown_link_auditor import audit_directory
report = audit_directory('./docs/')
# {broken: [...], orphans: [...], total_links: 123}
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 15+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
