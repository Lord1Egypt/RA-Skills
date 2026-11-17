## Description:

ClawVision turns an OpenClaw chat session into a local visual summary with self-contained HTML, PNG tab screenshots, Markdown, and PowerPoint exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monaxamo](https://clawhub.ai/user/monaxamo)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use ClawVision to create exportable visual summaries of explicitly selected chat sessions for review, sharing, or presentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads selected OpenClaw session history and can export private conversation content.

Mitigation: Run it only after explicit user confirmation, avoid sessions containing secrets or personal data, and review generated files before sharing.

Risk: Generated HTML and export files may contain model-produced or user-provided content.

Mitigation: Treat generated HTML as untrusted until reviewed; keep output local and validate rendered content before opening broadly or distributing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/monaxamo/skills/clawvision-publish-106)
- [Project homepage](https://github.com/monaxamo/clawvision)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with local export files: self-contained HTML, PNG screenshots, Markdown summary, and PowerPoint deck.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are written locally after explicit user confirmation of session scope.]

## Skill Version(s):

1.0.6 (source: artifact/SKILL.md metadata.version and evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
