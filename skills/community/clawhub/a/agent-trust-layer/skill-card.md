## Description:

Agent Trust Layer is a rule-based discriminator that checks AI input, drafts, and output for trustworthiness, safety, honesty, and manipulative patterns before delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to gate AI responses, user inputs, and draft outputs with deterministic pass, verify, rewrite, or block decisions. It is intended for local integration as a text-checking and MCP-enabled agent service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review characterizes the package as a broad local agent service with MCP functions rather than only a passive text-checking skill.

Mitigation: Review the exposed MCP functions before installation and deploy only in environments where a local agent service is expected.

Risk: The security review notes local memory and log files plus under-disclosed persistence.

Mitigation: Set HEARTFLOW_MEMORY=off when memory is not wanted and review local data and log retention before use.

Risk: The security review notes plaintext project .env token persistence and localhost MCP access.

Mitigation: Use an explicit HEARTFLOW_MCP_TOKEN, protect project .env files, avoid privileged or root execution, and enable HEARTFLOW_PATH_GUARD=enforce for stricter path handling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yun520-1/skills/agent-trust-layer)
- [README](README.md)
- [Agent Integration Guide](AGENTS.md)
- [Security Advisory](SECURITY.md)
- [Installation Guide](INSTALL.md)
- [Public Evaluation Report 2026-08-17](docs/eval-report-2026-08-17.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, configuration notes, and structured gate results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Gate outputs use pass, verify, rewrite, or block actions with reasons, findings, severity, guidance, and checked_by traces.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence); artifact declares 6.6.1 in SKILL.md and package.json

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
