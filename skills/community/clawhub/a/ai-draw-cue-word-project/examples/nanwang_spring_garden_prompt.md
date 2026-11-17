# Example: Nanwang · Spring Garden Edition — Finished Prompts in Four Syntax Flows

> **Adult declaration (v2.9.0 safety-patch, 2026-09-01):** Nanwang depicted in this example is an **adult (18+) woman**. Do not reintroduce minor ages ("16-year-old", "teen girl", "loli", "未成年") into anchors, prompts, or logs. See `SKILL.md → Safety & Content Policy` for full rules.

> This example demonstrates assembling the complete prompt for the same character setting (**Nanwang · Plain-Dress Garden Version v1.2**, see `sheets/CharacterAnchors.csv`) across four syntax flows. Core rule: **anchor sentences are reused verbatim across images; synonym rewriting is forbidden**.

## Character Anchor Summary (quoted from `sheets/CharacterAnchors.csv`)

| Field | Value |
|---|---|
| Core identity anchor (≥1.6) | young woman (adult); faint brown 1mm mole below the left eye corner; often wears a small white daisy in the hair (1.8) |
| Core temperament tag (≥1.3) | Gentle, quiet, slightly timid, restrained body language (1.3) |
| Color scheme · primary | Light mint #A8D8C9 |
| Color scheme · secondary/accent | White (daisy, skirt-hem pattern) / faint brown (mole), light pink (lips) |
| Skin / hair / eye color | Warm white / black hair / dark brown eyes |
| Usage restrictions (negative anchoring) | No red tones / dark tones / ornate gowns |

**Scene**: spring garden · golden-hour backlight · 85mm portrait

---

## 1. Natural-language narrative flow (Flux / DALL-E 3 / SD3)

> Assembly order: [scene overview + shot scale] → [character anchors] → [posture & micro-expression] → [lighting & color] → [background layers]; weight brackets and plus signs forbidden; anchor sentences go at the start of the character block.

An 85mm portrait shot at eye level. young woman Nanwang stands deep in a spring garden. She wears a light mint cotton plain dress with delicate white daisy embroidery on the hem. Her black straight waist-length hair falls to her waist, with a single white daisy tucked in it. A tiny, faint brown mole sits below her left eye corner. She looks at the camera with a gentle, quiet expression. Golden-hour backlighting outlines warm rims of light around her hair and dress. The foreground is a blurred patch of white daisies; the background is a breezy garden wall.

Exclusion: affirmative writing first (the dress sentence naturally excludes red dresses / leather jackets) + fallback `without heavy makeup, no other hair accessories`.

## 2. Conversational image models (GPT-4o / Gemini 2.5 Flash Image)

> Give a complete description in the first round, then make conversational single-point fixes; change only single points, never the anchor sentences.

**Round 1**: young woman Nanwang, light mint cotton plain dress with white daisy embroidery, black waist-length straight hair, tiny faint brown mole below the left eye, one white daisy in the hair, spring garden, golden-hour backlight, 85mm half-body portrait.

**Fix round**: make the mole smaller and fainter; keep the dress mint green, not blue.

## 3. Mixed Tag + parameter flow (Midjourney v8.2 / Niji 7)

> Core anchors within the first 20 tokens; the mid-section stacks shot scale and lighting; append CLI parameters uniformly at the end.

```
A young woman Nanwang, faint brown mole under left eye, single white daisy in hair, light mint green plain dress, black waist-length straight hair, rule of thirds composition, 85mm portrait shot, side-backlighting, golden hour glow, spring garden, shallow depth of field --ar 3:4 --niji 7
```

`--no` filters only the 4-5 highest-risk words: `--no heavy makeup, red dress, short hair, dark lighting`

> ⚠️ `--cref` / `--cw` have been removed above v6 — they are dead on v7/v8. Use `--oref`/`--ow` on v7 or the v8 Edit Model (`--edit` / attach up to 4 references on the web). `--niji 7` must be written explicitly because Niji has no V8 counterpart: without it the V8.2 default renders the anime request instead.

## 4. Weighted Tag flow (Stable Diffusion 1.5 / XL / SD3)

> Assembly order (v2.2): identity anchors (1.5+) → core features (1.3-1.5) → posture/composition → lighting/atmosphere (0.7-0.9).

```
(young woman Nanwang:1.2), (mole under left eye:1.5), (single white daisy in hair:1.3), (light mint green plain dress:1.4), (black waist-length straight hair:1.2), rule of thirds, 85mm portrait shot, side-backlighting, golden hour, spring garden, soft bokeh, masterwork, high quality
```

Negative Prompt box: `(deformed hands, bad anatomy, extra fingers, missing fingers:1.4), (mole under right eye, heavy makeup, red dress, short hair:1.3), (blurry, low quality, watermark, text:1.2)`

---

## Exclusion mechanism quick reference

| Syntax flow | Exclusion method |
|---|---|
| Natural-language flow | Affirmative writing first; negation as fallback |
| Conversational | No negative-word concept; exclude directly in conversation |
| MJ | `--no` filters only the highest-risk words; the rest is covered by the reference method (`--oref` on v7 / Edit Model on v8) and the positive description |
| SD | Fill the separate Negative Prompt box |
