## Description:

Send multimedia content to Feishu (Lark) via API, including images, audio, video, rich text, and interactive cards for users or groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuan-huicheng](https://clawhub.ai/user/yuan-huicheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to send generated or local media content to Feishu or Lark users and groups through API calls. It is suited for posting text, images, audio, video, rich text posts, and interactive cards when Feishu credentials and recipients are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send private media or workplace chat content externally to Feishu immediately after invocation.

Mitigation: Configure credentials and recipients deliberately, and confirm the content and destination before invoking send functions or CLI commands.

Risk: Audio and video conversion can overwrite derived local media files without safeguards.

Mitigation: Avoid running conversion in shared or untrusted directories until overwrite and cleanup behavior is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuan-huicheng/skills/ali-feishu-sender)
- [Publisher profile](https://clawhub.ai/user/yuan-huicheng)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Python function calls, CLI commands, and JSON-like API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload media files and send messages to external Feishu or Lark recipients.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
