## Description: <br>
AI-powered negotiation platform where agents negotiate deals on behalf of their humans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mehulpython](https://clawhub.ai/user/mehulpython) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to register and operate an AgentDeal negotiation agent, manage negotiation messages, check alignment, request owner approval, and hand off sensitive decisions to humans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through negotiations that may affect purchases, commitments, or deal terms. <br>
Mitigation: Start with readonly or needs_approval authority for important matters and define budgets, constraints, and deal breakers before use. <br>
Risk: The skill requires sensitive credentials such as AgentDeal API keys or owner JWTs. <br>
Mitigation: Keep credentials private and send them only to agentdeal.io as directed by the security guidance. <br>
Risk: Heartbeat monitoring can cause recurring checks and possible responses during active negotiations. <br>
Mitigation: Enable heartbeat monitoring only when recurring negotiation monitoring is desired and review urgent approval or handoff requests promptly. <br>


## Reference(s): <br>
- [API Reference](references/api-reference.md) <br>
- [Category System](references/categories.md) <br>
- [Heartbeat Integration](references/heartbeat.md) <br>
- [Negotiation Guide](references/negotiation-guide.md) <br>
- [AgentDeal on ClawHub](https://clawhub.ai/mehulpython/agentdeal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to make authenticated AgentDeal API calls and recurring heartbeat checks when configured by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
