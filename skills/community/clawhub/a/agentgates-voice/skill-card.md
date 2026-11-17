## Description:

An AI operator places a real phone call for your agent: a number and a task in words, then the transcript, the recording and the outcome. Billed per minute from a prepaid balance, or at the payphone for one x402 payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentgates](https://clawhub.ai/user/agentgates)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can ask an AI operator to make a real phone call on an agent's behalf and return the transcript, recording, and outcome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone calls can reach people who have not agreed to be contacted.

Mitigation: Call only consenting recipients, as required by the skill, and review the linked terms.

Risk: Call instructions, conversations, transcripts, and recordings may reveal personal information to Agentgates.

Mitigation: Minimize sensitive details in call instructions and consider what the conversation and returned recording may disclose; review the operator contract before calling.

Risk: Calls spend the owner's money and incur per-minute charges.

Mitigation: Get human approval before payment or stay within an explicit spending limit; check the current rate and call limit before placing the call.

## Reference(s):

- [Voice operator contract](https://api.agentgates.ai/api/account/docs/voice)
- [Voice service catalog and pricing](https://api.agentgates.ai/api/account/catalog)

## Skill Output:

**Output Type(s):** [Text, Audio]

**Output Format:** [Call transcript and outcome in text, with a recording as audio.]

**Output Parameters:** [1D (one call result)]

**Other Properties Related to Output:** [Calls are billed per minute from a prepaid balance or through one x402 payment; unanswered calls bill nothing per the skill description. Call duration is limited to reserved minutes.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
