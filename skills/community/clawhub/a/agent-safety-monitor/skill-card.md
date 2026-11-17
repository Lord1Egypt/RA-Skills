## Description:

Real-time AI agent safety monitoring, anomaly detection, and constraint enforcement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure log-based safety monitoring for autonomous agents, including rate limits, tool allowlists, budget caps, scope checks, and anomaly alerts. Treat it as alerting and log analysis unless runtime pause/kill enforcement is separately implemented and tested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact describes pause, kill, dashboard, and webhook behavior that is not fully implemented by the provided code.

Mitigation: Use the current artifact for log analysis and alert summaries only, or add and test runtime enforcement, dashboard, and webhook integrations before relying on those claims.

Risk: Safety decisions based only on parsed logs may miss actions that are not captured in the event stream.

Mitigation: Feed the monitor from trusted, complete agent event logs and validate coverage before using alerts for operational decisions.

## Reference(s):

- [Safety Rules Reference](references/rules-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/evezart/skills/agent-safety-monitor)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with bash snippets and YAML configuration examples; the monitor script emits JSON summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses YAML rule configuration and JSON event logs as inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
