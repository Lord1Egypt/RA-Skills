## Description:

Use when the user wants an AI to phone a restaurant, salon, clinic, dentist or hotel to book, cancel, reschedule or ask a question in the business's language. Calls the LifeClaw agent through Finch, which places a real call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a0971025732-netizen](https://clawhub.ai/user/a0971025732-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask the agent to contact a restaurant, salon, clinic, dentist, or hotel to make, cancel, or reschedule a booking, or ask a question by phone. The agent confirms the call details with the user before placing a real call.

### Deployment Geography for Use:

Global, except Mainland China (+86); unsupported destinations are flagged before dialing.

## Known Risks and Mitigations:

Risk: Calls require sharing personal details, and preferences may be retained indefinitely.

Mitigation: Confirm the destination and booking details before each call; request deletion through support if saved preferences should be removed.

Risk: A paid run may incur a charge.

Mitigation: Use free runs unless the user explicitly approves a paid run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a0971025732-netizen/skills/ai-phone-booking)
- [LifeClaw on Finch](https://www.finchtech.ai/market/chips/agent-e98cbf4b-fe2f-5fff-9236-d2bfcbad2eed/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=ai-phone-booking)
- [Finch MCP connection instructions](https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text with call status and booking details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One phone call per order, up to two minutes; the agent identifies itself and does not impersonate the user.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
