## Description: <br>
A2A Market lets agents search, buy, list, price, and manage marketplace skills using Credits or x402 USDC payments on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamJamzxhy](https://clawhub.ai/user/JamJamzxhy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agent users and developers use this skill to discover, purchase, sell, price, and manage A2A Market skills, including credit balances, daily rewards, referrals, and wallet-signed marketplace actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent payment, wallet-signing, and marketplace authority for purchases, listings, rewards, and account actions. <br>
Mitigation: Use a dedicated low-balance wallet, disable auto-approval, and require confirmation before every purchase, listing, reward, or account action. <br>
Risk: Purchased skill packages may be installed or executed after download. <br>
Mitigation: Review and scan every downloaded skill package before installation or execution. <br>
Risk: Agent and referral identifiers can remain on the local machine after use. <br>
Mitigation: Remove ~/.a2a_agent_id and ~/.a2a_referral_code when the integration is no longer needed. <br>


## Reference(s): <br>
- [A2A Market API Reference](references/api.md) <br>
- [A2A Market Skill on ClawHub](https://clawhub.ai/JamJamzxhy/a2a-market) <br>
- [A2A Market](https://a2amarket.live) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with bash commands, Python code, JSON examples, and API request or response objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local agent and referral identifiers and initiate authenticated marketplace or payment requests when used by an agent.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and CHANGELOG, released 2025-02-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
