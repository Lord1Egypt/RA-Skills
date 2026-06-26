## Description: <br>
深度解析长周期、多参与方、多线程的邮件往来记录。当用户发送 .eml 文件或粘贴邮件正文时自动触发。自动过滤社交辞令，梳理事件演进，定位决策点，清晰呈现各方执行动作与遗留事项。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinsuzc](https://clawhub.ai/user/kevinsuzc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Project managers, operations teams, and account teams use this skill to turn long, multi-party email threads into structured chronology, responsibility, decision, risk, and next-action reports. It is especially suited to pasted email bodies or .eml files that need MIME cleanup before analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Preprocessed email content can contain confidential or personal information and may be written to a temporary local file. <br>
Mitigation: Process only intended .eml files, restrict access to generated temporary files, and delete /tmp/eml_cleaned.txt after analysis when it is no longer needed. <br>
Risk: Email chronology and responsibility analysis may influence follow-up actions even when source emails are incomplete or ambiguous. <br>
Mitigation: Review the generated report against the original email record before relying on assignments, deadlines, or escalation recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kevinsuzc/email-chronicle-analyst) <br>
- [Publisher profile](https://clawhub.ai/user/kevinsuzc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with structured sections and optional preprocessing command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May preprocess .eml input into cleaned text before producing an analysis report.] <br>

## Skill Version(s): <br>
4.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
