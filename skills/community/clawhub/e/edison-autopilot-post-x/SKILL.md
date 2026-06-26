# Edison Autopilot Post X

AI-powered auto-tweeting system. Generates and posts 5 tweets per day to X using GPT-5.1, with Telegram notifications and built-in safeguards.

Built entirely through **vibe coding** with Claude Code — zero lines of code written by hand.

## What It Does

- Generates 5 tweets/day using GPT-5.1, matching your persona and voice
- Posts automatically to X at scheduled times via cron
- Sends Telegram notifications for every posted tweet
- Checks last 10 tweets to avoid repetition
- 3-layer character limit protection (target 220 → retry at 280 → hard reject)
- Configurable banned phrases list to kill GPT filler
- Explicit rules to prevent AI from fabricating data/statistics
- Style variety — mixes formats (hot takes, questions, one-liners, stories)

## Setup

### 1. Install dependencies

```bash
pip install tweepy requests
```

### 2. Set environment variables

```bash
export OPENAI_API_KEY="sk-..."
export X_CONSUMER_KEY="..."
export X_CONSUMER_SECRET="..."
export X_ACCESS_TOKEN="..."
export X_ACCESS_TOKEN_SECRET="..."

# Optional: Telegram notifications
export TWEET_BOT_TOKEN="..."
export TWEET_BOT_CHAT_ID="..."
```

### 3. Customize your persona

Edit `auto_tweet.py` — update the `PERSONA`, `TOPICS`, and `BANNED_PHRASES` sections to match your voice, topics, and style.

### 4. Run

```bash
python auto_tweet.py --dry-run   # preview without posting
python auto_tweet.py              # post for real
```

### 5. Schedule with cron (5x daily)

```bash
crontab -e
# Add: 0 8,11,14,17,21 * * * cd /path/to/repo && python auto_tweet.py
```

## API Keys Required

| Service | Cost | Where |
|---------|------|-------|
| X API (Basic) | $25/month | developer.x.com |
| OpenAI API | ~$0.50/day | platform.openai.com |
| Telegram Bot | Free | @BotFather on Telegram |

## Prompt Engineering Tips

1. **Study real people** — encode tweet styles you admire into the persona
2. **Ban the filler** — maintain a growing list of GPT's favorite empty phrases
3. **Never let AI make up numbers** — explicit "NEVER FABRICATE DATA" rule
4. **Force variety** — require different formats, tones, and structures
5. **Shorter is better** — target 140-220 chars, not 280
