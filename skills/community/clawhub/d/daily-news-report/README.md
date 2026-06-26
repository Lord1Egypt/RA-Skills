# Daily News Brief

OpenClaw skill for daily news collection and delivery.

## Features
- **Multiple News Sources**: Support Cailian Press, IT之家, 36Kr, and more
- **Intelligent Deduplication**: URL-based, title-based, and multi-source deduplication
- **Smart Classification**: Policy, public companies, and private companies/industry
- **One-sentence Rewriting**: Convert news to concise summaries with key data
- **Intelligent Ranking**: Sort by category priority, topic relevance, and data signals
- **Telegram Delivery**: Push reports to Telegram in Markdown format
- **Scheduled Execution**: Run at configurable times (08:00, 17:30, 22:30)
- **Two Modes**: Full mode and focused mode for specific topics

## Installation
1. Download this skill to OpenClaw's skills directory
2. Configure Telegram settings
3. Register the skill with `daily-news-brief register`

## Configuration
Set your Telegram credentials:
```bash
# Set your chat ID
set config.telegram_chat_id "YOUR_CHAT_ID"

# Set your bot token
set config.telegram_bot_token "YOUR_BOT_TOKEN"
```

## Usage
```bash
# Execute once
daily-news-brief run

# Test mode (no delivery)
daily-news-brief test

# Start scheduler
daily-news-brief start

# View configuration
daily-news-brief config
```

## Configuration Options
- `mode`: "all" or "focused" mode
- `focus_topics`: Topics for focused mode (robot, real_estate, ai)
- `sources`: News sources configuration
- `schedule`: Execution times
- `max_items`: Maximum items per report
- `include_links`: Include links in output
- `timezone`: Timezone for scheduling
- `telegram_chat_id`: Telegram Chat ID
- `telegram_bot_token`: Telegram Bot Token

## Troubleshooting
1. If Telegram delivery fails, check your Chat ID and Bot Token
2. Use test mode to verify functionality
3. Check logs for error messages
4. Ensure you have proper permissions for internet access

## License
MIT