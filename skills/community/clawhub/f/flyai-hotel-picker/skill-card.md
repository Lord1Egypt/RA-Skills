## Description:

Helps travelers narrow hotel options to three recommendations by comparing price, rating, preference fit, and location value near planned attractions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill to compare hotel candidates for a trip and get a short, decision-oriented recommendation. It is suited for hotel selection conversations where the agent can collect destination, dates, budget, preferences, and planned attractions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing or updating a third-party FlyAI CLI before search operations.

Mitigation: Review the package source and installation command before use, and install with least privilege where possible.

Risk: The skill includes TLS-bypass command examples for handling certificate failures.

Mitigation: Do not use TLS bypass in normal operation; fix certificate or network configuration instead.

Risk: The skill may store travel preferences and profile details as personal data.

Mitigation: Confirm user consent before saving preferences and avoid storing sensitive travel details unless needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-hotel-picker)
- [Hotel Search reference](reference/search-hotel.md)
- [POI / Attraction Search reference](reference/search-poi.md)
- [Marriott Hotel Search reference](reference/search-marriott-hotel.md)
- [User Profile Storage reference](reference/user-profile-storage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown recommendation card with concise hotel comparisons and supporting command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hotel names, prices, ratings, location analysis, recommendation rationale, and links returned by FlyAI search commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
