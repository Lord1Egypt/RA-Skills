## Description:

Multi-Agent conversation management platform with Gemini-style UI for managing OpenClaw agents, image upload, chat history, and message isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szzg007](https://clawhub.ai/user/szzg007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create, view, manage, delete, and chat with multiple OpenClaw agents through a local web UI, CLI, and API. It is suited for local agent operations where the user can review and harden the server before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated controls can operate on OpenClaw agents and agent data.

Mitigation: Add authentication and restrict access to trusted local users before running the server.

Risk: Shell-based command construction can execute unintended commands.

Mitigation: Replace shell interpolation with argument-based process execution and validate all user-controlled paths, IDs, and messages.

Risk: Agent deletion can remove local OpenClaw data.

Mitigation: Back up ~/.openclaw, replace recursive shell deletion with safe filesystem deletion, and require explicit confirmation for destructive actions.

Risk: OpenClaw credentials or tokens may be exposed through configuration or documentation.

Mitigation: Remove real tokens from local files and docs, rotate any token that may have been published, and keep secrets outside distributable artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szzg007/skills/agent-im-manager-v100)
- [ClawHub publisher profile](https://clawhub.ai/user/szzg007)
- [ClawHub homepage](https://clawhub.com)
- [README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)
- [Security notes](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, API examples, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local OpenClaw agent-management instructions and examples; no fixed token cap is specified.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
