# Prompt System — Drawing

Use this scaffold when quality matters more than speed.

## Universal Slot Order

Keep the same order so prompts stay portable across image models:

1. **Outcome**
   - children's illustration, coloring page, or learning-card visual
2. **Audience**
   - age band and difficulty level
3. **Subject**
   - who or what must appear
4. **Scene**
   - setting with only essential supporting elements
5. **Style**
   - one style pack only
6. **Composition**
   - portrait or landscape, camera distance, centered or wide
7. **Color mode**
   - full color palette or black outlines only
8. **Constraints**
   - what must stay out, what must stay simple, what must remain printable

## Long-Form Template

```text
Create an original [outcome] for children aged [age band].
Subject: [subject].
Scene: [simple scene].
Style: [style pack].
Composition: [orientation], [camera distance], [focal arrangement].
Color mode: [palette or black outlines only].
Keep it [tone].
Must include: [1-3 essentials].
Must avoid: text, watermark, cropped subject, [other blockers].
If printable: white background, clean margins, uncluttered page.
```

## Short-Form Template

Use this when the model follows simple instructions well:

```text
[Outcome] for ages [age band]: [subject] in [scene], [style pack], [composition], [color mode], friendly and simple, no text or watermark.
```

## Stable Series Block

For packs or multi-page sets, keep one unchanged block:

```text
Always keep: same line style, same character proportions, same face shape, same palette family, same framing, same age appropriateness.
```

Then add only the page-specific content under it.

## Iteration Loop

After each generation, label the main failure:
- too much detail
- wrong mood
- weak composition
- broken anatomy
- dirty line art
- inconsistent style

Then change only one lever:
- simplify subject count
- tighten background
- switch style pack
- increase outline thickness
- change camera distance
- add or remove a specific negative constraint

## Negative Constraint Bank

Common blockers:
- no text
- no watermark
- no logo
- no extra fingers
- no cropped face
- no scary expression
- no busy background
- no tiny decorative details
- no gray shading for coloring pages

Use only the blockers that matter for the current task.
