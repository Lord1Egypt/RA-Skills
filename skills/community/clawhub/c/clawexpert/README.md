# ClawExpert 🧠

**Make your Claw a Self-Evolving Domain Expert**

[中文版](README-zh.md)

ClawExpert is an OpenClaw skill that lets your agent autonomously research any topic for hours, then answer questions from a structured, citable local knowledge base — not from parametric memory.

---

## Quick Start

```bash
# Install
clawhub install clawexpert

# Learn a topic
/clawexpert learn Bretton Woods System

# Specify max duration
/clawexpert learn --hours 3 "China A-share market framework"

# Check status
/clawexpert status

# Deepen an existing topic
/clawexpert learn --deepen bretton-woods-system
```

After learning, ask questions normally. ClawExpert auto-detects relevant topics and answers from the knowledge base with source citations.

---

## How It Works

### Learning (`/clawexpert learn`)

| Step | What happens |
|------|-------------|
| **1. Init** `[0%]` | Generates slug, checks for duplicate/overlapping topics, creates directories |
| **2. Decompose** `[5%]` | Breaks topic into subtopics based on complexity (min 4, no hard cap) |
| **3. Launch** `[10%]` | Spawns parallel subagents (up to `maxChildrenPerAgent`); pipeline-batches if subtopics exceed the limit |
| **4. Monitor** `[10–60%]` | Polls flag files every 30s, shows live progress |
| **5. Merge** `[60–97%]` | Deduplicates, builds knowledge tree, writes formal nodes and index |
| **6. Index** `[97%]` | Writes to the library-style `_index/` layer (L1 → L2 → topic summaries + source abstracts) |
| **7. Report** `[100%]` | Outputs completion summary |

### Retrieval (ask any question)

Three-layer retrieval, coarse to fine:

```
Layer 1: _index/_root_index.md
         Topic map across all domains — routing decision made here

Layer 2: _index/{l1}/{l2}/_index.md
         Key conclusions + source abstracts per topic — most questions answered here

Layer 3: {slug}/raw/web/*.md
         Original downloaded documents — triggered only for precise fact verification
```

### Source Priority (T1–T4)

| Tier | Examples |
|------|---------|
| **T1** | Peer-reviewed papers, official standards, government statistical reports |
| **T1.5** | Preprints (arXiv, SSRN) from recognized institutions |
| **T2** | Central bank publications, think tank reports, international organization docs, official social media |
| **T3** | Specialist media, domain-specific publications, expert commentary |
| **T4** | General news, blogs, aggregators |

Higher-tier sources are preferred during learning; T4 is used only when T1–T3 coverage is insufficient.

---

## Knowledge Base Structure

```
~/.openclaw/workspace/knowledge/
│
├── _categories.json                   # Your L1 category definitions (set on first use)
│
├── _index/                            # Library-style index layer
│   ├── _root_index.md                 # Full knowledge map — auto-loaded each session
│   └── {l1-id}/
│       └── {l2-label}/
│           └── _index.md             # Per-category index: summaries, conclusions, source abstracts
│
└── {topic-slug}/                      # Storage layer — one directory per topic
    ├── meta.json                      # Metadata: status, subtopics, session log
    ├── index.md                       # Knowledge tree overview + further directions
    ├── raw/
    │   ├── web/{hash}.md              # Downloaded web sources
    │   └── pdf/{hash}/                # PDF sources (split into parts if large)
    └── nodes/
        ├── node-001.md                # Formal knowledge nodes
        └── ...
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/clawexpert learn <topic>` | Start learning |
| `/clawexpert learn --hours <n> <topic>` | Set max duration (hours, default: 2) |
| `/clawexpert learn --deepen <slug>` | Deepen an existing topic (append, no overwrite) |
| `/clawexpert learn --auto` | Auto-mode: deepen all incomplete topics (for Cron) |
| `/clawexpert status` | Show all topic statuses |
| `/clawexpert show <slug>` | Display knowledge tree for a topic |
| `/clawexpert ask <slug> <question>` | Force answer from a specific topic's knowledge base |
| `/clawexpert forget <slug>` | Delete a topic's knowledge (requires confirmation) |
| `/clawexpert export <slug>` | Export knowledge tree as a single Markdown file |

---

## Configuration

Recommended `openclaw.json` settings:

```json
{
  "agents": {
    "defaults": {
      "subagents": { "maxChildrenPerAgent": 8 },
      "pdfModel": { "primary": "google/gemini-2.0-flash" }
    }
  },
  "plugins": {
    "entries": {
      "google": {
        "config": {
          "webSearch": {
            "apiKey": "{YOUR_GOOGLE_AI_STUDIO_KEY}",
            "model": "gemini-2.0-flash"
          }
        }
      }
    }
  },
  "env": {
    "CLAWEXPERT_KNOWLEDGE_DIR": "/custom/path"
  }
}
```

| Setting | Notes |
|---------|-------|
| `maxChildrenPerAgent` | Parallel subagent limit (default: 5 if not set) |
| `pdfModel` | Must use `provider: "google"` for native PDF support |
| Web search | Requires Google AI Studio key; use `gemini-2.0-flash` (15 RPM free tier) — `gemini-2.5-flash` is only 5 RPM |
| `CLAWEXPERT_KNOWLEDGE_DIR` | Custom KB path (default: `~/.openclaw/workspace/knowledge`) |

---

## Comparison with Other Skills

| | self-improving-agent | ClawExpert |
|--|---------------------|------------|
| What it learns | How to do things (procedural) | What is true (declarative) |
| Knowledge source | Conversation feedback | Autonomous web research |
| Best for | Long-term project collaboration | Domain-specific Q&A with citations |

Both can be installed simultaneously — they complement rather than compete.

---

## License

MIT License
