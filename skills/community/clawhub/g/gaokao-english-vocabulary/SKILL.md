---
name: gaokao-english-vocabulary
description: >
  This skill generates interactive "高考英语词汇频率分级系统" (Gaokao English Vocabulary
  Frequency Grading System) webpages. It creates beautiful, dark-themed, single-page HTML
  study tools that classify English vocabulary by exam frequency based on real Gaokao (Chinese
  College Entrance Exam) data from 1977-2025. Each word/phrase is tagged with exam frequency,
  mastery level (145-essential / must-know / general / familiar), and wrong-word warnings.

  This skill should be used when:
  - User asks to create a Gaokao English vocabulary study tool or webpage
  - User wants to build an English word frequency classification system for exam prep
  - User wants a dark-themed interactive vocabulary learning page with search, filter, and level-based organization
  - Keywords: 高考英语词汇、词汇分级、频率统计、vocabulary frequency、Gaokao English
---

# Gaokao English Vocabulary Frequency Grading System

## Overview

This skill produces a self-contained interactive HTML webpage (`gaokao_english_vocabulary.html`) plus an external data file (`vocab_data.js`) that together form a comprehensive vocabulary study tool for Chinese Gaokao English preparation.

The system classifies 4000+ words and 800+ phrases into 6 frequency levels each (12 levels total), with mastery tags, wrong-word warnings, search, multi-filter, and collapsible sections — all in a responsive dark theme.

## Architecture

### File Structure

```
gaokao_english_vocabulary.html   # Main page (self-contained HTML + CSS + JS)
vocab_data.js                    # External vocabulary data (loaded via <script src>)
```

The data file is separated from HTML to keep the page loadable even with large datasets. The HTML contains all styling and logic inline.

### Data Format (`vocab_data.js`)

Each entry in the `VOCAB` array follows one of two formats:

**Word format:**
```javascript
{
  w: "abandon",        // word
  s: "vt.",            // part of speech
  d: [{m: "放弃", c: 28}],  // definitions array: [{meaning, exam_count}]
  l: 2,                // level (1-6)
  v: "must",           // mastery: "145" | "must" | "normal" | "know"
  p: "əˈbændən",       // phonetic (optional)
  e: true,             // has wrong-word warning (optional)
  t: "易写成abanden"    // wrong-word tip text (optional)
}
```

**Phrase format (flat):**
```javascript
{
  w: "a great deal of",  // phrase
  s: "phr.",              // part of speech (always "phr.")
  m: "大量的",            // meaning (flat string, not array)
  c: 15,                 // exam frequency count
  i: "normal",           // mastery: "145" | "must" | "normal" | "know"
  e: false               // wrong-word warning (optional)
}
```

### Level System

**Words (6 levels by exam count):**

| Level | Name | Range | Color |
|-------|------|-------|-------|
| Lv.1 | 超高频 Super High | ≥40 times | Green #3fb950 |
| Lv.2 | 高频 High | 20-39 times | Blue #58a6ff |
| Lv.3 | 次高频 Sub-High | 10-19 times | Yellow #e3b341 |
| Lv.4 | 中频 Medium | 5-9 times | Red #f85149 |
| Lv.5 | 低频 Low | 2-4 times | Purple #a371f7 |
| Lv.6 | 超低频 Very Low | 0-1 times | Gray #484f58 |

**Phrases (6 levels by exam count):**

| Level | Name | Range | Color |
|-------|------|-------|-------|
| P1 | 超高频 | ≥20 times | Cyan #38bdf8 |
| P2 | 高频 | 12-19 times | Teal #22d3ee |
| P3 | 次高频 | 8-11 times | Blue #38bdf8 |
| P4 | 中频 | 5-7 times | Light Blue #7dd3fc |
| P5 | 低频 | 3-4 times | Soft Blue #93c5fd |
| P6 | 超低频 | 1-2 times | Slate #94a3b8 |

### Mastery Levels

| Tag | Label | Color | CSS Class |
|-----|-------|-------|-----------|
| 145 | 🔥 145分必掌握 | Green bg | `.m145` |
| must | ✅ 必须掌握 | Yellow bg | `.mmust` |
| normal | 📖 一般掌握 | Gray bg | `.mnormal` |
| know | 👀 了解意思 | Dark bg | `.mknow` |

## Key Features

### 1. Sticky Top Bar
Header, stats, search box, and filter buttons are all in a `position:sticky` top bar that stays visible during scroll.

### 2. Filter Buttons with Frequency Annotations
Each filter button shows the level name and a small `<small>` tag with the exam count range (e.g., "20-39次").

### 3. Sticky Level Headers
Each level section header (e.g., "🟢 Lv.1 超高频") uses `position:sticky` so it remains visible while scrolling through cards in that section.

### 4. Collapsible Sections
Each level section can be expanded/collapsed by clicking its header. Sections start collapsed and expand with a smooth `max-height` transition.

### 5. Card Design
Each vocabulary card displays:
- Frequency bar (width proportional to exam count)
- Word + part of speech + phonetic
- Meaning(s) with per-meaning count (for words with multiple meanings)
- Mastery badge + exam count badge
- Wrong-word tip (if applicable)

### 6. Search
Real-time search across word, meaning, and phonetic fields. Supports both word `d[].m` and phrase `m` formats.

### 7. Multi-Filter
Filter buttons for: All, 6 word levels, All phrases, 6 phrase levels, 145-essential, Wrong-word.

## Page Layout Structure

```
┌─────────────────────────────────────┐
│  📚 高考英语词汇频率分级系统          │  ← Sticky top bar
│  Stats: 总词汇 / 单词 / 词组 / ...   │
│  [🔍 搜索框]                         │
│  [全部] [Lv.1≥40次] [Lv.2 20-39次]… │  ← Filter buttons with annotations
├─────────────────────────────────────┤
│  🟢 Lv.1 超高频（≥40次考查） 161 词 ▼ │  ← Sticky level header
│  ┌──────────┐ ┌──────────┐          │
│  │  card    │ │  card    │          │  ← Card grid
│  └──────────┘ └──────────┘          │
│  🔵 Lv.2 高频（20-39次考查） 415 词 ▼ │
│  ┌──────────┐ ┌──────────┐          │
│  │  card    │ │  card    │          │
│  └──────────┘ └──────────┘          │
│  ... (remaining levels)              │
│  📌 词组 P1 超高频（≥20次考查） 22 词 ▼│
│  ... (phrase levels)                 │
└─────────────────────────────────────┘
```

## Workflow

### Generating a New Vocabulary System

1. **Gather vocabulary data** — Collect word lists with:
   - Word, part of speech, meaning, exam frequency count
   - Mastery level assignment (145 / must / normal / know)
   - Wrong-word warnings with tip text (optional)

2. **Generate `vocab_data.js`** — Format data as `var VOCAB = [...];` following the data format above. Words use `d:[{m,c}]` array; phrases use flat `m` and `c` fields.

3. **Create the HTML page** — Use the template structure from `references/template_structure.md`. Key sections:
   - `<style>` block with all CSS (dark theme, card styles, level colors, responsive breakpoints)
   - Top bar with header, stats, search, filter buttons
   - Main content area `<div id="mainContent">`
   - `<script>` block with: `getLevel()`, `getMaxCount()`, `renderCard()`, `render()`, `filterWord()`, `toggleSection()`, `setFilter()`, `doSearch()`, `updateStats()`

4. **Ensure all 12 levels are non-empty** — If any level has zero entries, either add more vocabulary or adjust the count thresholds.

5. **Validate data integrity** — Run Python checks:
   - Every entry has `w` and `s` fields
   - Every entry has either `d[]` (words) or `m` (phrases) for meaning
   - Every entry has `v` (words) or `i` (phrases) for mastery
   - No NaN or null values

6. **Test in browser** — Start HTTP server (`python -m http.server 8080`) and verify:
   - Stats display correct totals
   - All filters work
   - Search works across word/meaning/phonetic
   - Collapsible sections expand/collapse
   - Sticky headers and top bar work during scroll

## CSS Design Principles

- **Dark theme**: Background `#0d1117`, cards `#161b22`, borders `#30363d`
- **Top bar gradient**: `linear-gradient(135deg, #1a1f2e, #0d1117)`
- **Card hover**: Border color changes to `#58a6ff`, slight translateY lift + box-shadow
- **Responsive grid**: `grid-template-columns: repeat(auto-fill, minmax(300px, 1fr))`
- **Mobile**: Single column at `max-width: 600px`
- **Level header sticky**: `position: sticky; top: 0; z-index: 50; box-shadow: 0 2px 8px rgba(0,0,0,0.3)`
- **Sticky top bar**: `position: sticky; top: 0; z-index: 100; backdrop-filter: blur(12px)`

## Customization Points

- **Exam year range**: Update the subtitle text (default: "1977—2025年")
- **Level thresholds**: Adjust in `getLevel()` function
- **Level colors**: Update CSS `.level-X .level-header` and `.level-X .word-bar` rules
- **Mastery labels**: Update `getMasteryLabel()` function
- **Signature/署名**: Add below subtitle in header section
- **Additional filters**: Add new cases in `setFilter()` and `filterWord()` switch statements

## Resources

### references/template_structure.md
Complete HTML template structure with all CSS styles and JavaScript functions. Use as the starting point when generating a new page — copy and customize the thresholds, colors, and data.

### scripts/generate_vocab.py
Python script that generates `vocab_data.js` from a structured vocabulary source. Demonstrates the data generation workflow including word/phrase classification, mastery assignment, and JS output formatting.
