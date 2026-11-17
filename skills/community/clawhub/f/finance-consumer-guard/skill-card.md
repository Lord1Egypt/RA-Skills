## Description:

Checks Chinese financial product marketing, sales scripts, advertisements, website copy, and public-facing promotional text before publication for high-risk consumer-protection phrases and returns risk-ranked findings with revision guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Financial institutions, wealth managers, compliance teams, operations teams, and agents use this skill as a lightweight pre-publication guard for Chinese financial marketing and sales copy. It flags phrases related to guaranteed principal or returns, exaggerated yield claims, weakened risk disclosure, misleading past performance, unqualified sales activity, and advertising superlatives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat phrase matches and suggested revisions as legal advice or proof of compliance.

Mitigation: Use the output only as an auxiliary pre-publication check and route material decisions to qualified compliance or legal reviewers.

Risk: The local term-list approach can miss context-dependent violations or flag text that needs human interpretation.

Mitigation: Review flagged and unflagged high-impact copy against current regulations, product disclosures, and institutional policies before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/finance-consumer-guard)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text report or structured JSON findings from a Python CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a clean or flagged decision, highest risk level, finding count, matched terms, categories, severity, positions, and suggested revisions.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json, CHANGELOG, and skill text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
