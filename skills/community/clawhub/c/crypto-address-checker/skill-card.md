## Description: <br>
Checks cryptocurrency addresses for scam indicators such as phishing, honeypots, rug pulls, and suspicious transaction messages using local storage and Etherscan-backed synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[princedoss77](https://clawhub.ai/user/princedoss77) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to check blockchain addresses before interacting with them, review risk scores and scam indicators, and receive cautious recommendations about suspected malicious or suspicious addresses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uncached wallet addresses may be sent to Etherscan during normal checks despite local-only claims. <br>
Mitigation: Deploy only with clear user consent for network lookups, document when external sync occurs, and review behavior before use with sensitive addresses. <br>
Risk: The package requires an Etherscan API key and evidence flags any included or previously used key as exposed. <br>
Mitigation: Configure a fresh user-controlled API key, rotate any exposed key, and avoid storing secrets in shared logs, prompts, or source files. <br>
Risk: Address risk results may be incomplete when data is missing, stale, or unsupported for a chain. <br>
Mitigation: Treat results as advisory, re-check high-value addresses with independent sources, and avoid using the skill as the sole basis for financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/princedoss77/crypto-address-checker) <br>
- [README](artifact/README.md) <br>
- [Database architecture](artifact/DATABASE_ARCHITECTURE.md) <br>
- [Security guidance](artifact/SECURITY.md) <br>
- [Multi-chain support](artifact/MULTICHAIN_SUPPORT.md) <br>
- [Etherscan API key setup](https://etherscan.io/myapikey) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [Human-readable terminal text or JSON, with setup and sync commands documented in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include risk score, risk level, scam indicators, suspicious transaction summaries, and recommendations when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter, package.json, manifest, and changelog declare 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
