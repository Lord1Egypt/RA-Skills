## Description:

Check EV charger availability (favorites, nearby search) via Google Places.

This skill is ready for commercial/non-commercial use.

## Publisher:

[borahm](https://clawhub.ai/user/borahm)

### License/Terms of Use:


## Use Case:

External users and operators use this skill to check EV charger availability by favorite, place ID, query, or nearby location, and optionally trigger scheduled notifications when a charger becomes available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Google Places API key and may reveal charger lookup usage to the API provider and skill publisher.

Mitigation: Provide GOOGLE_PLACES_API_KEY only when you trust the publisher and are comfortable with the charger lookup usage.

Risk: Optional recurring notifications store last-seen charger availability state in the user's local cache.

Mitigation: Enable cron-based notifications only when recurring checks are desired, and review or clear ~/.cache/charger-notify state as needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/borahm/skills/charger)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and plain text notification output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOOGLE_PLACES_API_KEY; optional notification state is stored under the user's local cache.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
