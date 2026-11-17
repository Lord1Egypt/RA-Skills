## Description:

Audits Claude Code, OpenClaw, and Hermes Agent configurations for misconfigurations, token waste, security issues, and stale authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis-drakon](https://clawhub.ai/user/jarvis-drakon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use the CLI to audit Claude Code, OpenClaw, and Hermes Agent configurations, review optimization suggestions, and apply approved changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool reads sensitive local configuration and can access remote hosts through fleet SSH.

Mitigation: Start with read-only audits and dry-run previews, approve specific configuration changes, and review the package version before granting access to local credentials or remote hosts.

Risk: Optional monitoring adds scheduled audits and sends summary reporting to a server.

Mitigation: Enable monitoring only when wanted; use monitor disable to remove its schedule.

## Reference(s):

- [Agent Optimizer product page](https://drakonsystems.com/products/agent-optimizer)
- [Agent Optimizer npm package](https://www.npmjs.com/package/@drakon-systems/agent-optimizer)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Configuration instructions]

**Output Format:** [JSON audit reports and plans, with CLI commands and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include findings and suggested changes; applying configuration changes requires explicit user approval.]

## Skill Version(s):

0.16.3 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
