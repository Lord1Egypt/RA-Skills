## Description:

Tracks public U.S. congressional stock trade disclosures, highlights concentrated buying and anomaly signals, and helps agents relate trade patterns to committees, legislation, and regulatory events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goatdeesign](https://clawhub.ai/user/goatdeesign)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch public U.S. congressional trade disclosures, filter them by politician, ticker, chamber, transaction type, or amount, and produce structured research reports with concentration and anomaly analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market analysis could be mistaken for investment advice.

Mitigation: Present outputs as research only and include the required non-investment-advice disclaimer.

Risk: Congressional trading disclosures can lag and are not real-time.

Mitigation: Tell readers that public disclosures may be delayed by up to 45 days before drawing conclusions.

Risk: The skill fetches public web data and can write JSON or CSV files to requested paths.

Mitigation: Review command arguments and choose output paths deliberately before execution.

Risk: Public data sources or website structures may change and cause incomplete or failed fetches.

Mitigation: Treat empty or failed fetch results as source availability issues and verify important findings against public disclosures.

## Reference(s):

- [Congressional trade analysis framework](references/analysis_framework.md)
- [Congressional committee and industry map](references/committee_industry_map.md)
- [Capitol Trades public trade data](https://www.capitoltrades.com/trades)
- [ClawHub skill page](https://clawhub.ai/goatdeesign/skills/congress-stock-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, shell commands, guidance]

**Output Format:** [Markdown research reports with tables, plus JSON or CSV data from the fetch script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save JSON or CSV files to user-selected paths; reports should include disclosure-delay and non-investment-advice disclaimers.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
