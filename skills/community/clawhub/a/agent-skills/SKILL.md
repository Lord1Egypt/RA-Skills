---
name: agent-skills
description: Agent Skills standard reference guide. Covers SKILL.md specification format, progressive disclosure mechanism, skill discovery and activation, frontmatter metadata fields, directory structure conventions. 
---

# Agent Skills

> A standardized way to give AI agents new capabilities and expertise.
> 35+ agent products support it: Claude Code, GitHub Copilot, Cursor, Pi, Codex, Gemini CLI, and more.

## Use Cases 

Use when creating new skills, validating skill formats, or understanding the standardized skill system design.

## Directory Structure

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + Markdown instructions
├── scripts/          # Optional: executable scripts
├── references/       # Optional: on-demand reference docs
├── assets/           # Optional: templates, resource files
└── ...               # Any additional files
```

## SKILL.md Format

### Frontmatter

| Field | Required | Constraints |
|------|----------|-------------|
| `name` | ✅ | 1-64 chars, lowercase/numbers/hyphens, no leading/trailing hyphens, no consecutive hyphens, must match directory name |
| `description` | ✅ | 1-1024 chars, describe what it does and when to use |
| `license` | — | License name or reference |
| `compatibility` | — | ≤500 chars, environment requirements |
| `metadata` | — | Arbitrary key-value pairs |
| `allowed-tools` | — | Space-separated pre-approved tool list (experimental) |

### Minimal Example

```markdown
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
---
```

### Body Content

Markdown body after frontmatter, no format restrictions. Recommended: step-by-step instructions, input/output examples, common edge cases. Split to `references/` if over 500 lines.

## Progressive Disclosure (Three Tiers)

| Tier | What's Loaded | When | Token Cost |
|------|--------------|------|------------|
| 1. Catalog | name + description | Session start | ~50-100 per skill |
| 2. Instructions | Full SKILL.md body | When skill is activated | <5000 tokens (recommended) |
| 3. Resources | scripts/references/assets | When referenced by instructions | Varies |

## Skill Discovery

### Scan Locations

| Scope | Path | Purpose |
|------|------|---------|
| Project | `<project>/.<client>/skills/` | Client-native location |
| Project | `<project>/.agents/skills/` | Cross-client interoperability |
| User | `~/.<client>/skills/` | Client-native location |
| User | `~/.agents/skills/` | Cross-client interoperability |

Scan subdirectories containing `SKILL.md`. Skip `.git/` and `node_modules/`. Name collisions: project-level overrides user-level.

## Integrating into an Agent

See [references/integrate.md](references/integrate.md) for the full integration guide, covering:
- Skill discovery (local/cloud/sandbox)
- SKILL.md parsing (YAML degradation, lenient validation)
- Model disclosure (XML/JSON catalog, behavior instructions)
- Activation mechanisms (file-read activation / dedicated tool activation / user explicit activation)
- Context management (compaction protection, caching strategies)

## Supported Agent Products

35+ products implement Agent Skills: Claude Code, GitHub Copilot, Cursor, OpenAI Codex, Pi, Gemini CLI, Junie, OpenCode, OpenHands, Goose, Roo Code, VS Code, Mux, Amp, Spring AI, Databricks Genie Code, Qodo, Laravel Boost, and more. See [references/products.md](references/products.md).

## Validation

```bash
skills-ref validate ./my-skill
```

## References

- **[integrate](references/integrate.md)** — Complete guide to integrating Skills support into agents
- **[best-practices](references/best-practices.md)** — Skill creation best practices: real expertise, context management, control granularity, effective instruction patterns
- **[eval-skills](references/eval-skills.md)** — Skill quality evaluation: test cases, assertions, grading, iteration loops
- **[optimize-desc](references/optimize-desc.md)** — Optimizing the description field: trigger testing, train/validation splits, optimization loops
- **[using-scripts](references/using-scripts.md)** — Bundling scripts in skills: one-off commands, self-contained scripts, agent-friendly design
- **[products](references/products.md)** — List of 35+ products supporting Agent Skills
