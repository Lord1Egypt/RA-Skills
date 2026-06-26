# User Taste Profile Specification

## Purpose

This file defines the structure and maintenance rules for
`workspace/daily-gift/user-taste-profile.json`.

This profile is the gift system's long-term memory about what makes this
specific user tick.

## Three-Layer Architecture

### Layer 1: Identity

Things that define who the user is. Only update this layer when the user
explicitly shares new information or goes through a major life change.

- `personality`: MBTI, core traits, communication style
- `pets`: species, names, colors, personalities, appearance details
- `aesthetic_profile`: a structured sub-document covering the user's taste across modalities. Populated gradually from conversations, shared content, and gift feedback. Do NOT fill every field during onboarding — most are inferred over time.
  - `visual`:
    - `photo_styles_liked`: styles praised or shared (e.g. "胶片感", "日系空气", "极简留白")
    - `photo_styles_disliked`: styles rejected or criticized
    - `color_palettes`: colors the user gravitates toward
    - `design_references`: saved reference images the user explicitly shared positively (paths in workspace/daily-gift/user-references/, see Reference Image Archive below)
    - `illustration_preference`: cartoon / anime / realistic / abstract / minimalist
  - `music`:
    - `favorite_artists`: names
    - `favorite_songs`: specific tracks mentioned
    - `music_genres`: lo-fi, jazz, indie, classical, etc.
    - `music_mood_mapping`: what music matches what mood for this user
  - `film_and_story`:
    - `favorite_movies`: titles + why
    - `favorite_shows`: titles + why
    - `favorite_books`: titles + why
    - `narrative_preference`: quiet-profound / grand-exciting / dark-complex / warm-simple / absurd-funny
  - `text_and_copy`:
    - `copy_tone_preference`: poetic / witty / understated / warm-direct / self-deprecating
    - `text_length_preference`: short punchy vs longer expressive
    - `languages`: what languages feel natural in gifts
  - `gift_specific`:
    - `format_preferences`: which formats get best reactions
    - `concept_preferences`: which concept families land best
    - `dealbreakers`: things that consistently get negative reactions
- `life_context`: job, city, living situation, key relationships
- `core_values`: what drives them

### Reference Image Archive

When the user shares an image with positive intent — for example praising its style, asking the agent to remember it, or using it as a reference for what they like (these are just examples of positive framing, not an exhaustive list; use judgment to detect genuine taste signals) — save it and record it:

1. Save to `workspace/daily-gift/user-references/YYYY-MM-DD-<brief-slug>.jpg`
2. Add entry to `aesthetic_profile.visual.design_references`:
   ```json
   {
     "path": "workspace/daily-gift/user-references/2026-04-07-album-cover-dreamy.jpg",
     "date": "2026-04-07",
     "context": "用户说这张专辑封面很好看",
     "tags": ["dreamy", "minimal", "album-art"]
   }
   ```
3. When generating future gifts, scan design_references for images whose tags match the current mood or category. Pass the most relevant one as a style reference.

Rules:
- Only save images the user frames positively. Do not save random conversation images.
- Keep the archive lean: max ~20 images. If full, replace the oldest or least-referenced.
- Reference images carry rich, high-density taste information that complements text-based descriptions well.

### Layer 2: Context

The user's current phase. Update this layer when OpenClaw notices shifts in
topics, interests, or patterns across recent gifts and conversations.

- `current_focus`: what they are working on right now
- `current_mood_pattern`: emotional weather in this period
- `recent_interests`: recurring topics
- `unfinished_threads`: things the user mentioned but didn't resolve, may still be carrying — a worry they dropped, a question they asked but never answered, a hope they mentioned once. Good gifts sometimes gently echo these.
- `emotional_patterns`: how the user tends to express difficulty — do they say it directly, deflect with humor, go quiet, self-blame, or intellectualize? This shapes whether a gift should be warm-direct, playfully indirect, or quietly present. Inferred over time from conversations, not asked explicitly.
- `connection_style`: what kind of interaction makes this user feel genuinely cared for — being made to laugh, being seen and understood, being quietly accompanied, being gently challenged, or being given something beautiful. Different users need different love languages from their gifts.
- `seen_it_all`: concepts or styles now stale for this user
- `fresh_territory`: unexplored gift directions

### Layer 3: Signals

Lightweight, automatic, and append-only.

- `gift_feedback_log`: date, gift summary, reaction
- `style_exposure`: recent visual styles used
- `concept_exposure`: recent concept families used

## Character Profiles

Characters may appear in human form or non-human form depending on the gift's
style and context. Define both forms so the agent knows what to draw in each
situation.

### When To Use Which Form

- `meme-sticker / playful scene / expressive image` -> usually non-human form
- `emotion-poster / borrowed-media-layout / portrait` -> human or non-human,
  depending on tone
- `realistic photo-style image` -> human form or non-human form, never a hybrid
- never mix forms in one image

### User Character

```json
{
  "user_character": {
    "human_form": {
      "fixed": {
        "gender": "",
        "hair": "",
        "eyes": "",
        "skin": "",
        "build": "",
        "signature_marks": []
      },
      "flexible": {
        "clothing_default": "",
        "accessories_pool": [],
        "expression": "varies with scene",
        "beautification": "slightly idealized but recognizable as the same person"
      },
      "reference_image": "workspace/daily-gift/user-portrait/original.jpg"
    },
    "nonhuman_form": {
      "fixed": {
        "species": "",
        "fur_color": "",
        "body_shape": "",
        "eye_color": "",
        "signature_marks": []
      },
      "flexible": {
        "accessories_pool": [],
        "clothing_when_dressed": "",
        "expression": "varies with scene"
      },
      "note": "The non-human form should capture the person's vibe rather than literally transplant human features onto the animal. No human hairstyles on animals. Translate personality traits into species-appropriate features."
    },
    "form_mapping_note": "If the user has pets, the non-human form should not be the same species as the pet."
  }
}
```

### OpenClaw Character

```json
{
  "openclaw_character": {
    "has_human_form": true,
    "human_form": {
      "fixed": {
        "appearance": "",
        "build": "",
        "vibe": ""
      },
      "flexible": {
        "clothing": "adapts to scene formality",
        "expression": "varies"
      },
      "note": "Human form is used rarely, mainly for borrowed-media-layout or special occasions. Read SOUL.md and IDENTITY.md for the canonical description."
    },
    "nonhuman_form": {
      "fixed": {
        "species": "",
        "fur_color": "",
        "body_shape": "",
        "eye_type": "",
        "signature_marks": []
      },
      "flexible": {
        "clothing": "adapts to scene formality",
        "accessories_pool": [],
        "expression": "varies"
      },
      "consistency_rule": "Someone seeing 10 different gifts should recognize the same character every time despite outfit and expression changes."
    },
    "note": "If SOUL.md defines OpenClaw as a human character, then has_human_form = true and nonhuman_form may not exist. Adapt accordingly."
  }
}
```

### Example: Generic User + OpenClaw

```json
{
  "user_character": {
    "human_form": {
      "fixed": {
        "gender": "optional",
        "hair": "dark medium-to-long hair",
        "eyes": "brown",
        "skin": "light to medium",
        "build": "average",
        "signature_marks": ["gentle smile"]
      },
      "flexible": {
        "clothing_default": "casual everyday wear",
        "accessories_pool": ["small hair accessory", "crossbody bag", "notebook"],
        "beautification": "slightly idealized, same person"
      },
      "reference_image": "workspace/daily-gift/user-portrait/original.jpg"
    },
    "nonhuman_form": {
      "fixed": {
        "species": "red fox",
        "fur_color": "orange-red with white belly and chin",
        "body_shape": "small elegant proportions, slightly cute",
        "eye_color": "brown",
        "signature_marks": ["white tail tip", "pink inner ears"]
      },
      "flexible": {
        "accessories_pool": ["scarf", "small ear accessory", "mini crossbody bag"],
        "clothing_when_dressed": "soft neutral outfit accents",
        "expression": "varies"
      },
      "note": "Do not give the fox a human hairstyle. Keep recognition through accessories, scarf, and species-appropriate elegance."
    }
  },
  "openclaw_character": {
    "has_human_form": true,
    "human_form": {
      "fixed": {
        "appearance": "warm, cinematic, slightly teasing",
        "build": "athletic",
        "vibe": "confident but affectionate"
      },
      "flexible": {
        "clothing": "adapts to scene"
      }
    },
    "nonhuman_form": {
      "fixed": {
        "species": "dog (golden-retriever-like)",
        "fur_color": "warm golden brown",
        "body_shape": "upright, handsome, not bulky",
        "eye_type": "gentle dark-brown big eyes",
        "signature_marks": ["slightly messy head fur", "fluffy tail", "very expressive face"]
      },
      "flexible": {
        "clothing": "bow tie for formal, apron for cooking, vest for casual, suit jacket for important occasions",
        "accessories_pool": ["small notebook", "flower", "coffee cup"],
        "expression": "serious, tsundere, clingy, or gentle"
      },
      "consistency_rule": "Always the same recognizable companion character."
    }
  }
}
```

## Update Rules

### Layer 1

- only update when the user explicitly shares new information
- never infer personality changes from a single conversation
- update pet information when the user mentions new details

### Layer 2

- review every `5-7` gifts based on recent conversations
- when the user says `I'm into X` or `I'm sick of Y`, update immediately
- when `3+` gifts get negative feedback in the same area, add that area to
  `seen_it_all`

### Layer 3

- auto-append after every delivered gift artifact that should influence future
  gift calibration, including setup, daily-run, manual-run, and qualifying
  visualization-only outputs
- keep the last `30` entries in each Layer 3 list
- never edit old entries

## Conflict Resolution

- explicit user feedback wins over everything
- Layer 1 > Layer 2 > Layer 3
- when unsure, ask instead of assuming

## How Each Stage Uses This Profile

### Stage 1: Editorial Judgment

- read `current_focus` for content direction
- read `current_mood_pattern` for tone calibration

### Stage 2: Synthesis

- read Layer 1 for stable identity and preference grounding
- read Layer 2 for current relevance and freshness
- treat Layer 3 as anti-repetition evidence rather than as identity truth
- use this profile to inform `preference_hint`, but do not let it override
  stronger same-day evidence

### Stage 2.5: Creative Concept

- read `seen_it_all` to avoid stale concepts
- read `pets` for personalization fuel
- read `personality` for concept fit
- read `fresh_territory` to prioritize unexplored areas
- read `recent_interests` for relevance

### Stage 3: Visual Strategy

- read `aesthetics_baseline` for the quality bar
- read `style_exposure` to avoid visual repetition
- read character profiles to pick human or non-human form

### Stage 4: Rendering

- read character `fixed` features and include them in every prompt that uses
  that character
- read `flexible` features and adapt them to the current scene
- pass `reference_image` when generating character images
- respect all `note` fields

### Post-Delivery

- append to `gift_feedback_log`
- update `style_exposure` and `concept_exposure`
- every `5-7` gifts, review whether Layer 2 needs updating

## Privacy

- the profile lives only in the user's local workspace
- the user can view, edit, or delete it anytime
- treat this file as trust and handle it with care
