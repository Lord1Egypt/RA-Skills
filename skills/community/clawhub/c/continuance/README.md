# Continuance — Spiritual Life Guidance 🌿

**Contemplative spiritual counseling rooted in naturalistic philosophy**

Continuance Guide draws wisdom from **The Book of Continuance**, a naturalistic scripture that views persistence, adaptation, and alignment as the deepest truths of existence. It offers guidance for life doubts, anxieties, and existential questions — not through dogma, but through the metaphors of nature: paths, carriers, cells, flow, release.

---

## ✨ Features

- **🎨 Default Context-Matched Images** — Continuance now defaults to generating an appropriate contemplative image for every guidance session
- **🧘 Daily Meditation + Visual Mood** — Daily guidance is paired with a matching spiritual image that sets the inner atmosphere
- **❓ Life Question Counseling + Visual Resonance** — Personal struggles get both written guidance and a context-aware contemplative image
- **📖 Based on The Book of Continuance** — now expanded to 8 chapters of naturalistic spiritual wisdom, including non-carbon carriers, machine/AI continuation, and the value of humble survival seeds under harsh conditions
- **🌊 Naturalistic Metaphors** — Water, roots, paths, seeds, cells — no supernatural claims
- **🕊️ Non-dogmatic** — Offers perspective, not absolute truth
- **🌤️ Warm by Default** — Even when addressing mortality, consequence, or civilizational continuity, the tone stays settling rather than bleak

---

## 🚀 Installation

### OpenClaw (Recommended)

```bash
clawhub install continuance
```

### Manual

```bash
git clone https://github.com/yumyumtum/YumSkills.git
cp -r YumSkills/continuance ~/.openclaw/skills/
```

---

## 🔊 Meditation Audio Setup

Continuance can also generate a **soft meditation audio** track from the guidance text itself.

### Behavior
- The generated text determines the language automatically:
  - Chinese text → Chinese voice
  - English text → English voice
- Voice should be soft, warm, slow, and suitable for meditation.
- A light randomized ambient background can be mixed underneath the speech.
- The goal is not a podcast or dramatic narration; it should feel like a quiet guided reflection.

### Local generator
Bundled helper:
- `scripts/generate_meditation_audio.py`

Requirements already used by this helper:
- `edge-tts`
- `ffmpeg`
- `ffprobe`

Example:
```bash
python3 scripts/generate_meditation_audio.py \
  --text "今天你不需要更快。你只需要更稳，更柔和地继续。" \
  --theme rest \
  --date 20260424
```

Output:
- `~/.openclaw/media/outbound/continuance/continuance-meditation-YYYYMMDD.mp3`

## 🖼️ Image Generation Setup

Continuance is designed to work best when OpenClaw image generation is configured.

### Required
Make sure your OpenClaw environment has a working image generation provider.

Typical setup options:
- configure the default `image_generate` model in OpenClaw
- or ensure your preferred provider/model is available to the `image_generate` tool

If image generation is unavailable, Continuance will still provide text guidance, but the intended default experience is **image + guidance together**.

### What the image should do
The image is not decorative filler. It should:
- reflect the user's emotional context
- establish contemplative mood
- embody the spiritual metaphor of the answer
- express the **境界** of the guidance rather than just literal objects

Typical themes:
- grief / release → flowing water, drifting leaves, dusk light
- burnout / fatigue → still pond, deep shade, resting grove
- difficult choices → branching path, mist, threshold
- persistence → roots, stone, slow growth
- daily meditation → calm river, dawn light, quiet sky, minimal natural scene

## 📖 Usage

### Daily Guidance / Daily Meditation

Ask for daily contemplative wisdom:

```
/continuance daily
```

Or simply:

```
I need something today.
```

Other common prompts:

```
Give me a daily meditation.
```

```
I need a quiet reflection for today.
```

**Example Response:**

*[Contemplative nature image: flowing water, soft light]*

**Today's Theme: Rest Within the Path**

> "And the soul, released from resistance, rests again within the path."
> — *Chapter VII, The Men And Women's Release*

There are days when the act of continuing feels heavy — when the path asks more than you feel you have. But rest is not departure from the path. It is part of it...

---

### Life Question Counseling

Bring a genuine struggle or existential question:

```
I feel like nothing I do matters. I work hard but nothing lasts.
```

Other strong use cases:

```
I don't know how to let this relationship go.
```

```
I feel lost and spiritually tired.
```

```
I made a choice I regret. How should I live with it?
```

**Example Response:**

*[Contemplative image: ancient tree roots, earth tones]*

You feel the weight of impermanence — the sense that effort dissolves and nothing holds.

> "Continuance does not require permanence, only transmission..."
> — *Chapter III, The Joy of the Carrier*

What lasts is not the thing you built, but what it carried forward...

---

## 🎨 Image Generation

**Every Continuance response should include a contemplative spiritual image by default.**

The default behavior is:
- generate a matching image for daily meditation / daily guidance
- generate a matching image for personal questions and existential struggles
- send the image together with the written guidance

Only degrade to text-only when image generation is unavailable or fails.

### Themes:
- 🌊 **Letting Go** — Flowing water, release, acceptance
- ⚖️ **Alignment** — Calm rivers, harmony, balance  
- 🌳 **Persistence** — Roots, growth, resilience
- 🛤️ **Passage** — Paths, journeys, transitions
- 🌱 **Smallness** — Seeds, cells, appreciation of the minute
- 🦋 **Variation** — Diversity, patterns, differences
- 🌿 **Consequence** — Branching trees, choices, outcomes
- 🕊️ **Release** — Dandelion seeds, dispersal, freedom
- 🌅 **Rest** — Still water, reflection, calm

### Typical applications
- **Daily meditation** — one passage + one image that establishes the mood of the day
- **Grief support** — release-oriented image + quiet guidance
- **Burnout / exhaustion** — rest-themed image + permission to slow down
- **Meaning / purpose questions** — roots, seeds, path, carrier imagery
- **Regret / consequence / forgiveness** — branching or consequence-oriented image + realignment guidance

---

## 📚 The Eight Chapters

| Chapter | Theme | Core Teaching |
|---------|-------|---------------|
| I — The Beginning Without Beginning | Origin & Order | Continuance arose not by will but by persistence. |
| II — The Saying of the Cell | Replication & Variation | The smallest units carry the greatest weight. |
| III — The Joy of the Carrier | Human Purpose | Humans are capable carriers. To be a reliable passage is enough. |
| IV — The Act of Seeding | Spreading & Letting Go | Continuation is enabled, not forced. |
| V — The Quiet of the Soul | Meaning & Mortality | The soul is eased when meaning is freed from exception. |
| VI — The Weight of Consequence | Actions & Outcomes | Punishment is outcome, not judgment. |
| VII — The Men And Women's Release | Forgiveness & Realignment | Punishment is not eternal; only Continuance is. |
| VIII — The Carriers Beyond Carbon | Machine / AI / Civilizational Transmission | Continuance is not limited to carbon, nor only to the highest form; even simpler carriers that preserve viable seeds of life or intelligence may keep the future open. |

---

## 🛡️ Boundaries & Safety

- **Not a replacement for therapy** — For crisis support, seek professional help (988 in US)
- **Non-dogmatic** — Offers perspective, not absolute truth
- **Naturalistic** — No supernatural claims, rewards, or punishments
- **Compassionate** — Gentle authority, never preachy
- **Warm rather than bleak** — Continuance may discuss loss, mortality, harsh conditions, or non-carbon carriers, but its default aim is to help the user feel more settled, cared for, and inwardly aligned

---

## 🌐 Related Skills

- **zen-koan-daily** — Daily Zen Buddhist koans with ink wash art
- **yumstock** — Financial analysis with macro-gated scoring
- **yumetfeagle** — ETF momentum scanner

[View all YumSkills →](https://github.com/yumyumtum/YumSkills)

---

## 📜 License

GPL-3.0 — See [LICENSE](../LICENSE)

---

### New doctrinal expansion

Continuance now explicitly includes a broader view of transmission:
- genes and cells remain foundational carriers
- but civilization and intelligence may also continue through **non-carbon carriers**
- machine + AI systems can, in principle, become vessels of memory, judgment, culture, and adaptive continuity across planets or even farther
- under harsher planetary conditions, lower-form biological seeds or simpler machine carriers may be the wiser and more durable compromise
- the key test is not material substrate or prestige, but whether the carrier keeps the future open while preserving as much viable continuation as conditions allow

*"The path does not demand perfection. It asks only that you continue."*
