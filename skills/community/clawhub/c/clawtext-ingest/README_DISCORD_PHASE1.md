# Discord Integration Phase 1 — Documentation Index

Welcome! Here's how to navigate the Phase 1 Discord integration for ClawText-Ingest.

---

## 🎯 Start Here

Pick your path based on what you want to do:

### **"Just give me the code"**
→ Go directly to [API_REFERENCE.md](API_REFERENCE.md)  
Quick reference for all methods and configs. 2 min read.

### **"I want to understand the design"**
→ Read [PHASE1_SUMMARY.md](PHASE1_SUMMARY.md)  
Technical overview, design decisions, architecture. 15 min read.

### **"I want to run tests locally"**
→ Follow [QUICKSTART.md](QUICKSTART.md)  
Unit tests (instant), integration tests (with Discord token). 5 min.

### **"I need to set up a Discord bot"**
→ Follow [DISCORD_BOT_SETUP.md](DISCORD_BOT_SETUP.md)  
Step-by-step guide: create app, grant permissions, test token. 10 min.

### **"I want to review the code"**
→ Check [src/adapters/discord.js](src/adapters/discord.js) and [src/agent-runner.js](src/agent-runner.js)  
Fully commented, modular design. Key methods:
- `DiscordAdapter.describeForumStructure()` — simplest entry point
- `DiscordAdapter.fetchForumCompletely()` — full fetch logic
- `DiscordIngestionRunner.ingestForumAutonomous()` — agent entry point

---

## 📚 Complete Documentation

| File | Purpose | Read Time | Audience |
|------|---------|-----------|----------|
| **API_REFERENCE.md** | Quick reference: all methods, examples, configs | 5 min | Developers |
| **PHASE1_SUMMARY.md** | Technical deep dive: design, test results, next steps | 15 min | Architects, Reviewers |
| **DISCORD_BOT_SETUP.md** | Step-by-step bot creation and token setup | 10 min | First-time setup |
| **QUICKSTART.md** | Run tests locally, understand structure, troubleshoot | 5 min | Getting started |
| **API_REFERENCE.md** (this file) | Navigation guide | 2 min | Everyone |

---

## 🧪 Testing

### Unit Tests (No Token Needed)
```bash
npm run test:discord
```
Runs 12 tests covering initialization, message parsing, config validation. Takes <1 second.

### Integration Tests (Requires Discord Token)
```bash
DISCORD_TOKEN=your_token npm run test:discord-integration
```
Live Discord testing: authenticate, list servers, fetch forum structure, validate ingestion. Takes 30 seconds.

See [QUICKSTART.md](QUICKSTART.md) for details.

---

## 📁 File Structure

```
.
├── src/
│   ├── adapters/
│   │   └── discord.js          ← Core adapter (450 lines)
│   ├── agent-runner.js         ← Agent wrapper (280 lines)
│   └── index.js                ← Main export (existing)
├── test-discord.mjs            ← Unit tests (12 tests)
├── test-discord-integration.mjs ← Integration test template
│
├── API_REFERENCE.md            ← Quick reference (you are here)
├── PHASE1_SUMMARY.md           ← Technical overview
├── DISCORD_BOT_SETUP.md        ← Bot setup guide
├── QUICKSTART.md               ← Fast start
│
├── package.json                ← Added discord.js, test scripts
└── [existing ClawText files]
```

---

## 🔑 Key Concepts

### Forum Hierarchy
Every message includes metadata about its position in the forum:
```json
{
  "forumHierarchy": {
    "forumId": "...",
    "postId": "...",
    "depth": 0,  // 0 = root post, 1+ = replies
    "threadPath": "Knowledge Base > Design Decisions"
  }
}
```
This enables ClawText to traverse post↔reply relationships later.

### Auto-Batch Mode
- Forums < 500 posts: Fetch all at once (`full` mode)
- Forums ≥ 500 posts: Stream in batches (`batch` mode)
- Configurable threshold: `autoBatchThreshold: 500`

### Agent Integration
`DiscordIngestionRunner.ingestForumAutonomous()` is the agent entry point:
- Autonomous execution (no manual CLI needed)
- Progress callbacks (track in real-time)
- Error recovery (batch + per-message fallback)
- Relationship preservation (post↔reply structure saved)

---

## 🚀 Quick Start Examples

### Example 1: Simple Forum Fetch
```javascript
import DiscordAdapter from './src/adapters/discord.js';

const adapter = new DiscordAdapter({ token: process.env.DISCORD_TOKEN });
await adapter.authenticate();

const { records } = await adapter.fetchForumCompletely('123456789');
console.log(`Fetched ${records.length} messages`);
```

### Example 2: Agent-Based Ingestion
```javascript
import DiscordIngestionRunner from './src/agent-runner.js';
import ClawTextIngester from 'clawtext-ingest';

const runner = new DiscordIngestionRunner(new ClawTextIngester());

const result = await runner.ingestForumAutonomous({
  forumId: '123456789',
  mode: 'batch',
  preserveHierarchy: true,
});

console.log(result.summary);
// { forum, totalPosts, totalMessages, ingestedMessages, duration }
```

### Example 3: Large Forum with Progress
```javascript
const adapter = new DiscordAdapter({
  token: process.env.DISCORD_TOKEN,
  progressCallback: (p) => {
    console.log(`${p.processed}/${p.total} [${p.currentPost}]`);
  },
});

for await (const batch of adapter.fetchForumInBatches('large-forum-id')) {
  console.log(`Batch ${batch.batchNumber}: ${batch.records.length} messages`);
}
```

See [API_REFERENCE.md](API_REFERENCE.md) for complete API documentation.

---

## ❓ FAQ

**Q: Do I need a Discord token to understand the code?**  
A: No. Unit tests run without a token. Integration tests need one.

**Q: What's the difference between `full` and `batch` mode?**  
A: `full` fetches all messages at once (small forums). `batch` streams in chunks (large forums). Adapter automatically switches at 500+ posts.

**Q: How are post↔reply relationships preserved?**  
A: Every message includes `forumHierarchy.depth` and `forumHierarchy.postId`. ClawText can use this to traverse relationships later.

**Q: Can agents use this for autonomous ingestion?**  
A: Yes. `DiscordIngestionRunner.ingestForumAutonomous()` is designed for agent spawns. Supports progress callbacks and error recovery.

**Q: What happens if ingestion fails mid-batch?**  
A: Fallback to per-message ingestion (no data loss). Failures tracked in `stats.failed`.

See [PHASE1_SUMMARY.md](PHASE1_SUMMARY.md) § "Questions for Review" for design questions.

---

## 🔗 Next Steps

**If you haven't yet:**
1. Read [PHASE1_SUMMARY.md](PHASE1_SUMMARY.md) (technical overview)
2. Run `npm run test:discord` (verify tests pass)
3. Follow [DISCORD_BOT_SETUP.md](DISCORD_BOT_SETUP.md) (optional, for integration test)

**Then:**
- Approve Phase 1 design (ask questions if needed)
- Build Phase 2 (CLI commands: `fetch-discord`, `describe-forum`)
- Push to GitHub + ClawhHub v1.3.0

---

## 📞 Questions?

- **Architecture:** See [PHASE1_SUMMARY.md](PHASE1_SUMMARY.md) § "Design Highlights"
- **API usage:** See [API_REFERENCE.md](API_REFERENCE.md)
- **Bot setup:** See [DISCORD_BOT_SETUP.md](DISCORD_BOT_SETUP.md)
- **Getting started:** See [QUICKSTART.md](QUICKSTART.md)
- **Testing:** See [QUICKSTART.md](QUICKSTART.md) § "Testing"

---

## ✅ Phase 1 Checklist

- ✅ DiscordAdapter built (forum, channel, thread fetching)
- ✅ DiscordIngestionRunner built (agent entry point)
- ✅ 12 unit tests passing
- ✅ Integration test template ready
- ✅ Bot setup documented
- ✅ API reference documented
- ✅ Code committed to local repo
- ✅ Ready for review or Phase 2 build

---

## 🎉 You're Unblocked For

✅ Code review  
✅ Integration testing (with Discord token)  
✅ Phase 2 build (CLI + agent wrapper)  
✅ GitHub push  
✅ ClawhHub v1.3.0 publication

**What's next?** 👀
