# Bangumi Tracker - Command Reference

## Commands

### Authentication

```bash
# Configure OAuth credentials
python bangumi_tracker.py config --client-id <id> --client-secret <secret>

# Run OAuth authorization flow
python bangumi_tracker.py auth

# Check current login status
python bangumi_tracker.py status

# Logout (remove saved token)
python bangumi_tracker.py logout
```

### Collections

```bash
# List my collections
python bangumi_tracker.py collections [--type anime|book|game|music|real] [--status wish|doing|collect|on_hold|dropped]

# Add/update collection status
python bangumi_tracker.py collect <subject_id> <status>
# status: wish, doing, collect, on_hold, dropped

# Remove from collection
python bangumi_tracker.py uncollect <subject_id>
```

### Progress Tracking

```bash
# Get watch progress for a subject
python bangumi_tracker.py progress <subject_id>
```

### User Info

```bash
# Get current user info
python bangumi_tracker.py me
```

## Parameters

| Flag | Values | Default |
|------|--------|---------|
| `--type` | anime, book, game, music, real | anime |
| `--status` | wish, doing, collect, on_hold, dropped | all |

## Status Values

| Status | Type Value | Description |
|--------|------------|-------------|
| wish | 1 | 想看 |
| doing | 2 | 在看 |
| collect | 3 | 已看 |
| on_hold | 4 | 搁置 |
| dropped | 5 | 抛弃 |

## Subject Types

| Type | Type Value | Description |
|------|------------|-------------|
| book | 1 | 书籍 |
| anime | 2 | 动画 |
| music | 3 | 音乐 |
| game | 4 | 游戏 |
| real | 6 | 真人 |

## API Endpoints

This implementation uses the official [Bangumi API v0](https://github.com/bangumi/api):

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get user info | GET | `/v0/me` |
| Get collections | GET | `/v0/users/{username}/collections` |
| Get collection progress | GET | `/v0/users/{username}/collections/{subject_id}` |
| Add collection | POST | `/v0/users/-/collections/{subject_id}` |
| Update collection | PATCH | `/v0/users/-/collections/{subject_id}` |
| Remove collection | PATCH | `/v0/users/-/collections/{subject_id}` (type=0) |

## Data Storage

### Windows
- Client ID: `~/.bangumi/config.json`
- Client Secret: Windows Credential Manager (`BangumiTracker:client_secret`)
- Access Token: Windows Credential Manager (`BangumiTracker:access_token`)
- Refresh Token: Windows Credential Manager (`BangumiTracker:refresh_token`)
- Expires At: `~/.bangumi/token.json`

### Other Platforms
- `~/.bangumi/config.json` - OAuth app credentials
- `~/.bangumi/token.json` - Access/refresh tokens

## Troubleshooting

### "Callback server failed" or "No authorization code received"
- Make sure `http://localhost:17321/callback` is accessible
- Check that your OAuth app's Callback URL matches exactly

### "Token expired" errors
- Run `python bangumi_tracker.py auth` to re-authorize

### Check credential storage (Windows)
1. Open Windows Credential Manager (Control Panel → Credential Manager)
2. Look for entries starting with `BangumiTracker:`