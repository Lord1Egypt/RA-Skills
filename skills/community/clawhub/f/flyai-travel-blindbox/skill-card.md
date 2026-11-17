## Description:

旅行盲盒 helps an agent collect travel constraints, build a compliant destination pool, randomly reveal a surprise destination, and produce a trip plan with flight, hotel, and POI options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan surprise trips by setting limits such as budget, travel dates, flight duration, and excluded destinations. The agent searches travel options, randomly selects a destination that fits the constraints, and presents a concise itinerary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install or run latest-version Node packages and may suggest sudo for installation.

Mitigation: Verify the FlyAI CLI package identity, version, and integrity before installation; avoid sudo unless the operator has reviewed the command and environment.

Risk: The workflow includes commands with NODE_TLS_REJECT_UNAUTHORIZED=0, which disables TLS certificate verification.

Mitigation: Do not run commands with TLS verification disabled; resolve certificate issues or use a trusted network and package source instead.

Risk: The skill can persist travel preferences, household details, and visited cities through memory tools or a local profile file.

Mitigation: Enable profile storage only after user consent, limit saved data to necessary preferences, and provide a clear way to inspect and delete stored data.

Risk: Travel prices and availability can change after search results are shown.

Mitigation: Treat prices as current estimates and ask the user to verify booking details before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-travel-blindbox)
- [FlyAI tool overview](reference/tools.md)
- [Travel blind-box workflow](reference/workflow.md)
- [Weighted random destination algorithm](reference/algorithm.md)
- [Flight search reference](reference/search-flight.md)
- [Hotel search reference](reference/search-hotel.md)
- [POI search reference](reference/search-poi.md)
- [User profile storage](reference/user-profile-storage.md)
- [Example dialogues](reference/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and structured travel-plan summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current travel search results, user-confirmed profile data, and randomized destination selection; prices require user review before booking.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
