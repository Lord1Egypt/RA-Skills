## Description:

Compares patent portfolios for two to five companies, including totals, legal status, invention share, yearly filings, overlapping technology areas, and distinctive strengths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Business teams, investors, and procurement professionals use this skill to compare the patent portfolios and technology areas of two to five companies. It organizes patent data into a comparison table and highlights shared and distinctive areas without treating patent counts as a measure of overall technical or market strength.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using a paid API key can expose credentials and send company names or technical terms to an external service; poorly controlled retries may also incur charges.

Mitigation: Before using a paid key, validate the HTTPS destination and handle redirects safely; protect saved credential files, share only company names and technical terms approved for external processing, set a spending limit, and check provider billing before retrying a timed-out whole-patent request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ip930/skills/company-patent-compare)
- [PatentMax](https://ip930.com)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [PatentMax API reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Analysis, Markdown, CSV file]

**Output Format:** [Concise comparison guidance and a UTF-8 CSV table suitable for spreadsheet applications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares two to five companies; includes source attribution and caveats about interpreting patent counts.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
