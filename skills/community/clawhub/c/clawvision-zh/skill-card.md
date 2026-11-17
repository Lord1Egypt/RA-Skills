## Description:

ClawVision-zh is a local OpenClaw session exporter that summarizes selected session history with a local LLM and writes HTML, Markdown, PowerPoint, and PNG exports to local disk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monaxamo](https://clawhub.ai/user/monaxamo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill when they explicitly want to turn a selected conversation into a shareable visual summary and local export bundle. It supports local review and presentation workflows after the user confirms the session scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected session history can contain credentials, personal data, private identifiers, or internal context that may be written into shareable exports.

Mitigation: Get explicit scope before accessing history, avoid sessions with sensitive content, and review generated files before sharing.

Risk: Custom output slugs or untrusted session content can affect generated local filenames or exported content.

Mitigation: Use trusted output names, keep exports in expected local directories, and inspect outputs before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monaxamo/skills/clawvision-zh)
- [Project homepage from metadata](https://github.com/monaxamo/clawvision-zh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance plus local HTML, Markdown, PowerPoint, and PNG export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses selected session history, local LLM inference, local Python and Playwright execution, and local file writes; artifact metadata states that transcripts are not sent to external APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
