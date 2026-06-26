---
name: cross-post
description: "Cross-post content to Twitter/X, Reddit, and LinkedIn from one prompt. Use when user wants to publish the same content to multiple social platforms, schedule social posts, or post to Twitter/X + Reddit + LinkedIn at once. Supports thread posting on Twitter, custom titles/subreddits on Reddit, and professional formatting for LinkedIn. Use when user says post this, publish to social, cross-post, share on twitter/reddit/linkedin, or post to all my platforms."
---

# Cross-Post

Post content to Twitter/X, Reddit, and LinkedIn via official APIs.

## Setup

First time use:

```bash
python3 scripts/cross_post.py init-config
```

Config stored at `~/.config/cross-post/config.json`.

## Usage

```bash
# Post to all platforms
python3 scripts/cross_post.py post "Your content here"

# Post to specific platform
python3 scripts/cross_post.py post "Content" -p twitter

# Post as Twitter thread
python3 scripts/cross_post.py post "Long content..." -p twitter --thread

# Post to Reddit with title
python3 scripts/cross_post.py post "Body text" -p reddit -t "Title" -s python

# Read from file
python3 scripts/cross_post.py post -f draft.txt

# Preview formatting
python3 scripts/cross_post.py preview "Content" -p twitter
python3 scripts/cross_post.py preview "Content" -p reddit
python3 scripts/cross_post.py preview "Content" -p linkedin
```

## Platform Requirements

### Twitter/X

- Bearer Token (API v2)
- User ID
- Setup: developer.twitter.com

### Reddit

- Client ID, Client Secret, Username
- Password via REDDIT_PASSWORD env var
- Setup: reddit.com/prefs/apps

### LinkedIn

- Access Token
- Person URN
- Setup: developers.linkedin.com

## Tips

- Use `--thread` for long Twitter content (auto-splits at 280 chars)
- Use `--file` to post from files
- Use `preview` before posting to check formatting
- Each platform has different length limits:
  - Twitter: 280 chars per tweet
  - Reddit: 100 char title, unlimited body
  - LinkedIn: 3000 chars

## Security

Config file is chmod 600. Never commit config.json.
