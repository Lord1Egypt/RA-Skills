## Description:

Agent DLP helps agents inspect prompts, memory entries, tool requests, and outputs for prompt injection, sensitive data exposure, dangerous tool use, and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caidongyun](https://clawhub.ai/user/caidongyun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add DLP checks around agent workflows, including input injection detection, memory filtering, tool approval checks, output redaction or blocking, and audit review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill claims broad inspection and audit logging of prompts, outputs, memory entries, tool parameters, IP addresses, and MAC addresses without enough scoping, retention, or user-notice detail.

Mitigation: Before using it with real user data, define logged fields, redaction-before-storage behavior, access controls, retention, and user notice.

Risk: Normal mode may log some detected issues while blocking only severe risks.

Mitigation: Use strict mode for sensitive workflows and test representative prompts, outputs, memory entries, and tool calls before relying on the skill.

Risk: Dangerous tool control depends on correctly configured approval policy and review practices.

Mitigation: Require explicit approval for destructive or high-impact tools and review audit logs for denied, approved, and bypassed tool actions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/caidongyun/skills/agent-dlp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, Python examples, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes normal and strict operating modes plus audit-log review guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/SKILL.md; artifact/FEATURES.md mentions v2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
