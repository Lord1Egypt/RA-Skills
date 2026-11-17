## Description:

Prevent runaway API costs with 3-tier protection: caution, emergency, and hard cap. Works for ANY expensive API GPT-4, Claude Opus, Gemini, cloud services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to add tiered cost controls around expensive API or cloud-service calls. It helps monitor request costs, block calls after emergency thresholds, and optionally run an external watchdog that can stop the protected process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional watchdog can terminate a local process when configured thresholds are exceeded.

Mitigation: Run it only under a dedicated unprivileged account, avoid root cron, verify the PID file target, and require operator approval before recovery.

Risk: State files and emergency flags control whether API calls continue or stop.

Mitigation: Protect the state directory from other users and use inspected local files or a pinned, verified package.

Risk: Cost totals depend on recorded calls and can drift from provider billing data.

Mitigation: Use conservative thresholds and reconcile tracker totals against provider dashboards before relying on the limits in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/cost-control)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)
- [README](artifact/README.md)
- [Known limitations](artifact/LIMITATIONS.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces integration guidance for local cost tracking, threshold configuration, emergency flags, and watchdog deployment.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
