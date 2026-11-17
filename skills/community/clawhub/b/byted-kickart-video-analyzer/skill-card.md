## Description:

Analyzes local or downloaded short videos to extract metadata, shot breakdowns, product details, and Seedance-oriented video generation data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to validate, upload, and analyze short MP4/MOV videos. It returns structured video metadata, product information, shot-level analysis, and Seedance-format JSON for downstream creative workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos are sent to an external Volcengine/Ark service for processing.

Mitigation: Use the skill only when external processing is approved, and avoid submitting sensitive or restricted media.

Risk: The workflow asks for cloud credentials and may expose them in chat output or logs.

Mitigation: Provide tightly scoped, disposable credentials through a secure environment mechanism, avoid pasting long-lived AK/SK values into chat, and rotate any keys already used.

Risk: The version-check workflow can return a command to update the skill.

Mitigation: Review the update command, package source, and integrity information before approving or running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-kickart-video-analyzer)
- [Publisher profile](https://clawhub.ai/user/volcengine-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, json, guidance]

**Output Format:** [Markdown user responses with JSON output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces original analysis JSON and Seedance-format JSON; inputs are local MP4/MOV videos up to 60 seconds, 50 MB, and at least 480p.]

## Skill Version(s):

1.0.7 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
