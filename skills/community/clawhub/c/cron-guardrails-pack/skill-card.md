## Description: <br>
Lint cron entries for schedule validity, bad model names, and missing NO_REPLY discipline markers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Highlander89](https://clawhub.ai/user/Highlander89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations engineers use this skill to lint cron definitions, catch malformed schedules, reject known bad model names, and check notification jobs for explicit NO_REPLY discipline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron lint results may miss context-specific operational requirements or flag entries that need human judgment. <br>
Mitigation: Review the cron file and lint findings before changing schedules or notification behavior. <br>
Risk: Cron files may contain sensitive operational details even when the skill itself does not handle secrets. <br>
Mitigation: Use appropriate local files and avoid sharing sensitive cron contents in untrusted environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and cron lint findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports OK, FAIL with issue lines, or usage/read errors via exit codes 0, 1, and 2.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
