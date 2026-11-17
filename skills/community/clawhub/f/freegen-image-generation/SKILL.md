---
name: "freegen-image-generation"
description: "Freegen image-gen API: TXT2IMG, I2I, Inpainting, RemoveBG, Upscale via local freegen container. Supports Flux, SDXL, SD1.5, Lightning models."
---

# Freegen Image Generation

## Übersicht

**freegen** ist ein Docker-Container auf dem `homedocker`-Server, der die **[Dezgo.com](https://dezgo.com) API** wrapped.  
Interne URL: `http://freegen:3000`

Alle Generierungen laufen über einen **einzigen Endpunkt**: `POST /generate`  
Bild-Download: `GET /files/{filename}.png`  
Info: `GET /info`  
Health: `GET /health`

---

## Endpoints

### `POST /generate`

Der zentrale Endpoint. Unterstützt folgende `category`-Werte:

| Kategorie | Typ | Modelle | Kosten |
|---|---|---|---|
| `flux` | TXT2IMG | Eingebaut (kein Select) | ~$0.0029 |
| `sdxl` | TXT2IMG | dreamshaperxl, juggernautxl, ponyxl_6, realismengine, sdxl, bluepencilxl, illustrious* | ~$0.0075 |
| `sd1` | TXT2IMG | realistic_vision_5_1, deliberate_2, juggernaut_reborn, dreamshaper_8, absolute_reality + 90+ | ~$0.0019 |
| `sdxl2` | TXT2IMG (Lightning) | juggernautxl_10_hyper, dreamshaperxl_lightning, ponyxl_6_turbo_dpo, envy_starlight_xl | ~$0.0032 |
| `i2i` | IMG2IMG | SD 1.5 Modelle (realistic_vision_5_1, etc.) | ~$0.0019 |
| `inpaint` | Inpainting SD 1.5 | SD 1.5 Inpainting-Modelle | ~$0.0019 |
| `inpaint_sdxl` | Inpainting SDXL | juggernautxl_x_inpaint_1024px u.a. | ~$0.0032 |
| `textinpaint` | Mask-per-Text | SDXL Inpainting-Modelle | ~$0.0032 |
| `controlnet` | Struktur-T2I | SD 1.5 Modelle + control_model | ~$0.0019 |
| `edit` | Bild editieren | SD 1.5 Modelle | ~$0.0019 |
| `removebg` | Hintergrund entfernen | – | ~$0.0019 |
| `upscale` | Hochskalieren | – | ~$0.0019 |

---

## Payload-Formate

### TXT2IMG

**Flux (zuverlässig, schnell, uncensored):**
```json
{
  "prompt": "a red dragon breathing fire, fantasy art, detailed",
  "category": "flux",
  "width": 1024,
  "height": 1024,
  "steps": 4
}
```

**SDXL:**
```json
{
  "prompt": "a portrait of a young woman with purple hair, photorealistic",
  "category": "sdxl",
  "model": "dreamshaperxl_1024px",
  "width": 768,
  "height": 1024,
  "guidance": 7,
  "steps": 30,
  "seed": 2024
}
```

**SD 1.5:**
```json
{
  "prompt": "a cute cat on a windowsill, detailed fur",
  "category": "sd1",
  "model": "realistic_vision_5_1",
  "width": 512,
  "height": 768,
  "guidance": 7,
  "steps": 30,
  "sampler": "dpmpp_2m_karras",
  "seed": 2024
}
```

**SDXL Lightning:**
```json
{
  "prompt": "a cyberpunk cityscape at night, neon lights",
  "category": "sdxl2",
  "model": "juggernautxl_10_hyper",
  "width": 768,
  "height": 1024,
  "guidance": 2,
  "steps": 10
}
```

### IMG2IMG (Image-to-Image) — Outfit-Änderung, Style-Transfer

```json
{
  "prompt": "person wearing a red summer dress",
  "category": "i2i",
  "model": "realistic_vision_5_1",
  "init_image": "data:image/png;base64,...",
  "strength": 0.75,
  "width": 512,
  "height": 768,
  "steps": 30
}
```

### Inpainting — Bereich ersetzen

**Mit manueller Maske (SD 1.5):**
```json
{
  "prompt": "a silver belly button piercing",
  "category": "inpaint",
  "init_image": "data:image/png;base64,...",
  "mask_image": "data:image/png;base64,...",
  "strength": 1,
  "steps": 30,
  "sampler": "euler"
}
```

**Mit manueller Maske (SDXL):**
```json
{
  "prompt": "a silver belly button piercing",
  "category": "inpaint_sdxl",
  "init_image": "data:image/png;base64,...",
  "mask_image": "data:image/png;base64,...",
  "strength": 1,
  "steps": 20
}
```

**Per Text-Prompt maskieren (✨ am einfachsten!):**
```json
{
  "prompt": "a belly button piercing with a silver ring",
  "category": "textinpaint",
  "mask_prompt": "belly button, navel",
  "init_image": "data:image/png;base64,...",
  "strength": 0.85,
  "steps": 20,
  "sampler": "euler"
}
```

### ControlNet — Struktur-gesteuert
```json
{
  "prompt": "a person in the same pose, wearing armor",
  "category": "controlnet",
  "init_image": "data:image/png;base64,...",
  "control_model": "canny",
  "control_scale": 1
}
```
`control_model`: canny, hed, openpose, depth, normal

### Remove Background
```json
{
  "category": "removebg",
  "init_image": "data:image/png;base64,..."
}
```

### Upscale
```json
{
  "category": "upscale",
  "init_image": "data:image/png;base64,...",
  "scale": 2
}
```
`scale`: 2, 3, oder 4

---

## ⚠️ Hinweise

**Dezgo Content Policy (Stand 28.07.2026):**

| API | Content-Filter |
|---|---|
| Flux TXT2IMG | Kein Filter – alle Prompts erlaubt |
| SDXL/SD1.5/SDXL2 TXT2IMG | Standard Dezgo-Filter |
| **Image-Tools** (I2I, Inpainting, RemoveBG, Upscale, Edit, ControlNet) | Dezgo blockt bestimmte Prompts (HTTP 500) |

**Workaround für restriktive Prompts:**
- Flux TXT2IMG mit direktem Prompt (kein Filter)
- Clean-Inhalte funktionieren mit allen Tools einwandfrei (Kleidungswechsel, Piercings, Styling etc.)

---

## Status-Tabelle

| Funktion | Status | Hinweis |
|---|---|---|
| Flux TXT2IMG | ✅ | ~5s, $0.0029, **uncensored** |
| SDXL TXT2IMG | ✅ | ~7s, $0.0032 |
| SD 1.5 TXT2IMG | ✅ | ~38s, $0.0023 |
| SDXL Lightning | ✅ | ~17s |
| Inpainting (SDXL) | ✅ | NSFW blockt Dezgo |
| Inpainting (SD 1.5) | ✅ | NSFW blockt Dezgo |
| I2I | ✅ | NSFW blockt Dezgo |
| RemoveBG | ✅ | |
| Upscale | ✅ | |
| Text-Inpainting | ⚠️ | Korrekter Model-Name nötig |

---

## Beispiel-Workflow (Node.js/OpenClaw)

```javascript
// Bild generieren
const res = await fetch('http://freegen:3000/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'a cute orange cat',
    model: 'flux'
  })
});
const data = await res.json();
// data = { success, file, url, size, elapsed, cost, balance, model, sub_model, params }

// Bild runterladen
const imgRes = await fetch(`http://freegen:3000${data.url}`);
const imgBuf = Buffer.from(await imgRes.arrayBuffer());
```

---

## Verfügbare Modelle

**Komplette Liste** via `GET /info` abrufbar.

**SDXL:** dreamshaperxl_1024px, juggernautxl_1024px, ponyxl_6, realismenginesdxl_1024px, sdxl_1024px, bluepencilxl_1024px, illustrious_*

**SDXL Lightning (sdxl2):** juggernautxl_10_hyper, dreamshaperxl_lightning_1024px, ponyxl_6_turbo_dpo, envy_starlight_xl_01_lightning_1024px

**SD 1.5 (sd1):** realistic_vision_5_1, deliberate_2, juggernaut_reborn, dreamshaper_8, absolute_reality_1_8_1 + 99+ weitere

---

## Fehlerbehandlung

- **Flux:** `model` und `category` können fehlen (defaults to flux)
- **SDXL/SD1.5/SD2:** `category` + `model` sind beide nötig
- **HTTP 400 InvalidEnumValue:** Falscher Model-Name
- **HTTP 499: Timeout/Abort – Request war zu langsam oder zu groß
- **Fake Images (310 bytes):** Flux 2, Flux 2 Pro, Grok Imagine, Nano Banana sind Broken Models – nicht verwenden!
