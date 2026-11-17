## Description:

A-share (Chinese stock market) daily briefing that collects index data, sector rankings, capital flows, major announcements, and generates a structured daily report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bustes01](https://clawhub.ai/user/bustes01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to generate a concise daily briefing on China's A-share market, including indices, sector movement, capital flows, market sentiment, announcements, and next-day watch items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional API mode sends requests to AShareHub using a user-provided API key.

Mitigation: Confirm AShareHub is trusted before use and use a dedicated API key with only the needed access.

Risk: Market data may be delayed or unavailable, and the generated brief could be mistaken for investment advice.

Mitigation: Treat the brief as informational only, preserve unavailable-data markings, and keep the investment-advice disclaimer visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bustes01/skills/astock-daily-brief)
- [ClawHub homepage metadata](https://clawhub.ai/BusTes01/astock-daily-brief)
- [AShareHub](https://asharehub.com/zh/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown daily market brief with optional shell command examples for API access]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public web search by default; optional AShareHub API mode requires ASHAREHUB_API_KEY.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
