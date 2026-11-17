## Description:

Monitor and control OpenClaw API costs by tracking token usage across sessions, estimating spend by model, alerting on budget overruns, and recommending cheaper model routing for routine tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tso1079](https://clawhub.ai/user/tso1079)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect API usage, estimate spending, identify top-cost sessions, configure budget alerts, and plan lower-cost model routing for routine work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script reads local OpenClaw session metadata, which may include sensitive session labels or usage history.

Mitigation: Review before installing when session metadata is sensitive, and run reports only in environments where the local OpenClaw usage data may be inspected.

Risk: The --agent value can affect the session file path used by the report script.

Mitigation: Run the script only for trusted agent IDs, avoid path-like --agent values, and prefer a patched version that validates agent IDs and keeps resolved files under ~/.openclaw/agents.

Risk: Automated cron reports can become recurring access to local usage metadata.

Mitigation: Treat cron setup as an explicit opt-in recurring job and review the delivery channel before enabling scheduled reports.

## Reference(s):

- [Cost Guardian by Dexter Labs on ClawHub](https://clawhub.ai/tso1079/skills/dex-cost-guardian)
- [Publisher profile: tso1079](https://clawhub.ai/user/tso1079)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON cost reports with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include estimated cost, token breakdowns, model-level totals, session rankings, budget alerts, and model-routing recommendations.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
