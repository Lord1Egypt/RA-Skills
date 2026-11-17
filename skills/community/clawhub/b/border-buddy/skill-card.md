## Description:

Border Buddy provides pre-trip border intelligence for visa requirements, passport validity, Schengen 90/180-day stay calculations, yellow-fever certificate needs, customs limits, and transit-visa checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External travelers, travel planners, and AI agents use this skill for first-pass international trip checks across visa, transit, passport, Schengen stay, customs, and health-certificate requirements. It should be paired with official authority verification before booking or travel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel and border rules may be stale because the skill uses an offline rules snapshot.

Mitigation: Treat outputs as planning guidance and verify visa, passport, transit, customs, and health rules with the named official authorities near the travel date.

Risk: Users may mistake trip-planning output for legal immigration advice.

Mitigation: Use the skill for short-term travel readiness only and refer asylum, residency, work-permit, waiver, or criminal-record entry questions to official channels or qualified legal counsel.

Risk: Incorrect or missing itinerary details can change the result, especially for transits and Schengen repeat travel.

Mitigation: Collect nationality, every destination and transit point, purpose, dates, passport expiry, and prior Schengen visits before presenting a conclusion.

## Reference(s):

- [Border Buddy ClawHub Skill Page](https://clawhub.ai/voronindenis5/skills/border-buddy)
- [Visa Rules Knowledge Model](references/visa-rules.md)
- [The Schengen 90/180 Rule](references/schengen-180.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text reports with inline shell commands and optional JSON rule dumps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline snapshot-based guidance; reports include authority names for verification.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
