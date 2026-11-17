## Description:

Didichuxing helps agents compare DiDi ride-hailing options, estimate fare ranges, plan peak-hour travel, and guide enterprise API integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compare DiDi travel products, estimate fare ranges, plan around peak demand or weather, and understand enterprise ride policy and API integration patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API examples may involve client secrets, employee phone numbers, trip locations, or billing data.

Mitigation: Use only organization-approved DiDi Enterprise access, review API behavior before use, and avoid entering real sensitive data unless authorized.

Risk: Fare estimates can differ from real app prices because city rates, routing, wait time, weather, and dynamic pricing change.

Mitigation: Present estimates as ranges and ask users to confirm final pricing in the DiDi app or approved enterprise tooling.

Risk: Travel advice for late-night or remote trips can affect personal safety.

Mitigation: Include practical safety reminders such as route sharing and emergency contacts when the trip context suggests elevated risk.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhangifonly/skills/didichuxing)
- [DiDi Enterprise API Endpoint](https://api.es.xiaojukeji.com)
- [DiDi Open Platform](https://open.didichuxing.com)
- [DiDi Enterprise Console](https://es.xiaojukeji.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with optional Python code snippets and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fare ranges, ride-selection rationale, peak-hour strategies, enterprise API examples, policy configuration examples, and safety reminders.]

## Skill Version(s):

1.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
