<div align="center">

<img src="assets/icon-512.png" width="112" height="112" alt="Free Douyin video and image downloader icon">

# Free Douyin Downloads for Videos and Images

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

## Free · no extra downloader account · no third-party API key

Give an Agent a Douyin link and it saves the video or image post locally. You do not need to register with a third-party downloader or request an API key. If Douyin shows a login wall, verification challenge, or restricted detail response, the script stops and preserves its task tab for you to handle manually.

[简体中文](README.md) | [English](README.en.md)

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-2563EB?style=flat-square)](https://agentskills.io/)
[![Easy WebBridge](https://img.shields.io/badge/runtime-Easy%20WebBridge-111827?style=flat-square)](https://github.com/xxjrq/easy-webbridge)
[![GitHub Stars](https://img.shields.io/github/stars/xxjrq/douyin-download-webbridge?style=flat-square)](https://github.com/xxjrq/douyin-download-webbridge/stargazers)
[![skills.sh](https://skills.sh/b/xxjrq/douyin-download-webbridge)](https://skills.sh/xxjrq/douyin-download-webbridge)
[![License](https://img.shields.io/badge/license-MIT--0-16A34A?style=flat-square)](LICENSE)

</div>

## Highlights

- **Free and open source:** no per-download charge.
- **No extra login:** no third-party downloader account; it keeps using your own browser.
- **No third-party key:** no TikHub, redfox, or similar content API token.
- **Videos and images:** selects the highest available video quality and saves multi-image posts in order.

## What it does

- Downloads Douyin videos by reading available bitrate variants from the work detail page.
- Chooses the highest resolution by default and prefers H.264 when resolutions match.
- Downloads Douyin image posts from the detail image list, with numbered files for multi-image posts.
- Accepts canonical work URLs, numeric IDs, and Douyin share short links that resolve from one safely checked HTTPS response. It reads `Location` to extract the work ID and never requests the redirect target.
- Keeps each run in its own browser task group and closes only that group afterward.
- Creates readable filenames from the work title and prints saved paths plus basic media information.
- Free to use and does not require TikHub, redfox, or another third-party API key.

“No extra login” means no third-party downloader account. “No key” means no token for a third-party content API. The local runtime still needs Easy WebBridge, Node.js, Python, and a Chromium browser. If Douyin shows a login wall, sign in to Douyin in that browser.

This is a downloader and organizer, not an editor or watermark-removal service. It saves content you are authorized to use and does not upload, publish, or operate your account.

## How it works with Easy WebBridge

```text
Claude Code / Codex / OpenCode / WorkBuddy
                    |
       douyin-download-webbridge Skill
              download + organize
                    |
          Easy WebBridge 127.0.0.1:17777
                    |
       browser extension + public Douyin work
```

This repository owns the Douyin download workflow. [Easy WebBridge](https://github.com/xxjrq/easy-webbridge) connects the real browser. They are independent repositories linked through the local HTTP Bridge, with no author-specific filesystem path. Install Easy WebBridge once and reuse it from other business Skills.

## Install

### 1. Install Easy WebBridge once

```bash
git clone https://github.com/xxjrq/easy-webbridge.git
cd easy-webbridge
npm install
node cli/easy-webbridge.mjs start
```

Load the Easy WebBridge `extension/` directory in a Chromium browser, then confirm that the Bridge sees it. Public works can usually be handled directly; sign in to Douyin only when Douyin shows a login wall.

### 2. Install this Skill

```bash
npx skills add xxjrq/douyin-download-webbridge
```

Universal manual location:

```bash
git clone https://github.com/xxjrq/douyin-download-webbridge.git ~/.agents/skills/douyin-download-webbridge
```

## Use it

After Easy WebBridge is connected, ask any compatible Agent:

```text
Use douyin-download-webbridge to download this Douyin work: https://www.douyin.com/video/123456789012
```

Or run the script directly:

```bash
python3 scripts/douyin_download.py "https://www.douyin.com/video/123456789012"
python3 scripts/douyin_download.py "https://www.douyin.com/video/1234567890" -o ~/Downloads/douyin
python3 scripts/douyin_download.py 7669474316672716066 --browser Creator
python3 scripts/douyin_download.py "<link>" --quality worst
```

Options:

| Option | Purpose |
| --- | --- |
| First argument | Canonical Douyin work URL, work ID, or a safely resolvable `v.douyin.com` short link |
| `-o, --out` | Output directory; defaults to `~/Downloads/DouyinDownloads` |
| `--browser` | Target browser display name or `browserId`; may be omitted only when one browser is online |
| `--quality best` | Default mode; choose the highest available quality |
| `--quality worst` | Choose the smallest variant for a quick preview |

## Requirements

- Python 3.9+, Node.js 20+, and `curl`.
- Easy WebBridge running at `127.0.0.1:17777` by default.
- At least one Chromium browser online; sign in to Douyin if the page shows a login wall.
- `ffmpeg` and `ffprobe` are discovered through `PATH`; Apple Silicon macOS also checks `/opt/homebrew/bin`. On Windows, add FFmpeg's `bin` directory to `PATH`. Downloads still work without ffprobe, but media inspection is skipped; `--audio-only` requires ffmpeg.

The script checks the Bridge and online browsers before opening the work. An explicit `--browser` must match that online display name or `browserId`; it never substitutes another browser. Without an explicit selection, it chooses a browser only when exactly one is online. If two or more are online, it lists their names and `browserId`s and asks you to choose, even when one is named `自媒体`.

## Output

- Videos are saved as `.mp4` files named from the work title.
- Image posts are saved as `_01.jpeg`, `_02.jpeg`, and so on, preferring original, JPEG, then WebP variants.
- The default output directory is `~/Downloads/DouyinDownloads`; use `-o` to change it.
- Douyin media URLs expire. If a download returns 403, run the command again to obtain a fresh URL.
- Media files are fetched only from public HTTPS URLs. The script checks DNS and pins connections to verified public IPs, rejecting local/private addresses, non-HTTPS URLs, and redirects. If system DNS returns a `198.18.0.0/15` fake IP or fails, only the media hostname (never its path or signed query) is sent to the fixed AliDNS HTTPS resolver; all returned addresses must be public. If an environment proxy is used, the HTTPS CONNECT target is still the verified IP and TLS checks the original hostname. Unverifiable addresses fail closed.
- A share short link triggers one HTTPS request pinned to verified public IPs. Only a direct `Location` to a supported Douyin work URL is accepted; the target is never requested. Multi-hop, non-work, and unverifiable redirects fail and ask for the canonical URL or ID.

## Boundaries

The Skill stops at login walls, verification challenges, and restricted detail responses, preserves the task tab, and asks you to handle the page manually. It does not retry through the barrier, switch accounts, or bypass CAPTCHA, access controls, or platform restrictions. Image posts are downloaded only from the work's detail image list; if that list cannot be confirmed, the download fails instead of using page-wide recommendation images. It does not upload, publish, comment, send messages, or collect post-publication metrics.

Only download content you created, have permission to use, or are otherwise legally allowed to save. Follow Douyin's terms, copyright rules, and privacy requirements.

## License

[MIT-0](LICENSE)

## EasyBR AI onboarding and task completion

Read the official [EasyBR AI operation guide](https://www.ebrower.com/helperdoc/ai-agent-workflow.html); use the [Easy WebBridge guide](https://www.ebrower.com/helperdoc/easy-webbridge.html) for connection and system requirements. EasyBR 1.7.8 and later includes the Bridge and browser extension on Apple Silicon Macs and Windows, so no separate Bridge installation is needed there. Ordinary browsers and other systems require the full Easy WebBridge setup described in the official guide.

For a browser task the user has authorized through this Skill, check and reuse a suitable existing environment first. If a new one is genuinely needed, create one unique environment for this task with safe defaults, read back its actual environment ID, and start it. Do not ask the user to reconfirm or supply an environment name or default parameters. After confirming the correct account and `browserId`, continue the user's current task instead of stopping at setup instructions; do not ask for approval at each necessary step. Pause only for CAPTCHA/account security checks, real ambiguity about the target account or authorization, or missing local-control capability. At completion, close only the task tab group created for this run and report results and limits under this Skill's rules.

This Skill provides the business workflow. Automatic installation, sign-in assistance, and environment management also depend on the AI agent's local-control capabilities and the components described in the official guide.
