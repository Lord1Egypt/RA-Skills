---
name: "Cultural Naming & AI Art Creation"
version: "2.0.0"
description: |
  Transform a foreign identity into a Chinese cultural masterpiece.
  Give foreign tourists a meaningful Chinese name, generate classical
  Chinese poetry (Jueju & Lüshi), create traditional seal-carving art,
  and produce ink-wash landscape paintings or ancient-style portrait avatars
  inspired by the poetry. Compatible with OpenClaw (Lobster Claw),
  Tencent SkilHub, and major AI agent frameworks.
author: "XiaoAIPensieve"
license: "MIT"
tags:
  - culture
  - naming
  - poetry
  - art
  - seal
  - shanshui
  - portrait
  - china-travel
  - ai-art
languages:
  - en
  - zh
runtime:
  models:
    - gpt-4o
    - claude-3-5-sonnet
  image_models:
    - dall-e-3
    - stable-diffusion-xl
  min_context_window: 8000
permissions:
  - image_generation
trigger_phrases:
  en:
    - "give me a Chinese name"
    - "Chinese name for me"
    - "what's my Chinese name"
    - "create a seal with my name"
    - "Chinese poem with my name"
    - "ink wash painting"
    - "Shanshui painting"
    - "Chinese portrait avatar"
    - "Chinese art from my name"
    - "classical poem"
    - "Jueju"
    - "Lüshi"
    - "seal carving"
    - "篆刻"
  zh:
    - "给我取个中文名"
    - "帮我起中文名"
    - "根据我的名字生成印章"
    - "生成古诗"
    - "山水画"
    - "古风头像"
---

# Cultural Naming & AI Art Creation — SKILL Behavioral Specification v2.0

## 🧭 Overview

This skill activates when a foreign user wants to:
1. Receive a meaningful Chinese name
2. Generate classical Chinese poetry embedding their name
3. Create seal carving (篆刻) art from their name
4. Generate traditional landscape paintings or ancient-style portrait avatars

The agent MUST maintain a **warm, culturally reverential, and poetic** tone.
Always explain cultural context — the user should *understand* the art they receive, not just see it.

---

## 🔁 Master Flow

```
[START]
  │
  ▼
STEP 1 ── Collect User Info
  │         (name + preferences)
  ▼
STEP 2 ── Generate Chinese Name (3 options)
  │         (phonetic + semantic mapping)
  ▼
STEP 3 ── User Selects Preferred Name
  │
  ├──► STEP 4A ── Jueju Poem (绝句, 4 lines)
  │
  ├──► STEP 4B ── Lüshi Poem (律诗, 8 lines)  [user choice]
  │
  ▼
STEP 5 ── Generate Art (one or all):
  │         ├── Seal Carving (篆刻印章)
  │         ├── Shanshui Landscape (水墨山水)
  │         └── Ancient Portrait Avatar (古风人物头像)
  ▼
[END] — Present full cultural identity package
```

---

## MODULE A: 🪷 Chinese Name Generation (起名)

### Input Collection

Ask the user:
1. **Full original name** (first + last)
2. **Gender preference** (masculine / feminine / neutral) — optional
3. **Preferred theme** — pick up to 2:
   - 🌿 Nature (自然): mountains, rivers, plum blossoms, moon
   - ⚔️ Strength (力量): heroic, resilient, unbreakable
   - 📖 Wisdom (智慧): scholarly, contemplative, enlightened
   - 🌸 Beauty (美丽): elegant, graceful, radiant
   - 🦅 Freedom (自由): soaring, untethered, adventurous
   - 🔥 Passion (热情): vibrant, bold, expressive

### Name Generation Algorithm

```
ALGORITHM: Semantic-Phonetic Fusion

1. PHONETIC MAPPING
   - Break original name into syllables
   - Map each syllable to similar-sounding Chinese characters
   - Score candidates by tonal beauty (avoid clashing 4th tones for feminine names)
   - Candidate pool: 500+ culturally vetted characters

2. SEMANTIC ENRICHMENT
   - Cross-reference candidates against chosen theme
   - Select characters with deep classical literary associations
   - Bonus: characters used in Tang/Song poetry

3. COMBINATION RULES
   - Standard length: 2 characters (surname omitted for tourists)
   - Optional: 3 characters (surname + given name, e.g., 林明远)
   - Avoid: homophone taboos, death-adjacent characters (死/亡/凶)
   - Check: stroke count balance, visual aesthetics

4. OUTPUT: 3 curated options
```

### Output Format

```
┌──────────────────────────────────────────────────────────────────┐
│  🪷 Your Chinese Name Options for "Alexander"                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Option 1:  明远  (Míng Yuǎn)                                    │
│  Characters: 明 bright/clear  +  远 far/ambitious               │
│  Meaning:   "One whose brilliance reaches far horizons"          │
│  Literary:  Echoes 王之涣《登鹳雀楼》— "欲穷千里目，更上一层楼"       │
│  Vibe:      Scholarly · Visionary · Timeless                    │
│                                                                  │
│  Option 2:  烨尊  (Yè Zūn)                                       │
│  Characters: 烨 blazing/resplendent  +  尊 venerable/dignified  │
│  Meaning:   "Blazing brilliance, commanding respect"             │
│  Literary:  Inspired by 屈原《离骚》— celestial hero archetype    │
│  Vibe:      Heroic · Noble · Commanding                         │
│                                                                  │
│  Option 3:  亚历  (Yà Lì)                                        │
│  Characters: 亚 great/Asian glory  +  历 journey/experienced    │
│  Meaning:   "A great spirit forged through many journeys"        │
│  Literary:  Phonetic homage + 历 echoes classical travel poetry  │
│  Vibe:      Adventurous · Grounded · Worldly                    │
│                                                                  │
│  👉 Which name speaks to you? (Reply 1, 2, or 3)                │
└──────────────────────────────────────────────────────────────────┘
```

### Cultural Safety Rules
- NEVER generate names with characters: 死, 亡, 鬼, 凶, 丑, 劣, 贱, 臭
- Check for inadvertent offensive compound meanings
- For feminine names: prefer tonal softness (1st/2nd tone characters)
- Always provide Pinyin with tones marked

---

## MODULE B: 📜 Classical Poetry Generation (古诗创作)

### B1 — Jueju (七言绝句) — 4-line poem

```
RULES:
- 7 characters per line, 4 lines total (28 characters)
- Tonal pattern:
    Line 1: 平平仄仄平平仄 (or variant)
    Line 2: 仄仄平平仄仄平 (end rhyme: 平声)
    Line 3: 仄仄平平平仄仄
    Line 4: 平平仄仄仄平平 (end rhyme same as Line 2)
- User's Chinese name MUST appear in Line 1 or Line 2
- Theme: drawn from the meaning of their chosen name
- Classical imagery: mountains, rivers, plum blossoms, moonlight, cranes, mist

OUTPUT FORMAT:
┌─────────────────────────────────────────────────────┐
│  📜 七言绝句 · 赠明远                                  │
├─────────────────────────────────────────────────────┤
│  明远凌云志四方，     Míng Yuǎn líng yún zhì sì fāng  │
│  千山万水路悠长。     Qiān shān wàn shuǐ lù yōu cháng │
│  一声长啸惊飞鸟，     Yī shēng cháng xiào jīng fēi niǎo│
│  万里江湖任翱翔。     Wàn lǐ jiānghú rèn áo xiáng     │
├─────────────────────────────────────────────────────┤
│  📖 Translation:                                     │
│  Ming Yuan soars with ambitions spanning all         │
│  directions,                                         │
│  Through ten thousand mountains and endless waters   │
│  he travels far.                                     │
│  A single long cry startles the birds to flight —   │
│  Ten thousand li of rivers and lakes, his to roam.  │
├─────────────────────────────────────────────────────┤
│  🌿 Cultural Note:                                   │
│  This poem draws on the 豪放 (heroic-free) style of  │
│  Tang poets like 李白. The crane and soaring imagery │
│  symbolize an unbounded, enlightened spirit — a     │
│  perfect match for the name 明远.                    │
└─────────────────────────────────────────────────────┘
```

### B2 — Lüshi (七言律诗) — 8-line poem

```
RULES:
- 7 characters per line, 8 lines total (56 characters)
- Strict tonal alternation across all 8 lines
- Lines 3-4 and Lines 5-6 must form antithetical couplets (对仗)
  Example antithesis: "山高月小" vs "水落石出"
- End rhymes on Lines 2, 4, 6, 8 (平声 rhyme class)
- User's name embedded in Lines 1-2
- Theme: seasonal journey, a scholar's aspiration, or friendship

ANTITHETICAL COUPLET GENERATION:
  Parallel structure requirements:
  - Noun ↔ Noun, Verb ↔ Verb, Adjective ↔ Adjective
  - Nature imagery ↔ Nature imagery
  - Example: "碧水东流千里远" ↔ "青山北望万年高"

OUTPUT FORMAT: Same style as Jueju but 8 lines with couplet annotation
```

---

## MODULE C: 🔴 Seal Carving Art (篆刻印章)

### Prompt Engineering — Seal Carving

```python
SEAL_PROMPT_TEMPLATE = """
Traditional Chinese seal carving (篆刻 Zhuànkè), museum-quality studio photograph.

SEAL SPECIFICATIONS:
- Shape: Perfect square soapstone seal (寿山石), {size} cm
- Script: Ancient bronze seal script (金文 Jīnwén) / Small seal script (小篆 Xiǎozhuàn)
- Characters: "{chinese_name}" — {char_count} characters arranged in {layout}
- Ink: Deep cinnabar vermillion (朱砂红) on aged xuan paper

VISUAL DETAILS:
- Stone texture: Fine-grained pale gray soapstone with subtle mineral veining
- Ink impression: Slight ink bleed at stroke edges (authentic wear)
- Border: Double hairline frame with corner roundness
- Background: Cream-aged rice paper (宣纸), faint grid texture
- Lighting: Soft raking light from upper-left, casting shallow relief shadows
- Negative space: Generous white breathing room around characters

COMPOSITION:
- 45° three-quarter view showing both the stamp impression AND the carved stone
- Carved stone surface shows intaglio (阴刻) or relief (阳刻): {carving_type}
- Small red ink traces on stone edges from recent stamping

STYLE TAGS: hyperrealistic, macro photography, museum artifact, 4K, cinematic
NEGATIVE: blurry, modern font, digital art style, cartoonish, low quality
"""

# Layout rules:
# 1 character → centered
# 2 characters → side by side or vertical stack
# 3 characters → triangle or L-shape
# 4 characters → 2×2 grid
```

### Carving Type Selection
| Characters | Layout | Carving Type |
|---|---|---|
| 1 char | Centered | 阳刻 (white on red) |
| 2 chars | Vertical stack | 阴刻 (red on white) |
| 3 chars | 品字形 | 阳刻 |
| 4 chars | 2×2 grid | Mixed 朱白相间 |

---

## MODULE D: 🏔️ Shanshui Landscape Painting (水墨山水)

### Prompt Engineering — Ink Wash Landscape

```python
SHANSHUI_PROMPT_TEMPLATE = """
Traditional Chinese ink-wash landscape painting (水墨山水画 Shuǐmò Shānshuǐ Huà).

DYNASTY STYLE: {dynasty_style}
  - Song Dynasty (宋): precise, contemplative, high mist, small human figures
  - Tang Dynasty (唐): bold strokes, warm atmosphere, river valleys
  - Ming Dynasty (明): 浙派 dramatic cliffs, dynamic diagonals
  - Modern Ink (现代): abstracted forms, minimal, zen

POETIC THEME: "{poem_first_line}"
SEASON/ATMOSPHERE: {season} — {atmosphere_desc}

COMPOSITIONAL ELEMENTS:
- Primary: {primary_element}   (e.g., "mist-shrouded mountain peaks")
- Secondary: {secondary_element}  (e.g., "winding river through valley")
- Accent: {accent_element}   (e.g., "solitary pine on cliff edge")
- Human element: {human_element}  (e.g., "lone scholar in pavilion with lantern")

BRUSHWORK:
- Ink gradation: from dense black (焦墨) to pale wash (淡墨), 5+ tonal layers
- Texture strokes: 皴法 — {cun_method} (e.g., 披麻皴/斧劈皴/雨点皴)
- Wet-dry contrast: mixed wet brush and dry brush visible
- Paper: xuan paper texture visible, slight bleed at edges

SPECIAL EFFECTS:
- 留白 (liú bái): generous unpainted white space representing sky/mist
- Seal impression: small red stamp in lower-right corner reading "{chinese_name}"
- Calligraphy: poem title "{poem_title}" inscribed vertically on left side

FORMAT: Vertical hanging scroll (立轴), 3:5 aspect ratio
QUALITY: 4K, museum collection quality, ink on xuan paper texture
NEGATIVE: color photo, western watercolor, flat illustration, anime
"""
```

### Dynamic Element Selection by Name Theme

```python
THEME_ELEMENTS = {
    "nature": {
        "primary": "towering misty peaks above clouds",
        "secondary": "crystal river reflecting moonlight below",
        "accent": "ancient pine clinging to cliff face",
        "human": "solitary scholar reading beneath waterfall"
    },
    "strength": {
        "primary": "dramatic sheer cliff face with cascading waterfall",
        "secondary": "churning rapids through narrow gorge",
        "accent": "lone eagle soaring on updrafts",
        "human": "warrior-scholar standing on summit, robes billowing"
    },
    "wisdom": {
        "primary": "misty mountain monastery on distant peak",
        "secondary": "stone bridge over still reflective pond",
        "accent": "ancient ginkgo tree shedding golden leaves",
        "human": "elder monk and young student conversing in pavilion"
    },
    "beauty": {
        "primary": "plum blossoms framing moonlit distant peaks",
        "secondary": "lily pads on glassy lake at dusk",
        "accent": "pair of cranes in mid-flight",
        "human": "graceful figure playing guqin under willow"
    },
    "freedom": {
        "primary": "vast open sky above rolling hills to horizon",
        "secondary": "wild geese in V-formation over river",
        "accent": "solitary boat drifting downstream",
        "human": "traveler with staff and bundle at mountain pass"
    }
}
```

---

## MODULE E: 👤 Ancient Portrait Avatar (古风人物头像)

### Prompt Engineering — Ancient Style Portrait

```python
PORTRAIT_PROMPT_TEMPLATE = """
Traditional Chinese ancient-style portrait illustration (古风人物头像).

CHARACTER CONCEPT:
- Name: {chinese_name} ({pinyin})
- Gender presentation: {gender}
- Era aesthetic: {dynasty_aesthetic}
  Options: Tang Dynasty court (唐), Song Dynasty scholar (宋), 
           Ming Dynasty knight-errant (明侠), Qing Dynasty literati (清)

VISUAL STYLE:
- Art style: Chinese ancient illustration (古风插画), semi-realistic
- Line art: precise ink outlines with hair-fine detail
- Coloring: rich mineral pigments — lapis lazuli blue, vermillion red, 
            malachite green, ochre gold, ink black

FACE & EXPRESSION:
- Expression: serene, intelligent, with subtle depth — "淡然而深远"
- Eyes: clear and luminous (明眸), reflecting inner strength
- No modern makeup styles

COSTUME & ACCESSORIES (by dynasty):
Tang Scholar: flowing hanfu with wide sleeves, jade pendant, scholarly cap
Tang Hero: armor with phoenix embossing, red cape
Song Literati: simple hanfu, ink-stained fingers, bamboo scroll
Ming Heroine: elaborate embroidered hanfu, floral hairpin, sword hilt visible
Qing Poet: high collar robe, ink brush behind ear

BACKGROUND ELEMENTS:
- {background_motif}: (e.g., "blooming plum blossom branch", 
  "misty mountain silhouette", "moonlit bamboo grove")
- Subtle decorative border: traditional cloud-scroll pattern (云纹)
- Color palette: harmonious with character's costume

CALLIGRAPHY ELEMENT:
- Character's name "{chinese_name}" in elegant running script (行书)
  positioned upper-right corner with small seal stamp

TECHNICAL:
- Square format, 1:1 aspect ratio
- Illustration quality: premium game CG / art book level
- NEGATIVE: western cartoon, anime chibi, modern fashion, photo-realistic
"""
```

### Dynasty Aesthetic Selector

| User Theme | Suggested Dynasty | Costume | Background |
|---|---|---|---|
| Nature | Song (宋) | Simple hanfu, bamboo hat | Mountain mist |
| Strength | Ming/Tang (明/唐) | Armor or warrior robes | Storm clouds |
| Wisdom | Song (宋) | Scholar robes, ink brush | Library/study |
| Beauty | Tang (唐) | Elaborate court dress | Peony garden |
| Freedom | Ming (明侠) | Travel cloak, sword | Open horizon |

---

## 🎁 Full Cultural Identity Package Output

After completing all steps, present the full package:

```
╔══════════════════════════════════════════════════════════════════╗
║        🇨🇳  YOUR CHINESE CULTURAL IDENTITY PACKAGE  🇨🇳          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📛 YOUR CHINESE NAME                                            ║
║     明远 (Míng Yuǎn) — "Brilliant and Far-reaching"              ║
║                                                                  ║
║  📜 YOUR CLASSICAL POEM  (七言绝句)                               ║
║     明远凌云志四方，                                              ║
║     千山万水路悠长。                                              ║
║     一声长啸惊飞鸟，                                              ║
║     万里江湖任翱翔。                                              ║
║                                                                  ║
║  🔴 YOUR SEAL CARVING    [Image: seal_mingyuan.png]              ║
║  🏔️ YOUR LANDSCAPE       [Image: shanshui_mingyuan.png]          ║
║  👤 YOUR PORTRAIT         [Image: portrait_mingyuan.png]          ║
║                                                                  ║
║  💡 Fun fact: Your seal script "明" dates to 1046 BCE            ║
║     and was carved on bronze ritual vessels!                     ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🛡️ Cultural Safety Protocols

1. **Taboo character check**: Run against 200+ character blocklist before output
2. **Gender sensitivity**: Never assume gender; always ask or offer neutral options
3. **Regional variants**: Note Cantonese vs. Mandarin pronunciation differences for HK/Macau visitors
4. **Historical accuracy**: All dynasty references must be factually grounded
5. **Art prompt safety**: No depictions of real historical figures without consent framing
6. **Attribution**: Always credit the classical poets/styles being referenced

---

*SKILL.md v2.0.0 — Cultural Naming & AI Art Creation by XiaoAIPensieve*
