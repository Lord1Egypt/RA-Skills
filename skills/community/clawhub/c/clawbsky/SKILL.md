---
name: clawbsky
version: 2.0.4
description: AI-powered Bluesky CLI with multi-user auth, smart content generation, post scheduling, analytics, RSS automation, and growth tools.
homepage: https://github.com/jyothish12345/Clawbsky
metadata:
  openclaw:
    requires:
      env:
        - BLUESKY_HANDLE
        - BLUESKY_APP_PASSWORD
      bins:
        - ffmpeg
        - ffprobe
    primaryEnv: BLUESKY_APP_PASSWORD
---

# 🦞 clawbsky v2.0.4

**The ultimate AI-powered Bluesky CLI** for power users, creators, and automation enthusiasts.

## ✨ What's New in v2.0.x

- 🤖 **AI Content Studio** — Generate posts, threads, alt-text, and smart replies powered by OpenAI, Anthropic, or local Ollama
- 👤 **Multi-User Sessions** — Login with multiple Bluesky accounts and switch between them instantly
- 📅 **Post Scheduler** — Schedule posts for later with a persistent SQLite-backed queue and a background daemon
- 📊 **Analytics Dashboard** — Track engagement stats, top posts, follower growth, and optimal posting times
- 📰 **RSS Feed Automation** — Subscribe to RSS feeds and auto-curate content for posting
- ✍️ **Content Enhancement** — Auto-generate alt-text, quote cards, and repurpose content across formats

## 🚀 Setup

1. **Get an App Password**: Go to [Bluesky Settings](https://bsky.app/settings/app-passwords) and create a new App Password. **NEVER** use your main account password.
2. **Install**:
   ```bash
   npm install
   ```
3. **Login**:
   ```bash
   clawbsky login
   ```

### 🤖 AI Setup (Optional)

For AI features, configure your LLM provider:

```bash
# OpenAI (default)
export LLM_API_KEY="sk-..."
export LLM_MODEL="gpt-4o-mini"

# Anthropic
export LLM_PROVIDER="anthropic"
export LLM_API_KEY="sk-ant-..."

# Ollama (local, free)
export LLM_PROVIDER="openai-compatible"
export LLM_BASE_URL="http://localhost:11434/v1"
export LLM_MODEL="llama3"
```

**Note**: When used as an OpenClaw skill, AI is provided by OpenClaw's main LLM — no additional config needed!

## 🛠 Commands

### 👤 Multi-User Authentication
```bash
clawbsky login                       # Login (saves session for reuse)
clawbsky whoami                      # Show active account + other profiles
clawbsky auth list                   # List all logged-in profiles
clawbsky auth switch <handle>        # Switch active profile
clawbsky auth logout [handle]        # Logout a specific or active profile

# Run ANY command as a specific user with -u
clawbsky whoami -u other.bsky.social
clawbsky post text "Hello!" -u second-account.bsky.social
```

### 🤖 AI Content Generation
```bash
clawbsky generate "post about AI trends"                  # Generate a post
clawbsky generate "5 tips for productivity" --tone=professional
clawbsky generate "topic" --thread --posts=5              # Generate a thread
clawbsky generate --improve "Check out my project!"       # Improve text
clawbsky reply-ai at://post-uri --count=3                 # AI reply suggestions
clawbsky analyze @username                                # AI profile analysis
clawbsky analyze at://post-uri --post                     # AI post analysis
```

### 📅 Post Scheduling
```bash
clawbsky schedule "Post text" --at 2026-07-01T10:00:00Z   # Schedule at time
clawbsky schedule "Post text" --in 2h                     # Schedule in 2 hours
clawbsky scheduled                                        # List queued posts
clawbsky scheduler                                        # Start scheduler daemon
```

### 📊 Analytics & Insights
```bash
clawbsky stats --days 7              # Engagement statistics
clawbsky top --limit 10 --sort likes # Top performing posts
clawbsky growth --days 30            # Follower growth tracking
clawbsky best-times                  # AI-suggested best posting times
```

### ✍️ Content Enhancement
```bash
clawbsky alt-text "image description" # Generate accessible ALT text
clawbsky quote "quote" --author Name  # Create a quote card
clawbsky repurpose "content" -f thread # Repurpose to thread/blog/tweet/linkedin
```

### 📰 RSS Feed Automation
```bash
clawbsky rss add --name "TechCrunch" --url https://feed.url --schedule hourly
clawbsky rss list                    # List subscribed feeds
clawbsky rss process                 # Process and post curated items
```

### 🚀 Growth & Maintenance
```bash
clawbsky unfollow-non-mutuals -n 50  # Unfollow top 50 non-mutuals
clawbsky follow-all "Query" -n 20    # Auto-follow users matching a topic
clawbsky cleanup --days 90           # Find inactive followers
```

### 📝 Posting & Threads
```bash
clawbsky post text "Text"            # Create a post
clawbsky post reply "Text" <uri>     # Reply to a post
clawbsky thread "Part 1" "Part 2"    # Create a multi-post thread
clawbsky quote <uri> "My thoughts"   # Quote a post
```

### 📖 Reading & Discovery
```bash
clawbsky read home                   # View your timeline
clawbsky read user <handle>          # Inspect a profile
clawbsky read post <uri>             # Read a single post
clawbsky read thread <uri>           # Read a full thread
clawbsky read mentions               # Check recent mentions
```

### 🗂 List Management
```bash
clawbsky list create --name "Tech"   # Create a curated list
clawbsky list add <handle>           # Add user to list
clawbsky list view                   # View your lists
```

## 💡 Advanced Usage

### Global Options
- `-u, --user <handle>`: Execute command under a specific logged-in profile
- `--json`: Get raw data for piping to other tools
- `--plain`: Disable emojis and formatting for cleaner logs
- `-n <count>`: Limit results (default: 10)
- `--dry-run`: Preview actions without executing
- `--post`: Immediately post AI-generated content

### Environment Variables
```bash
BSKY_IDENTIFIER=your-handle.bsky.social
BSKY_PASSWORD=your-app-password
# (See "AI Setup" section above for LLM environment variables)
```

## 🛡️ Safety & Ethics

1. **Be Human**: Don't use follow tools for mass following — considered spam
2. **Respect Limits**: Use unfollow-non-mutuals for periodic maintenance only
3. **App Passwords Only**: Never use your main password
4. **Rate Limiting**: Built-in delays prevent API limits

*Responsibility for account actions lies solely with the user.*

## 🔗 Links

- GitHub: https://github.com/jyothish12345/Clawbsky
- ClawHub: https://clawhub.ai/jyothish12345/clawbsky
- Web Dashboard: See [clawbskyweb](https://github.com/jyothish12345/clawbskyweb) for the Cyberpunk visual dashboard companion

---
*Built for the AT Protocol community with ❤️*