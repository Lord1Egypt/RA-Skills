## Description: <br>
Turn scattered notes, chat logs, meeting fragments, issue updates, or calendar context into a concise daily brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuweikang](https://clawhub.ai/user/wuweikang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, and developers use this skill to convert raw daily notes, chat logs, issue updates, meeting fragments, and calendar context into a concise status brief with priorities, blockers, and next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive notes, calendar details, chat logs, or meeting fragments supplied by a user. <br>
Mitigation: Only provide source material that is appropriate for the active AI assistant to process, and remove confidential details that are not needed for the brief. <br>
Risk: A generated brief could imply commitments, owners, dates, or metrics that were not present in the source material. <br>
Mitigation: Keep facts traceable to the provided notes and mark missing or inferred context explicitly before sharing the brief. <br>


## Reference(s): <br>
- [Daily Brief Format](references/brief-format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wuweikang/daily-brief-writer) <br>
- [Publisher Profile](https://clawhub.ai/user/wuweikang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown daily brief with optional Slack/chat or email-ready variants] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to a headline plus Done today, In progress, Blockers / risks, and Next actions sections; shorter channel-specific variants may omit empty sections.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
