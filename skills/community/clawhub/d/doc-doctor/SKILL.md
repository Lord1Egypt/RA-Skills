---
name: Doc Doctor
description: "Say 'lint my docs' to scan your markdown KB for broken links, orphan pages, and missing metadata — then auto-fix them."
version: 3.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🔍"
    homepage: https://github.com/SingggggYee/kb-lint
    os:
      - macos
      - linux
    install:
      - kind: uv
        package: kb-lint
---

# Doc Doctor

Your markdown docs have broken links, orphan pages, missing metadata, and you don't know it. This skill finds them all and fixes them for you.

## Quick start

Just say:

- **"lint my docs"** — scan your project's markdown files
- **"check my KB"** — get a health score out of 100
- **"fix my wiki"** — auto-fix broken links, missing frontmatter, bad filenames
- **"lint my memory"** — audit your Claude Code memory files

## What it checks

| Check | What it finds | Auto-fixable? |
|-------|--------------|---------------|
| Broken links | `[[wiki-links]]` pointing to nothing | Yes — fuzzy-matches the right target |
| Orphan pages | Files no other page links to | Suggests where to add links |
| Missing frontmatter | No title, tags, or metadata | Yes — generates from content |
| Thin articles | Under 100 words | Suggests outlines |
| Bad filenames | Spaces, non-kebab-case | Yes — renames + updates all references |
| Inconsistency | Mixed tag casing, date formats | Yes — normalizes |

## Links

- GitHub: [SingggggYee/kb-lint](https://github.com/SingggggYee/kb-lint)
- PyPI: `pip install kb-lint`

---

*Below are instructions for Claude Code. You can ignore this section.*

## Instructions

1. **Find the target.** User-specified path, or scan for `docs/`, `wiki/`, `notes/`, `content/`. If user says "memory", target `~/.claude/`.

2. **Run the linter.**
   ```bash
   kb-lint --version 2>/dev/null || pip install kb-lint
   kb-lint <path> --format json --severity info 2>&1
   ```
   If kb-lint unavailable, check files manually for: broken `[[wiki-links]]`, missing frontmatter, thin articles (<100 words), orphans, bad filenames.

3. **Show a health dashboard.** Score out of 100, issues grouped by category and severity, most critical first.

4. **Offer to fix.** Go beyond the CLI:
   - **Broken links**: fuzzy-match the intended target, confirm with user
   - **Frontmatter**: generate meaningful title/tags/confidence from content, get `created` date from git history
   - **Orphans**: suggest which articles should link to the orphan
   - **Thin articles**: suggest an outline, never fabricate content
   - **Filenames**: rename to kebab-case, update all references

5. **Verify.** Re-run linter, show before/after score.

**Claude Code memory mode:** For `~/.claude/` targets, also check MEMORY.md index accuracy, validate memory frontmatter, flag stale entries (>90 days), find duplicates.

**Rules:** Never fabricate content. Always show changes before applying. Respect `<!-- kb-lint-disable -->` inline comments and per-check severity overrides.
