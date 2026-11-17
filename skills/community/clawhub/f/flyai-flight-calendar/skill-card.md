## Description:

机票低价日历助手，帮助时间弹性的用户找到最便宜的出发日期，扫描出发地、目的地和弹性日期范围内的每日机票价格并生成可视化低价日历。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and assistant agents use this skill to compare flexible departure dates, find low-price flight windows, and produce booking-oriented recommendations. It is most useful when the traveler can vary travel dates and wants a calendar view of round-trip flight prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow instructs agents to bypass TLS certificate validation.

Mitigation: Do not run commands with NODE_TLS_REJECT_UNAUTHORIZED=0; use a verified TLS configuration or stop until the CLI endpoint can be trusted.

Risk: The workflow installs a global npm CLI using an unpinned @latest version and may suggest sudo.

Mitigation: Install a pinned, reviewed CLI version in an isolated environment and avoid sudo or global installation where possible.

Risk: Returned booking links may send users to external destinations.

Mitigation: Treat booking links as untrusted until the CLI output and destination domains are independently verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-flight-calendar)
- [Core workflow](reference/core-workflow.md)
- [Flight search reference](reference/search-flight.md)
- [Examples](reference/examples.md)
- [User profile storage](reference/user-profile-storage.md)
- [Advanced features](reference/advanced.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with calendar tables, recommendation summaries, inline shell commands, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight prices are time-sensitive and booking links should be treated as untrusted until independently verified.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
