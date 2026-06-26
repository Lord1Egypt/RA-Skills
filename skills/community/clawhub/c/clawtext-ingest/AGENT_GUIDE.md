# Agent Integration Guide

**For OpenClaw agents and subagents:** Complete guide to autonomous memory ingestion workflows.

---

## Overview

ClawText-Ingest provides multiple APIs for agents to autonomously ingest data:

1. **CLI-based** — Simplest, run as subprocess
2. **Node.js API** — Direct use in agent code
3. **Discord Agent** — Purpose-built for Discord ingestion
4. **Scheduled/Cron** — Recurring ingestion tasks

Choose based on your agent's architecture and needs.

---

## Pattern 1: Direct API (In-Agent Code)

Best for: Agents that ingest data as part of their workflow.

### Basic Example

```javascript
import { ClawTextIngest } from 'clawtext-ingest';

async function agentIngestDocumentation() {
  const ingest = new ClawTextIngest();
  
  // Ingest documentation files
  const result = await ingest.fromFiles(
    ['docs/**/*.md'],
    {
      project: 'documentation',
      type: 'fact',
      source: 'agent-import'
    }
  );
  
  // Rebuild ClawText clusters
  await ingest.rebuildClusters();
  
  console.log(`✅ Ingested ${result.imported} documents`);
  return result;
}
```

### With Error Handling

```javascript
async function agentIngestWithFallback(config) {
  const ingest = new ClawTextIngest();
  
  try {
    const result = await ingest.fromFiles(
      config.patterns,
      config.metadata
    );
    
    if (result.errors.length > 0) {
      console.warn(`⚠️ ${result.errors.length} items failed:`, result.errors);
    }
    
    await ingest.rebuildClusters();
    return result;
    
  } catch (err) {
    console.error('Ingestion failed:', err.message);
    // Fallback: log error, don't crash agent
    return { imported: 0, skipped: 0, errors: [err] };
  }
}
```

---

## Pattern 2: Discord Agent (Autonomous)

Best for: Autonomous agents that fetch and ingest Discord content.

### Minimal Example

```javascript
import { DiscordIngestionRunner } from 'clawtext-ingest/src/agent-runner.js';
import ClawTextIngest from 'clawtext-ingest';

async function autonomousDiscordIngest(forumId) {
  const ingest = new ClawTextIngest();
  const runner = new DiscordIngestionRunner(ingest);
  
  const result = await runner.ingestForumAutonomous({
    forumId,
    mode: 'batch',
    token: process.env.DISCORD_TOKEN
  });
  
  console.log(`✅ Ingested ${result.summary.ingestedMessages} messages`);
  return result;
}

// Usage
await autonomousDiscordIngest('123456789');
```

### With Progress Tracking

```javascript
async function autonomousDiscordWithProgress(forumId) {
  const ingest = new ClawTextIngest();
  const runner = new DiscordIngestionRunner(ingest);
  
  const result = await runner.ingestForumAutonomous({
    forumId,
    mode: 'batch',
    token: process.env.DISCORD_TOKEN,
    batchSize: 50,
    concurrency: 3,
    onProgress: (progress) => {
      const pct = ((progress.current / progress.total) * 100).toFixed(0);
      const elapsed = ((Date.now() - progress.startTime) / 1000).toFixed(1);
      console.log(
        `[${pct}%] ${progress.current}/${progress.total} ` +
        `in ${elapsed}s (batch ${progress.batchNumber})`
      );
    }
  });
  
  return result;
}
```

### Full Configuration

```javascript
const result = await runner.ingestForumAutonomous({
  // Required
  forumId: '123456789',
  
  // Mode selection
  mode: 'batch',  // full, batch, or posts-only
  
  // Performance tuning
  batchSize: 50,       // Messages per batch
  concurrency: 3,      // Parallel requests
  
  // Content filtering
  preserveHierarchy: true,    // Keep post↔reply structure
  skipEmbeds: true,          // Skip Discord embeds
  skipAttachments: true,      // Skip attachment metadata
  
  // Deduplication
  dedupStrategy: 'strict',    // strict, lenient, or skip
  
  // Agent integration
  token: process.env.DISCORD_TOKEN,
  onProgress: (progress) => { /* ... */ },
  
  // Optional: save to disk
  outputPath: 'forum-export.json'
});
```

---

## Pattern 3: CLI-Based (Subprocess)

Best for: Agents that trigger CLI commands.

### Using execSync

```javascript
import { execSync } from 'child_process';

async function agentFetchDiscordViaCli(forumId) {
  try {
    const output = execSync(
      `DISCORD_TOKEN=${process.env.DISCORD_TOKEN} ` +
      `clawtext-ingest-discord fetch-discord ` +
      `--forum-id ${forumId} --verbose`,
      { encoding: 'utf-8', timeout: 300000 }  // 5 min timeout
    );
    
    console.log(output);
    return { success: true, output };
    
  } catch (err) {
    console.error('CLI command failed:', err.message);
    return { success: false, error: err.message };
  }
}
```

### Using execFile

```javascript
import { execFile } from 'child_process';
import { promisify } from 'util';

const execFileAsync = promisify(execFile);

async function agentIngestViaCliAsync(forumId) {
  try {
    const { stdout, stderr } = await execFileAsync(
      'clawtext-ingest-discord',
      ['fetch-discord', '--forum-id', forumId, '--verbose'],
      { env: { ...process.env, DISCORD_TOKEN: process.env.DISCORD_TOKEN } }
    );
    
    return { success: true, stdout };
    
  } catch (err) {
    return { success: false, error: stderr };
  }
}
```

---

## Pattern 4: Cron-Based Recurring Ingestion

Best for: Periodic tasks (hourly, daily, weekly syncs).

### OpenClaw Cron Job

```javascript
// In your cron job configuration
const cronJob = {
  schedule: { kind: 'cron', expr: '0 */4 * * *' },  // Every 4 hours
  payload: {
    kind: 'agentTurn',
    message: `
      Ingest recent documentation into memory.
      Use ClawTextIngest to update all docs/**/*.md into project "docs".
      Then rebuild clusters. Report count of items ingested.
    `
  },
  sessionTarget: 'isolated'
};
```

### Direct Scheduled Function

```javascript
import { CronJob } from 'cron';
import { ClawTextIngest } from 'clawtext-ingest';

// Run every 6 hours
const job = new CronJob('0 */6 * * *', async () => {
  console.log('Running daily memory sync...');
  
  try {
    const ingest = new ClawTextIngest();
    
    const result = await ingest.ingestAll([
      {
        type: 'files',
        data: ['recent-notes/**/*.md'],
        metadata: { project: 'daily-notes', type: 'note' }
      },
      {
        type: 'files',
        data: ['decisions/**/*.md'],
        metadata: { project: 'decisions', type: 'decision' }
      }
    ]);
    
    await ingest.rebuildClusters();
    
    console.log(`✅ Synced: ${result.totalImported} items`);
    
  } catch (err) {
    console.error('❌ Sync failed:', err.message);
  }
});

job.start();
```

---

## Pattern 5: Batch Multi-Source Ingestion

Best for: Agents that collect from multiple sources.

### Unified Batch Ingest

```javascript
async function agentMultiSourceIngest() {
  const ingest = new ClawTextIngest();
  
  const result = await ingest.ingestAll([
    // Source 1: Local documentation
    {
      type: 'files',
      data: ['docs/**/*.md'],
      metadata: {
        project: 'documentation',
        type: 'fact',
        source: 'internal-docs'
      }
    },
    
    // Source 2: External API docs
    {
      type: 'urls',
      data: [
        'https://api.example.com/docs',
        'https://api.example.com/guide'
      ],
      metadata: {
        project: 'api-docs',
        type: 'documentation',
        source: 'external-api'
      }
    },
    
    // Source 3: Chat export (JSON)
    {
      type: 'json',
      data: chatExport,
      metadata: {
        project: 'team-discussions',
        type: 'decision',
        source: 'slack'
      },
      options: {
        keyMap: {
          contentKey: 'text',
          dateKey: 'timestamp',
          authorKey: 'user'
        }
      }
    },
    
    // Source 4: Raw text (quick findings)
    {
      type: 'text',
      data: 'Key learning: Always validate input',
      metadata: {
        project: 'lessons-learned',
        type: 'finding',
        source: 'agent-observation'
      }
    }
  ]);
  
  // Check for errors
  if (result.errors.length > 0) {
    console.warn(`⚠️ ${result.errors.length} sources had errors`);
    result.errors.forEach(err => console.error(`  - ${err.source}: ${err.message}`));
  }
  
  // Rebuild and report
  await ingest.rebuildClusters();
  
  return {
    success: result.errors.length === 0,
    imported: result.totalImported,
    skipped: result.totalSkipped,
    errors: result.errors
  };
}
```

---

## Pattern 6: Discord Thread (Agent-Specific)

Best for: Agents monitoring Discord threads for updates.

### Thread Ingestion

```javascript
async function agentIngestThread(threadId) {
  const ingest = new ClawTextIngest();
  const runner = new DiscordIngestionRunner(ingest);
  
  // Fetch single thread
  const result = await runner.ingestForumAutonomous({
    forumId: threadId,  // Can use thread ID
    mode: 'posts-only',  // Just the thread itself
    token: process.env.DISCORD_TOKEN,
    preserveHierarchy: true
  });
  
  return result;
}

// Usage: Agent responds to new Discord thread
async function onNewDiscordThread(threadId) {
  console.log(`New thread: ${threadId}`);
  await agentIngestThread(threadId);
  console.log('Thread ingested into memory');
}
```

---

## Best Practices

### 1. Always Rebuild Clusters After Batch Ingestion

```javascript
// ✅ Good
await ingest.ingestAll([...sources]);
await ingest.rebuildClusters();  // Required!

// ❌ Bad
await ingest.ingestAll([...sources]);
// Forgot rebuild — memories won't be indexed!
```

### 2. Use Deduplication (It's Safe)

```javascript
// ✅ Good: Dedup enabled (default)
await ingest.fromFiles(patterns, metadata);
// Can run repeatedly without duplicates

// ⚠️ Only use this if you're absolutely sure no duplicates exist:
await ingest.fromFiles(patterns, metadata, { checkDedupe: false });
```

### 3. Log Ingestion Results

```javascript
async function agentIngestWithReporting(config) {
  const result = await ingest.ingestAll(config.sources);
  
  // Log for debugging
  console.log(`📊 Ingestion Report:`);
  console.log(`  ✅ Imported: ${result.totalImported}`);
  console.log(`  ⏭️  Skipped: ${result.totalSkipped}`);
  console.log(`  ❌ Errors: ${result.errors.length}`);
  
  if (result.errors.length > 0) {
    result.errors.forEach(e => console.error(`    - ${e}`));
  }
  
  return result.errors.length === 0;
}
```

### 4. Handle Large Batches

```javascript
async function agentIngestLargeForum(forumId) {
  const runner = new DiscordIngestionRunner(new ClawTextIngest());
  
  // Let it auto-detect batch mode (≥500 posts)
  const result = await runner.ingestForumAutonomous({
    forumId,
    // Auto-selects batch mode if needed
    // Large forums won't crash due to memory limits
  });
  
  return result;
}
```

### 5. Use Metadata for Routing

```javascript
// Different metadata → different ClawText clusters
await ingest.ingestAll([
  {
    type: 'files',
    data: ['architecture/**/*.md'],
    metadata: {
      project: 'architecture',  // ClawText groups by project
      type: 'design-doc',
      entities: ['system-design']
    }
  },
  {
    type: 'files',
    data: ['incidents/**/*.md'],
    metadata: {
      project: 'incidents',  // Different project
      type: 'postmortem',
      entities: ['incidents']
    }
  }
]);

// Later, queries about "architecture" get first cluster,
// queries about "incidents" get second cluster
```

---

## Common Agent Tasks

### Task 1: Sync GitHub Docs Daily

```javascript
async function dailyGithubSync() {
  // Fetch latest from GitHub
  const docs = await fetchGithubDocs('org/repo', 'docs/**/*.md');
  
  // Ingest
  const ingest = new ClawTextIngest();
  await ingest.fromFiles(docs.localPaths, {
    project: 'github-docs',
    source: 'github',
    type: 'documentation'
  });
  
  await ingest.rebuildClusters();
}
```

### Task 2: Monitor Discord Forum (Every 1 Hour)

```javascript
async function hourlyDiscordCheck(forumId) {
  const runner = new DiscordIngestionRunner(new ClawTextIngest());
  
  // Get new messages since last run
  const lastRun = fs.readJsonSync('last-discord-sync.json');
  
  const result = await runner.ingestForumAutonomous({
    forumId,
    mode: 'batch',
    token: process.env.DISCORD_TOKEN,
    // Optional: filter by date
  });
  
  // Update timestamp
  fs.writeJsonSync('last-discord-sync.json', {
    lastSyncTime: new Date().toISOString(),
    messageCount: result.summary.ingestedMessages
  });
}
```

### Task 3: Team Decision Ingestion

```javascript
async function agentIngestTeamDecisions() {
  const ingest = new ClawTextIngest();
  
  // Collect from multiple sources
  const result = await ingest.ingestAll([
    {
      type: 'files',
      data: ['decisions/adr/**/*.md'],
      metadata: { project: 'adr', type: 'architecture-decision' }
    },
    {
      type: 'json',
      data: slackThreadExport,
      metadata: { project: 'team', type: 'decision', source: 'slack' },
      options: { keyMap: { contentKey: 'text', dateKey: 'ts', authorKey: 'user' } }
    }
  ]);
  
  await ingest.rebuildClusters();
  
  // Report
  return {
    decisions: result.totalImported,
    source: 'ADRs + Slack discussions'
  };
}
```

---

## Troubleshooting

### "Memory cluster not updated after ingest"

```javascript
// ✅ Fix: Make sure you rebuild
await ingest.ingestAll([...sources]);
await ingest.rebuildClusters();  // This step is required!
```

### "High memory usage on large Discord forum"

```javascript
// ✅ Use batch mode (auto-enabled at ≥500 posts)
await runner.ingestForumAutonomous({
  forumId,
  mode: 'batch',  // Streams instead of loading all
  batchSize: 50   // Adjust based on available memory
});
```

### "Same data ingested multiple times"

```javascript
// Dedup is enabled by default - shouldn't happen
// If it does, check:
const result = await ingest.fromFiles(patterns, metadata);
console.log(`Imported: ${result.imported}, Skipped: ${result.skipped}`);

// If too many duplicates, reset:
import fs from 'fs';
fs.unlinkSync('.ingest_hashes.json');  // Reset hash store
```

### "DISCORD_TOKEN is undefined"

```javascript
// Make sure it's set before calling
if (!process.env.DISCORD_TOKEN) {
  throw new Error('DISCORD_TOKEN environment variable required');
}

const result = await runner.ingestForumAutonomous({
  forumId,
  token: process.env.DISCORD_TOKEN
});
```

---

## Performance Tips

| Task | Pattern | Speed |
|------|---------|-------|
| Ingest 100 files | `fromFiles()` | ~5 sec |
| Ingest 1000 JSON items | `fromJSON()` | ~15 sec |
| Fetch small forum (<100 msgs) | Full mode | ~10 sec |
| Fetch large forum (1000+ msgs) | Batch mode | ~2 min (streaming) |
| Rebuild clusters | `rebuildClusters()` | ~5-30 sec (depends on total memories) |

---

## Next Steps

1. **Choose your pattern** — CLI, Direct API, Discord, or Cron
2. **Copy example code** from this guide
3. **Test locally** before deploying to production
4. **Monitor results** — Check ingestion logs and cluster stats
5. **Iterate** — Adjust metadata, filtering, scheduling as needed

See [API_REFERENCE.md](./API_REFERENCE.md) for complete method documentation.
