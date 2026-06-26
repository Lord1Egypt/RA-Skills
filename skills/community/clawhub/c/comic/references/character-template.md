# Character Definition Template

To keep characters consistent across multiple pages, create `characters/characters.md` first.

## File Structure

```markdown
# Character Definitions - <Comic Title>

**Art**: <art>
**Tone**: <tone>
**Language**: <zh|en|ja|ko>

---

## Character 1: <Name>

**Role**: <protagonist | mentor | antagonist | narrator>
**Age**: <age or age range>

**Appearance**:
- Face shape: <face shape>
- Hair: <hair style, color, and length>
- Eyes: <eye features>
- Build: <body type and posture>
- Distinguishing features: <glasses, scar, beard, signature accessory>

**Costume**:
- Default outfit: <default clothing>
- Color palette: <main colors>
- Accessories: <tools, bag, hat, and so on>

**Expression Range**:
- Neutral: <description>
- Happy/Excited: <description>
- Thinking/Confused: <description>
- Determined: <description>

---

## Reference Sheet Prompt

Character reference sheet in <art> style:

[ROW 1 - <Name>]
- Front view: <description>
- 3/4 view: <description>
- Expression sheet: Neutral | Happy | Focused | Worried

COLOR PALETTE:
- <Name>: <color list>

White background, clear labels under each character.
```

## Usage Rules

- Every major character should have a stable appearance description.
- Be specific about colors, clothing, and accessories.
- Reuse the same character document across all comic page prompts.
- If the base image model supports `--ref`, generate `characters/characters.png` first and pass that same reference image for every page.
- Include stable defaults, not just generic traits: default outfit, signature prop, color palette, hairstyle, body shape, and any always-visible accessory.
- If a character changes costume or scene state later, write the default look here first and describe the change explicitly in the page-level storyboard.
