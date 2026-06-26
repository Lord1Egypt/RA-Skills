## Description: <br>
AgentBox Twitter lets agents search Twitter/X posts, fetch tweets with conversation context, and retrieve user profiles through a paid x402 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to research public Twitter/X activity by searching posts, fetching tweet threads, replies, and quotes, and inspecting user profiles when paid API access is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Twitter/X research terms and lookup targets are sent to the AgentBox API, which may expose sensitive or confidential investigations to the provider. <br>
Mitigation: Use the skill only when the provider's data handling is acceptable, and avoid sensitive or confidential investigations unless that risk has been reviewed. <br>
Risk: Every API call, including each paginated request, incurs a $0.003 USDC payment. <br>
Mitigation: Plan queries with specific operators and reasonable limits before running calls to control cost. <br>


## Reference(s): <br>
- [AgentBox Twitter ClawHub release](https://clawhub.ai/tenequm/agentbox-twitter) <br>
- [AgentBox Twitter API](https://twitter.x402.agentbox.fyi) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with x402_payment request examples and JSON API response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the openclaw runtime and x402_payment tool; each API call costs $0.003 USDC on Solana, and paginated requests are billed separately.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
