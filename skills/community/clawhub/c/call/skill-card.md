## Description: <br>
Call is a local call-management skill that prepares for calls, captures key points and decisions, tracks commitments, drafts follow-ups, and builds conversation history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenticio](https://clawhub.ai/user/agenticio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to prepare for phone calls or meetings, capture decisions and commitments, track follow-ups, and draft follow-up messages while keeping call data local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive local call history under broad activation wording. <br>
Mitigation: Install only if agent access to local call notes is acceptable; use explicit call-preparation or follow-up requests and review or clear stored records that contain sensitive business or personal information. <br>
Risk: Call records may contain private commitments, contact history, and follow-up details. <br>
Mitigation: Keep records local, avoid sharing conversation data unless intentionally exported, and apply the user's retention and deletion choices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agenticio/call) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and plain text with occasional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local call-management JSON files under memory/calls when workflows are invoked.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
