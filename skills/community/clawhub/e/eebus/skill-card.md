## Description:

查询永东直通巴士（eebus）班次、票价和余座，支持中文自然语言输入并自动解析日期、上车点和下车点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[porridgec](https://clawhub.ai/user/porridgec)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to check Yongdong cross-border bus schedules, fares, and remaining seats between Hong Kong and Shenzhen from Chinese travel requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends queried dates and station names to www.myeebus.com.

Mitigation: Use it only for eebus-specific Hong Kong/Shenzhen bus lookups and avoid entering sensitive personal information.

Risk: The skill relies on embedded API signing logic for the external bus service.

Mitigation: Review behavior before deployment and re-check functionality if the bus service changes its API.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with a route summary and tabular schedule details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a Node.js query script against www.myeebus.com and summarizes all returned bus departures, fares, and remaining seats.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
