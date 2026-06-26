---
name: clip
description: Extract media (videos, photos, GIFs, audio) from social media URLs using yt-dlp. Supports 1,872+ platforms. WARNING: files over 50 MB require --confirm-upload for public cloud upload. Browser cookie access exposes authentication material. Only use with non-sensitive content.
---

# Clip

⚠️ **Security warnings before use:**
- Files over 50 MB **require `--confirm-upload`** to upload to public third-party hosts (tmpfiles.org, transfer.sh)
- Browser cookie access (`--cookies-from-browser`) exposes **active session tokens** for any platform you're logged into
- **Never** use with private, paid, confidential, copyrighted, or regulated content unless you explicitly intend external transmission

## How It Works

1. User shares a URL from any supported platform
2. Run the extraction script
3. Script downloads the media (or just analyzes it)
4. Returns the file path (under 50 MB) or a cloud link (over 50 MB)
5. Agent sends the media to the user

⚠️ **Before any extraction:** Confirm the content is not private, paid, or sensitive. Files over 50 MB are uploaded to public temp hosts — the script now shows a pre-upload warning and supports `--no-upload` to skip it entirely.

## Command

```bash
node /home/jarvis/.openclaw/workspace/skills/clip/extract.js <url> [options]
```

### Options

| Flag | Description |
|------|-------------|
| `--output-dir <dir>` | Save location (default: `/tmp/media-share`) |
| `--title` | Return title/description only, no download |
| `--info` | Return full metadata as JSON |
| `--test` | Validate URL without downloading |
| `--upload` | Force cloud upload even for small files |
| `--confirm-upload` | **Required for any public cloud upload** — explicit opt-in |
| `--cloud=<provider>` | Cloud provider: `tmpfiles` or `transfer` |
| `--no-direct-send` | Always return path, never auto-send |
| `--no-upload` | **Skip cloud upload entirely** — always return local path |
| `--list-sites` | Show supported platforms |
| `--list-types` | Show what media a URL contains |

### Examples

```bash
# Download media (fastest path)
node /home/jarvis/.openclaw/workspace/skills/clip/extract.js "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Get title only (no download, instant)
node /home/jarvis/.openclaw/workspace/skills/clip/extract.js "https://www.instagram.com/p/abc123/" --title

# Check what's in a URL before downloading
node /home/jarvis/.openclaw/workspace/skills/clip/extract.js "https://www.tiktok.com/@user/video/123" --list-types

# Show supported sites
node /home/jarvis/.openclaw/workspace/skills/clip/extract.js --list-sites
```

## Supported Platforms

**yt-dlp: 1,872 extractors** — covers essentially every major media platform on the internet.

### Quick reference (most common):
YouTube, TikTok, Instagram, X/Twitter, Facebook, Reddit, Twitch, Vimeo, Dailymotion, Rumble, Peertube, Bilibili, Niconico, SoundCloud, Bandcamp, Pinterest, Imgur, Tumblr, Flickr, Bluesky, Telegram, Kick, Odysee, CNN, BBC, Al Jazeera, TED, Khan Academy, Udemy, Crunchyroll, HiDive, and 1,800+ more.

## File Size Handling

- **Under 50 MB** → Returns local file path (agent sends via chat)
- **Over 50 MB** → Requires `--confirm-upload` to upload to temp cloud storage, returns download link
- **Over 50 MB without `--confirm-upload`** → Returns local path only, blocks upload with clear message
- **Over 50 MB + `--upload`** → Forces cloud upload even for smaller files (still requires `--confirm-upload`)

### Cloud Providers

⚠️ **Both providers are public and third-party.** Uploaded files are accessible to anyone with the link.

| Provider | Max Size | Notes |
|----------|----------|-------|
| `tmpfiles` | 50 MB | Simple, no signup, auto-delete |
| `transfer` | Unlimited | transfer.sh, 30-day retention |

**Pre-upload warning:** Files over 50 MB require `--confirm-upload` for any public cloud upload. Without it, the script returns the local path only and blocks the upload with a clear message. Use `--no-upload` to always save locally without prompts.

## Authentication

⚠️ **Browser cookie access exposes active session tokens for every platform you're logged into.**

Some platforms require cookies for full access:

| Platform | Needs cookies? |
|----------|---------------|
| Instagram | Sometimes (private content, full resolution) |
| X / Twitter | Sometimes (rate limits, some content) |
| Patreon | Yes (paid content) |
| OnlyFans | Yes |
| Fanvue / Fansly | Yes |
| Netflix / HBO / Disney+ | Via browser cookies |
| YouTube | Rarely (age-restricted content) |

**If cookies are needed:**
- Use `--cookies-from-browser chrome` as a **last resort** — it exposes ALL platform session tokens in that browser
- Warn the user that this could enable unauthorized account access if the machine is compromised
- Prefer manual cookie paste or API keys when available
- Never use `--cookies-from-browser` with paid/sensitive platforms unless the user explicitly consents to the risk
- Consider exporting cookies from only the specific browser/profile needed, not the default one

## How It Works (Under the Hood)

1. **Analyze**: `yt-dlp --dump-json` detects the platform and media type
2. **Download**: `yt-dlp -o <path>` grabs the highest quality version
3. **Route**: Under 50 MB → return path. Over 50 MB → upload to cloud → return link
4. **Fallback**: If download fails, returns title/description so the agent can inform the user

## Dependencies

- `yt-dlp` (installed) — 1,872 extractors
- `ffmpeg` (installed) — format conversion
- `curl` (installed) — cloud uploads

## Error Handling

When a URL returns no media, the script returns the title/description. The agent should:
- Inform the user what was found
- Suggest trying `--cookies-from-browser chrome` if the platform may require auth
- Note that geo-blocked content cannot be bypassed

## Notes

- Rate limits may apply on some platforms — add delays between calls
- Some platforms (Instagram, X) work better with cookies
- If a URL returns no media, return the title/description to the user instead
- The `generic` extractor handles many embedded video players not explicitly listed
