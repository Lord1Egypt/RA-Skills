## Description:

Queries CTG Bus (hkctgbus) schedules, fares, and remaining seats from Chinese natural-language requests about cross-border bus travel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porridgec](https://clawhub.ai/user/porridgec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to parse Chinese CTG Bus travel requests, query hkctgbus schedules between supported Hong Kong, Macau, and mainland China cities, and summarize available departures, fares, and remaining seats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Route, station, and travel-date details are sent to the hkctgbus API when queries run.

Mitigation: Avoid using the skill for sensitive travel plans unless sharing those query details with hkctgbus is acceptable.

Risk: Generic cross-border bus wording may activate this skill when the user intended a different provider.

Mitigation: Confirm the user wants CTG Bus or hkctgbus before querying when the request only mentions cross-border bus travel generally.

## Reference(s):

- [hkctgbus API base endpoint](https://wechat.hkctgbus.com/ctb)
- [ClawHub skill page](https://clawhub.ai/porridgec/skills/ctg-bus)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON schedule data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script returns JSON that the agent formats into a human-readable timetable including stations, dates, fares, availability, and route details.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
