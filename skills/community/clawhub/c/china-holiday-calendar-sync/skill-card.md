## Description:

Discover and parse China's official holiday notices from gov.cn, normalize holiday and adjusted-workday rows, and apply low-frequency probing rules for future years.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyyyy0430](https://clawhub.ai/user/joeyyyy0430)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build or maintain China business holiday calendars from official gov.cn notices, including adjusted workdays and holiday-aware weekly scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future-year holiday schedules may be unavailable until an official notice is published.

Mitigation: Return no future-year URL until a validated gov.cn notice exists, and cache negative checks by month to avoid excessive probing.

Risk: Calendar accuracy depends on accepting only authoritative notices.

Mitigation: Use configured official notice URLs first, prefer gov.cn policy search for discovery, and validate candidate page titles or official content before trusting them.

Risk: Local calendar configuration or cache may be modified during synchronization.

Mitigation: Review project storage paths before use and keep stable notice URLs separate from short-lived discovery cache records.

## Reference(s):

- [Official Notice Method](references/official-notice-method.md)
- [China Holiday Calendar Sync on ClawHub](https://clawhub.ai/joeyyyy0430/skills/china-holiday-calendar-sync)
- [joeyyyy0430 Publisher Profile](https://clawhub.ai/user/joeyyyy0430)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-shaped examples and implementation details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces normalized holiday and adjusted-workday rows with date, is_holiday, is_workday, holiday_name, and source_url fields.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
