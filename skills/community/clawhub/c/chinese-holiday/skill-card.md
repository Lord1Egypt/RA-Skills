## Description:

查询中国法定节假日、周末和调休安排，帮助判断指定日期是工作日还是节假日。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check Chinese holiday, weekend, and make-up workday status for one or more dates. It is useful for scheduling, calendar checks, and holiday arrangement lookups involving Chinese public holidays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Date checks call a third-party holiday API and reveal the queried year or date range to that service.

Mitigation: Avoid using sensitive date queries when third-party API disclosure is unacceptable, or review network behavior before installation.

Risk: If the holiday API is unavailable, results fall back to weekday/weekend classification and may miss make-up workday or holiday adjustments.

Mitigation: Verify important scheduling decisions against an authoritative holiday source when the output reports fallback behavior or when high accuracy is required.

## Reference(s):

- [Timor holiday API](https://timor.tech/api/holiday/year/{year})
- [ClawHub skill page](https://clawhub.ai/weidongkl/skills/chinese-holiday)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON from a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one or more dates in YYYY-MM-DD or YYYYMMDD format and reports workday or holiday status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
