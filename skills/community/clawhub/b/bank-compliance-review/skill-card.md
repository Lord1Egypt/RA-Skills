## Description:

Supports bank compliance staff with draft reviews of marketing materials, KYC and AML cases, regulatory controls, and reporting checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gechengling](https://clawhub.ai/user/gechengling)

### License/Terms of Use:

MIT-0

## Use Case:

Bank compliance officers and KYC/AML analysts use it to draft checklists and preliminary review notes for promotional materials, customer due diligence, alerts, regulatory controls, and reporting. Qualified staff must verify the drafts; the skill does not make final compliance determinations, provide formal legal opinions, or submit reports.

### Deployment Geography for Use:

China; the skill states that it does not cover compliance determinations under overseas regulatory systems.

## Known Risks and Mitigations:

Risk: The security evidence reports a partial inspection with zero-percent coverage, a malformed manifest, an unresolved local reference, and a possible instruction-scope concern.

Mitigation: Treat the benign verdict as limited evidence, consider the scanner guidance before installing, and review the package and unresolved manifest/reference issues.

Risk: Compliance examples may involve sensitive personal, account, or transaction information.

Mitigation: Provide only necessary information, replace direct identifiers with placeholders, and use aggregated transaction descriptions where possible.

Risk: Draft reviews may be incomplete or outdated and could be mistaken for a final compliance decision.

Mitigation: Have qualified staff verify current official requirements and internal procedures before relying on or sharing a draft; do not treat it as a legal opinion or final customer determination.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gechengling/skills/bank-compliance-review)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Chinese-language text or Markdown checklists, review notes, and draft reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference drafts for human review; no regulatory-system or external-database connection, report submission, or file writing.]

## Skill Version(s):

4.1.5 (source: SKILL.md frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
