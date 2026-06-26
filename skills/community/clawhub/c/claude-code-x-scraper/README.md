# X (Twitter) Data Scraper

Extract and analyze X/Twitter data programmatically within Claude Code.

## Features

- **User Timeline Fetch** - Get recent tweets from any public X account
- **Keyword Search** - Search X for topics, hashtags, or mentions
- **Advanced Filtering** - Exclude replies, retweets, filter by language
- **Social Media Research** - Analyze trends, monitor brand mentions, track influencers

## Installation

```bash
clawhub install claude-code-x-scraper
```

## Quick Start

### Get User Tweets
```bash
python3 scripts/get_user_tweets.py elonmusk 20
```

### Search X
```bash
python3 scripts/search_tweets.py "machine learning" 30
```

## Requirements

- X API Bearer Token (get from https://developer.twitter.com/en/portal/dashboard)
- Python 3.8+

## Setup

1. Get your X API token from Twitter Developer Portal
2. Set environment variable:
   ```bash
   export X_BEARER_TOKEN="Bearer YOUR_TOKEN"
   ```
   Or create `~/.openclaw/credentials/x_api_tokens.env`:
   ```
   X_BEARER_TOKEN=Bearer YOUR_TOKEN_HERE
   ```

## Usage Examples

### Basic Usage
```bash
# Get 10 tweets from a user
python3 scripts/get_user_tweets.py elonmusk 10

# Search for a topic
python3 scripts/search_tweets.py "AI news" 20

# Exclude replies and retweets
python3 scripts/get_user_tweets.py elonmusk 20 --no-replies --no-retweets
```

### Advanced Search
```bash
# Complex search with operators
python3 scripts/search_tweets.py '(from:elonmusk OR from:sama) "AI" lang:en -is:retweet' 20
```

### Python Module
```python
from scripts.x_api_client import XAPIClient

client = XAPIClient()
user = client.get_user_by_username('elonmusk')
tweets = client.get_user_tweets(user['data']['id'], max_results=100)
```

## API Access Levels

| Feature | Level | How to Get |
|---------|-------|------------|
| User lookup | Essential | Default |
| User tweets | Essential | Default |
| Search recent | Elevated | Apply in portal |

## Troubleshooting

- **401 Unauthorized**: Check your Bearer token
- **403 Forbidden**: Search API requires Elevated access
- **429 Rate Limit**: Wait 15 minutes for reset

## License

MIT-0

## References

- [X API Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Search Operators](references/x_api_limits.md)
