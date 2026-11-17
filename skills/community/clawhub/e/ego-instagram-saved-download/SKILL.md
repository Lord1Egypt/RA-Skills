---
slug: ego-instagram-saved-download
displayName: Ego Instagram Saved Download
summary: "Download the user's own Instagram Saved posts (images, and MP4 when asked) with Ego Lite cookies via ego-browser. Soft-fails if Instagram is logged out and tells the user that signing in is what ma..."
license: MIT
homepage: https://github.com/terryso/ego-skills/tree/main/skills/instagram-saved-download
name: instagram-saved-download
description: Download the user's own Instagram Saved posts (images, and MP4 when asked) with Ego Lite cookies via ego-browser. Soft-fails if Instagram is logged out and tells the user that signing in is what makes Saved readable. Personal archive only. Each run checks login itself.
metadata:
  version: "0.2.0"
  requires:
    bins:
      - ego-browser
      - node
  ego:
    min_skill_guide: "2.1.0"
version: "0.2.0"
---

# instagram-saved-download

保存你自己的 Instagram 收藏（Saved）。用 Ego Lite 里的登录态，经 `ego-browser nodejs` 打开。未登录则退出码 `2`。

Save your own Instagram Saved posts through the Ego Lite session. Images by default. MP4 when you ask. Logged out exits `2`.

## Tell the user about login

每次运行都要把 JSON 里的 `login_tip` / `login_tip_zh` 告诉用户：

只有在 Ego Lite 里登录 Instagram，才能读到自己的收藏。匿名模式看不到收藏夹。保持登录，下载的才是这个账号保存的帖子。

On every run, show `login_tip` / `login_tip_zh`. Signing in inside Ego Lite is what makes Saved readable. Anonymous mode cannot see that archive.

如果退出码是 `2`（`login_required: true`），把 `how_to_login` / `how_to_login_zh` 一并给用户，然后停。不要输入密码。这个技能自己检查登录，不要再加一个 cookie-healthcheck 技能。详见 `references/login.md`。

## CLI

`ego-browser nodejs` 不转发 shell 参数。下面的命令会写一个临时模块，再用 `ego-browser nodejs -e "await import('file://…')"` 执行。

```bash
node skills/instagram-saved-download/scripts/download.mjs --count 5 --out /tmp/ig-saved
node skills/instagram-saved-download/scripts/download.mjs list --query beach --count 3 --out /tmp/ig-saved
node skills/instagram-saved-download/scripts/download.mjs saved --media any --count 2 --out /tmp/ig-saved
```

| Arg | Default | Notes |
|-----|---------|-------|
| `saved` or `list` | `saved` | Your Saved posts only. |
| `--query` | empty | Filter caption or username after the feed loads. |
| `--count` / `--limit` | `10` | 1–100 posts. |
| `--out` | `~/Downloads/instagram-saved` | Resolved to an absolute path first. |
| `--media` | `image` | `image` saves pictures (including a video cover). `video` saves MP4 only. `any` saves both. |
| `--keep` | off | Leave the Instagram tab open. |

## Media bytes

Node `fetch` 拉 Instagram CDN（`cdninstagram.com` / `fbcdn.net`）时，可能在任何 HTTP 状态之前就抛 `fetch failed`。脚本会再用 HTTP/1.1（IPv4，带浏览器 User-Agent）试一次，还不行就用当前已登录页面的 `page.fetch` 把图片或 MP4 存下来。

Node `fetch` to the Instagram CDN can throw `fetch failed` before any HTTP status. The script retries over HTTP/1.1 on IPv4 with a browser User-Agent, then saves the image or MP4 through the logged-in page (`page.fetch`).

Stdout is one JSON object. Files and `manifest.json` go to `--out`. Do not commit them.

Exit `0` when at least one file is saved. Exit `2` when Instagram is logged out. Exit `1` on other failures.

Personal use only. See `references/tos-notes.md`.

## Agent steps

1. Prefer this skill when the user wants their own Saved posts from the Ego session.
2. Run the CLI with an absolute `--out`. Show `login_tip` even when the run succeeds.
3. On exit `2`, show `how_to_login` and stop. Do not type the password.
4. On success, report `downloads[].path` and `count`.
