## Description: <br>
Discover and control Apple media/AirPlay devices (HomePod, Apple TV, AirPlay speakers) from macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[officialpm](https://clawhub.ai/user/officialpm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users on macOS use this skill to discover local Apple/AirPlay media devices, map device names to network identifiers, connect speakers, and control playback or volume through pyatv and Airfoil. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local network scans and JSON summaries can reveal private device names, IP addresses, identifiers, and service details. <br>
Mitigation: Run scans only on networks and devices you own or are authorized to manage, and avoid storing or sharing scan outputs. <br>
Risk: The skill can control Apple/AirPlay devices through pyatv, Airfoil, and sibling Airfoil scripts. <br>
Mitigation: Verify pyatv, Airfoil, and the referenced Airfoil skill before granting permissions or issuing control commands. <br>


## Reference(s): <br>
- [Apple Media ClawHub listing](https://clawhub.ai/officialpm/apple-media-officialpm) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON scan summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local network scan results that include device names, IP addresses, identifiers, and service details.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and changelog, released 2026-01-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
