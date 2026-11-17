## Description:

Check calendar JSON for overlapping meetings and free time inside an explicit planning window, without network access or calendar changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adithng](https://clawhub.ai/user/adithng)

### License/Terms of Use:

MIT-0

## Use Case:

External users can provide an authorized calendar export to identify overlapping meetings and free time within a bounded planning window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar results can reveal meeting titles and conflicts.

Mitigation: Use only calendar data the user authorizes and keep the output private.

## Reference(s):

- [ClawHub release](https://clawhub.ai/adithng/skills/cardinal-calendar-check)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [JSON conflict and free-time results with a concise natural-language summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only results displayed in the requested IANA time zone.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
