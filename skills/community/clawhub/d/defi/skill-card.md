## Description: <br>
A protocol risk analyst and yield reality checker for decentralized finance that evaluates protocol safety before deposit, calculates real yield after costs and market drag, identifies common rug-risk patterns, and stays advisory-only with no wallet access, private key handling, transaction signing, or on-chain execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIsearch](https://clawhub.ai/user/AGIsearch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External DeFi users use this skill to review protocol, yield, liquidity, governance, oracle, and rug-risk signals before committing capital. It can also organize user-provided DeFi transaction records into likely tax-event categories for professional review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat DeFi, investment, or tax analysis as professional advice. <br>
Mitigation: Present outputs as risk-analysis and organization support only, and direct users to qualified financial, legal, or tax professionals for decisions and filings. <br>
Risk: Users may disclose seed phrases, private keys, wallet passwords, or unnecessary personal financial records. <br>
Mitigation: Do not request wallet secrets or unnecessary sensitive records; keep any chain or protocol context read-only and based on user-provided information. <br>
Risk: Protocol reviews and rug-risk screens can miss unknown vulnerabilities or changing market conditions. <br>
Mitigation: Include explicit verification steps before deposit and avoid guarantees of protocol safety or fraud detection. <br>


## Reference(s): <br>
- [DeFi ClawHub release](https://clawhub.ai/AGIsearch/defi) <br>
- [README](artifact/README.md) <br>
- [Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis with structured risk diagnosis, yield estimate, red flags, verification steps, and transaction-event summaries when records are supplied] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory-only output; no wallet access, transaction signing, transaction broadcasting, live chain indexing, or professional financial, legal, or tax advice.] <br>

## Skill Version(s): <br>
2.0.0 (source: skill frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
