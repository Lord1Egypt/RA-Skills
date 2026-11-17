## Description:

Find 24-hour businesses, well-lit public areas, transit stations, police stations, and hospitals near any location for late night safety awareness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check nearby late-night safety resources around coordinates, such as hospitals, police stations, transit, open businesses, and pharmacies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install guidance in the artifact includes mutable remote sources and recommends installing a broader companion suite outside this reviewed skill.

Mitigation: Prefer a pinned ClawHub version or immutable commit, and install only camino-safety-checker unless the additional skills have also been reviewed.

Risk: The skill sends queried coordinates, radius, and the Camino API key to an external API.

Mitigation: Use it only when sharing that location context with Camino is acceptable, and scope API key access to the agent environment that needs the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/james-southendsolutions/skills/camino-safety-checker)
- [Camino API Activation](https://app.getcamino.ai/skills/activate)
- [Camino API Endpoint](https://api.getcamino.ai/context)
- [x402](https://x402.org)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON returned by shell commands, with Markdown usage examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAMINO_API_KEY plus curl and jq; sends coordinates and radius to the Camino external API.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
