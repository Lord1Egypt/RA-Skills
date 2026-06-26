---
name: artclaw-creative-suite
description: |
  ARTCLAW AI Creative Suite - invoke ARTCLAW platform's AI content creation capabilities via CLI.
  Supports AI image generation, video generation, workflow execution, multimodal analysis, and job management.
  All generation commands must run asynchronously using the current platform adapter. Requires an API Key prefixed with vk_ for authenticated features.
  Trigger keywords: generate image, generate video, AI painting, text-to-image, text-to-video, image-to-video, marketing image,
  logo, cover, workflow, video analysis, image analysis, ARTCLAW, ArtClaw.
compatibility:
  dependencies:
    - ARTCLAW REST API (https://artclaw.com/api/v1)
    - Python 3.8+ with requests package
metadata:
  {
    'openclaw':
      {
        'emoji': '🎨',
        'requires': { 'env': ['ARTCLAW_API_KEY'] },
        'primaryEnv': 'ARTCLAW_API_KEY',
      },
  }
---

# ARTCLAW AI Creative Suite

ARTCLAW is an all-in-one AI content creation platform. This skill uses `scripts/artclaw.py` as the single CLI entry point for authentication, submission, polling, retry, history, and JSON output.

## Mandatory Startup Flow

1. Detect the current agent platform.
2. Read exactly one matching adapter document from `docs/adapters/` before running generation or workflow commands.
3. Run the pre-flight API key check before authenticated operations.
4. Never mix execution rules from multiple adapters.

If platform detection is ambiguous, ask the user which platform they are using. If the platform is unsupported, use `docs/adapters/others.md`.

## Platform Adapter Map

| Platform | Adapter document |
| --- | --- |
| OpenClaw | `docs/adapters/openclaw.md` |
| Claude Code | `docs/adapters/claude-code.md` |
| Hermes Agent | `docs/adapters/hermes.md` |
| Unknown / unsupported platform | `docs/adapters/others.md` |

## Universal Rules

1. Use the CLI, not raw curl: `python3 scripts/artclaw.py ...`.
2. Run `python3 scripts/artclaw.py verify-key` before authenticated operations.
3. Generation and workflow commands are long-running and must not block the main agent silently.
4. In Claude Code, prefer Bash `run_in_background: true` so `/tasks` can track the local background task. **DO NOT manually poll with `job-status` after the background task completes** — the background task already polls internally and returns the final result in its output.
5. In non-spawn platforms, use `--no-wait` by default unless the selected adapter explicitly defines a different async strategy or the user explicitly asks the agent to wait.
6. In OpenClaw-compatible spawn platforms, use `--spawn` instead of `--no-wait`.
7. Immediately tell the user after a generation/workflow job is submitted or a background task is started.
8. Analysis commands are synchronous and do not require spawn/background execution.
9. Guide users to https://artclaw.com/settings for API key creation and credit top-up.
10. Deliver generated media as native platform messages when the adapter supports it; otherwise return the result URL and job metadata.
11. Platform-specific async behavior, delivery semantics, and anti-blocking rules must be defined only in the selected adapter document under `docs/adapters/` and followed strictly.

---

## API Key & Account

Run this before authenticated operations:

```bash
python3 scripts/artclaw.py verify-key
```

- `{"status": "valid"}`: continue.
- Missing, invalid, or revoked key: stop and guide the user to configure a key.

Setup:

1. Open https://artclaw.com/settings.
2. Create an API key in the API Keys section.
3. Copy the generated key. It is prefixed with `vk_` and is shown only once.
4. Configure locally:

```bash
python3 scripts/artclaw.py config-init --api-key "vk_xxx"
```

Useful account commands:

```bash
python3 scripts/artclaw.py account-info
python3 scripts/artclaw.py config
```

All local ARTCLAW data is stored under `~/.artclaw/`, including `config.json`, `last_job.json`, and `history/`.

---

## Generation Commands

Generation and workflow commands are long-running. Always follow the current platform adapter before choosing `--spawn`, Claude Code `run_in_background`, `--no-wait`, or explicit waiting.

Safe default:

- OpenClaw-compatible adapters use `--spawn`.
- Claude Code uses Bash `run_in_background: true` when available.
- Other non-spawn adapters use `--no-wait` — unless the adapter defines its own background strategy (e.g. Hermes uses background terminal; see adapter doc).
- Only omit both when the user explicitly asks the agent to wait for completion.

### Generate Image

```bash
python3 scripts/artclaw.py generate-image \
  --prompt "Cyberpunk cityscape at night, neon lights reflected in rainwater" \
  --aspect-ratio 16:9 \
  --no-wait
```

With references:

```bash
python3 scripts/artclaw.py generate-image \
  --prompt "Landscape painting in the same style" \
  --reference-urls https://example.com/style_ref.jpg \
  --no-wait
```

| Parameter | Description | Values |
| --- | --- | --- |
| `--prompt` | Image description, required | Text |
| `--aspect-ratio` | Aspect ratio | `16:9`, `9:16`, `1:1`, `4:3`, `21:9` |
| `--resolution` | Resolution | `1K`, `2K`, `4K` |
| `--reference-urls` | Reference image URLs or base64 data URIs | One or more values |
| `--reference-files` | Local reference files, auto-converted to base64 | One or more paths |
| `--model` | Model override | Model ID |

### Generate Video

```bash
python3 scripts/artclaw.py generate-video \
  --prompt "Waves crashing on rocks, slow motion" \
  --aspect-ratio 16:9 \
  --duration 5 \
  --resolution 720p \
  --no-wait
```

Image-to-video:

```bash
python3 scripts/artclaw.py generate-video \
  --prompt "Make the person in the frame turn their head and smile" \
  --reference-urls https://example.com/portrait.jpg \
  --no-wait
```

| Parameter | Description | Values |
| --- | --- | --- |
| `--prompt` | Video description, required | Text |
| `--aspect-ratio` | Aspect ratio | `16:9`, `9:16`, `1:1`, `4:3`, `21:9` |
| `--duration` | Duration in seconds | `2` - `12` |
| `--resolution` | Resolution | `480p`, `720p`, `1080p` |
| `--reference-urls` | Reference image URLs or base64 data URIs | One or more values |
| `--reference-files` | Local reference image files, auto-converted | One or more paths |
| `--model` | Model override | Model ID |

### Generate Marketing Image

```bash
python3 scripts/artclaw.py generate-marketing-image \
  --prompt "Summer cool drinks promotional poster" \
  --size 1080x1920 \
  --no-wait
```

### Execute Workflow

```bash
python3 scripts/artclaw.py list-workflows
```

```bash
python3 scripts/artclaw.py run-workflow \
  --workflow-id "text-to-image-basic" \
  --inputs '{"prompt": "Anime-style forest"}' \
  --no-wait
```

Replace `--no-wait` with `--spawn`, `--deliver-to`, and `--deliver-channel` only when the current platform adapter says to do so.

---

## Analysis Commands

Analysis commands are synchronous. They do not require `--spawn` or background execution.

### Image Analysis

```bash
python3 scripts/artclaw.py analyze-image \
  --reference-urls https://example.com/photo.jpg \
  --query "Describe the main content of this image"
```

### Video Analysis

```bash
python3 scripts/artclaw.py analyze-video \
  --reference-urls https://example.com/clip.mp4 \
  --query "Summarize the video content"
```

### Script Extraction

```bash
python3 scripts/artclaw.py analyze-script \
  --reference-paths https://example.com/drama.mp4
```

### Character Profiles

```bash
python3 scripts/artclaw.py analyze-characters \
  --text "Li Ming is an introverted but brilliant programmer..."
```

---

## Job Management & Errors

```bash
python3 scripts/artclaw.py job-status --job-id "job_xxxxxxxx"
python3 scripts/artclaw.py list-jobs --status success --limit 10
python3 scripts/artclaw.py cancel-job --job-id "job_xxxxxxxx"
python3 scripts/artclaw.py last-job
python3 scripts/artclaw.py history --limit 50
```

Use `job-status`, `last-job`, and `history` for follow-up instead of resubmitting generation requests. There is no `latest-job` command.

| Error | Cause | Resolution |
| --- | --- | --- |
| `401 Unauthorized` | API key invalid, missing, or revoked | Guide user to regenerate the key |
| `402` / insufficient credits | Account balance depleted | Guide user to top up at https://artclaw.com/settings |
| `404 Job not found` | Job ID does not exist or expired after 24h | Tell user the job expired and ask whether to regenerate |
| `404 Workflow not found` | Workflow does not exist | Run `list-workflows` first |
| `429 Too Many Requests` | Rate limit exceeded | Wait and retry |

---

## Delivery Targets

Use delivery options only when the platform adapter supports spawn/delivery mode.

`--spawn` must be paired with both `--deliver-to` and `--deliver-channel`.

| Scenario | `--deliver-channel` | `--deliver-to` value | Source |
| --- | --- | --- | --- |
| Feishu group chat | `feishu` | `oc_xxx` chat ID | `conversation_label` or `chat_id`, strip `chat:` prefix |
| Feishu direct message | `feishu` | `ou_xxx` open ID | `sender_id`, strip `user:` prefix |
| Telegram | `telegram` | `chat_id` | Inbound message context |
| Discord | `discord` | `channel_id` | Inbound message context |

For Feishu, check `is_group_chat` in inbound metadata: `true` → use `oc_` chat ID; `false` → use `ou_` open ID.

| Channel | Credential source |
| --- | --- |
| `feishu` | `~/.openclaw/openclaw.json` → `channels.feishu.accounts.main` |
| `telegram` | `TELEGRAM_BOT_TOKEN` environment variable |
| `discord` | Framework built-in message tool |

---

## Self Update

```bash
python3 scripts/artclaw.py self-update
```

Preview without writing files:

```bash
python3 scripts/artclaw.py self-update --dry-run
```

Downloads `https://github.com/ArtClaw1/artclaw-skill/archive/refs/heads/main.zip`, atomically applies added or modified files, and reports a JSON summary. Does not delete local-only files.
