## Description: <br>
钉钉日报自动提交工具 - 定时自动提交工作日报到钉钉日志系统，适用于每日工作汇报自动化、定时提交日报、钉钉日志集成等场景，并支持 Python 导入和命令行两种方式使用，可自定义接收人列表和定时任务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[519989179](https://clawhub.ai/user/519989179) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to automate DingTalk daily report submission, including preparing report content, configuring recipients, and setting up scheduled or manual submission workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic report submission can send work content to DingTalk recipients without further review. <br>
Mitigation: Confirm the recipient list and report content source before enabling scheduled submission. <br>
Risk: DingTalk AppKey and AppSecret values may be exposed if configuration files are shared. <br>
Mitigation: Keep DingTalk credentials out of shared files and replace placeholder values with locally managed secrets. <br>
Risk: The artifact describes submit_log.py and cron setup, but those implementation files are not included for review. <br>
Mitigation: Inspect the actual submit_log.py and cron configuration before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/519989179/daily-dd-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes DingTalk application credential placeholders, receiver configuration examples, and cron scheduling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog dated 2026-03-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
