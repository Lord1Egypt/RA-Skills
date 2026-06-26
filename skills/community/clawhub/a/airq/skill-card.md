## Description: <br>
Check air quality, AQI, PM2.5, PM10, pollution levels for any city from the terminal using airq CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install, configure, and run the airq CLI for air-quality checks, pollution monitoring, source comparison, history, rankings, and reports for cities or coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Linux installation path moves a downloaded binary into a system-wide location with sudo. <br>
Mitigation: Prefer Homebrew or cargo where practical, pin a specific release, verify checksums or signatures if available, and avoid installing the binary system-wide unless the upstream project is trusted. <br>
Risk: Air-quality queries and reports may contact external data and map services with user-provided locations. <br>
Mitigation: Use only locations the user is comfortable sharing with external services and review generated reports before distributing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fortunto2/airq) <br>
- [Linux release archive referenced by the skill](https://github.com/fortunto2/airq/releases/latest/download/airq-linux-x86_64.tar.gz) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local configuration files and reports through the airq CLI.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
