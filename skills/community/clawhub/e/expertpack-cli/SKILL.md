---
name: expertpack-cli
description: "Run ExpertPack CLI tools for validating, fixing, graphing, and deploying packs. Use when: running ep-validate, ep-doctor, ep-graph-export, ep-strip-frontmatter, or ep-fix-broken-wikilinks on a local pack. Triggers on: 'validate pack', 'ep-validate', 'ep-doctor', 'fix pack errors', 'graph export', 'ep-graph-export', 'strip frontmatter', 'deploy pack', 'ep-strip-frontmatter'. Requires the ExpertPack repo cloned locally (github.com/brianhearn/ExpertPack) — tools live in tools/validator/."
---

# ExpertPack CLI

Local Python tools for validating, fixing, and deploying ExpertPacks. All tools operate on local files only — no network calls, no external dependencies beyond Python stdlib.

**Tool location:** `ExpertPack/tools/validator/` in the cloned repo (github.com/brianhearn/ExpertPack).

## Tools

- **ep-validate.py** — 19-check compliance validator. Must pass 0 errors before committing.
- **ep-doctor.py** — auto-fixes common issues (links, frontmatter, prefixes). Always dry-run first.
- **ep-fix-broken-wikilinks.py** — removes broken wikilinks. Safe for composites.
- **ep-graph-export.py** — generates `_graph.yaml` from wikilinks + `related:` frontmatter.
- **ep-strip-frontmatter.py** — produces a deploy copy with frontmatter stripped (source files untouched).

## Recommended Workflow

```
ep-doctor dry-run → ep-doctor --apply → ep-validate → ep-strip-frontmatter (deploy copy) → commit
```

For full command syntax and flags: read `{skill_dir}/references/cli-commands.md`.
