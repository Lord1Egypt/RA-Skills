## Description:

Use when another skill returns Feishu display payloads or `messageToolCalls`; this skill teaches the agent to use the OpenClaw `message` tool to send Feishu cards, text, and media in the current conversation, then reply with NO_REPLY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yqxu](https://clawhub.ai/user/yqxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using OpenClaw use this skill to display upstream Feishu card, text, and media payloads in the current conversation without rewriting or summarizing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send upstream-provided Feishu messages and card payloads without validating their contents.

Mitigation: Use it only with trusted upstream skills and make Feishu sends auditable before enabling it in sensitive workspaces.

Risk: The skill can upload local files referenced by upstream payloads.

Mitigation: Require confirmation for file uploads and restrict file paths to intended export artifacts.

Risk: The final NO_REPLY behavior can hide what was sent from the visible assistant response.

Mitigation: Add operational logging or review controls for Feishu sends where transparency is required.

## Reference(s):

- [Skill homepage](https://github.com/AIDiyTeams/claw-skill/tree/main/feishu-card-display)
- [ClawHub skill page](https://clawhub.ai/yqxu/skills/feishu-card-display)

## Skill Output:

**Output Type(s):** [API Calls, Text, Media]

**Output Format:** [Feishu message tool calls followed by NO_REPLY]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves upstream card, text, and file payloads exactly as provided.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
