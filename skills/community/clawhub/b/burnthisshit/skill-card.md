## Description: <br>
Forensically obliterate an OpenClaw session and all its traces -- transcript, trajectory, bak files, deleted archives, and sessions.json entry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genortg](https://clawhub.ai/user/genortg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to direct an agent to securely remove local OpenClaw session records and associated session index entries when intentional, irreversible cleanup is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can permanently erase OpenClaw session records and related files. <br>
Mitigation: Install and invoke it only when intentional irreversible cleanup is required, and use specific session IDs. <br>
Risk: The skill instructions tell the agent to run the cleanup immediately and may bypass the script's interactive confirmation by using --force. <br>
Mitigation: Avoid --force unless the target session and files have already been reviewed, and do not rely on this skill where auditability or recovery matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/genortg/burnthisshit) <br>
- [Publisher Profile](https://clawhub.ai/user/genortg) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute irreversible local file deletion when invoked with a valid OpenClaw session ID.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
