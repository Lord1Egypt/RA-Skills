## Description:

ClawVision East Edition turns selected OpenClaw conversations into local visual summary exports in HTML, Markdown, PowerPoint, and PNG using local LLM summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monaxamo](https://clawhub.ai/user/monaxamo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they explicitly want to convert an OpenClaw session into a shareable, exportable visual summary while keeping processing local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated exports can include sensitive conversation content from selected session history.

Mitigation: Use the skill only after confirming the intended session scope, and review or redact generated files before sharing them.

Risk: Generated HTML can include unsafe model-controlled checklist status attributes.

Mitigation: Validate checklist status values against the expected ready, pending, or blocked values and review generated HTML before opening or distributing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monaxamo/skills/clawvision-ee)
- [Project homepage](https://github.com/monaxamo/clawvision-ee)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance plus local HTML, Markdown, PowerPoint, and PNG export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses selected language, visual preset, accent color, font, layout, and export format settings before generating local files.]

## Skill Version(s):

1.0.8 (source: server release evidence and artifact frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
