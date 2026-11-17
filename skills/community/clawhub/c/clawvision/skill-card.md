## Description:

ClawVision turns an OpenClaw chat session into a tabbed visual summary with HTML, PNG, Markdown, and PowerPoint exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monaxamo](https://clawhub.ai/user/monaxamo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to turn an explicitly selected chat session into a local visual summary, including analytics and exportable HTML, PNG, Markdown, and PowerPoint files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session exports can persist sensitive conversation content to disk.

Mitigation: Use the skill only after explicit user confirmation and only on conversations safe to export; exclude secrets, credentials, personal data, and internal identifiers.

Risk: Chart rendering can fall back to remote ECharts code when a fixed local bundle is unavailable.

Mitigation: Prefer a reviewed, pinned local chart package and disable CDN fallback for sensitive or controlled environments.

Risk: Untrusted summary JSON, slug values, or output paths could affect generated files.

Mitigation: Validate summary JSON against a strict schema, sanitize slugs, and contain all generated output paths to an approved directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monaxamo/skills/clawvision)
- [ClawVision homepage](https://github.com/monaxamo/clawvision)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Local files and agent guidance, including HTML, PNG, Markdown, PowerPoint, JSON status, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read session history after explicit user confirmation and write persistent export files to disk.]

## Skill Version(s):

1.0.13 (source: server release metadata; artifact metadata lists 1.0.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
