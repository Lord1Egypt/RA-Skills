## Description:

Manages OpenClaw agent avatars by accepting an image or URL, or by using Freepik vector search to help select and apply a new avatar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to update an agent avatar from a supplied image, a URL, or Freepik search candidates. It helps place the selected avatar in the OpenClaw workspace and update the agent identity configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses unsafe shell templates and unrestricted URL downloads.

Mitigation: Validate agent names, agent IDs, filenames, and URLs before running curl or openclaw commands; prefer direct local images when possible.

Risk: The skill can persist a Freepik API key in plaintext TOOLS.md.

Mitigation: Avoid storing valuable API keys in TOOLS.md unless plaintext storage is acceptable, and do not echo full keys in chat.

Risk: The skill may receive sensitive descriptions or private image URLs during avatar selection.

Mitigation: Avoid pasting sensitive descriptions or private URLs, and review the skill before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/agent-avatar-manager)
- [Publisher profile](https://clawhub.ai/user/songhonglei)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Freepik API key dashboard](https://www.freepik.com/developers/dashboard/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update avatar image files and IDENTITY.md entries in an OpenClaw workspace.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
