## Description:

Generate upper-arc Chinese/CJK text icons for packaging labels, seals, badges, banners, and related design assets with configurable fonts, colors, strokes, curvature, canvas, and background.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blizzard-bj](https://clawhub.ai/user/blizzard-bj)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and agents use this skill to render upper-arc Chinese or CJK text for packaging labels, stickers, seal-style badges, banner headings, and similar visual assets. It helps choose rendering parameters and produce inspectable PNG outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated arc text images may be blank, mispositioned, overlapping, or difficult to inspect when transparent backgrounds are used.

Mitigation: Use the white-background preview and strong-pixel checks, then visually verify the generated image before relying on or delivering it.

Risk: Some geometry and validation notes in the documentation may be stale relative to the current script behavior.

Mitigation: Prefer the current rendered output and validation result over older explanatory notes, and rerender with adjusted parameters when visual checks fail.

## Reference(s):

- [Arc Text Icon Parameter Tuning Guide](references/params.md)
- [Available CJK Fonts](assets/sample_fonts.txt)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image files plus Markdown guidance with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a main PNG and a white-background preview PNG; includes visual and strong-pixel verification guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact changelog, released 2026-07-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
