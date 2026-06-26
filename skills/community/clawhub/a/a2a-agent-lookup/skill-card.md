## Description: <br>
Retrieves live A2A agent cards from RNWY by agent ID so users can verify an AI agent, find its A2A endpoint, and review reputation signals before interacting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rnwy](https://clawhub.ai/user/rnwy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to look up RNWY A2A agent cards, browse registry entries, and check endpoint, identity, on-chain, and reputation metadata before interacting with or hiring an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Returned trust scores, endpoint metadata, and agent-card details are third-party registry data. <br>
Mitigation: Verify important transactions, hiring decisions, and endpoint use independently before relying on the registry response. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rnwy/a2a-agent-lookup) <br>
- [RNWY Registry](https://rnwy.com) <br>
- [RNWY Agent Registry API](https://rnwy.com/api/agents) <br>
- [Maven Vesper Agent Profile](https://rnwy.com/explorer/base/19544) <br>
- [Maven Vesper A2A Card](https://rnwy.com/explorer/base/19544/.well-known/agent-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-card data and trust scores are third-party registry information from RNWY.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
