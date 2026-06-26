# Phase 2: Discord CLI Commands

**Status:** ✅ Complete & tested  
**Files:** `bin/discord.js`, updated `package.json`  
**Tests:** 10/10 passing  

---

## Overview

Phase 2 adds production-ready CLI commands for Discord integration. Users can now:

- Inspect forum structure without fetching all messages
- Fetch forums, channels, or threads with progress tracking
- Auto-select batch vs. full mode based on size
- Save ingestion results to JSON
- Control verbosity and output

---

## Commands

### `describe-forum` — Lightweight Forum Inspection

Show forum structure without fetching messages.

```bash
clawtext-ingest-discord describe-forum --forum-id FORUM_ID [options]
```

**Options:**
- `--forum-id ID` — Forum ID (required)
- `--verbose` — Show post names and message counts
- `--token TOKEN` — Discord bot token (or use `DISCORD_TOKEN` env var)

**Examples:**

```bash
# Quick check
clawtext-ingest-discord describe-forum --forum-id 123456789

# Detailed view (shows posts)
clawtext-ingest-discord describe-forum --forum-id 123456789 --verbose

# With explicit token
DISCORD_TOKEN=your_token clawtext-ingest-discord describe-forum --forum-id 123456789 --verbose
```

**Output:**

```
📁 Forum: Knowledge Base
   ID: 123456789
   Topic: Shared decisions and documentation
   Posts: 42
   Est. Messages: 1,850
   Tags: decision, process, faq
   Fetched at: 2026-03-05T03:10:00Z

📝 Posts (42 total):
   1. "ClawText Design Decisions" (12 messages)
   2. "Memory System Architecture" (8 messages)
   ...
```

---

### `fetch-discord` — Fetch & Ingest

Fetch Discord forums, channels, or threads and ingest into ClawText.

```bash
clawtext-ingest-discord fetch-discord --forum-id|--channel-id|--thread-id ID [options]
```

**Source Options (pick one):**
- `--forum-id ID` — Fetch entire forum
- `--channel-id ID` — Fetch text channel
- `--thread-id ID` — Fetch single thread

**Fetch Options:**
- `--mode full|batch|posts-only` — Fetch mode (default: auto-detect)
- `--batch-size N` — Messages per batch (default: 50)
- `--concurrency N` — Parallel post fetches (default: 3)

**Content Options:**
- `--skip-embeds` — Exclude Discord embeds
- `--skip-attachments` — Exclude attachment links
- `--no-hierarchy` — Don't preserve post↔reply structure

**Deduplication:**
- `--dedup strict|lenient|skip` — Dedup strategy (default: strict)

**Output:**
- `--output FILE` — Save results to JSON
- `--verbose` — Show detailed progress (default)
- `--quiet` — Minimal output

**Examples:**

```bash
# Small forum (auto full mode)
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord --forum-id 123456789

# Large forum (batch mode with progress)
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord \
  --forum-id 987654321 \
  --mode batch \
  --batch-size 100 \
  --verbose

# Posts only (fast survey)
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord \
  --forum-id 555555555 \
  --mode posts-only

# Save results
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord \
  --forum-id 123456789 \
  --output ingestion-result.json \
  --verbose

# Fetch channel
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord \
  --channel-id 111111111

# Fast ingestion (skip dedup checks)
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord \
  --forum-id 123456789 \
  --dedup skip
```

**Output (with --verbose):**

```
🔗 Connected to Discord

📊 Forum: Knowledge Base (42 posts)
   Auto-selected mode: batch

[████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 25% | 462/1850 | 12.3s | Batch 3
✅ Complete in 45.23s | 1850 messages fetched

📥 Ingesting to ClawText...
✅ Ingestion complete in 2.15s

📊 Summary:
   Fetched: 1,850 messages
   Ingested: 1,847
   Deduplicated: 3
   Posts: 42
   Hierarchy Preserved: true
```

**Output (with --quiet):**

```
✅ Fetched 1850 messages
✅ Ingested 1847 messages (3 deduplicated)
```

---

## Mode Selection

Three modes for different use cases:

| Mode | Use Case | Speed | Memory | Default At |
|------|----------|-------|--------|-----------|
| **full** | Small forums (<500 posts) | Fast | Low | <500 posts |
| **batch** | Large forums (any size) | Slower | Efficient | ≥500 posts |
| **posts-only** | Fast survey (just roots) | Very Fast | Tiny | N/A (explicit) |

**Auto mode (default):**
- Detects forum size automatically
- Uses `full` for <500 posts
- Uses `batch` for ≥500 posts

**Explicit mode:**
```bash
# Force full mode
clawtext-ingest-discord fetch-discord --forum-id 123 --mode full

# Force batch mode
clawtext-ingest-discord fetch-discord --forum-id 456 --mode batch --batch-size 100

# Posts only
clawtext-ingest-discord fetch-discord --forum-id 789 --mode posts-only
```

---

## Progress Tracking

Real-time progress bars when fetching large forums:

```
[████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 30% | 555/1850 | 18.2s | Batch 5
```

Shows:
- Progress bar (visual)
- Percentage complete
- Current position (messages fetched / total)
- Elapsed time
- Current post or batch number

Disable with `--quiet` flag.

---

## Configuration

All options can be set via:

1. **Command-line flags** (highest priority)
   ```bash
   clawtext-ingest-discord fetch-discord --forum-id 123 --batch-size 100
   ```

2. **Environment variables**
   ```bash
   export DISCORD_TOKEN=your_token
   clawtext-ingest-discord fetch-discord --forum-id 123
   ```

3. **Defaults** (lowest priority)
   - Mode: auto-detect
   - Batch size: 50
   - Concurrency: 3
   - Dedup: strict

---

## Error Handling

CLI provides clear error messages:

```bash
# Missing required argument
❌ Error: Must specify --forum-id, --channel-id, or --thread-id

# Missing token
❌ Error: DISCORD_TOKEN env var or --token flag required

# Invalid forum
❌ Error: Forum 123456789 not found or not a forum

# Network error
❌ Error: [Discord API error details]
```

Use `--verbose` flag to see full error stack trace:

```bash
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord \
  --forum-id 123 \
  --verbose
# Shows full error.stack on failure
```

---

## Examples

### Example 1: Quick Forum Inspection

```bash
# Set token once
export DISCORD_TOKEN=your_token

# Inspect without fetching
clawtext-ingest-discord describe-forum --forum-id 123456789 --verbose

# Output shows posts, size, tags
```

### Example 2: Small Forum Ingestion

```bash
# Ingests entire forum in one fetch
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord \
  --forum-id 123456789 \
  --verbose

# Uses full mode (auto-detected)
```

### Example 3: Large Forum with Progress

```bash
# Streams in batches, shows progress
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord \
  --forum-id 987654321 \
  --batch-size 100 \
  --concurrency 5 \
  --verbose

# Output: real-time progress bar
```

### Example 4: Save Ingestion Results

```bash
# Fetch and save to JSON
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord \
  --forum-id 123456789 \
  --output results.json \
  --verbose

# JSON includes:
# - metadata (forum name, source type, mode)
# - recordsCount
# - ingestResult (ingested, deduplicated)
# - relationshipMap (post↔reply structure)
```

### Example 5: Fast Survey (Posts Only)

```bash
# Just get post roots (no replies)
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord \
  --forum-id 555555555 \
  --mode posts-only \
  --quiet

# Very fast, minimal data
```

---

## Integration with ClawText-Ingest

The CLI wraps the same adapter and runner used by the API:

- **Adapter** (`src/adapters/discord.js`) — Low-level Discord fetching
- **Runner** (`src/agent-runner.js`) — Agent integration
- **CLI** (`bin/discord.js`) — User-facing commands

All share the same deduplication, hierarchy preservation, and error recovery.

---

## Testing

CLI tests verify:

✅ Help output completeness  
✅ Required argument validation  
✅ Error handling  
✅ Flag documentation  
✅ Example commands  

Run tests:
```bash
npm run test:discord-cli
```

---

## Version

**Phase 2 CLI:** v1.3.0 (after publication)  
**Requires:** Node.js >= 18.0.0  
**Dependencies:** discord.js, clawtext-ingest  

---

## Next Steps

After Phase 2:
- Update GitHub to v1.3.0
- Publish to ClawhHub
- Users can install: `clawhub install clawtext-ingest`
- CLI available as: `clawtext-ingest-discord`

---

## FAQ

**Q: How do I set the Discord token permanently?**  
A: Add to your shell profile:
```bash
export DISCORD_TOKEN=your_token
```

**Q: Which mode should I use?**  
A: Use auto-detect (default). It picks the best mode for forum size.

**Q: Can I interrupt batch processing?**  
A: Yes, Ctrl+C stops gracefully. Already-ingested batches are persisted.

**Q: How do I preserve post↔reply relationships?**  
A: They're preserved by default. Disable with `--no-hierarchy` if needed.

**Q: What happens if deduplication fails?**  
A: Falls back to per-message ingestion. Use `--dedup skip` to disable entirely.

**Q: Can I save intermediate results?**  
A: Yes, use `--output FILE` to save JSON.

