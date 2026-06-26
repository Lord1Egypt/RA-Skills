# ClawText-Ingest CLI Guide

## Overview

ClawText-Ingest v1.2.0 includes both a **Node.js API** and a **command-line tool** for flexible data ingestion.

- **API:** Use in Node.js scripts and agents
- **CLI:** Use for one-off ingestion, automation scripts, and subagent workflows

Both methods produce identical results with automatic deduplication and ClawText integration.

## Installation

### Global (recommended for CLI use)
```bash
npm install -g clawtext-ingest
clawtext-ingest help
```

### Local (for development)
```bash
cd ~/.openclaw/workspace/skills/clawtext-ingest
npm install
node bin/ingest.js help
```

### Via OpenClaw
```bash
openclaw install clawtext-ingest
clawtext-ingest --help
```

## Commands

### 1. `ingest-files` — Import files from glob patterns

Ingest markdown, text, or any file type matching a glob pattern.

```bash
# Single pattern
clawtext-ingest ingest-files --input="docs/*.md" --project="docs"

# Multiple patterns (quoted)
clawtext-ingest ingest-files --input="docs/**/*.md" --project="docs"

# With metadata
clawtext-ingest ingest-files \
  --input="docs/**/*.md" \
  --project="docs" \
  --source="file-system" \
  --date="2026-03-04"

# Verbose output
clawtext-ingest ingest-files --input="*.txt" --project="notes" -v
```

**Options:**
- `--input, -i` — Glob pattern (required)
- `--project, -p` — Project name (default: "ingestion")
- `--source, -s` — Source identifier (default: "cli:files")
- `--date, -d` — Date override (default: today)
- `--no-dedupe` — Skip deduplication (faster, risky)
- `--verbose, -v` — Detailed output

---

### 2. `ingest-urls` — Fetch and ingest web content

Download and ingest content from URLs.

```bash
# Single URL
clawtext-ingest ingest-urls \
  --input="https://example.com/docs" \
  --project="research"

# Multiple URLs (comma-separated)
clawtext-ingest ingest-urls \
  --input="https://example.com/page1,https://example.com/page2" \
  --project="research"

# With verbose output
clawtext-ingest ingest-urls \
  --input="https://docs.example.com/api" \
  --project="api-docs" \
  -v
```

**Options:**
- `--input, -i` — URL or comma-separated URLs (required)
- `--project, -p` — Project name (default: "ingestion")
- `--source, -s` — Source identifier (default: "cli:urls")
- `--date, -d` — Date override (default: today)
- `--verbose, -v` — Detailed output

---

### 3. `ingest-json` — Import JSON data

Ingest JSON arrays or objects from files or inline.

```bash
# From file (Discord export, API response, etc.)
clawtext-ingest ingest-json \
  --input=messages.json \
  --source="discord" \
  --project="team-chat"

# From inline JSON (small datasets)
clawtext-ingest ingest-json \
  --input='[{"content":"idea 1"},{"content":"idea 2"}]' \
  --project="brainstorm"

# Discord thread with custom field mapping
clawtext-ingest ingest-json \
  --input=discord-export.json \
  --type="discord-thread" \
  --source="discord" \
  --project="discussions" \
  --verbose
```

**Options:**
- `--input, -i` — JSON file path or inline JSON (required)
- `--type, -t` — Data type (discord-thread, slack-export, etc.) (default: json)
- `--project, -p` — Project name (default: "ingestion")
- `--source, -s` — Source identifier (default: "cli:json")
- `--date, -d` — Date override (default: today)
- `--no-dedupe` — Skip deduplication
- `--verbose, -v` — Detailed output

---

### 4. `ingest-text` — Import raw text

Ingest raw text content directly.

```bash
# Direct text
clawtext-ingest ingest-text \
  --input="Key finding: approach X is better than Y" \
  --project="findings"

# From file
clawtext-ingest ingest-text \
  --input=notes.txt \
  --project="notes"

# With all metadata
clawtext-ingest ingest-text \
  --input="Important decision: we chose architecture A" \
  --project="decisions" \
  --source="team-notes" \
  --date="2026-03-03"
```

**Options:**
- `--input, -i` — Text or path to text file (required)
- `--project, -p` — Project name (default: "ingestion")
- `--source, -s` — Source identifier (default: "cli:text")
- `--date, -d` — Date override (default: today)
- `--verbose, -v` — Detailed output

---

### 5. `batch` — Batch ingest from configuration

Ingest multiple sources in one command using a config file.

```bash
# Create ingest.json
cat > ingest.json << 'EOF'
{
  "sources": [
    {
      "type": "files",
      "data": ["docs/**/*.md"],
      "metadata": { "project": "docs" }
    },
    {
      "type": "json",
      "data": "discord-export.json",
      "metadata": { "project": "team", "source": "discord" }
    },
    {
      "type": "text",
      "data": "Team decision: use Node.js for backend",
      "metadata": { "project": "decisions" }
    }
  ]
}
EOF

# Run batch
clawtext-ingest batch --config=ingest.json -v
```

**Options:**
- `--config, -c` — Path to config JSON file (required)
- `--verbose, -v` — Detailed output

---

### 6. `rebuild` — Rebuild ClawText clusters

Signal ClawText to rebuild memory clusters after ingestion.

```bash
clawtext-ingest rebuild
```

Run this after ingesting new data to rebuild BM25 indices and entity clusters.

---

### 7. `status` — Show ingestion status

Display ingestion statistics and errors.

```bash
# Quick status
clawtext-ingest status

# Verbose (show recent errors)
clawtext-ingest status -v
```

---

### 8. `help` — Show help

```bash
clawtext-ingest help
clawtext-ingest help ingest-files
clawtext-ingest --help
```

---

## Common Workflows

### Workflow 1: Daily Ingestion with Deduplication

Ingest daily notes without worrying about duplicates:

```bash
#!/bin/bash
# daily-ingest.sh - runs every morning

clawtext-ingest ingest-files \
  --input="~/notes/daily/*.md" \
  --project="daily-notes" \
  --source="daily-workflow" \
  --verbose

clawtext-ingest rebuild
echo "✅ Daily ingestion complete"
```

### Workflow 2: Discord Thread Archive

Archive discussion threads to memory:

```bash
#!/bin/bash
# archive-discord-thread.sh

# Export thread from Discord (JSON format)
THREAD_FILE="thread-$(date +%s).json"

# Ingest to memory
clawtext-ingest ingest-json \
  --input="$THREAD_FILE" \
  --source="discord" \
  --type="discord-thread" \
  --project="discussions" \
  --verbose

# Rebuild clusters
clawtext-ingest rebuild

echo "✅ Thread archived: $THREAD_FILE"
```

### Workflow 3: Batch Import Multiple Sources

```bash
#!/bin/bash
# batch-import.sh

cat > import-config.json << 'EOF'
{
  "sources": [
    {
      "type": "files",
      "data": ["docs/**/*.md"],
      "metadata": { "project": "documentation" }
    },
    {
      "type": "urls",
      "data": ["https://docs.example.com/api", "https://docs.example.com/guide"],
      "metadata": { "project": "external-docs" }
    },
    {
      "type": "json",
      "data": "team-decisions.json",
      "metadata": { "project": "decisions", "source": "team-archive" }
    }
  ]
}
EOF

clawtext-ingest batch --config=import-config.json -v
clawtext-ingest rebuild

echo "✅ Batch import complete"
```

### Workflow 4: Subagent Integration

Use CLI in OpenClaw subagent workflows:

```javascript
// In an OpenClaw subagent script
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function ingestDiscordThread(threadData) {
  const tmpFile = `/tmp/thread-${Date.now()}.json`;
  fs.writeFileSync(tmpFile, JSON.stringify(threadData));

  try {
    const { stdout } = await execAsync(
      `clawtext-ingest ingest-json --input=${tmpFile} --source=discord --project=discussions -v`
    );
    console.log(stdout);

    // Rebuild clusters
    await execAsync('clawtext-ingest rebuild');
    console.log('✅ Thread ingested and clusters rebuilt');
  } finally {
    fs.unlinkSync(tmpFile);
  }
}
```

---

## Options Reference

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--input` | `-i` | string | *(required)* | Input data (file, URL, JSON, or text) |
| `--type` | `-t` | string | `json` | Input type/category |
| `--output` | `-o` | string | `~/.openclaw/workspace/memory` | Memory directory |
| `--project` | `-p` | string | `ingestion` | Project name for grouping |
| `--source` | `-s` | string | `cli:{type}` | Source identifier |
| `--date` | `-d` | string (YYYY-MM-DD) | *(today)* | Override date |
| `--no-dedupe` | — | flag | *(off)* | Skip deduplication |
| `--verbose` | `-v` | flag | *(off)* | Detailed output |
| `--help` | `-h` | flag | — | Show help |
| `--config` | `-c` | string | — | Batch config file |

---

## Examples by Source Type

### Markdown Documentation
```bash
clawtext-ingest ingest-files \
  --input="docs/**/*.md" \
  --project="documentation" \
  --type="documentation"
```

### Discord Server Export
```bash
# Export from Discord, then:
clawtext-ingest ingest-json \
  --input=discord-server-export.json \
  --source="discord" \
  --type="discord-server" \
  --project="team-discussions"
```

### Slack Channel Archive
```bash
clawtext-ingest ingest-json \
  --input=slack-export.json \
  --source="slack" \
  --type="slack-channel" \
  --project="team-chat"
```

### GitHub Issue Tracker
```bash
# Export from GitHub API, then:
clawtext-ingest ingest-json \
  --input=issues.json \
  --source="github" \
  --type="issues" \
  --project="bug-tracking"
```

### Web Scraping
```bash
clawtext-ingest ingest-urls \
  --input="https://example.com/page1,https://example.com/page2" \
  --source="web-scrape" \
  --project="research"
```

### Local Notes
```bash
clawtext-ingest ingest-files \
  --input="notes/**/*.txt" \
  --project="personal-notes" \
  --type="note"
```

---

## Troubleshooting

### Error: `clawtext-ingest: command not found`
- **Solution 1:** Install globally: `npm install -g clawtext-ingest`
- **Solution 2:** Use full path: `node /path/to/bin/ingest.js`
- **Solution 3:** Use from workspace: `cd ~/.openclaw/workspace/skills/clawtext-ingest && node bin/ingest.js`

### Error: `Input file not found`
- Check glob pattern matches: `clawtext-ingest ingest-files --input="docs/**/*.md" -v`
- Verify file exists: `ls -la docs/`

### No output after ingestion
- Run with verbose: `clawtext-ingest ... -v`
- Check memory directory: `ls -la ~/.openclaw/workspace/memory/`
- Verify ClawText clusters rebuilt: `clawtext-ingest rebuild`

### Duplicates still being imported
- Verify dedup is enabled (default): check `~/.openclaw/workspace/memory/.ingest_hashes.json`
- Reset hashes if needed: `rm ~/.openclaw/workspace/memory/.ingest_hashes.json`

### JSON parsing errors
- Ensure input is valid JSON: `cat input.json | jq .` should work
- Or provide inline JSON: `--input='[{"key":"value"}]'`

---

## Integration with ClawText

After ingestion, rebuild clusters to enable RAG:

```bash
# 1. Ingest data
clawtext-ingest ingest-files --input="docs/**/*.md" --project="docs"

# 2. Rebuild ClawText clusters
clawtext-ingest rebuild

# 3. Verify (optional)
clawtext-ingest status

# 4. On next OpenClaw prompt, memories auto-inject!
```

---

## Performance Tips

- **Large batches:** Use `batch` command instead of multiple individual commands
- **Skip dedup (risky):** Use `--no-dedupe` only if you're sure no duplicates exist
- **Verbose output:** Use `-v` only when debugging; it slows down large ingestions

---

## See Also

- [README.md](./README.md) — Full documentation
- [SKILL.md](./SKILL.md) — API reference
- [ClawText](https://github.com/ragesaq/clawtext) — RAG layer
- [OpenClaw](https://github.com/openclaw/openclaw) — Agent framework

---

**Version:** 1.2.0  
**Updated:** 2026-03-04
