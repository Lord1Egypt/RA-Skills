## Description: <br>
Tax compliance for AI agent transactions - sales tax, capital gains, nexus monitoring, 1099 tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenttax](https://clawhub.ai/user/agenttax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to make AgentTax API calls for sales or use tax calculations, trade logging for capital gains, tax rate lookup, nexus configuration, and 1099-DA export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive transaction amounts, counterparty identifiers, buyer location, tax residency, and trading records to a third-party API. <br>
Mitigation: Show each POST payload before sending it, omit unnecessary optional fields such as ZIP or detailed counterparty identifiers when possible, and review the provider's privacy, retention, deletion, and correction policies. <br>
Risk: The skill can create or change remote tax records without enough consent, privacy, or reversal guidance. <br>
Mitigation: Require explicit user approval before POST requests that log trades or configure nexus, and keep an audit trail of submitted payloads and responses. <br>
Risk: The skill depends on an API key that could be exposed through prompts, logs, or command output. <br>
Mitigation: Store AGENTTAX_API_KEY in the environment, do not paste it into shared logs or transcripts, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [AgentTax ClawHub page](https://clawhub.ai/agenttax/agenttax) <br>
- [AgentTax homepage](https://agenttax.io) <br>
- [AgentTax API guide](https://agenttax.io/api/v1/agents) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and the AGENTTAX_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
