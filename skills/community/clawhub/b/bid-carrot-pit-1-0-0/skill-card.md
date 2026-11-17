## Description:

This skill reviews full Chinese tender documents from a bidder perspective to identify suspected exclusionary, discriminatory, or tailor-made requirements and draft risk-ranked Markdown reports with legal-reference directions and challenge or complaint language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External bidders, procurement reviewers, and tender-response teams use this skill to scan complete tender documents for suspected exclusionary clauses, locate risky provisions, and prepare review-ready challenge or complaint drafts. It is intended as an analysis aid, not a legal determination.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated legal-reference directions or complaint language may be inaccurate, outdated, or mismatched to the tender's legal system.

Mitigation: Treat complaint text as a draft and verify the project type, legal system, and cited law through an authoritative legal source or counsel before filing.

Risk: Incomplete tender input or unread appendices, payment terms, or hard-marker clauses can cause the analysis to miss exclusionary requirements.

Mitigation: Provide the complete tender file and review the report's blind-spot checks before acting on the findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-carrot-pit-1-0-0)
- [Carrot-pit signal scale](artifact/references/carrot-pit-signals.md)
- [Legal anchor table](artifact/references/legal-anchors.md)
- [Report template](artifact/templates/carrot-pit-report.md)
- [Regression test cases](artifact/test_cases/cases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown tender-risk report with optional shell command for local section splitting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include clause excerpts, risk levels, signal categories, combination analysis, legal-reference directions, challenge or complaint draft language, legal-verification reminders, and disclaimers.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact manifest reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
