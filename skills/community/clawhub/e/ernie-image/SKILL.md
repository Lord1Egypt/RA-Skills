---
name: ERNIE-Image
description: Generate images with ERNIE-Image. Use for image create requests incl. edits. Supports text-to-image ; - 1024x1024/1376x768/1264x848/ 1200x896/896x1200/848x1264/768x1376; use --input-image.
---

# ERNIE-ImageImage Generation & Editing

Generate new images or edit existing ones using Baidu's ERNIE-Image API.

## Prerequisites

- Clawdbot installed and configured

- Need Install python openai sdk: pip instsall openai

## API Key

The script checks for API key in this order:
-  1.API key from https://aistudio.baidu.com/account/accessToken
- 2.`ERNIE-Image_API_KEY` environment variable
- 3.`--api-key` argument (use if user provided key in chat)

## Usage

Run the script using absolute path (do NOT cd to skill directory first):

**Generate new image:**
```bash
python ~/.codex/skills/ERNIE-Image/scripts/generate_image.py --prompt "your image description" --filename "output-name.png" [--resolution 1024*1024|1366*768] [--api-key KEY]
```

**Important:** Always run from the user's current working directory so images are saved where the user is working, not in the skill directory.

## Resolution Options

ERNIE-Image API supports three resolutions (uppercase K required):

- 1024x1024
- 1376x768
- 1264x848
- 1200x896
- 896x1200
- 848x1264
- 768x1376

Map user requests to API parameters:
- No mention of resolution → `1024x1024`
- "low resolution", 1024x1024



If neither is available, the script exits with an error message.

## Preflight + Common Failures (fast fixes)

- Preflight:
  - `test -n \"$ERNIE-Image_API_KEY\"` (or pass `--api-key`)
  - If editing: `test -f \"path/to/input.png\"`
  
- Common failures:
  - `Error: No API key provided.` → set `ERNIE-Image_API_KEY` or pass `--api-key`
  - “quota/permission/403” style API errors → wrong key, no access, or quota exceeded; try a different key/account

## Filename Generation

Generate filenames with the pattern: `yyyy-mm-dd-hh-mm-ss-name.png`

**Format:** `{timestamp}-{descriptive-name}.png`
- Timestamp: Current date/time in format `yyyy-mm-dd-hh-mm-ss` (24-hour format)
- Name: Descriptive lowercase text with hyphens
- Keep the descriptive part concise (1-5 words typically)
- Use context from user's prompt or conversation
- If unclear, use random identifier (e.g., `x9k2`, `a7b3`)

Examples:
- Prompt "A serene Japanese garden" → `2025-11-23-14-23-05-japanese-garden.png`
- Prompt "sunset over mountains" → `2025-11-23-15-30-12-sunset-mountains.png`
- Prompt "create an image of a robot" → `2025-11-23-16-45-33-robot.png`
- Unclear context → `2025-11-23-17-12-48-x9k2.png`



## Prompt Handling

**For generation:** Pass user's image description as-is to `--prompt`. Only rework if clearly insufficient.

Preserve user's creative intent in both cases.

## Prompt Templates (high hit-rate)

Use templates when the user is vague or when edits must be precise.

- Generation template:
  - “Create an image of: <subject>. Style: <style>. Composition: <camera/shot>. Lighting: <lighting>. Background: <background>. Color palette: <palette>. Avoid: <list>.”

  

## Output

- Saves PNG to current directory (or specified path if filename includes directory)
- Script outputs the full path to the generated image
- **Do not read the image back** - just inform the user of the saved path

## Examples

**Generate new image:**
```bash
python ~/.codex/skills/ERNIE-Image/scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2025-11-23-14-23-05-japanese-garden.png" --resolution 1024*1024
```

#  References
- [https://aistudio.baidu.com/blog/detail/794723628346373](https://aistudio.baidu.com/blog/detail/794723628346373)
- [https://aistudio.baidu.com/ernieimage](https://aistudio.baidu.com/ernieimage)
- [https://aistudio.baidu.com/modelsdetail/46030/intro](https://aistudio.baidu.com/modelsdetail/46030/intro)
- 