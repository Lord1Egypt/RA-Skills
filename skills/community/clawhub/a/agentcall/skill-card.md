## Description:

AgentCall gives AI agents US and Canadian VoIP phone numbers for SMS, application testing, AI voice calls, scheduling, and caller memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kintupercy](https://clawhub.ai/user/kintupercy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use AgentCall in AI systems that need programmable US and Canadian phone numbers for SMS, voice calls, receptionist workflows, and caller context. The skill provides API guidance and actions for configuring numbers, messaging, scheduling, webhooks, and call memory.

### Deployment Geography for Use:

United States and Canada

## Known Risks and Mitigations:

Risk: Reporting unexpected charges may lead to incoming AI calls being disabled, disconnecting callers.

Mitigation: Before disabling inbound calls, obtain approval for the specific number and explain that callers will be disconnected.

Risk: Provisioning numbers, messaging, calls, and scheduled outreach can incur charges or contact real people.

Mitigation: Confirm the number, recipient, message or call details, schedule, and expected charges with the user before acting.

Risk: Call memory and optional caller information, recordings, and provider-key sharing can affect privacy and data handling.

Mitigation: Review what caller information is stored and whether a provider key will be shared; enable memory or recording only with the user's approval.

## Reference(s):

- [AgentCall API reference](https://api.agentcall.co/llms.txt)
- [Voice prompt guide](https://agentcall.co/docs/voice-prompts)
- [Post-call webhook guide](https://agentcall.co/docs/post-call-webhook)

## Skill Output:

**Output Type(s):** [API calls, Configuration, Code, Guidance]

**Output Format:** [Markdown guidance with HTTP and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.15.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
