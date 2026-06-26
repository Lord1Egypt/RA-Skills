## Description: <br>
Web3 token security scanner with expert cross-validation engine that detects honeypots, rug pulls, and contract risks across Ethereum, BSC, Polygon, and other EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and Web3 security reviewers use Anti Rug to scan token contract addresses, classify token scenarios, and produce risk findings before interacting with a token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token chain IDs and contract addresses are sent to GoPlus or to a user-selected API gateway during scans. <br>
Mitigation: Use the default GoPlus endpoint or a trusted gateway only, and avoid routing scans through unknown custom proxies. <br>
Risk: The artifact documentation lists different GitHub repository paths, which can make maintainer verification unclear. <br>
Mitigation: Verify the ClawHub publisher profile and repository link from release metadata before relying on the artifact as an upstream source. <br>
Risk: The scanner reports on-chain contract indicators and does not determine project value or investment suitability. <br>
Mitigation: Treat the output as one security signal and combine it with independent project, liquidity, and market review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deanpeng-dotcom/anti-rug) <br>
- [Publisher profile](https://clawhub.ai/user/deanpeng-dotcom) <br>
- [Repository link from release metadata](https://github.com/ZorroShao/anti-rug) <br>
- [GoPlus API endpoint used by artifact](https://api.gopluslabs.io) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Guidance] <br>
**Output Format:** [JSON CLI output with token scenario classification, risk scores, cross-validation findings, and final verdicts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a supported chain ID and contract address; optionally accepts a custom API gateway.] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
