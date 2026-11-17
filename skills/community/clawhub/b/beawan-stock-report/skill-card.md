## Description:

查询A股上市公司财务报告分析地址，支持一季报、中报、三季报、年报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sqjsytqte](https://clawhub.ai/user/sqjsytqte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up financial report analysis pages for A-share listed companies by stock code, year, and report type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if sent over the documented plaintext HTTP endpoints.

Mitigation: Use the skill only if the provider supports HTTPS for the API and returned report pages; rotate any key that may already have been used over plaintext HTTP.

Risk: The skill depends on a third-party provider API and externally hosted report pages.

Mitigation: Review the provider, endpoint availability, and returned URLs before relying on results in financial workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sqjsytqte/skills/beawan-stock-report)
- [Beawan report lookup API endpoint](http://api.beawan.com/beawanSkill/api/skill/report)

## Skill Output:

**Output Type(s):** [guidance, configuration, api_calls, text]

**Output Format:** [Markdown instructions with HTTP request examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key and returns a report analysis URL when the provider API succeeds.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
