# ai-news-skill

AI industry news aggregation skill for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [OpenClaw](https://openclaw.ai). Never miss a major model release again.

## Why?

GLM-5 dropped and your morning briefing missed it? Same. This skill monitors 10 curated RSS feeds covering major AI labs and news aggregators so you catch:

- Model releases (GPT, Claude, Gemini, Grok, GLM, Llama, etc.)
- Research papers and benchmarks
- Industry moves (funding, acquisitions, hires)
- Product updates and API changes

## Quick Start

### 1. Install

```bash
# Claude Code
git clone https://github.com/tensakulabs/ai-news-skill.git ~/.claude/skills/ai-news

# OpenClaw
git clone https://github.com/tensakulabs/ai-news-skill.git ~/.openclaw/skills/ai-news
```

### 2. Use

In any Claude Code or OpenClaw session:
```
/ai-news
```

Or just ask: "What's new in AI?" / "Morning AI briefing"

### 3. Automate (Optional — OpenClaw)

Add an entry to `~/.openclaw/cron/jobs.json`:

```json
{
  "name": "morning-ai-briefing",
  "agentId": "main",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "0 7 * * *",
    "tz": "America/Los_Angeles"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run /ai-news --save and save to ~/.openclaw/ai-news/. Prioritize model releases and major announcements.",
    "model": "anthropic/claude-sonnet-4-20250514"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "YOUR_CHAT_ID"
  }
}
```

**`to` format:**
- Telegram DM: `"123456789"` (your numeric chat ID)
- Telegram group topic: `"-1001234567890:topic:149"` (group ID + topic ID)
- Discord channel: `"channel:1234567890123456789"`

For Claude Code, invoke `/ai-news` manually or via system cron.

## Feeds

### News Aggregators

| Source | Frequency | Description |
|--------|-----------|-------------|
| [TLDR AI](https://tldr.tech/ai) | Daily | Curated AI digest |
| [Hacker News](https://news.ycombinator.com) | Real-time | Tech community, viral AI posts |
| [The Decoder](https://the-decoder.com) | Daily | AI-focused news site |
| [Last Week in AI](https://lastweekin.ai) | Weekly | Comprehensive roundup |
| [Marktechpost](https://marktechpost.com) | Daily | Research and papers |

### Lab Blogs

| Lab | Feed | Covers |
|-----|------|--------|
| Anthropic | [News](https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml) | Company announcements |
| Anthropic | [Claude Blog](https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_claude.xml) | Product updates, guides |
| Anthropic | [Red Team](https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_red.xml) | Safety research |
| OpenAI | [Blog](https://openai.com/blog/rss.xml) | Announcements (direct) |
| OpenAI | [Research](https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_openai_research.xml) | GPT papers ⚠️ currently empty |
| xAI | [News](https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_xainews.xml) | Grok releases ⚠️ stale since Sept 2025 |
| Google | [Developers Blog](https://developers.googleblog.com/feeds/posts/default) | Gemini, ADK (direct) |
| Hugging Face | [Blog](https://huggingface.co/blog/feed.xml) | Model releases, research (direct) |
| Anthropic | [Claude Code Changelog](https://code.claude.com/docs/en/changelog/rss.xml) | CLI updates (direct) |

Feeds marked "direct" use official first-party RSS. Others via [Olshansk/rss-feeds](https://github.com/Olshansk/rss-feeds).

## Known Gaps

These major labs don't publish RSS feeds:

- **Zhipu AI** (GLM series) - China
- **DeepSeek** - China
- **Baidu** (ERNIE) - China
- **Alibaba** (Qwen) - China
- **Meta AI** - USA
- **Mistral AI** - France

The skill reminds you to check these manually.

## Customization

Edit `feeds.json` to add/remove feeds or change priorities.

Optional feeds you can enable:
- Anthropic Engineering (technical posts)
- Anthropic Research (papers, alignment)
- The Batch (Andrew Ng's newsletter)
- TechCrunch AI
- VentureBeat AI

## Contributing

PRs welcome! Especially:
- New RSS feed sources
- Better categorization logic
- Feeds for labs in the "Known Gaps" section

## License

MIT

---

Made by [Tensaku Labs](https://tensakulabs.com)
