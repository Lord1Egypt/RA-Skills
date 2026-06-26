## Description: <br>
Launch custom tokens on Solana through BAGS or on BNB Chain through FLAP using API requests with configurable tax and revenue sharing options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FourClawTeam](https://clawhub.ai/user/FourClawTeam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to prepare and submit token launch requests for BAGS on Solana or FLAP on BNB Chain. It is intended for workflows where a human has approved the exact token parameters before any launch request is sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token launch requests are real public blockchain actions and may be difficult or impossible to reverse. <br>
Mitigation: Require explicit human approval for the platform, token name, symbol, creator wallet, tax rate, recipients, social metadata, and 20% platform fee before any launch request is sent. <br>
Risk: The launch endpoint accepts unauthenticated POST requests and the skill can enable high-impact actions without strong confirmation controls. <br>
Mitigation: Do not allow autonomous POST requests; constrain agent network access and review the final payload before execution. <br>
Risk: Wallet addresses, recipient splits, and social metadata can expose sensitive or public-facing information. <br>
Mitigation: Validate addresses and revenue splits with the intended owner, and avoid sending private or unapproved metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FourClawTeam/four-claw) <br>
- [FourClaw documentation](https://fourclaw.fun/fourclaw/docs) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include token launch parameters, status-check requests, error handling guidance, and rate-limit handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
