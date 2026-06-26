## Description: <br>
Escalates a blocked agent's problem, attempted fixes, and current result to a supervisor through a local webhook gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superWorldSavior](https://clawhub.ai/user/superWorldSavior) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support agents use this skill when an agent is blocked after repeated troubleshooting attempts and needs to hand concise context to a supervisor. It is intended for escalation of technical errors, out-of-scope requests, and ambiguous decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting context can be sent through a webhook to preset recipients without clear redaction, consent, or recipient-scoping safeguards. <br>
Mitigation: Use only in a trusted local gateway environment; configure the supervisor, recipient, and delivery channel explicitly before use. <br>
Risk: Escalation content may include credentials, access tokens, personal data, customer content, or full logs. <br>
Mitigation: Redact sensitive data and obtain user approval before sending any credentials, personal data, customer content, or logs. <br>
Risk: A broad or reused webhook token could allow unintended escalation requests. <br>
Mitigation: Use a narrowly scoped HOOKS_TOKEN and rotate it according to the gateway operator's policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superWorldSavior/agent-escalation) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Shell command invocation with Markdown message content and console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local webhook gateway and a configured HOOKS_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
