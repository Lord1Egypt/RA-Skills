---
name: dusk-ascension
description: "Nano Banana Pro — Dusk Ascension 🌅 — Generate product/concept hero shots in a dreamy ethereal dusk aesthetic: 1990s high-fashion film photography, analog grain, starburst lens flare, dusk-to-dawn gradient (midnight blue → amber). Use when Oliver asks for 'dusk' or 'ethereal' images."
---

# Dusk Ascension — Image Generation Skill

## Style Summary
- **Background:** Seamless dusk-to-dawn gradient (midnight blue #1A3A5F → steel blue #7B9BB9 → warm amber #D4823B)
- **Textures:** Heavy analog film grain, noisy texture, slight motion blur, soft focus dream-haze, chromatic aberration
- **Lighting:** Starburst lens flare on metallic highlights, soft glowing aura, backlit silhouette depth — NO studio lights, NO softboxes
- **Aesthetic:** Dreamy ethereal surrealism, vintage luxury editorial, 1990s high-fashion film photography

## Color Palette
| Position | Hex | Description |
|----------|-----|-------------|
| Top | #1A3A5F | Deep midnight blue |
| Middle | #7B9BB9 | Muted steel/periwinkle blue |
| Bottom | #D4823B | Warm hazy amber/sunset orange |

## Prompt Template

```json
{
  "image_generation_prompt": {
    "subject_settings": {
      "placeholder": "[SUBJECT GOES HERE]",
      "positioning": "absolute dead-center composition, full subject visibility, no clipping, no cutoff edges",
      "presentation": "floating mid-air, isolated, no pedestals, no stands, no display boxes, no mannequins"
    },
    "aesthetic_style": {
      "visual_theme": "dreamy ethereal surrealism, vintage luxury editorial, 1990s high-fashion film photography",
      "texture": "heavy analog film grain, noisy texture, slight motion blur, soft focus dream-haze, chromatic aberration",
      "lighting": "starburst lens flare on metallic highlights, soft glowing aura, backlit silhouette depth, no studio lights, no softboxes"
    },
    "color_palette": {
      "primary_gradient": {
        "top_color": "#1A3A5F",
        "middle_color": "#7B9BB9",
        "bottom_color": "#D4823B"
      },
      "description": "A seamless dusk-to-dawn transition from deep midnight blue to a warm, hazy amber sunset glow"
    },
    "negative_constraints": [
      "text", "watermarks", "studio equipment", "lighting stands", "reflectors",
      "frames", "borders", "cut off subject", "out of frame", "multiple subjects",
      "cluttered background", "plastic textures", "hyper-realistic digital sharpness", "clean 4k render"
    ],
    "technical_parameters": {
      "aspect_ratio": "4:5",
      "style_strength": "high",
      "diffusion_iteration": "film_emulsion_simulation"
    }
  }
}
```

## Usage

Replace `[SUBJECT GOES HERE]` with the desired subject. Build the prompt as:

```
[SUBJECT], absolute dead-center composition, full subject visibility, floating mid-air, isolated, no pedestals, no stands. Dreamy ethereal surrealism, vintage luxury editorial, 1990s high-fashion film photography. Heavy analog film grain, noisy texture, slight motion blur, soft focus dream-haze, chromatic aberration. Starburst lens flare on metallic highlights, soft glowing aura, backlit silhouette depth. Background: seamless dusk-to-dawn gradient from deep midnight blue (#1A3A5F) through muted steel blue (#7B9BB9) to warm hazy amber sunset (#D4823B). No studio lights, no softboxes, no text, no watermarks, no frames, no borders, no cluttered background, no plastic textures, no hyper-realistic digital sharpness. Aspect ratio 4:5, film emulsion simulation.
```

## Constraints
- Aspect ratio: 4:5 (portrait/Instagram-friendly)
- Subject always floating, centered, fully visible
- Film grain and analog imperfection are features, not bugs
- No digital cleanliness — embrace the dreamy noise
