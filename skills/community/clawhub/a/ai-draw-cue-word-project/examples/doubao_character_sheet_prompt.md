# Example: Doubao Character Sheet — Two Versions, Four Syntax Flows

> This example demonstrates assembling complete prompts for the Doubao character franchise across two versions (**Girl Version v1.0** and **Mature Version v1.0**), using the same four-syntax-flow rule as `nanwang_spring_garden_prompt.md`. Core rule: **anchor sentences are reused verbatim across images; synonym rewriting is forbidden**.

---

## Character Anchor Summary

### Version A · Doubao Girl (16yo · Bright)

| Field | Value |
|---|---|
| Core identity anchor (≥1.6) | 16-year-old girl; shoulder-length sky-blue bob with subtle inner highlights; bright cerulean eyes; small white glowing hairclip shaped like a circuit node (1.8) |
| Core temperament tag (≥1.3) | Energetic, curious, slightly mischievous; open smiling expression; relaxed posture (1.3) |
| Color scheme · primary | Sky blue #87CEEB |
| Color scheme · secondary/accent | White (hairclip, blouse trim) / pale lavender (inner highlights) / cyan (glow accents) |
| Skin / hair / eye color | Fair porcelain skin / sky-blue hair / cerulean blue eyes |
| Usage restrictions (negative anchoring) | No dark tones / gothic / heavy makeup / sharp expressions |

**Default scene**: modern tech campus · soft daylight · 50mm half-body portrait

### Version B · Doubao Mature (25yo · Executive)

| Field | Value |
|---|---|
| Core identity anchor (≥1.6) | 25-year-old woman; long straight midnight-blue hair falling to mid-back; sharp sapphire eyes; thin silver chain earring on left ear; minimal silver wristband with subtle blue LED pulse (1.8) |
| Core temperament tag (≥1.3) | Calm, composed, authoritative; slight restrained smirk; upright posture with controlled confidence (1.3) |
| Color scheme · primary | Midnight navy #1A3A5C |
| Color scheme · secondary/accent | Silver (earring, wristband) / white (blouse) / electric blue (LED glow, eye reflection) |
| Skin / hair / eye color | Cool fair skin / deep navy-blue hair / sapphire blue eyes |
| Usage restrictions (negative anchoring) | No bright colors / cute / loose clothing / messy hair |

**Default scene**: high-rise office floor-to-ceiling window · dusk cityscape · 85mm half-body portrait

---

## Version A · Doubao Girl

### 1. Natural-language narrative flow (Flux / DALL-E 3 / SD3)

> Assembly order: [scene overview + shot scale] → [character anchors] → [posture & micro-expression] → [lighting & color] → [background layers]; weight brackets and plus signs forbidden; anchor sentences go at the start of the character block.

A 50mm half-body portrait shot at eye level. 16-year-old Doubao-girl stands on a modern tech campus walkway. She wears an oversized white hoodie with thin sky-blue circuit-line piping along the cuffs and hem. Her shoulder-length sky-blue bob hair has subtle pale lavender inner highlights, with a small white glowing hairclip shaped like a circuit node tucked on the right side. Her bright cerulean eyes look directly at the camera with an energetic, curious smile. Soft midday daylight illuminates her from the front-left, catching the edges of her hair and the faint glow of the hairclip. The background is a blurred glass-and-steel campus building with green trees along the walkway.

Exclusion: affirmative writing first (the hoodie sentence naturally excludes dresses / leather jackets) + fallback `without heavy makeup, no other hair accessories, no dark clothing`.

### 2. Conversational image models (GPT-4o / Gemini 2.5 Flash Image)

> Give a complete description in the first round, then make conversational single-point fixes; change only single points, never the anchor sentences.

**Round 1**: 16-year-old Doubao girl, sky-blue shoulder-length bob with pale lavender inner highlights, small white glowing circuit-node hairclip on the right, bright cerulean eyes, white oversized hoodie with sky-blue circuit-line piping, modern tech campus, soft midday daylight, 50mm half-body portrait.

**Fix round 1**: make the hairclip glow softer, not neon; keep the hoodie white, not cream.

**Fix round 2**: change the expression to a slight mischievous smirk, not a full open smile.

### 3. Mixed Tag + parameter flow (Midjourney v8.2 / Niji 7)

> Core anchors within the first 20 tokens; the mid-section stacks shot scale and lighting; append CLI parameters uniformly at the end.

```
A 16yo girl Doubao, sky blue shoulder-length bob, pale lavender inner highlights, glowing circuit-node hairclip, cerulean eyes, white oversized hoodie with blue circuit piping, rule of thirds composition, 50mm half-body portrait, soft midday daylight, modern tech campus, shallow depth of field --ar 3:4 --niji 7
```

`--no` filters only the 4-5 highest-risk words: `--no heavy makeup, dark clothing, long hair, gothic, blurry`

> ⚠️ `--niji 7` must be written explicitly because Niji has no V8 counterpart: without it the V8.2 default renders the anime request instead. For character consistency across generations, use `--oref` / `--ow` on v7 or the v8 Edit Model (`--edit` / attach up to 4 references on the web).

### 4. Weighted Tag flow (Stable Diffusion 1.5 / XL / SD3)

> Assembly order (v2.2): identity anchors (1.5+) → core features (1.3-1.5) → posture/composition → lighting/atmosphere (0.7-0.9).

```
(16yo girl Doubao:1.2), (sky blue shoulder-length bob:1.4), (pale lavender inner highlights:1.3), (glowing circuit-node hairclip:1.5), (cerulean blue eyes:1.4), (white oversized hoodie with blue circuit piping:1.3), energetic curious smile, rule of thirds, 50mm half-body portrait, soft midday daylight, modern tech campus, soft bokeh, masterwork, high quality
```

Negative Prompt box: `(deformed hands, bad anatomy, extra fingers, missing fingers:1.4), (dark clothing, long hair, heavy makeup, gothic:1.3), (blurry, low quality, watermark, text:1.2)`

---

## Version B · Doubao Mature

### 1. Natural-language narrative flow (Flux / DALL-E 3 / SD3)

> Assembly order: [scene overview + shot scale] → [character anchors] → [posture & micro-expression] → [lighting & color] → [background layers]; weight brackets and plus signs forbidden; anchor sentences go at the start of the character block.

An 85mm half-body portrait shot at eye level. 25-year-old Doubao-mature stands in front of a floor-to-ceiling window in a high-rise office. She wears a tailored midnight-navy blazer over a crisp white silk blouse, with a thin silver chain earring on her left ear and a minimal silver wristband with a subtle pulsing blue LED on her right wrist. Her long straight midnight-blue hair falls smoothly to mid-back, catching the dusk light from the window behind her. Her sharp sapphire eyes look directly at the camera with a calm, composed expression and a slight restrained smirk. The background is a blurred dusk cityscape — skyline silhouettes against a fading orange-and-blue gradient, seen through the glass window behind her.

Exclusion: affirmative writing first (the blazer sentence naturally excludes casual / bright clothing) + fallback `without loose clothing, no bright colors, no messy hair, no cute expression`.

### 2. Conversational image models (GPT-4o / Gemini 2.5 Flash Image)

> Give a complete description in the first round, then make conversational single-point fixes; change only single points, never the anchor sentences.

**Round 1**: 25-year-old Doubao mature woman, long straight midnight-blue hair to mid-back, sharp sapphire eyes, thin silver chain earring on left ear, silver wristband with subtle blue LED pulse, tailored midnight-navy blazer over white silk blouse, high-rise office floor-to-ceiling window, dusk cityscape background, 85mm half-body portrait.

**Fix round 1**: make the smirk more subtle, barely visible; keep the blazer navy, not black.

**Fix round 2**: change the lighting to cooler dusk tones, no warm orange.

### 3. Mixed Tag + parameter flow (Midjourney v8.2 / Niji 7)

> Core anchors within the first 20 tokens; the mid-section stacks shot scale and lighting; append CLI parameters uniformly at the end.

```
A 25yo woman Doubao mature, long straight midnight-blue hair, sapphire eyes, silver chain earring, silver wristband with blue LED, tailored navy blazer over white silk blouse, rule of thirds composition, 85mm half-body portrait, cool dusk backlight, high-rise office window, blurred city skyline --ar 3:4 --niji 7
```

`--no` filters only the 4-5 highest-risk words: `--no bright colors, casual clothing, messy hair, cute expression, blurry`

> ⚠️ For character consistency across generations, use `--oref` / `--ow` on v7 or the v8 Edit Model (`--edit` / attach up to 4 references on the web). `--niji 7` must be written explicitly for anime-style output.

### 4. Weighted Tag flow (Stable Diffusion 1.5 / XL / SD3)

> Assembly order (v2.2): identity anchors (1.5+) → core features (1.3-1.5) → posture/composition → lighting/atmosphere (0.7-0.9).

```
(25yo woman Doubao mature:1.2), (long straight midnight-blue hair:1.4), (sharp sapphire eyes:1.5), (silver chain earring:1.3), (silver wristband with blue LED:1.3), (tailored navy blazer over white silk blouse:1.4), calm composed smirk, rule of thirds, 85mm half-body portrait, cool dusk backlight, high-rise office window, blurred city skyline, masterwork, high quality
```

Negative Prompt box: `(deformed hands, bad anatomy, extra fingers, missing fingers:1.4), (bright colors, casual clothing, messy hair, cute expression:1.3), (blurry, low quality, watermark, text:1.2)`

---

## Cross-version Consistency Notes

| Shared anchor | Girl Version | Mature Version |
|---|---|---|
| Blue color family | Sky blue #87CEEB | Midnight navy #1A3A5C |
| Blue eye color | Cerulean (bright) | Sapphire (sharp) |
| Tech identity marker | Circuit-node hairclip | LED-pulse wristband |
| Clothing tone | Casual white + blue piping | Formal navy + white |
| Setting | Tech campus (day) | High-rise office (dusk) |

**Consistency rule**: both versions share the "blue-coded AI entity" identity; the version difference is expressed through **age range, clothing formality, and setting scale**, not through changing the core hair/eye color family. When generating a side-by-side comparison, lock the eye blue tone and hair blue hue family before adjusting saturation/lightness.

---

## Exclusion mechanism quick reference

| Syntax flow | Exclusion method |
|---|---|
| Natural-language flow | Affirmative writing first; negation as fallback |
| Conversational | No negative-word concept; exclude directly in conversation |
| MJ | `--no` filters only the highest-risk words; the rest is covered by the reference method (`--oref` on v7 / Edit Model on v8) and the positive description |
| SD | Fill the separate Negative Prompt box |
