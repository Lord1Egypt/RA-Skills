## Description:

ClawVision Lite exports an OpenClaw session into a lightweight, English-only, self-contained HTML summary file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monaxamo](https://clawhub.ai/user/monaxamo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to turn a selected chat session into a concise local HTML summary for review or sharing. It is intended for simple session visualization when PNG, Markdown, PowerPoint, analytics, multilingual output, and external assets are not needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the selected OpenClaw session history, which may contain private or sensitive content.

Mitigation: Confirm the session before export, avoid sessions containing secrets, and review the generated HTML before sharing it.

Risk: Crafted summary data may inject browser script into the generated HTML.

Mitigation: Use trusted summary inputs and inspect generated HTML before sharing until strict status validation and HTML attribute escaping are added.

Risk: Supplying a slug may allow HTML to be written outside the intended output folder.

Mitigation: Prefer default output naming and avoid user-supplied slugs until slug path containment is added.

## Reference(s):

- [ClawVision project homepage](https://github.com/monaxamo/clawvision)
- [ClawHub skill page](https://clawhub.ai/monaxamo/skills/clawvision-lite)
- [Publisher profile](https://clawhub.ai/user/monaxamo)

## Skill Output:

**Output Type(s):** [text, code, shell commands, files, guidance]

**Output Format:** [Self-contained HTML file with inline CSS and JavaScript, plus concise text guidance and the generated local file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [English-only UI labels; no external assets, CDN, analytics, PowerPoint, or Markdown output.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
