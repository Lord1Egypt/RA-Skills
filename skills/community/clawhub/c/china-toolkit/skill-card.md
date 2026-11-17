## Description:

中国效率工具集 provides Chinese-language lookup utilities for package tracking, exchange rates, Chinese holidays, mobile number attribution, and IP attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxg852621787](https://clawhub.ai/user/dxg852621787)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to answer China-focused productivity queries by invoking command-line utilities for logistics tracking, currency conversion, holiday schedules, phone number lookup, and IP lookup. It is most relevant for users who need concise Chinese-language operational lookups from public web services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package tracking numbers, phone numbers, and IP addresses are sent to public third-party services.

Mitigation: Review the skill before installation and avoid submitting sensitive identifiers unless sharing them with those services is acceptable.

Risk: IP lookup uses an unencrypted HTTP endpoint.

Mitigation: Avoid sensitive IP lookups where plaintext transit is unacceptable, or replace the provider with an approved HTTPS service before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxg852621787/skills/china-toolkit)
- [ClawHub publisher profile](https://clawhub.ai/user/dxg852621787)
- [Kuaidi100 package tracking API endpoint](https://www.kuaidi100.com/query)
- [ExchangeRate-API public endpoint](https://open.er-api.com/v6/latest/)
- [Timor holiday API endpoint](https://timor.tech/api/holiday/year/)
- [360 mobile number attribution endpoint](https://cx.shouji.360.cn/phonearea.php)
- [ip-api.com IP geolocation endpoint](http://ip-api.com/json/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON command output with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on public third-party API availability and the identifiers supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
