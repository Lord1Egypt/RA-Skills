## Description:

Agent work status monitoring and automatic activation system. Triggers when monitoring subagent runtime status, detecting prolonged unresponsive "stalled" states, and automatically activating them to resume operation. Suitable for long-running task monitoring, automated operations, agent health checks, and similar scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor long-running subagents, detect agents that appear stalled after an idle threshold, and optionally send activation messages to resume work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically steer or reactivate other agents across a broad scope with limited built-in safeguards.

Mitigation: Start with dry-run or target-specific use, add allowlists and logging before scheduled auto-activation, and set thresholds that account for long-running quiet work.

Risk: False stall detection can interrupt agents that are still doing useful quiet work.

Mitigation: Tune the idle threshold by task type and review activation logs before enabling continuous operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/agent-monitor)
- [Publisher profile](https://clawhub.ai/user/openlark)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, JSON]

**Output Format:** [Markdown guidance with Python and bash examples; optional JSON from the monitoring script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run mode, target-specific monitoring, configurable idle thresholds, and optional automatic activation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
