## Description:

Audits Claude Code, OpenClaw, and Hermes Agent configurations for misconfigurations, security issues, stale authentication, and optimization opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis-drakon](https://clawhub.ai/user/jarvis-drakon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use the CLI to review Claude Code, OpenClaw, and Hermes Agent setup, identify configuration and security concerns, and plan or apply selected optimizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI inspects agent configuration, authentication profile, and workspace files that may contain sensitive settings.

Mitigation: Review the documented paths and run it only where that access is appropriate; the release evidence says audit, scan, and optimize do not transmit those file contents.

Risk: Optional monitoring, license activation, updates, and fleet audits use network connections when those commands are run.

Mitigation: Review the disclosed data and destinations before enabling monitoring or activating a license, and limit fleet targets to hosts you are authorized to inspect.

## Reference(s):

- [Agent Optimizer product page](https://drakonsystems.com/products/agent-optimizer)
- [Agent Optimizer on npm](https://www.npmjs.com/package/@drakon-systems/agent-optimizer)
- [ClawHub release page](https://clawhub.ai/jarvis-drakon/skills/drakon-agent-optimizer)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON reports and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit findings, scan results, optimization plans, and recommendations.]

## Skill Version(s):

0.16.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
