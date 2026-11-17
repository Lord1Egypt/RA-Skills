## Description:

Provides beach surf, weather, UV, and swimming-safety reports through an MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanfoglia](https://clawhub.ai/user/evanfoglia)

### License/Terms of Use:

MIT

## Use Case:

Beachgoers and their assistants use this skill to check waves, wind, UV exposure, rip-current risk, and advisory swimming conditions for a named beach or location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Beach names and coordinates are sent to third-party geocoding and weather services.

Mitigation: Share only locations you are comfortable sending to public services.

Risk: The advisory safety score may not reflect current local hazards.

Mitigation: Check lifeguard guidance and official beach warnings before entering the water.

Risk: Unpinned dependencies may change behavior after installation.

Mitigation: Consider pinning and reviewing dependencies before operational use.

## Reference(s):

- [Beach Safety on ClawHub](https://clawhub.ai/evanfoglia/skills/beach-safety)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain-text report or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a 1–10 advisory safety score, conditions and recommendations; NOAA surf-zone detail is primarily available for US coasts.]

## Skill Version(s):

1.1.4 (source: ClawHub release metadata; bundled SKILL.md lists 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
