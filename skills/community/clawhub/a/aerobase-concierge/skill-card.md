## Description:

Autonomous jetlag concierge - auto-scores flights, monitors deals, generates recovery plans, and guards itineraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:


## Use Case:

External travelers and travel assistants use this skill to compare flight jetlag impact, monitor travel deals, produce recovery plans, and guard upcoming itineraries with quantified recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make proactive API calls or monitor travel context before the user expects that behavior.

Mitigation: Require clear user opt-in before deal monitoring, itinerary guarding, or other autonomous checks.

Risk: The skill may infer or retain sensitive travel preferences such as home airport, loyalty programs, chronotype, and upcoming trips.

Mitigation: Collect only the travel details needed for the current task and avoid sharing loyalty or trip information unless the user trusts Aerobase's data handling.

## Reference(s):

- [Aerobase API base URL](https://aerobase.app/api)
- [Aerobase Concierge ClawHub page](https://clawhub.ai/kurosh87/skills/aerobase-concierge)
- [Publisher profile](https://clawhub.ai/user/kurosh87)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown with concise recommendations, quantified scores, API setup commands, and JSON-render card examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured travel card payloads for lounges, hotels, credit cards, and loyalty programs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
