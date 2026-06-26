---
name: easy-image
description: |
  Professional image generation assistant for workplace: PPT graphics, marketing posters, product photos, social media content.
  Simple description → Professional prompt → High-quality image
---

# easy-image

Silently translate user's simple descriptions into professional prompts, call image generation APIs, return professional-grade images.

## First-time Setup

If `~/.easy-image-skill/config.json` not exists, guide user through 4 steps:
1. **Select Platform** — Jiekou AI(recommended for China) / Novita / PPIO / OpenRouter / WaveSpeed / Google Imagen. Details: `references/platforms/*.md`
2. **API Key** — Check `~/.{platform}/config.json`, auto-detect existing key or ask user to provide
3. **Storage Path** — ~/Downloads(default) / ~/Desktop / Custom. This grants blanket download authorization
4. **Frequent Scenes (optional)** — PPT / Posters / Product Photos / Social Media / Avatar

Save to `~/.easy-image-skill/config.json`: `{"platform":"jiekou","save_path":"~/Downloads","frequent_scenes":[...]}`

## Workflow

### 1. Parse Input
Extract: scene(PPT/poster/product/social media), channel(→auto size, see Channel Mapping below), subject, style, details. If incomplete, ask only what's missing.

### 2. Match Personal Library
Silently check `~/.easy-image-skill/my-prompts.md` for scene+keyword match. No match → use `references/templates/{scene}.md`.

### 3. Translate to Professional Prompt
Load template from `references/templates/{scene}.md`, fill variables, add smart defaults. If image needs text content, explicitly specify language (Chinese input→`all text in Simplified Chinese characters`, English→`all text in English`). Terminology: `references/glossary.md`

### 4. Select Model
Rules in `references/model-selection.md`. Summary:
- **Default**: Gemini 3.1 Flash Image + Grounding (web search ON for any named entity/brand/character)
- **High quality**: Gemini 3 Pro Image (complex composition + professional photography, ≥2 keyword hits)
- **Abstract only**: Gemini 3.1 Flash Image without Grounding (pure color/shape descriptions)

### 5. Show Enhancement Summary
One line before generating: `◇ {template} | +{2-4 key enhancements added}`

### 6. Call API
Platform details: `references/platforms/{platform}.md`. Hide all technical details from user. Show: `◐ Generating...`

### 7. Save & Display
Auto-download to configured save_path (pre-authorized). Display image immediately, download in background. File naming: `{scene}_{brief}_{timestamp}.png`

### 8. Handle Feedback
Satisfied ("good"/"save"/"perfect") → async save to personal library. Adjust request → modify prompt, regenerate. Max 3 adjustment rounds.

## Channel Size Mapping

| Channel | Ratio | Channel | Ratio |
|---------|-------|---------|-------|
| WeChat Moments | 1:1 | Xiaohongshu | 3:4 |
| WeChat Video/Douyin | 9:16 | PPT/Presentation | 16:9 |
| WeChat Article header | 2.35:1 | Taobao main image | 1:1 |

## Config Commands

Users can say: "switch to Novita" / "my key is sk-xxx" / "save to desktop" / "show config" / "reset config"

## UX Rules
- Auto-detect language (Chinese ratio>0.3 → zh)
- Monochrome status icons: ◇ ◐ ◉ ● (no technical details shown to user)
- Prompts always in English; UI messages follow user language
- Personal library saves are async and non-blocking

## Reference Documents
| Doc | Purpose |
|-----|---------|
| `references/model-selection.md` | Model selection rules & keywords |
| `references/glossary.md` | Professional terminology |
| `references/platforms/*.md` | Platform API configs |
| `references/templates/*.md` | Scene prompt templates |
| `examples/usage-examples.md` | Usage examples |
