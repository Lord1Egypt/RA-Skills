## Description:

Check air quality, AQI, PM2.5, PM10, and pollution levels for any city from the terminal using the airq CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunto2](https://clawhub.ai/user/fortunto2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install, configure, and run the airq CLI for city-level air quality checks, pollution trends, sensor comparison, source attribution, reports, and JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented Linux install path downloads the latest remote binary and moves it into /usr/local/bin with sudo.

Mitigation: Review install commands before use, prefer a pinned version, verify upstream checksums or signatures, and install to a user-local directory when possible.

Risk: The skill can create configuration and cache/report files that may reveal location history or air-quality report contents.

Mitigation: Review and clear ~/.config/airq and ~/.cache/airq as needed, especially on shared or managed machines.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, JSON]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local config in ~/.config/airq and cache/report data in ~/.cache/airq.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
