## Description:

Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ken0122](https://clawhub.ai/user/ken0122)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, presales, teaching, conference, and internal presentation authors use this skill to create browser-run slide decks from prompts, notes, images, or PowerPoint files. It helps non-designers choose a visual direction through style previews and then generate responsive HTML presentations with navigation and animations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation files and speaker notes can contain sensitive customer, sales, or internal information.

Mitigation: Only convert or generate decks whose contents the agent is allowed to read, and review generated output before sharing.

Risk: PowerPoint conversion and image processing depend on local Python libraries.

Mitigation: Install python-pptx and Pillow in a virtual environment with pinned versions before using those optional workflows.

Risk: Optional browser editing can retain deck text in the browser profile through auto-save.

Mitigation: Clear saved browser data for the generated deck when editing sensitive material, or skip inline editing for sensitive presentations.

## Reference(s):

- [Frontend Slides README](README.md)
- [Style Presets](STYLE_PRESETS.md)
- [HTML Architecture for Presentations](reference/html-architecture.md)
- [Viewport and Base CSS](reference/viewport-and-base.css)
- [Animation Patterns Reference](reference/animation-patterns.md)
- [PowerPoint Extraction Helper](reference/ppt-extract.py)
- [Image Processing Helpers](reference/image-processing.py)
- [Inline Editing Implementation](reference/edit-button-implementation.md)
- [OpenClaw Documentation](https://docs.openclaw.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated self-contained HTML/CSS/JavaScript presentation files and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce presentation assets, extracted PowerPoint images, processed images, style preview HTML files, and optional browser-editing JavaScript.]

## Skill Version(s):

2.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
