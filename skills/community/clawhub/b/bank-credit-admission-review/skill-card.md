## Description:

Helps bank credit and risk teams screen admission red flags and prepare evidence-based preliminary credit review reports for corporate borrowers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chriskinhaha](https://clawhub.ai/user/chriskinhaha)

### License/Terms of Use:

MIT-0

## Use Case:

Bank credit approval and risk-management staff use this skill to screen corporate borrowers against admission red flags, review business and financial risks, and prepare a sourced preliminary report with due-diligence gaps and a proposed admission outcome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive banking records may be exposed through third-party data lookups.

Mitigation: Approve use of 财汇MCP, WebSearch, and Neodata for the data involved; redact customer audit reports, credit records, identifiers, and review notes before external calls.

Risk: Local caches and reusable review history may retain sensitive customer information.

Mitigation: Restrict access to local SQLite, rules, and case files, and require human review before adding reusable rules or case history.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/chriskinhaha/skills/bank-credit-admission-review)
- [Admission red-line criteria](references/negative_criteria.md)
- [Four-dimensional analysis framework](references/analysis_framework.md)
- [Source reliability and data gaps](references/source_reliability.md)
- [Credit review report template](references/report_template.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Structured Markdown screening or preliminary credit review report; screening calculations can also be emitted as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evidence sources, missing-data flags, risk rating, proposed admission outcome, and follow-up due-diligence items.]

## Skill Version(s):

1.4.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
