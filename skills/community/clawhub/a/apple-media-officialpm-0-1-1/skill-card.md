## Description: <br>
Discover and control Apple media/AirPlay devices (HomePod, Apple TV, AirPlay speakers) from macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DurtyDhiana](https://clawhub.ai/user/DurtyDhiana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS automation users use this skill to discover local Apple TVs, HomePods, and AirPlay speakers, map device names to IPs or IDs, and control playback, connection, and volume through pyatv and Airfoil workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local network scans and JSON summaries can expose device names, IP addresses, identifiers, and service metadata. <br>
Mitigation: Run scans only on trusted networks, avoid committing scan outputs, and review generated JSON before sharing it. <br>
Risk: Speaker and Apple TV control may require pairing, credentials, or macOS Accessibility permissions. <br>
Mitigation: Grant permissions deliberately on trusted hosts and confirm the target device before running control or volume commands. <br>
Risk: The workflow depends on pyatv, Airfoil, and a referenced Airfoil skill for device control. <br>
Mitigation: Review installed dependencies and the referenced Airfoil skill before deployment or execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/DurtyDhiana/apple-media-officialpm-0-1-1) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime scan output may include local device names, IP addresses, identifiers, and service metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
