## Description:

Feishu Ai Coding Assistant helps developers run AI coding workflows by guiding tool selection, installation commands, sub-agent sessions, task monitoring, and result collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate coding tasks across supported AI coding tools and sub-agent runtimes. It is intended for project generation, refactoring, testing, documentation, and monitored multi-step coding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a suspicious security verdict because the skill requests broad agent, command, file, and session permissions.

Mitigation: Evaluate and run it only in a sandboxed workspace until permissions are narrowed to the implemented workflow and sensitive operations require explicit confirmation.

Risk: The release evidence reports exposed publishing tokens in the shipped artifact.

Mitigation: Remove the exposed tokens from the artifact and rotate them before installing, publishing, or reusing the skill.

Risk: The release evidence flags risky install guidance for global package installation and command execution.

Mitigation: Require user confirmation before running installation commands, inspect commands before execution, and prefer disposable or least-privilege environments.

Risk: Persistent session history and thread binding can expose or reuse prior coding context beyond the immediate request.

Mitigation: Limit session-history access, avoid sensitive inputs, and clear or isolate sessions when switching projects or trust boundaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rfdiosuao/skills/feishu-ai-coding-assistant)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw sub-agent tutorial](https://my.feishu.cn/docx/IgkrdJvgxowAuMxAAkAcDaCOntf)
- [Feishu usage tutorial](https://www.feishu.cn/docx/HcQGd4wDsok2wTxOeWAcAXmEnje)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tool installation commands, sub-agent session parameters, status summaries, and project completion reports.]

## Skill Version(s):

1.0.0 (source: server release evidence, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
