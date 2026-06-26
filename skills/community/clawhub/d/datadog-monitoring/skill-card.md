## Description: <br>
Inspect Datadog monitors, metrics, logs, incidents, dashboards, and observability data - powered by ClawLink. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect Datadog observability data and manage monitors, dashboards, incidents, logs, traces, metrics, SLOs, webhooks, and related resources through ClawLink. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents Datadog operations that can change or delete production observability resources, including monitors, dashboards, host tags, webhooks, and alert muting. <br>
Mitigation: Install only when write-capable Datadog administration is intended, use the least-privilege Datadog connection available, and require explicit confirmation before write or delete actions. <br>
Risk: The skill requires OAuth tokens and sensitive credentials through the ClawLink connection flow. <br>
Mitigation: Pair only through the expected ClawLink flow, limit granted Datadog scopes where possible, and reconnect or revoke access when scopes or operational needs change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/datadog-monitoring) <br>
- [ClawLink Datadog connection dashboard](https://claw-link.dev/dashboard?add=datadog) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=datadog-monitoring) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call ClawLink tools that return Datadog API results and may propose or execute write-capable Datadog actions when authorized.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
