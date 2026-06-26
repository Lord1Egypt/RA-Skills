# CLI Reference

## Commands

### record

Record an AI-driven browser demo.

```
npx screencli record [url] -p "<prompt>" [options]
```

**Options:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-p, --prompt <text>` | string | *(required)* | Instructions for the AI agent |
| `-o, --output <dir>` | string | `./recordings` | Output directory |
| `--viewport <WxH>` | string | `1920x1080` | Browser viewport dimensions |
| `-m, --model <model>` | string | `claude-sonnet-4-20250514` | Claude model |
| `--headless / --no-headless` | flag | headless | Show browser window if `--no-headless` |
| `--slow-mo <ms>` | number | `0` | Extra delay between actions (ms) |
| `--max-steps <n>` | number | `50` | Maximum agent iterations |
| `-v, --verbose` | flag | off | Debug logging |
| `--background <name>` | choice | auto | Override gradient: `midnight`, `ember`, `forest`, `nebula`, `slate`, `copper`, `none` |
| `--no-background` | flag | — | Alias for `--background none` |
| `--padding <percent>` | number | `8` | Background padding (0-50%) |
| `--corner-radius <px>` | number | `12` | Corner radius in pixels |
| `--no-shadow` | flag | — | Disable drop shadow |
| `--login` | flag | — | Open browser for manual login first |
| `--auth <name>` | string | — | Save/load auth state by name |
| `--local` | flag | — | Skip cloud upload |
| `--unlisted` | flag | — | Upload as unlisted |

### export

Export a recording with platform-specific presets.

```
npx screencli export <recording-dir> --preset <name> [options]
```

**Options:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--preset <name>` | choice | `youtube` | Platform preset |
| `-o, --output <path>` | string | auto | Custom output file path |
| `--background <name>` | choice | — | Apply gradient background |
| `--no-background` | flag | — | Disable background |
| `--padding <percent>` | number | `8` | Background padding |
| `--corner-radius <px>` | number | `12` | Corner radius |
| `--no-shadow` | flag | — | Disable drop shadow |
| `--no-zoom` | flag | — | Disable auto-zoom |
| `--no-highlight` | flag | — | Disable click highlights |
| `--no-cursor` | flag | — | Disable cursor trail |

**Presets:**

| Preset | Resolution | Aspect | Format | Max Duration | Codec |
|--------|-----------|--------|--------|--------------|-------|
| `youtube` | 1920x1080 | 16:9 | mp4 | — | libx264 |
| `twitter` | 1280x720 | 16:9 | mp4 | 140s | libx264 |
| `instagram` | 1080x1920 | 9:16 | mp4 | 90s | libx264 |
| `tiktok` | 1080x1920 | 9:16 | mp4 | — | libx264 |
| `linkedin` | 1080x1080 | 1:1 | mp4 | — | libx264 |
| `github-gif` | 800x450 | 16:9 | gif | 12s | gif |

### login

Sign in to screencli cloud.

```
npx screencli login
```

### logout

Sign out of screencli cloud.

```
npx screencli logout
```

### whoami

Show current user and plan info.

```
npx screencli whoami
```

Displays: user, email, plan, credits remaining, recordings this month.

### recordings

List your cloud recordings.

```
npx screencli recordings
```

Displays a table with recording ID, title, view count, and shareable link.

### delete

Delete a cloud recording.

```
npx screencli delete <id>
```

### upload

Upload a local recording to the cloud.

```
npx screencli upload <dir>
```

Requires a valid recording directory containing `metadata.json` and `composed.mp4`.

### render

Re-render a cloud recording with different settings.

```
npx screencli render <id> [options]
```

**Options:**

| Flag | Type | Description |
|------|------|-------------|
| `--background <name>` | choice | Gradient background |
| `--preset <name>` | choice | Export preset |

Enqueues a server-side render job and polls until complete.

## Config

**Location:** `~/.screencli/config.json`

Stores authentication token, email, and plan after login. Login is triggered automatically on first `record`, or manually via `npx screencli login`.

**Auth state:** `~/.screencli/auth/<name>.json`

Stores browser session (cookies, localStorage) for `--auth` reuse.

## Output Structure

Each recording is saved to `./recordings/<id>/`:

```
recordings/<id>/
  raw.webm           # Raw browser recording
  composed.mp4       # Final video with effects
  events.json        # Event log (clicks, scrolls, narrations)
  metadata.json      # Recording metadata (id, url, prompt, duration, etc.)
  exports/           # Platform exports (created by export command)
```
