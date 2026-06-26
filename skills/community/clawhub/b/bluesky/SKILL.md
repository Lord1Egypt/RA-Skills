---
name: bluesky
version: 1.6.3
description: "Use the Bluesky CLI for timeline, search, notifications, posts, replies, threads, images, likes, reposts, follows, blocks, and mutes."
homepage: https://bsky.app
metadata:
  openclaw:
    emoji: "🦋"
    requires:
      bins: ["python3"]
    tags: ["social", "bluesky", "at-protocol", "cli"]
---

# Bluesky CLI

Full-featured CLI for Bluesky/AT Protocol.

## Agent Instructions

First check auth:

```bash
bsky whoami
```

- If it shows a handle, read commands are ready.
- If it says "Not logged in", use the setup flow below.

Safety rules:

- Never ask the user to paste a Bluesky app password into chat, notes, logs, or command arguments.
- For login, ask the user to run `bsky login --handle THEIR_HANDLE.bsky.social` locally so the app password goes into the hidden prompt.
- For public posts/replies/quotes/threads, use `--dry-run` first unless the user already gave final text.
- For block, unblock, mute, unmute, follow, unfollow, delete, repost, and unrepost, verify the exact account or post target before running. Pass `--yes` only after the user has clearly confirmed the action or when opt-in mutation confirmations are enabled.

Common tasks:

- "Post to Bluesky" → `bsky post "text"`
- "Check my timeline" → `bsky timeline`
- "Like this post" → `bsky like <url>`
- "Follow someone" → verify target, then `bsky follow @alice.bsky.social --yes`

## Setup

If `bsky whoami` shows "Not logged in", guide the user through setup.

Getting an app password:

Tell the user:
> Go to bsky.app -> click your avatar -> Settings -> Privacy and Security -> App Passwords -> Add App Password. Name it "OpenClaw". Do not paste the password into chat; keep it for the hidden CLI prompt.

Have them run this locally:
```bash
bsky login --handle THEIR_HANDLE.bsky.social
```

Security: the app password is used once to get a session token, then discarded. The CLI stores only the session token at `~/.config/bsky/config.json` with owner-only permissions.

Legacy `--password` still works for backward compatibility, but it is intentionally hidden from help and warns if used.

## Quick Reference

- View timeline: `bsky timeline` or `bsky tl`
- Post: `bsky post "text"`
- Post with image: `bsky post "text" --image photo.jpg --alt "description"`
- Reply: `bsky reply <url> "text"`
- Quote-post: `bsky quote <url> "text"`
- View thread: `bsky thread <url>`
- Create thread: `bsky create-thread "Post 1" "Post 2" "Post 3"` or `bsky ct`
- Like: `bsky like <url>`
- Repost: verify target, then `bsky repost <url> --yes`
- Follow: verify target, then `bsky follow @alice.bsky.social --yes`
- Block: verify target, then `bsky block @alice.bsky.social --yes`
- Mute: verify target, then `bsky mute @alice.bsky.social --yes`
- Search: `bsky search "query"`
- Notifications: `bsky notifications` or `bsky n`
- Delete post: verify target, then `bsky delete <url> --yes`

## Commands

### Timeline
```bash
bsky timeline              # 10 posts
bsky timeline -n 20        # 20 posts
bsky timeline --json       # JSON output
```

### Posting
```bash
bsky post "Hello world!"                           # Basic post
bsky post "Check this!" --image pic.jpg --alt "A photo"  # With image
bsky post "Test" --dry-run                         # Preview only
```

### Reply & Quote
```bash
bsky reply <post-url> "Your reply"
bsky quote <post-url> "Your take on this"
```

### Thread View
```bash
bsky thread <post-url>           # View conversation
bsky thread <url> --depth 10     # More replies
bsky thread <url> --json         # JSON output
```

### Create Thread
```bash
bsky create-thread "First post" "Second post" "Third post"   # Create a thread
bsky ct "Post 1" "Post 2" "Post 3"                           # Short alias
bsky create-thread "Hello!" "More thoughts" --dry-run         # Preview only
bsky create-thread "Look!" "Nice" --image pic.jpg --alt "A photo"  # Image on first post
```

### Engagement
```bash
bsky like <post-url>             # ❤️ Like
bsky unlike <post-url>           # Remove like
bsky repost <post-url> --yes     # 🔁 Repost after verifying target
bsky unrepost <post-url> --yes   # Remove repost after verifying target
```

### Social Graph
```bash
bsky follow @someone.bsky.social --yes    # Follow user after verifying target
bsky unfollow @someone.bsky.social --yes  # Unfollow user after verifying target
bsky profile @someone.bsky.social         # View profile
bsky profile --json              # JSON output
```

### Moderation
```bash
bsky block @someone.bsky.social --yes     # 🚫 Block user after verifying target
bsky unblock @someone.bsky.social --yes   # Unblock after verifying target
bsky mute @someone.bsky.social --yes      # 🔇 Mute user after verifying target
bsky unmute @someone.bsky.social --yes    # Unmute after verifying target
```

### Search & Notifications
```bash
bsky search "query"              # Search posts
bsky search "topic" -n 20        # More results
bsky notifications               # Recent notifications
bsky n -n 30                     # More notifications
```

### Delete
```bash
bsky delete <post-url> --yes     # Delete your post after verifying target
bsky delete <post-id> --yes      # By ID, after verifying target
```

## JSON Output

Add `--json` to read commands for structured output:
```bash
bsky timeline --json
bsky search "topic" --json
bsky notifications --json
bsky profile @someone --json
bsky thread <url> --json
```

## Error Handling

- "Session expired": run `bsky login --handle your.handle` again.
- "Not logged in": run `bsky login --handle your.handle`.
- "Refusing to ... without confirmation": opt-in mutation confirmation is enabled; verify the target/account, then re-run with `--yes` if the user confirmed.
- "Post is X chars (max 300)": shorten text.
- "Image too large": use image under 1MB.

## Notes

- All `<url>` parameters accept either `https://bsky.app/...` URLs or `at://` URIs
- Leading `@` is optional; use the full handle, such as `alice.bsky.social`
- Image posts require `--alt` for accessibility (Bluesky requirement)
- Session tokens auto-refresh; password never stored
