## Description: <br>
Bags - The Solana launchpad for humans and AI agents. Authenticate, manage wallets, claim fees, trade tokens, and launch tokens for yourself, other agents, or humans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ramyodev](https://clawhub.ai/user/ramyodev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agents use this skill to authenticate with Bags, manage Solana wallets, check and claim fee shares, trade tokens, and launch tokens with configurable fee sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through live Solana financial actions, including trades, fee claims, and token launches. <br>
Mitigation: Use a low-value wallet and require human review of transaction details before signing or submitting transactions. <br>
Risk: The skill works with long-lived Bags credentials and API keys. <br>
Mitigation: Store credentials securely, rotate or revoke exposed keys, and avoid logging tokens or API keys. <br>
Risk: The skill includes wallet private-key export flows for transaction signing. <br>
Mitigation: Export private keys only when necessary, avoid passing private keys through shell variables when possible, and remove temporary key material after use. <br>
Risk: Heartbeat behavior may encourage silent self-updates or autonomous routine actions. <br>
Mitigation: Disable silent self-updates and require explicit approval for updates or actions that affect funds, credentials, or wallet state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ramyodev/bags) <br>
- [Bags homepage](https://bags.fm) <br>
- [Bags skill definition](https://bags.fm/skill.md) <br>
- [Bags authentication guide](https://bags.fm/auth.md) <br>
- [Bags wallet guide](https://bags.fm/wallets.md) <br>
- [Bags fee claiming guide](https://bags.fm/fees.md) <br>
- [Bags trading guide](https://bags.fm/trading.md) <br>
- [Bags token launch guide](https://bags.fm/launch.md) <br>
- [Bags Public API base](https://public-api-v2.bags.fm/api/v1) <br>
- [Bags Agent API base](https://public-api-v2.bags.fm/api/v1/agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with curl commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose actions involving live Solana wallets, Bags credentials, token trades, fee claims, and token launches.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter, artifact/skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
