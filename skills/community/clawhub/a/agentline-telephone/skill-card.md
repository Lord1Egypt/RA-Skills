## Description:

Make phone calls, view received SMS, provision numbers, manage agents, and track billing through the AgentLine telephony API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sameersribot](https://clawhub.ai/user/sameersribot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate AgentLine telephony workflows, including outbound calls, inbound SMS review, call transcript retrieval, phone number provisioning, agent configuration, and billing checks.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill can expose sensitive call transcripts, inbound SMS, billing details, and phone number records to the agent.

Mitigation: Use a dedicated AgentLine API key with the minimum account access practical, keep the key out of command-line arguments and logs, and review transcript or message content before sharing it further.

Risk: Outbound calls and phone number provisioning can create charges or permanent account changes.

Mitigation: Require explicit human confirmation before every outbound call and every number purchase, and verify billing after chargeable actions.

Risk: The skill instructs the agent to run an unbounded background event poller.

Mitigation: Avoid running the provided background poller by default; if polling is needed, run it in a time-limited session with visible logs and a clear stop condition.

## Reference(s):

- [AgentLine Website](https://agentline.cloud)
- [AgentLine API Base URL](https://api.agentline.cloud)
- [ClawHub Skill Page](https://clawhub.ai/sameersribot/skills/agentline-telephone)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with API endpoint references and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTLINE_API_KEY and may produce summaries of call transcripts, inbound SMS events, billing details, and number provisioning results.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
