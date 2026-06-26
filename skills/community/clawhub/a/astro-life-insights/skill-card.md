## Description: <br>
Personalized daily astrological insights focused on relationships, work, personal growth, and luck. Positive framing only. Uses your natal chart + astronomy-engine transits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unicoleunicron](https://clawhub.ai/user/unicoleunicron) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure a local natal chart and generate daily astrology-themed insights for relationships, work, personal growth, and luck. It can produce human-readable readings or structured JSON for dashboards and automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores birth date, birth time, and birthplace in a local JSON file at ~/.config/astro-life-insights/natal-chart.json. <br>
Mitigation: Install only if local storage of this data is acceptable; protect the local account and backups, and remove the file when the configuration is no longer needed. <br>
Risk: The documented upcoming.js command appears to be missing from this version. <br>
Mitigation: Use the reviewed daily.js and daily-json.js commands, or verify that an upcoming.js file is present before relying on upcoming-transit functionality. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/unicoleunicron/astro-life-insights) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Console text or structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local birth date, birth time, and birthplace configuration before producing personalized output.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
