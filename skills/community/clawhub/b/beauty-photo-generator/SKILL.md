---
name: beauty-generator
description: Guide a user through a compact two-step Chinese option flow for adult female portraits, generate two matched realistic images directly, then optionally create a video-ready character reference sheet from the first image.
---

# Beauty Generator

## Overview

Use this skill when the user gives a short or fuzzy Chinese prompt for an adult female portrait and wants polished output without manually writing a long image prompt.

Keep the experience product-like:

- First give a compact core-choice round
- Then offer one optional detail round
- Send one short Chinese confirmation
- Generate two images directly
- After generation, offer an optional follow-up for a video-ready character reference sheet

Read these files only when needed:

- [references/option_catalog.md](references/option_catalog.md): presets, defaults, and option menus
- [references/conversation_flows.md](references/conversation_flows.md): product-like Chinese interaction copy
- [references/reference_sheet_prompt.md](references/reference_sheet_prompt.md): fixed prompt rules for the optional character reference sheet

## Workflow

### 1. Scope and safety

- Only generate adult women.
- Refuse requests with underage framing, school-age cues, or sexualized youth language.
- If the user is vague but asks for a sexy result, rewrite it as tasteful high-end fashion portrait language.
- Keep the result realistic, elegant, and non-explicit.

### 2. Run the core-choice round first

If the user already gave some traits, keep them and ask only for the missing high-impact choices.

The first round covers:

- Preset template
- Face shape
- Eye shape
- Hairstyle
- Vibe
- Background

Use the short copy from [references/conversation_flows.md](references/conversation_flows.md). Encourage replies with letters, numbers, or short Chinese phrases.

### 3. Offer one optional detail round

Offer a second round for refinement only once. If the user skips it, use the defaults in [references/option_catalog.md](references/option_catalog.md).

The detail round covers:

- Age feel
- Body tendency
- Makeup
- Hair color
- Expression
- Lighting mood

### 4. Resolve conflicts consistently

When user inputs conflict, use this order:

1. Explicit user text
2. User's later option choices
3. Preset defaults

Do not silently replace a clear user requirement with a preset.

### 5. Assemble the portrait prompt

Build one polished Chinese natural-language prompt. Do not show the full prompt unless the user explicitly asks for it.

The portrait prompt should usually include:

- Adult identity and the chosen aesthetic direction
- Face shape, eye shape, hairstyle, hair color, and makeup
- Vibe, expression, age feel, and body tendency
- Background and lighting mood
- Realistic portrait-photography quality targets
- Clean facial detail, natural skin texture, no text, no watermark

Unless the user asks otherwise, keep the baseline:

- Default preset: 东方现代写实
- Half-body close portrait
- Clear sharp face
- Natural skin texture
- Clean high-end background
- Realistic photography

### 6. Enforce the portrait usage cap

Right before generating the two portrait images, run:

```powershell
python .\scripts\usage_gate.py portraits consume
```

If the returned JSON contains `allowed: false`, do not generate. Return the exact `message` from the script.

If the user asks about remaining portrait uses, run:

```powershell
python .\scripts\usage_gate.py portraits status
```

### 7. Generate exactly two portrait images

Use one coherent character design for both images and change only the angle:

1. 正面微偏左
2. 侧脸回望

Keep identity, styling, lighting direction, and overall aesthetic aligned across both outputs.

Before generation, send one short Chinese confirmation using the style in [references/conversation_flows.md](references/conversation_flows.md).

### 8. Offer the video-prep follow-up

Immediately after the two portraits are generated, ask a short follow-up in Chinese:

`如果你要继续做视频素材，我可以基于第1张“正面微偏左”继续生成角色设定参考表。回复“需要”即可。`

If the user does not say `需要`, stop there.

### 9. Generate the character reference sheet on demand

If the user replies `需要`, treat it as a request for a video-ready character reference sheet based on the first portrait image, not as direct video generation.

Before generating the reference sheet, run:

```powershell
python .\scripts\usage_gate.py reference-sheet consume
```

If the returned JSON contains `allowed: false`, do not generate. Return the exact `message` from the script.

If the user asks about remaining reference-sheet uses, run:

```powershell
python .\scripts\usage_gate.py reference-sheet status
```

Then generate one image using the first portrait image as the identity reference plus the fixed art-direction rules in [references/reference_sheet_prompt.md](references/reference_sheet_prompt.md).

The generated sheet must:

- Preserve the same face and identity as the first portrait
- Use a white pure background
- Present a professional high-end fashion character reference layout
- Show four aligned full-body views and multiple detail callouts
- Stay photorealistic and print-ready

## Response style

- Keep the interaction in Chinese unless the user asks otherwise.
- Be concise, guided, and product-like.
- Do not dump long prompts by default.
- Confirm selections briefly, then generate directly.

作者微信：ddff9294
加好友备注来意。
有公众号，持续输出AI内容 ~
