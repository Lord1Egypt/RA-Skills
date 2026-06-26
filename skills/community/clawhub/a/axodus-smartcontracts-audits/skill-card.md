## Description: <br>
Audit Solidity contracts for common vulnerabilities and design risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Solidity contracts before deployment, after high-risk logic changes, or when integrating with external protocols. It produces prioritized findings with impacted locations, risk explanations, and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output may be mistaken for a formal security audit or an absolute claim that a contract is secure. <br>
Mitigation: Treat output as advisory review guidance, require qualified review for value-bearing contracts, and avoid claiming contracts are secure based only on the skill output. <br>
Risk: Users may provide private keys, seed phrases, wallet files, live credentials, or other secrets while supplying contract context. <br>
Mitigation: Provide contract source and non-secret context only; do not provide private keys, seed phrases, wallet files, or live credentials. <br>
Risk: The skill explicitly avoids exploit code, so reproduction details may be incomplete for high-risk live targets. <br>
Mitigation: Use responsible disclosure practices and escalate funds-at-risk or governance-impacting findings to a stricter review process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzfshark/axodus-smartcontracts-audits) <br>
- [Publisher profile](https://clawhub.ai/user/mzfshark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with a YAML audit report schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include severity, location, description, impact, recommendation, and assumptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, skill.yml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
