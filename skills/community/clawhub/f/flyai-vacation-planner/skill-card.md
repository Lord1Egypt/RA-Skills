## Description:

Helps Chinese-language travelers compare leave-extension vacation plans, then queries FlyAI travel commands for flight, hotel, destination, and visa context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to identify efficient vacation periods around Chinese holidays, compare travel dates, and gather flight, hotel, destination, and visa information for a chosen trip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install or upgrade an unpinned global FlyAI CLI package.

Mitigation: Install only after trusting the FlyAI CLI publisher, avoid sudo unless the system-wide risk is accepted, and review the global npm package before use.

Risk: The skill may read or persist personal travel-profile data such as budget, family details, travel history, and accessibility needs.

Mitigation: Treat travel profiles as personal data, ask before saving preferences, and prefer one-time use when the user does not want data persisted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hello-ahang/skills/flyai-vacation-planner)
- [User Profile Storage](reference/user-profile-storage.md)
- [China Holiday Reference](reference/holidays-cn.md)
- [Flight Search](reference/search-flight.md)
- [Hotel Search](reference/search-hotel.md)
- [Keyword Search](reference/keyword-search.md)
- [POI Search](reference/search-poi.md)
- [Train Search](reference/search-train.md)
- [Visa Rules](reference/visa-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured travel plan cards and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference live FlyAI CLI results and optional saved user travel profile data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
