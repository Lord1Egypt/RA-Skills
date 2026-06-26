---
name: contrast-poster-prompt
description: Match the most suitable type from 15 contrast gameplay styles (gender, age, identity, image, scene, object, role, consumption/economy, pre-post state, skill level, cognitive common sense, time-space dislocation, tone/attitude, item function, physique/appearance) based on user needs, generate high-quality English AI drawing prompts and Chinese poster copy.
---

# Contrast Poster Prompt Generator

Based on user needs, select the most suitable type from 15 contrast gameplay styles, and generate high-quality AI image generation prompts.

## Applicable Scenarios

- User wants to create contrast/comparison posters
- User needs creative ideas for short video covers, Xiaohongshu (Red Note), or WeChat public account posters
- User mentions keywords like "contrast", "comparison poster", "AI drawing prompt", "poster design"
- User describes a creative poster need requiring visual impact. Supports multiple formats including split-screen comparison, single image, and combination contrast.

## Workflow

### Step 1: Understand User Needs

Extract key information from user input:
- **Subject/Person**: Who or what?
- **Industry/Track**: Beauty, fitness, education, comedy, pet, knowledge popularization, workplace, traditional Chinese style, handicraft DIY, etc.
- **Platform**: Xiaohongshu (Red Note), Douyin (TikTok), WeChat public account,朋友圈 poster, etc.
- **Format Preference**: Split-screen comparison | Single image | Nine-grid layout | Video cover

If information is incomplete, ask up to 2 clarifying questions; do not ask too many at once.

### Step 2: Match Contrast Type

Based on user needs, select 1-2 best matching types from 15 contrast styles (combinations allowed):

| # | Type | Key Features | Applicable Tracks |
|---|------|--------------|-------------------|
| 1 | Gender Contrast | Male-female behavior swap | Comedy, social topics |
| 2 | Age Contrast | Generational behavior subversion | Parenting, silver economy |
| 3 | Identity Contrast | Professional identity vs hidden skills | Personal IP, store引流 |
| 4 | Image Contrast | External image vs真实 behavior | Personal IP, rural |
| 5 | Scene Contrast | Behavior vs environment mismatch | Short video openings, comedy |
| 6 | Object Contrast | Unconventional interaction objects | Pets, comedy |
| 7 | Role Contrast | Human-pet role swap | Pets, comedy |
| 8 | Consumption/Economic Contrast | Spending power vs external image mismatch | Physical stores, rural, luxury cars |
| 9 | Pre-Post State Contrast | Extreme transformation in short time | Beauty, fitness, home, inspirational |
| 10 | Skill Level Contrast | Ordinary person with顶级 skills | Talent, education, workplace |
| 11 | Cognitive Common Sense Contrast | Subverting大众 common sense | Knowledge科普, health, finance |
| 12 | Time-Space Dislocation Contrast | Mixing elements from different eras | Traditional Chinese style, history, creativity |
| 13 | Tone/Attitude Contrast | Tone严重 mismatched with content | Comedy, parenting, workplace |
| 14 | Item Function Contrast |颠覆 Item用途 | Life hacks, handicraft DIY |
| 15 | Physique/Appearance Contrast | Body type vs ability强烈冲突 | Fitness, talent, workplace |

See `references/contrast-playbook.md` for detailed cases and visual references.

**Combination Contrast**: Can stack 2 types to enhance conflict (e.g., age + skill, identity + consumption).

### Step 3: Generate Prompts

#### A. Split-Screen Comparison Poster (Most Common)

```
A split-screen comparison poster. Left half: [left scene -常规/expected state, detailed description of person, action, environment, lighting]. Right half: [right scene - contrast/subversive state, same person, detailed description]. Same person in both halves, seamless transition at center. Cinematic lighting, high contrast, professional photography, 4K resolution. Clean design with negative space at top/bottom for headline text. Poster layout, vertical orientation, 3:4 aspect ratio.
```

**Key points**:
- Left and right must feature the same person/subject
- Left side is "expected/常规", right side is "contrast/subversive"
- Be specific in descriptions: clothing, expression, action, environment, lighting
- Indicate留白 areas for text

#### B. Single Image Contrast Poster

```
[subject description], showing striking contrast: [contrast detail — presenting conflicting elements within a single frame]. High quality poster, dramatic lighting, vibrant studio colors, 4K resolution, professional commercial photography. Clean composition with headline space reserved. Vertical poster, 3:4 ratio.
```

#### C. Combination Contrast Poster

Stack 2 contrast types:

```
A split-screen poster combining [contrast A] and [contrast B]. Left half: [scene A]. Right half: [scene B]. Same person. Double contrast effect — [brief description of the叠加 effect of two contrasts]. Cinematic, 4K, poster layout.
```

#### D. Cognitive Common Sense Poster (Text-Focused)

```
A knowledge-fact poster design. Left area: large text "[common sense观点]" in clean font, with [corresponding visual element]. Right area: bold red text "[truth]" with [corresponding visual element]. Minimalist infographic style, high contrast colors (dark background, white and red text), modern typography layout, 4K, vertical 3:4 poster.
```

### Step 4: Attach Poster Copy

Attach 1-2 Chinese poster copy suggestions per prompt, format `Topic word ≠ Stereotype tag | Catchphrase`.

## Output Format

```
## 🎯 Selected Contrast Type: [Type Name]

**Why this type**: [One-sentence reason]

**English Prompt**:
[Complete prompt]

**Chinese Translation**:
[Prompt translation]

**Recommended Copy**:
- [Copy 1]
- [Copy 2]

**Applicable Platforms**: [Platform suggestions]
```

## Important Notes

- Always output prompts in English (AI drawing tools respond better to English)
- Include Chinese translation for user understanding
- Split-screen is the most recommended poster format for strongest visual impact
- If user does not specify contrast type, automatically recommend the optimal type based on track and theme
- Support generating multiple options (up to 3) for a single poster for user selection