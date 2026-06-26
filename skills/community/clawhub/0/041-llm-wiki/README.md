# LLM-Wiki Skill

[简体中文](docs/README.cn.md) | English

Claude Code SKILL implementation of [Karpathy's llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

> **Core Philosophy**: LLM as programmer, Wiki as codebase, User as product manager.

## Why SKILL Form?

We chose the SKILL form because it brings these advantages:

- **Zero deployment** — No services to run, no databases to configure; works the moment you clone the repository
- **Native integration** — Direct command execution via Claude Code, no middleware or protocol translation needed
- **Plain-text data** — Pure Markdown files, git-native, with no proprietary formats or vendor lock-in
- **Editor freedom** — Use Obsidian, VS Code, or any text editor you prefer
- **Minimal footprint** — A small Python helper/CLI layer around a plain Markdown wiki, keeping complexity low

## Quick Start

### 1. Clone/Copy This Project

```bash
git clone https://github.com/Nemo4110/llm-wiki.git
cd llm-wiki
```

### 2. Install Dependencies (Optional)

The CLI tool requires Python 3.8+. Choose your preferred installation method:

#### Using uv (Recommended if you have uv)

```bash
# Create virtual environment and install dependencies
uv venv
uv pip install -r src/requirements.txt --python .venv/Scripts/python.exe

# Activate (Windows)
.venv\Scripts\activate
# Or Linux/macOS
source .venv/bin/activate
```

#### Using conda

```bash
# Create environment
conda create -n llm-wiki python=3.11

# Activate
conda activate llm-wiki

# Install dependencies
pip install -r src/requirements.txt
```

#### Using pip

```bash
# Create virtual environment
python -m venv .venv

# Activate
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r src/requirements.txt
```

#### Verify Installation

```bash
python -c "from src.llm_wiki.core import WikiManager; print('✓ Installation successful')"
```

**Important Dependency Notes**:

The project includes the following core dependencies (defined in `src/requirements.txt`):

| Dependency | Version | Purpose | Notes |
|------------|---------|---------|-------|
| `click` | >=8.0.0 | CLI framework | - |
| `pyyaml` | >=6.0 | YAML parsing | - |
| `pymupdf` | >=1.25.0 | PDF processing | PyMuPDF, more friendly to CJK and complex layouts |
| `numpy` | >=1.24.0 | Vector operations | Required for embedding retrieval |
| `httpx` | >=0.27.0 | HTTP client | For Ollama local service communication |
| `mcp` | >=1.0.0 | MCP SDK | Invoke remote embedding via MCP |
| `openai` | >=1.0.0 | OpenAI SDK | OpenAI embedding API |
| `pytest` | >=7.0.0 | Test runner | For the included test suite |

**Fallback dependencies** (only used when PyMuPDF table extraction is poor):
- `pdfplumber >= 0.11.8` — Table extraction (requires secure version to fix CVE-2025-64512)
- `pdfminer.six >= 20251107` — PDF underlying library

**Pure Protocol Mode**: If you only want to use Claude Code's natural language commands (e.g. "please ingest this material") for plain text files, **no installation is required**. PyMuPDF is only needed when reading PDFs.

### 3. Add Your First Material

```bash
# Copy any file into sources/
cp ~/Downloads/interesting-paper.pdf sources/
cp ~/Notes/ideas.md sources/
```

### 4. Let Claude Work

In Claude Code:

```bash
Please ingest sources/interesting-paper.pdf into wiki
```

Claude will:

1. Read the material
2. Extract key insights
3. Create/update wiki pages
4. Establish cross-references
5. Record in log.md

## Core Commands

### Protocol Mode (Recommended)

Use natural language to interact with the Agent:

```
"Please ingest sources/paper.pdf into wiki"
"Query wiki: What is the difference between Transformer and RNN?"
"Check wiki health"
```

### Agent Bridge (Recommended for Agents)

After installing dependencies, Agents should use `scripts/agent-bridge.py` as the single tool-assisted entry point for checks, status, linking, merging, semantic query, and indexing:

```bash
# Verify runtime and wiki availability
python scripts/agent-bridge.py check

# View wiki status and health
python scripts/agent-bridge.py status
python scripts/agent-bridge.py lint

# Discover and apply page relations
python scripts/agent-bridge.py link --source "NewPage" --mode light
python scripts/agent-bridge.py merge --source "NewPage" --target "OldPage" --strategy append_related --dry-run

# Build/search embedding index when enabled in config.yaml
python scripts/agent-bridge.py index
python scripts/agent-bridge.py query "optimization methods" --semantic
```

### Legacy CLI Mode (Optional)

After installing dependencies, you can use the command line tool:

```bash
# View wiki status
python -m src.llm_wiki status

# Health check
python -m src.llm_wiki lint

# Build embedding index (requires enabling embedding in config.yaml first)
python -m src.llm_wiki index

# Semantic search
python -m src.llm_wiki query "optimization methods" --semantic

# View help
python -m src.llm_wiki --help
```

**Note**: The `ingest` and `query` commands in CLI only provide auxiliary functions (such as listing pages, semantic retrieval). Actual content processing requires interacting with the Agent via natural language.

## Directory Structure

```text
llm-wiki/
├── CLAUDE.md           # ⭐ Core protocol: Agent behavior guidelines
├── AGENTS.md           # Agent implementation guide and tool-selection protocol
├── README.md           # This file
├── docs/
│   ├── README.cn.md    # Simplified Chinese README
│   └── *.md            # Topic-specific documentation
├── log.md              # Timeline log (append-only)
├── config.yaml.example # Optional embedding/provider configuration
├── sources/            # Raw materials (user-managed, Agent read-only, not tracked by git by default)
│   └── README.md
├── wiki/               # Generated knowledge pages (Agent-managed)
│   ├── index.md        # Entry index
│   └── *.md            # Topic pages
├── assets/             # Templates and configuration
│   ├── page_template.md
│   └── ingest_rules.md
├── src/                # SKILL implementation (optional, for CLI)
│   ├── llm_wiki/
│   └── requirements.txt
├── scripts/            # Auxiliary scripts
├── tests/              # pytest suite for CLI, bridge, linker, merge, embedding
├── hooks/              # Platform hooks (optional)
├── SKILL.md            # Standard-format skill description
└── examples/           # Example wiki
```

**About `sources/`**: Excluded from `.gitignore` by default to avoid repository bloat. Wiki only retains extracted knowledge; original files are managed separately (cloud storage, Zotero, etc.). See `sources/README.md` for tracking specific files.

## How It Works

### Data Flow

```text
+----------+     +--------------------+     +--------------+
| sources/ |---->|    LLM Processing  |---->|    wiki/     |
|  (Raw)   |     | (Extract + Link)   |     | (Structured) |
+----------+     +--------------------+     +--------------+
                          |
                          v
                    +----------+
                    |  log.md  |
                    | (Record) |
                    +----------+
```

### Key Design

1. **CLAUDE.md as Protocol**: Defines Agent behavior standards; anyone/any Agent can follow
2. **Pure Markdown**: No database, no lock-in, native git version control
3. **Bidirectional Links**: `[[PageName]]` format, compatible with Obsidian
4. **Cumulative Learning**: Each query can generate new wiki pages, knowledge continuously accumulates
5. **Temporal Context**: Preserve publication, release, collection, and ingest dates so related works can be read in historical order
6. **Zotero as Literature Layer**: Use existing Agent/Zotero skills to reach the Zotero library; llm-wiki keeps distilled Markdown knowledge

## Query Mechanism

### Current Implementation: Symbolic Navigation + LLM Synthesis (Default)

By default, this SKILL **does not require Embedding/vector retrieval**. Queries are completed through:

```text
User asks question
         |
         v
+-------------------------------+
|  1. Read index.md             |  <-- Human/Agent-maintained category index
|     Locate relevant topics    |
+-------------------------------+
         |
         v
+-------------------------------+
|  2. Read relevant pages       |  <-- Discover associations through [[links]]
|     and their link neighbors  |
+-------------------------------+
         |
         v
+-------------------------------+
|  3. LLM Synthesis             |  <-- Generate answers based on read content
|     Generate with citations   |  Citation format: [[PageName]]
+-------------------------------+
```

**Optional Enhancement**: After enabling embedding via `config.yaml`, CLI's `wiki query --semantic` will use **hybrid retrieval** (Keyword Match + Vector Search + Link Traversal) to quickly locate relevant pages, providing the Agent with more precise context.

**Example Flow**:

User asks: "What is LoRA?"

1. **Agent reads** `wiki/index.md`, finds `[[LoRA]]` under the "AI/ML" topic
2. **Agent reads** `wiki/LoRA.md`, discovers links to `[[Fine-tuning]]`, `[[Adapter]]`
3. **Agent synthesizes** answer:
   > LoRA (Low-Rank Adaptation) is a parameter-efficient fine-tuning method — see [[LoRA]].
   > Compared to traditional [[Fine-tuning]], it only trains low-rank matrices...

### Why No Embedding?

| Consideration | Current Solution | Embedding Solution |
|---------------|------------------|-------------------|
| **Dependencies** | Zero external dependencies | Requires Embedding API or local model |
| **Cost** | No additional fees | Charged per token/request |
| **Privacy** | Data not uploaded | Must send content to external service |
| **Accuracy** | Precise links, explainable | Approximate similarity, may retrieve irrelevant content |
| **Scale** | Suitable for 0-500 pages | Essential for large scale (1000+ pages) |

**Conclusion**: For personal/small team knowledge bases, maintaining `index.md` and page links is simpler and more effective than introducing Embedding. Embedding is available as an opt-in CLI enhancement when scale demands it.

### When to Use Embedding?

Consider upgrading when your wiki shows:

- [ ] Page count > 500, manual indexing hard to maintain
- [ ] Queries are mostly fuzzy semantic ("that paper about optimization...")
- [ ] Need cross-topic associations (user didn't mention keywords, but semantically related)

See [ROADMAP.md](ROADMAP.md) for upgrade plans.

## Example Workflows

### Scenario 1: Researching a New Domain

```bash
# Day 1: Add materials
sources/
├── 2026-04-10-transformer-paper.pdf
└── 2026-04-10-lora-blog.md
```

```bash
User: Please ingest new materials
Claude: Processed 2 materials
  - Created [[Transformer]] — Attention mechanism architecture
  - Created [[LoRA]] — Low-rank adaptation
  - Created [[Self-Attention]] — Self-attention details
  - Updated wiki/index.md
```

### Scenario 2: Deep Exploration

```bash
User: What is the difference between LoRA and full fine-tuning?

Claude (reads wiki/index.md → finds [[LoRA]] → synthesizes answer):

Based on our wiki:

**LoRA** — [[LoRA]]
- Freezes pre-trained weights, only trains low-rank matrices
- Parameter count reduced ~10,000x

**Full Fine-tuning**
- Updates all parameters
- High computational cost

Key differences:
1. Parameters: LoRA only trains 0.1%~1% of parameters [[Parameter Efficiency]]
2. Storage: LoRA only saves adapters, not full model
3. Composition: Multiple LoRAs can be stacked [[LoRA Composition]]

Was this helpful? Should I archive this answer to wiki?
```

### Scenario 3: Knowledge Accumulation

```bash
User: Yes, archive this answer

Claude: Created [[LoRA vs Full Fine-tuning]]
- Extracted comparison points from conversation
- Linked to [[LoRA]] and [[Fine-tuning]]
- Added to FAQ section in wiki/index.md
```

## Using with Obsidian

1. Open the `wiki/` directory in Obsidian
2. Enjoy graph view, quick navigation, beautiful rendering
3. Claude Code handles maintenance, Obsidian handles reading and thinking

## Using Zotero Through Agent Skills

llm-wiki does not need to become a Zotero client. When an Agent has a Zotero skill available, Zotero can remain the literature layer while llm-wiki remains the Markdown knowledge layer.

A recommended public source is the OpenAI Plugins Zotero skill: [plugins/zotero/skills/zotero](https://github.com/openai/plugins/tree/main/plugins/zotero/skills/zotero). Agents can use that skill, or an equivalent Zotero-capable skill, instead of adding a native Zotero client to llm-wiki.

The current Zotero skill workflow can:

- Probe or enable the local Zotero Desktop API.
- Search local items, collections, and tags.
- Export BibTeX/citations and insert citation keys into drafts.
- Retrieve attachment file URLs or indexed full text when explicitly requested.
- Import BibTeX/RIS records into Zotero after confirmation.

For llm-wiki ingest, use Zotero results as source discovery and provenance: read Zotero metadata, full text, annotations, or attachment paths; synthesize wiki pages; and preserve identifiers such as `zotero_item_key`, `citation_key`, `library_id`, `zotero_uri`, DOI, and arXiv ID in frontmatter when available.

This keeps `sources/` integrity intact. Zotero-managed originals can be referenced as source assets, but Agent-generated summaries must never be written into `sources/`. Arbitrary document upload/attachment management is not part of the verified llm-wiki workflow; leave document ownership to Zotero unless a Zotero-capable Agent explicitly supports that operation.

See [docs/ZOTERO_MCP_INTEGRATION.md](docs/ZOTERO_MCP_INTEGRATION.md) for the earlier implementation analysis.

## Advanced Configuration

### Custom Page Template

Edit `assets/page_template.md`:

```markdown
---
created: {{date}}
updated: {{date}}
sources:
{{sources}}
tags:
{{tags}}
---

# {{title}}

## TL;DR

One-sentence summary.

## Key Insights

{{insights}}

## My Thoughts

(Write your original thoughts here)

## Related

{{links}}
```

### Custom Ingest Rules

Edit `assets/ingest_rules.md` to add domain-specific processing logic.

## Comparison with Alternatives

| Solution | Characteristics | Best For |
|----------|----------------|----------|
| **This SKILL** | Zero dependencies, pure text, Claude Code native | Personal knowledge management, research notes |
| Sage-Wiki | Full-featured, multimodal, standalone app | Team knowledge base, enterprise deployment |
| Obsidian + Plugins | Strong visualization, rich community | Existing Obsidian workflow |
| Notion/Logseq | Collaborative, real-time sync | Multi-user collaboration, mobile access |

## Contributing

Issues and PRs welcome!

Detailed roadmap at [ROADMAP.md](ROADMAP.md).

### Current TODO

- [ ] Lint auto-fix for common wiki health issues
- [ ] Query result archiving as a guided workflow
- [ ] Domain template packs and richer example wikis
- [x] Agent Bridge unified entry point for other Agents
- [x] Zotero literature workflow via external Agent/Zotero skills
- [x] Temporal metadata protocol and visible timeline anchors
- [x] Obsidian compatibility by opening the `wiki/` directory directly
- [x] Incremental embedding for faster retrieval
- [x] Multi-language support (English + Chinese)

## License

MIT License — free to use, modify, and distribute.

---

*Inspired by [Karpathy's llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)*
