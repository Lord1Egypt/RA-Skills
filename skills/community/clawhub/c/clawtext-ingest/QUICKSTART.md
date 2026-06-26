# Discord Ingestion Phase 1: Quick Start

## Fastest Path to Running Everything

### 1. Unit Tests (No Discord Token Needed)

```bash
cd ~/.openclaw/workspace/skills/clawtext-ingest

# Run all unit tests (12 tests, instant)
npm run test:discord
```

**Output:**
```
✓ Test 1: Adapter initialization ✅
✓ Test 2: Missing token error ✅
... (12 total, all pass)
```

---

### 2. Integration Tests (Requires Discord Bot Token)

**First time only:** Set up bot token (5 minutes)

```bash
# Follow DISCORD_BOT_SETUP.md to:
# 1. Create Discord app
# 2. Create bot user
# 3. Grant permissions
# 4. Invite to test server
# 5. Copy token
```

**Then run tests:**

```bash
export DISCORD_TOKEN="your_token_here"
npm run test:discord-integration
```

**What it does:**
- Authenticates with your Discord bot
- Lists your servers
- Finds forums
- Fetches forum structure
- Fetches first post (all messages)
- Validates message structure
- Simulates ingestion

---

### 3. Code Review

Key files to skim:

| File | Size | Purpose | Read Time |
|------|------|---------|-----------|
| `PHASE1_SUMMARY.md` | 5 KB | Overview + design decisions | 10 min |
| `src/adapters/discord.js` | 14 KB | Core adapter (skip internals) | 5 min |
| `src/agent-runner.js` | 9 KB | Agent wrapper | 3 min |
| `test-discord.mjs` | 10 KB | Unit tests (skim test names) | 2 min |

**Critical sections:**
1. PHASE1_SUMMARY.md: "Design Highlights" (forum hierarchy)
2. discord.js: `describeForumStructure()` method (simplest)
3. agent-runner.js: `ingestForumAutonomous()` (entry point)

---

## Architecture Overview

```
DiscordAdapter (low-level)
  ├─ fetchForumStructure()      [lightweight inspection]
  ├─ fetchForumHierarchy()      [list posts, no messages]
  ├─ fetchForumCompletely()     [full fetch, <500 posts]
  └─ fetchForumInBatches()      [stream, >500 posts]
        ↓
DiscordIngestionRunner (high-level)
  └─ ingestForumAutonomous()     [agent entry point]
        ├─ full mode   (small forums)
        ├─ batch mode  (large forums)
        └─ posts-only  (just roots)
```

---

## Message Format

Every message includes forum context:

```javascript
{
  id: "msg_123",
  source: "discord",
  sourceType: "forum_post_reply",  // or "forum_post_root"
  content: "This is the message",
  author: "alice",
  authorId: "user_456",
  timestamp: 1709619283000,
  
  // Forum-specific metadata
  forumHierarchy: {
    forumId: "forum_001",
    forumName: "Knowledge Base",
    postId: "post_789",
    postName: "ClawText Design Decisions",
    depth: 0,  // 0 = post root, 1+ = replies
    threadPath: "Knowledge Base > ClawText Design Decisions"
  },
  
  // Message-level metadata
  metadata: {
    reactionsCount: 3,
    edited: false,
    mentions: ["@alice", "@bob"],
    links: ["https://example.com"]
  }
}
```

---

## Config Examples

### Small Forum (Auto Full Mode)

```javascript
await runner.ingestForumAutonomous({
  forumId: '123456789',
  mode: 'full',
  skipEmbeds: true,
  skipAttachments: true,
  preserveHierarchy: true,
  dedupStrategy: 'strict',
});
```

### Large Forum (Batch Mode)

```javascript
await runner.ingestForumAutonomous({
  forumId: '987654321',
  mode: 'batch',
  batchSize: 50,
  concurrency: 3,
  onProgress: (progress) => {
    console.log(`${progress.processed}/${progress.total}`);
  },
});
```

### Posts Only (Fast Survey)

```javascript
await runner.ingestForumAutonomous({
  forumId: '555555555',
  mode: 'posts-only',
  preserveHierarchy: false,
});
```

---

## Files & Locations

```
~/.openclaw/workspace/skills/clawtext-ingest/

src/
  adapters/
    discord.js           ← Core adapter (450 lines)
  agent-runner.js        ← Agent wrapper (280 lines)
  index.js               ← Main export (existing)

test-discord.mjs         ← Unit tests (12 tests)
test-discord-integration.mjs  ← Live Discord tests
DISCORD_BOT_SETUP.md     ← Bot creation guide
PHASE1_SUMMARY.md        ← Full technical summary
```

---

## Troubleshooting

### Unit Tests Fail
- Node.js version: must be >= 18.0.0
- Run: `node --version`
- If old: upgrade node

### Integration Tests Show "Token not set"
- Run: `export DISCORD_TOKEN="your_token_here"`
- Then: `npm run test:discord-integration`

### "Invalid Token" in Integration Tests
- Go back to DISCORD_BOT_SETUP.md step 1-4
- Double-check bot was invited to server
- Token must be current (doesn't expire by default)

### "Channel not found"
- Ensure bot has permission to view that channel
- Use numeric ID (right-click → Copy Channel ID)

### "Forum not found"
- Make sure it's a Discord Forum channel (not regular text channel)
- Bot must be invited to the forum's server

---

## Next Steps

1. ✅ Run: `npm run test:discord` (unit tests)
2. ✅ Review: Read PHASE1_SUMMARY.md
3. ✅ Setup: Follow DISCORD_BOT_SETUP.md (optional, for integration test)
4. ✅ Test: `npm run test:discord-integration` (if token ready)
5. → Approve Phase 1, then build CLI (Phase 2)

---

## Questions?

Ask about:
- Design decisions (see PHASE1_SUMMARY.md → "Questions for Review")
- Code structure (see Architecture Overview above)
- Test coverage (see PHASE1_SUMMARY.md → "Test Results")
- Next phase scope (see PHASE1_SUMMARY.md → "What's Ready for Phase 2")

All code is local—no GitHub changes yet. Review complete, then we lock it in and build the CLI wrapper.
