## Description:

CompanyInformation queries FEEDAX company news and public-opinion data for listed companies, including sentiment, heat score, industry classification, related companies, and risk-oriented news signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longgggggg](https://clawhub.ai/user/longgggggg)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to query recent company news, monitor negative or positive public-opinion signals, and export company-news results for deeper review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed because the security evidence reports plaintext HTTP use and query-parameter key handling.

Mitigation: Use a scoped FEEDAX key from a secure secret store or environment variable, avoid pasting keys into chat or agent memory, and rotate any key used with this version.

Risk: Generated CSV files may carry spreadsheet-opening risk.

Mitigation: Review generated CSV content before opening it in spreadsheet software.

## Reference(s):

- [FEEDAX](https://www.feedax.cn)
- [ClawHub skill page](https://clawhub.ai/longgggggg/skills/company-information)
- [Publisher profile](https://clawhub.ai/user/longgggggg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, CSV files]

**Output Format:** [Conversation summary plus generated CSV and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows a top-result summary in conversation and can write timestamped company_information CSV and Markdown files.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
