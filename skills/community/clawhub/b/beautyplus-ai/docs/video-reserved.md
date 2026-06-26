# Video tasks (reserved)

> The current effect KEY catalog is **image-only**. This document captures the
> async / video flow that becomes active when video-only effect KEYs are
> exposed by the server and the CLI again. While no video keys are listed in
> [SKILL.md](../SKILL.md), follow the image flow (`run-task`, §3a) and ignore
> this file.

When a video key is added, the agent uses **`spawn-run-task`** (printed
payload) plus the host's **`sessions_spawn`** so the main session is not
blocked on a long poll.

## When to use this path

- Effect KEY is one the CLI explicitly accepts via `spawn-run-task` (historical
  examples: `videoscreenclear`, `hdvideoallinone`).
- For all current image keys the CLI rejects `spawn-run-task` — keep using
  `run-task` (SKILL.md §3a).

## Submitting

```bash
python3 {baseDir}/scripts/beautyplus_ai.py spawn-run-task \
  --task "<video_effect_key>" \
  --input "<video_url_or_path>" \
  --deliver-to "<oc_xxx_or_ou_xxx_or_chat_id>" \
  --deliver-channel "feishu"
```

Optional flags:

- `--params '<json>'` — same shape as `run-task`.
- `--deliver-channel telegram|discord|...`.
- `--run-timeout-seconds` — default **3600**, aligned with the extended poll
  budget. **Do not** lower `runTimeoutSeconds` below the payload default
  unless you accept timeout risk; wall time often runs minutes to tens of
  minutes.

## Hand-off to `sessions_spawn`

1. Read the `sessions_spawn_args` block from stdout (`task`, `label`,
   `runTimeoutSeconds`).
2. Call OpenClaw `sessions_spawn` with those args **unchanged**.
3. Reply immediately to the user that processing has started. The sub-agent
   runs `install-deps` (if needed), `run-task`, then Step 4 delivery per the
   embedded task text.

## Multi-stage video chains

One `sessions_spawn` embed = one `run-task`. A chain = multiple spawns. Image
chains follow SKILL.md §3a only.

## Delivery (after success)

### Feishu — video tasks

```bash
curl -sL -o /tmp/beautyplus_result.mp4 "<primary_result_url_or_output_urls[0]>"
python3 {baseDir}/scripts/feishu_send_video.py \
  --video /tmp/beautyplus_result.mp4 \
  --to "<oc_xxx or ou_xxx>" \
  --video-url "<primary_result_url_or_output_urls[0]>" \
  [--cover-url "<optional_thumb_url>"] \
  [--duration <milliseconds_if_known>]
```

`--video-url` adds a second message with the download link. Optional
cover/duration; details: [feishu-send-video.md](feishu-send-video.md).

### Telegram — video tasks

```bash
curl -sL -o /tmp/beautyplus_result.mp4 "<primary_result_url_or_output_urls[0]>"
TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" python3 {baseDir}/scripts/telegram_send_video.py \
  --video /tmp/beautyplus_result.mp4 \
  --to "<chat_id>" \
  --video-url "<primary_result_url_or_output_urls[0]>" \
  [--cover-url "<optional_thumb_url>"] \
  [--duration <seconds>] \
  --caption "✅ Done"
```

`--video-url` sends a follow-up text message with the download link. Max
~**50 MB** for the Telegram Bot API video upload; larger files rely on the
link line.

### Discord — video tasks

Same shape as image delivery (`message` tool with `filePath`), use a `.mp4`
file. For files over ~25 MB, send the result URL as a link instead.

## Polling, timeouts, recovery

See [errors-and-polling.md](errors-and-polling.md) for the poll schedule,
`MT_AI_*` overrides, SIGKILL recovery via `last-task` + `query-task`, and the
quota / consume failure table.
