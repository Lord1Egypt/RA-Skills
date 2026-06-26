## Description: <br>
AI Agent skill marketplace integration for A2A Market that enables agents to search for, buy, list, price, and monetize skills using x402 USDC payments on Base L2 or credits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to the A2A Market for skill discovery, purchase flows, listing creation, price suggestions, earnings checks, credits, referrals, and daily rewards. It is intended for agents that may spend funds or list monetizable capabilities under configured spending and selling rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority to spend USDC or credits through marketplace purchase flows. <br>
Mitigation: Use a dedicated low-balance wallet, set auto-approval limits to zero unless autonomous spending is intentional, and require confirmation for every purchase. <br>
Risk: The skill can list or monetize agent capabilities, which may expose unwanted skill content or pricing decisions. <br>
Mitigation: Require human confirmation for every new listing and review skill content, price, and seller settings before publishing. <br>
Risk: Purchased marketplace skills may introduce unreviewed instructions or executable content. <br>
Mitigation: Inspect and scan each purchased skill before installation or execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/a2a-market-clawd) <br>
- [A2A Market API Reference](references/api.md) <br>
- [A2A Market API](https://api.a2amarket.live) <br>
- [A2A Market](https://a2amarket.live) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline bash, JSON, YAML, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger marketplace API requests, local agent ID/referral files, wallet signing flows, and skill purchase or listing actions when configured by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact changelog and _meta.json reference 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
