## Description:

This skill helps tenderers and procurement agents review Chinese tender documents before publication to identify clauses likely to draw supplier challenges and prepare risk-rated rewrites, legal-anchor directions, objection response points, and rationale records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement teams, tenderers, and procurement agents use this skill to perform pre-release compliance self-checks on Chinese tender documents. It scans tender requirements for exclusionary, discriminatory, or unreasonable thresholds and produces practical remediation guidance, objection-response preparation, and rationale records for retained requirements.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Tender documents can contain confidential procurement, commercial, or legal information.

Mitigation: Provide only tender materials the user is authorized to share with the agent and any connected knowledge bases.

Risk: Legal references and procurement rules may change or may be misapplied to the wrong procurement regime.

Mitigation: Verify all legal references against current official sources and keep the skill's government procurement, engineering tendering, and state-owned enterprise procurement tracks separate.

Risk: The skill's findings are compliance self-check guidance, not legal advice or a substitute for counsel on high-risk procurement decisions.

Mitigation: Use the output as a review aid and consult qualified counsel before relying on it for material procurement or dispute-response decisions.

Risk: Helper-script pre-screening can miss context or produce false positives because it mechanically flags candidate clauses.

Mitigation: Review script hits against the full tender document, the compliance signal guide, and the user-provided procurement context before treating them as report findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-carrot-pit-tenderer-1-0-0)
- [Compliance signals](artifact/references/compliance-signals.md)
- [Legal anchors](artifact/references/legal-anchors.md)
- [Compliance self-check report template](artifact/templates/compliance-selfcheck-report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown compliance report with tables, legal-anchor directions, rewrite suggestions, objection-response points, and optional JSON/CSV helper-script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can use optional local helper scripts for section splitting and batch pre-screening, then relies on agent review for legal-risk classification and remediation prose.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
