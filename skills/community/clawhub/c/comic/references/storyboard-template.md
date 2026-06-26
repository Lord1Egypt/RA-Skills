# Storyboard Template

Use `storyboard.md` to define the narrative flow before finalizing page prompts.

## Recommended Structure

```markdown
---
title: "<comic title>"
topic: "<topic summary>"
art: "<art>"
tone: "<tone>"
layout: "<layout>"
aspect: "3:4"
content_scope: "standard"
language: "en"
panels_per_page: 3
page_count: 4
---

# <comic title>

**Character Reference**: characters/characters.png

## Cover
**Filename**: 00-cover-topic.png
**Core Message**: <one-line hook>
**Visual Focus**: <main cover concept>
**Prompt Notes**:
- <note 1>
- <note 2>

## Page 1
**Filename**: 01-page-topic.png
**Core Message**: <what this page must convey>
**Scene**: <location and situation>
**Characters**:
- <character 1>
- <character 2>
**Continuity Anchors**:
- <what must stay consistent from the previous page: outfit, prop, location, time of day, injuries, etc.>
**Panel Count**: 3
**Panel Plan**:
- Panel 1: <content>
- Panel 2: <content>
- Panel 3: <content>
**Page Hook**: <transition to next page>

## Page 2
...
```

## Rules

- Keep one clear narrative purpose per page.
- Cover pages should establish the hook and tone.
- Page filenames should match the final image naming pattern.
- Use `Page Hook` when the page should transition strongly into the next one.
- If a page depends on character continuity, list the key characters explicitly in that page block.
- For multi-page comics, add `Continuity Anchors` to every page so prompts preserve outfit, props, location, and scene progression.
- Decide the aspect ratio, total content scope, and panel density before locking prompts.

## Minimum Fields

For each page after the cover, include at least:

- `Filename`
- `Core Message`
- `Scene`
- `Characters`
- `Continuity Anchors`
- `Panel Count`
- `Panel Plan`
