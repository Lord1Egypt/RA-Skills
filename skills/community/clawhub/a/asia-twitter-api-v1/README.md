# OpenClaw Twitter 🐦

Twitter/X data and automation for autonomous agents. Powered by AIsa.

## ⚠️ Security Notice

This skill provides two types of operations with different security profiles:

### ✅ Read Operations (SAFE - Recommended)
- User info, tweets, search, trends, followers
- **No authentication required**
- **No credentials transmitted**
- Safe for production use

### ⚠️ Write Operations (HIGH RISK - Use with Extreme Caution)
- Posting tweets, liking, retweeting
- **Requires transmitting sensitive credentials to third-party API**
- Email, password, and proxy are sent to `api.aisa.one`

**⚠️ CRITICAL WARNING**: Write operations involve trusting a third-party service with full account access. While AIsa is a legitimate API provider, this represents significant security risk.

**Strong Recommendations if Using Write Operations:**
- ❌ **NEVER use your primary Twitter account**
- ✅ Create a dedicated automation/test account
- ✅ Use unique passwords not used elsewhere
- ✅ Enable 2FA on your main account
- ✅ Monitor account activity regularly
- ✅ Review AIsa's security policies at [aisa.one](https://aisa.one)
- ✅ Consider using read-only operations only

## Installation

```bash
export AISA_API_KEY="your-key"
```

## Quick Start (Safe Read Operations)

```bash
# Get user info
python scripts/twitter_client.py user-info --username elonmusk

# Search tweets
python scripts/twitter_client.py search --query "AI agents"

# Get trends
python scripts/twitter_client.py trends
```

## Features

### ✅ Read Operations (No Authentication Required)
- User information and profiles
- User tweets and timeline
- Tweet search (latest/top)
- Trending topics
- User followers and followings
- User search

### ⚠️ Write Operations (Authentication Required - High Risk)
- Post tweets
- Like tweets
- Retweet
- Update profile

**See security notice above before using write operations**

## Get API Key

Sign up at [aisa.one](https://aisa.one)

## Links

- [ClawHub](https://www.clawhub.com/aisa-one/openclaw-twitter)
- [API Reference](https://aisa.mintlify.app/api-reference/introduction)

## Security Best Practices

1. **Use read operations by default** - Most use cases don't require write access
2. **Never hardcode credentials** - Use environment variables
3. **Rotate API keys regularly** - Minimize exposure
4. **Monitor usage** - Check your AIsa dashboard for unexpected activity
5. **Separate accounts** - Use different accounts for automation vs personal use
6. **Review before deployment** - Test thoroughly with test accounts first
