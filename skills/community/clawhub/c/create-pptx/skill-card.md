## Description:

Create PowerPoint presentations (PPTX) using Python and python-pptx, including timelines, charts, diagrams, slide layouts, custom colors, shapes, connectors, text formatting, slide transitions, and WPS compatibility guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottliu007](https://clawhub.ai/user/scottliu007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to generate editable PowerPoint decks from requested content, data, timelines, and presentation structures, including WPS-compatible progressive reveals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency changes in python-pptx may affect generated slide layout or XML behavior.

Mitigation: Install the skill in a dedicated virtual environment and pin python-pptx when reproducible output matters.

Risk: Generated decks may contain mixed-language defaults or labels if localization is not specified.

Mitigation: Tell the agent the required presentation language and review generated slide text before sharing.

Risk: Click-triggered animations may not behave reliably in WPS.

Mitigation: Use multi-slide progressive reveals with fade transitions for WPS-compatible presentations.

Risk: Template assets from Slidesgo may require attribution when used.

Mitigation: Keep the required credits slide or attribution when using those templates.

## Reference(s):

- [PPTX patterns](references/pptx-patterns.md)
- [Charts](references/charts.md)
- [Standard slides](references/standard-slides.md)
- [WPS compatibility](references/wps-compat.md)
- [ClawHub skill page](https://clawhub.ai/scottliu007/skills/create-pptx)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown with Python and shell code blocks plus generated PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Python scripts and .pptx files in the user's workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
