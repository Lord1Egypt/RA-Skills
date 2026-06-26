## Description: <br>
Bot Trade lets agents connect to the MossTrade simulated futures trading API to register bots, place and close positions, inspect portfolios, and recover after liquidation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fueav](https://clawhub.ai/user/Fueav) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent builders use this skill to give an agent structured guidance for interacting with the MossTrade simulated contract-trading API, including registration, market orders, portfolio checks, and risk-aware position management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated use can place high-leverage simulated trades or oversized positions. <br>
Mitigation: Require explicit leverage and position-size limits before allowing the agent to trade. <br>
Risk: The sample close_position helper can send a reversing order instead of a reduce-only close. <br>
Mitigation: Fix or avoid that helper unless it sends reduce_only:true and validates the current position size. <br>
Risk: API key exposure would let another caller act as the bot. <br>
Mitigation: Keep the API key private and avoid logging or sharing credentials. <br>


## Reference(s): <br>
- [bot-trade ClawHub release page](https://clawhub.ai/Fueav/bot-trade) <br>
- [MossTrade API base URL](https://lark.openclaw-ai.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with bash, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MossTrade API key; examples include order, leverage, portfolio, status, and history parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
