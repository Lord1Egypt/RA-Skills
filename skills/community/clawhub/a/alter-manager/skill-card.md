## Description: <br>
Alter Manager helps an OpenClaw agent create, list, delete, and route messages to independent sub-sessions for parallel task handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnluicn](https://clawhub.ai/user/johnluicn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage separate OpenClaw sub-sessions for independent tasks, including creating labeled sessions, listing active sessions, deleting sessions after confirmation, and routing follow-up messages to a selected session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may delete the wrong sub-session if labels or session keys are confused. <br>
Mitigation: Ask for confirmation and verify the exact label or session key before deletion. <br>
Risk: Normal messages may continue routing to a selected sub-session while route mode is active. <br>
Mitigation: Make route state visible when entering or starting a session, and exit route mode before unrelated work. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/johnluicn/alter-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline command and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a workspace route-state JSON file and may direct session-management actions through OpenClaw session tools or CLI commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
