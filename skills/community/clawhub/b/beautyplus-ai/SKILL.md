---
name: beautyplus-ai
description: "AI image editing and beautification suite for portrait retouching, body reshaping (breast/butt), AI hair styling, AI clothes / cosplay change, expression edits, photo restoration & upscaling, and artistic filters."
version: 1.1.0
author: BeautyPlus
metadata: {"openclaw":{"emoji":"🖼️","requires":{"bins":["python3"],"env":{"BP_AK":{"required":true},"BP_SK":{"required":true}}},"tags":["image-processing","portrait-retouching","body-reshape","virtual-try-on","ai-cosplay","photo-restoration","image-upscaling","makeover"]}}
---

# BeautyPlus Skills & API

> **`{baseDir}` placeholder.** Every CLI command in this file uses
> `{baseDir}/scripts/...`. The host (skill loader) substitutes `{baseDir}`
> with this skill's installation directory at load time. If your host does
> not expand placeholders, replace `{baseDir}` with the absolute path to
> this skill folder, or run from inside the skill folder using `scripts/...`.

## When to Use This Skill

Activate whenever the user requests modifications, enhancements, or artistic
changes to a **photo / image** (path, URL, or attachment).

**Trigger keywords:** "make me look better", "change my clothes", "fix this
blurry photo", "make me smile", "enhance my body", "change my hair color /
style", "add a filter", "cosplay", "outfit change", "upscale", "virtual
try-on".

## Effect KEY catalog (`--task` values)

The CLI `--task` value is always one of the **effect KEYs** below. Per-key
algorithm params are returned inline by `POST /skill/consume.json`
(`invoke_spec`) — never hard-code AIGC paths. If the server returns
`Unknown invoke preset`, the key is not in the tenant's invoke map; do not
invent params, check config or admin.

All KEYs operate on **still images** (`.jpg` / `.jpeg` / `.png` / `.webp`). The current catalog is image-only; the async / video flow
is reserved — see [docs/video-reserved.md](docs/video-reserved.md).

### 1. 💪 Body reshape

**When:** user explicitly asks to enhance, enlarge, or reshape breast or buttocks.

**Tier rule:** append `_strong` / `_medium` / `_weak` to the base KEY.
Default tier: `_medium` (e.g. `breast_natural_medium`).

| KEY (base)        | Description |
|-------------------|-------------|
| `breast_natural`  | Natural fullness; subtle lift. |
| `breast_teardrop` | Teardrop contour, fuller lower pole. |
| `breast_round`    | Rounded, lifted look with upward emphasis. |
| `breast_outward`  | Editorial spread with outward emphasis. |
| `butt_peach`      | Lift and side volume for a peach shape. |
| `butt_o_shape`    | Smooth, continuous curve, even side profile. |

### 2. 💇‍♀️ Hair editing

**When:** new hair color or new hairstyle.

| KEY                     | Description |
|-------------------------|-------------|
| `hair_black`            | Deep black shine; natural look. |
| `hair_blonde`           | Classic golden blonde. |
| `hair_brown_highlights` | Brown with highlights for dimension. |
| `hair_platinum`         | Soft creamy platinum. |
| `hair_silver_platinum`  | Cool metallic silver; edgy modern look. |
| `hair_teddy_brown`      | Warm soft brown; youthful vibe. |
| `hair_glossy`           | Extra shine and sleek fall. |
| `hair_high_layer`       | Light layers and airy volume. |
| `hair_soft_waves`       | Romantic large waves. |
| `hair_latino_curls`     | Tight curls, maximum volume. |

### 3. 👗 Outfit change (AI clothes)

**When:** user asks to change clothes, try on different styles, or dress up
for a specific occasion / cosplay.

**Formal / Evening**

| KEY                     | Description |
|-------------------------|-------------|
| `dress_yellow_gown`     | Vivid yellow silk evening gown. |
| `dress_arctic_allure`   | Rhinestone mesh gown with galaxy sparkle. |
| `dress_ostrich_feather` | Ethereal feather gown. |
| `dress_muse_goddess`    | Couture-heavy beaded goddess gown. |
| `suit_tartan_eve`       | Smart, polished British tartan suit. |
| `suit_red_carpet`       | Classic sharp black suit. |

**Vacation / Casual**

| KEY                      | Description |
|--------------------------|-------------|
| `accessory_bunny_ear`    | Playful bunny ear accessory. |
| `dress_butter_moonlight` | Pale yellow slip dress; fresh light look. |
| `dress_pink_puffy`       | Tiered pink puff dress; sweet portrait style. |
| `dress_gold_hoodie`      | Urban casual hoodie dress. |
| `dress_lace_corset`      | French-inspired lace corset set. |
| `dress_chiffon_cake`     | Tiered chiffon maxi; relaxed vacation mood. |
| `dress_sheer_bikini`     | Bikini under sheer cover; resort look. |

**Cosplay / Fantasy**

| KEY                     | Description |
|-------------------------|-------------|
| `cosplay_carnival`      | Carnival samba outfit with feather headpiece. |
| `cosplay_bunny_cop`     | Navy bunny police uniform. |
| `cosplay_fox_boyfriend` | Green fox print shirt; relaxed vibe. |
| `cosplay_deer_girl`     | Forest fawn-inspired mini skirt. |
| `cosplay_grinch`        | Green fuzzy Grinch party costume. |
| `victoria_angel`        | Lingerie set with wings (runway showstopper). |
| `dallas_cowboy`         | Iconic blue-and-white cheerleader uniform. |

**Party / Futuristic**

| KEY                | Description |
|--------------------|-------------|
| `floral_camisole`  | Botanical floral cami. |
| `puff_skirt`       | Strapless puff corset dress. |
| `one_shoulder_lbd` | One-shoulder little black dress. |
| `red_latex`        | Bold red latex mini skirt. |
| `moonlight_dress`  | Full-rhinestone bodycon long gown. |
| `y3k_set`          | Futuristic metallic Y3K co-ord. |

**Sports / Activewear**

| KEY                | Description |
|--------------------|-------------|
| `brazilian_bikini` | Brazilian-cut bikini. |
| `tennis_set`       | Sporty athletic-chic tennis skirt and top. |
| `cozy_fit`         | Relaxed hoodie and jogger; urban athleisure. |
| `racing_suit`      | Bold motorsport racing driver suit. |
| `white_yoga`       | Minimal white yoga set. |

### 4. 🎭 Facial retouch & expression

**When:** retouch / apply a makeup style, or change the subject's expression.

| KEY               | Description |
|-------------------|-------------|
| `natural_beauty`  | Soft natural enhancement; clear skin. |
| `glamour_beauty`  | Polished, charismatic look with full makeup. |
| `sweet_beauty`    | Youthful sweet-girl vibe. |
| `luminous_beauty` | Radiant glow; bright complexion. |
| `youthful_beauty` | Fresh, energetic style. |
| `closed_smile`    | Gentle closed-lip smile. |
| `open_smile`      | Wide toothy grin. |
| `cool_expression` | Serious, composed, edgy. |
| `wink`            | Single-eye wink. |

### 5. 🖼️ Photo quality & art filters

**When:** image is blurry / noisy / old / low-resolution, or the user wants
a camera vibe / lighting filter.

| KEY                    | Description |
|------------------------|-------------|
| `photo_restoration_v3` | Denoise, deblur, reduce artifacts; keeps a natural look. |
| `ai_ultra_hd_v3`       | Deep-learning upscale + detail recovery for old / small photos. |
| `tanning_filter`       | Warm bronzed tan skin filter. |
| `ccd_flash`            | Vintage CCD-camera flash effect. |
| `film_flash`           | Film grain with flash overlay. |
| `fuji_flash`           | Fujifilm-style flash; soft grain, warm tones. |

## Defaults & disambiguation (MANDATORY)

Use this table when the user's intent is broad or under-specified. Do **not**
guess a wrong KEY.

| Situation | Action |
|-----------|--------|
| Vague intent ("make this photo look better") | Default to `natural_beauty` if a face is present, else `photo_restoration_v3`. |
| User asks for retouch / makeup but did not pick a style | Offer 2–3 KEYs from §4 (e.g. `natural_beauty`, `glamour_beauty`, `sweet_beauty`). |
| User says "change my hair / outfit / cosplay" without a style | Ask one question, or offer 2–3 KEYs from §2 / §3. |
| Body reshape, no tier given | Default to `_medium`, or briefly confirm before submit. |
| User mentions video / motion / "make a video" | No video keys exist today — see [docs/video-reserved.md](docs/video-reserved.md). Stay on still images. |
| Ambiguous or missing attachment | Ask one clarifying question, or pull media from IM per [docs/im-attachments.md](docs/im-attachments.md). |

## API submission path (MANDATORY)

- **New jobs** must go through
  **`python3 {baseDir}/scripts/beautyplus_ai.py run-task …`** (or the same
  `run-task` embedded inside `spawn-run-task` → `sessions_spawn` for the
  reserved video flow).
- **Do not** hand-craft HTTP to the skill's `wapi` gateway or to
  AIGC / invoke endpoints — that skips `POST /skill/consume.json` (quota and
  permission) and breaks the supported pipeline. This skill does not emit
  debug curl for API calls.
- **`query-task --task-id`** is for **resuming polling** on an existing
  full `task_id` only; it does **not** replace `run-task` for a new
  submission.

## Billing and user-facing claims (MANDATORY)

- Each successful `run-task` (including inside a `sessions_spawn` worker)
  triggers server-side **quota / credit consumption** for the `BP_AK`
  tenant. This is a paid, metered commercial API.
- **Do not** state or imply that the service is free, costs nothing, has an
  unlimited trial, or invent prices, plan names, promotions, or trial rules.
- **Allowed wording:** processing uses the BeautyPlus account quota tied to
  the configured keys; billing and plans are per the user's console or
  administrator.
- On quota / membership errors, surface the server `detail` and
  `pricing_url` (see Step 3 error table). Never add "free" or zero-cost
  wording, even on success.

---

## Step 0 — Pre-flight check (MANDATORY)

Verify AK / SK are configured. **Only run this command** at this stage; do
not read other Python sources first.

```bash
python3 {baseDir}/scripts/beautyplus_ai.py preflight
```

- Output `ok` → continue to Step 1.
- Output `missing` → **stop** and prompt the user. Use the channel-appropriate
  template in [docs/credentials-prompt.md](docs/credentials-prompt.md)
  (plain text by default; Feishu interactive card when the host exposes a
  Feishu account).

## Step 1 — Pick effect KEY and input

1. Map the user's intent to one **effect KEY** from the catalog above. Apply
   the **Defaults & disambiguation** table when the request is broad.
2. Confirm the input file location. If the user already gave a path or URL,
   continue to Step 2 without asking again.
3. **Reply immediately** to acknowledge, e.g. *"🖼️ Processing — please wait
   a moment…"*

### Getting media from IM messages

Full detail: [docs/im-attachments.md](docs/im-attachments.md).

| Platform | How to obtain |
|----------|---------------|
| Feishu   | Message resource URL / `image_key` + `message_id` → optional `resolve-input` |
| Telegram | `file_id` → `resolve-input --telegram-file-id` (needs `TELEGRAM_BOT_TOKEN`) |
| Discord  | `attachments[0].url` — often usable directly as `--input` |
| Generic  | URL or path |

```bash
python3 {baseDir}/scripts/beautyplus_ai.py resolve-input --file /tmp/saved.jpg --output-dir /tmp
# or: --url, --telegram-file-id, --feishu-image-key + --feishu-message-id
```

Use the JSON `path` field as `--input`.

**`--input` as a URL:** quote the full URL in the shell to avoid `&`
splitting. Defaults: 120 s read timeout, 100 MB max — override with
`MT_AI_URL_READ_TIMEOUT`, `MT_AI_URL_CONNECT_TIMEOUT`, `MT_AI_URL_MAX_BYTES`.
For flaky or large links, use `resolve-input --url` first and pass the local
`path`.

## Step 2 — Install dependencies

```bash
python3 {baseDir}/scripts/beautyplus_ai.py install-deps
```

If dependencies are already installed this step is quick; then continue to
Step 3.

## Step 3 — Run the task

All listed effect KEYs are image jobs — use the inline `run-task` flow
(§3a). Video keys are reserved; see [docs/video-reserved.md](docs/video-reserved.md).

### 3a — Inline `run-task` (blocking, default)

```bash
python3 {baseDir}/scripts/beautyplus_ai.py run-task \
  --task "<effect_key>" \
  --input "<image_url_or_path>"
```

Replace `<effect_key>` (e.g. `hair_soft_waves`) and `<image_url_or_path>`
with real values. Default params include `rsp_media_type: url`. For custom
JSON params:

```bash
python3 {baseDir}/scripts/beautyplus_ai.py run-task \
  --task "<effect_key>" \
  --input "<url_or_path>" \
  --params '{"parameter":{"rsp_media_type":"url"}}'
```

#### When `run-task` exits 0

Stdout is JSON containing:

- `skill_status: "completed"` — job done.
- `output_urls` — ordered `http(s)` links (extracted from
  `data.result.urls`, `images`, `media_info_list`, etc.).
- `primary_result_url` — same as `output_urls[0]`; convenient for delivery.
- `task_id` — full task id when the API returns one. Keep it for support /
  recovery; do not truncate. Some sync completions may omit it.
- `agent_instruction` — short reminder for the model.
- `meta` / `data` — full API payload for debugging.

**You must:**

1. Send the user a short natural-language summary of what was done.
2. Complete Step 4 delivery using `primary_result_url` or `output_urls[0]`,
   unless the user explicitly asked for the URL only.

Never end the turn with raw JSON alone. Never resubmit `run-task` for the
same `task_id` — use `query-task` to resume polling.

#### When `run-task` exits non-zero

Stdout has `skill_status: "failed"` with an `error` field. Map it as:

| `error`               | `api_code` | Action |
|-----------------------|------------|--------|
| `credit_required`     | 60002      | Show server `detail` to the user; include `pricing_url` as a link if present. Do **not** retry by tweaking params. |
| `membership_required` | 60001      | Same — show `detail` / `pricing_url`. |
| `consume_param_error` | —          | Fix `--task` / `--input` / `--params`; do **not** tell the user to recharge. |
| Other (`task_failed`, `poll_timeout`, `poll_aborted`, …) | — | See [docs/errors-and-polling.md](docs/errors-and-polling.md). |

Never dump raw JSON to the user. Never retry `run-task` for credit /
membership errors.

### 3b — Resume polling (`query-task`)

When you already have a full `task_id` (from previous stdout JSON, polling
checkpoint, or `task_id=...` lines in stderr) and the job may still be
running, **do not run `run-task` again** — resume polling only:

```bash
python3 {baseDir}/scripts/beautyplus_ai.py query-task \
  --task-id "<full_task_id>"
```

Optional `--task` sets the `task_name` field in the success JSON for your
logs (default labels as `query_task`). Uses the same `BP_AK` / `BP_SK` and
remote config as the original submit. Stdout JSON and exit codes match
`run-task`.

### 3c — Last task and history

Local state lives under `~/.openclaw/workspace/beautyplus-ai/`
(`last_task.json`, `history/task_*.json`, last 50 records). For async jobs,
`last_task.json` may briefly show `skill_status: "polling"` with a
`task_id` while the client is still polling — a checkpoint that lets
`query-task` resume if the process is killed mid-poll.

```bash
python3 {baseDir}/scripts/beautyplus_ai.py last-task
python3 {baseDir}/scripts/beautyplus_ai.py history
```

Use when the user asks whether a recent job finished, or wants a short
history summary. Do not expose raw secrets.

## Step 4 — Deliver result to the channel

Required after `skill_status: "completed"`. The CLI does not post to IM by
itself — send the processed image back on the user's platform, in the same
turn as the success summary.

### Resolve `deliver-to`

| Platform     | Source                                                   | Format |
|--------------|----------------------------------------------------------|--------|
| Feishu group | `conversation_label` or `chat_id` without `chat:` prefix | `oc_xxx` |
| Feishu DM    | `sender_id` without `user:` prefix                       | `ou_xxx` |
| Telegram     | inbound message `chat_id`                                | e.g. `-1001234567890` |
| Discord      | `channel_id`                                             | e.g. `123456789` |

### Feishu

```bash
python3 {baseDir}/scripts/feishu_send_image.py \
  --image "<result_url>" \
  --to "<oc_xxx or ou_xxx>"
```

### Telegram

```bash
TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" python3 {baseDir}/scripts/telegram_send_image.py \
  --image "<result_url>" \
  --to "<chat_id>" \
  --caption "✅ Done"
```

### Discord

Download the result, then send with the `message` tool:

```bash
curl -L "<result_url>" -o /tmp/result_image.jpg
```

```
message(action="send", channel="discord", target="<channel_id>", filePath="/tmp/result_image.jpg")
```

For files over ~25 MB, send the result URL as a link instead.

### WhatsApp / Signal / others

Use the `message` tool with `media`, or send the result URL directly.

**Video delivery (reserved):** see [docs/video-reserved.md](docs/video-reserved.md).

## Multi-stage pipelines (chaining tasks)

When the user asks for more than one BeautyPlus step on the same media
(e.g. `photo_restoration_v3` → `dress_yellow_gown`), treat each step as a
**separate job** with its own `--task`:

1. After stage A completes, pass `primary_result_url` (or `output_urls[0]`)
   as `--input` for the next stage. That is a new job, not a retry.
2. *"Do not re-run `run-task`"* means: do not resubmit the **same**
   `task_id`. It does not forbid the next stage with a different effect KEY.
3. Deliver only after the **final** stage completes.

Video chains are reserved — see [docs/video-reserved.md](docs/video-reserved.md).

## Notes

- **Single business entrypoint:** all algorithm runs and config fetches go
  through `beautyplus_ai.py`; agents do not need to open `client.py` or
  `ai/api.py`. See **API submission path** above for the no-direct-HTTP
  rule.
- **AK / SK loading:** environment variables `BP_AK` / `BP_SK` first; if
  unset, `scripts/.env` is read automatically.
- **Client init** pulls the latest algorithm config from the server; no
  manual `INVOKE` setup is required.
- **Bot token safety:** pass `TELEGRAM_BOT_TOKEN`, `DISCORD_BOT_TOKEN`, etc.
  only via environment variables — never as CLI arguments.
- **URL input errors** may report HTTP 403 (expired signed URL) or timeout —
  see `MT_AI_URL_*` env vars in Step 1.

## Further reading

- [BeautyPlus Developers](https://www.beautyplus.com/developers/console) — API and skill key integration, use cases.
- [BeautyPlus](https://www.beautyplus.com) — product overview.
- [README.md](README.md)
- [docs/video-reserved.md](docs/video-reserved.md) — async / video flow (reserved).
- [docs/credentials-prompt.md](docs/credentials-prompt.md) — `preflight: missing` user prompt templates.
- [docs/multi-platform.md](docs/multi-platform.md) — delivery details (Feishu, Telegram, Discord, …).
- [docs/im-attachments.md](docs/im-attachments.md) — IM attachments and `resolve-input`.
- [docs/errors-and-polling.md](docs/errors-and-polling.md) — polling, timeouts, failure codes.
