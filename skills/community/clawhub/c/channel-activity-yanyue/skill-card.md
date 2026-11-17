## Description:

Multi-channel short-term memory for AI assistants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eightroad](https://clawhub.ai/user/eightroad)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to record short-lived activity summaries across channels such as Feishu and QQ, then retrieve recent context from other channels during an assistant session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored conversation summaries can be shared across channels and identities without adequate access controls or consent safeguards.

Mitigation: Use only with trusted users unless family sharing, cross-channel recall, automatic hooks, and long-term memory access are explicitly consented to and scoped.

Risk: Shared cache files can expose one user or tenant's recent activity to another deployment context.

Mitigation: Isolate cache files per user or tenant and restrict file permissions before deployment.

Risk: Automatic prompt injection of memory records can introduce unintended or sensitive context into assistant replies.

Mitigation: Avoid automatic prompt injection for sensitive deployments, and scope retrieved memory records to the current consent and channel-sharing policy.

Risk: Installer and import behavior may be brittle when versions or local paths are not controlled.

Mitigation: Pin the installer version and remove hard-coded import paths before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eightroad/skills/channel-activity-yanyue)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text and Markdown with Python examples, shell commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and returns recent channel activity summaries with configurable TTL, summary length, and context length limits.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
