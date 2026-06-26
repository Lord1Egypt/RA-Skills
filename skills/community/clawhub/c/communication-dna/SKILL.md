---
name: communication-dna
description: Analyze speech and meeting transcriptions to build communication profiles — vocabulary fingerprints, filler word detection, speech patterns, commitment extraction, sentiment arcs, topic detection, and speaker comparison. Use when asked to analyze transcripts, profile speakers, compare communication styles, ingest meeting recordings/transcriptions, find commitments/promises in meetings, or understand someone's speaking patterns. Supports TXT, SRT, VTT, and JSON transcript formats. Integrates with Personal CRM and Knowledge Base.
---

# Communication DNA 🧬

Analyze transcriptions to extract communication intelligence — how people speak, what they commit to, how they compare.

## Setup

The project lives at `communication-dna/` in the workspace. On first use, initialize the DB:

```bash
cd <skill-dir>/scripts
python3 db.py  # Creates communication_dna.db with all tables + FTS5
```

## Core Workflow

### 1. Ingest Transcriptions

```bash
python3 dna.py ingest <file> --title "Meeting Name" --date 2026-02-23 --context meeting
python3 dna.py ingest-dir <directory>  # Batch ingest
```

**Supported formats:**
- **TXT** — Auto-detects speaker labels (`"John:"`, `"[Alice]"`, `"Speaker 1:"`)
- **SRT** — SubRip subtitles with timestamps
- **VTT** — WebVTT with timestamps
- **JSON** — Whisper/Otter.ai exports with segments

Speaker matching is fuzzy — reuses existing speakers by name.

### 2. Analyze Speakers

```bash
python3 dna.py analyze <speaker_id>    # Full report
python3 dna.py analyze-all             # All speakers
python3 dna.py fingerprint <speaker_id> # Vocabulary deep dive
python3 dna.py fillers <speaker_id>     # Filler word report
python3 dna.py patterns <speaker_id>    # Speech patterns
python3 dna.py commitments             # All extracted commitments
python3 dna.py sentiment <trans_id>    # Sentiment arc
python3 dna.py topics                  # Top topics
python3 dna.py compare <id1> <id2>    # Side-by-side comparison
```

### 3. Speaker Profiles

Auto-generated style tags based on analysis:
- Formal/Casual, Assertive/Cautious, Inquisitive, Filler-heavy/Articulate, Optimistic/Critical, Diverse vocabulary/Repetitive

### 4. Cross-System Integration

```bash
python3 dna.py link-crm               # Auto-link speakers → CRM contacts
python3 dna.py link-kb                 # Cross-reference with Knowledge Base
python3 dna.py push-to-kb <trans_id>  # Push transcription to KB
python3 dna.py cross-search "query"   # Search DNA + KB together
```

CRM path: `../personal-crm/crm.db` | KB path: `../knowledge-base/knowledge.db`

### 5. Web UI

```bash
python3 app.py  # Starts on port 5053
```

Pages: Dashboard, Speakers, Speaker Profile, Transcriptions, Transcription Detail, Compare, Search, Ingest (drag & drop), Integrations.

API endpoints: `/api/speakers`, `/api/speaker/<id>`, `/api/search`, `/api/ingest`, `/api/link-crm`, `/api/link-kb`, `/api/cross-search`, `/api/push-to-kb/<id>`

## Analysis Capabilities

| Analysis | What it extracts |
|----------|-----------------|
| **Vocabulary Fingerprint** | Word frequency, type-token ratio, sentence length, formality score, unique words |
| **Filler Detection** | Rate per 100 words, filler distribution, cross-speaker comparison |
| **Speech Patterns** | Bigram/trigram phrases, question rate, hedging vs assertiveness scores |
| **Commitments** | "I'll do X", decisions, action items — stored in `extractions` table |
| **Sentiment** | Per-segment scoring (-1 to +1), arcs over time, speaker averages |
| **Topics** | TF-IDF extraction per transcription and per speaker |

## File Reference

All source files are in `scripts/`:
- `db.py` — Schema + DB initialization
- `ingest.py` — Format parsers + speaker detection
- `analyze.py` — Analysis engine (6 functions + caching)
- `wordlists.py` — Stop words, fillers, sentiment words, formal/informal lists
- `profiles.py` — Speaker profile generator + comparison engine
- `integrations.py` — CRM + KB connectors
- `dna.py` — CLI (argparse, 17 subcommands)
- `app.py` — Flask web UI
- `templates/` — Jinja2 templates (dark theme, Tailwind CSS)

## Dependencies

- Python 3 stdlib (no pip installs for core)
- Flask (for web UI only)
- SQLite FTS5 (built into Python's sqlite3)
