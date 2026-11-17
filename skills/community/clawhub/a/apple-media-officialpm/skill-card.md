## Description:

Discover and control Apple media and AirPlay devices, including HomePod, Apple TV, and AirPlay speakers, from macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[officialpm](https://clawhub.ai/user/officialpm)

### License/Terms of Use:


## Use Case:

Developers and technical users use this skill to discover local AirPlay and Apple media devices, map names to IP addresses or identifiers, and issue playback, connection, and volume commands through pyatv and Airfoil.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs local-network discovery and control of Apple and AirPlay devices, which can expose device names, IP addresses, identifiers, and service metadata at runtime.

Mitigation: Run scans only on networks and devices you are authorized to discover or control, and avoid committing scan output.

Risk: The skill depends on third-party tools, including pyatv and Airfoil, for installation and device control.

Mitigation: Confirm the dependencies are trusted before installing and consider pinning pyatv to a reviewed version.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON scan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local network scan output containing device names, IP addresses, models, identifiers, and service metadata.]

## Skill Version(s):

0.1.1 (source: server release metadata and changelog, released 2026-01-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
