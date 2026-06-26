## Description: <br>
Automatically write daily, weekly, and monthly diary summaries and extract insights to auto-learn.md for HexaLoop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcjl](https://clawhub.ai/user/0xcjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate bilingual daily, weekly, and monthly diary summaries from workspace memory, extract reusable insights into auto-learn.md, and send diary cards to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can summarize private OpenClaw workspace memory and post diary content to a fixed Feishu chat on a schedule. <br>
Mitigation: Install only when the Feishu chat ID belongs to the user, make delivery configurable or disable it before cron use, and periodically review diary and auto-learn outputs for sensitive content. <br>


## Reference(s): <br>
- [Diary template](templates/diary_template.md) <br>
- [ClawHub skill page](https://clawhub.ai/0xcjl/auto-diary-0xcjl) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Configuration, Shell commands] <br>
**Output Format:** [Markdown diary and review files, extracted insight text, Feishu interactive card JSON, and cron setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes diary files under the OpenClaw workspace memory directory and appends extracted insights to auto-learn.md.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
