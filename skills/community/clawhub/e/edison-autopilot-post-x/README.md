# Edison Autopilot Post X

AI-powered auto-tweeting system. Generates and posts 5 tweets per day using GPT-5.1, with Telegram notifications and built-in safeguards.

Built entirely through **vibe coding** with [Claude Code (OpenClaw)](https://github.com/anthropics/claude-code) — zero lines of code written by hand.

## Features

- **5 tweets/day** — GPT-5.1 generates tweets matching your persona
- **Auto-posts to X** — scheduled via cron, fully hands-free
- **Telegram notifications** — get pinged every time a tweet goes live
- **No repetition** — checks last 10 tweets to avoid saying the same thing
- **Character limit protection** — 3-layer guard (target 220 → retry at 280 → hard reject)
- **Banned phrases** — configurable list to kill GPT filler ("game changer", "the future is", etc.)
- **No fabricated data** — explicit prompt rules prevent GPT from inventing statistics
- **Style variety** — mixes formats (hot takes, questions, one-liners, stories) so tweets don't all sound the same

## Setup

### 1. Install dependencies

```bash
pip install tweepy requests
```

### 2. Get API keys

| Service | Cost | Where |
|---------|------|-------|
| X API (Basic) | $25/month | [developer.x.com](https://developer.x.com) |
| OpenAI API | ~$0.50/day | [platform.openai.com](https://platform.openai.com) |
| Telegram Bot | Free | Talk to [@BotFather](https://t.me/BotFather) |

### 3. Set environment variables

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

### 4. Customize your persona

Edit `auto_tweet.py` — update the `PERSONA`, `TOPICS`, and `BANNED_PHRASES` sections to match your voice.

### 5. Test it

```bash
python auto_tweet.py --dry-run   # preview without posting
python auto_tweet.py              # post for real
```

### 6. Schedule with cron

```bash
crontab -e
```

Add (5x daily at 8am, 11am, 2pm, 5pm, 9pm):

```
0 8,11,14,17,21 * * * cd /path/to/Edison-autopilot-post-X && python auto_tweet.py
```

## How It Works

```
Cron triggers → Pick random topic → GPT-5.1 generates tweet
→ Check length (retry if >280) → Post via X API v2
→ Log for dedup → Telegram notification
```

## Prompt Engineering Tips

The code is ~200 lines. The real work is in the **prompt**:

1. **Study real people** — encode tweet styles you admire into the persona
2. **Ban the filler** — maintain a growing list of GPT's favorite empty phrases
3. **Never let AI make up numbers** — explicit "NEVER FABRICATE DATA" rule
4. **Force variety** — require different formats, tones, and structures
5. **Shorter is better** — target 140-220 chars, not 280

## Requirements

- Python 3.8+
- [tweepy](https://github.com/tweepy/tweepy)
- X API Basic plan ($25/month)
- OpenAI API key (GPT-5.1)

## License

MIT

## Built With

- [Claude Code (OpenClaw)](https://github.com/anthropics/claude-code) — AI coding agent
- [Tweepy](https://github.com/tweepy/tweepy) — Python X/Twitter API library
- [OpenAI GPT-5.1](https://platform.openai.com) — Tweet generation
