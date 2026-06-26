## Description: <br>
Query and track health indicators from the CareMax Health API, including saved metrics, lab trends, categories, and quick logging of everyday vitals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kittenyang](https://clawhub.ai/user/kittenyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CareMax users and their agents use this skill to review health indicators, inspect trends and abnormal values, and log a single authenticated reading for the selected profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and write sensitive health indicator records through external authentication scripts. <br>
Mitigation: Install only when the CareMax auth scripts are trusted, verify token storage and revocation, and confirm the target profile before accessing or saving records. <br>
Risk: A quick-log action could save an incorrect value, unit, date, or family profile. <br>
Mitigation: List available presets first and require user confirmation of the value, unit, date, and profile before saving a reading. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kittenyang/caremax-indicators) <br>
- [Publisher profile](https://clawhub.ai/user/kittenyang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and health indicator summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dates, units, reference ranges, abnormal flags, and confirmation text for saved readings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
