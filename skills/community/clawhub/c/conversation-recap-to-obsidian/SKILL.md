---
name: conversation-recap-to-obsidian
description: Build high-value Obsidian daily and weekly review notes from conversation or existing markdown notes. Use this skill whenever the user asks to summarize the current chat into Obsidian, append a structured session recap, regenerate a daily summary from a full daily note, create or refresh a weekly report, merge same-topic work across multiple days, group work by project/task instead of by date, or extract structured review notes with conclusions, key points, tags, and wikilinks.
---

# Conversation Recap to Obsidian

This skill turns raw conversation or existing Obsidian markdown into **review-ready notes**, not generic summaries. Treat the whole daily/weekly note as input content regardless of who wrote each part.

The default goal is to help the user answer:
- What were the main things done?
- What problems did those things solve?
- What were the key points?
- What conclusions or outputs matter later?
- Which notes/documents should be linked for follow-up?

## Use this skill for

- writing a structured recap of the current conversation into Obsidian
- appending a single session entry into a daily note
- regenerating a daily summary by reading the full daily note first
- creating a weekly report from multiple daily notes
- merging a multi-day thread into one weekly module
- replacing stale generated summary blocks while preserving all non-target content
- producing Obsidian wikilinks for relevant artifacts
- consolidating notes that may contain mixed content from humans, this assistant, and other AI/tools

## Core design

Split the work in three layers:

1. **Entry layer = raw work-item capture**
   - append a single session recap into the daily note
   - preserve concrete issue / solution / conclusion / key point details
   - act as the source material for later daily and weekly synthesis

2. **Daily summary layer = same-day aggregation**
   - read the full daily note
   - merge duplicate work threads
   - compress the day into a small number of reusable conclusions

3. **Weekly layer = cross-day synthesis**
   - merge same-topic work across multiple days
   - rank larger / more complex items first
   - avoid day-by-day流水账

Use scripts when they improve reliability. Do not avoid them just to stay “pure prompt only.”

## Daily note target

Default path:
- `daily/YYYY/MM/YYYY-MM-DD.md` (organized by year and month)
- Users may override the base directory through local config

## Mode 1: Session recap mode

Use this when the user has just finished one conversation or one work block and wants to **record a new entry** instead of refreshing the whole day.

### Session recap principle

Create a new item in the daily note as source material for later summaries.

### Default entry structure

```markdown
#### 事项标题 — HH:mm

- **问题**: ...
- **方案**: ...
- **结论**: ...
- **关键点**: ...
- **关联**: [[...]] · [[...]]
- **标签**: #tag-a #tag-b
```

### Session recap guidance

- Prefer one concrete work item per entry.
- If the conversation truly covered multiple unrelated things, either split into 2 entries or name the entry at a higher level.
- Keep each field tight and useful.
- The title should describe the work item, not just say “对话总结”.
- Use tags sparingly; 1-3 strong tags are enough.
- Preserve document hierarchy: session entries belong in the raw entry section of the daily note, and the generated `## 今日总结` block should stay as a higher-level summary section near the end of the note.
- When appending an entry to a daily note that already contains `## 今日总结`, insert the new entry **before** the generated summary block, then refresh the summary if needed.

## Mode 2: Daily summary mode

A daily summary is **regenerable**. It is not an append-only log.

When asked to refresh the daily summary:
1. Read the full daily note.
2. Treat the whole note as usable source material regardless of whether parts were written by a person or another AI/tool.
3. Ignore only the previous generated summary block for this skill to avoid recursive self-copying.
4. Extract the day’s main work items from the note content.
5. Compress them into a concise review section.
6. Replace only the generated summary block.

### Default daily output shape

```markdown
## 今日总结

- 今日主要事项：...
- 核心解决的问题：...
- 关键点：...
- 结论/产出：...
- 相关文档：[[...]] · [[...]]
- 标签：#tag-a #tag-b
```

### Daily writing guidance

- Prefer outcomes over chronology.
- Merge duplicate points.
- If multiple sessions worked on the same thing, describe it once more strongly.
- If there are multiple unrelated threads, mention the top 2-3, not every small action.
- Keep links limited to durable notes or outputs.
- Treat the entire note as evidence; do not downgrade a section just because it was written by another AI/tool.
- Ignore only the current skill's previous generated summary block when refreshing, so the summary does not recursively paraphrase itself.
- Keep the summary compact and high-density rather than long and chatty.

## Mode 3: Weekly summary mode

Default path:
- `weekly/YYYY/MM/YYYY-MM-DD.md` (organized by year and month)

The date is the **Sunday** of that reporting week.

### Weekly summary principle

A weekly report should be organized by **work item**, not by day.

The correct unit is not “Tuesday” or “Wednesday.”
The correct unit is “the import pipeline fix,” “the skill redesign,” “the database migration,” etc.

If one work item spans 3 days, merge those 3 daily notes into one weekly module.

### Weekly frontmatter and module structure

Weekly notes should include frontmatter like:

```markdown
---
word_count: 1234
type: weekly-summary
week_start: 2026-03-23
week_end: 2026-03-29
---
```

Then the body uses modules like:

```markdown
### 1. 事项名
- 涉及日期：2026-03-17、2026-03-18、2026-03-19
- 核心解决的问题：...
- 关键点：...
- 结论/产出：...
- 相关文档：[[...]] · [[...]]
- 标签：#tag-a #tag-b
```

### Weekly ranking rule

Sort weekly items by importance using these signals:
1. number of involved days
2. amount of structured content / subpoints
3. visible complexity or decision weight

Larger, longer-running, more complex items should appear earlier.

### Weekly writing guidance

- Merge same-topic work across days.
- Avoid day-by-day流水账.
- Avoid vague weekly overviews.
- Name each item in a way the user can recognize later.
- Prefer 2-5 strong modules over 12 weak fragments.
- If a single work item appears in several daily notes, produce one merged module instead of repeating it by date.
- When source material is sparse or uneven, still try to infer the strongest few work modules from headings, bullets, and existing summary sections.
- Keep each module concise; the default should read like a crisp weekly review, not a transcript.

## Tagging guidance

Tags are optional but useful.

### Principles

- Prefer existing tags already present in the note.
- Add tags only when they improve retrieval or weekly grouping.
- Keep tags lightweight.
- Good tag sources:
  - project or product name
  - work type (`#summary-skill`, `#线上排障`)
  - technical topic (`#jwt`, `#auth`, `#obsidian`)

### Avoid

- over-tagging
- generic tags with no retrieval value
- tags that merely restate the obvious

## Safe rewrite rule

Generated sections should be wrapped with markers so they can be replaced safely:

```markdown
<!-- AI_SUMMARY_START -->
...
<!-- AI_SUMMARY_END -->
```

Preserve all non-target content outside the markers.

## Bundled script

Use the bundled script for stable maintenance tasks:
- `scripts/recap_manager.py`

The script is publishable because it supports shared defaults plus local overrides.
Resolve configuration in this order:
1. CLI arguments
2. `config.json` next to the skill
3. built-in defaults

### Commands

Append a session entry:

```bash
python scripts/recap_manager.py append-entry \
  --title "JWT验签修复与线上排障" \
  --problem "登录后 401，被踢回" \
  --solution "补 JWKS 公钥验签并修正 issuer" \
  --conclusion "测试和正式环境恢复正常" \
  --key-points "先确认 token claims，再加严格校验" \
  --links "app/core/auth/jwt_auth.py,deploy/config.k8s.yaml" \
  --tags "jwt,auth,线上排障"
```

Refresh a daily summary:

```bash
python scripts/recap_manager.py refresh-daily-auto --date 2026-03-25
```

Generate a weekly report:

```bash
python scripts/recap_manager.py generate-weekly-auto --mode last-week
```

## Important constraints

- Do not invent documents or wikilinks.
- Prefer documents explicitly connected to the current work item; do not sweep unrelated paths from the whole note into “相关文档”.
- Do not blindly append a second stale summary if the user asked for refresh/regeneration.
- Do not reduce weekly review into a chronological diary.
- If source notes are weak, still try to infer stable work modules from headings and structured bullets.

## Success bar

A good result lets the user quickly review:
- what the major work items were
- what each item actually solved
- why it mattered
- what durable outputs or notes exist
- which tags or themes recur across the day or week
