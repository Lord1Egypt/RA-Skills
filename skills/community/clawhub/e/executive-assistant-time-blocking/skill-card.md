## Description: <br>
Standard Operating Procedure (SOP) that acts as an executive assistant to block out calendar time using TS atomic plugins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or assistants use this skill to collect incomplete Google Tasks, identify open calendar gaps, and schedule time blocks while auditing for overlaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create calendar events, which may place tasks at incorrect times or with unsuitable durations. <br>
Mitigation: Require a proposed schedule preview and explicit user confirmation before creating calendar events. <br>
Risk: The workflow includes calendar deletion during overlap resolution, which could remove events beyond the intended scheduling changes. <br>
Mitigation: Allow deletion only for events the workflow created or events the user specifically named. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/executive-assistant-time-blocking) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with scheduling commands and calendar action confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes scheduled tasks, timeline placement, and overlap-free scheduling status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
