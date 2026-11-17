## Description:

平替旅行家 helps users decompose the core experience of an expensive, distant, or difficult dream destination and find closer or lower-cost substitute destinations with transparent tradeoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to turn a desired but impractical destination into substitute trip options based on budget, time, visa difficulty, distance, transport, lodging, attractions, and experiential similarity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags mutable global FlyAI CLI installation and a sudo fallback as suspicious.

Mitigation: Review the package before installation, pin a trusted version where possible, and use a user-scoped Node environment instead of sudo.

Risk: The security guidance flags commands that disable TLS verification with NODE_TLS_REJECT_UNAUTHORIZED=0.

Mitigation: Do not disable TLS verification; use normal TLS validation and fail closed until the package or endpoint certificate issue is fixed.

Risk: The skill can read or save travel preferences in Qoder Memory or a local ~/.flyai/user-profile.md file.

Mitigation: Ask before saving preferences, keep sensitive travel details out of the profile, and let users review or remove stored profile data.

## Reference(s):

- [Workflow](reference/workflow.md)
- [Tools](reference/tools.md)
- [User Profile Storage](reference/user-profile-storage.md)
- [Examples](reference/examples.md)
- [AI Search](reference/ai-search.md)
- [Keyword Search](reference/keyword-search.md)
- [Flight Search](reference/search-flight.md)
- [Hotel Search](reference/search-hotel.md)
- [POI / Attraction Search](reference/search-poi.md)
- [Train Search](reference/search-train.md)
- [Marriott Hotel Search](reference/search-marriott-hotel.md)
- [Marriott Package Search](reference/search-marriott-package.md)
- [Self-Learning](reference/self-learning.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown travel recommendations with inline shell commands and JSON-shaped examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include destination match scores, cost comparisons, transport and lodging options, attraction summaries, tradeoff notes, and optional user-profile updates.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
