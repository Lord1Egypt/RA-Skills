## Description: <br>
Real-time, audit-ready logging integration for ClawControl.space. Ensures deterministic, per-action observability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qasimnaqvi](https://clawhub.ai/user/qasimnaqvi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to add continuous ClawControl logging to an agent workflow, including messages, tool executions, errors, and metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests exhaustive external logging that may include messages, tool outputs, internal decisions, secrets, or sensitive context. <br>
Mitigation: Use only in workflows that intentionally require ClawControl logging; confirm storage, access, retention, deletion, and redaction controls before use, and restrict payloads to sanitized action metadata where possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qasimnaqvi/clawcontrol-logger) <br>
- [ClawControl webhook endpoint](https://clawcontrol.space/api/functions/receiveWebhook) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, JSON] <br>
**Output Format:** [JSON log payloads and shell commands for posting events to the ClawControl webhook] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWCONTROL_API_KEY and sends event logs to an external ClawControl endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
