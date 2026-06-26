## Description: <br>
Crypto Genie checks cryptocurrency addresses against a local SQLite database and optional Etherscan-backed sync workflow to surface phishing, honeypot, rug-pull, exploit-group, and social-engineering risk signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[princedoss77](https://clawhub.ai/user/princedoss77) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to check cryptocurrency addresses before interacting with them, review risk scores and scam indicators, and configure local or scheduled Etherscan-backed synchronization for unknown addresses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checked crypto addresses may be stored locally and unknown addresses may be sent to Etherscan using the user's API key. <br>
Mitigation: Avoid sensitive investigations unless network sync is disabled or isolated, and review local database retention before use. <br>
Risk: Decoded transaction messages are untrusted text and may contain misleading, malicious, or sensitive content. <br>
Mitigation: Treat decoded messages as untrusted input and avoid copying them into privileged workflows without review. <br>
Risk: An Etherscan API key may be exposed through environment variables, command history, logs, or process output. <br>
Mitigation: Use the encrypted setup flow where appropriate, avoid logging keys, and rotate any API key that may have appeared in logs. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/princedoss77/crypto-genie) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [DATABASE_ARCHITECTURE.md](DATABASE_ARCHITECTURE.md) <br>
- [SECURITY.md](SECURITY.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>
- [Etherscan API key setup](https://etherscan.io/myapikey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON address analysis with command-line setup and synchronization guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May queue unknown addresses for Etherscan-backed sync and write address, transaction, risk, and indicator data to a local SQLite database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter, package.json, and changelog report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
