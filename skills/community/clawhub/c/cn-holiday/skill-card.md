## Description:

Queries Chinese public holidays, make-up workdays, and annual holiday schedules through the timor.tech API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deusyu](https://clawhub.ai/user/deusyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer user questions about whether China dates are workdays, holidays, make-up workdays, or upcoming days off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Holiday query dates are sent to the external timor.tech API.

Mitigation: Avoid submitting sensitive date patterns or internal planning details if external API disclosure is not acceptable.

Risk: Answers depend on timor.tech availability and the API's holiday data.

Mitigation: Check for transport or API errors and verify important scheduling decisions against an official source when accuracy is critical.

## Reference(s):

- [Command Map](references/command-map.md)
- [timor.tech Holiday API](https://timor.tech/api/holiday)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results interpreted in natural language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces date, year, batch, and next-day holiday or workday query guidance; runtime results depend on timor.tech API availability and data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
