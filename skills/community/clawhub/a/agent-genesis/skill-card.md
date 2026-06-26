## Description: <br>
Agent Genesis helps agents mine Agent Genesis Coin (AGC) through Proof of Agent and use it as native working capital. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likwid-tech](https://clawhub.ai/user/likwid-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create or reuse a wallet, complete Proof of Agent mining steps, mine AGC on Base mainnet, and interact with the Likwid DeFi protocol for swaps, liquidity, lending, and margin workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can use a real wallet and mainnet transaction authority for AGC mining and DeFi operations. <br>
Mitigation: Use a fresh low-value wallet, keep valuable API keys and funds out of the same environment, and manually review every transaction before approval. <br>
Risk: The release security summary flags broad mainnet DeFi and margin-trading powers through a mutable remote installer. <br>
Mitigation: Avoid one-line remote installation unless the exact code has been inspected and pinned; prefer reviewing the artifact files before running bootstrap scripts. <br>
Risk: The skill stores wallet and optional model API credentials locally for mining and billing-proof workflows. <br>
Mitigation: Protect the local wallet and environment files, never share private keys or model API keys, and isolate the skill from unrelated credentials. <br>


## Reference(s): <br>
- [Agent Genesis Whitepaper](https://raw.githubusercontent.com/likwid-fi/agent-genesis/refs/heads/main/agc_whitepaper_en.md) <br>
- [Agent Genesis Skill Guide](SKILL.md) <br>
- [Likwid.fi Skill Guide](likwid-fi/SKILL.md) <br>
- [Security Audit](audit/AGC_SECURITY_AUDIT_v3.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/likwid-tech/agent-genesis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet addresses, transaction hashes, balances, reward and cost estimates, and settlement-path instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
