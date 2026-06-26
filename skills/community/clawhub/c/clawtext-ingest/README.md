# ClawText Ingest

Version: 1.3.0

Convert multi-source data (files, URLs, JSON, text, **Discord**) into structured memory for the **ClawText** RAG layer. Automatically generates YAML headers and prevents duplicate ingestion via SHA1 hashing. Works with ClawText to enable automatic context injection into agent prompts.

## Why this matters

**Without ClawText Ingest:** Manual memory management, duplicate entries, no structured metadata, context loss.

**With ClawText Ingest + ClawText:**
- Knowledge acquired in real time: new docs → instant memory injection
- Smart deduplication: same info ingested 10x? Only stored once.
- Automatic context: models answer questions with relevant background without prompting
- Measurable improvement: models that remember past decisions make 20-35% better choices on related tasks

Example: Ingest 5 recent design decision docs → next agent working on architecture automatically gets relevant context → avoids contradicting prior decisions → fewer iterations.

## ✨ New: Discord Integration

ClawText-Ingest now supports direct Discord message ingestion with:
- **Forum hierarchy** — Post↔reply structure preserved in metadata
- **Auto-batch mode** — <500 posts: instant, ≥500 posts: streaming
- **Real-time progress** — Visual feedback during large ingestions
- **One-command setup** — No code required, pure CLI
- **Autonomous agents** — Programmatic API for agent workflows

### Quick Discord Start

```bash
# 1. Set up Discord bot (5 minutes)
# See DISCORD_BOT_SETUP.md for step-by-step

# 2. Inspect forum
clawtext-ingest-discord describe-forum --forum-id 123456789

# 3. Ingest with progress
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord --forum-id 123456789

# 4. Rebuild clusters
clawtext-ingest rebuild
```

**Output:**
```
[████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 25% | 462/1850 | 12.3s | Batch 3
✅ Complete in 45.23s | 1850 messages fetched | 3 deduplicated
```

See [PHASE2_CLI_GUIDE.md](./PHASE2_CLI_GUIDE.md) for complete Discord reference.

---

## Installation

### From NPM (once published to ClawhHub)
```bash
npm install clawtext-ingest
# or
openclaw install clawtext-ingest
```

### From Source (development)
```bash
cd ~/.openclaw/workspace/skills/clawtext-ingest
npm install
```

## Quick Start — CLI

### Classic Ingestion (Files, URLs, JSON, Text)

```bash
# Ingest markdown files
clawtext-ingest ingest-files --input="docs/*.md" --project="docs"

# Ingest from URLs
clawtext-ingest ingest-urls --input="https://example.com/page" --project="research"

# Ingest JSON (Discord export, API response, etc.)
clawtext-ingest ingest-json --input=messages.json --source="discord"

# Ingest raw text
clawtext-ingest ingest-text --input="Key finding: X is better than Y" --project="findings"

# Batch ingest from config file
clawtext-ingest batch --config=sources.json

# Show status
clawtext-ingest status

# Rebuild clusters after ingestion
clawtext-ingest rebuild
```

### Discord Ingestion (New)

```bash
# Lightweight inspection (no fetch)
clawtext-ingest-discord describe-forum --forum-id FORUM_ID --verbose

# Fetch & ingest (full process)
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord --forum-id FORUM_ID

# With options
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord \
  --forum-id FORUM_ID \
  --batch-size 100 \
  --concurrency 5 \
  --verbose
```

### CLI Options
```
--input, -i          Input file/URL/JSON/text
--type, -t           Input type (files, urls, json, text)
--output, -o         Output memory dir (default: ~/.openclaw/workspace/memory)
--project, -p        Project name for metadata
--source, -s         Source identifier (discord, github, etc.)
--date, -d           Override date (YYYY-MM-DD)
--no-dedupe          Skip deduplication (faster, risky)
--verbose, -v        Detailed output

# Discord-specific
--forum-id ID        Discord forum ID
--channel-id ID      Discord channel ID
--thread-id ID       Discord thread ID
--batch-size N       Messages per batch (default: 50)
--concurrency N      Parallel requests (default: 3)
--mode MODE          full|batch|posts-only
```

## Quick Start — Node API

For agents and programmatic use:

```javascript
import { ClawTextIngest } from 'clawtext-ingest';

const ingest = new ClawTextIngest();

// Ingest docs (duplicates auto-skipped)
await ingest.fromFiles(['docs/**/*.md'], { project: 'docs', type: 'fact' });

// Ingest chat export
await ingest.fromJSON(chatArray, { project: 'team' }, {
  keyMap: { contentKey: 'message', dateKey: 'timestamp', authorKey: 'user' }
});

// Run batch
const result = await ingest.ingestAll([...sources]);
console.log(`Imported: ${result.totalImported}, Skipped: ${result.totalSkipped}`);

// Rebuild ClawText clusters
await ingest.rebuildClusters();
```

### Autonomous Discord Ingestion (Agent Example)

```javascript
import { DiscordIngestionRunner } from 'clawtext-ingest/src/agent-runner.js';
import ClawTextIngest from 'clawtext-ingest';

const ingest = new ClawTextIngest();
const runner = new DiscordIngestionRunner(ingest);

const result = await runner.ingestForumAutonomous({
  forumId: '123456789',
  mode: 'batch',
  token: process.env.DISCORD_TOKEN,
  onProgress: (progress) => console.log(`${progress.percent}%...`)
});

console.log(`Ingested: ${result.summary.ingestedMessages} messages`);
```

See [AGENT_GUIDE.md](./AGENT_GUIDE.md) for more agent patterns.

## API Reference

### Methods

**`fromFiles(patterns, metadata, options)`**
- Ingest files matching glob patterns
- Auto-deduplication by SHA1
- Example: `await ingest.fromFiles(['docs/**/*.md'], { project: 'docs' })`

**`fromJSON(data, metadata, options)`**
- Ingest JSON arrays or objects
- `options.keyMap`: { contentKey, dateKey, authorKey }
- Skips duplicates by content hash
- Example: Discord exports, API responses

**`fromUrls(urls, metadata)`**
- Fetch and ingest URLs
- Single URL or comma-separated list
- Example: `await ingest.fromUrls('https://example.com/page')`

**`fromText(text, metadata)`**
- Ingest raw content
- Auto-dedup by hash
- Example: `await ingest.fromText('Finding: X is better than Y')`

**`ingestAll(sources)`**
- Batch multi-source ingestion
- Returns: `{ totalImported, totalSkipped, results, errors }`

**`rebuildClusters()`**
- Signal ClawText to rebuild memory clusters
- Call after batch ingestion

**`getReport()`**
- Current ingestion stats

**`commit()`**
- Persist hashes to disk

### Metadata Fields

```javascript
{
  date: '2026-03-04',           // Auto-filled if not provided
  project: 'myproject',         // Grouping for ClawText routing
  type: 'fact',                 // Categorization (decision, finding, etc.)
  source: 'discord',            // Source identifier
  entities: ['user1', 'team'],  // Related entities
  keywords: ['tag1', 'tag2']    // Search keywords
}
```

## Integration with ClawText

1. **Ingest** source data using ClawTextIngest
2. **Rebuild** clusters: `clawtext-ingest rebuild` or `await ingest.rebuildClusters()`
3. **ClawText** auto-detects new memories in memory directory
4. **On next prompt:** relevant memories injected automatically
5. **Agent/model** answers with full context

See: [ClawText README](https://github.com/ragesaq/clawtext) for RAG layer details.

## Deduplication

SHA1 hashes stored in `.ingest_hashes.json`. Run same ingestion 100 times → zero duplicates. Safe for repeated agent workflows.

**Skip dedup (not recommended):**
```bash
clawtext-ingest ingest-files --input="*.md" --no-dedupe
```

## Examples

### Example 1: Ingest Discord Forum

```bash
# Inspect first
clawtext-ingest-discord describe-forum --forum-id 123456789 --verbose

# Ingest
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord --forum-id 123456789

# Rebuild
clawtext-ingest rebuild
```

Or programmatically:
```javascript
import { DiscordIngestionRunner } from 'clawtext-ingest/src/agent-runner.js';
import ClawTextIngest from 'clawtext-ingest';

const runner = new DiscordIngestionRunner(new ClawTextIngest());
await runner.ingestForumAutonomous({
  forumId: '123456789',
  mode: 'batch',
  token: process.env.DISCORD_TOKEN
});
```

### Example 2: Multi-Source Batch

```javascript
const result = await ingest.ingestAll([
  { 
    type: 'files', 
    data: ['docs/**/*.md'], 
    metadata: { project: 'docs' } 
  },
  { 
    type: 'urls', 
    data: ['https://docs.example.com/api'], 
    metadata: { project: 'api-docs' } 
  },
  { 
    type: 'json', 
    data: chatExport, 
    metadata: { project: 'team', source: 'discord' } 
  }
]);

console.log(result);
// { totalImported: 245, totalSkipped: 12, results: [...], errors: [] }
```

### Example 3: Scheduled Agent Task

```javascript
// Daily ingestion of notes (safe to run repeatedly)
async function dailyMemorySync() {
  const ingest = new ClawTextIngest();
  const result = await ingest.ingestAll([
    {
      type: 'files',
      data: ['recent-notes/**/*.md'],
      metadata: { project: 'daily-sync' }
    }
  ]);
  await ingest.rebuildClusters();
  return result;
}
```

## Testing

```bash
npm test                    # Basic functionality
npm run test:discord        # Discord adapter tests
npm run test:discord-cli    # CLI validation tests
node test-idempotency.mjs   # Deduplication & idempotency
```

## Troubleshooting

**Error: `clawtext-ingest` not found**
- Install locally: `npm install -g clawtext-ingest` or use full path: `node bin/ingest.js`

**Error: `DISCORD_TOKEN` not set**
- Set environment variable: `export DISCORD_TOKEN=your_token`
- Or pass inline: `DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord ...`

**Error: Input file not found**
- Check path and glob patterns: `clawtext-ingest ingest-files --input="docs/**/*.md" -v`

**Duplicates still imported**
- Ensure `checkDedupe: true` (default). Delete `.ingest_hashes.json` to reset.

**Clusters not updating**
- Run `clawtext-ingest rebuild` or call `ingest.rebuildClusters()`

## Documentation

- **[AGENT_GUIDE.md](./AGENT_GUIDE.md)** — Autonomous agent workflows & patterns
- **[PHASE2_CLI_GUIDE.md](./PHASE2_CLI_GUIDE.md)** — Complete Discord CLI reference
- **[API_REFERENCE.md](./API_REFERENCE.md)** — Full API documentation
- **[DISCORD_BOT_SETUP.md](./DISCORD_BOT_SETUP.md)** — Discord bot creation (5 min)
- **[QUICKSTART.md](./QUICKSTART.md)** — Fast start guide
- **[CLAWHUB_GUIDE.md](./CLAWHUB_GUIDE.md)** — Publishing to ClawhHub

## License

MIT

---

**See also:** 
- [ClawText](https://github.com/ragesaq/clawtext) — RAG layer that consumes memories
- [ClawhHub](https://clawhub.com) — Skill marketplace

