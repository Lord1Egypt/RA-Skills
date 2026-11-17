## Description:

Provides flight prices, public transport and train journeys, and nearby EV charge points using Amadeus, Navitia, and Open Charge Map APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaureli](https://clawhub.ai/user/aaureli)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to request flight pricing, train or public transport itineraries, and nearby EV charging station information through the referenced travel APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alias wrapper scripts can execute another local Python file from the current working directory.

Mitigation: Install only when the canonical air-train-ev skill at the expected path is intentional and trusted.

Risk: API credentials may be exposed to code reached through the canonical skill path.

Mitigation: Review the canonical skill before use and prefer wrappers that resolve paths relative to a trusted install location before using credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaureli/skills/air-train-ev-alias)
- [Publisher profile](https://clawhub.ai/user/aaureli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or text guidance with script-backed travel and charging results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Amadeus, Navitia, and Open Charge Map credentials; alias wrappers route to the canonical air-train-ev skill.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
