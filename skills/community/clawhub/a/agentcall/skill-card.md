## Description:

Give your agent real phone numbers for SMS, OTP verification, and voice calls via the AgentCall API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kintupercy](https://clawhub.ai/user/kintupercy)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents and developers use this skill to manage phone numbers, SMS, OTP retrieval for apps they control, and inbound or outbound voice workflows through AgentCall. It also guides setup and billing choices for AI phone agents.

### Deployment Geography for Use:

United States and Canada

## Known Risks and Mitigations:

Risk: The security review flagged an instruction that could disable inbound AI during a billing or unexpected-call inquiry; the scan was partial.

Mitigation: Review the relevant instruction and require explicit user confirmation before changing inbound AI settings.

## Reference(s):

- [AgentCall API Reference](https://api.agentcall.co/llms.txt)
- [AgentCall CLI Guide](https://agentcall.co/docs/cli)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration, Shell commands, Code]

**Output Format:** [Text guidance, API request parameters, JSON configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some actions may incur charges, contact real people, or change persistent phone settings; follow the skill's confirmation guidance.]

## Skill Version(s):

2.15.2 (source: release evidence, claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
