## Description:

Helps an agent plan immediate, time-constrained travel by searching feasible flights, hotels, attractions, and booking links from a user's departure city and earliest departure time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to identify destinations reachable on short notice, compare flight, hotel, and attraction options, and prepare concise booking-oriented itineraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the user to install or upgrade a global CLI package, including a sudo-based fallback.

Mitigation: Review installation steps before execution, avoid the sudo install path, and prefer a pinned CLI version in a sandboxed environment.

Risk: The artifact describes disabling TLS certificate verification when CLI requests fail.

Mitigation: Keep TLS verification enabled and resolve certificate or network issues without using NODE_TLS_REJECT_UNAUTHORIZED=0.

Risk: The skill can save personal and family travel preferences in memory or a local profile file.

Mitigation: Ask for explicit user consent before persistence, minimize stored profile details, and avoid saving sensitive travel or family information unless the user accepts that storage.

Risk: Travel prices, availability, and booking links are time-sensitive and may change quickly.

Mitigation: Label results as time-sensitive, prompt the user to confirm details at booking time, and avoid presenting stale search output as guaranteed availability.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hello-ahang/skills/flyai-instant-departure)
- [Workflow](reference/workflow.md)
- [User Profile Storage](reference/user-profile-storage.md)
- [Examples](reference/examples.md)
- [Flight Search](reference/search-flight.md)
- [Train Search](reference/search-train.md)
- [Hotel Search](reference/search-hotel.md)
- [POI / Attraction Search](reference/search-poi.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel options with command examples, structured itinerary details, prices, timing, and booking links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include time-sensitive prices, seat or room availability, local user travel preferences, and external booking URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
