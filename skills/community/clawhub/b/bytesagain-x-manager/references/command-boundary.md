# Command Boundary — BytesAgain X Manager

## In Scope

| Action | Method | Notes |
|--------|--------|-------|
| Post tweets | X API v2 POST /tweets | Validate before posting |
| Reply to tweets | X API v2 reply param | Human approval required for mentions |
| Like tweets | X API v2 POST /likes | Dedup via liked-ids file |
| Follow users | X API v2 POST /following | Manual trigger only |
| Search tweets | X API v2 search/recent | Used for monitoring + like targets |
| Generate drafts | xAI grok-4 | 1 call/day, saved to /tmp |
| Translate reports | xAI grok-3-mini | Appended to Telegram reports |

## Out of Scope

- Sending DMs (requires additional OAuth scope)
- Deleting tweets (requires explicit human command each time)
- Accessing private/protected accounts
- Posting images or videos (text-only currently)
- Reading full follower/following lists (API tier limitation)
- Accessing X analytics data (not in current API plan)

## Safety Rules

1. All tweet content passes `validate_tweet()` before posting
2. Mention replies always go through Telegram approval — never auto-reply
3. Like deduplication prevents repeat-liking the same tweet
4. Bot-detection avoidance: multiple sends staggered 30–90s randomly
5. Own tweets are never liked by the auto-like function
6. Low-engagement posts (0 likes + 0 RTs) are skipped in auto-like
