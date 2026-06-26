---
name: baoyu-post-to-xhs
description: Posts image-text notes to Xiaohongshu (小红书) via Chrome CDP. Supports uploading multiple images, filling title/description, adding topics, and optional auto-submit. Use when user asks to "post to Xiaohongshu", "发小红书", "发布小红书笔记", "publish to XHS", or "share on RedNote".
version: 1.2.0
metadata:
  openclaw:
    homepage: https://github.com/praguepp/baoyu-skills#baoyu-post-to-xhs
    requires:
      anyBins:
        - bun
        - npx
---

# Post to Xiaohongshu (小红书)

Posts image-text notes to Xiaohongshu via real Chrome browser (bypasses anti-bot detection).

## Language

**Match user's language**: Respond in the same language the user uses. If user writes in Chinese, respond in Chinese. If user writes in English, respond in English.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `{baseDir}`
2. Script path = `{baseDir}/scripts/<script-name>.ts`
3. Replace all `{baseDir}` in this document with the actual path
4. Resolve `${BUN_X}` runtime: if `bun` installed → `bun`; if `npx` available → `npx -y bun`; else suggest installing bun

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/xhs-browser.ts` | Image-text note publishing |
| `scripts/check-permissions.ts` | Verify environment & permissions |

## Preferences (EXTEND.md)

Check EXTEND.md existence (priority order):

```bash
# macOS, Linux, WSL, Git Bash
test -f .baoyu-skills/baoyu-post-to-xhs/EXTEND.md && echo "project"
test -f "${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-post-to-xhs/EXTEND.md" && echo "xdg"
test -f "$HOME/.baoyu-skills/baoyu-post-to-xhs/EXTEND.md" && echo "user"
```

```powershell
# PowerShell (Windows)
if (Test-Path .baoyu-skills/baoyu-post-to-xhs/EXTEND.md) { "project" }
$xdg = if ($env:XDG_CONFIG_HOME) { $env:XDG_CONFIG_HOME } else { "$HOME/.config" }
if (Test-Path "$xdg/baoyu-skills/baoyu-post-to-xhs/EXTEND.md") { "xdg" }
if (Test-Path "$HOME/.baoyu-skills/baoyu-post-to-xhs/EXTEND.md") { "user" }
```

┌──────────────────────────────────────────────────────┬───────────────────┐
│                         Path                         │     Location      │
├──────────────────────────────────────────────────────┼───────────────────┤
│ .baoyu-skills/baoyu-post-to-xhs/EXTEND.md            │ Project directory │
├──────────────────────────────────────────────────────┼───────────────────┤
│ $HOME/.baoyu-skills/baoyu-post-to-xhs/EXTEND.md      │ User home         │
└──────────────────────────────────────────────────────┴───────────────────┘

┌───────────┬───────────────────────────────────────────────────────────────────────────┐
│  Result   │                                  Action                                   │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Found     │ Read, parse, apply settings                                               │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Not found │ Use defaults                                                              │
└───────────┴───────────────────────────────────────────────────────────────────────────┘

**EXTEND.md Supports**: Default Chrome profile path

**Recommended EXTEND.md example**:

```md
chrome_profile_path: /path/to/chrome/profile
```

## Prerequisites

- Google Chrome or Chromium
- `bun` runtime
- First run: log in to Xiaohongshu manually in the browser (session saved)

## Pre-flight Check (Optional)

Before first use, suggest running the environment check. User can skip if they prefer.

```bash
${BUN_X} {baseDir}/scripts/check-permissions.ts
```

Checks: Chrome, profile isolation, Bun.

**If any check fails**, provide fix guidance per item:

| Check | Fix |
|-------|-----|
| Chrome | Install Chrome or set `XHS_BROWSER_CHROME_PATH` env var |
| Profile dir | Shared profile at `baoyu-skills/chrome-profile` |
| Bun runtime | `npm install -g bun` or `brew install oven-sh/bun/bun` (macOS) |

---

## Image-Text Note Posting (图文笔记)

```bash
${BUN_X} {baseDir}/scripts/xhs-browser.ts --title "标题" --content "描述" --image img1.png --image img2.png
${BUN_X} {baseDir}/scripts/xhs-browser.ts --markdown article.md --images ./photos/
${BUN_X} {baseDir}/scripts/xhs-browser.ts --title "标题" --content "描述" --images ./photos/ --topic "话题1" --topic "话题2" --submit
```

**Parameters**:
| Parameter | Description |
|-----------|-------------|
| `--title <text>` | Note title (max 20 chars, auto-compressed) |
| `--content <text>` | Note description (max 1000 chars, auto-compressed) |
| `--markdown <path>` | Markdown file for title/content extraction |
| `--image <path>` | Image file (repeatable, max 18) |
| `--images <dir>` | Directory containing images (PNG/JPG/WEBP) |
| `--topic <text>` | Topic/hashtag (repeatable) |
| `--submit` | Actually publish (default: preview only) |
| `--profile <dir>` | Custom Chrome profile directory |
| `--help` | Show help |

**Note**: By default the script only fills content into the browser. User reviews and publishes manually. Add `--submit` to auto-publish.

**Image Limits**: Up to 18 images per note. Supported formats: PNG, JPG, JPEG, WEBP, GIF.

---

## Publishing Workflow

### Step 1: Prepare Content

| Input Type | Detection | Action |
|------------|-----------|--------|
| Markdown file | `--markdown <path>` | Extract title from H1, content from body |
| Direct input | `--title` + `--content` | Use as-is |
| Images dir | `--images <dir>` | Load all images from directory |

### Step 2: Launch Browser & Login

1. Launch Chrome with dedicated profile
2. Navigate to `https://creator.xiaohongshu.com/publish/publish`
3. If not logged in → prompt user to scan QR code
4. Wait for login (up to 2 minutes timeout)

### Step 3: Upload Images

1. Find the image upload area on the publish page
2. Use `DOM.setFileInputFiles` or file chooser interception to upload images
3. Wait for upload completion (verify thumbnail count)

### Step 4: Fill Content

1. Fill title in the title input
2. Fill description/content in the editor
3. Add topics/hashtags if provided

### Step 5: Submit or Preview

- Default: leave browser open for user review
- With `--submit`: click the publish button

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Chrome debug port not ready | Kill existing Chrome CDP instances and retry |
| Not logged in | First run opens browser — scan QR code to log in |
| Chrome not found | Set `XHS_BROWSER_CHROME_PATH` env var |
| Image upload fails | Check file exists and is a valid image format |
| Title too long | Title auto-compressed to 20 chars |
| Content too long | Content auto-compressed to 1000 chars |

### Chrome debug port not ready

If a script fails with `Chrome debug port not ready`, kill existing Chrome CDP instances first, then retry:

```bash
pkill -f "Chrome.*remote-debugging-port" 2>/dev/null; sleep 2
```

```powershell
# PowerShell (Windows)
Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'remote-debugging-port' } | Stop-Process -Force
Start-Sleep -Seconds 2
```

**Important**: This should be done automatically — when encountering this error, kill Chrome CDP instances and retry the command without asking the user.

## Notes

- First run: manual login required (session persists in Chrome profile)
- All scripts fill content into the browser; user must review and publish manually unless `--submit` is used
- Cross-platform: macOS, Linux, Windows
- Xiaohongshu publish page: `https://creator.xiaohongshu.com/publish/publish`

## Extension Support

Custom configurations via EXTEND.md. See **Preferences** section for paths and supported options.
