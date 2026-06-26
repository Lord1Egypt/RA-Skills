## Description: <br>
采集市场和新闻数据，生成每日金融 Word 日报与 PPT 简报，并在完成后通过邮件发送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szrw1825](https://clawhub.ai/user/szrw1825) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial-reporting users and agents use this skill to orchestrate market data collection, Word report creation, PPT briefing creation, and email delivery for a daily financial report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad natural-language trigger can start a workflow that collects market/news data, creates files, and sends results externally by email. <br>
Mitigation: Confirm the trigger intent, trusted local configuration, companion skills, and email recipients before running the skill. <br>
Risk: The workflow depends on companion skills and local configuration paths that are outside this artifact. <br>
Mitigation: Review the referenced companion skills and local config before deployment, especially data sources, output directories, Python interpreter settings, and mail delivery settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szrw1825/daily-financial-report) <br>
- [Publisher profile](https://clawhub.ai/user/szrw1825) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with referenced Python scripts and generated report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates companion skills that produce JSON market data, Word documents, PPT briefings, logs, and outbound email.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
