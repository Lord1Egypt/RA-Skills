## Description: <br>
Teaches agents how to use @getalby/cli to operate a Bitcoin Lightning wallet via Nostr Wallet Connect for sending and receiving money, paying invoices, checking balances, creating invoices, converting between fiat and sats, handling 402 paid requests, discovering paid services, and paying supported on-chain cryptocurrency or stablecoin addresses through automatic swaps from a Bitcoin balance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rolznz](https://clawhub.ai/user/rolznz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to let an agent operate an Alby-compatible Nostr Wallet Connect wallet for Lightning payments, wallet balance checks, invoice creation, paid HTTP 402 requests, paid service discovery, and supported on-chain crypto or stablecoin payments. It is intended for workflows where the user explicitly wants wallet-connected payment capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent spending-capable access to a Lightning wallet and paid service workflows. <br>
Mitigation: Install it only when wallet-connected payment behavior is intended, use a low-balance or test wallet, and set wallet-side budgets or limits. <br>
Risk: Nostr Wallet Connect secrets can grant wallet access or reduce wallet privacy if exposed. <br>
Mitigation: Do not paste NWC secrets into chat or shell history, do not print them in logs, and prefer local wallet configuration or environment handling that avoids disclosure. <br>
Risk: Payment, swap, or paid API commands may spend real funds. <br>
Mitigation: Require explicit user confirmation before every payment, swap, or paid API request, and report the purchased service or payment amount after execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rolznz/alby-bitcoin-payments) <br>
- [Alby](https://getalby.com) <br>
- [Nostr Wallet Connect](https://nwc.dev) <br>
- [Alby CLI](https://github.com/getAlby/cli) <br>
- [402index](https://402index.io) <br>
- [Alby Hub](https://getalby.com/alby-hub) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of NWC_URL, local Alby CLI wallet configuration, paid service discovery, and payment commands that can spend real funds.] <br>

## Skill Version(s): <br>
1.3.8 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
