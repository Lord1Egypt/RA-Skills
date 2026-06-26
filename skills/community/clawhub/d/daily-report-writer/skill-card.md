## Description: <br>
Generates a daily report Markdown draft from provided input and writes it to the reports directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoiFG](https://clawhub.ai/user/JoiFG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and team members use this skill to draft daily work reports from a date, required highlights, and optional blockers, then save the Markdown report under reports/. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a local Markdown report file in the reports directory, so repeated use with the same date may affect an existing report. <br>
Mitigation: Check whether reports/{{date}}-daily-report.md already exists before invoking the skill. <br>
Risk: Daily reports may contain sensitive work details that are persisted in the workspace. <br>
Mitigation: Avoid including sensitive information unless it is appropriate to store it locally in the workspace. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report file with structured status, summary, data, and nextAction response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates reports/{{date}}-daily-report.md using the provided date.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
