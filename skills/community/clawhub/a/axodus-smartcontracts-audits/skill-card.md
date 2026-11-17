## Description:

Audit Solidity contracts for common vulnerabilities and design risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to review Solidity contract scopes before deployment or after changes to access control, external calls, accounting, token logic, upgradeability, or protocol integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed trigger metadata may make automatic activation less predictable.

Mitigation: Replace malformed trigger metadata with explicit smart-contract audit trigger phrases before relying on automatic activation.

Risk: Audit reports can miss vulnerabilities or overstate confidence if they are not reviewed against the full contract scope, threat model, and deployment assumptions.

Mitigation: Use the skill as review support, require human security review for value-bearing contracts, and avoid treating reports as a guarantee that contracts are secure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/axodus-smartcontracts-audits)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with a structured YAML finding schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a system summary, prioritized findings, assumptions, impacted locations, impact, and remediation recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.yml, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
