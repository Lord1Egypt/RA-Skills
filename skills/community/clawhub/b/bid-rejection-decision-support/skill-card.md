## Description:

Supports procurement evaluation committees in deciding whether a specific bidder response should be rejected, clarified, or corrected, and drafts report-ready rejection wording with clause and legal-basis references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement evaluation committee members use this skill when they have a specific bidder response and the corresponding tender clause and need a structured rejection, clarification, or correction decision. It helps produce a decision opinion with facts, applicable clauses, legal basis, complaint-review considerations, and standardized wording for evaluation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bid facts, evaluation records, prices, bidder deficiencies, complaint strategy, or personal data may be sensitive.

Mitigation: Use only in an approved environment and redact real names, project identifiers, exact prices, personal data, and confidential document text unless the organization has approved that data flow.

Risk: The skill may use external knowledge search when the runtime provides an approved IMA MCP connection.

Mitigation: Confirm the knowledge-base environment is approved for the matter and avoid confidential search queries unless that use has been authorized.

Risk: AI-generated procurement guidance could be incorrect or insufficient for a legally significant evaluation decision.

Mitigation: Treat outputs as decision support only; require evaluation committee review, source verification, complete recordkeeping, and legal counsel for high-stakes matters.

## Reference(s):

- [Decision framework](artifact/references/decision_framework.md)
- [Rejection wording templates](artifact/references/rejection_wording_templates.md)
- [Knowledge-base mounting guidance](artifact/references/kb_mounting.md)
- [Discipline redlines and compliance guardrails](artifact/references/discipline_redlines.md)
- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-rejection-decision-support)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown decision opinion with structured sections and optional clause/legal citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include rejection, clarification, or correction determinations, risk level, complaint-review notes, and standardized report wording.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, manifest.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
