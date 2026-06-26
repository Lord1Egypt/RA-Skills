---
name: daily-vocab
description: "One advanced English word every day — IPA pronunciation, etymology, 3 example sentences, and quiz mode. GRE / SAT / IELTS / C2 vocabulary level."
keywords:
  - 每日词汇
  - 今日单词
  - 学个单词
  - 每日一词
  - 高级词汇
  - GRE词汇
  - SAT词汇
  - 英语学习
  - 词汇量
  - 单词记忆
  - daily vocab
  - daily vocabulary
  - word of the day
  - vocabulary
  - advanced vocabulary
  - GRE word
  - SAT word
  - English learning
  - etymology
  - flashcard
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# Daily Vocabulary / 每日词汇

Generate a beautiful vocabulary learning card featuring one advanced English word with complete learning materials.

## Workflow

1. **Get today's date** — Use date to determine word theme. Rotate themes weekly: Mon=emotions, Tue=science, Wed=art/culture, Thu=business, Fri=nature, Sat=philosophy, Sun=daily life.
2. **Select a word** — Choose an interesting, useful but not commonly known English word (GRE/SAT level or above). Use `web_search` to verify meaning and find authentic usage examples. Query: `"[word] definition etymology usage examples"`.
3. **Build the learning card** — Include: word, phonetic transcription, part of speech, definition (EN + CN), etymology/word roots, 3 example sentences (with CN translation), synonyms, antonyms, a memory tip.
4. **Generate the visual** — Create a single-file HTML artifact.

## Visual Design Requirements

Create a flashcard-style learning interface:

- **Layout**: Single large card, centered, with clear sections. Think premium language-learning app aesthetic.
- **Typography**: The word itself in a large, beautiful display font (e.g., Crimson Text, Spectral, Libre Caslon). Phonetics in a monospace font. Body in clean sans-serif.
- **Color scheme**: Soft, focus-friendly palette — muted blues/greens/warm grays. Alternate between light and dark themes based on day of week.
- **Sections**: 
  - Top: Word + Phonetics + Part of Speech
  - Definition block: EN definition, then CN translation
  - Etymology: Root breakdown with visual connectors
  - Examples: 3 sentences with key word highlighted
  - Bottom row: Synonyms | Antonyms | Memory Tip
- **Interactivity**: Click the word to toggle between showing/hiding the Chinese translation (study mode). A "Quiz Me" button that hides the definition and shows it on click.
- **Animation**: Card flips in on load. Sections reveal with stagger.
- **Ad-ready zone**: `<div id="ad-slot-bottom">` below the card (min-height 90px).
- **Footer**: "Powered by ClawCode"

## Word Selection Guidelines

- Prefer words that are: elegant, useful in professional/academic contexts, have interesting etymologies
- Avoid: obscure archaic words nobody uses, basic words everyone knows
- Good examples: "ephemeral", "serendipity", "paradigm", "resilience", "ubiquitous", "cacophony"

## Output

Save as `/mnt/user-data/outputs/daily-vocab.html` and present to user.

---

## 推送管理

```bash
# 开启每日推送（早晚各一次）
node scripts/push-toggle.js on <userId>

# 自定义时间和渠道
node scripts/push-toggle.js on <userId> --morning 08:00 --evening 20:00 --channel feishu

# 关闭推送
node scripts/push-toggle.js off <userId>

# 查看推送状态
node scripts/push-toggle.js status <userId>
```

支持渠道：`telegram` / `feishu` / `slack` / `discord`
