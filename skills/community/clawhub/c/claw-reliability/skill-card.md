## Description:

Agent observability that monitors tool invocations, LLM calls, token usage, costs, and anomalies with pluggable alerts and a real-time dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fiddyrod](https://clawhub.ai/user/fiddyrod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw agent activity, review tool and LLM metrics, detect reliability anomalies, configure alerts, and inspect a local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent transcripts may contain secrets, customer data, or sensitive file paths that are read and retained by the observability store.

Mitigation: Review before installing in sensitive environments, add redaction before storage, set retention limits, and restrict local database file permissions.

Risk: External webhook alerts can send sanitized but still sensitive operational context to a third-party endpoint.

Mitigation: Configure only trusted webhook destinations and do not commit config.yaml after adding a webhook URL.

Risk: Dashboard exposure can reveal local agent activity if it is bound beyond localhost.

Mitigation: Keep the dashboard bound to localhost unless an explicit access-control plan is in place.

Risk: Frontend CDN dependencies may be unsuitable for air-gapped or high-security deployments.

Mitigation: Bundle and serve frontend assets locally in restricted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fiddyrod/skills/claw-reliability)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, reports, and local dashboard instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local observability reports and setup guidance; metrics are stored in local SQLite unless external alerts are configured.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
