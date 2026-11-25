## Description:

Research-grade astronomical data from NASA/JPL DE440 through the Astro Agents API: sunrise, sunset and twilight, altitude and azimuth, observation windows, Moon phase and distance, the day's sky for a place, planet positions, eclipses with local circumstances, planetary phenomena, seasons, celestial event calendars, longitude time series, time scales and coordinate conversion, for any date 1800-2200. Use it when a task needs exact astronomical times, positions or events instead of estimating them: every result is computed (no LLM) and SHA-256 verifiable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidatatools-dev](https://clawhub.ai/user/aidatatools-dev)

### License/Terms of Use:

MIT

## Use Case:

Developers and other users can request precise astronomical times, positions, and events for a date or observing location, including sunrise and twilight, planetary positions, lunar data, eclipses, and coordinate conversions. The skill is useful when an agent needs sourced astronomical results instead of estimating them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Place-based requests send the supplied location and requested date or time to astro-agent.dev.

Mitigation: Provide only a location and date or time you are comfortable sharing; leave out location when the query does not require one.

## Reference(s):

- [Astro Agents documentation](https://astro-agent.dev/docs)
- [Astro Agents API reference](https://astro-agent.dev/llms-full.txt)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured astronomy data with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include stated calculation conventions and a SHA-256 result hash for verification.]

## Skill Version(s):

1.10.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
