---
languages:
  - en
  - zh
  - ja
---

# CJL Skills Collection

A personal Claude Code plugin providing 17 production-ready skills for research, content creation, presentation design, and workflow automation.

**English** | [简体中文](./README_zh.md) | [日本語](./README_ja.md)

---

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| `cjl-card` | `/cjl-card` | Content → PNG visuals (long cards, infographics, posters) |
| `cjl-paper` | `/cjl-paper` | Academic paper analysis pipeline |
| `cjl-paper-flow` | `/cjl-paper-flow` | Paper workflow (paper analysis + PNG card) |
| `cjl-paper-river` | `/cjl-paper-river` | Academic paper genealogy / citation tracing |
| `cjl-plain` | `/cjl-plain` | Plain language rewriter |
| `cjl-rank` | `/cjl-rank` | Dimensional reduction analysis |
| `cjl-relationship` | `/cjl-relationship` | Relationship analysis |
| `cjl-roundtable` | `/cjl-roundtable` | Multi-perspective roundtable discussion |
| `cjl-skill-map` | `/cjl-skill-map` | Visual overview of all installed skills |
| `cjl-travel` | `/cjl-travel` | City travel research workflow |
| `cjl-word` | `/cjl-word` | English word deep-dive with etymology |
| `cjl-word-flow` | `/cjl-word-flow` | Word analysis → infographic card |
| `cjl-writes` | `/cjl-writes` | Writing engine for thinking through ideas |
| `cjl-x-download` | `/cjl-x-download` | X/Twitter media downloader |
| `cjl-learn` | `/cjl-learn` | Concept dissection and learning |
| `cjl-invest` | `/cjl-invest` | Investment research and analysis |
| `cjl-slides` | `/cjl-slides` | HTML presentations in 24 international design styles |

---

## Design Philosophy

Each skill follows these principles:

- **Atomic**: One skill, one responsibility
- **Observable**: Clear input → output contract
- **Self-contained**: No external state dependencies
- **User-invocable**: Triggered via `/skill-name` or natural language

---

## Usage

### Install via Plugin

If your Claude Code supports plugin installation from GitHub:

```
/install-plugin https://github.com/0xcjl/cjl-plugin
```

### Manual Install

```bash
# Clone the repository
git clone https://github.com/0xcjl/cjl-plugin ~/.claude/plugins/cjl-plugin

# Skills will be available under ~/.claude/plugins/cjl-plugin/skills/
```

### Activate a Skill

```
/cjl-paper
/cjl-slides
/cjl-card
```

---

## Dependencies

| Skill | Dependency |
|-------|-----------|
| `cjl-card` | Node.js + Playwright |

---

## Development

See [CLAUDE.md](./CLAUDE.md) for development guidelines.

---

## Credits

Skills in this collection are adapted from [lijigang/ljg-skills](https://github.com/lijigang/ljg-skills), with skill renaming (`ljg-` → `cjl-`) and the addition of `cjl-slides`.

---

## License

MIT
