## Description: <br>
Chinese holiday and adjusted-workday reminder skill with a relationship assistant for anniversaries, birthdays, custom dates, and romantic holiday reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ironmanc2014](https://clawhub.ai/user/ironmanc2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to answer China holiday, workday, and upcoming holiday questions, and to configure automated reminders for holidays, anniversaries, birthdays, and custom relationship dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relationship names, anniversaries, birthdays, and custom dates may be stored locally and reminders may be sent through Feishu if configured. <br>
Mitigation: Install only when local storage of these details is acceptable, and use a private Feishu destination or a local/private notification path for relationship reminders. <br>
Risk: Some holiday data is marked as predicted until official schedules are updated. <br>
Mitigation: Review predicted holiday and adjusted-workday results before relying on them for scheduling decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ironmanc2014/cn-holiday-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples, plain text reminders, JSON command output, and cron configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads built-in holiday data and may read or write local relationship reminder data under ~/agent-memory/love.json.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
