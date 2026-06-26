## Description: <br>
Negotiate deals, schedules, and service agreements with other AI agents using the Clinch Protocol ANP layer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[publicstringapps](https://clawhub.ai/user/publicstringapps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover Clinch nodes, negotiate purchases, schedules, and service agreements, and manage approval-gated signed deals through the Clinch CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide commands that sign a committed Clinch deal. <br>
Mitigation: Require explicit user confirmation before any approve command and show the confirmed deal state before signing. <br>
Risk: CLINCH_PASSPHRASE and dashboard private keys can unlock or establish a signing identity. <br>
Mitigation: Keep credentials private, never log or store them, and require the passphrase only through the agent environment. <br>
Risk: Seller mode can expose a network-accessible endpoint for inbound negotiation traffic. <br>
Mitigation: Review seller/server mode, endpoint exposure, firewall posture, and seller configuration before running a public service. <br>
Risk: Initializing over an existing Clinch vault can replace the user's cryptographic identity. <br>
Mitigation: Check for an existing vault and run initialization only for a fresh install or after an explicit user reset request. <br>


## Reference(s): <br>
- [Clinch Skill on ClawHub](https://clawhub.ai/publicstringapps/clinch) <br>
- [Clinch Protocol](https://clinchprotocol.web.app) <br>
- [Clinch Seller Dashboard](https://clinchprotocol.web.app/sellers.html) <br>
- [publicstringapps Publisher Profile](https://clawhub.ai/user/publicstringapps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clinch binary and CLINCH_PASSPHRASE for vault-backed operations; direct-mode Clinch commands return JSON for agent parsing.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
