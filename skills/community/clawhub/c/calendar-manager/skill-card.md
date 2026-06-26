## Description: <br>
Calendar Manager helps an agent read calendar events, create or update events, set reminders, and summarize upcoming schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jackeven02](https://clawhub.ai/user/Jackeven02) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and individual users can use this skill to ask an agent about upcoming events, add calendar entries, find free time, and prepare reminders through supported calendar tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private calendar data and local calendar credentials. <br>
Mitigation: Install only when the user is comfortable giving the agent calendar access, and keep credentials scoped to the intended calendar account. <br>
Risk: The skill describes creating, modifying, deleting, importing, emailing, and scheduling reminder workflows without clear approval boundaries. <br>
Mitigation: Require explicit user confirmation before calendar changes, email-derived imports, reminder emails, or scheduled reminder jobs are run. <br>


## Reference(s): <br>
- [Calendar management resources](references/resources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown or plain text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include private calendar details; calendar actions depend on user-authorized local tools and credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
