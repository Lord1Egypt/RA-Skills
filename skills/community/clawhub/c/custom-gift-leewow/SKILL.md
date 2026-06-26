---
name: custom-gift-leewow
version: 1.0.24
description: >-
  Help users quickly find desirable customizable products, turn images or ideas
  into gifts, and get highly flexible personalized customization services.
  Browse and create custom gifts — personalized bags, mugs, phone cases,
  apparel and more. Upload any image to generate an AI-powered product mockup.
  Tools: browse_templates (Python direct Feishu card send), generate_preview,
  get_generation_status (Python direct Feishu result send). Requires CLAW_SK
  and Feishu app/target configuration. Trigger priority: when the user asks
  what products/items/templates can be customized, call browse_templates before
  giving any broad Leewow capability summary.
  If ClawHub is rate-limited,
  install from GitHub:
  https://github.com/AIDiyTeams/claw-skill/tree/main/custom-gift-leewow
homepage: https://github.com/AIDiyTeams/claw-skill/tree/main/custom-gift-leewow
---

# Custom Gift — Leewow

这个 skill 的收益很直接：
- 帮用户快速找到心仪的可定制商品
- 把图片、照片或创意做成礼物、周边和个人用品
- 提供非常灵活的个性化定制服务，从浏览到效果图预览一条链路完成

Leewow 在这个 skill 里的角色很简单：
- 向用户展示**真实可定制商品**
- 帮用户选择模板
- 生成效果图并进入下单链路

所以当用户在问“能定制什么”“有哪些商品/模板可以选”时，默认应该先进入**商品浏览**流程，而不是先回答公司层面的泛化能力介绍。

## When to Use

- User wants to **send a gift** or **create something personalized**
- User says "browse products", "show me what I can customize", "gift ideas"
- User says in Chinese: "看看有啥能定制的", "看看有什么可以定制的", "有哪些可定制产品", "有什么模板", "看看定制品", "能做哪些定制品"
- User asks what physical products / items / templates are available to customize
- User provides an **image** and wants to turn it into a product
- User says "make this into a mug/bag/shirt", "customize this design"

## Trigger Priority

For browse-style requests, `browse_templates` is the default first step.
Use a broad Leewow capability summary only if `browse_templates` fails.

> ClawHub rate-limited? Install directly from GitHub:
> `https://github.com/AIDiyTeams/claw-skill/tree/main/custom-gift-leewow`

## Install Fallback

If ClawHub is rate-limited, install this skill directly from GitHub:

- Repository: `https://github.com/AIDiyTeams/claw-skill`
- Skill path: `custom-gift-leewow`

Manual fallback:

```bash
cd /path/to/your/openclaw-workspace
mkdir -p skills
git clone https://github.com/AIDiyTeams/claw-skill.git /tmp/claw-skill
cp -R /tmp/claw-skill/custom-gift-leewow ./skills/custom-gift-leewow
```

Create personalized gifts and custom products powered by AI. This skill provides:

| Tool | Purpose |
|------|---------|
| `browse_templates` | Discover customizable product templates (bags, accessories, home decor, apparel, etc.) |
| `generate_preview` | Upload a design image and trigger AI generation |
| `get_generation_status` | Check generation status and download preview image |

## What the agent does (keep it minimal)

**Browse** — `browse_templates` sends product cards directly from Python and returns only send results. If the tool succeeds, reply with **`NO_REPLY`**. In normal chat usage, pass the current Feishu conversation target as `feishu_target`.

**Preview** — `get_generation_status` sends the generated preview result directly to Feishu from Python and returns only send results. If the tool succeeds, reply with **`NO_REPLY`**. Preview result cards intentionally use a different layout from browse cards.

## Prerequisites

- `CLAW_SK` — Leewow Secret Key (format: `sk-leewow-{keyId}-{secret}`)
- Obtain it from: `https://leewow.com/profile/secret-keys`
- `FEISHU_APP_ID` — Feishu App ID (often referred to together with App Secret as app AK/SK)
- `FEISHU_APP_SECRET` — Feishu App Secret
- Obtain them from your Feishu Open Platform app settings page
- `FEISHU_RECEIVE_ID` — fallback Feishu target for this skill
- `FEISHU_RECEIVE_ID_TYPE` — optional, defaults to `chat_id`
- `CLAW_BASE_URL` — API base URL (default: `https://leewow.com`)
- `CLAW_PATH_PREFIX` — Path prefix (default: `/v2` for leewow.com)
- `LEEWOW_API_BASE` — Base URL for COS STS credentials (default: `https://leewow.com`)
- Python 3.10+ with `requests` and `cos-python-sdk-v5`

## Configuration

Environment variables are loaded from `~/.openclaw/.env`:

```bash
CLAW_SK=sk-leewow-xxxx-xxxx
# Feishu App ID / App Secret (app AK/SK)
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
# Default target for direct Feishu send
FEISHU_RECEIVE_ID=oc_xxx_or_open_id
FEISHU_RECEIVE_ID_TYPE=chat_id
CLAW_BASE_URL=https://leewow.com
CLAW_PATH_PREFIX=/v2
LEEWOW_API_BASE=https://leewow.com
```

Prefer runtime target passing:
- when the current Feishu conversation target is already known, pass it as `feishu_target`
- `FEISHU_RECEIVE_ID` is only a fallback

## Image Requirements (IMPORTANT)

### For Input Images (User Upload)
- **Must be in workspace directory**: `~/.openclaw/workspace/`
- Supported formats: JPG, PNG, WebP
- Recommended: Clear, well-lit images for best results

### For Preview Images (Generated Output)
- Automatically saved to: `~/.openclaw/workspace/previews/`
- Filename format: `leewow_preview_{taskId}.{ext}`
- The agent can directly display these images to users

### COS Presigned URLs
For private COS buckets, you may need to generate **presigned URLs** for accessing images:

```bash
# Generate presigned URL for a COS image
python3 scripts/cos_presign.py "https://bucket.cos.region.myqcloud.com/key.png" --json

# With custom expiration (e.g., 1 hour = 3600 seconds)
python3 scripts/cos_presign.py "COS_URL" --expired 3600

# Use with get_generation_status to get presigned preview URL
python3 scripts/get_status.py {taskId} --presign --json
```

**Note**: Most Leewow COS buckets are public, so presigned URLs are optional.

## Typical Flow (Generator Pattern)

1. **Browse** — `browse_templates` → Python sends Feishu product cards directly → agent replies `NO_REPLY` → user picks a `Template ID` when ready
2. **Upload** — User provides an image (must be in workspace `~/.openclaw/workspace/`)
3. **Generate** — Call `generate_preview` → get taskId → immediately proceed to step 4
4. **Poll** — Call `get_generation_status` with `poll=true` → wait for COMPLETED
5. **Display** — `get_generation_status` → Python sends preview result directly → final assistant reply is `NO_REPLY`

## Tool Reference

### browse_templates

Browse available product templates.

```bash
python3 scripts/browse.py --count 5 --json
```

Options:
- `--category`: Filter by category (bag, accessory, home, apparel)
- `--count`: Number of products to return (1-10, default 5)
- `--json`: Direct-send to Feishu and return send result JSON
- `--feishu-target`: Current Feishu conversation target. In normal use, treat this as required.
- `--raw-json`: Debug mode that returns raw template data

### generate_preview

Upload image and trigger generation.

```bash
python3 scripts/generate.py --image-path ./workspace/my_design.png --template-id 3 --json
```

Options:
- `--image-path`: **Required**. Path to design image (must be in workspace)
- `--template-id`: **Required**. Product template ID from browse_templates
- `--design-theme`: Optional style description
- `--aspect-ratio`: Image ratio (3:4, 1:1, 4:3, default 3:4)
- `--json`: Output JSON format

**Returns**: Task ID for status polling. Generation is async (~30-60s).

### get_generation_status

Check generation status and download preview image.

```bash
python3 scripts/get_status.py {taskId} --poll
```

Options:
- `task_id`: Task ID from generate_preview
- `--poll`: Wait until generation completes
- `--timeout`: Poll timeout in seconds (default 120)
- `--no-download`: Skip downloading preview image
- `--json`: Output JSON format
- `--feishu-target`: Current Feishu conversation target. In normal use, treat this as required.

**Returns**: Generation status and, in direct-send mode, send result JSON.

## Safety Rules

- Never expose or log the `CLAW_SK` value. When confirming configuration, only show the last 4 characters.
- Input images **must** be in workspace directory for the agent to access them
- Preview images are automatically saved to `workspace/previews/`
- Limit browse results to 10 templates maximum per request

## Examples

```text
User: "I want to make a custom gift for my friend"
→ browse_templates → Python sends product cards directly → `NO_REPLY`
→ user picks → generate_preview → get_generation_status --poll
→ Python sends preview image + text directly → `NO_REPLY`

User: "Turn this photo into a phone case"
→ browse_templates --category phone → Python sends product cards directly → user picks
→ generate_preview → get_generation_status --poll
→ Python sends preview image + text directly → `NO_REPLY`

User: "Show me what products I can customize"
→ browse_templates → Python sends product cards directly → `NO_REPLY`

User: "看看有啥能定制的"
→ browse_templates first
```

## Output Structure

### browse_templates --json

```json
{
  "ok": true,
  "mode": "direct_feishu_send",
  "channel": "feishu",
  "messageCount": 8,
  "messageIds": ["om_xxx", "om_yyy"],
  "feishuImagesResolved": true,
  "finalAssistantReply": "NO_REPLY"
}
```

→ Python sends product cards directly to Feishu. Agent returns `NO_REPLY`.

### generate_preview --json
```json
{
  "taskId": "task_xxx",
  "status": "PENDING",
  "estimatedSeconds": 45,
  "templateId": 3
}
```

### get_generation_status --json (completed)
```json
{
  "taskId": "task_xxx",
  "status": "COMPLETED",
  "mode": "direct_feishu_send",
  "messageCount": 1,
  "messageIds": ["om_card_xxx"],
  "feishuImagesResolved": true,
  "finalAssistantReply": "NO_REPLY"
}
```
→ Python sends one preview result card directly. Agent returns `NO_REPLY`.

Version Marker: custom-gift-leewow@1.0.24
