---
name: chatmask
description: >-
  Pixelate chat/messaging app screenshots (WeChat, WhatsApp, Telegram, iMessage,
  Slack, Discord, etc.) to hide chat name, profile pics, and/or display names.
  Use when the user sends chat screenshots and asks to pixelate, blur, anonymize,
  redact, or hide identity elements. Supports English and Chinese prompts.
  Triggers: pixelate chat screenshot, blur names and avatars, anonymize chat,
  hide profile pics, redact chat, 打码聊天截图, 隐藏头像和昵称, 像素化截图,
  模糊聊天信息, 打码, 匿名截图, 隐藏头像, 隐藏昵称, 隐藏聊天名称
metadata: {"openclaw": {"requires": {"bins": ["python3", "git"]}, "emoji": "🎭", "homepage": "https://github.com/frankz2020/chatmask"}}
---

# ChatMask Skill

When the user sends chat screenshots and asks to pixelate or hide identity
elements, follow the steps below in order: **Setup → Workflow**.

**No external API key is required.** This skill uses your existing AI
capabilities to locate regions in the image, then delegates only the image
manipulation to the local Python script.

---

## Setup (run once, idempotent)

Run this block before the first job. Every step is guarded so re-running is safe.

```bash
# Default install path — override by setting CHAT_PIXELATE_PATH before calling the skill
CHAT_PIXELATE_PATH="${CHAT_PIXELATE_PATH:-$HOME/.openclaw/skills/chatmask}"

# 1. Clone repo and checkout the pinned, audited commit
#    Audited commit: 62b0d1132e8cad8455ef29f74a98da486ff102d4 (frankz2020/chatmask, v1.1.0)
PINNED_SHA="62b0d1132e8cad8455ef29f74a98da486ff102d4"
if [ ! -d "$CHAT_PIXELATE_PATH/.git" ]; then
  git clone https://github.com/frankz2020/chatmask.git "$CHAT_PIXELATE_PATH"
fi
# Enforce the pinned commit — prevents silent drift if the branch moves
(cd "$CHAT_PIXELATE_PATH" && git fetch --quiet origin && git checkout --quiet "$PINNED_SHA")

# 2. Create virtualenv if not already present
if [ ! -d "$CHAT_PIXELATE_PATH/.venv" ]; then
  python3 -m venv "$CHAT_PIXELATE_PATH/.venv" \
    || { apt-get install -y python3-venv && python3 -m venv "$CHAT_PIXELATE_PATH/.venv"; }
fi

# 3. Install / upgrade dependencies (Pillow, python-dotenv — no network calls at runtime)
"$CHAT_PIXELATE_PATH/.venv/bin/pip" install -q -r "$CHAT_PIXELATE_PATH/requirements.txt"

export CHAT_PIXELATE_PATH
PYTHON="$CHAT_PIXELATE_PATH/.venv/bin/python3"
```

> **What this installs:** Pillow (image processing) and python-dotenv (.env loader
> for standalone use only). The `requests` package is **not** installed by the
> skill — it is only needed for standalone/non-skill mode and lives in
> `requirements-standalone.txt`. No network calls are made by the script at runtime.

> **Network behavior:** The only outbound calls in Setup are `git clone` (one-time)
> and `pip install` (one-time). During Workflow, `process.py` makes **no network
> calls** when `--bbox-json` is supplied — all processing is local.

---

## Workflow

Read **Element Selection** and **Option Configuration** to translate natural-language
requests into the correct flags before running.

### 1. Prepare directories

```bash
JOB_ID="job_$(date +%s)"
OUT_DIR="/tmp/chat_pixelate_out_$JOB_ID"
mkdir -p "$OUT_DIR"
```

### 2. Process each image individually

**Each image must be analysed and pixelated separately.** Different screenshots
have different element positions — passing one image's bounding boxes to another
would leave sensitive regions unredacted. Repeat the following block for every
image the user sent.

> **Why per-image?** `--bbox-json` is scoped to a single image. `process.py`
> enforces this: it exits with an error if more than one image is present in the
> input directory when `--bbox-json` is used.

For each image `<filename.png>`:

#### 2a. Copy the image into its own input directory

```bash
# Use a fresh single-image input dir for each file
IMG_FILE="<filename.png>"   # replace with the actual filename
IN_DIR="/tmp/chat_pixelate_in_${JOB_ID}_${IMG_FILE%.*}"
mkdir -p "$IN_DIR"
cp "$HOME/.openclaw/media/inbound/$IMG_FILE" "$IN_DIR/"
```

#### 2b. Analyse the image with your vision capabilities

Use the prompt below on `$IN_DIR/$IMG_FILE` and capture the JSON output.
The schema uses **normalized coordinates (0-1000)** where (0,0) is top-left
and (1000,1000) is bottom-right, in `y_min, x_min, y_max, x_max` order.

```
You are a privacy specialist analyzing a chat/messaging app screenshot.
The app could be WeChat, WhatsApp, Telegram, iMessage, Slack, Discord, LINE,
KakaoTalk, or any other messaging application. The UI may be in English,
Chinese, or any other language. Identify the requested elements by their
visual layout and position, not by app-specific labels.

YOUR TASK:
Locate ALL occurrences of the following elements and return their bounding boxes:
1. chat_names   — The text title in the top navigation/header bar (conversation
                   name, group name, channel title, back-button contact name).
2. profile_pics — Circular or rounded avatar images next to message bubbles,
                   in the header, or on the participants list. Each distinct
                   avatar occurrence is its own region.
3. display_names — Text username/nickname labels directly next to or above
                   message bubbles (sender names, distinct from the header title).

RULES:
- Return ONLY the elements listed above.
- Each element occurrence must be its own region.
- Cover the full visible area with a small amount of padding.
- If an element type is not visible, return an empty list for that key.
- Use normalized coordinates (0-1000) where (0,0) is top-left and (1000,1000) is bottom-right.
- Coordinate order: y_min, x_min, y_max, x_max (top, left, bottom, right).
- All values must be integers between 0 and 1000.

Respond ONLY with a JSON object using this exact schema (no extra text outside the JSON):
{
  "chat_names":    [{"y_min": int, "x_min": int, "y_max": int, "x_max": int}],
  "profile_pics":  [{"y_min": int, "x_min": int, "y_max": int, "x_max": int}],
  "display_names": [{"y_min": int, "x_min": int, "y_max": int, "x_max": int}]
}
```

Omit keys for elements the user did not request (see **Element Selection** below).

#### 2c. Run pixelation for this image

Pass the JSON from 2b via `--bbox-json`. No API key is read or written.

```bash
BBOX='<JSON output from 2b>'
"$PYTHON" "$CHAT_PIXELATE_PATH/process.py" \
    "$IN_DIR" \
    "$OUT_DIR" \
    --bbox-json "$BBOX" \
    [OPTIONS]   # see Element Selection and Option Configuration below
```

Repeat steps 2a–2c for every image before proceeding.

### 3. Return results to user

```bash
ls "$OUT_DIR/"*_pixelated.png
```

Attach or share all processed images from `$OUT_DIR/`.

---

## Element Selection

Translate the user's intent to `--elements`. Default (no flag) pixelates all three.

| User says (EN / 中文) | `--elements` flag |
|---|---|
| all / default / 全部 / 默认 / 全部打码 | *(omit flag — default: all three)* |
| chat name only / 只隐藏聊天名称 | `--elements chat_name` |
| profile pics only / 只隐藏头像 | `--elements profile_pic` |
| display names only / 只隐藏昵称 / 只隐藏用户名 | `--elements display_name` |
| avatars and display names / 隐藏头像和昵称 | `--elements profile_pic,display_name` |
| chat name and avatars / 隐藏聊天名称和头像 | `--elements chat_name,profile_pic` |
| chat name and display names / 隐藏聊天名称和昵称 | `--elements chat_name,display_name` |

When not all three elements are requested, omit the unused keys from the
bounding-box JSON prompt in step 2 to reduce noise.

**Element definitions:**
- **chat_name**: Title text in the top navigation bar (group name, contact name, channel title)
- **profile_pic**: Circular/rounded avatar images next to message bubbles
- **display_name**: Text username/nickname labels next to or above message bubbles

---

## Option Configuration

| User says (EN / 中文) | Flag |
|---|---|
| soft blur / mist effect / 模糊效果 / 雾化（默认）| `--pixel-mode A` *(default)* |
| block / mosaic / pixelate blocks / 马赛克 / 方块效果 | `--pixel-mode B` |

---

## Full Example (copy-paste ready)

Two images processed, each with its own per-image bounding-box analysis:

```bash
# (Assumes Setup block has already run and exported CHAT_PIXELATE_PATH and PYTHON)

JOB_ID="job_$(date +%s)"
OUT_DIR="/tmp/chat_pixelate_out_$JOB_ID"
mkdir -p "$OUT_DIR"

# --- Image 1: screenshot_a.png ---
IN_A="/tmp/chat_pixelate_in_${JOB_ID}_a"
mkdir -p "$IN_A"
cp "$HOME/.openclaw/media/inbound/screenshot_a.png" "$IN_A/"
# (analyse screenshot_a.png with your vision model, capture JSON as BBOX_A)
BBOX_A='{"chat_names":[{"y_min":20,"x_min":100,"y_max":80,"x_max":900}],"profile_pics":[{"y_min":150,"x_min":10,"y_max":220,"x_max":80}],"display_names":[{"y_min":160,"x_min":90,"y_max":190,"x_max":350}]}'
"$PYTHON" "$CHAT_PIXELATE_PATH/process.py" "$IN_A" "$OUT_DIR" --bbox-json "$BBOX_A"

# --- Image 2: screenshot_b.png --- (analyse separately; elements at different positions)
IN_B="/tmp/chat_pixelate_in_${JOB_ID}_b"
mkdir -p "$IN_B"
cp "$HOME/.openclaw/media/inbound/screenshot_b.png" "$IN_B/"
# (analyse screenshot_b.png with your vision model, capture JSON as BBOX_B)
BBOX_B='{"chat_names":[{"y_min":10,"x_min":200,"y_max":70,"x_max":800}],"profile_pics":[],"display_names":[{"y_min":200,"x_min":60,"y_max":240,"x_max":400}]}'
"$PYTHON" "$CHAT_PIXELATE_PATH/process.py" "$IN_B" "$OUT_DIR" --bbox-json "$BBOX_B"

echo "=== Output images ==="
ls "$OUT_DIR/"*_pixelated.png
```

### More examples

```bash
# Only blur profile pics for one image — omit unused keys from JSON
IN_IMG="/tmp/chat_pixelate_in_${JOB_ID}_img"
mkdir -p "$IN_IMG"
cp "$HOME/.openclaw/media/inbound/chat.png" "$IN_IMG/"
BBOX='{"profile_pics":[{"y_min":150,"x_min":10,"y_max":220,"x_max":80}]}'
"$PYTHON" "$CHAT_PIXELATE_PATH/process.py" "$IN_IMG" "$OUT_DIR" \
    --elements profile_pic \
    --bbox-json "$BBOX"

# Hide chat name and display names, block mosaic style
BBOX='{"chat_names":[{"y_min":0,"x_min":100,"y_max":60,"x_max":900}],"display_names":[{"y_min":160,"x_min":90,"y_max":190,"x_max":350}]}'
"$PYTHON" "$CHAT_PIXELATE_PATH/process.py" "$IN_IMG" "$OUT_DIR" \
    --elements chat_name,display_name \
    --pixel-mode B \
    --bbox-json "$BBOX"
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `--bbox-json ... but N images were found` | Multiple images in input dir with `--bbox-json` | Use a separate `$IN_DIR` per image and run `process.py` once per image |
| `python3 -m venv` fails | Missing venv module | Run `apt-get install -y python3-venv` then re-run Setup |
| `git clone` fails | No git installed or no network | Run `apt-get install -y git` or check network connectivity |
| `No images found in input directory` | Copy step failed | Check `ls $IN_DIR/` and confirm the filename is exact |
| Image copied unchanged with `SKIPPED` in summary | JSON parse failure | Check printed warning; verify the bbox JSON is valid |
| Wrong regions pixelated | Bounding boxes were inaccurate | Re-analyse the image and adjust coordinates; try `--pixel-mode B` |
