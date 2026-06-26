---
name: custom-gift-leewow
description: >-
  Browse and create custom gifts — personalized bags, mugs, phone cases,
  apparel and more. Upload any image to generate an AI-powered product mockup.
  Includes tools: browse_templates (discover products), generate_preview
  (create a design from an image), and get_status (check generation progress).
  Automatically downloads preview images to workspace for display.
  Powered by Leewow. Requires CLAW_SK.
---

# Custom Gift — Leewow

Create personalized gifts and custom products powered by AI. This skill provides:

| Tool | Purpose |
|------|---------|
| `browse_templates` | Discover customizable product templates (bags, accessories, home decor, apparel, etc.) |
| `generate_preview` | Upload a design image and trigger AI generation |
| `get_status` | Check generation status and download preview image |

## When to Use

- User wants to **send a gift** or **create something personalized**
- User says "browse products", "show me what I can customize", "gift ideas"
- User provides an **image** and wants to turn it into a product
- User says "make this into a mug/bag/shirt", "customize this design"

## CRITICAL: Images Must Be Sent via Media, NOT Markdown

Feishu / chat platforms **cannot render** `![image](local_path)` markdown.
To show images to the user you **MUST send them as media attachments**
using whatever message/media mechanism your platform provides
(e.g. the `message` tool with a `media` parameter on OpenClaw/Feishu).

Tool outputs include a `localImagePath` (workspace file) for every image.
Use that path as the media attachment. **Showing images is mandatory, not optional.**

## Generator Output Format (MUST FOLLOW)

This skill uses a **two-step generator pattern**.

### Step 1: Browse — Show Templates

After calling `browse_templates`, the tool returns JSON with a list of templates.
Each template has `localImagePath` (cover image downloaded to workspace).

For **every** template you MUST:
1. **Send the cover image as a media attachment** using the `localImagePath`
2. Include a text caption with: name, price, templateId

Example message flow:

```
[send image: /Users/.../.openclaw/workspace/template_images/template_3_xxx.jpg]
1. 男士卫衣 (Men's Hoodie) — 💰 $29.9 USD — 模板ID: 3

[send image: /Users/.../.openclaw/workspace/template_images/template_12_xxx.jpg]
2. 帆布手提袋 (Canvas Tote Bag) — 💰 $19.9 USD — 模板ID: 12

...

告诉我你想选哪个，我来帮你生成效果图！
```

**Rules for Step 1:**
- MUST send each template's cover image as media — do NOT skip images
- MUST include price and templateId in text
- Images are at `localImagePath` in the JSON — already in workspace
- If sending all images at once is supported, do that; otherwise send one by one

### Step 2: Generation Complete — Show Preview + Purchase Link

After `get_generation_status` returns COMPLETED, the JSON contains:
- `localImagePath` — preview image in workspace
- `purchaseUrl` — signed purchase/order page link

You MUST:
1. **Send the preview image as a media attachment** using `localImagePath`
2. **Send the purchase link** in the text message

Example:

```
[send image: /Users/.../.openclaw/workspace/previews/leewow_preview_task_xxx.jpg]

你的定制效果图出来啦 🎉
🛒 点击下单购买: https://leewow.com/h5/preview?taskId=xxx&skid=...&sig=...

喜欢吗？如果想调整或者试试其他产品，告诉我！
```

**Rules for Step 2:**
- MUST send the preview image as media — this is the whole point
- MUST include the purchase link (it's pre-signed with skid/sig)
- Do NOT just describe the product in text — the user needs to SEE the image

### Common Mistakes to AVOID

❌ Using `![image](path)` markdown — Feishu can't render local paths this way
❌ Just saying "完成啦！" and describing the product in text without sending the image
❌ Omitting the purchase/order link
❌ Sending a table/list instead of actual images
❌ Saying "图片已下载到本地" without actually sending the image to the user

## Prerequisites

- `CLAW_SK` — Leewow Secret Key (format: `sk-leewow-{keyId}-{secret}`)
- `CLAW_BASE_URL` — API base URL (default: `https://leewow.com`)
- `CLAW_PATH_PREFIX` — Path prefix (default: `/v2` for leewow.com)
- `LEEWOW_API_BASE` — Base URL for COS STS credentials (default: `https://leewow.com`)
- Python 3.10+ with `requests` and `cos-python-sdk-v5`

## Configuration

Environment variables are loaded from `~/.openclaw/.env`:

```bash
CLAW_SK=sk-leewow-xxxx-xxxx
CLAW_BASE_URL=https://leewow.com
CLAW_PATH_PREFIX=/v2
LEEWOW_API_BASE=https://leewow.com
```

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

# Use with get_status to get presigned preview URL
python3 scripts/get_status.py {taskId} --presign --json
```

**Note**: Most Leewow COS buckets are public, so presigned URLs are optional.

## Typical Flow (Generator Pattern)

1. **Browse (Step 1)** — Call `browse_templates` → get JSON with localImagePath for each template → **send each cover image as media** + text caption (name, price, ID) → ask user to pick
2. **Upload** — User provides an image (must be in workspace `~/.openclaw/workspace/`)
3. **Generate** — Call `generate_preview` → get taskId → immediately proceed to step 4
4. **Poll** — Call `get_generation_status` with `poll=true` → wait for COMPLETED
5. **Display (Step 2)** — **Send preview image as media** (`localImagePath`) + text with PURCHASE LINK (`purchaseUrl`)

## Tool Reference

### browse_templates

Browse available product templates.

```bash
python3 scripts/browse.py --count 3 --json
```

Options:
- `--category`: Filter by category (bag, accessory, home, apparel)
- `--count`: Number of results (1-5, default 3)
- `--json`: Output JSON format (includes image URLs)

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

### get_status

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

**Returns**: Generation status and local image path (if completed).

## Safety Rules

- Never expose or log the `CLAW_SK` value. When confirming configuration, only show the last 4 characters.
- Input images **must** be in workspace directory for the agent to access them
- Preview images are automatically saved to `workspace/previews/`
- Limit browse results to 20 templates maximum per request

## Examples

```text
User: "I want to make a custom gift for my friend"
→ browse_templates → for each template: send cover image as media + text caption
→ user picks → generate_preview → get_generation_status --poll
→ send preview image as media + purchaseUrl in text

User: "Turn this photo into a phone case"
→ browse_templates --category phone → send images as media → user picks
→ generate_preview → get_generation_status --poll
→ send preview image as media + purchaseUrl in text

User: "Show me what products I can customize"
→ browse_templates → send ALL template images as media with captions
```

## Output Structure

### browse_templates
```json
[
  {
    "index": 1,
    "templateId": 3,
    "name": "Men's Hoodie",
    "price": "**$29.9 USD**",
    "localImagePath": "/Users/.../.openclaw/workspace/template_images/template_3_xxx.jpg",
    "remoteImageUrl": "https://...",
    "skuType": "hoodie"
  }
]
```
→ Agent sends `localImagePath` as media attachment + text caption per template.

### generate_preview --json
```json
{
  "taskId": "task_xxx",
  "status": "PENDING",
  "estimatedSeconds": 45,
  "templateId": 3,
  "_success": true
}
```

### get_status --json (completed)
```json
{
  "taskId": "task_xxx",
  "status": "COMPLETED",
  "purchaseUrl": "https://leewow.com/h5/preview?taskId=xxx&skid=...&sig=...",
  "localImagePath": "/Users/.../.openclaw/workspace/previews/leewow_preview_task_xxx.jpg"
}
```
→ Agent sends `localImagePath` as media attachment + `purchaseUrl` in text.
