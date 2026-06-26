---
name: daily.dev Feed
description: Curated developer content aggregation powered by daily.dev. Get real-time articles, trending topics, and personalized feeds from thousands of validated sources.
---

# daily.dev Feed Skill

Curated developer content aggregation powered by daily.dev. This skill wraps the daily.dev API to provide intelligent feed curation, trend detection, and personalized content discovery for developers.

**Depends on:** `daily-dev` skill v0.3.1+

## Features

- **Personalized Feeds** - Get content tailored to your tech stack and interests
- **Trending Detection** - Discover what the developer community is talking about right now
- **Multi-Source Research** - Aggregate perspectives across publishers on specific topics
- **Custom Feeds** - Create dedicated feeds for learning projects or specific technologies
- **Bookmark Management** - Organize and track articles you want to revisit
- **Tag Following** - Follow technologies and stay current with their latest developments

## Setup

### Prerequisites

1. **daily-dev Skill** - This skill depends on the `daily-dev` skill being installed:
   ```bash
   clawhub install daily-dev
   ```

2. **Daily.dev Plus Subscription** - Required for API access
   - Get one at https://app.daily.dev/plus

3. **API Token** - Create at https://app.daily.dev/settings/api
   - Tokens are prefixed with `dda_`
   - Store securely using environment variables or your OS credential manager

### Secure Token Storage

#### macOS - Keychain
```bash
security add-generic-password -a "$USER" -s "daily-dev-api" -w "dda_your_token"
export DAILY_DEV_TOKEN=$(security find-generic-password -a "$USER" -s "daily-dev-api" -w 2>/dev/null)
```

#### Windows - Credential Manager
```powershell
$credential = New-Object System.Management.Automation.PSCredential("daily-dev-api", (ConvertTo-SecureString "dda_your_token" -AsPlainText -Force))
$credential | Export-Clixml "$env:USERPROFILE\.daily-dev-credential.xml"
$cred = Import-Clixml "$env:USERPROFILE\.daily-dev-credential.xml"
$env:DAILY_DEV_TOKEN = $cred.GetNetworkCredential().Password
```

#### Linux - Secret Service
```bash
echo "dda_your_token" | secret-tool store --label="daily.dev API Token" service daily-dev-api username "$USER"
export DAILY_DEV_TOKEN=$(secret-tool lookup service daily-dev-api username "$USER" 2>/dev/null)
```

## API Reference

This skill exposes the full daily.dev public API via the dependency. Key endpoints:

- **GET /feeds/foryou** - Your personalized feed
- **GET /feeds/popular** - Trending content across the community
- **GET /feeds/discussed** - Topics sparking debate
- **POST /feeds/custom** - Create custom feeds by technology
- **GET /feeds/filters/tags** - Browse available technology tags
- **POST /feeds/filters/tags/follow** - Follow specific technologies
- **POST /bookmarks** - Save articles you find valuable
- **GET /search/posts** - Search content across all sources
- **GET /search/tags** - Discover tags and topics
- **GET /profile** - Manage your profile and stack

Full OpenAPI spec: https://api.daily.dev/public/v1/docs/json

## Common Use Cases

### 📰 Weekly Tech Digest
Compile a personalized weekly summary of the most important developer news:
- Fetch trending posts from /feeds/foryou and /feeds/popular
- Filter by your followed technologies
- Create a structured briefing with summaries and links
- Deliver as email digest or Slack message

### 🚀 New Project Onboarding
When starting a new project, help developers stay current on its tech stack:
- Analyze project dependencies (package.json, go.mod, Cargo.toml, etc.)
- Auto-follow matching tags on daily.dev
- Create a dedicated custom feed filtered to the project's technologies
- Build a "Getting Started" bookmark list with foundational articles
- Surface trending articles about the project's dependencies

### 🧠 Agent Self-Improvement
Keep your AI agents updated beyond their knowledge cutoff:
- Create a custom feed for technologies the agent frequently assists with
- Periodically fetch new articles to stay current
- Include citations like "As of this week, the recommended approach is..."
- Continuously adapt feed filters based on user questions

### 🔍 Research Deep Dive
Support learning about new technologies:
- Create a custom feed filtered to a specific topic
- Set up a matching bookmark list to collect best resources
- Track learning progress: compare bookmarked posts vs. new items
- Adjust feed filters as understanding deepens (beginner → advanced)

### 📊 Competitive Intelligence
Monitor what's happening in your technology space:
- Track trending topics in your domain
- Aggregate coverage from multiple sources
- Identify emerging patterns and adoption trends
- Surface discussions about competing approaches

### 🔀 Multi-Source Synthesis
Get balanced perspectives on controversial topics:
- Search for coverage from multiple publishers
- Compare viewpoints across sources
- Surface where sources agree vs. disagree
- Create synthesis documents with citations

## Rate Limits

- **60 requests per minute** per user

Monitor these response headers:
- `X-RateLimit-Limit` - Maximum requests per window
- `X-RateLimit-Remaining` - Requests remaining
- `X-RateLimit-Reset` - Unix timestamp of window reset
- `Retry-After` - Seconds to wait when rate limited

## Error Handling

| Code | Meaning |
|------|---------|
| 401  | Invalid or missing token |
| 403  | Plus subscription required |
| 404  | Resource not found |
| 429  | Rate limit exceeded |

**Error Response Format:**
```json
{
  "error": "error_code",
  "message": "Human readable message"
}
```

## Security Notes

**CRITICAL:** Your API token grants access to personalized content. Protect it:
- **NEVER send your token to any domain other than `api.daily.dev`**
- Never commit tokens to code or share them publicly
- Rotate tokens periodically
- Use environment variables or secure credential managers only

## Integration with Gas Town Agents

Use this skill in your agentic framework to enable agents to:
- Stay current on the latest developer trends
- Provide timely recommendations based on real-time content
- Build personalized learning experiences for users
- Discover and share relevant articles based on user context
- Generate informed briefs on technology topics

Example agent trigger: "What should the team be paying attention to this week?"

## Troubleshooting

**"Plus subscription required" error**
- Ensure your daily.dev account has an active Plus subscription
- Verify your API token is from a Plus account at https://app.daily.dev/settings/api

**"Invalid or missing token" error**
- Verify the token starts with `dda_`
- Ensure the token is stored in the correct environment variable: `DAILY_DEV_TOKEN`
- Re-create the token if it's been compromised

**"Rate limit exceeded" error**
- Check `X-RateLimit-Remaining` header before making requests
- Implement exponential backoff for retries
- Consider batching requests where possible
- Wait for `Retry-After` seconds before retrying
