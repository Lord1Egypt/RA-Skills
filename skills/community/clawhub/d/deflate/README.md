# 🗜️ Deflate — Intelligent Context Compression for OpenClaw

> Stop burning money on bloated context windows. Deflate keeps your conversations lean, your data safe, and your wallet happy.

## The Problem

Every message you send to an AI agent, it **re-reads the ENTIRE conversation**. A 100K token chat costs 100K input tokens **per message**. After 50 messages without compression, you've paid for 5M+ tokens of re-reading.

Most people don't know this. They chat all day in one session, topics pile up, and their bill explodes. **One user spent 4 months of budget in 1 month** before realizing the problem.

## The Solution

Deflate is an intelligent context compression skill that:

- 🧠 **Tracks topics** and detects when conversations are done
- 💰 **Recommends `/new`** (free) over `/compact` (paid) when possible
- 📋 **Compresses by topic** using Cornell-MapReduce methodology
- 🔒 **Never loses critical data** — IDs, dates, amounts are lossless
- 📊 **Measures compression quality** — stops when it's no longer effective
- 💡 **Estimates session cost** so you know what you're spending

## How It Works

### Cornell-MapReduce Hybrid Compression

Instead of dumb summarization that loses information:

1. **MAP** — Separate conversation into distinct topics
2. **FILTER** — Remove noise (greetings, failed attempts, repeated info)
3. **DISTILL** — Create atomic Cornell notes per topic (keyword + summary + data)
4. **PRESERVE** — IDs, dates, amounts survive compression unchanged
5. **COMBINE** — Merge notes with most important first (prevents "lost in the middle")

### Smart /new Detection

```
All topics done? → "Hey, we finished everything. Start fresh?"
Topic still active? → Compress and keep going
Compression ineffective (<20% reduction)? → Flush memory + /new
```

## Installation

### Option 1: ClawHub (Recommended)
```
openclaw skill install deflate
```

### Option 2: Manual
Copy the `SKILL.md` file to your agent's skills directory:
```
~/.openclaw/workspace/skills/deflate/SKILL.md
```

### Recommended Config

Add to your `openclaw.json` under `agents.defaults.compaction`:

```json
{
  "compaction": {
    "mode": "default",
    "reserveTokens": 920000,
    "reserveTokensFloor": 920000,
    "keepRecentTokens": 20000,
    "memoryFlush": {
      "enabled": true,
      "softThresholdTokens": 4000
    },
    "identifierPolicy": "strict"
  }
}
```

Adjust `reserveTokens` based on your model:

| Model Window | reserveTokens | Compress trigger |
|---|---|---|
| 128K (GPT-4) | 80,000 | ~48K |
| 200K (Claude) | 130,000 | ~70K |
| 1M (Gemini Flash) | 920,000 | ~80K |
| 2M (Gemini Pro) | 1,800,000 | ~200K |

## What Makes Deflate Different

| Feature | OpenClaw Default | Deflate |
|---|---|---|
| Compression trigger | Fixed token limit | Zone-based (🟢🟡🔴) |
| Compression method | Generic summary | Cornell-MapReduce per topic |
| Data preservation | `identifierPolicy: strict` | Lossless layer (IDs, dates, amounts) |
| Topic awareness | None | Tracks active/completed topics |
| /new recommendation | Never | Detects when topics are done |
| Quality control | None | Measures reduction %, stops when ineffective |
| Cost tracking | None | Estimates cost per session |
| Multi-topic handling | Treats all as one blob | Compresses each topic independently |

## Research Behind Deflate

This skill was built by combining proven methodologies:

- **Cornell Note-Taking** — Cue → Notes → Summary (academic research)
- **MapReduce** — Parallel chunk processing (distributed computing)
- **Recursive Summarization** — Iterative condensation (NLP research)
- **Medical Shorthand** — Maximum info in minimum space
- **Knowledge Distillation** — Teacher-student model compression (ML research)
- **Lossless Compression** — Huffman/RLE for critical data preservation

## Contributing

Found a bug? Have an idea? Open an issue or PR.

This skill was born from real pain — $2,400 in unexpected API costs in one month.
If it saves you money, share it with someone who needs it.

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.

---

Created by [@thevibestack](https://github.com/thevibestack)
