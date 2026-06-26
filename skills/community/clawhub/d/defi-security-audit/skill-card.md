## Description: <br>
Analyze a DeFi protocol for vulnerabilities, mechanism safety, and risk factors. Use when the user wants to audit a DeFi project, check protocol security, or assess risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[truenorth-lj](https://clawhub.ai/user/truenorth-lj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security researchers, and DeFi operators use this skill to produce protocol risk reports covering governance, oracle design, admin privileges, economic mechanisms, public audit history, and operational security. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Protocol names, contract addresses, and related lookup targets may be sent to public web and blockchain APIs. <br>
Mitigation: Use the skill only for research targets that can be safely disclosed to public API providers. <br>
Risk: Generated risk assessments may influence high-stakes DeFi decisions. <br>
Mitigation: Treat reports as informational security analysis, verify current protocol state independently, and do not treat the output as financial advice. <br>
Risk: Wallet secrets or transaction-signing authority could create unnecessary exposure if provided during research. <br>
Mitigation: Do not provide seed phrases, private keys, or transaction-signing authority to the agent when using this skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/truenorth-lj/defi-security-audit) <br>
- [README](artifact/README.md) <br>
- [Methodology](artifact/docs/methodology.md) <br>
- [Audit Report Index](artifact/docs/audit-reports.md) <br>
- [DeFiLlama API](https://api.llama.fi/protocols) <br>
- [GoPlus Security API](https://api.gopluslabs.io/api/v1) <br>
- [RugCheck Token Reports](https://api.rugcheck.xyz/v1/tokens/{mint_address}/report) <br>
- [Birdeye Token Security API](https://public-api.birdeye.so/public/token_security?address={mint_address}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown risk report with structured tables, quantitative scores, information gaps, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public API lookup results, protocol risk ratings, peer comparisons, and explicit non-financial-advice disclaimers.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
