---
name: Beauty Karma
description: Analyze an uploaded portrait photo with MiniMax-M3 and generate a playful, shareable camera-presence report with a 1-10 lens score, positive visual highlights, practical photo tips, social captions, and a report-card image. Use for selfie feedback, profile-photo selection, portrait presentation, content creation, mini-program sharing, and light entertainment decisions.
version: 1.0.3
---

# Beauty Karma

## Overview

Beauty Karma turns an uploaded portrait photo into a playful camera-presence report. It uses `MiniMax-M3` to analyze photo presentation factors such as lighting, composition, expression, clarity, atmosphere, and shareability. The skill returns a 1-10 lens score, a positive status label, short highlights, practical improvement tips, social-ready title/caption text, and a shareable report-card page.

Use cases:

- Generate a fun camera-presence report from a selfie, avatar, or portrait photo.
- Help choose or improve a profile photo.
- Create interactive social content and shareable mini-program cards.
- Provide lightweight, friendly, non-professional photo presentation feedback.

## Quick Start

Create a JSON request file:

```json
{
  "imagePath": "/absolute/path/to/photo.jpg",
  "userLabel": "Beauty Karma",
  "outputDir": "output/demo"
}
```

Run:

```bash
MINIMAX_API_KEY=your_key node scripts/run-skill.js request.json
```

Generated files:

- `analysis.json`: structured lens score and copy.
- `yan-zhi-report.html`: report-card page that can export a PNG.
- `yan-zhi-report.svg`: static fallback preview.

## Inputs

- `imagePath`: local portrait photo path, absolute or relative to the skill folder.
- `imageUrl`: remote portrait photo URL.
- `imageBase64`: base64 image content, with or without a `data:image/...;base64,` prefix.
- `imageNotes`: optional visual notes used only if the configured MiniMax endpoint rejects image input.
- `userLabel`: optional footer label for the report card.
- `outputDir`: optional output directory.
- `mock`: optional; set to `true` for local demos without calling the model.

## Model And Configuration

- Model: `MiniMax-M3`.
- Real analysis requires `MINIMAX_API_KEY`.
- Default endpoint: `https://api.minimax.io/v1`.
- Override with `MINIMAX_BASE_URL` if needed.

## Safety Boundaries

The lens score is for entertainment and content creation only. It is not a measure of personal worth, scientific quality, or professional evaluation. Do not infer identity, age, ethnicity, health, wealth, or other sensitive attributes. Do not produce insults, degrading language, or appearance-value judgments. If the input is not a portrait or cannot be analyzed, ask for a clearer portrait photo.
