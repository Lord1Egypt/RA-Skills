# X API v2 Reference

## API Access Levels

X API v2 has three access levels:

### Essential (Free)
- 500 tweets/month read limit
- 1 app only
- Basic search (not available)

### Elevated (Free, requires application)
- 2 million tweets/month read limit  
- 3 apps
- Recent search (7 days)
- Filtered stream

### Academic / Enterprise
- Higher rate limits
- Full archive search
- Advanced features

## Rate Limits

### User Lookup
- 900 requests per 15 minutes

### User Tweets Timeline
- 1500 requests per 15 minutes (app auth)
- 900 requests per 15 minutes (user auth)

### Recent Search
- 450 requests per 15 minutes (app auth)
- 180 requests per 15 minutes (user auth)

## Common Tweet Fields

| Field | Description |
|-------|-------------|
| `created_at` | ISO 8601 timestamp |
| `author_id` | User ID who posted |
| `public_metrics` | Impressions, likes, retweets, replies, quotes |
| `source` | Client used to post |
| `lang` | Language code |
| `entities` | Hashtags, mentions, urls, cashtags |
| `geo` | Location data (if available) |
| `referenced_tweets` | Retweets, replies, quotes |

## Search Query Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `from:` | From specific user | `from:elonmusk` |
| `to:` | Reply to user | `to:elonmusk` |
| `@` | Mentions user | `@elonmusk` |
| `#` | Hashtag | `#AI` |
| `""` | Exact phrase | `"machine learning"` |
| `()` | Grouping | `(AI OR ML)` |
| `-` | Exclude | `AI -crypto` |
| `is:retweet` | Retweets only | `is:retweet` |
| `is:reply` | Replies only | `is:reply` |
| `has:media` | Has media | `has:media` |
| `has:images` | Has images | `has:images` |
| `has:videos` | Has videos | `has:videos` |
| `lang:` | Language filter | `lang:en` |

## Error Codes

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Bad request |
| 401 | Unauthorized - check bearer token |
| 403 | Forbidden - check API access level |
| 404 | Not found |
| 429 | Rate limit exceeded |
| 500 | Server error |

## Troubleshooting

### "Unauthorized" Error
- Check bearer token is valid
- Ensure token has correct format (without 'Bearer ' prefix in code)

### "Forbidden" Error  
- Feature requires higher access level (e.g., search needs Elevated)
- Apply for Elevated access at https://developer.twitter.com/en/portal/dashboard

### Rate Limit Exceeded
- Implement exponential backoff
- Cache results when possible
- Use appropriate request limits
