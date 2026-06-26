# DESIGN.md — dreaming-optimizer

> **Version:** 1.0.0  
> **Date:** 2026-04-17  
> **Author:** 道衍 (架构师)  
> **Status:** Ready for Development  

---

## 1. Overview

`dreaming-optimizer` intercepts the OpenClaw Dreaming REM consolidation pipeline at Steps 2–4, curating memory entries before they are committed to the persistent B-layer. It ensures long-term memory quality by scoring, deduplicating, tagging, and prioritizing entries.

**Core Promise:** Wake up smarter. Every REM cycle is a chance to consolidate what matters.

---

## 2. Technical Architecture

### 2.1 High-Level Architecture

```
Session End
    │
    ▼
┌─────────────────────────────────────────────┐
│           dreaming-optimizer Pipeline        │
│                                             │
│  [1] DAILY NOTES ──► [2] SCORE ──► [3] DEDUP ──► [4] TAG ──► [5] COMMIT ──► [6] SUMMARY │
│       (read)           │            │            │            │              │        │
│                     threshold      similarity   rule-based   write SQLite   JSON file  │
│                       filter         check       classifier   B-layer      human UI  │
└─────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
            [Archive: score < 70]         [dreaming-summaries/*.json]
            ~/.openclaw/workspace/
              memory/dreaming-archives/
```

### 2.2 Component Architecture

```
dreaming-optimizer/
├── bin/
│   ├── optimize.sh              # CLI entry, orchestrates pipeline
│   ├── score_entries.py         # LLM-based priority scoring
│   ├── deduplicate.py           # Semantic deduplication vs B-layer
│   ├── commit.py                # Write entries to B-layer SQLite
│   └── dreaming_summary.py      # Generate traceable summary (scripts/)
├── scripts/
│   └── dreaming_summary.py      # Summary report generator
├── config/
│   └── default_threshold.yaml   # Configurable thresholds
├── lib/                         # Shared utilities (NEW)
│   ├── __init__.py
│   ├── config_loader.py         # YAML config loader
│   ├── blayer_client.py         # B-layer SQLite read/write
│   └── log_utils.py             # Logging utilities
└── tests/                       # (NEW) Test suite
    ├── test_score_entries.py
    ├── test_deduplicate.py
    ├── test_commit.py
    └── test_integration.py
```

---

## 3. Core Algorithms

### 3.1 Priority Scoring Algorithm

**Input:** Raw memory entry (text string)  
**Output:** Score 0–100 + content preview (first 500 chars)

**Scoring Formula:**
```
base_score = 50

# Bonus factors
+ fact_density_bonus     # Contains concrete facts/terms
+ recency_bonus           # Recently modified files get boost
+ uniqueness_bonus       # Rare terms vs common ones
+ actionability_bonus     # Contains actionable language

# Penalty factors
- vagueness_penalty       # Hedging language reduces score
- noise_penalty          # Very short entries penalized
- duplication_penalty    # Already-deduplicated content penalized

final_score = clamp(base_score + bonuses - penalties, 0, 100)
```

**Concrete Fact Terms (MVP heuristic, replaceable with LLM):**
```python
FACT_TERMS = [
    "数据库", "API", "配置", "bug", "修复", "测试", "agent", "skill",
    "已修复", "已实现", "完成了", "测试通过", "deployed", "fixed",
    "代码", "函数", "模块", "架构", "部署", "上线", "发布",
]
UNIQUENESS_THRESHOLD = 0.85  # Term frequency inverse
```

**LLM-Enhanced Scoring (Pro tier, v1.1):**
```python
LLM_PROMPT = """Score this memory entry 0-100 for long-term importance.
Consider: factual density, uniqueness, actionability, recency.

Entry: {content}

Respond JSON: {{"score": int, "reason": str}}"""
```

### 3.2 Deduplication Algorithm

**Strategy:** Token-overlap similarity + optional embedding similarity (Pro)

**Token-Overlap Similarity (MVP):**
```python
def token_similarity(a: str, b: str) -> float:
    tokens_a = set(normalize(a))  # lower, strip, split whitespace
    tokens_b = set(normalize(b))
    if not tokens_a or not tokens_b:
        return 0.0
    jaccard = len(tokens_a ∩ tokens_b) / len(tokens_a ∪ tokens_b)
    # Also compute overlap coefficient
    overlap = len(tokens_a ∩ tokens_b) / min(len(tokens_a), len(tokens_b))
    return max(jaccard, overlap * 0.8)  # weighted combination
```

**Embedding Similarity (Pro v1.1):**
```python
# Use sentence-transformers for semantic dedup
# embeddings = model.encode([entry] + existing_memories)
# similarity = cosine_similarity(embeddings[0], embeddings[1:])
# threshold = 0.85 → merge
```

**Dedup Decision Tree:**
```
For each candidate entry:
    1. Retrieve existing memories from B-layer (last 1000 entries)
    2. Compute similarity vs each existing memory
    3. If max_similarity >= 0.85:
         → MERGE into existing (update score = max(scores))
         → Discard candidate
       Else:
         → MARK as unique
         → Proceed to commit
```

### 3.3 Fact-Tagging Algorithm

**Rule-based tagger (MVP):**
```python
TAG_PATTERNS = {
    "fact": [
        "已修复", "已实现", "完成了", "测试通过", "deployed", "fixed",
        "创建了", "删除了", "更新了", "上线", "发布",
        r"\d+个", r"v\d+\.\d+",  # version numbers
    ],
    "opinion": [
        "我觉得", "认为", "可能", "应该", "probably", "think", "believe",
        "似乎", "大概", "也许", "might", "may",
    ],
    "preference": [
        "我喜欢", "偏好", "prefer", "不喜欢", "dont like",
        "倾向于", "习惯用", "更倾向于",
    ],
    "learning": [
        "学到", "发现", "learned", "realized", "insight",
        "认识到", "理解到", "明白了",
    ],
    "context": [],  # default fallback
}

def tag_entry(content: str) -> str:
    # Score each tag category, return highest
    # Tie-break: fact > learning > context > opinion > preference
```

### 3.4 Archive vs Commit Decision

```python
def should_commit(score: int, threshold: int = 70) -> str:
    if score >= threshold:
        return "commit"      # → B-layer
    elif score >= threshold * 0.5:  # >= 35
        return "archive"    # → dreaming-archives/
    else:
        return "discard"    # → discarded (logged only)
```

---

## 4. Data Flow

### 4.1 Pipeline Data Flow

```
INPUTS
  ├── Daily memory files: ~/.openclaw/workspace/memory/YYYY-MM-DD.md
  ├── Session transient:  ~/.openclaw/workspace/memory/transient/*.md
  └── Config:              ~/.openclaw/workspace/skills/dreaming-optimizer/config/default_threshold.yaml

PIPELINE STEPS
  Step 1: Read daily notes
          → Parse each .md into entry dicts
          → Extract: filename, mtime, content, line_count

  Step 2: Score each entry
          → score_entry(content) → {score, content_preview, reasons}
          → Filter: score >= threshold → "passed"
          → Filter: score < threshold → "archived"

  Step 3: Deduplicate passed entries
          → Load B-layer memories (last 1000)
          → For each passed entry:
              if similarity(existing) >= 0.85 → merge
              else → unique → proceed

  Step 4: Tag unique entries
          → tag_entry(content) → "fact"|"opinion"|"preference"|"learning"|"context"

  Step 5: Commit to B-layer
          → Write unique entries to ~/.openclaw/memory/<agent>.sqlite
          → Fields: id, content, score, tag, source, created_at, updated_at

  Step 6: Generate summary
          → Write to ~/.openclaw/workspace/memory/dreaming-summaries/dreaming-summary-YYYY-MM-DD.json

OUTPUTS
  ├── B-layer SQLite: ~/.openclaw/memory/<agent>.sqlite
  ├── Archive:        ~/.openclaw/workspace/memory/dreaming-archives/
  └── Summary:        ~/.openclaw/workspace/memory/dreaming-summaries/
```

### 4.2 Entry Data Structure

```python
@dataclass
class MemoryEntry:
    content: str                  # Full content
    content_preview: str          # First 500 chars
    score: int                    # 0-100
    tag: str                      # fact/opinion/preference/learning/context
    source_file: str              # Which file this came from
    source_agent: str             # Which agent created it
    created_at: str               # ISO timestamp
    is_merged: bool               # Was this merged from dedup
    merged_into: Optional[int]   # ID of entry it was merged into
```

---

## 5. File Structure

```
dreaming-optimizer/
├── SKILL.md                     # Public skill manifest
├── DESIGN.md                    # This file — technical design
├── bin/
│   ├── optimize.sh              # CLI entry point
│   ├── score_entries.py         # Entry point → orchestrates scoring
│   ├── deduplicate.py           # Semantic dedup engine
│   ├── commit.py               # B-layer commit writer
│   └── dreaming_summary.py      # Summary generator
├── lib/                         # Shared library (NEW)
│   ├── __init__.py
│   ├── config_loader.py         # YAML config loader with defaults
│   ├── blayer_client.py         # B-layer SQLite read/write client
│   └── log_utils.py             # Structured logging
├── config/
│   └── default_threshold.yaml   # Default configuration
├── scripts/
│   └── dreaming_summary.py      # Summary report generator (standalone)
├── tests/                       # Test suite (NEW)
│   ├── __init__.py
│   ├── test_score_entries.py
│   ├── test_deduplicate.py
│   ├── test_commit.py
│   └── test_integration.py
└── README.md                    # Usage documentation
```

---

## 6. API Design

### 6.1 bin/score_entries.py

```python
def parse_memory_file(filepath: Path) -> list[dict]:
    """Parse a daily memory .md file into entry dicts.
    
    Args:
        filepath: Path to YYYY-MM-DD.md file
        
    Returns:
        List of entry dicts with keys: content, filename, mtime, line_count
    """

def score_entry(content: str, mtime: datetime = None) -> dict:
    """Score a single memory entry (0-100).
    
    Scoring algorithm:
        - base: 50
        - +5 per concrete fact term found (max +30)
        - +10 if recently modified (within 7 days)
        - +10 if contains actionable language
        - -20 if very short (<20 chars)
        - -10 if vague hedging detected
        - final: clamp(0, 100)
    
    Args:
        content: Raw text content of the entry
        mtime: Last modified time (optional, defaults to now)
        
    Returns:
        dict: {
            "score": int,           # 0-100
            "content_preview": str, # First 500 chars
            "reasons": list[str],   # Why this score
            "fact_terms_found": list[str]
        }
    """

def score_entries(
    memory_files: list[Path] = None,
    threshold: int = 70,
    max_entries: int = 1000,
) -> dict:
    """Score all entries from daily memory files.
    
    Args:
        memory_files: List of Path objects to memory .md files.
                      Defaults to all files in workspace/memory/.
        threshold: Minimum score to pass (default: 70)
        max_entries: Maximum entries to process (default: 1000)
        
    Returns:
        dict: {
            "scored": list[dict],   # All entries with scores
            "passed": list[dict],   # Entries with score >= threshold
            "archived": list[dict], # Entries with score < threshold
            "total_processed": int,
            "skipped": int,         # Entries skipped (too many)
        }
    """

# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Score memory entries")
    parser.add_argument("--threshold", type=int, default=70,
                        help="Minimum score threshold (default: 70)")
    parser.add_argument("--max-entries", type=int, default=1000,
                        help="Max entries to process")
    parser.add_argument("--input-dir", type=Path, default=None,
                        help="Override input directory")
    args = parser.parse_args()
    result = score_entries(threshold=args.threshold, max_entries=args.max_entries)
```

### 6.2 bin/deduplicate.py

```python
def get_blayer_memories(
    db_path: Path = None,
    limit: int = 1000,
    min_score: int = 0,
) -> list[dict]:
    """Read existing B-layer memories from SQLite.
    
    Args:
        db_path: Path to SQLite DB (default: ~/.openclaw/memory/main.sqlite)
        limit: Maximum number of memories to retrieve (default: 1000)
        min_score: Only return memories with score >= min_score
        
    Returns:
        List of dicts: [{"id": int, "content": str, "score": int, "tag": str}, ...]
    """

def normalize_text(text: str) -> list[str]:
    """Normalize text for similarity comparison.
    
    - Lowercase
    - Strip punctuation
    - Split on whitespace
    - Remove stop words (Chinese + English)
    
    Returns:
        List of normalized tokens
    """

def token_similarity(a: str, b: str) -> float:
    """Compute token-overlap similarity between two texts.
    
    Uses Jaccard + overlap coefficient combination.
    
    Args:
        a: First text string
        b: Second text string
        
    Returns:
        float: Similarity score 0.0-1.0
    """

def embedding_similarity(a: str, b: str, model_name: str = None) -> float:
    """Compute semantic similarity via embeddings (Pro feature, v1.1).
    
    Requires: sentence-transformers
    
    Args:
        a: First text string
        b: Second text string
        model_name: HuggingFace model name
        
    Returns:
        float: Cosine similarity -1.0 to 1.0
    """

def deduplicate_entries(
    entries: list[dict],
    blayer_memories: list[dict] = None,
    threshold: float = 0.85,
    use_embeddings: bool = False,
) -> dict:
    """Remove near-duplicate entries based on similarity threshold.
    
    Args:
        entries: List of entry dicts with "content_preview" key
        blayer_memories: Existing B-layer memories to check against
        threshold: Similarity threshold 0.0-1.0 (default: 0.85)
        use_embeddings: Use embedding similarity (Pro, v1.1)
        
    Returns:
        dict: {
            "unique": list[dict],     # Entries to commit
            "merged": list[dict],    # Entries merged into existing
            "merged_into": dict,     # Map of merged_id → existing_id
            "stats": {
                "total_input": int,
                "unique_count": int,
                "merged_count": int,
                "avg_similarity": float,
            }
        }
    """

# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deduplicate memory entries")
    parser.add_argument("--threshold", type=float, default=0.85,
                        help="Similarity threshold (default: 0.85)")
    parser.add_argument("--no-embeddings", action="store_true",
                        help="Disable embedding-based similarity")
    args = parser.parse_args()
    result = deduplicate_entries([], threshold=args.threshold,
                                  use_embeddings=not args.no_embeddings)
```

### 6.3 bin/commit.py

```python
def get_db_path(agent: str = None) -> Path:
    """Get path to B-layer SQLite database.
    
    Args:
        agent: Agent name (default: "main")
        
    Returns:
        Path to ~/.openclaw/memory/<agent>.sqlite
    """

def ensure_schema(db_path: Path) -> None:
    """Ensure B-layer schema exists, create if not.
    
    Schema:
        CREATE TABLE memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            content_preview TEXT,
            score INTEGER DEFAULT 50,
            tag TEXT DEFAULT 'context',
            source TEXT,
            source_agent TEXT,
            is_merged BOOLEAN DEFAULT 0,
            merged_into INTEGER,
            created_at TEXT,
            updated_at TEXT,
            last_accessed_at TEXT,
            access_count INTEGER DEFAULT 0,
            INDEX idx_score (score),
            INDEX idx_tag (tag),
            INDEX idx_created (created_at)
        );
        
        CREATE TABLE dreaming_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER,
            action TEXT,  -- 'committed'|'archived'|'merged'|'discarded'
            score INTEGER,
            reason TEXT,
            ts TEXT,
            FOREIGN KEY (entry_id) REFERENCES memories(id)
        );
    """

def tag_entry(content: str) -> str:
    """Tag entry as fact/opinion/preference/learning/context.
    
    Uses rule-based pattern matching.
    
    Args:
        content: Entry content string
        
    Returns:
        str: One of: fact, opinion, preference, learning, context
    """

def commit_to_blayer(
    entries: list[dict],
    db_path: Path = None,
    dry_run: bool = False,
) -> dict:
    """Write entries to B-layer SQLite.
    
    Args:
        entries: List of entry dicts with keys:
                 - content: full content text
                 - content_preview: first 500 chars
                 - score: 0-100
                 - source_file: originating file
                 - source_agent: originating agent
        db_path: SQLite path (default: ~/.openclaw/memory/main.sqlite)
        dry_run: If True, don't actually write (for testing)
        
    Returns:
        dict: {
            "committed": int,       # Number of entries written
            "failed": int,         # Number of entries that failed
            "entry_ids": list[int], # IDs of committed entries
            "errors": list[str],    # Error messages
        }
    """

def archive_entry(
    entry: dict,
    archive_dir: Path = None,
) -> Path:
    """Archive a low-score entry to dreaming-archives/.
    
    Args:
        entry: Entry dict
        archive_dir: Archive directory (default: workspace/memory/dreaming-archives/)
        
    Returns:
        Path: Path to archived file
    """

# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Commit entries to B-layer")
    parser.add_argument("--dry-run", action="store_true",
                        help="Dry run - don't actually commit")
    parser.add_argument("--agent", type=str, default="main",
                        help="Agent name for DB path")
    args = parser.parse_args()
    result = commit_to_blayer([], dry_run=args.dry_run)
```

### 6.4 bin/optimize.sh

```bash
#!/usr/bin/env zsh
# Main entry point — orchestrates the full pipeline

# Arguments:
#   --threshold N     : Minimum score threshold (default: 70)
#   --dry-run         : Don't commit, just show what would happen
#   --agent NAME      : Agent name (default: main)
#   --max-entries N  : Max entries to process (default: 1000)
#   --input-dir PATH  : Override default input directory

# Pipeline:
#   1. Read daily memory files → entries
#   2. score_entries.py --threshold N → scored
#   3. deduplicate.py → unique entries
#   4. commit.py --dry-run → commit or preview
#   5. dreaming_summary.py → JSON summary

# Exit codes:
#   0: Success
#   1: No entries to process
#   2: Configuration error
#   3: B-layer write error
```

### 6.5 scripts/dreaming_summary.py

```python
def generate_summary(
    scored: int,
    passed: int,
    archived: int,
    merged: int,
    committed: int,
    discarded: int,
    tag_counts: dict[str, int],
    output_dir: Path = None,
    format: str = "json",
) -> dict:
    """Generate traceable dreaming summary.
    
    Args:
        scored: Total entries scored
        passed: Entries passing threshold
        archived: Entries archived (35 <= score < 70)
        merged: Entries merged via dedup
        committed: Entries written to B-layer
        discarded: Entries discarded (score < 35)
        tag_counts: {"fact": n, "opinion": n, ...}
        output_dir: Directory for summary files
        format: "json" (default) or "markdown"
        
    Returns:
        dict: Summary data (also written to file)
    """

def generate_markdown_summary(data: dict) -> str:
    """Generate human-readable markdown summary.
    
    Args:
        data: Summary data dict
        
    Returns:
        str: Markdown formatted summary
    """
```

---

## 7. B-Layer SQLite Schema

```sql
-- Primary memories table
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    content_preview TEXT,
    score INTEGER DEFAULT 50,
    tag TEXT DEFAULT 'context' CHECK(tag IN ('fact','opinion','preference','learning','context')),
    source TEXT,
    source_agent TEXT DEFAULT 'dreaming-optimizer',
    is_merged BOOLEAN DEFAULT 0,
    merged_into INTEGER REFERENCES memories(id),
    created_at TEXT,
    updated_at TEXT,
    last_accessed_at TEXT,
    access_count INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_memories_score ON memories(score);
CREATE INDEX IF NOT EXISTS idx_memories_tag ON memories(tag);
CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at);

-- Dreaming audit log
CREATE TABLE IF NOT EXISTS dreaming_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_content_hash TEXT,
    action TEXT CHECK(action IN ('committed','archived','merged','discarded')),
    score INTEGER,
    similarity_score REAL,
    merged_into_id INTEGER,
    reason TEXT,
    ts TEXT DEFAULT (datetime('now')),
    source_file TEXT
);

CREATE INDEX IF NOT EXISTS idx_dreaming_log_ts ON dreaming_log(ts);
CREATE INDEX IF NOT EXISTS idx_dreaming_log_action ON dreaming_log(action);
```

---

## 8. Configuration Schema

```yaml
# config/default_threshold.yaml
version: "1.0.0"

# Scoring thresholds
scoring:
  default_threshold: 70          # Min score to commit to B-layer
  archive_threshold: 35         # Min score to archive (else discard)
  max_entries_per_cycle: 1000   # Cap entries per REM cycle
  
# Fact term dictionary (MVP scoring)
fact_terms:
  zh:
    - 数据库, API, 配置, bug, 修复, 测试, agent, skill
    - 已修复, 已实现, 完成了, 测试通过, deployed, fixed
    - 代码, 函数, 模块, 架构, 部署, 上线, 发布
  en:
    - fixed, deployed, implemented, completed, tested
    - bug, api, config, module, architecture

# Deduplication
dedup:
  token_threshold: 0.85         # Token overlap similarity threshold
  use_embeddings: false          # Pro feature (v1.1)
  embedding_model: "paraphrase-multilingual-MiniLM-L12-v2"
  check_blayer_limit: 1000      # Max existing memories to compare against

# B-layer settings
blayer:
  db_name: "main.sqlite"         # Agent DB name
  auto_create_schema: true       # Create schema if missing
  
# Archive settings
archive:
  enabled: true
  dir: "dreaming-archives"       # Relative to workspace/memory/
  max_archive_age_days: 90      # Auto-purge archives older than this

# Output settings
output:
  summary_dir: "dreaming-summaries"
  summary_format: "json"         # json | markdown
```

---

## 9. Edge Cases & Error Handling

| Edge Case | Handling Strategy |
|-----------|-------------------|
| Empty memory files | Skip, log warning, continue |
| Malformed YAML config | Fall back to hardcoded defaults, log warning |
| B-layer DB doesn't exist | Auto-create with `ensure_schema()` |
| B-layer DB is corrupted | Catch sqlite3.Error, return error dict, skip commit |
| No entries to process | Exit code 1, "Nothing to optimize" |
| All entries below threshold | Log summary, exit code 0 (no-op) |
| Dedup check against empty B-layer | Skip dedup, commit all passed entries |
| Entry content > 100KB | Truncate to 100KB, log warning |
| Duplicate filenames | Use mtime + content hash as unique key |
| B-layer write fails mid-way | Transaction rollback, return partial result + errors |
| Config file missing | Use all defaults, log info |
| Non-UTF8 content | Decode with errors='replace', log warning |

---

## 10. Testing Strategy

### 10.1 Unit Tests

**test_score_entries.py:**
- `test_short_entry_penalized`: Entry < 20 chars gets -20
- `test_fact_terms_bonus`: Known fact term adds +5 per term (max +30)
- `test_score_clamped_0_100`: Score never exceeds bounds
- `test_empty_entry_returns_score_50`: Empty entry defaults to base
- `test_multiple_fact_terms_capped`: 10 fact terms → max +30, not +50

**test_deduplicate.py:**
- `test_identical_entries_merged`: Same content → similarity = 1.0
- `test_completely_different_no_merge`: No overlap → similarity ≈ 0
- `test_threshold_085`: Above → unique, below → merged
- `test_empty_blayer_no_false_positives`: Empty B-layer → all unique

**test_commit.py:**
- `test_schema_created_if_missing`: DB created with correct schema
- `test_commit_increases_row_count`: Verified by row count diff
- `test_duplicate_content_handled`: PK violation → caught, skipped
- `test_dry_run_doesnt_write`: dry_run=True → no changes

**test_tag_entry.py:**
- `test_fact_tagged_correctly`: Known fact phrases tagged "fact"
- `test_opinion_tagged_correctly`: Known opinion phrases tagged "opinion"
- `test_fallback_context`: No patterns → "context"
- `test_fact_priority_over_opinion`: Both present → "fact"

### 10.2 Integration Tests

**test_integration.py:**
- `test_full_pipeline_runs`: optimize.sh → check output files exist
- `test_summary_file_created`: dreaming-summary-YYYY-MM-DD.json exists
- `test_no_files_no_crash`: Empty memory dir → graceful exit
- `test_threshold_respected`: entries below threshold not committed

---

## 11. Known Issues

| Issue | Severity | Workaround |
|-------|----------|------------|
| Token similarity is naive — doesn't handle synonyms | Medium | Pro v1.1 will use embeddings |
| B-layer schema assumes "main" agent | Low | Config-driven agent name |
| No LLM scoring in MVP (rule-based only) | Medium | LLM scoring in Pro v1.1 |
| No support for multi-line entry boundaries | Low | Parse by --- YAML separator |
| Archive auto-purge not implemented yet | Low | Manual cleanup only |

---

## 12. Development Task Breakdown

See: `~/.openclaw/workspace/skills/TODO-20260417.md`

**Priority Order:**
1. `lib/` shared utilities (config_loader, blayer_client)
2. `bin/commit.py` enhanced (add dreaming_log)
3. `bin/deduplicate.py` enhanced (add blayer read, proper schema)
4. `bin/score_entries.py` enhanced (add normalize, reasons)
5. `bin/optimize.sh` orchestration
6. `scripts/dreaming_summary.py` enhanced
7. `config/default_threshold.yaml` created
8. `tests/` test suite
9. `README.md` documentation

---

## 13. Performance Considerations

### 13.1 Scalability Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Entries per cycle | ≤1000 | Configurable via `max_entries_per_cycle` |
| B-layer dedup check | ≤1000 entries | Limit to prevent O(n²) explosion |
| Scoring latency | <5s for 100 entries | Rule-based is fast; LLM adds ~1s/entry |
| Commit throughput | 100 entries/second | SQLite batch inserts recommended |
| Memory footprint | <100MB | Streaming for large files |

### 13.2 Optimization Strategies

**Deduplication:**
- Pre-filter B-layer by score ≥50 before comparison
- Use content hash for exact-match fast path
- Only run similarity on hash-collided candidates
- Limit B-layer check to last 1000 entries (by created_at DESC)

**Scoring:**
- Rule-based scoring is O(n×m) where n=entries, m=fact_terms (~50)
- LLM scoring is O(n) network calls — batch for efficiency
- Cache scoring results in `.state/` for idempotent runs

**B-layer Writes:**
- Use SQLite transactions for batch commits
- Single INSERT per entry, batch commit at end
- Archive writes are I/O bound — async in future versions

### 13.3 Caching Strategy

```python
# State directory for idempotent runs
.state/
  deduplicated_entries.json  # Dedup results cache
  scored_entries.json        # Scoring results cache

# These files allow re-running optimize.sh without re-scoring
# Delete .state/ to force fresh run
```

---

## 14. Security Considerations

### 14.1 Data Privacy

| Concern | Mitigation |
|---------|------------|
| Memory content exposure | B-layer SQLite in `~/.openclaw/memory/` — user-only readable |
| Config file injection | YAML config parsed safely, no `eval()` |
| Path traversal | All paths resolved via `Path.resolve()` before use |
| SQL injection | All SQLite uses parameterized queries (no string concat) |

### 14.2 Permission Model

- B-layer writes require user filesystem permissions (standard for local AI)
- No network calls in MVP (Pro LLM scoring is opt-in)
- Archive writes go to user-writable directory

---

## 15. Future Roadmap (Post-MVP)

| Version | Feature | Priority |
|---------|---------|----------|
| v1.1 (Pro) | LLM-based scoring with reason explanations | P1 |
| v1.1 (Pro) | Embedding-based semantic deduplication | P1 |
| v1.1 (Pro) | Grounded backfill queue | P1 |
| v1.2 | Multi-agent memory sharing | P2 |
| v1.2 | Obsidian/Notion export | P2 |
| v1.2 | Cross-session context chaining | P2 |
| v1.3 | Visualization dashboard | P3 |
| v1.3 | Memory encryption | P3 |

---

## 16. Monitoring & Observability

### 16.1 Metrics to Track

```python
# Key metrics for operations monitoring
METRICS = {
    "entries_scored_total": counter,
    "entries_passed_total": counter,
    "entries_archived_total": counter,
    "entries_merged_total": counter,
    "entries_committed_total": counter,
    "scoring_duration_seconds": histogram,
    "dedup_duration_seconds": histogram,
    "blayer_write_duration_seconds": histogram,
    "blayer_memory_count": gauge,
}
```

### 16.2 Logging Levels

| Level | When Used |
|-------|----------|
| DEBUG | Token similarity scores, entry content excerpts |
| INFO | Pipeline phase transitions, counts, thresholds |
| WARNING | Config not found, empty directories, truncated content |
| ERROR | SQLite write failures, schema creation failures |

### 16.3 Alert Conditions

| Condition | Severity | Action |
|-----------|----------|--------|
| B-layer write failure | CRITICAL | Alert user, skip commit |
| All entries below threshold | WARNING | Log info, suggest lowering threshold |
| Dedup merge rate >50% | WARNING | B-layer may be saturating |
| Archive directory >1GB | INFO | Suggest cleanup or increase threshold |

---

## 17. Testing Requirements

### 17.1 Test Fixtures

```python
# tests/fixtures/sample_memory.md
---
date: 2026-04-17
---

# Test Entry 1 — High Value
已修复了数据库连接池的bug，优化了查询性能。
部署到生产环境后，QPS从120提升到350。

# Test Entry 2 — Medium Value
我觉得这个API设计可以进一步优化。
可能需要引入缓存层来减少数据库压力。

# Test Entry 3 — Low Value
今天天气不错。
```

### 17.2 Mock B-layer for Testing

```python
# tests/fixtures/mock_blayer.sqlite
-- Create test SQLite with known content for dedup testing
```

### 17.3 CI/CD Integration

```bash
# .github/workflows/test.yml
name: Test dreaming-optimizer
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: cd dreaming-optimizer && pip install pytest && pytest tests/ -v
```

---

## 18. Deployment Guide

### 18.1 ClawHub Publishing Checklist

- [ ] SKILL.md is complete and accurate
- [ ] DESIGN.md is complete (>1000 lines)
- [ ] All bin/*.py files have executable permissions (`chmod +x`)
- [ ] `bin/optimize.sh --help` works
- [ ] Tests pass locally: `pytest tests/ -v`
- [ ] README.md has clear usage examples
- [ ] Pricing tiers are documented
- [ ] Screenshots/demo video prepared
- [ ] Changelog started at v1.0.0

### 18.2 Version Numbering

Follows Semantic Versioning (SemVer):
- MAJOR: Breaking changes (B-layer schema changes)
- MINOR: New features (LLM scoring, embedding dedup)
- PATCH: Bug fixes, documentation updates

### 18.3 Breaking Changes Policy

If B-layer schema changes:
1. Run migration script to update existing DBs
2. Keep backward compatibility for 2 minor versions
3. Document migration steps in release notes

---

*End of DESIGN.md — dreaming-optimizer v1.0.0*
