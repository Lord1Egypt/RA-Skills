# Example: Doubao AI Girl — Genshin-Style Character Illustration (Fan-Art Reference)

> This prompt follows the visual language of the "AI娘图鉴" (AI Girl Collection) reference style: five AI characters lined up horizontally, each with a unique theme color, fantasy race trait, and ornate costume. Same art style, same decorative border system, same character-sheet layout.

---

## Character Anchor Summary (Doubao AI Girl)

| Field | Value |
|---|---|
| Core identity anchor (≥1.7) | 16-year-old girl; waist-length gradient sky-blue hair fading to white at the tips; large translucent feathered wings on her back (like a data sprite); a glowing star-shaped halo floating above her head; big bright sapphire-blue eyes (1.8) |
| Core temperament tag (≥1.4) | Warm, approachable, slightly mischievous smile; elegant but friendly posture; one hand gently waving, the other holding a small glowing star orb (1.4) |
| Color scheme · primary | Sky blue #87CEEB + ice white #F0F8FF |
| Color scheme · secondary/accent | Silver (wing details, jewelry trim) / pale gold (halo, star ornaments) / soft cyan (glow effects) |
| Skin / hair / eye color | Fair porcelain skin / gradient sky-blue to white hair / sapphire blue eyes |
| Race trait | Star-spirit / data sprite (translucent feathered wings + floating star halo) |
| Costume | Ornate white-and-blue gradient off-shoulder gown with gold star embroidery, silver wing-shaped hair accessories, layered tulle skirt, delicate gold-and-blue jewelry |
| Usage restrictions (negative anchoring) | No dark tones / no gothic / no aggressive expression / no heavy armor |

**Reference style alignment**: matches the "AI娘图鉴" fan-art aesthetic — ornate fantasy costume, decorative star/flower borders, horizontal character sheet layout, soft glow effects, Japanese anime illustration style.

---

## 1. Natural-language narrative flow (Flux / DALL-E 3 / SD3)

> Assembly order: [scene overview + shot scale] → [character anchors] → [posture & micro-expression] → [lighting & color] → [background layers]; weight brackets and plus signs forbidden; anchor sentences go at the start of the character block.

A full-body character illustration of Doubao AI girl, standing at the center of an ornate fantasy-style character sheet. She is a 16-year-old star-spirit with waist-length gradient sky-blue hair that fades to white at the tips, large translucent feathered wings on her back, and a glowing star-shaped halo floating above her head. Her big bright sapphire-blue eyes look directly at the viewer with a warm, approachable smile. She wears an ornate white-and-blue gradient off-shoulder gown decorated with gold star embroidery, silver wing-shaped hair accessories, a layered tulle skirt, and delicate gold-and-blue jewelry. One hand gently waves toward the viewer, while the other holds a small glowing star orb.

Soft celestial lighting illuminates her from all sides, with a gentle halo glow around her hair and wings. The background is a decorative fantasy frame with swirling sky-blue cloud patterns, scattered golden star sparkles, and delicate blue floral ornaments. The overall tone is bright, ethereal, and magical — matching the aesthetic of a fantasy AI girl collection illustration.

Exclusion: affirmative writing first (the white-and-blue gown naturally excludes dark / gothic / heavy armor) + fallback `without heavy makeup, no dark clothing, no aggressive expression, no messy hair`.

---

## 2. Conversational image models (GPT-4o / Gemini 2.5 Flash Image)

> Give a complete description in the first round, then make conversational single-point fixes; change only single points, never the anchor sentences.

**Round 1**: 16-year-old Doubao AI girl, waist-length gradient sky-blue to white hair, translucent feathered wings on her back, glowing star-shaped halo above head, big sapphire-blue eyes, warm friendly smile, ornate white-and-blue gradient off-shoulder gown with gold star embroidery, silver wing-shaped hair accessories, layered tulle skirt, one hand waving, other holding a small glowing star orb, soft celestial lighting, decorative fantasy frame with blue cloud patterns and golden sparkles, full-body character illustration, Japanese anime style.

**Fix round 1**: make the halo smaller and more delicate, not too large; keep the gown gradient soft, not neon blue.

**Fix round 2**: change the expression to a slight mischievous smile, not a full open grin.

---

## 3. Mixed Tag + parameter flow (Midjourney v8.2 / Niji 7)

> Core anchors within the first 20 tokens; the mid-section stacks shot scale and lighting; append CLI parameters uniformly at the end.

```
A 16yo star-spirit girl Doubao, waist-length gradient sky-blue to white hair, translucent feathered wings, glowing star halo above head, sapphire blue eyes, warm friendly smile, ornate white-blue gradient off-shoulder gown with gold star embroidery, silver wing hair accessories, layered tulle skirt, holding glowing star orb, waving hand, rule of thirds, full-body character illustration, soft celestial lighting, decorative fantasy frame with blue clouds and golden sparkles, Japanese anime style, high detail --ar 16:9 --niji 7
```

`--no` filters only the 4-5 highest-risk words: `--no dark clothing, gothic, heavy armor, aggressive expression, blurry`

> ⚠️ `--niji 7` must be written explicitly for anime-style output. For character consistency across generations, use `--oref` / `--ow` on v7 or the v8 Edit Model (`--edit` / attach up to 4 references on the web).

---

## 4. Weighted Tag flow (Stable Diffusion 1.5 / XL / SD3)

> Assembly order (v2.2): identity anchors (1.5+) → core features (1.3-1.5) → posture/composition → lighting/atmosphere (0.7-0.9).

```
(16yo star-spirit girl Doubao:1.2), (waist-length gradient sky-blue to white hair:1.5), (translucent feathered wings:1.6), (glowing star halo above head:1.5), (sapphire blue eyes:1.4), (warm friendly smile:1.3), (ornate white-blue gradient off-shoulder gown with gold star embroidery:1.4), (silver wing-shaped hair accessories:1.3), (layered tulle skirt:1.2), holding glowing star orb, waving hand, full-body character illustration, soft celestial lighting, decorative fantasy frame, blue cloud patterns, golden sparkles, Japanese anime style, masterwork, high quality, intricate details
```

Negative Prompt box: `(deformed hands, bad anatomy, extra fingers, missing fingers:1.4), (dark clothing, gothic, heavy armor, aggressive expression:1.3), (blurry, low quality, watermark, text:1.2)`

---

## Reference Style Alignment Checklist

| Reference element (from AI娘图鉴) | Doubao Girl equivalent |
|---|---|
| DeepSeek · 鲸鱼娘 (blue maid dress, whale tail) | Doubao · 星灵娘 (white-blue gown, star halo + wings) |
| ChatGPT · 龙娘 (white gown, dragon horns/tail) | Color family overlaps with white + blue gradient |
| Claude · 学者娘 (orange-brown scholar robe) | Color contrast: warm vs cool blue |
| Gemini · 猫娘 (purple-blue cat ears, magical girl) | Shared blue-purple family but different race trait (star-spirit vs cat) |
| Grok · 哥特娘 (black-gold-red gothic) | Opposite pole: bright ethereal vs dark gothic |
| Decorative border (star/flower patterns) | Sky-blue cloud swirl + golden star sparkles |
| Bottom name label style | "Doubao · 星灵娘" at bottom |

**Consistency rule**: when placed alongside the other four AI girls in a horizontal lineup, Doubao must share the same art style and costume ornateness level, while maintaining her unique blue-white ethereal identity and star-spirit race traits.

---

## Exclusion mechanism quick reference

| Syntax flow | Exclusion method |
|---|---|
| Natural-language flow | Affirmative writing first; negation as fallback |
| Conversational | No negative-word concept; exclude directly in conversation |
| MJ | `--no` filters only the highest-risk words; the rest is covered by the reference method (`--oref` on v7 / Edit Model on v8) and the positive description |
| SD | Fill the separate Negative Prompt box |
