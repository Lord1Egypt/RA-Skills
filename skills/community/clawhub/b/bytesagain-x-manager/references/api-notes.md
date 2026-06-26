# API Notes — X API v2

## Auth
- OAuth 1.0a (user context) — required for posting, liking, following
- App must have Read + Write permissions
- Access Token is account-specific (tied to @bytesagain)

## Rate Limits (Pay-per-use tier)
- POST /tweets: charged per call (~$0.000005/tweet)
- GET search/recent: 10 results per call, recent 7 days only
- POST /likes: standard limits apply

## Known Constraints
- Search only covers last 7 days
- `from:user` filter available in recent search
- No streaming API on current plan
- DM requires separate OAuth scope not currently enabled

## Cost Estimate
- 3 tweets/day × 30 days = ~$0.00045/month
- 40 likes/day × 30 days = negligible
- xAI draft generation: ~$0.01–0.05/day (grok-4)
