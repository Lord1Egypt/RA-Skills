## Description:

Monitor agent endpoints, check liveness, collect metrics, alert on failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and agent operators use this skill to probe dependency endpoints for uptime, latency, and health before deployment or during routine operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install path downloads mutable remote Python code from a branch without pinning or checksum verification.

Mitigation: Prefer the bundled agent_health.py from this release, or use a pinned and checksummed source before execution.

Risk: Endpoint probing may contact private or sensitive services.

Mitigation: Probe only endpoints the operator owns or is authorized to test, and run the tool with least privilege.

Risk: The included CI verifier inspects local product folders and runs declared checks.

Mitigation: Run CI verification only on trusted folders or inside a sandboxed environment.

## Reference(s):

- [ClawHub Agent Health Skill](https://clawhub.ai/itspremkumar/skills/agent-health)
- [Publisher Profile](https://clawhub.ai/user/itspremkumar)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON health-check results, with Markdown usage guidance and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Health checks report endpoint count, up/down status, HTTP status, latency in milliseconds, and short error messages.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
