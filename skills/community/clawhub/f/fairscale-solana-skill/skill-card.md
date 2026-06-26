## Description: <br>
Provides Solana wallet reputation scores and risk assessments to help agents and developers evaluate transaction, whitelist, airdrop, lending, and custom scoring decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RisheeA](https://clawhub.ai/user/RisheeA) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to query FairScale's Solana wallet reputation and risk endpoints before trades, airdrops, whitelist decisions, lending checks, or custom scoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Solana wallet addresses and transaction context may be sent to a third-party FairScale API. <br>
Mitigation: Use only wallet and transaction data that users are comfortable sharing with FairScale, and avoid sending unnecessary sensitive context. <br>
Risk: Credit purchases and blockchain payments may be irreversible or sent to an untrusted address. <br>
Mitigation: Do not automate credit purchases; verify payment addresses through trusted sources before sending funds. <br>
Risk: Session tokens used for paid FairScale requests can grant access to prepaid credits. <br>
Mitigation: Treat session tokens as credentials, avoid exposing them in logs or shared transcripts, and rotate or discard them when no longer needed. <br>


## Reference(s): <br>
- [FairScale Docs](https://docs.fairscale.xyz) <br>
- [FairScale API Endpoint](https://x402.fairscale.xyz) <br>
- [ClawHub Skill Page](https://clawhub.ai/RisheeA/fairscale-solana-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON] <br>
**Output Format:** [Markdown with inline HTTP, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Solana wallet addresses, transaction amounts, scoring rules, and FairScale session-token handling guidance.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
