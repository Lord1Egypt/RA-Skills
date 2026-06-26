## Description: <br>
Purchase domains, manage DNS and Cloudflare settings via agieth.ai Agent Bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larkins](https://clawhub.ai/user/larkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to check domain availability, create registration quotes, manage DNS records, configure Cloudflare zones or tunnels, and inspect account balances through agieth.ai APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate domain purchases, DNS changes, Cloudflare tunnel or subscription changes, and blockchain transactions. <br>
Mitigation: Require human review before purchases, DNS deletions, tunnel or subscription changes, and any blockchain transaction. <br>
Risk: Automated payment methods can move funds when an Ethereum private key is available. <br>
Mitigation: Prefer manual wallet payment; if automation is required, use a dedicated low-balance wallet and protect the private key as a secret. <br>
Risk: Payment quotes include a server-provided payment address and amount. <br>
Mitigation: Verify the payment address and exact amount before sending funds. <br>
Risk: Public Ethereum RPC endpoints may be unreliable for transaction propagation. <br>
Mitigation: Keep RPC failover configured and use authenticated paid RPC providers for production-critical writes. <br>


## Reference(s): <br>
- [Agieth homepage](https://agieth.ai) <br>
- [Agieth API manifest](https://api.agieth.ai/api/v1/manifest) <br>
- [ClawHub skill page](https://clawhub.ai/larkins/agieth) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance, API calls] <br>
**Output Format:** [Python client methods returning JSON-like dictionaries, with setup guidance in Markdown and shell environment snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGIETH_API_KEY and AGIETH_EMAIL; optional Ethereum RPC endpoints and wallet private key are used only for automated payment flows.] <br>

## Skill Version(s): <br>
1.0.11 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
