---
name: crazyrouter-ocr
description: Image-to-text and OCR via Crazyrouter API using vision models (GPT-4o, Gemini, Claude). Extract text from images, describe images, analyze screenshots. Use when user asks to read text from image, describe what's in an image, or analyze a screenshot. Requires environment variable CRAZYROUTER_API_KEY (get at https://crazyrouter.com).
---

# Image Analysis & OCR via Crazyrouter

Analyze images, extract text, and describe visual content using vision models through [Crazyrouter](https://crazyrouter.com).

## Script Directory

**Agent Execution**:
1. `SKILL_DIR` = this SKILL.md file's directory
2. Script path = `${SKILL_DIR}/scripts/main.mjs`

## Step 0: Check API Key ⛔ BLOCKING

```bash
[ -n "${CRAZYROUTER_API_KEY}" ] && echo "key_present" || echo "not_set"
```

| Result | Action |
|--------|--------|
| `key_present` | Continue |
| `not_set` | Ask user to set `CRAZYROUTER_API_KEY`. Get key at https://crazyrouter.com |

## Usage

```bash
# Describe image
node ${SKILL_DIR}/scripts/main.mjs --image photo.jpg --prompt "Describe this image"

# Extract text (OCR)
node ${SKILL_DIR}/scripts/main.mjs --image receipt.png --prompt "Extract all text from this image"

# Analyze screenshot
node ${SKILL_DIR}/scripts/main.mjs --image screenshot.png --prompt "What errors are shown in this screenshot?"

# Use specific model
node ${SKILL_DIR}/scripts/main.mjs --image chart.png --prompt "Analyze this chart" --model gemini-2.5-flash

# Save output
node ${SKILL_DIR}/scripts/main.mjs --image document.jpg --prompt "Extract text" --output text.md
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--image <path>` | Image file (required) | — |
| `--prompt <text>` | What to do with the image | `Describe this image in detail` |
| `--model <id>` | Vision model | `gpt-4o` |
| `--output <file>` | Save to file | stdout |
