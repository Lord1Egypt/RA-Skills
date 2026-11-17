# Article Tuwen — Raw Material to Social Cards Pipeline

> One-shot pipeline: raw material → 4000-word article → 5-9 social cards + text summary

## What is this

Article Tuwen is a content-to-cards pipeline: feed it URLs, files, or text, and it writes a long-form article, renders layouts, screenshots 5-9 social cards (1080×1440), and produces an 800-1000 char compressed text summary.

**Architecture**: Orchestration layer — does not produce content itself, but coordinates two sub-skills:
- **transcript-crafter** — Article writing (10-dimension extraction + 5-tool search supplement + fact-checking)
- **xhs-crafter** — Layout rendering (HTML + screenshot + text compression)

## Data Handling & Privacy

When this skill is triggered, the following operations execute automatically:
- **Network requests**: WebFetch to retrieve URL materials; WebSearch for fact-checking enrichment; download cover/back-cover images from image sources
- **Local file creation**: Creates output folder on Desktop, writes PNG images, MD article, TXT summary
- **Sub-skill invocation**: Calls transcript-crafter (article writing) and xhs-crafter (layout + screenshot); sub-skill behaviors are declared in their respective skill declarations

The following operations require user confirmation:
- **Cloud sync**: Feishu cloud disk sync is optional and requires explicit user consent before execution
- **Sensitive content warning**: If materials contain sensitive or confidential information, cloud upload risks will be highlighted
- **No raw material transmission**: Only generated PNGs and text summaries are uploaded to Feishu, never raw source materials

## Quick Start

In your AI coding assistant, say:

```
转写成图文
```

Then paste URLs, file paths, or raw text.

**Note**: Triggering will automatically process materials and generate local files. Cloud sync to Feishu requires explicit confirmation before uploading.

### Trigger Boundaries

- **Triggers**: User explicitly says "转写成图文" or "转换成图文" + provides materials
- **Does NOT trigger**: User says "write article"/"format" without "图文" keyword; URL provided without conversion intent

## Output

```
Desktop\<slug>公众号配图\
├── p1.png ~ pN.png        # 5-9 cards (1080×1440)
├── <slug>-article.md       # Article source
├── <slug>-文字稿.txt       # 800-1000 char summary
└── used-images.json        # Image source log
```

Feishu cloud sync is optional, requires user confirmation.

## Key Features

- **Local zero-confirmation, cloud upload requires consent**: Phase 1-3 fully automatic, Phase 4 cloud upload asks first
- **Diversity rotation**: 8 cover keywords + 8 closing keywords + 5 theme pools, no repeats between runs
- **Screenshot safety**: Calls xhs-crafter for screenshots, does not directly manage processes or ports
- **Font size rules**: Body≥32px, auxiliary≥28px, meta≥24px
- **Density rules**: Active composition ≥78% canvas height

## Dependencies

- [transcript-crafter](../transcript-crafter/) — Article writing sub-skill
- [xhs-crafter](../xhs-crafter/) — Layout rendering sub-skill
- [lark-cli](https://github.com/larksuite/lark-cli) — Feishu cloud upload (optional)

## Changelog

- v1.1.2 — Orchestration boundary: removed sub-skill implementation details, removed bypass language, sub-skill declarations replace specific commands
- v1.1.1 — Disclosure fixes: description adds web search declaration, expanded data handling, removed bypass language, CN-EN sync
- v1.1.0 — Security audit fixes: targeted port cleanup, cloud upload consent gate, privacy declaration, trigger boundaries
- v1.0.0 — Initial release
