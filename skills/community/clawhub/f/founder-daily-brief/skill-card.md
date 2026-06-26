## Description: <br>
Generate a personalized daily briefing for startup founders that combines tasks, meetings, industry news, competitor updates, and priorities into a structured brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wulaosiji](https://clawhub.ai/user/wulaosiji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Startup founders and operators use this skill to turn daily inputs such as schedules, tasks, company stage, news items, competitor updates, and metrics into a focused morning brief. It supports planning, prioritization, and quick scanning in English or Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Founder brief inputs may include confidential company information, credentials, regulated personal data, or raw calendar details. <br>
Mitigation: Use summaries instead of sensitive raw data and avoid pasting credentials, regulated personal data, or confidential details unless the execution environment is appropriate. <br>
Risk: The bundled script writes generated Founder_Brief markdown files to the selected output path or current working directory. <br>
Mitigation: Run the skill in a folder where creating briefing markdown files is expected and review the output path before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wulaosiji/founder-daily-brief) <br>
- [UniqueClub](https://uniqueclub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown brief with optional command-line usage and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Founder_Brief markdown files in the current working directory when the bundled script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
