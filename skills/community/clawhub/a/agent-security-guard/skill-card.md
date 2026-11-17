## Description:

Agent Security Guard provides security-policy guidance for gating risky agent transitions by separating origin trust, data sensitivity, and action tiers before tool calls, memory writes, and external actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmannixx](https://clawhub.ai/user/xmannixx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add security-policy guidance for workflows that keep routine read, search, and summarization actions autonomous while gating higher-risk transitions such as secret exfiltration, command execution chains, and privileged memory writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could rely on the documentation-only artifact as though it were an installed enforcement layer.

Mitigation: Before operational use, verify the separately installed implementation, plugin, CLI, audit database, or memory integration and confirm it follows explicit confirmation and deny-by-default behavior.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/xMannixx/Agent-Security-Guard/tree/main/security/agent-security-guard)
- [ClawHub skill listing](https://clawhub.ai/xmannixx/skills/agent-security-guard)

## Skill Output:

**Output Type(s):** [Guidance, Text, Configuration]

**Output Format:** [Markdown skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only artifact; no executable files were included in the release evidence.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata and target metadata; artifact frontmatter states 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
