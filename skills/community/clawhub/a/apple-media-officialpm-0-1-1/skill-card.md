## Description:

Discover and control Apple media and AirPlay devices from macOS, including scanning for HomePod, Apple TV, and AirPlay speakers, mapping names to IPs/IDs, and using pyatv and Airfoil for playback and volume workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durtydhiana](https://clawhub.ai/user/durtydhiana)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to discover local Apple media devices, identify device addresses and IDs, and run guided pyatv or Airfoil commands for playback, routing, and volume control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local network scans can expose private device names, IP addresses, identifiers, services, and credential-related fields.

Mitigation: Run scans only on authorized networks and do not commit or share scan outputs containing local network inventory.

Risk: The workflow relies on third-party local tooling installed through pipx or Homebrew.

Mitigation: Install dependencies from trusted sources and pin, review, or approve dependency versions according to deployment policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/durtydhiana/skills/apple-media-officialpm-0-1-1)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON scan summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime scan output may include local device names, IP addresses, identifiers, services, and credential-related fields.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog lists 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
