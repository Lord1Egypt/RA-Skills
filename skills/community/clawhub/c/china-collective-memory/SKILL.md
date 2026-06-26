---
name: china-collective-memory
description: Search and browse Chinese collective-memory anchors across 1935-2025 using decade-based reference files that organize events, sensory cues, prompts, and cultural context for reminiscence, cultural-history, and intergenerational storytelling work.
---

# china-collective-memory

> A knowledge skill providing searchable Chinese collective memory anchors
> spanning 1935-2025, organized by era, event type, and cultural theme.

## Description

This skill provides access to more than 12,000 Chinese historical collective
memory anchors. Each anchor includes sensory cues, narrative prompts, and
cultural context. It is useful for agents working with Chinese cultural
history, reminiscence, oral history, or intergenerational storytelling.

## Data Structure

Each anchor contains:

- `id`, `year`, `time_bucket`, `event_type`
- `title` (Chinese), `motivation`, `tags`
- sensory cues: `visual`, `auditory`, `olfactory`, `tactile`, `gustatory`
- `probe_question` (Chinese)
- `cultural_context` (Chinese)

## How to Use

- Browse by era in the `references/` directory.
- Each file covers one decade-style bucket:
  `1935-1949.md`, `1950-1959.md`, `1960-1969.md`, `1970-1979.md`,
  `1980-1989.md`, `1990-1999.md`, `2000-2009.md`, `2010-2019.md`, and the
  current 2020s bucket `2020-2026.md`.
- Search within the reference files by keyword, year, tag, or event type.
- Use sensory cues to enrich conversations about specific time periods.
- Use probe questions as conversation starters, then follow the person's own
  memory rather than reciting history.
- Treat the dataset as a memory aid, not as a substitute for lived experience.

## Eras

- `1935-1949`: War, occupation, and founding years (`战乱与建国初期`)
- `1950-1959`: Early PRC and reconstruction (`新中国建设初期`)
- `1960-1969`: Scarcity and political upheaval (`困难年代与政治动荡`)
- `1970-1979`: Late collective era and transition (`集体年代后期与转折`)
- `1980-1989`: Reform, opening, and urban change (`改革开放与城市变化`)
- `1990-1999`: Marketization and media expansion (`市场化与大众传媒扩张`)
- `2000-2009`: Digitization and rapid growth (`数字化起步与高速发展`)
- `2010-2019`: Mobile internet and social transformation (`移动互联网与社会转型`)
- `2020s`: Pandemic era and recent life-world shifts (`疫情年代与近期生活变迁`)

## Working Notes

- This skill is reference-only. It does not require tools, APIs, or a storage
  layer.
- The source material is in Chinese; use it directly when working with Chinese
  speakers, or translate selectively when the host workflow needs bilingual
  output.
- When using anchors in conversation, keep historical framing brief and let the
  person's own associations lead.

## Note

This skill contains reference data only. It can be used by any agent regardless
of persona or platform.
