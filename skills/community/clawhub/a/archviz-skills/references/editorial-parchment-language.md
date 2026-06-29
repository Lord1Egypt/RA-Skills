# Editorial Parchment Language

Distilled from [claude-design-card](https://github.com/geekjourneyx/claude-design-card) (MIT) and adapted for **archviz-skills** HTML/card deliverables. archviz remains diagram-first; this reference governs **editorial surfaces** when the brief asks for cards, covers, or publishable HTML — not a full card-generator clone.

---

## Core thesis

| Principle | Meaning for archviz |
|---|---|
| **Warm canvas, not SaaS white** | Default surfaces are tinted cream (`#f5f4ed` / `#faf9f5`), never `#ffffff` or cool slate |
| **Humanist accent** | Terracotta `#c96442` replaces IKB when the host doc is editorial / Anthropic-adjacent — still **max 1 accent** |
| **Serif display + sans UI** | Headlines: Georgia / Newsreader / Noto Serif SC at **500**, never 700. Body/UI: system-ui |
| **Color-block pacing** | Alternate cream canvas → cream card → dark band → accent band. Never same surface twice in a row |
| **Hairline, not shadow** | Depth via 0.5–1px warm borders (`#e8e6dc`). Container ring-shadow only: `0 0 0 1px rgba(0,0,0,.08)` |
| **Caption = finding** | Same as archviz §9 — "V1 只需五屏" not "V1 架构图" |

---

## Token map (Editorial Parchment system)

| Token | Hex | Role |
|---|---|---|
| Parchment | `#f5f4ed` | Page / diagram canvas |
| Ivory | `#faf9f5` | Card face, elevated surface |
| Near-Black | `#141413` | Primary text on light |
| Olive-Gray | `#5e5d59` | Secondary text |
| Stone-Gray | `#87867f` | Meta, captions |
| Border-Warm | `#e8e6dc` | Hairline dividers |
| Dark-Surface | `#30302e` | Contrast band, code/mockup blocks |
| Terracotta | `#c96442` | Single accent — CTA, key node, one data bar |
| Warm-Silver | `#b0aea5` | Text on dark surfaces |

**Contrast**: Parchment/Ivory luminance ≥128 → Near-Black text. Dark-Surface → Ivory/Warm-Silver text.

**Host-document override**: If the brief already uses Warm Paper (`#f5f0eb` + Ink Navy `#1B365D`) or Aver cinnabar (`#A24A2D`), match the host — do not mix Terracotta and IKB in one set.

---

## Typography

| Role | Family | Weight | Notes |
|---|---|---|---|
| Display / headline | Georgia, Newsreader, Noto Serif SC | 400–500 | Negative tracking on large sizes (-0.01em to -0.03em) |
| Body | system-ui, Hanken, Manrope | 400 | line-height 1.55–1.65 |
| Kicker / label | system-ui | 500 | 9–11px, letter-spacing 0.08em, uppercase sparingly |
| Numbers | JetBrains Mono, ui-monospace | 500 | tabular-nums |

**Hard ban**: `font-weight: 700` on serif display; cool blue-gray (`#64748b`, default Mermaid purple); pure white backgrounds.

---

## Format families (HTML deliverables)

Route by **job contract**, not aspect ratio alone.

### Family A — Attention contract (covers / heroes)

Purpose: click or pause — **not** article summary.

```
Primary judgment headline
+ one supporting promise
+ one evidence cue (number / source / contrast)
+ intentional whitespace
```

| Platform | Aspect | Headline share | Headline size |
|---|---|---:|---:|
| WeChat banner | 900×383 | 28–36% | 44–64px |
| Bilibili / YouTube | 1280×720 | 32–42% | 64–92px |
| Vertical story / Douyin | 1080×1920 | 28–34% | 76–104px |

**Safe zones (9:16)**: top 14% weak · center 44–52% primary · bottom 20% weak · right edge free of critical text.

### Family B — Knowledge artifact (content cards)

Purpose: stop, understand, save — not summary slides.

| Mode | Use |
|---|---|
| Editorial Artifact | Default premium knowledge card |
| Dark Magazine Cover | Strong first-card for conflict/contrast |
| Practical Toolkit | Steps, checklists, tutorials |

1080×1440 baseline: headline 64–96px · promise 26–34px · body 24–30px · meta 16–20px.

### Family C — Social square (1080×1080)

Quote card · data hero · general single-column. One focal element per card.

### Family D — Long-form editorial (width-led, auto height)

Broadsheet (800px) · Feature (760) · Reader (720) · Digest (760). Book-grade line-height, marginalia optional.

---

## Surface pacing (multi-section HTML)

```
[Canvas Parchment]
  -> [Card Ivory / Surface-Card #efe9de]
  -> [Dark band #30302e]   // product chrome, code, contrast
  -> [Canvas]
  -> [Terracotta accent band]  // one per page max
```

In **embedded SVG inside Markdown**: use solid fills only; dashed stroke = deferred/vision; 2px Terracotta or IKB = single ritual highlight.

---

## Ask-before-generate (ambiguous briefs)

When platform, aspect, or read-vs-share intent is unclear:

1. State **1 primary format + 2 alternatives** with one-line rationale each.
2. Ask ≤3 questions: platform · read vs share · host palette already established?
3. If user says "your call" or brief is explicit → proceed with primary.

Do not block on clear diagram-only requests (Mermaid/ASCII in Obsidian).

---

## Anti-patterns (from claude-design-card + archviz)

| Anti-pattern | Fix |
|---|---|
| Cover with 4–6 bullet summaries | Compress to judgment + promise + one evidence |
| Equal-weight rounded card grid | One hero + supporting rows; hierarchy via size not color rainbow |
| Shrinking title until unreadable | Split to second card or Family D long-form |
| Cool AI-blue default theme | Apply Editorial or Warm Paper init |
| Serif at 700 | Cap at 500; enlarge type instead |
| Decorative labels | Every kicker must encode category, source, or scope |

---

## Cross-reference

- Palette registration: `DESIGN.md` §2 Editorial Parchment row
- Template skeleton: `templates/html/editorial-card.html`
- SKILL routing: `SKILL.md` §Editorial Mode + Format Families table
- Full upstream spec: [claude-design-card/DESIGN.md](https://github.com/geekjourneyx/claude-design-card/blob/main/DESIGN.md)