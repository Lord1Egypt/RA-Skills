## Description: <br>
Let an AI agent complete flight booking payments after the user confirms the payee and amount using a CAI custodial wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to complete the payment step for a flight booking after the itinerary, recipient, amount, chain, and token are confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help complete real payments from a CAI wallet. <br>
Mitigation: Install only when this payment workflow is intended, use the narrowest CAI key scope available, and prefer pay scope over full scope. <br>
Risk: Payment transfers may be irreversible if the recipient, amount, chain, or token is wrong. <br>
Mitigation: Manually verify the airline or OTA recipient, amount, chain, and token before approving any transfer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bernardtai/book-flight-with-agent) <br>
- [Full CAI skill contract](https://cai.com/skill.md) <br>
- [CAI agent payment workflow](https://cai.com/skill-references/agent-payment-workflow.md) <br>
- [CAI agent card](https://cai.com/.well-known/agent.json) <br>
- [CAI developers](https://cai.com/developers.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and payment workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CAI_API_KEY with pay or full scope and user confirmation before transfers.] <br>

## Skill Version(s): <br>
1.0.15 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
