## Description:

Query gov.cn Chinese holiday notices to determine workdays, holidays, and make-up workdays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silent-blue](https://clawhub.ai/user/silent-blue)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer China holiday-calendar questions for a specific date or month, including statutory holidays, make-up workdays, weekday status, lunar date summaries, and solar terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Captured API signing material is included for the gov.cn search flow.

Mitigation: Replace the captured values with an authorized access method before deployment and rotate or remove any values that should not be distributed.

Risk: The notice-body fetch path accepts a selected URL and may follow unexpected destinations.

Mitigation: Restrict notice fetches to official gov.cn hosts, reject redirects to localhost or private-network addresses, and keep request timeouts enabled.

Risk: Refreshing holiday data performs network requests during normal use when a yearly cache is missing.

Mitigation: Review the skill before installation and refresh official holiday data only as needed, using cached yearly data for routine queries.

## Reference(s):

- [Gov Holiday Reference](references/api_reference.md)
- [gov.cn holiday notice search endpoint](https://sousuoht.www.gov.cn/athena/forward/2B22E8E39E850E17F95A016A74FCB6B673336FA8B6FEC0E2955907EF9AEE06BE)
- [Example State Council holiday notice](https://www.gov.cn/gongbao/2025/issue_12406/202511/content_7048922.html)
- [ClawHub skill page](https://clawhub.ai/silent-blue/skills/cn-holiday-calendar)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown tables for month queries and short structured JSON-style summaries for single-date queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional expanded lunar calendar details when requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
