# 🦞 clawbsky v2.0.4

**AI-powered Bluesky CLI** for power users, creators, and automation enthusiasts.

[![ClawHub](https://img.shields.io/badge/ClawHub-clawbsky-blue)](https://clawhub.ai/jyothish12345/clawbsky)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

| Category | Highlights |
|---|---|
| 🤖 **AI Studio** | Generate posts, threads, alt-text, smart replies via OpenAI / Anthropic / Ollama |
| 👤 **Multi-User** | Login with multiple accounts, switch instantly with `auth switch`, or use `-u` flag |
| 📅 **Scheduler** | Queue posts for later with SQLite persistence and a background daemon |
| 📊 **Analytics** | Engagement stats, top posts, follower growth, and AI-suggested best times |
| 📰 **RSS Feeds** | Subscribe to feeds and auto-curate content for posting |
| ✍️ **Content Tools** | Auto alt-text, quote cards, content repurposing (thread/blog/tweet/linkedin) |
| 🚀 **Growth** | Unfollow non-mutuals, auto-follow by topic, inactive follower cleanup |
| 🎬 **Media** | Post images (up to 4) and videos with automatic metadata & aspect ratio detection |
| 🧵 **Threads** | Create long-form threads automatically from multiple text blocks |
| 🛡️ **Moderation** | Block, mute, and notification management with built-in rate limiting |

## 📦 Quick Start

```bash
# 1. Install
npm install

# 2. Login
npx tsx scripts/cli.ts login

# 3. Explore
npx tsx scripts/cli.ts --help
```

### AI Setup (Optional)

```bash
# OpenAI
export LLM_API_KEY="sk-..."

# Or Ollama (free, local)
export LLM_PROVIDER="openai-compatible"
export LLM_BASE_URL="http://localhost:11434/v1"
export LLM_MODEL="llama3"
```

## 🛠 Commands at a Glance

### Multi-User Auth
```bash
clawbsky login                         # Login and save session
clawbsky whoami                        # Show active + other profiles
clawbsky auth list                     # All logged-in accounts
clawbsky auth switch <handle>          # Switch active profile
clawbsky auth logout [handle]          # Logout specific or active
clawbsky post text "Hi" -u alt.bsky.social  # Post as another account
```

### AI Generation
```bash
clawbsky generate "AI trends post"     # Generate a post
clawbsky generate "topic" --thread     # Generate a thread
clawbsky reply-ai at://uri            # AI reply suggestions
clawbsky analyze @user                # AI profile analysis
```

### Scheduling & Analytics
```bash
clawbsky schedule "Post" --in 2h      # Schedule post in 2 hours
clawbsky scheduled                     # View queue
clawbsky stats --days 7                # Engagement stats
clawbsky top --limit 10               # Top performing posts
clawbsky best-times                    # Best time to post
```

### Content & RSS
```bash
clawbsky alt-text "description"        # Generate ALT text
clawbsky repurpose "content" -f blog   # Repurpose content
clawbsky rss add --name "Feed" --url https://... --schedule daily
```

### Growth & Posting
```bash
clawbsky post text "Hello world 🦞"   # Post
clawbsky thread "Part 1" "Part 2"     # Thread
clawbsky unfollow-non-mutuals -n 50   # Cleanup
clawbsky read home                     # Timeline
```

## ⚙️ Global Options

| Flag | Description |
|---|---|
| `-u, --user <handle>` | Execute as a specific logged-in profile |
| `--json` | Raw JSON output for piping |
| `--plain` | No emojis or formatting |
| `-n <count>` | Limit results |
| `--dry-run` | Preview without executing |

## 🛡️ Safety & Ethics

- **App Passwords Only** — Never use your main password
- **Rate Limiting** — Built-in 1s delay between operations
- **Confirmation Prompts** — Large batch operations require manual confirmation
- **Responsible Use** — Don't use growth tools for aggressive follow/unfollow churning

*Responsibility for account actions lies solely with the user.*

## 🔗 Ecosystem

- **ClawHub**: [clawhub.ai/jyothish12345/clawbsky](https://clawhub.ai/jyothish12345/clawbsky)
- **Web Dashboard**: See [clawbskyweb](https://github.com/jyothish12345/clawbskyweb) for the Cyberpunk visual dashboard companion
- **GitHub**: [github.com/jyothish12345/Clawbsky](https://github.com/jyothish12345/Clawbsky)

---
*Built for the AT Protocol community. 🦞*
