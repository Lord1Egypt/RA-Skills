## Description: <br>
Aegis Security Tool Free helps agents check blockchain addresses and tokens for basic reputation, honeypot, and quota status signals before a user proceeds with a transaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to run lightweight blockchain address reputation checks, token safety checks, and free-tier quota checks before interacting with DeFi addresses or tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repeated external requests can expose stable client fingerprints derived from local identity. <br>
Mitigation: Avoid OS username or hostname based fingerprints; prefer anonymous requests or a user-chosen opaque identifier when quota tracking is required. <br>
Risk: The skill is not a broad security audit and may miss complex transaction or token behavior. <br>
Mitigation: Use it only for blockchain address or token checks, review results before acting, and combine LOW risk results with user judgment or deeper review for high-value transactions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/aegis-security-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external blockchain-check APIs and return risk levels, safety flags, quota status, logs, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
