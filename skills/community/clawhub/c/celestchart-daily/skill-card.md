## Description:

CelestChart Astrology Skills lets an agent fetch CelestChart daily horoscope and birth chart data, then turn it into a user-facing astrology reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maye08](https://clawhub.ai/user/maye08)

### License/Terms of Use:

MIT-0

## Use Case:

External users configure a CelestChart API key and birth details so their agent can request and interpret daily transit forecasts or natal chart data. The skill is intended for astrology-oriented prompts where personalized horoscope guidance is expected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a CelestChart API key and birth date, time, and location details to xp.broad-intelli.com.

Mitigation: Use a dedicated revocable API key, review the release before installing, and only configure birth details you are comfortable sending to the CelestChart service.

Risk: Broad everyday horoscope phrases can invoke the skill and trigger external requests.

Mitigation: Invoke the skill only for explicit CelestChart or astrology requests, and review trigger behavior before using it in shared or sensitive agent environments.

Risk: Installing through an unpinned latest installer can make reviewed behavior harder to reproduce.

Mitigation: Prefer a pinned, reviewed installer version for deployment.

## Reference(s):

- [CelestChart homepage](https://xp.broad-intelli.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown narrative for users, with JSON returned from the CelestChart API for agent interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl plus CelestChart API key and birth detail environment variables; daily forecasts require VIP access.]

## Skill Version(s):

1.2.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
