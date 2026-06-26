# Discord Ingestion API Reference — Phase 1

## Quick Reference Card

### DiscordAdapter

```javascript
import DiscordAdapter from './src/adapters/discord.js';

const adapter = new DiscordAdapter({
  token: process.env.DISCORD_TOKEN,      // Required
  includeEmbeds: false,                  // Default
  includeAttachments: false,             // Default
  resolveUsers: true,                    // Default
  threadDepth: 'full',                   // 'none' | 'replies-only' | 'full'
  concurrency: 3,                        // Parallel fetches
  batchSize: 50,                         // Messages per batch
  progressCallback: (progress) => {},    // Optional
  autoBatchThreshold: 500,               // Switch to batch at this many posts
});

await adapter.authenticate();
```

### Methods

#### `describeForumStructure(forumId)`
Lightweight inspection—no message fetch.

```javascript
const info = await adapter.describeForumStructure('123456789');

// Returns:
{
  id: '123456789',
  name: 'Knowledge Base',
  topic: 'Shared decisions and docs',
  postCount: 42,
  estimatedMessageCount: 1850,
  tags: ['decision', 'process', 'faq'],
  fetchedAt: '2026-03-05T02:56:00Z'
}
```

#### `fetchForumHierarchy(forumId)`
List all posts without fetching messages.

```javascript
const posts = await adapter.fetchForumHierarchy('123456789');

// Returns: [
//   {
//     postId: 'post_111',
//     postName: 'ClawText Design Decisions',
//     authorId: 'user_456',
//     messageCount: 12,
//     tags: ['decision'],
//     createdAt: 1709619283000,
//     updatedAt: 1709700000000,
//     archived: false
//   },
//   ...
// ]
```

#### `fetchForumCompletely(forumId)`
Full fetch for small forums. Throws error if ≥500 posts.

```javascript
const { forumMetadata, records, relationshipMap } = 
  await adapter.fetchForumCompletely('123456789');

// Returns:
{
  forumMetadata: {
    forumId: '123456789',
    forumName: 'Knowledge Base',
    totalPosts: 42,
    totalMessages: 1850,
    tags: ['decision', 'process', 'faq'],
    fetchedAt: '2026-03-05T02:56:00Z'
  },
  records: [
    {
      id: 'msg_123',
      source: 'discord',
      sourceType: 'forum_post_root',
      content: '...',
      author: 'alice',
      authorId: 'user_456',
      timestamp: 1709619283000,
      forumHierarchy: { ... },
      metadata: { ... }
    },
    // ... more messages
  ],
  relationshipMap: {
    post_111: {
      rootMessageId: 'msg_123',
      replyIds: ['msg_124', 'msg_125', ...],
      postAuthor: 'user_456',
      postTags: ['decision'],
      postName: 'ClawText Design Decisions'
    },
    // ... more posts
  }
}
```

#### `fetchForumInBatches(forumId, options)`
Stream large forums in batches. Handles forums of any size.

```javascript
for await (const batch of adapter.fetchForumInBatches('123456789', {
  batchSize: 50,
  concurrency: 3,
})) {
  // batch = { batchNumber, records, relationshipMap, forumId, forumName }
  console.log(`Batch ${batch.batchNumber}: ${batch.records.length} messages`);
  
  // Ingest as you go
  await ingester.fromJSON(batch.records, {
    source: 'discord',
    forumId: batch.forumId,
  });
}
```

#### `fetchChannel(channelId, options)`
Fetch regular text channel (non-forum).

```javascript
const { channelMetadata, records, relationshipMap } = 
  await adapter.fetchChannel('987654321', { limit: 100 });

// relationshipMap is empty for channels (no post structure)
```

#### `fetchThread(threadId, options)`
Fetch single thread or forum post.

```javascript
const { threadMetadata, records, relationshipMap } = 
  await adapter.fetchThread('555555555', { limit: 100 });

// relationshipMap = {
//   threadId: {
//     rootMessageId: 'msg_1',
//     replyIds: ['msg_2', 'msg_3', ...]
//   }
// }
```

---

### DiscordIngestionRunner

```javascript
import DiscordIngestionRunner from './src/agent-runner.js';

const runner = new DiscordIngestionRunner(ingestModule, {
  // options (optional)
});
```

#### `ingestForumAutonomous(config)`
Main entry point for agent-based ingestion.

```javascript
const result = await runner.ingestForumAutonomous({
  forumId: '123456789',                  // Required
  mode: 'batch',                         // 'full' | 'batch' | 'posts-only'
  batchSize: 50,                         // If mode='batch'
  concurrency: 3,
  skipEmbeds: true,
  skipAttachments: true,
  preserveHierarchy: true,               // Save post↔reply relationships
  dedupStrategy: 'strict',               // 'strict' | 'lenient' | 'skip'
  token: process.env.DISCORD_TOKEN,
  outputPath: './ingestion-result.json', // Optional: save intermediate
  onProgress: (progress) => {
    console.log(`${progress.processed}/${progress.total}`);
  },
});

// Returns:
{
  success: true,
  summary: {
    mode: 'batch',
    forum: 'Knowledge Base',
    totalPosts: 42,
    totalMessages: 1850,
    totalBatches: 37,
    ingestedMessages: 1847,
    deduplicatedMessages: 3,
    hierarchyPreserved: true,
    duration: '45.23s'
  },
  stats: {
    totalFetched: 1850,
    totalIngested: 1847,
    totalDeduplicated: 3,
    failed: [],
    startTime: 1709619283000,
    endTime: 1709619328230
  }
}
```

**Progress callback:**
```javascript
onProgress: (progress) => {
  // {
  //   processed: 123,
  //   total: 1850,
  //   currentPost: 'ClawText Design Decisions',
  //   batchNumber: 2,
  //   mode: 'batch'
  // }
}
```

---

### Message Format

Every fetched message is normalized to this structure:

```javascript
{
  // Identity
  id: 'msg_123',                         // Discord message ID
  source: 'discord',
  sourceType: 'forum_post_root',         // or 'forum_post_reply'
  
  // Content
  content: 'This is the message text',
  author: 'alice',                       // Username if resolveUsers=true
  authorId: 'user_456',                  // Numeric Discord ID
  timestamp: 1709619283000,
  
  // Forum-specific (if from forum)
  forumHierarchy: {
    forumId: 'forum_001',
    forumName: 'Knowledge Base',
    postId: 'post_789',
    postName: 'ClawText Design Decisions',
    depth: 0,                            // 0=root, 1+=replies
    threadPath: 'Knowledge Base > ClawText Design Decisions'
  },
  
  // Message-level metadata
  metadata: {
    reactionsCount: 3,
    edited: false,
    editedAt: null,
    mentions: ['@alice', '@bob'],
    links: ['https://example.com', ...]
  },
  
  // Optional (if includeEmbeds=true / includeAttachments=true)
  embeds: [
    { title: 'Title', description: 'Desc', url: 'https://...' }
  ],
  attachments: [
    { name: 'file.txt', url: 'https://...', size: 1024, contentType: 'text/plain' }
  ]
}
```

---

### Configuration Profiles

**Small Forum (Auto Full Mode)**
```javascript
await runner.ingestForumAutonomous({
  forumId: '123',
  mode: 'full',
  skipEmbeds: true,
  skipAttachments: true,
  dedupStrategy: 'strict',
});
```

**Large Forum (Batch Mode with Progress)**
```javascript
await runner.ingestForumAutonomous({
  forumId: '456',
  mode: 'batch',
  batchSize: 100,
  concurrency: 5,
  onProgress: (p) => console.log(`[${p.processed}/${p.total}] ${p.currentPost}`),
  dedupStrategy: 'strict',
});
```

**Posts Only (Fast Survey)**
```javascript
await runner.ingestForumAutonomous({
  forumId: '789',
  mode: 'posts-only',
  preserveHierarchy: false,
});
```

**Lenient Dedup (Performance)**
```javascript
await runner.ingestForumAutonomous({
  forumId: '999',
  mode: 'batch',
  dedupStrategy: 'lenient',  // Skip expensive dedup checks
});
```

---

### Error Handling

All errors are caught and returned in `result.success` and `result.error`:

```javascript
const result = await runner.ingestForumAutonomous({ forumId: '...' });

if (!result.success) {
  console.error(`Ingestion failed: ${result.error}`);
  // Handle gracefully
}

// Per-message failures are captured in stats.failed:
result.stats.failed.forEach(failure => {
  console.warn(`Message failed: ${failure.error}`);
});
```

---

### Testing

**Unit tests** (no token needed):
```bash
npm run test:discord
```

**Integration tests** (requires Discord token):
```bash
export DISCORD_TOKEN="your_token"
npm run test:discord-integration
```

---

### Examples

#### Example 1: Simple Forum Fetch
```javascript
import DiscordAdapter from './src/adapters/discord.js';

const adapter = new DiscordAdapter({ token: process.env.DISCORD_TOKEN });
await adapter.authenticate();

const { records } = await adapter.fetchForumCompletely('forum-id');
console.log(`Fetched ${records.length} messages`);
```

#### Example 2: Agent-Based Ingestion
```javascript
import DiscordIngestionRunner from './src/agent-runner.js';
import ClawTextIngester from 'clawtext-ingest';

const ingester = new ClawTextIngester();
const runner = new DiscordIngestionRunner(ingester);

const result = await runner.ingestForumAutonomous({
  forumId: '123456789',
  mode: 'batch',
  preserveHierarchy: true,
});

console.log(result.summary);
```

#### Example 3: Streaming Large Forum
```javascript
const adapter = new DiscordAdapter({ token: process.env.DISCORD_TOKEN });
await adapter.authenticate();

let totalMessages = 0;
for await (const batch of adapter.fetchForumInBatches('large-forum-id')) {
  totalMessages += batch.records.length;
  console.log(`Batch ${batch.batchNumber}: ${batch.records.length} messages`);
}

console.log(`Total: ${totalMessages} messages`);
```

---

### Key Decisions

1. **Auto-batch threshold (500 posts):** Prevents memory bloat; configurable via `autoBatchThreshold`
2. **Forum hierarchy preserved:** Every message knows its post and reply depth; enables future ClawText enhancements
3. **Streaming support:** Large forums ingested in batches, not loaded all at once
4. **Error recovery:** If batch fails, fall back to per-message ingestion (no data loss)
5. **Configurable content:** Agents can skip embeds/attachments, resolve usernames, control thread depth

---

### Migration Path

When Phase 2 adds CLI commands:

```bash
# Future Phase 2 CLI (not yet implemented)
clawtext-ingest fetch-discord --forum-id 123456789 --mode batch --preserve-hierarchy
clawtext-ingest describe-forum --forum-id 123456789
```

Will wrap the same `DiscordAdapter` and `DiscordIngestionRunner` classes.

