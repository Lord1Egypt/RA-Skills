## Description:

Audits Aptos Move contracts for security vulnerabilities before deployment using a seven-category checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and auditors use this skill to review Aptos Move contracts for access control, input validation, object safety, reference safety, arithmetic safety, generic type safety, and test coverage issues before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad security wording may trigger the skill outside the intended Aptos Move contract review context.

Mitigation: Use the skill when the target is an Aptos Move contract or clearly confirm the review scope before applying the checklist.

Risk: Checklist-based audit guidance can miss project-specific vulnerabilities or produce incomplete assurance.

Mitigation: Require human review and run the recommended Aptos compile, test, and coverage checks before deployment decisions.

Risk: A security audit workflow may encounter private keys or secret-bearing local files.

Mitigation: Do not read or disclose private key config, .env files, or secret-like values during review.

## Reference(s):

- [Aptos Move Security Guidelines](https://aptos.dev/build/smart-contracts/move-security-guidelines)
- [ClawHub Skill Page](https://clawhub.ai/iskysun96/skills/aptos-security-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown audit report with checklists, findings, recommendations, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external tools or credentials are requested by the skill.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
