## Description:

Creates magazine-style presentation decks from a topic or outline, with guided layout selection, theme planning, and optional single-file HTML or PPTX output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwbwin](https://clawhub.ai/user/wwbwin)

### License/Terms of Use:

MIT

## Use Case:

External users, creators, and developers use this skill to turn a presentation topic, outline, or source material into a visually polished slide deck for talks, launches, demos, and private sharing. It is best suited to narrative and visual presentations rather than dense data tables or collaborative slide editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can run active content from supplied presentation material.

Mitigation: Use trusted outlines and source content, and review generated HTML before opening or sharing it.

Risk: The generator can automatically open generated files through shell-based preview behavior.

Mitigation: Disable or remove automatic preview behavior when reviewing untrusted decks or running in controlled environments.

Risk: Attacker-controlled output paths could cause generated files to be written in unintended locations.

Mitigation: Use fixed, trusted output directories and avoid passing untrusted output paths to the generator.

Risk: External browser assets can affect offline or reproducible presentation rendering.

Mitigation: Vendor or pin external assets and dependencies when reproducible or offline presentation output is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwbwin/skills/canvasflow-ppt)
- [Layout system](references/layouts.md)
- [Theme presets](references/themes.md)
- [Quality checklist](references/checklist.md)
- [Component reference](references/components.md)
- [Lucide browser bundle](https://unpkg.com/lucide@latest/dist/umd/lucide.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with HTML, JSON outline, and optional PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included scripts can generate timestamped outline JSON, single-file HTML presentations, and PPTX decks.]

## Skill Version(s):

2.0.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
