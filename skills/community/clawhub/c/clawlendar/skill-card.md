## Description: <br>
Timestamp-first perpetual calendar interop for AI agents that need cross-calendar conversion, timestamp timeline normalization, true month boundaries, and day-level calendar or almanac payloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hosuke](https://clawhub.ai/user/Hosuke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to normalize dates and timestamps across Gregorian, Julian, ISO, ROC, Buddhist, Japanese era, sexagenary, solar-term, and optional lunar calendar systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the skill requires trusting an external Python package. <br>
Mitigation: Pin the package version in sensitive environments, install in an isolated environment, review the package before deployment, and avoid running setup with elevated privileges. <br>
Risk: The optional HTTP or MCP server can expose calendar-conversion tools to clients that can reach it. <br>
Mitigation: Expose the server only to trusted local clients unless access controls and network restrictions are added. <br>
Risk: Some calendar, solar-term, lunar, or almanac outputs may be approximate or depend on optional providers. <br>
Mitigation: Call capabilities first, inspect warnings or approximation markers, and verify critical scheduling or compliance dates against authoritative calendar sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Hosuke/clawlendar) <br>
- [Clawlendar Homepage](https://github.com/Hosuke/Clawlender) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request or response payload conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward MCP tools, CLI commands, and HTTP endpoints that return normalized JSON calendar payloads and warnings for optional or approximate providers.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
