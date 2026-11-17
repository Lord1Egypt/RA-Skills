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

### Option A — One-command install with `uv` (Recommended, no clone needed)

Install the CLI as an isolated tool directly from the repository and scaffold a
knowledge base anywhere — you never run `git clone` yourself:

```bash
# 1. Install uv once (https://docs.astral.sh/uv/)
#    Windows:  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
#    macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install llm-wiki straight from GitHub (uv fetches it for you)
uv tool install git+https://github.com/Nemo4110/llm-wiki.git
# or run without installing:  uvx --from git+https://github.com/Nemo4110/llm-wiki.git llm-wiki --help

# 3. Create a knowledge base in any directory
llm-wiki init my-kb
cd my-kb

# 4. Drop materials into sources/ and let your agent ingest them
llm-wiki status
```

`llm-wiki init` materializes `wiki/`, `sources/`, `AGENTS.md`, `CLAUDE.md`, and
`config.yaml.example` from templates bundled inside the installed package — so
there is no checkout to manage at all. It also creates or non-destructively extends
`.gitignore` so private/local state such as `var/`, `temp/`, `.mcp.json`, and
`config.yaml` cannot be committed accidentally.

> Upgrading later is one command: `uv tool upgrade llm-wiki` (re-fetches the
> latest commit from the default branch).

### Option B — Clone and install from source

For development or to hack on the SKILL itself:

```bash
git clone https://github.com/Nemo4110/llm-wiki.git
cd llm-wiki
```

The CLI tool currently supports Python 3.12-3.13. The actively verified local development matrix is:

| Platform | Python | Status |
|----------|--------|--------|
| Windows | 3.13 | Verified |
| Windows | 3.12 | Supported target |
| Linux/macOS | 3.12-3.13 | Supported target, not the primary local verification platform |

Python 3.8-3.11 are not part of the current support matrix. Choose your preferred installation method:

#### Using uv (Recommended if you have uv)

```bash
# Create virtual environment and install the package (editable)
uv venv
uv pip install -e .

# Activate (Windows)
.venv\Scripts\activate
# Or Linux/macOS
source .venv/bin/activate
```

#### Using conda

```bash
# Create environment
conda create -n llm-wiki python=3.13

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

# Install the package (editable) so the llm-wiki command is available
pip install -e .
```

#### Verify Installation

```bash
# Installed as a tool / package
llm-wiki --help

# Or, from a source checkout without installing
python -c "from src.llm_wiki.core import WikiManager; print('✓ Installation successful')"
```

**Important Dependency Notes**:

The project includes the following core dependencies (defined in `src/requirements.txt`):

| Dependency | Version | Purpose | Notes |
|------------|---------|---------|-------|
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

### 2. Add Your First Material

```bash
# Copy any file into sources/
cp ~/Downloads/interesting-paper.pdf sources/
cp ~/Notes/ideas.md sources/
```

### 3. Let Claude Work

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

After installing dependencies, Agents should use `scripts/agent-bridge.py` as the single tool-assisted entry point for checks, status, linking, merging, atomic writes, semantic query, and indexing:

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

# Build a read-only Zotero metadata/tag plan from an MCP snapshot
python scripts/agent-bridge.py zotero-plan --snapshot temp/zotero-snapshot.yaml \
  --manifest-out temp/zotero-mutation-manifest.yaml

# Refresh DOI/citation/publication state through Zotero MCP (dry-run by default)
python scripts/agent-bridge.py zotero-refresh --collection-key A9VNJUPI \
  --manifest-out temp/zotero-refresh.yaml

# Verify a collection ingest allocation and its wiki provenance/page invariants
python scripts/agent-bridge.py zotero-ingest-verify \
  --snapshot temp/zotero-snapshot.yaml \
  --allocation temp/zotero-allocation.yaml \
  --report-out temp/zotero-ingest-report.yaml

# Audit an explicitly authorized managed-tag/Related-item local write plan
python scripts/agent-bridge.py zotero-writeback --plan temp/zotero-write-plan.yaml \
  --action audit --report-out temp/zotero-write-audit.yaml

# Plan controlled attachment relocation (root comes from config.yaml; apply needs explicit config + local authorization)
python scripts/agent-bridge.py zotero-relocate

# Apply relocation only after reviewing the dry-run report
python scripts/agent-bridge.py zotero-relocate --apply --report-out temp/zotero-relocate.yaml

# Apply multi-file writes (page + index + log) atomically; always dry-run first
python scripts/agent-bridge.py apply-bundle temp/tx-bundle.yaml --dry-run
python scripts/agent-bridge.py apply-bundle temp/tx-bundle.yaml

# Inspect per-command capability contracts (write scope, network, dry-run)
python scripts/agent-bridge.py capabilities

# Print bounded recent-activity context (wiki/hot.md)
python scripts/agent-bridge.py hot
```

#### Zotero review manifests

`agent-bridge.py zotero-plan` is a read-only bridge between wiki provenance and Zotero MCP. It compares an MCP-produced YAML/JSON snapshot with `sources_meta`, reports DOI/publication audits and managed-tag changes, and leaves all Zotero writes to the reviewed MCP workflow. With `--manifest-out`, it may write a deterministic `mode: review-only` YAML manifest only under `temp/`; the manifest is not directly executable, and tag-removal or relation candidates still require review before any Zotero MCP mutation.

`agent-bridge.py zotero-refresh` is a one-shot enrichment worker inspired by Zotero plugin freshness workflows. It reads the collection through `54yyyu/zotero-mcp`, uses Crossref for DOI identity/publication candidates and OpenAlex for citation and open journal metrics, stores only a small ignored SQLite cache under `var/`, and defaults to dry-run. `--apply-safe` may incrementally upsert `LLM-Wiki ...` Extra keys, manage only `llm-wiki:*` status tags, and normalize an empty or conflicting `doi.org` URL; DOI candidates and preprint-to-published changes remain review-only. The first collection-wide apply can take minutes because Zotero writes remain serial and incremental; verification is batched after writes, and later runs normally become no-ops until freshness windows expire.

`agent-bridge.py zotero-ingest-verify` compares a verified MCP snapshot with an explicit allocation ledger (example: `docs/examples/zotero-ingest-allocation.example.yaml`). It fails on missing/duplicate allocations, unexplained omissions, missing `sources_meta` bindings, invalid frontmatter, broken page invariants, control characters, trailing whitespace, or machine-specific private paths. Suspiciously identical three-page batch structure is advisory rather than an automatic failure.

`agent-bridge.py zotero-writeback` is the temporary, explicitly authorized Zotero 10 loopback exception for additions that the current MCP cannot express. It accepts only a secret-free `mode: authorized-write` plan (example: `docs/examples/zotero-write-plan.example.yaml`), supports separate `audit`, `apply`, and `verify` phases, adds only `llm-wiki:*` tags, and ensures reviewed reciprocal Related pairs. It preserves existing tag objects, retries one version conflict from a fresh GET, and verifies every accepted PATCH. Metadata, collection membership, notes, tag removal, and Trash remain out of scope. `--memory-authorize` keeps the key in process memory only.

`agent-bridge.py zotero-relocate` is the opt-in, verified attachment relocation workflow. It plans from `sources/zotero/metadata.yaml` bindings but reads the current attachment path from Zotero, never overwrites an existing target, and defaults to dry-run. Apply requires `zotero_relocation.enabled: true`, local Zotero authorization, and a path template/root that pass the capability and containment checks. It changes only the attachment's `linkMode`/`path`, preserves the original item key, updates private metadata and aliases after post-write verification, never edits notes, and leaves old sources in place unless explicitly configured for scoped cleanup. See `docs/ZOTERO_ATTACHMENT_RELOCATION.md` for the Phase 0 API gate and recovery rules.

Configure the managed attachment root once in `config.yaml` under `zotero_relocation.root` rather than passing `--root` on every run; `config.yaml` is gitignored, so each machine keeps its own value. For cross-device sync, point `root` at a cloud-synced folder and use environment-variable interpolation to keep the path portable, e.g. `root: "${OneDrive}/zotero-attachments"` (Windows resolves `${OneDrive}`). When devices run different operating systems (e.g. Windows + Linux), absolute paths can never match; set `zotero_relocation.base_dir_relative: true` so Zotero stores portable `attachments:<relative>` paths, and point Zotero's **Linked Attachment Base Directory** at the synced root on each device. Note the sync caveat: a stored→linked conversion may stop Zotero File Sync from managing the file bytes, so every device must be able to reach the same synced root.

#### Depth lint warnings

`agent-bridge.py lint` also reports **Shallow Pages** as advisory warnings. The detector excludes `Related Pages` / `相关页面`, `Sources` / `来源`, and `Changelog` / `变更日志`, then combines normalized knowledge length, meaningful paragraph and section counts, local text-source volume, source count, and source-to-synthesis compression ratio. Findings do not change the command's exit behavior.

Pages tagged `QRF` are skipped by default. A deliberately concise, already-reviewed page may set `lint_depth: skip` in frontmatter, but the exemption should be justified by a source-coverage audit. Passing the heuristic does not replace unit-level coverage review, and pages must never be padded mechanically just to cross a threshold. Thresholds and skipped tags are configurable under `lint.depth` in `config.yaml`.

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
├── AGENTS.md           # ⭐ Canonical Agent protocol and tool-selection guide
├── CLAUDE.md -> AGENTS.md # Relative symbolic link to the canonical protocol
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

**About `sources/`**: Excluded from `.gitignore` by default to avoid repository bloat. Wiki only retains extracted knowledge; original files are managed separately (cloud storage, Zotero, etc.). See `sources/README.md` for tracking specific files. `sources/zotero/` is reserved for private Zotero bindings and local symlink aliases; do not commit it.

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

Ingest is adaptive rather than template-sized. Before drafting, the Agent maps the source's mechanisms, evidence, comparisons, implementation details, failure modes, and open questions; allocates each important unit; then chooses headings that fit the knowledge. A short source can produce a short page, while a long technical source should not collapse into a fixed summary card.

### Key Design

1. **AGENTS.md as Canonical Protocol**: Defines Agent behavior standards; `CLAUDE.md` is a relative symbolic link that keeps every Agent entry point identical
2. **Pure Markdown**: No database, no lock-in, native git version control
3. **Bidirectional Links**: `[[PageName]]` format, compatible with Obsidian
4. **Cumulative Learning**: Each query can generate new wiki pages, knowledge continuously accumulates
5. **Temporal Context**: Preserve publication, release, collection, and ingest dates so related works can be read in historical order
6. **Zotero as Literature Layer**: Use the required `54yyyu/zotero-mcp` integration to reach the Zotero library; llm-wiki keeps distilled Markdown knowledge

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

## Using Zotero Through zotero-mcp

Zotero remains the literature layer and llm-wiki remains the distilled Markdown knowledge layer. Discovery, reads, sources, metadata identity, and normal writes go through [`54yyyu/zotero-mcp`](https://github.com/54yyyu/zotero-mcp). The only supported direct exception is the temporary, explicitly authorized Zotero 10 loopback write path documented above and in the canonical protocol; alternate Zotero skills, direct database access, and direct Web API integrations remain outside the workflow.

See the canonical [Zotero MCP operating protocol](docs/ZOTERO_MCP_INTEGRATION.md) for setup and capability gates, read/write workflows, Zotero-backed ingest, private `sources/zotero/` bindings, provenance fields, and failure handling.

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
- [x] Zotero literature workflow via `54yyyu/zotero-mcp`
- [x] Temporal metadata protocol and visible timeline anchors
- [x] Obsidian compatibility by opening the `wiki/` directory directly
- [x] Incremental embedding for faster retrieval
- [x] Multi-language support (English + Chinese)

## License

MIT License — free to use, modify, and distribute.

---

*Inspired by [Karpathy's llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)*
