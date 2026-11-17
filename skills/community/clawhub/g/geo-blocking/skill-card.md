## Description:

Implement geographic content restrictions with IP geolocation, VPN/Tor detection, and regional law compliance for tailored geo-blocking rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi)

### License/Terms of Use:


## Use Case:

Developers and compliance teams use this skill to plan country-based content filtering, regional restrictions, VPN/proxy and Tor detection, and geo-specific compliance controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install an unaudited, unpinned npm package that is not included in the artifact.

Mitigation: Review the npm package source and provenance before installing, pin an exact reviewed version with lockfile or integrity metadata, and test first in an isolated environment without unnecessary secrets.

Risk: Geo-blocking behavior may involve IP addresses, VPN/proxy checks, and Tor detection results.

Mitigation: Confirm how these signals are transmitted, stored, and retained before deploying the package in environments that process user traffic.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raghulpasupathi/skills/geo-blocking)
- [Publisher profile](https://clawhub.ai/user/raghulpasupathi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference an external npm package that should be reviewed and pinned before installation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
