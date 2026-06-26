---
name: designkit-ecommerce-product-kit
description: >-
  Use when users need ecommerce listing images from a product photo, including
  hero/detail images with guided multi-step input. Trigger on requests like
  listing image packs, product image sets, and amazon listing images.
version: "1.8.2"
metadata:
  openclaw:
    requires:
      env:
        - DESIGNKIT_OPENCLAW_AK
      bins:
        - bash
        - python3
    primaryEnv: DESIGNKIT_OPENCLAW_AK
    homepage: https://www.designkit.com/openClaw
---

# Designkit Ecommerce Product Kit

Conversation-first workflow: guide users through required inputs and deliver a full listing image set.

## Step-by-Step Output (Mandatory, No Merging)

- In one assistant reply, advance only one collection step:
  either ask selling points + style preference, or ask listing configuration.
  Do not include both in the same message.
- Required rhythm:
  ask selling points + style preference -> stop for user reply ->
  ask listing configuration only -> stop for user reply ->
  proceed to style generation/API calls.
- If users provide selling points, style preference, and configuration in one message,
  accept all at once, but still confirm in clearly separated points.
- Fast path:
  if configuration is already included during selling-point confirmation
  (for example "Amazon US English 1:1"), skip step 2 and proceed.

## Workflow (In Order)

1. **Product image**: if missing, ask user to upload or provide URL/path.
2. **Core selling points + style preference (Round 1, one assistant message only)**:
   after receiving product image, first generate a suggested selling-point summary from the image, then:
   - ask user to adopt/edit/replace the suggested selling points
   - ask style preference in the same round
   - do not mention platform/market/language/aspect ratio in this message
   - use user's final confirmed version as `product_info`
   - record user's style preference and prioritize matching style options later
   - only ask user to fully write selling points if AI cannot infer meaningful points
3. **Listing configuration (Round 2, one assistant message only)**:
   only after user replies to selling points (or skips), send configuration-only guidance:
   - **Platform**: Amazon, JD, 1688, Temu, TikTok Shop, AliExpress, Alibaba, etc.
   - **Market/region**: US, China, Japan, UK, Germany, Southeast Asia, etc.
   - **Language**: Chinese, English, Japanese, German, French, Korean, etc.
   - **Aspect ratio**: 1:1, 3:4, 9:16, 16:9, etc.
   Rules:
   users may skip or provide partial config. Do not repeatedly ask to complete all fields.
   Use sensible defaults for missing values.
   Before API call, restate final applied configuration in one sentence (user-specified vs defaults).
   Fast path:
   if config already provided in previous step, skip this step.
4. **Style selection (Optional, skip by default and let server auto-select)**:
   - default: skip style selection and proceed to rendering without `brand_style`
   - only run style-selection flow when user explicitly asks to choose style:
     1. `bash __SKILL_DIR__/scripts/run_ecommerce_kit.sh style_create --input-json '<with image, product_info, platform, market...>'`
     2. poll by returned `task_id`:
        `bash __SKILL_DIR__/scripts/run_ecommerce_kit.sh style_poll --input-json '{"task_id":"..."}'`
        (optionally with `max_wait_sec` / `interval_sec`)
   - if style API is used, do not invent styles. Show only API-returned options.
     Ask user to choose one, then pass the full returned structure (for example `brand_style`) without manual rewrite.
5. **Render + auto download**:
   - run `render_submit` / `render_poll` to generate final images
   - during polling, report progress based on stderr `[PROGRESS]` lines (for example "3/7 completed")
   - auto-download all final images to working directory with naming:
     `{product_name}_{index}_{label}.jpg` (`label` from `items[].label`)
   - show results in Markdown image format and report save location
   - rerun with new style:
     if user wants another style after preview, run `style_create`, let user choose, then rerun from `render_submit`

**Strict sequence constraint**:
Product image -> **selling points + style preference (round 1)** -> **user reply** ->
**listing configuration (round 2, or fast-path skip)** -> **user reply** ->
**render + auto download**.
Style selection is optional and inserted only when user explicitly asks.
