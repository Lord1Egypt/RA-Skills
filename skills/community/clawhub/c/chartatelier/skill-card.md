## Description:

Turn one sentence of intent into a presentation-grade business diagram, delivered as a high-resolution PNG plus an editable SVG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengjianli0721](https://clawhub.ai/user/fengjianli0721)

### License/Terms of Use:

MIT-0

## Use Case:

External users preparing slide decks, tender documents, and white papers use ChartAtelier to turn a concise requirement into a structured business diagram with editable source and export-ready image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The renderer fallback's local-file access could expose local files, and the skill's tool scope and part of its checklist were not fully assessed.

Mitigation: Review the renderer and checklist before installation, and avoid providing sensitive local files as diagram inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengjianli0721/skills/chartatelier)
- [Diagram selection guide](artifact/references/diagram-selection.md)
- [Visual specification](artifact/references/visual-spec.md)
- [Render pipeline guide](artifact/references/render-pipeline.md)
- [QA checklist](artifact/references/qa-checklist.md)

## Skill Output:

**Output Type(s):** [HTML, SVG, PNG, JSON, Markdown]

**Output Format:** [Single-file HTML diagram, editable SVG, high-resolution PNG, JSON QA report, and Markdown hand-off note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Five deliverables per diagram; the PNG is exported at 2× with a long edge of at least 3000 px. The skill requires placeholders such as XX% when trustworthy data is unavailable.]

## Skill Version(s):

1.0.2 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
