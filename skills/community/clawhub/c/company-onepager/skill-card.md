## Description:

Generates a one-page listed-company research brief with basic company information, market data, 10-year financial tables, monthly price charts, shareholder structure, recent news, and source labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laigen](https://clawhub.ai/user/laigen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to generate concise stock or listed-company research reports from financial data, market data, shareholder information, news, charts, and source annotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Tushare and iFinD credentials and contacts external financial and search services.

Mitigation: Use only credentials approved for this workflow, limit credential scope where possible, and run the skill only in an environment where those services are allowed.

Risk: The security scan flags disabled TLS verification, cross-skill Python import behavior, output path validation, and Markdown/PDF sanitization for review.

Mitigation: Review or fix those items before using the skill with valuable credentials, sensitive research targets, or untrusted output paths.

Risk: Generated financial research may rely on incomplete, stale, or unavailable third-party data.

Mitigation: Check the report's data-source labels and verify important figures against authoritative market or company filings before making decisions.

## Reference(s):

- [Data Sources](references/data_sources.md)
- [Tushare](https://tushare.pro)
- [Company Onepager on ClawHub](https://clawhub.ai/laigen/skills/company-onepager)
- [Publisher Profile](https://clawhub.ai/user/laigen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Generated report files and console output, including JSON data, PNG chart, Markdown report, HTML conversion, and PDF report paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a stock code input and writes outputs to the requested directory or an OpenClaw temp directory.]

## Skill Version(s):

7.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
