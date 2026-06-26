## Description: <br>
Recognizes and resolves Chinese and English time expressions to exact dates and queries Chinese public holidays and weekends by date range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youngfreefjs](https://clawhub.ai/user/youngfreefjs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to resolve relative time expressions in Chinese or English and to produce date-aware holiday and weekend summaries for scheduling conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or running the referenced PyPI package executes local code. <br>
Mitigation: Use a virtual environment, consider pinning the package version, and install only after reviewing the package to the level required for the deployment. <br>
Risk: The trigger wording is broad enough to activate on casual weekday, holiday, or date mentions. <br>
Mitigation: Configure activation only for user requests that need date resolution or holiday lookup. <br>
Risk: Holiday schedules can change because official calendars and workday adjustments may be updated. <br>
Mitigation: Use the skill output as calendar assistance and verify high-impact scheduling decisions against an authoritative holiday calendar. <br>


## Reference(s): <br>
- [Fcalendar Skill on ClawHub](https://clawhub.ai/youngfreefjs/fcalendar-skill) <br>
- [fcalendar PyPI package](https://pypi.org/project/fcalendar/) <br>
- [Chinese Holidays and Solar Terms Reference](references/holidays.md) <br>
- [Time Expression Types Reference](references/time-expressions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses derived from CLI JSON results, with shell command examples when setup or verification is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI emits single-line JSON; agents should present returned result fields without semantic rewriting.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
