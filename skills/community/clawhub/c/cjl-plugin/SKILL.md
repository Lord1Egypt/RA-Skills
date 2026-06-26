---
name: cjl-plugin
description: |
  CJL Skills Collection — a personal Claude Code plugin with 17 production skills.
  Use when the user wants to: read papers, create content cards, design presentations,
  analyze relationships, improve writing, research travel, learn vocabulary, and more.
user_invocable: true
version: "1.0.0"
---

# CJL Skills Collection

This is a **plugin** containing 17 individual skills. Activate any skill directly:

| Command | Description |
|---------|-------------|
| `/cjl-card` | Content → PNG visuals (infographics, posters) |
| `/cjl-paper` | Academic paper analysis |
| `/cjl-paper-flow` | Paper analysis + PNG card pipeline |
| `/cjl-paper-river` | Paper genealogy / citation tracing |
| `/cjl-plain` | Plain language rewriter |
| `/cjl-rank` | Dimensional reduction analysis |
| `/cjl-relationship` | Relationship analysis |
| `/cjl-roundtable` | Multi-perspective roundtable discussion |
| `/cjl-skill-map` | Visual overview of installed skills |
| `/cjl-travel` | City travel research workflow |
| `/cjl-word` | English word deep-dive |
| `/cjl-word-flow` | Word analysis → infographic card |
| `/cjl-writes` | Writing engine for idea development |
| `/cjl-x-download` | X/Twitter media downloader |
| `/cjl-learn` | Concept dissection and learning |
| `/cjl-invest` | Investment research and analysis |
| `/cjl-slides` | HTML presentations in 24 design styles |

## Installation

```
/install-plugin https://github.com/0xcjl/cjl-plugin
```

## Design Philosophy

- **Atomic**: one skill, one responsibility
- **Observable**: clear input → output contract
- **Self-contained**: no external state dependencies
- **User-invocable**: trigger via `/cjl-{name}` or natural language

## Credits

Adapted from [lijigang/ljg-skills](https://github.com/lijigang/ljg-skills), with `ljg-` → `cjl-` renaming and the addition of `cjl-slides`.
