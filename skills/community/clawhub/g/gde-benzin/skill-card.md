## Description:

Find nearby fuel stations in Russia and check reported availability and prices for a chosen petrol or diesel grade using the official API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tylnyi](https://clawhub.ai/user/tylnyi)

### License/Terms of Use:

MIT-0

## Use Case:

Drivers in Russia can use this skill to find nearby stations and review reported availability and prices for the selected fuel type.

### Deployment Geography for Use:

Russia

## Known Risks and Mitigations:

Risk: A location lookup may send a user's address or coordinates to gde-benzin.ru.

Mitigation: Tell the user when a precise location will be sent; use only a location they provided or authorized, and offer a city-level search when appropriate.

## Reference(s):

- [API contract](references/api.md)
- [Official gde-benzin.ru API](https://gde-benzin.ru/api)
- [gde-benzin.ru](https://gde-benzin.ru)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or concise text with station details and links; optional JSON lookup output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live results; availability and prices may have different ages.]

## Skill Version(s):

1.1.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
