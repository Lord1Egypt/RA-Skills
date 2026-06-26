---
name: doc-setup
description: Organize, summarize, and index technical documentation from any source (GitHub repos, websites, manuals) into a structured second-brain format. Use when the user needs to (1) map and categorize documentation into numbered topical files, (2) create concise summaries with original source links, (3) set up step-by-step installation/configuration guides, or (4) maintain living documentation that gets updated over time. Triggers on requests like "organize this docs", "summarize documentation", "create indexed notes from", or any task involving documentation extraction and structuring.
---

# Doc Setup

## Overview

Transform raw documentation into a navigable, topic-based knowledge base. This skill extracts key concepts, structures them into numbered files, preserves source links, and creates actionable step-by-step guides.

## Workflow

```
Source Documentation
    ↓
1. MAP — Identify all topics and subtopics
    ↓
2. EXTRACT — Fetch content from original sources
    ↓
3. STRUCTURE — Organize into numbered files (00-index, 01-topic, 02-topic...)
    ↓
4. SUMMARIZE — Concise explanations with verbatim quotes where needed
    ↓
5. LINK — Always reference original source URLs
    ↓
6. UPDATE — Mark as living document for future revisions
```

## Core Capabilities

### 1. Documentation Mapping

Before writing anything, map the full structure:

```
Source: https://github.com/user/repo/tree/main/docs
    ↓
Topics identified:
- Installation & Setup
- Architecture
- Configuration
- Data Ingestion
- Search & Embeddings
- Skills & Automation
- MCP & Integrations
- Evaluation & Quality
- Security & Permissions
- Practical Guides
```

**Output:** `00-index.md` — master index with all topics and file references.

### 2. Topic Extraction

For each topic, create a numbered file:

```
01-instalacao-e-setup.md
02-arquitetura.md
03-configuracao-operacao.md
...
```

**Each file must contain:**
- Source attribution (`> Source: URL`)
- Concise summary (not raw copy-paste)
- Key tables/decision matrices
- Step-by-step commands where applicable
- Links back to original documentation

### 3. Source Linking Rules

**ALWAYS include original source:**
```markdown
> **Source:** [github.com/user/repo/docs/INSTALL.md](https://github.com/user/repo/docs/INSTALL.md)
> **Extracted:** 2026-05-22
```

**For verbatim quotes:**
```markdown
> **Quote from source:**
> "The brain wires itself. Every page write extracts entity references..."
> — [Source](URL)
```

### 4. Living Document Markers

Mark files that will be updated:

```markdown
---
**Status:** 🟢 Living Document — updates as source changes
**Last Sync:** 2026-05-22
**Next Review:** On demand or when source updates
---
```

### 5. Step-by-Step Installation Guides

When documenting installation, use checklists:

```markdown
## Quick Start Checklist

- [ ] Step 1: Install dependencies
- [ ] Step 2: Configure API keys
- [ ] Step 3: Initialize database
- [ ] Step 4: Verify with health check

**Verification:**
```bash
command --verify  # should output: ✅ OK
```
```

## File Naming Convention

| Pattern | Use Case |
|---------|----------|
| `00-index.md` | Master index with all topics |
| `01-topic-name.md` | First topic (installation) |
| `02-topic-name.md` | Second topic (architecture) |
| `NN-topic-name.md` | Nth topic |

**Rules:**
- Two-digit prefix for sorting
- Lowercase with hyphens
- Portuguese or English matching user's preference

## Directory Structure

```
second-brain/
└── {project-name}/
    ├── 00-index.md
    ├── 01-topic.md
    ├── 02-topic.md
    └── ...
```

## Templates

### Index Template (00-index.md)

```markdown
# {Project} - Documentação Organizada

> **Fonte:** [URL principal](URL)
> **Gerado:** {date}
> **Status:** 🟢 Living Document

---

## Índice de Tópicos

| # | Arquivo | Conteúdo |
|---|---------|----------|
| 00 | `00-index.md` | Este índice |
| 01 | `01-{topic}.md` | {Descrição} |

---

_Last updated: {date}
```

### Topic Template (NN-topic.md)

```markdown
# {N}. {TÍTULO DO TÓPICO}

> **Fonte:** [URL específico](URL)
> **Extraído:** {date}

---

## {Subtópico 1}

{Resumo conciso}

### {Sub-subtópico}

```bash
# Comandos relevantes
command example
```

| Tabela | De | Decisão |
|--------|-----|---------|
| Opção A | Prós | Contras |

---

_Last updated: {date}
```

## Resources

### references/
- `workflow-patterns.md` — Common documentation structures
- `output-examples.md` — Sample organized docs for reference

### scripts/
- `validate_structure.py` — Verify file naming and index completeness

## Important Notes

1. **Never copy-paste raw docs.** Summarize and structure.
2. **Always link sources.** Every claim needs a URL.
3. **Use tables for comparisons.** Easier to scan than paragraphs.
4. **Include decision matrices.** Help user choose between options.
5. **Mark living documents.** Documentation evolves; mark it so.
6. **Prefer Portuguese.** Match user's language preference.
7. **Keep SKILL.md lean.** Move detailed examples to references/.

## Examples

### Example 1: Organizing GBrain Docs

**User request:** "Mapeie a documentação do GBrain"

**Result:**
- `00-index.md` — 11 topics mapped
- `01-instalacao-e-setup.md` — Installation paths, providers, config
- `02-arquitetura.md` — Topologies, retrieval, auto-linking
- ...through `10-guias-praticos.md`

### Example 2: Organizing OpenClaw Config

**User request:** "Resuma toda a config do OpenClaw"

**Result:**
- `00-indice.md` — 29 configuration topics
- `01-gateway.md` — Core runtime settings
- `02-canais.md` — Channel configuration
- ...through `29-secrets-management.md`

---

**When to update:** Re-run this skill when (1) source documentation changes, (2) user needs new topics added, (3) installation steps need revision, or (4) new configuration options are released.
